"""Upgrade step 2 on C-MAPSS (PROTOCOL_upgrade2.md). Usage: python3 bb_c.py tcn|tf FD001 seed"""
import sys, json, os, numpy as np, cm, bbm
from q3lib import obs_idx, win_from_obs, interp_grid, locf_grid, mixed_gaps, test_gaps, W, LONG
bb, fd, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]); os.makedirs('results', exist_ok=True); MMIN = 3
ARMS = ('A1', 'A5', 'A6', 'A8', 'S4')


def win(Z, t, m, flag=False, pad='rep'):
    lo = 0 if m is None else max(0, t - m + 1)
    lo = max(lo, t - W + 1); X = Z[lo:t + 1]; n = len(X)
    fill = np.repeat(X[:1], W - n, 0) if pad == 'rep' else np.zeros((W - n, Z.shape[1]), np.float32)
    X = np.concatenate([fill, X]) if n < W else X
    if flag: X = np.concatenate([X, np.r_[np.ones(W - n), np.zeros(n)][:, None].astype(np.float32)], 1)
    return X.astype(np.float32)


def build(engines, nm, kind, rng):
    Xs, Ys = [], []
    for e in engines.values():
        Z = nm(e); T = len(Z)
        for t in range(T):
            if kind == 'A1': x = win(Z, t, None)
            elif kind == 'A6': x = win_from_obs(Z, np.arange(max(0, t - LONG + 1), t + 1), LONG, False)
            elif kind == 'A5': x = win_from_obs(Z, obs_idx(t + 1, mixed_gaps(rng)), W, True)
            elif kind == 'A8': x = interp_grid(Z, obs_idx(t + 1, mixed_gaps(rng)), LONG)
            elif kind == 'S4': x = win(Z, t, int(rng.integers(MMIN, W + 1)), flag=True)
            Xs.append(x); Ys.append(min(T - 1 - t, cm.CAP))
    return np.stack(Xs).astype(np.float32), np.array(Ys, np.float32)


tr = cm.raw(fd, 'train')
# ---------- selection on validation engines (once per backbone and subset; test data not read) ----------
sel_file = f'results/sel_{bb}_{fd}.json'
if not os.path.exists(sel_file):
    ids = sorted(tr); r = np.random.default_rng(12345); val = set(r.choice(ids, size=len(ids) // 5, replace=False).tolist())
    trs = {u: tr[u] for u in ids if u not in val}; vas = {u: tr[u] for u in ids if u in val}; nms = cm.Norm(trs); sel = {}
    for arm in ARMS:
        X, Y = build(trs, nms, arm, np.random.default_rng(0)); Xv, Yv = build(vas, nms, arm, np.random.default_rng(777)); sc = []
        for cfg in bbm.GRID:
            m = bbm.train(bb, X, Y, 0, cfg); sc.append(bbm.rmse(bbm.predict(m, Xv) - Yv)); del m
        sel[arm] = dict(cfg=list(bbm.GRID[int(np.argmin(sc))]), val_rmse=sc); print('select', bb, fd, arm, sel[arm], flush=True); del X, Xv
    json.dump(sel, open(sel_file, 'w'))
sel = json.load(open(sel_file))
# ---------- final models on all training engines ----------
rng = np.random.default_rng(seed); nm = cm.Norm(tr); te = cm.raw(fd, 'test'); units = sorted(te); yt = np.minimum(cm.test_rul(fd), cm.CAP)
M = {}
for arm in ARMS:
    X, Y = build(tr, nm, arm, rng); M[arm] = bbm.train(bb, X, Y, seed, tuple(sel[arm]['cfg'])); print(bb, fd, seed, arm, X.shape, flush=True); del X
Zs = [nm(te[u]) for u in units]; out = {'y': yt.tolist()}
for sc in ('k1', 'k5', 'irr5'):
    I = [obs_idx(len(Z), test_gaps(sc, u)) for Z, u in zip(Zs, units)]
    st = lambda f: np.stack([f(Z, i) for Z, i in zip(Zs, I)]); GL = st(lambda Z, i: interp_grid(Z, i, LONG))
    P = {'A1': bbm.predict(M['A1'], st(lambda Z, i: win_from_obs(Z, i, W, False))), 'A2': bbm.predict(M['A1'], st(lambda Z, i: interp_grid(Z, i, W))),
         'A3': bbm.predict(M['A1'], st(lambda Z, i: locf_grid(Z, i, W))), 'A5': bbm.predict(M['A5'], st(lambda Z, i: win_from_obs(Z, i, W, True))),
         'A6': bbm.predict(M['A6'], GL), 'A8': bbm.predict(M['A8'], GL)}
    out[sc] = {a: (p - yt).tolist() for a, p in P.items()}
    print(bb, fd, seed, sc, ' '.join(f'{a} {bbm.rmse(np.array(v)):.2f}' for a, v in out[sc].items()), flush=True)
for h, m in (('full', None), ('h10', 10), ('h5', 5)):
    P = {'S1': bbm.predict(M['A1'], np.stack([win(Z, len(Z) - 1, m) for Z in Zs])), 'S2': bbm.predict(M['A1'], np.stack([win(Z, len(Z) - 1, m, pad='zero') for Z in Zs])),
         'S4': bbm.predict(M['S4'], np.stack([win(Z, len(Z) - 1, m, flag=True) for Z in Zs]))}
    out[h] = {a: (p - yt).tolist() for a, p in P.items()}
    print(bb, fd, seed, h, ' '.join(f'{a} {bbm.rmse(np.array(v)):.2f}' for a, v in out[h].items()), flush=True)
json.dump(out, open(f'results/bbc_{bb}_{fd}_s{seed}.json', 'w'))
