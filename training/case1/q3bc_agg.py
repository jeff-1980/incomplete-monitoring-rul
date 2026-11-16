"""Summarise strong baselines (q3b) and reviewer arm A8 (q3c); same-run comparisons with A5. Run from bearing_rul_ideas."""
import json, numpy as np
from scipy.stats import wilcoxon
FDS = ['FD001', 'FD002', 'FD003', 'FD004']; rm = lambda e: float(np.sqrt(np.mean(np.square(e))))
L = []; P = L.append
for tag, arms, scs in [('q3b', ['A5', 'B1_GRUD', 'B2_GAIN', 'B3_PSR'], ['k1', 'k3', 'k5', 'irr5']),
                       ('q3c', ['A5', 'A8', 'A5_gap1', 'A5_as3'], ['k1', 'k2', 'k3', 'k5', 'irr5', 'irr10'])]:
    P(f'\n## {tag}: RMSE of seed-averaged |error|; vs A5 of the same run: mean |err| diff (other - A5), engines where other is better, Wilcoxon p\n')
    P('| subset | scenario | ' + ' | '.join(arms) + ' |'); P('|---|---|' + '---|' * len(arms))
    for fd in FDS:
        R = [json.load(open(f'results/{tag}_{fd}_s{s}.json')) for s in range(3)]
        for sc in scs:
            a5 = np.mean([np.abs(r[sc]['A5']) for r in R], 0); cells = []
            for a in arms:
                if a not in R[0][sc]: cells.append('—'); continue
                x = np.mean([np.abs(r[sc][a]) for r in R], 0)
                if a == 'A5': cells.append(f'{rm(x):.2f}'); continue
                d = x - a5; cells.append(f'{rm(x):.2f} ({d.mean():+.2f}, {(d < 0).sum()}/{len(d)}, p={wilcoxon(x, a5).pvalue:.1g})')
            P(f'| {fd} | {sc} | ' + ' | '.join(cells) + ' |')
open('results/q3bc_summary.md', 'w').write('\n'.join(L)); print('\n'.join(L))
