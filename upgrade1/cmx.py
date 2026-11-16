"""Upgrade step 1 on C-MAPSS (PROTOCOL_upgrade1.md, parts B and C). Usage: python3 cmx.py FD001 seed"""
import sys, json, os, numpy as np, cm
from q3lib import obs_idx, win_from_obs, interp_grid, locf_grid, mixed_gaps, W, LONG
fd, seed = sys.argv[1], int(sys.argv[2]); rng = np.random.default_rng(seed); os.makedirs('results', exist_ok=True)
MMIN, THR = 3, 60


def win(Z, t, m):
    lo = 0 if m is None else max(0, t - m + 1)
    lo = max(lo, t - W + 1); X = Z[lo:t + 1]; n = len(X)
    return (np.concatenate([np.repeat(X[:1], W - n, 0), X]) if n < W else X).astype(np.float32)


def build(engines, nm, kind):
    Xs, Ys = [], []
    for e in engines.values():
        Z = nm(e); T = len(Z)
        for t in range(T):
            y = min(T - 1 - t, cm.CAP)
            if kind == 'A1': x = win(Z, t, None)
            elif kind == 'A6': x = win_from_obs(Z, np.arange(max(0, t - LONG + 1), t + 1), LONG, False)
            elif kind == 'A5': x = win_from_obs(Z, obs_idx(t + 1, mixed_gaps(rng)), W, True)
            elif kind == 'A8': x = interp_grid(Z, obs_idx(t + 1, mixed_gaps(rng)), LONG)
            elif kind == 'A8B':
                g = mixed_gaps(rng).copy()
                if rng.random() < 0.3: g[rng.integers(0, W)] += rng.integers(5, 21)
                x = interp_grid(Z, obs_idx(t + 1, g), LONG)
            elif kind == 'S3': x = win(Z, t, int(rng.integers(MMIN, W + 1)))
            elif kind == 'S3E': x = win(Z, t, int(rng.integers(MMIN, W + 1)) if y > THR else None)
            elif kind == 'S3L': x = win(Z, t, int(rng.integers(MMIN, W + 1)) if y <= THR else None)
            Xs.append(x); Ys.append(y)
    return np.stack(Xs).astype(np.float32), np.array(Ys, np.float32)


tr = cm.raw(fd, 'train'); nm = cm.Norm(tr); te = cm.raw(fd, 'test'); units = sorted(te); yt = np.minimum(cm.test_rul(fd), cm.CAP)
M = {}
for arm in ('A1', 'A6', 'A5', 'A8', 'A8B', 'S3', 'S3E', 'S3L'):
    X, Y = build(tr, nm, arm); M[arm] = cm.train(X, Y, seed); print(fd, seed, arm, X.shape, flush=True); del X
Zs = [nm(te[u]) for u in units]
if nm.km is not None:
    order = np.argsort(nm.km.cluster_centers_[:, 0]); high = set(order[3:].tolist())


def avail(sc, Z, u):
    T = len(Z)
    if sc == 'k1': return np.arange(T)
    if sc.startswith('blk'):
        B = int(sc[3:]); return np.r_[np.arange(0, max(T - 5 - B, 0)), np.arange(max(T - 5, 0), T)].astype(int)
    r = nm.regime(te[u]); g = np.random.default_rng(2000 + u); p = np.where(np.isin(r, list(high)), 0.9, 0.1)
    keep = g.random(T) >= p; keep[-1] = True; return np.where(keep)[0]


out = {'y': yt.tolist()}
for sc in ['k1', 'blk10', 'blk20'] + (['reg'] if nm.km is not None else []):
    I = [avail(sc, Z, u) for Z, u in zip(Zs, units)]
    st = lambda f: np.stack([f(Z, i) for Z, i in zip(Zs, I)]); GL = st(lambda Z, i: interp_grid(Z, i, LONG))
    P = {'A1': cm.predict(M['A1'], st(lambda Z, i: win_from_obs(Z, i, W, False))),
         'A2': cm.predict(M['A1'], st(lambda Z, i: interp_grid(Z, i, W))),
         'A3': cm.predict(M['A1'], st(lambda Z, i: locf_grid(Z, i, W))),
         'A5': cm.predict(M['A5'], st(lambda Z, i: win_from_obs(Z, i, W, True))),
         'A6': cm.predict(M['A6'], GL), 'A8': cm.predict(M['A8'], GL), 'A8B': cm.predict(M['A8B'], GL)}
    out[sc] = {a: (p - yt).tolist() for a, p in P.items()}; out[sc]['n_rec'] = [int(len(i)) for i in I]
    print(fd, seed, sc, ' '.join(f'{a} {cm.rmse(np.array(v)):.2f}' for a, v in out[sc].items() if a != 'n_rec'), flush=True)
for h, m in (('full', None), ('h10', 10), ('h5', 5)):
    X = np.stack([win(Z, len(Z) - 1, m) for Z in Zs])
    out[h] = {a: (cm.predict(M[k], X) - yt).tolist() for a, k in (('S1', 'A1'), ('S3', 'S3'), ('S3E', 'S3E'), ('S3L', 'S3L'))}
    print(fd, seed, h, ' '.join(f'{a} {cm.rmse(np.array(v)):.2f}/{np.mean(v):+.1f}' for a, v in out[h].items()), flush=True)
json.dump(out, open(f'results/cmx_{fd}_s{seed}.json', 'w'))
