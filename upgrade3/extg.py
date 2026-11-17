"""Upgrade step 3 on the external cohort N-CMAPSS DS03-DS08 (PROTOCOL_upgrade3.md). Usage: python3 extg.py seed"""
import sys, json, os, numpy as np, cm
seed = int(sys.argv[1]); os.makedirs('results', exist_ok=True)
W, KMAX, LONG = 10, 5, 50; RS = (0.0, 0.25, 0.5, 0.75)
z = np.load('ncm_cycles_ds03_08.npz')
D = {k[:-2]: (z[k], np.minimum(z[k[:-2] + '_y'], cm.CAP)) for k in z.files if k.endswith('_X')}
EXCL_TEST = {'DS03_u10_test', 'DS03_u11_test', 'DS03_u14_test', 'DS03_u15_test', 'DS08a_u14_test'}; EXCL_TRAIN = {'DS03_u5_dev'}
TRAIN = sorted(n for n in D if n.endswith('_dev') and n not in EXCL_TRAIN); TEST = sorted(n for n in D if n.endswith('_test') and n not in EXCL_TEST)
prof = lambda u: ('DS05-07_' + u.split('_')[1]) if u.split('_')[0] in ('DS05', 'DS06', 'DS07') else u


def win_from_obs(Z, idx, n, dt):
    X = Z[idx]; g = np.r_[0, np.diff(idx)].astype(np.float32)
    if len(X) < n: X = np.concatenate([np.repeat(X[:1], n - len(X), 0), X]); g = np.r_[np.zeros(n - len(g), np.float32), g]
    X, g = X[-n:], g[-n:]
    return np.concatenate([X, g[:, None] / KMAX], 1).astype(np.float32) if dt else X.astype(np.float32)


def interp_grid(Z, idx, n):
    grid = np.arange(idx[0], idx[-1] + 1)
    G = np.stack([np.interp(grid, idx, Z[idx, j]) for j in range(Z.shape[1])], 1).astype(np.float32)
    return win_from_obs(G, np.arange(len(G)), n, False)


def back_idx(t, gaps):
    idx = [t]
    for g in gaps:
        if idx[-1] - g < 0: break
        idx.append(idx[-1] - g)
    return np.array(idx[::-1])


def smooth(X, m):
    if m <= 1: return X
    c = np.cumsum(np.concatenate([np.zeros((1, X.shape[1]), X.dtype), X]), 0); n = len(X); i = np.arange(n); lo = np.maximum(0, i - m + 1)
    return ((c[i + 1] - c[lo]) / (i + 1 - lo)[:, None]).astype(np.float32)


def build(names, mu, sd, kind, rng, r=0.0):
    Xs, Ys = [], []
    law = lambda n: np.full(n, rng.integers(1, KMAX + 1)) if rng.random() < 0.5 else rng.integers(1, KMAX + 1, n)
    for nme in names:
        Z = ((D[nme][0] - mu) / sd).astype(np.float32); y = D[nme][1]
        for t in range(len(Z)):
            lo = max(0, t - LONG + 1)
            if kind == 'A1': x = win_from_obs(Z, np.arange(max(0, t - W + 1), t + 1), W, False)
            elif kind == 'A6': x = win_from_obs(Z, np.arange(lo, t + 1), LONG, False)
            elif kind == 'A8F': x = interp_grid(Z, back_idx(t, law(LONG)), LONG)
            elif kind == 'GEN':
                p = 1.0 / rng.integers(1, KMAX + 1) if rng.random() < 0.5 else 1.0 / 3.0; keep = rng.random(t - lo) < p
                x = interp_grid(Z, np.r_[np.arange(lo, t)[keep], t].astype(int), LONG)
            elif kind == 'A6M':
                m = int(rng.integers(1, KMAX + 1)) if rng.random() < 0.5 else 3
                x = win_from_obs(smooth(Z[lo:t + 1], m), np.arange(t + 1 - lo), LONG, False)
            elif kind == 'A5R':
                g = np.ones(W, int) if rng.random() < r else law(W)
                x = win_from_obs(Z, back_idx(t, g), W, True)
            Xs.append(x); Ys.append(y[t])
    return np.stack(Xs).astype(np.float32), np.array(Ys, np.float32)


def stats(names):
    A = np.concatenate([D[n][0] for n in names]); return A.mean(0), A.std(0) + 1e-6


sel_file = 'results/selr_ext.json'
if not os.path.exists(sel_file):
    G = sorted(set(prof(u) for u in TRAIN)); gv = set(G[::5]); val = [n for n in TRAIN if prof(n) in gv]; trs = [n for n in TRAIN if prof(n) not in gv]; mu, sd = stats(trs); sc = {}
    Xv = {1: [], 5: []}; Yv = []
    for nme in val:
        Z = ((D[nme][0] - mu) / sd).astype(np.float32); y = D[nme][1]
        for t in range(10, len(Z)):
            for k in (1, 5): Xv[k].append(win_from_obs(Z, back_idx(t, np.full(W, k)), W, True))
            Yv.append(y[t])
    Yv = np.array(Yv, np.float32)
    for r in RS:
        X, Y = build(trs, mu, sd, 'A5R', np.random.default_rng(0), r); m = cm.train(X, Y, 0)
        v = [cm.rmse(cm.predict(m, np.stack(Xv[k])) - Yv) for k in (1, 5)]; sc[str(r)] = dict(k1=v[0], k5=v[1], score=float(np.mean(v))); print('select ext', r, sc[str(r)], flush=True)
    rstar = min(RS, key=lambda r: sc[str(r)]['score']); json.dump(dict(scores=sc, rstar=rstar, val_units=val), open(sel_file, 'w')); print('rstar ext', rstar, flush=True)
rng = np.random.default_rng(seed); mu, sd = stats(TRAIN); M = {}
for arm in ('A1', 'A6', 'A8F', 'GEN', 'A6M'):
    X, Y = build(TRAIN, mu, sd, arm, rng); M[arm] = cm.train(X, Y, seed); print(seed, arm, X.shape, flush=True)
for r in RS:
    X, Y = build(TRAIN, mu, sd, 'A5R', rng, r); M[f'A5r{r}'] = cm.train(X, Y, seed); print(seed, 'A5R', r, flush=True)


def stream(T, sc, ui):
    if sc in ('k1', 'k5', 'irr5', 'bern'):
        if sc == 'k1': obs = np.arange(T)
        elif sc == 'k5': obs = np.arange(0, T, 5)
        elif sc == 'irr5':
            c = np.cumsum(np.r_[0, np.random.default_rng(1000 + ui).integers(1, KMAX + 1, T)]); obs = c[c < T]
        else: obs = np.where(np.random.default_rng(3000 + ui).random(T) < 1.0 / 3.0)[0]
        return [(obs[:j + 1], obs[j]) for j in range(len(obs)) if obs[j] >= 10]
    B = int(sc[3:]); return [(np.r_[np.arange(0, max(t - 2 - B, 0)), np.arange(t - 2, t + 1)].astype(int), t) for t in range(10, T)]


res = {}
for ui, te in enumerate(TEST):
    Zt, yt = ((D[te][0] - mu) / sd).astype(np.float32), D[te][1]; T = len(Zt); res[te] = {}
    for sc in ('k1', 'k5', 'irr5', 'blk5', 'blk10', 'bern'):
        S = stream(T, sc, ui); I = [s[0] for s in S]; y = yt[[s[1] for s in S]]; st = lambda f: np.stack([f(i) for i in I])
        GL = st(lambda i: interp_grid(Zt, i, LONG)); XA = st(lambda i: win_from_obs(Zt, i, W, True))
        P = {'A1': cm.predict(M['A1'], st(lambda i: win_from_obs(Zt, i, W, False))), 'A2': cm.predict(M['A1'], st(lambda i: interp_grid(Zt, i, W)))}
        for a in ('A6', 'A8F', 'GEN', 'A6M'): P[a] = cm.predict(M[a], GL)
        for r in RS: P[f'A5r{r}'] = cm.predict(M[f'A5r{r}'], XA)
        res[te][sc] = {a: (p - y).tolist() for a, p in P.items()}
    print(seed, te, {a: round(cm.rmse(np.array(v)), 2) for a, v in res[te]['k5'].items()}, flush=True)
json.dump(res, open(f'results/extg_s{seed}.json', 'w'))
