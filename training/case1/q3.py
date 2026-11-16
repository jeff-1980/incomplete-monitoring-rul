"""Q3 formal experiment on C-MAPSS (pre-registered in PREREG_Q3_sparse_2026-11-15.md). Usage: python3 q3.py FD001 seed"""
import sys, json, numpy as np, cm
fd, seed = sys.argv[1], int(sys.argv[2])
W, KMAX, LONG = cm.WIN, 5, 150
rng = np.random.default_rng(seed)


def obs_idx(T, gaps):
    """observation cycle indices ending at T-1, given a backwards gap sequence; returns ascending indices >= 0"""
    idx = [T - 1]
    for g in gaps:
        if idx[-1] - g < 0: break
        idx.append(idx[-1] - g)
    return np.array(idx[::-1])


def win_from_obs(Z, idx, n, dt):
    """last n observations at cycles idx (ascending); pad by repeating the first; optional per-step gap channel"""
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


def mixed_gaps(r):
    if r.random() < 0.5: return np.full(W, r.integers(1, KMAX + 1))
    return r.integers(1, KMAX + 1, W)


def build(engines, nm, kind, k=1):
    Xs, Ys = [], []
    for e in engines.values():
        Z = nm(e); T = len(Z)
        for t in range(T):
            y = min(T - 1 - t, cm.CAP)
            if kind == 'dense': x = win_from_obs(Z, np.arange(max(0, t - W + 1), t + 1), W, False)
            elif kind == 'long': x = win_from_obs(Z, np.arange(max(0, t - LONG + 1), t + 1), LONG, False)
            elif kind == 'matched': x = win_from_obs(Z, obs_idx(t + 1, np.full(W, k)), W, False)
            else: x = win_from_obs(Z, obs_idx(t + 1, mixed_gaps(rng)), W, kind == 'mixdt')
            Xs.append(x); Ys.append(y)
    return np.stack(Xs).astype(np.float32), np.array(Ys, np.float32)


SCEN = {'k1': ('reg', 1), 'k2': ('reg', 2), 'k3': ('reg', 3), 'k5': ('reg', 5), 'irr5': ('irr', 5), 'irr10': ('irr', 10)}


def test_gaps(sc, u):
    t, k = SCEN[sc]
    return np.full(400, k) if t == 'reg' else np.random.default_rng(1000 + u).integers(1, k + 1, 400)


tr = cm.raw(fd, 'train'); nm = cm.Norm(tr); te = cm.raw(fd, 'test'); units = sorted(te)
yt = np.minimum(cm.test_rul(fd), cm.CAP)
M = {}
for arm in ('dense', 'mix', 'mixdt', 'long'):
    X, Y = build(tr, nm, arm); M[arm] = cm.train(X, Y, seed); print(fd, seed, arm, X.shape, flush=True)
for k in (2, 3, 5):
    X, Y = build(tr, nm, 'matched', k); M[f'm{k}'] = cm.train(X, Y, seed); print(fd, seed, 'matched', k, flush=True)
out = {}
for sc in SCEN:
    Zs = [nm(te[u]) for u in units]; I = [obs_idx(len(Z), test_gaps(sc, u)) for Z, u in zip(Zs, units)]
    P = {}
    P['A1'] = cm.predict(M['dense'], np.stack([win_from_obs(Z, i, W, False) for Z, i in zip(Zs, I)]))
    P['A2'] = cm.predict(M['dense'], np.stack([interp_grid(Z, i, W) for Z, i in zip(Zs, I)]))
    P['A3'] = cm.predict(M['dense'], np.stack([locf_grid(Z, i, W) for Z, i in zip(Zs, I)]))
    P['A4'] = cm.predict(M['mix'], np.stack([win_from_obs(Z, i, W, False) for Z, i in zip(Zs, I)]))
    P['A5'] = cm.predict(M['mixdt'], np.stack([win_from_obs(Z, i, W, True) for Z, i in zip(Zs, I)]))
    P['A6'] = cm.predict(M['long'], np.stack([interp_grid(Z, i, LONG) for Z, i in zip(Zs, I)]))
    t, k = SCEN[sc]
    if t == 'reg' and k in (2, 3, 5): P['A7'] = cm.predict(M[f'm{k}'], np.stack([win_from_obs(Z, i, W, False) for Z, i in zip(Zs, I)]))
    out[sc] = {a: (p - yt).tolist() for a, p in P.items()}
    print(fd, seed, sc, ' '.join(f'{a} {cm.rmse(np.array(v)):.2f}' for a, v in out[sc].items()), flush=True)
json.dump(out, open(f'results/q3_{fd}_s{seed}.json', 'w'))
