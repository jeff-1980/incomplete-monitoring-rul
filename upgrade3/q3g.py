"""Upgrade step 3 on C-MAPSS (PROTOCOL_upgrade3.md): generic deletion control, training mixture ratio, smoothing. Usage: python3 q3g.py FD001 seed"""
import sys, json, os, numpy as np, cm
from q3lib import obs_idx, win_from_obs, interp_grid, mixed_gaps, test_gaps, W, LONG, KMAX
fd, seed = sys.argv[1], int(sys.argv[2]); os.makedirs('results', exist_ok=True)
RS = (0.0, 0.25, 0.5, 0.75)


def full_gaps(r):
    return np.full(LONG, r.integers(1, KMAX + 1)) if r.random() < 0.5 else r.integers(1, KMAX + 1, LONG)


def density(r):                       # keep probability matched to the two halves of the DMWT law
    return 1.0 / r.integers(1, KMAX + 1) if r.random() < 0.5 else 1.0 / 3.0


def bern_idx(t, p, r):
    lo = max(0, t - LONG + 1); keep = r.random(t - lo) < p
    return np.r_[np.arange(lo, t)[keep], t].astype(int)


def smooth(X, m):
    if m <= 1: return X
    c = np.cumsum(np.concatenate([np.zeros((1, X.shape[1]), X.dtype), X]), 0); n = len(X); i = np.arange(n); lo = np.maximum(0, i - m + 1)
    return ((c[i + 1] - c[lo]) / (i + 1 - lo)[:, None]).astype(np.float32)


def build(engines, nm, kind, rng, r=0.0):
    Xs, Ys = [], []
    for e in engines.values():
        Z = nm(e); T = len(Z)
        for t in range(T):
            if kind == 'A1': x = win_from_obs(Z, np.arange(max(0, t - W + 1), t + 1), W, False)
            elif kind == 'A6': x = win_from_obs(Z, np.arange(max(0, t - LONG + 1), t + 1), LONG, False)
            elif kind == 'A8F': x = interp_grid(Z, obs_idx(t + 1, full_gaps(rng)), LONG)
            elif kind == 'GEN': x = interp_grid(Z, bern_idx(t, density(rng), rng), LONG)
            elif kind == 'A6M':
                m = int(rng.integers(1, KMAX + 1)) if rng.random() < 0.5 else 3
                lo = max(0, t - LONG + 1); x = win_from_obs(smooth(Z[lo:t + 1], m), np.arange(t + 1 - lo), LONG, False)
            elif kind == 'A5R':
                g = np.ones(W, int) if rng.random() < r else mixed_gaps(rng)
                x = win_from_obs(Z, obs_idx(t + 1, g), W, True)
            Xs.append(x); Ys.append(min(T - 1 - t, cm.CAP))
    return np.stack(Xs).astype(np.float32), np.array(Ys, np.float32)


tr = cm.raw(fd, 'train')
# ---------- Q2 selection of r on validation engines (once per subset, seed 0; test data not read) ----------
sel_file = f'results/selr_{fd}.json'
if not os.path.exists(sel_file):
    ids = sorted(tr); g = np.random.default_rng(12345); val = set(g.choice(ids, size=len(ids) // 5, replace=False).tolist())
    trs = {u: tr[u] for u in ids if u not in val}; vas = {u: tr[u] for u in ids if u in val}; nms = cm.Norm(trs); sc = {}
    Xv = {k: [] for k in (1, 5)}; Yv = []
    for e in vas.values():
        Z = nms(e); T = len(Z)
        for t in range(T):
            for k in (1, 5): Xv[k].append(win_from_obs(Z, obs_idx(t + 1, np.full(W, k)), W, True))
            Yv.append(min(T - 1 - t, cm.CAP))
    Yv = np.array(Yv, np.float32)
    for r in RS:
        X, Y = build(trs, nms, 'A5R', np.random.default_rng(0), r); m = cm.train(X, Y, 0)
        v = [cm.rmse(cm.predict(m, np.stack(Xv[k]).astype(np.float32)) - Yv) for k in (1, 5)]; sc[str(r)] = dict(k1=v[0], k5=v[1], score=float(np.mean(v))); print('select', fd, r, sc[str(r)], flush=True)
    rstar = min(RS, key=lambda r: sc[str(r)]['score']); json.dump(dict(scores=sc, rstar=rstar), open(sel_file, 'w')); print('rstar', fd, rstar, flush=True)
# ---------- final models ----------
rng = np.random.default_rng(seed); nm = cm.Norm(tr); te = cm.raw(fd, 'test'); units = sorted(te); yt = np.minimum(cm.test_rul(fd), cm.CAP); M = {}
for arm in ('A1', 'A6', 'A8F', 'GEN', 'A6M'):
    X, Y = build(tr, nm, arm, rng); M[arm] = cm.train(X, Y, seed); print(fd, seed, arm, X.shape, flush=True); del X
for r in RS:
    X, Y = build(tr, nm, 'A5R', rng, r); M[f'A5r{r}'] = cm.train(X, Y, seed); print(fd, seed, 'A5R', r, flush=True); del X
Zs = [nm(te[u]) for u in units]


def avail(sc, Z, u):
    T = len(Z)
    if sc in ('k1', 'k5', 'irr5'): return obs_idx(T, test_gaps(sc, u))
    if sc.startswith('blk'):
        B = int(sc[3:]); return np.r_[np.arange(0, max(T - 5 - B, 0)), np.arange(max(T - 5, 0), T)].astype(int)
    g = np.random.default_rng(3000 + u); keep = g.random(T) < 1.0 / 3.0; keep[-1] = True; return np.where(keep)[0]


out = {'y': yt.tolist()}
for sc in ('k1', 'k5', 'irr5', 'blk10', 'blk20', 'bern'):
    I = [avail(sc, Z, u) for Z, u in zip(Zs, units)]; st = lambda f: np.stack([f(Z, i) for Z, i in zip(Zs, I)])
    GL = st(lambda Z, i: interp_grid(Z, i, LONG)); XA = st(lambda Z, i: win_from_obs(Z, i, W, True))
    P = {'A1': cm.predict(M['A1'], st(lambda Z, i: win_from_obs(Z, i, W, False))), 'A2': cm.predict(M['A1'], st(lambda Z, i: interp_grid(Z, i, W)))}
    for a in ('A6', 'A8F', 'GEN', 'A6M'): P[a] = cm.predict(M[a], GL)
    for r in RS: P[f'A5r{r}'] = cm.predict(M[f'A5r{r}'], XA)
    out[sc] = {a: (p - yt).tolist() for a, p in P.items()}
    print(fd, seed, sc, ' '.join(f'{a} {cm.rmse(np.array(v)):.2f}' for a, v in out[sc].items()), flush=True)
json.dump(out, open(f'results/q3g_{fd}_s{seed}.json', 'w'))
