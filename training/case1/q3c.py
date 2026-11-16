"""Reviewer requests (round 1): A8 = dense GRU trained on sparsified-then-interpolated every-cycle windows covering the
last 150 cycles (same interval law as A5), evaluated with the same interpolation at test; A5 re-trained and saved;
test-time checks of A5: k1_as3 (dense data deliberately sub-sampled every 3rd cycle, ~90-cycle coverage) and
k5_gap1 (k=5 data but the gap channel set to 1). Usage: python3 q3c.py FD001 seed"""
import sys, json, os, numpy as np, torch, cm
from q3lib import obs_idx, win_from_obs, interp_grid, mixed_gaps, test_gaps, W, LONG
fd, seed = sys.argv[1], int(sys.argv[2]); rng = np.random.default_rng(seed); os.makedirs('models', exist_ok=True)


def build(engines, nm, kind):
    Xs, Ys = [], []
    for e in engines.values():
        Z = nm(e); T = len(Z)
        for t in range(T):
            idx = obs_idx(t + 1, mixed_gaps(rng))
            Xs.append(interp_grid(Z, idx, LONG) if kind == 'A8' else win_from_obs(Z, idx, W, True)); Ys.append(min(T - 1 - t, cm.CAP))
    return np.stack(Xs).astype(np.float32), np.array(Ys, np.float32)


tr = cm.raw(fd, 'train'); nm = cm.Norm(tr); te = cm.raw(fd, 'test'); units = sorted(te); yt = np.minimum(cm.test_rul(fd), cm.CAP)
M = {}
for arm in ('A5', 'A8'):
    X, Y = build(tr, nm, arm); M[arm] = cm.train(X, Y, seed); torch.save(M[arm].state_dict(), f'models/{arm}_{fd}_s{seed}.pt'); print(fd, seed, arm, X.shape, flush=True)
out = {}
Zs = [nm(te[u]) for u in units]
for sc in ('k1', 'k2', 'k3', 'k5', 'irr5', 'irr10'):
    I = [obs_idx(len(Z), test_gaps(sc, u)) for Z, u in zip(Zs, units)]
    P = {'A5': cm.predict(M['A5'], np.stack([win_from_obs(Z, i, W, True) for Z, i in zip(Zs, I)])),
         'A8': cm.predict(M['A8'], np.stack([interp_grid(Z, i, LONG) for Z, i in zip(Zs, I)]))}
    if sc == 'k5':
        X5 = np.stack([win_from_obs(Z, i, W, True) for Z, i in zip(Zs, I)]); X5[:, :, -1] = np.where(X5[:, :, -1] > 0, 1 / 5, 0)
        P['A5_gap1'] = cm.predict(M['A5'], X5)
    if sc == 'k1':
        I3 = [obs_idx(len(Z), np.full(400, 3)) for Z in Zs]
        P['A5_as3'] = cm.predict(M['A5'], np.stack([win_from_obs(Z, i, W, True) for Z, i in zip(Zs, I3)]))
    out[sc] = {a: (p - yt).tolist() for a, p in P.items()}
    print(fd, seed, sc, ' '.join(f'{a} {cm.rmse(np.array(v)):.2f}' for a, v in out[sc].items()), flush=True)
json.dump(out, open(f'results/q3c_{fd}_s{seed}.json', 'w'))
