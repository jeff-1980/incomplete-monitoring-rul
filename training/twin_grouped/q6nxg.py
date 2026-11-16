"""Q6 appendix A on N-CMAPSS: C8 and A6L (window 50).
Q6 confirmation on N-CMAPSS DS01+DS02, Q3 N-CMAPSS protocol (leave-one-unit-out, 19 folds, streaming predictions
at every cycle with >=10 elapsed cycles). Pre-registered: PREREG_Q6_2026-11-15.md. Usage: python3 q6n.py seed"""
import os, sys, json, numpy as np, cm
seed = int(sys.argv[1]); OUT = os.environ.get('Q6_OUT', 'results'); os.makedirs(OUT, exist_ok=True)
W, MMIN = 50, 2
z = np.load(os.environ.get('Q6_NCM', 'ncm_cycles.npz'))
D = {}
for k in z.files:
    if k.endswith('_X'): D[k[:-2]] = (z[k], np.minimum(z[k[:-2] + '_y'], cm.CAP))
names = sorted(D)
HIST = {'full': None, 'h5': 5, 'h3': 3}


def win(Z, t, m, pad='rep', flag=False):
    lo = 0 if m is None else max(0, t - m + 1)
    lo = max(lo, t - W + 1); X = Z[lo:t + 1]; n = len(X)
    fill = np.repeat(X[:1], W - n, 0) if pad == 'rep' else np.zeros((W - n, Z.shape[1]), np.float32)
    X = np.concatenate([fill, X]) if n < W else X
    if flag: X = np.concatenate([X, np.r_[np.ones(W - n), np.zeros(n)][:, None].astype(np.float32)], 1)
    return X.astype(np.float32)


def build(Zs, ys, kind, rng, m_fixed=None):
    Xs, Ys = [], []
    for Z, y in zip(Zs, ys):
        for t in range(len(Z)):
            if kind == 'dense': x = win(Z, t, None)
            elif kind == 'matched': x = win(Z, t, m_fixed)
            else: x = win(Z, t, int(rng.integers(MMIN, W + 1)))   # C8: m ~ U{2..50}
            Xs.append(x); Ys.append(y[t])
    return np.stack(Xs), np.array(Ys, np.float32)


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
    Zs = [((D[n][0] - mu) / sd).astype(np.float32) for n in trn]; ys = [D[n][1] for n in trn]
    M = {}
    for arm in ('dense', 'trunc'):
        X, Y = build(Zs, ys, arm, rng); M[arm] = cm.train(X, Y, seed)
    for te in members:
        fold = names.index(te)
        Zt, yt = ((D[te][0] - mu) / sd).astype(np.float32), D[te][1]; pts = np.arange(10, len(Zt)); y = yt[pts]
        res[te] = {}
        for h, m in HIST.items():
            P = {'A6L': cm.predict(M['dense'], np.stack([win(Zt, t, m) for t in pts])),
                 'C8': cm.predict(M['trunc'], np.stack([win(Zt, t, m) for t in pts]))}
            res[te][h] = {a: (p - y).tolist() for a, p in P.items()}
        print(seed, te, {h: {a: round(cm.rmse(np.array(v)), 2) for a, v in d.items()} for h, d in res[te].items()}, flush=True)
json.dump(res, open(f'{OUT}/q6nxg_s{seed}.json', 'w'))
