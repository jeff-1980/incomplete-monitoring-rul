"""A8 history-span control (PROTOCOL_A8_control.md). Usage: python3 q3e.py FD001 seed"""
import sys, json, numpy as np, cm
from q3lib import obs_idx, win_from_obs, interp_grid, mixed_gaps, test_gaps, W, LONG, KMAX
fd, seed = sys.argv[1], int(sys.argv[2]); rng = np.random.default_rng(seed); SC = ('k1', 'k2', 'k3', 'k5', 'irr5', 'irr10')


def full_gaps(r):
    """same gap law as mixed_gaps, but LONG gaps so the records cover the whole 150-cycle window"""
    if r.random() < 0.5: return np.full(LONG, r.integers(1, KMAX + 1))
    return r.integers(1, KMAX + 1, LONG)


def build(engines, nm, kind):
    Xs, Ys = [], []
    for e in engines.values():
        Z = nm(e); T = len(Z)
        for t in range(T):
            if kind == 'A1': x = win_from_obs(Z, np.arange(max(0, t - W + 1), t + 1), W, False)
            elif kind == 'A6': x = win_from_obs(Z, np.arange(max(0, t - LONG + 1), t + 1), LONG, False)
            elif kind == 'A8': x = interp_grid(Z, obs_idx(t + 1, mixed_gaps(rng)), LONG)
            elif kind == 'A8F': x = interp_grid(Z, obs_idx(t + 1, full_gaps(rng)), LONG)
            elif kind == 'A6S':
                L = t - obs_idx(t + 1, mixed_gaps(rng))[0] + 1           # span of an A8 window
                x = win_from_obs(Z, np.arange(t - L + 1, t + 1), LONG, False)
            Xs.append(x); Ys.append(min(T - 1 - t, cm.CAP))
    return np.stack(Xs).astype(np.float32), np.array(Ys, np.float32)


tr = cm.raw(fd, 'train'); nm = cm.Norm(tr); te = cm.raw(fd, 'test'); units = sorted(te); yt = np.minimum(cm.test_rul(fd), cm.CAP)
M = {}
for arm in ('A1', 'A6', 'A8', 'A8F', 'A6S'):
    X, Y = build(tr, nm, arm); M[arm] = cm.train(X, Y, seed); print(fd, seed, arm, X.shape, flush=True); del X
Zs = [nm(te[u]) for u in units]; out = {}
for sc in SC:
    I = [obs_idx(len(Z), test_gaps(sc, u)) for Z, u in zip(Zs, units)]
    st = lambda f: np.stack([f(Z, i) for Z, i in zip(Zs, I)])
    G = st(lambda Z, i: interp_grid(Z, i, LONG))
    P = {'A1': cm.predict(M['A1'], st(lambda Z, i: win_from_obs(Z, i, W, False)))}
    for a in ('A6', 'A8', 'A8F', 'A6S'): P[a] = cm.predict(M[a], G)
    out[sc] = {a: (p - yt).tolist() for a, p in P.items()}
    print(fd, seed, sc, ' '.join(f'{a} {cm.rmse(np.array(v)):.2f}' for a, v in out[sc].items()), flush=True)
json.dump(out, open(f'results/q3e_{fd}_s{seed}.json', 'w'))
