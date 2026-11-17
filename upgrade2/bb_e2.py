"""Amended selection for the external cohort: validation by profile group; only arms whose selected configuration changed are retrained.
Usage: python3 bb_e2.py tcn|tf seed"""
import sys, json, os, numpy as np, bbm
bb, seed = sys.argv[1], int(sys.argv[2]); os.makedirs('results', exist_ok=True)
W, KMAX, LONG, MMIN = 10, 5, 50, 2
z = np.load('ncm_cycles_ds03_08.npz')
D = {k[:-2]: (z[k], np.minimum(z[k[:-2] + '_y'], bbm.CAP)) for k in z.files if k.endswith('_X')}
EXCL_TEST = {'DS03_u10_test', 'DS03_u11_test', 'DS03_u14_test', 'DS03_u15_test', 'DS08a_u14_test'}
EXCL_TRAIN = {'DS03_u5_dev'}
TRAIN = sorted(n for n in D if n.endswith('_dev') and n not in EXCL_TRAIN)
TEST = sorted(n for n in D if n.endswith('_test') and n not in EXCL_TEST)
ARMS = ('A1', 'A5', 'A6', 'A8', 'S4')


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


def win(Z, t, m, n, pad='rep', flag=False):
    lo = 0 if m is None else max(0, t - m + 1)
    lo = max(lo, t - n + 1); X = Z[lo:t + 1]; k = len(X)
    fill = np.repeat(X[:1], n - k, 0) if pad == 'rep' else np.zeros((n - k, Z.shape[1]), np.float32)
    X = np.concatenate([fill, X]) if k < n else X
    if flag: X = np.concatenate([X, np.r_[np.ones(n - k), np.zeros(k)][:, None].astype(np.float32)], 1)
    return X.astype(np.float32)


def build(names, mu, sd, kind, rng):
    Xs, Ys = [], []
    mixed = lambda: np.full(W, rng.integers(1, KMAX + 1)) if rng.random() < 0.5 else rng.integers(1, KMAX + 1, W)
    for n in names:
        Z = ((D[n][0] - mu) / sd).astype(np.float32); y = D[n][1]
        for t in range(len(Z)):
            if kind == 'A1': x = win(Z, t, None, W)
            elif kind == 'A6': x = win(Z, t, None, LONG)
            elif kind == 'A5': x = win_from_obs(Z, back_idx(t, mixed()), W, True)
            elif kind == 'A8': x = interp_grid(Z, back_idx(t, mixed()), LONG)
            elif kind == 'S4': x = win(Z, t, int(rng.integers(MMIN, W + 1)), W, flag=True)
            Xs.append(x); Ys.append(y[t])
    return np.stack(Xs).astype(np.float32), np.array(Ys, np.float32)


def stats(names):
    A = np.concatenate([D[n][0] for n in names]); return A.mean(0), A.std(0) + 1e-6


# ---- amendment: validation units are whole profile groups (PROTOCOL_upgrade2_amendment.md) ----
prof = lambda u: ('DS05-07_' + u.split('_')[1]) if u.split('_')[0] in ('DS05', 'DS06', 'DS07') else u
sel_file = f'results/sel_{bb}_ext_g.json'
if not os.path.exists(sel_file):
    G = sorted(set(prof(u) for u in TRAIN)); gv = set(G[::5]); val = [n for n in TRAIN if prof(n) in gv]; trs = [n for n in TRAIN if prof(n) not in gv]; mu, sd = stats(trs); sel = {}
    for arm in ARMS:
        X, Y = build(trs, mu, sd, arm, np.random.default_rng(0)); Xv, Yv = build(val, mu, sd, arm, np.random.default_rng(777)); sc = []
        for cfg in bbm.GRID:
            m = bbm.train(bb, X, Y, 0, cfg); sc.append(bbm.rmse(bbm.predict(m, Xv) - Yv)); del m
        sel[arm] = dict(cfg=list(bbm.GRID[int(np.argmin(sc))]), val_rmse=sc, val_units=val); print('select-g', bb, arm, sel[arm]['cfg'], sc, flush=True)
    json.dump(sel, open(sel_file, 'w'))
sel = json.load(open(sel_file)); old = json.load(open(f'results/sel_{bb}_ext.json'))
CH = [a for a in ARMS if sel[a]['cfg'] != old[a]['cfg']]; print(bb, seed, 'changed arms', CH, flush=True)
res = json.load(open(f'results/bbe_{bb}_s{seed}.json'))
if not CH:
    json.dump(res, open(f'results/bbe2_{bb}_s{seed}.json', 'w')); sys.exit()
rng = np.random.default_rng(seed); mu, sd = stats(TRAIN); M = {}
for arm in ARMS:                      # same random stream as the original run; only changed arms are retrained
    X, Y = build(TRAIN, mu, sd, arm, rng)
    if arm in CH: M[arm] = bbm.train(bb, X, Y, seed, tuple(sel[arm]['cfg'])); print(bb, seed, 'retrained', arm, flush=True)


def stream(T, sc, ui):
    if sc == 'k1': obs = np.arange(T)
    elif sc == 'k5': obs = np.arange(0, T, 5)
    else:
        c = np.cumsum(np.r_[0, np.random.default_rng(1000 + ui).integers(1, KMAX + 1, T)]); obs = c[c < T]
    return [(obs[:j + 1], obs[j]) for j in range(len(obs)) if obs[j] >= 10]


for ui, te in enumerate(TEST):
    Zt, yt = ((D[te][0] - mu) / sd).astype(np.float32), D[te][1]; T = len(Zt)
    for sc in ('k1', 'k5', 'irr5'):
        S = stream(T, sc, ui); I = [s[0] for s in S]; y = yt[[s[1] for s in S]]
        st = lambda f: np.stack([f(i) for i in I]); P = {}
        if 'A1' in M:
            P.update(A1=bbm.predict(M['A1'], st(lambda i: win_from_obs(Zt, i, W, False))), A2=bbm.predict(M['A1'], st(lambda i: interp_grid(Zt, i, W))), A3=bbm.predict(M['A1'], st(lambda i: locf_grid(Zt, i, W))))
        if 'A5' in M: P['A5'] = bbm.predict(M['A5'], st(lambda i: win_from_obs(Zt, i, W, True)))
        for a in ('A6', 'A8'):
            if a in M: P[a] = bbm.predict(M[a], st(lambda i: interp_grid(Zt, i, LONG)))
        for a, p in P.items(): res[te][sc][a] = (p - y).tolist()
    pts = np.arange(10, T); y = yt[pts]
    for h, m in (('full', None), ('h5', 5), ('h3', 3)):
        st = lambda f: np.stack([f(t) for t in pts]); P = {}
        if 'A1' in M: P.update(S1=bbm.predict(M['A1'], st(lambda t: win(Zt, t, m, W))), S2=bbm.predict(M['A1'], st(lambda t: win(Zt, t, m, W, pad='zero'))))
        if 'S4' in M: P['S4'] = bbm.predict(M['S4'], st(lambda t: win(Zt, t, m, W, flag=True)))
        for a, p in P.items(): res[te][h][a] = (p - y).tolist()
json.dump(res, open(f'results/bbe2_{bb}_s{seed}.json', 'w'))
