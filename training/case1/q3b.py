"""Q3 strong baselines under the pre-registered sparse protocol (C-MAPSS). Usage: python3 q3b.py FD001 seed
B1 GRU-D (Che et al. 2018) trained on the same mixed-interval windows as A5 (input = values, mask = 1, delta = gap)
B2 GAIN imputation (Yoon et al. 2018) of the every-cycle 30-cycle grid + the dense GRU (two-stage, MIGGAN-style)
A5 re-run (same run, reference)."""
import sys, json, numpy as np, torch, torch.nn as nn, cm
from q3lib import obs_idx, win_from_obs, mixed_gaps, SCEN, test_gaps, W, KMAX
import os; EP = int(os.environ.get("EP", 30))
fd, seed = sys.argv[1], int(sys.argv[2]); rng = np.random.default_rng(seed); dev = cm.dev


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


def train_any(model, X, Y, epochs=None, bs=256):
    epochs = epochs or EP; torch.manual_seed(seed); X = torch.tensor(X).to(dev); Y = torch.tensor(Y / cm.CAP).to(dev); model.to(dev)
    opt = torch.optim.Adam(model.parameters(), 1e-3); n = len(X)
    for ep in range(epochs):
        for i in range(max(30, n // bs)):
            j = torch.randint(0, n, (bs,), device=dev); loss = ((model(X[j]) - Y[j]) ** 2).mean()
            opt.zero_grad(); loss.backward(); opt.step()
    return model


class GAIN(nn.Module):
    """generator + discriminator on flattened 30 x d grids; rows are missing (whole snapshots)"""
    def __init__(s, d):
        super().__init__(); n = W * d; s.d = d
        s.G = nn.Sequential(nn.Linear(2 * n, n), nn.ReLU(), nn.Linear(n, n), nn.ReLU(), nn.Linear(n, n))
        s.D = nn.Sequential(nn.Linear(2 * n, n), nn.ReLU(), nn.Linear(n, n), nn.ReLU(), nn.Linear(n, n))

    def impute(s, x, m):
        z = torch.randn_like(x) * 0.01; xt = m * x + (1 - m) * z
        g = s.G(torch.cat([xt, m], 1)); return m * x + (1 - m) * g, g


def row_mask(r):
    """mask of the last W cycles produced by a random interval pattern (same law as mixed training)"""
    idx = obs_idx(W, mixed_gaps(r)); m = np.zeros(W, np.float32); m[idx] = 1; return m


def train_gain(Xd, epochs=None, bs=256, alpha=10.0, hint=0.9):
    epochs = epochs or EP; torch.manual_seed(seed); n, T, d = Xd.shape; X = torch.tensor(Xd.reshape(n, -1)).to(dev)
    M = torch.tensor(np.stack([np.repeat(row_mask(rng), d) for _ in range(n)])).to(dev)
    net = GAIN(d).to(dev); og = torch.optim.Adam(net.G.parameters(), 1e-3); od = torch.optim.Adam(net.D.parameters(), 1e-3)
    for ep in range(epochs):
        for i in range(max(30, n // bs)):
            j = torch.randint(0, n, (bs,), device=dev); x, m = X[j], M[j]
            H = m * (torch.rand_like(m) < hint).float() + 0.5 * (torch.rand_like(m) >= hint).float()
            xh, g = net.impute(x, m); dp = torch.sigmoid(net.D(torch.cat([xh.detach(), H], 1)))
            ld = -(m * torch.log(dp + 1e-8) + (1 - m) * torch.log(1 - dp + 1e-8)).mean(); od.zero_grad(); ld.backward(); od.step()
            xh, g = net.impute(x, m); dp = torch.sigmoid(net.D(torch.cat([xh, H], 1)))
            lg = -((1 - m) * torch.log(dp + 1e-8)).mean() + alpha * ((m * (g - x)) ** 2).sum() / m.sum()
            og.zero_grad(); lg.backward(); og.step()
    return net


@torch.no_grad()
def gain_fill(net, Z, idx):
    """every-cycle grid of the last W cycles ending at idx[-1]; observed rows from idx, the rest imputed"""
    end = idx[-1]; cyc = np.arange(end - W + 1, end + 1); keep = cyc >= 0
    G = np.zeros((W, Z.shape[1]), np.float32); m = np.zeros((W, Z.shape[1]), np.float32)
    obs = set(idx.tolist())
    for r, c in enumerate(cyc):
        if c in obs: G[r] = Z[c]; m[r] = 1
    if not keep.all():                                       # history shorter than W: pad with the first observation
        G[~keep] = Z[idx[0]]; m[~keep] = 1
    x = torch.tensor(G.reshape(1, -1)).to(dev); mm = torch.tensor(m.reshape(1, -1)).to(dev)
    net.eval(); return net.impute(x, mm)[0].cpu().numpy().reshape(W, -1)


class Static(nn.Module):
    """B3 PSR-lite (after Cheng et al., IJCAI 2025): static regression on a single snapshot, no interpolation"""
    def __init__(s, d):
        super().__init__(); s.net = nn.Sequential(nn.Linear(d, 64), nn.ReLU(), nn.Linear(64, 64), nn.ReLU(), nn.Linear(64, 1))
    def forward(s, x): return s.net(x).squeeze(-1)


def rectify(c, yh, last=10):
    """parametric rectification with the labelling function RUL = F - t: average implied failure cycle F_i = c_i + yhat_i
    over the most recent (up to `last`) snapshots predicted in the linear (below-cap) region"""
    lin = yh < 0.95 * cm.CAP
    if not lin.any(): return float(yh[-1])
    F = (c[lin] + yh[lin])[-last:].mean(); return float(np.clip(F - c[-1], 0, cm.CAP))


def build(engines, nm, kind):
    Xs, Ys = [], []
    for e in engines.values():
        Z = nm(e); T = len(Z)
        for t in range(T):
            if kind == 'dense': x = win_from_obs(Z, np.arange(max(0, t - W + 1), t + 1), W, False)
            else: x = win_from_obs(Z, obs_idx(t + 1, mixed_gaps(rng)), W, True)
            Xs.append(x); Ys.append(min(T - 1 - t, cm.CAP))
    return np.stack(Xs).astype(np.float32), np.array(Ys, np.float32)


tr = cm.raw(fd, 'train'); nm = cm.Norm(tr); te = cm.raw(fd, 'test'); units = sorted(te); yt = np.minimum(cm.test_rul(fd), cm.CAP)
Xd, Yd = build(tr, nm, 'dense'); dense = cm.train(Xd, Yd, seed, epochs=EP); print(fd, seed, 'dense', flush=True)
Xm, Ym = build(tr, nm, 'mixdt'); a5 = cm.train(Xm, Ym, seed, epochs=EP); print(fd, seed, 'A5', flush=True)
grud = GRUD(Xm.shape[-1] - 1); grud.mu.copy_(torch.tensor(Xd.reshape(-1, Xd.shape[-1]).mean(0)))
grud = train_any(grud, Xm, Ym); print(fd, seed, 'GRU-D', flush=True)
gain = train_gain(Xd); print(fd, seed, 'GAIN', flush=True)
Xs = np.concatenate([nm(e) for e in tr.values()]); Ys = np.concatenate([np.minimum(len(e) - 1 - np.arange(len(e)), cm.CAP) for e in tr.values()]).astype(np.float32)
static = train_any(Static(Xs.shape[1]), Xs.astype(np.float32), Ys); print(fd, seed, 'static', flush=True)
out = {}
for sc in ('k1', 'k3', 'k5', 'irr5'):
    Zs = [nm(te[u]) for u in units]; I = [obs_idx(len(Z), test_gaps(sc, u)) for Z, u in zip(Zs, units)]
    Xa = np.stack([win_from_obs(Z, i, W, True) for Z, i in zip(Zs, I)])
    P = {'A5': cm.predict(a5, Xa)}
    grud.eval()
    with torch.no_grad(): P['B1_GRUD'] = grud(torch.tensor(Xa).to(dev)).cpu().numpy() * cm.CAP
    with torch.no_grad():
        P['B3_PSR'] = np.array([rectify(i.astype(float), static(torch.tensor(Z[i]).to(dev)).cpu().numpy() * cm.CAP) for Z, i in zip(Zs, I)])
    P['B2_GAIN'] = cm.predict(dense, np.stack([gain_fill(gain, Z, i) for Z, i in zip(Zs, I)]))
    out[sc] = {a: (p - yt).tolist() for a, p in P.items()}
    print(fd, seed, sc, ' '.join(f'{a} {cm.rmse(np.array(v)):.2f}' for a, v in out[sc].items()), flush=True)
json.dump(out, open(f'results/q3b_{fd}_s{seed}.json', 'w'))
