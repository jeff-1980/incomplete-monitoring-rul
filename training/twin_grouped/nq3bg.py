"""Q3 confirmation on N-CMAPSS DS01+DS02 (PREREG_Q3_NCMAPSS_2026-11-15.md). Usage: python3 nq3.py seed"""
import sys, json, numpy as np, cm
seed = int(sys.argv[1])
W, KMAX, LONG = 10, 5, 50
z = np.load('ncm_cycles.npz')
units = sorted({k.rsplit('_', 2)[0] + '_' + k.rsplit('_', 2)[1] for k in z.files if k.endswith('_X')})
D = {}
for k in z.files:
    if k.endswith('_X'): D[k.rsplit('_', 2)[0]] = (z[k], np.minimum(z[k[:-2] + '_y'], cm.CAP))
names = sorted(D)


def win_from_obs(Z, idx, n, dt):
    X = Z[idx]; g = np.r_[0, np.diff(idx)].astype(np.float32)
    if len(X) < n: X = np.concatenate([np.repeat(X[:1], n - len(X), 0), X]); g = np.r_[np.zeros(n - len(g), np.float32), g]
    X, g = X[-n:], g[-n:]
    return np.concatenate([X, g[:, None] / KMAX], 1) if dt else X


def interp_grid(Z, idx, n):
    grid = np.arange(idx[0], idx[-1] + 1)
    G = np.stack([np.interp(grid, idx, Z[idx, j]) for j in range(Z.shape[1])], 1).astype(np.float32)
    return win_from_obs(G, np.arange(len(G)), n, False)


def locf_grid(Z, idx, n):
    grid = np.arange(idx[0], idx[-1] + 1); pos = np.searchsorted(idx, grid, side='right') - 1
    return win_from_obs(Z[idx][pos], np.arange(len(grid)), n, False)


def back_idx(t, gaps):
    idx = [t]
    for g in gaps:
        if idx[-1] - g < 0: break
        idx.append(idx[-1] - g)
    return np.array(idx[::-1])


def build(Zs, ys, kind, rng, k=1):
    Xs, Ys = [], []
    for Z, y in zip(Zs, ys):
        for t in range(len(Z)):
            if kind == 'dense': x = win_from_obs(Z, np.arange(max(0, t - W + 1), t + 1), W, False)
            elif kind == 'long': x = win_from_obs(Z, np.arange(max(0, t - LONG + 1), t + 1), LONG, False)
            elif kind == 'matched': x = win_from_obs(Z, back_idx(t, np.full(W, k)), W, False)
            else:
                g = np.full(W, rng.integers(1, KMAX + 1)) if rng.random() < 0.5 else rng.integers(1, KMAX + 1, W)
                x = win_from_obs(Z, back_idx(t, g), W, kind == 'mixdt')
            Xs.append(x); Ys.append(y[t])
    return np.stack(Xs).astype(np.float32), np.array(Ys, np.float32)


def stream(T, sc, fold):
    if sc == 'k1': return np.arange(T)
    if sc == 'k5': return np.arange(0, T, 5)
    g = np.random.default_rng(1000 + fold).integers(1, KMAX + 1, T); return np.cumsum(np.r_[0, g])[lambda c: c < T] if False else (lambda c: c[c < T])(np.cumsum(np.r_[0, g]))



import torch, torch.nn as nn
dev = cm.dev
class GRUD(nn.Module):
    """GRU-D with full observations: input decay toward the training mean and hidden-state decay, both driven by delta"""
    def __init__(s, d, h=64):
        super().__init__(); s.d, s.h = d, h
        s.gx = nn.Linear(1, d); s.gh = nn.Linear(1, h); s.cell = nn.GRUCell(2 * d + 1, h)
        s.head = nn.Sequential(nn.Linear(h, 32), nn.ReLU(), nn.Linear(32, 1)); s.register_buffer('mu', torch.zeros(d))

    def forward(s, x):           # x: B x T x (d+1), last channel = delta / KMAX
        v, dl = x[..., :-1], x[..., -1:]; B, T, _ = v.shape; h = torch.zeros(B, s.h, device=x.device); prev = v[:, 0]
        for t in range(T):
            gx = torch.exp(-torch.relu(s.gx(dl[:, t]))); gh = torch.exp(-torch.relu(s.gh(dl[:, t])))
            xin = v[:, t]                                    # all sensors observed at an observation time (mask = 1)
            xdec = gx * prev + (1 - gx) * s.mu               # decayed last value (used as extra input, GRU-D style)
            h = s.cell(torch.cat([xin, xdec, dl[:, t]], 1), gh * h); prev = xin
        return s.head(h).squeeze(-1)




def train_any(model, X, Y, epochs=30, bs=256):
    torch.manual_seed(seed); X = torch.tensor(X).to(dev); Y = torch.tensor(Y / cm.CAP).to(dev); model.to(dev)
    opt = torch.optim.Adam(model.parameters(), 1e-3); n = len(X)
    for ep in range(epochs):
        for i in range(max(30, n // bs)):
            j = torch.randint(0, n, (bs,), device=dev); loss = ((model(X[j]) - Y[j]) ** 2).mean()
            opt.zero_grad(); loss.backward(); opt.step()
    return model


def build8(Zs, ys, rng):
    Xs, Ys = [], []
    for Z, y in zip(Zs, ys):
        for t in range(len(Z)):
            g = np.full(W, rng.integers(1, KMAX + 1)) if rng.random() < 0.5 else rng.integers(1, KMAX + 1, W)
            Xs.append(interp_grid(Z, back_idx(t, g), LONG)); Ys.append(y[t])
    return np.stack(Xs).astype(np.float32), np.array(Ys, np.float32)


res = {}
GRP = {n: n.split('_')[1] for n in names if n.split('_')[1] in ('u2', 'u5', 'u10')}   # DS01/DS02 twins share unit id
GROUPS = []
for n in names:
    g = GRP.get(n, n)
    if g not in [x[0] for x in GROUPS]: GROUPS.append((g, []))
    [x[1] for x in GROUPS if x[0] == g][0].append(n)

for gi, (gname, members) in enumerate(GROUPS):
    rng = np.random.default_rng(seed * 100 + gi)
    trn = [n for n in names if n not in members]
    A = np.concatenate([D[n][0] for n in trn]); mu, sd = A.mean(0), A.std(0) + 1e-6
    Zs = [(D[n][0] - mu) / sd for n in trn]; ys = [D[n][1] for n in trn]
    X5, Y5 = build(Zs, ys, 'mixdt', rng); a5 = cm.train(X5, Y5, seed)
    g = GRUD(X5.shape[-1] - 1); g.mu.copy_(torch.tensor(np.concatenate(Zs).mean(0).astype(np.float32))); g = train_any(g, X5, Y5)
    X8, Y8 = build8(Zs, ys, rng); a8 = cm.train(X8, Y8, seed)
    for te in members:
        fold = names.index(te)
        Zt, yt = (D[te][0] - mu) / sd, D[te][1]; T = len(Zt); res[te] = {}
        for sc in ('k1', 'k5', 'irr5'):
            obs = stream(T, sc, fold); pts = [j for j in range(len(obs)) if obs[j] >= 10]
            I = [obs[:j + 1] for j in pts]; y = yt[obs[pts]]
            Xa = np.stack([win_from_obs(Zt, i, W, True) for i in I]); g.eval()
            with torch.no_grad(): pg = g(torch.tensor(Xa).to(dev)).cpu().numpy() * cm.CAP
            P = {'A5': cm.predict(a5, Xa), 'B1_GRUD': pg, 'A8': cm.predict(a8, np.stack([interp_grid(Zt, i, LONG) for i in I]))}
            res[te][sc] = {a: cm.rmse(p - y) for a, p in P.items()}
        print(seed, te, res[te], flush=True)
json.dump(res, open(f'results/nq3bg_s{seed}.json', 'w'))
