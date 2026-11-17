"""Trade-off table of the candidate training recipes, from stored errors only (no new experiment): best test-time remedy on the dense model, A5 (r = 0),
A5 with the validation-selected r*, A8 and GEN. RMSE in cycles, mean over five seeds (C-MAPSS) or mean unit RMSE of the seed-averaged unit RMSE (DS03-DS08).
Sources: upgrade3 (A5 r, GEN; all scenarios), data/q3d and upgrade1 (A8, A3; same dense models, checked), written to analysis/tables_tradeoff.md."""
import json, os, numpy as np
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); FDS = ['FD001', 'FD002', 'FD003', 'FD004']
rm = lambda e: float(np.sqrt(np.mean(np.square(e))))
G = {fd: [json.load(open(f'{B}/upgrade3/results/q3g_{fd}_s{s}.json')) for s in range(5)] for fd in FDS}
D = {fd: [json.load(open(f'{B}/data/q3d_{fd}_s{s}.json')) for s in range(5)] for fd in FDS}
C = {fd: [json.load(open(f'{B}/upgrade1/results/cmx_{fd}_s{s}.json')) for s in range(5)] for fd in FDS}
EG = [json.load(open(f'{B}/upgrade3/results/extg_s{s}.json')) for s in range(5)]; E1 = [json.load(open(f'{B}/upgrade1/results/ext_s{s}.json')) for s in range(5)]; units = sorted(EG[0])
SEL = {fd: json.load(open(f'{B}/upgrade3/results/selr_{fd}.json'))['rstar'] for fd in FDS}; SEL['ext'] = json.load(open(f'{B}/upgrade3/results/selr_ext.json'))['rstar']
for fd in FDS:
    for s in range(5):
        for sc in ('k1', 'k5', 'irr5'): assert np.allclose(G[fd][s][sc]['A1'], D[fd][s][sc]['A1'], atol=1e-3)
        for sc in ('k1', 'blk10', 'blk20'): assert np.allclose(G[fd][s][sc]['A1'], C[fd][s][sc]['A1'], atol=1e-3), (fd, s, sc)
for s in range(5):
    for u in units:
        for sc in ('k1', 'k5', 'irr5', 'blk5', 'blk10'): assert np.allclose(EG[s][u][sc]['A1'], E1[s][u][sc]['A1'], atol=1e-3)
SCS = [('complete records', 'k1', 'k1'), ('k = 5', 'k5', 'k5'), ('irregular 1–5', 'irr5', 'irr5'), ('block outage, shorter', 'blk10', 'blk5'), ('block outage, longer', 'blk20', 'blk10')]
def cm(fd, sc, arm):
    src = G[fd] if arm in G[fd][0][sc] else (D[fd] if sc in D[fd][0] and arm in D[fd][0][sc] else C[fd]); return float(np.mean([rm(r[sc][arm]) for r in src]))
def ex(sc, arm):
    src = EG if arm in EG[0][units[0]][sc] else E1; return float(np.mean([np.mean([rm(r[u][sc][arm]) for r in src]) for u in units]))
ARMS = ['remedy', 'A5', 'A5*', 'A8', 'GEN']; HEAD = ['Best dense model', 'A5 (r = 0)', 'A5 (r*)', 'A8', 'GEN']
def val(k, sc, arm):
    f = (lambda a: ex(sc, a)) if k == 'ext' else (lambda a: cm(k, sc, a))
    if arm == 'remedy': return min(f(a) for a in (('A1', 'A6') if sc == 'k1' else ('A1', 'A2', 'A3', 'A6')))
    return f({'A5': 'A5r0.0', 'A5*': f'A5r{SEL[k]}', 'A8': 'A8', 'GEN': 'GEN'}[arm])
S = {}; L = []; P = L.append
P('## Table S34. Trade-off between the candidate training recipes: RMSE (cycles) by data source and scenario\n')
P('From stored errors, no new experiment. C-MAPSS: mean over five seeds; DS03–DS08: mean unit RMSE. Best dense model: lowest RMSE among the densely trained models with or without test-time repair (A1, A2, A3 and the long-input model A6; A1 and A6 with complete records). Block outages: 10 and 20 cycles on C-MAPSS, 5 and 10 on DS03–DS08. The lowest value of a row is in bold.\n')
P('| Data | Scenario | ' + ' | '.join(HEAD) + ' |'); P('|---|---|' + '---|' * 5)
for k in FDS + ['ext']:
    for lab, c, e in SCS:
        v = [val(k, e if k == 'ext' else c, a) for a in ARMS]; S[f'{k}|{c}'] = v; m = min(v)
        P(f"| {'DS03–DS08' if k == 'ext' else k} | {lab} | " + ' | '.join(f'**{x:.2f}**' if x == m else f'{x:.2f}' for x in v) + ' |')
M = []; M.append('| Data | Scenario | ' + ' | '.join(HEAD) + ' |'); M.append('|---|---|' + '---|' * 5)
for lab, c, e in SCS:
    v = np.mean([S[f'{fd}|{c}'] for fd in FDS], 0); S[f'cmapss_mean|{c}'] = v.tolist(); m = v.min()
    M.append(f'| C-MAPSS (mean of four subsets) | {lab} | ' + ' | '.join(f'**{x:.2f}**' if x == m else f'{x:.2f}' for x in v) + ' |')
for lab, c, e in SCS:
    v = S[f'ext|{c}']; m = min(v); M.append(f'| DS03–DS08 | {lab} | ' + ' | '.join(f'**{x:.2f}**' if x == m else f'{x:.2f}' for x in v) + ' |')
wins = {a: sum(int(np.argmin(S[f'{k}|{c}']) == i) for k in FDS + ['ext'] for _, c, _ in SCS) for i, a in enumerate(ARMS)}; S['wins'] = wins
worst = {a: max(S[f'{k}|{c}'][i] - min(S[f'{k}|{c}']) for k in FDS + ['ext'] for _, c, _ in SCS) for i, a in enumerate(ARMS)}; S['max_excess'] = worst
P(f"\nLowest RMSE in the 25 rows: {', '.join(f'{h} {wins[a]}' for a, h in zip(ARMS, HEAD))}. Largest excess over the best arm of a row (cycles): {', '.join(f'{h} {worst[a]:.2f}' for a, h in zip(ARMS, HEAD))}.")
open(f'{B}/analysis/tables_tradeoff.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n'); open(f'{B}/analysis/table9_main.md', 'w', encoding='utf-8').write('\n'.join(M) + '\n')
json.dump(S, open(f'{B}/analysis/summary_tradeoff.json', 'w'), indent=1); print('\n'.join(L).replace('–', '-')); print('\n'.join(M).replace('–', '-'))
