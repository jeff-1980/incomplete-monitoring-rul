"""Sensitivity analysis added after the runs (not in the protocol): MIT statistics without the five cells of batch 2017-06-30 (c7, c8, c9, c15, c16)
that continue cells of batch 2017-05-12 and therefore enter as late-life fragments. No retraining: the five cells remain in the training folds."""
import json, numpy as np
from scipy.stats import wilcoxon
DROP = {f'2017-06-30|2017-06-30_c{i}' for i in (7, 8, 9, 15, 16)}; cell = {}
for f in range(5):
    J = json.load(open(f'results/rs_mit_f{f}.json')); own = np.array(J['owner'])
    for s, A in J['err'].items():
        for a, E in A.items():
            E = np.array(E)
            for c in J['test']: cell.setdefault((s, a), {})[c] = float(np.mean(np.sqrt((E[:, own == c] ** 2).mean(1))))
names = sorted(cell[('full', 'DENSE')]); assert DROP <= set(names); keep = [c for c in names if c not in DROP]
def pair(s, a, b, N):
    x = np.array([cell[(s, a)][c] for c in N]); y = np.array([cell[(s, b)][c] for c in N]); d = x - y; bs = np.random.default_rng(0).choice(d, (10000, len(d))).mean(1)
    return f"{d.mean():+.2f} [{np.percentile(bs, 2.5):+.2f}, {np.percentile(bs, 97.5):+.2f}] p = {wilcoxon(x, y).pvalue:.2g}"
out = ['MIT, paired differences in cell RMSE: all 128 cells | without the five continuation cells (123)']
for lab, s, a, b in (('R1 GEN vs DENSE, k10', 'k10', 'GEN', 'DENSE'), ('R2 GEN vs DENSE, blk', 'blk', 'GEN', 'DENSE'), ('R3 MIX vs DENSE, k10', 'k10', 'MIX', 'DENSE'),
                     ('cost GEN vs DENSE, full', 'full', 'GEN', 'DENSE'), ('cost MIX vs DENSE, full', 'full', 'MIX', 'DENSE')):
    out.append(f'{lab}: {pair(s, a, b, names)} | {pair(s, a, b, keep)}')
out.append('RMSE of the five cells (DENSE/GEN, full): ' + '; '.join(f"{c.split('_')[-1]} {cell[('full', 'DENSE')][c]:.1f}/{cell[('full', 'GEN')][c]:.1f}" for c in sorted(DROP)))
open('sens_continuation.md', 'w', encoding='utf-8').write('\n'.join(out) + '\n'); print('\n'.join(out))
