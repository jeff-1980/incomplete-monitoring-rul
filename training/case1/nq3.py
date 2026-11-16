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


res = {}
for fold, te in enumerate(names):
    rng = np.random.default_rng(seed * 100 + fold)
    trn = [n for n in names if n != te]
    A = np.concatenate([D[n][0] for n in trn]); mu, sd = A.mean(0), A.std(0) + 1e-6
    Zs = [(D[n][0] - mu) / sd for n in trn]; ys = [D[n][1] for n in trn]
    M = {}
    for arm in ('dense', 'mix', 'mixdt', 'long'):
        X, Y = build(Zs, ys, arm, rng); M[arm] = cm.train(X, Y, seed)
    X, Y = build(Zs, ys, 'matched', rng, 5); M['m5'] = cm.train(X, Y, seed)
    Zt, yt = (D[te][0] - mu) / sd, D[te][1]; T = len(Zt)
    res[te] = {}
    for sc in ('k1', 'k5', 'irr5'):
        obs = stream(T, sc, fold); pts = [j for j in range(len(obs)) if obs[j] >= 10]
        I = [obs[:j + 1] for j in pts]; y = yt[obs[pts]]
        P = {'A1': cm.predict(M['dense'], np.stack([win_from_obs(Zt, i, W, False) for i in I])),
             'A2': cm.predict(M['dense'], np.stack([interp_grid(Zt, i, W) for i in I])),
             'A3': cm.predict(M['dense'], np.stack([locf_grid(Zt, i, W) for i in I])),
             'A4': cm.predict(M['mix'], np.stack([win_from_obs(Zt, i, W, False) for i in I])),
             'A5': cm.predict(M['mixdt'], np.stack([win_from_obs(Zt, i, W, True) for i in I])),
             'A6': cm.predict(M['long'], np.stack([interp_grid(Zt, i, LONG) for i in I]))}
        if sc == 'k5': P['A7'] = cm.predict(M['m5'], np.stack([win_from_obs(Zt, i, W, False) for i in I]))
        res[te][sc] = {a: cm.rmse(p - y) for a, p in P.items()}
    print(seed, te, {sc: {a: round(v, 2) for a, v in d.items()} for sc, d in res[te].items()}, flush=True)
json.dump(res, open(f'results/nq3_s{seed}.json', 'w'))
