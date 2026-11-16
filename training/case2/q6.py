"""Q6 formal (C-MAPSS): RUL when the early history is missing (cold start). Pre-registered. Usage: python3 q6.py FD001 seed"""
import os, sys, json, numpy as np, cm
cm.ROOT = os.environ.get('Q6_DATA', cm.ROOT); OUT = os.environ.get('Q6_OUT', 'results'); os.makedirs(OUT, exist_ok=True)
fd, seed = sys.argv[1], int(sys.argv[2])
W, MMIN = cm.WIN, 3
rng = np.random.default_rng(seed)
HIST = {'full': None, 'h20': 20, 'h10': 10, 'h5': 5}


def win(Z, t, m, pad='rep', flag=False):
    lo = 0 if m is None else max(0, t - m + 1)
    lo = max(lo, t - W + 1); X = Z[lo:t + 1]; n = len(X)
    fill = np.repeat(X[:1], W - n, 0) if pad == 'rep' else np.zeros((W - n, Z.shape[1]), np.float32)
    X = np.concatenate([fill, X]) if n < W else X
    if flag: X = np.concatenate([X, np.r_[np.ones(W - n), np.zeros(n)][:, None].astype(np.float32)], 1)
    return X


def build(engines, nm, kind, m_fixed=None):
    Xs, Ys = [], []
    for e in engines.values():
        Z = nm(e); T = len(Z)
        for t in range(T):
            if kind == 'dense': x = win(Z, t, None)
            elif kind == 'matched': x = win(Z, t, m_fixed)
            else: x = win(Z, t, int(rng.integers(MMIN, W + 1)), flag=(kind == 'truncflag'))
            Xs.append(x); Ys.append(min(T - 1 - t, cm.CAP))
    return np.stack(Xs).astype(np.float32), np.array(Ys, np.float32)


tr = cm.raw(fd, 'train'); nm = cm.Norm(tr); te = cm.raw(fd, 'test'); units = sorted(te)
yt = np.minimum(cm.test_rul(fd), cm.CAP)
M = {}
for arm in ('dense', 'truncflag', 'trunc'):
    X, Y = build(tr, nm, arm); M[arm] = cm.train(X, Y, seed); print(fd, seed, arm, X.shape, flush=True)
for m in (20, 10, 5):
    X, Y = build(tr, nm, 'matched', m); M[f'm{m}'] = cm.train(X, Y, seed); print(fd, seed, 'matched', m, flush=True)
out = {}
for h, m in HIST.items():
    Zs = [nm(te[u]) for u in units]
    P = {'A1': cm.predict(M['dense'], np.stack([win(Z, len(Z) - 1, m) for Z in Zs])),
         'A2': cm.predict(M['dense'], np.stack([win(Z, len(Z) - 1, m, pad='zero') for Z in Zs])),
         'B3': cm.predict(M['trunc'], np.stack([win(Z, len(Z) - 1, m) for Z in Zs])),
         'B2': cm.predict(M['truncflag'], np.stack([win(Z, len(Z) - 1, m, flag=True) for Z in Zs]))}
    if m is not None: P['B4'] = cm.predict(M[f'm{m}'], np.stack([win(Z, len(Z) - 1, m) for Z in Zs]))
    out[h] = {a: (p - yt).tolist() for a, p in P.items()}
    print(fd, seed, h, ' '.join(f'{a} {cm.rmse(np.array(v)):.2f}' for a, v in out[h].items()), flush=True)
json.dump(out, open(f'{OUT}/q6_{fd}_s{seed}.json', 'w'))
