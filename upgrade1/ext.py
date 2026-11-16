"""Upgrade step 1 on N-CMAPSS DS03-DS08 (PROTOCOL_upgrade1.md, parts A, B, C). Fixed split, fixed models.
Usage: python3 ext.py seed"""
import sys, json, os, numpy as np, cm
seed = int(sys.argv[1]); os.makedirs('results', exist_ok=True)
W, KMAX, LONG, MMIN, THR = 10, 5, 50, 2, 40
z = np.load('ncm_cycles_ds03_08.npz')
D = {k[:-2]: (z[k], np.minimum(z[k[:-2] + '_y'], cm.CAP)) for k in z.files if k.endswith('_X')}
EXCL_TEST = {'DS03_u10_test', 'DS03_u11_test', 'DS03_u14_test', 'DS03_u15_test', 'DS08a_u14_test'}   # profile shared with DS01/DS02
EXCL_TRAIN = {'DS03_u5_dev'}                                                                          # profile shared with a test unit
TRAIN = sorted(n for n in D if n.endswith('_dev') and n not in EXCL_TRAIN)
TEST = sorted(n for n in D if n.endswith('_test') and n not in EXCL_TEST)
rng = np.random.default_rng(seed)
A = np.concatenate([D[n][0] for n in TRAIN]); mu, sd = A.mean(0), A.std(0) + 1e-6
Zs = [((D[n][0] - mu) / sd).astype(np.float32) for n in TRAIN]; ys = [D[n][1] for n in TRAIN]


def win_from_obs(Z, idx, n, dt):
    X = Z[idx]; g = np.r_[0, np.diff(idx)].astype(np.float32)
    if len(X) < n: X = np.concatenate([np.repeat(X[:1], n - len(X), 0), X]); g = np.r_[np.zeros(n - len(g), np.float32), g]
    X, g = X[-n:], g[-n:]
    return np.concatenate([X, g[:, None] / KMAX], 1).astype(np.float32) if dt else X.astype(np.float32)


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


def mixed():
    return np.full(W, rng.integers(1, KMAX + 1)) if rng.random() < 0.5 else rng.integers(1, KMAX + 1, W)


def win(Z, t, m, n, pad='rep', flag=False):
    lo = 0 if m is None else max(0, t - m + 1)
    lo = max(lo, t - n + 1); X = Z[lo:t + 1]; k = len(X)
    fill = np.repeat(X[:1], n - k, 0) if pad == 'rep' else np.zeros((n - k, Z.shape[1]), np.float32)
    X = np.concatenate([fill, X]) if k < n else X
    if flag: X = np.concatenate([X, np.r_[np.ones(n - k), np.zeros(k)][:, None].astype(np.float32)], 1)
    return X.astype(np.float32)


def build(kind):
    Xs, Ys = [], []
    for Z, y in zip(Zs, ys):
        for t in range(len(Z)):
            if kind == 'dense': x = win(Z, t, None, W)
            elif kind == 'long': x = win(Z, t, None, LONG)
            elif kind == 'mix': x = win_from_obs(Z, back_idx(t, mixed()), W, False)
            elif kind == 'mixdt': x = win_from_obs(Z, back_idx(t, mixed()), W, True)
            elif kind == 'a8': x = interp_grid(Z, back_idx(t, mixed()), LONG)
            elif kind == 'a8b':
                g = mixed().copy()
                if rng.random() < 0.3: g[rng.integers(0, W)] += rng.integers(3, 11)
                x = interp_grid(Z, back_idx(t, g), LONG)
            elif kind == 'trunc': x = win(Z, t, int(rng.integers(MMIN, W + 1)), W)
            elif kind == 'truncflag': x = win(Z, t, int(rng.integers(MMIN, W + 1)), W, flag=True)
            elif kind == 'trunclong': x = win(Z, t, int(rng.integers(MMIN, LONG + 1)), LONG)
            elif kind == 's3e': x = win(Z, t, int(rng.integers(MMIN, W + 1)) if y[t] > THR else None, W)
            elif kind == 's3l': x = win(Z, t, int(rng.integers(MMIN, W + 1)) if y[t] <= THR else None, W)
            Xs.append(x); Ys.append(y[t])
    return np.stack(Xs).astype(np.float32), np.array(Ys, np.float32)


M = {}
for arm in ('dense', 'long', 'mix', 'mixdt', 'a8', 'a8b', 'trunc', 'truncflag', 'trunclong', 's3e', 's3l'):
    X, Y = build(arm); M[arm] = cm.train(X, Y, seed); print(seed, arm, X.shape, flush=True)


def stream(T, sc, ui):
    """list of (index array of available records, prediction cycle)"""
    if sc in ('k1', 'k5', 'irr5'):
        if sc == 'k1': obs = np.arange(T)
        elif sc == 'k5': obs = np.arange(0, T, 5)
        else:
            c = np.cumsum(np.r_[0, np.random.default_rng(1000 + ui).integers(1, KMAX + 1, T)]); obs = c[c < T]
        return [(obs[:j + 1], obs[j]) for j in range(len(obs)) if obs[j] >= 10]
    B = int(sc[3:]); out = []
    for t in range(10, T):
        early = np.arange(0, max(t - 2 - B, 0)); out.append((np.r_[early, np.arange(t - 2, t + 1)].astype(int), t))
    return out


res = {}
for ui, te in enumerate(TEST):
    Zt, yt = ((D[te][0] - mu) / sd).astype(np.float32), D[te][1]; T = len(Zt); res[te] = {}
    for sc in ('k1', 'k5', 'irr5', 'blk5', 'blk10'):
        S = stream(T, sc, ui); I = [s[0] for s in S]; y = yt[[s[1] for s in S]]
        st = lambda f: np.stack([f(i) for i in I])
        GL = st(lambda i: interp_grid(Zt, i, LONG))
        P = {'A1': cm.predict(M['dense'], st(lambda i: win_from_obs(Zt, i, W, False))),
             'A2': cm.predict(M['dense'], st(lambda i: interp_grid(Zt, i, W))),
             'A3': cm.predict(M['dense'], st(lambda i: locf_grid(Zt, i, W))),
             'A4': cm.predict(M['mix'], st(lambda i: win_from_obs(Zt, i, W, False))),
             'A5': cm.predict(M['mixdt'], st(lambda i: win_from_obs(Zt, i, W, True))),
             'A6': cm.predict(M['long'], GL), 'A8': cm.predict(M['a8'], GL), 'A8B': cm.predict(M['a8b'], GL)}
        res[te][sc] = {a: (p - y).tolist() for a, p in P.items()}; res[te][sc]['y'] = y.tolist()
    pts = np.arange(10, T); y = yt[pts]
    for h, m in (('full', None), ('h5', 5), ('h3', 3)):
        st = lambda f: np.stack([f(t) for t in pts])
        P = {'S1': cm.predict(M['dense'], st(lambda t: win(Zt, t, m, W))),
             'S2': cm.predict(M['dense'], st(lambda t: win(Zt, t, m, W, pad='zero'))),
             'S3': cm.predict(M['trunc'], st(lambda t: win(Zt, t, m, W))),
             'S4': cm.predict(M['truncflag'], st(lambda t: win(Zt, t, m, W, flag=True))),
             'S6': cm.predict(M['long'], st(lambda t: win(Zt, t, m, LONG))),
             'S8': cm.predict(M['trunclong'], st(lambda t: win(Zt, t, m, LONG))),
             'S3E': cm.predict(M['s3e'], st(lambda t: win(Zt, t, m, W))),
             'S3L': cm.predict(M['s3l'], st(lambda t: win(Zt, t, m, W)))}
        res[te][h] = {a: (p - y).tolist() for a, p in P.items()}; res[te][h]['y'] = y.tolist()
    print(seed, te, {sc: {a: round(cm.rmse(np.array(v)), 2) for a, v in d.items() if a != 'y'} for sc, d in res[te].items() if sc in ('k5', 'h5')}, flush=True)
json.dump(res, open(f'results/ext_s{seed}.json', 'w'))
