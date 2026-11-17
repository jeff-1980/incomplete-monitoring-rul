"""Descriptive check added after the runs (no model): how many MIT prediction windows contain a record whose value was filled, during cleaning,
from a cycle that is deleted in the scenario. Cleaning precedes deletion in rslib.load. Usage: python3 check_preclean.py <export_dir>"""
import sys, numpy as np, pandas as pd, rslib as R
df = pd.read_csv(f'{sys.argv[1]}/mit.csv.gz', low_memory=False); out = []; n = {'k10': 0, 'blk': 0, 'full': 0}; tot = 0; future = 0
for (b, c), g in df.groupby(['batch', 'battery_id']):
    g = g.sort_values('cycle'); X = g[R.FEATS['mit']].to_numpy(float); q = X[:, 0]
    eol = next((i for i in range(10, len(q) - 2) if (q[i:i + 3] < 0.88).all()), None)
    if eol is None:
        if q[-1] > 0.885: continue
        eol = len(q) - 1
    X = X[:eol + 1]; bad = X <= 0
    bad[:, 0] |= (X[:, 0] < 0.55) | (X[:, 0] > 1.43); bad[:, 1] |= (X[:, 1] < 0.55) | (X[:, 1] > 1.43); bad[:, 6] |= X[:, 6] > 60
    T = len(X); src = np.full(X.shape, -1)                       # index of the cycle that supplies the value of an invalid entry
    for j in range(X.shape[1]):
        ok = np.where(~bad[:, j])[0]
        for i in np.where(bad[:, j])[0]:
            p = ok[ok < i]; src[i, j] = p[-1] if len(p) else ok[ok > i][0]
    for t in range(R.T0, T, R.K):
        tot += 1
        for sc in n:
            idx = R.scen_idx(sc, t); win = idx[idx >= t - R.L]; S = src[win]; m = S >= 0      # records that can enter the 200-cycle input; sources traced against all available records
            if m.any():
                if not np.isin(S[m], idx).all(): n[sc] += 1
                if (S[m] > t).any(): future += 1
out.append(f"MIT: {tot} prediction times. Windows containing a record whose filled value comes from a cycle that is deleted in the scenario (not among its available records): "
           f"complete records {n['full']}, one record in 10 cycles {n['k10']} ({100 * n['k10'] / tot:.1f}%), outage {n['blk']} ({100 * n['blk'] / tot:.1f}%). Filled values taken from a cycle after the prediction time: {future}.")
open('check_preclean.md', 'w', encoding='utf-8').write('\n'.join(out) + '\n'); print('\n'.join(out))
