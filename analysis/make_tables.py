"""Recompute all Q3 manuscript numbers from per-engine signed errors.

C-MAPSS (one prediction per official test engine, last record):
  RMSE_std  = RMSE over engines for each seed, then mean +- s.d. over 3 seeds   (conventional; used in the paper)
  RMSE_exp  = RMSE of the seed-averaged absolute error (as in the experimenter's q3_summary.md; kept for audit)
  Score     = PHM08 asymmetric score (sum over engines), mean over seeds
Statistics (pre-registered): engine is the unit; absolute error averaged over seeds; two-sided Wilcoxon; Holm within H1 family.
N-CMAPSS: unit RMSE (over streamed predictions) per seed, averaged over seeds, then mean over 19 units.
"""
import json, numpy as np
from scipy.stats import wilcoxon

D = str(__import__('pathlib').Path(__file__).resolve().parents[1]) + '/data'
OUT = str(__import__('pathlib').Path(__file__).resolve().parents[1]) + '/analysis'
FDS = ['FD001', 'FD002', 'FD003', 'FD004']; SC = ['k1', 'k2', 'k3', 'k5', 'irr5', 'irr10']
ARMS = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7']
rm = lambda e: float(np.sqrt(np.mean(np.square(e))))
def phm(e): return float(np.sum(np.where(e < 0, np.exp(-e / 13) - 1, np.exp(e / 10) - 1)))
def holm(ps):
    ps = np.asarray(ps); o = np.argsort(ps); m = len(ps); adj = np.empty(m); run = 0
    for i, j in enumerate(o): run = max(run, (m - i) * ps[j]); adj[j] = min(1, run)
    return adj
def boot(d, B=10000, seed=0):
    r = np.random.default_rng(seed); n = len(d)
    b = [d[r.integers(0, n, n)].mean() for _ in range(B)]; return np.quantile(b, [0.025, 0.975])

R = {}
for fd in FDS:
    runs = [json.load(open(f'{D}/q3_{fd}_s{s}.json')) for s in range(3)]
    R[fd] = {sc: {a: np.array([r[sc][a] for r in runs]) for a in runs[0][sc]} for sc in SC}
L = []; P = lambda *a: L.append(' '.join(map(str, a)))
S = {'cmapss': {}, 'ncmapss': {}}
P('## C-MAPSS conventional RMSE (mean ± s.d. over 3 seeds); [experimenter definition in brackets]\n')
P('| Subset | Scenario | ' + ' | '.join(ARMS) + ' |'); P('|---|---|' + '---|' * len(ARMS))
for fd in FDS:
    for sc in SC:
        cells = []
        for a in ARMS:
            if a not in R[fd][sc]: cells.append('—'); continue
            E = R[fd][sc][a]; per = [rm(e) for e in E]
            S['cmapss'][f'{fd}|{sc}|{a}'] = dict(rmse=float(np.mean(per)), sd=float(np.std(per, ddof=1)), rmse_exp=rm(np.abs(E).mean(0)),
                                                 mae=float(np.abs(E).mean()), score=float(np.mean([phm(e) for e in E])))
            cells.append(f'{np.mean(per):.2f}±{np.std(per, ddof=1):.2f} [{rm(np.abs(E).mean(0)):.2f}]')
        P(f'| {fd} | {sc} | ' + ' | '.join(cells) + ' |')

def cmp(fd, sc, a, b):
    x = np.abs(R[fd][sc][a]).mean(0); y = np.abs(R[fd][sc][b]).mean(0); d = x - y
    return float(d.mean()), boot(d), int((d < 0).sum()), len(d), float(wilcoxon(x, y).pvalue)

P('\n## H1 (pre-registered): A5 vs best naive remedy chosen by RMSE; engine-level |error| seed-averaged; Holm over 8\n')
P('| Subset | Scenario | Best naive | its RMSE | A5 RMSE | Δ mean |e| [95% CI] | engines A5 better | p | p_Holm | seeds A5 better |'); P('|---|---|---|---|---|---|---|---|---|---|')
rows = []
for fd in FDS:
    for sc in ['k5', 'irr5']:
        best = min(['A1', 'A2', 'A3'], key=lambda a: S['cmapss'][f'{fd}|{sc}|{a}']['rmse'])
        best_exp = min(['A1', 'A2', 'A3'], key=lambda a: S['cmapss'][f'{fd}|{sc}|{a}']['rmse_exp'])
        d, ci, nb, n, p = cmp(fd, sc, 'A5', best)
        seeds = sum(rm(R[fd][sc]['A5'][s]) < rm(R[fd][sc][best][s]) for s in range(3))
        rows.append([fd, sc, best, S['cmapss'][f'{fd}|{sc}|{best}']['rmse'], S['cmapss'][f'{fd}|{sc}|A5']['rmse'], d, ci, nb, n, p, seeds, best_exp])
adj = holm([r[9] for r in rows])
for r, a in zip(rows, adj):
    P(f'| {r[0]} | {r[1]} | {r[2]}{"" if r[2]==r[11] else " (exp-def: "+r[11]+")"} | {r[3]:.2f} | {r[4]:.2f} | {r[5]:+.2f} [{r[6][0]:+.2f}, {r[6][1]:+.2f}] | {r[7]}/{r[8]} | {r[9]:.2g} | {a:.2g} | {r[10]}/3 |')
S['H1'] = [dict(fd=r[0], sc=r[1], best=r[2], p=r[9], p_holm=float(a), d=r[5], ci=list(map(float, r[6])), nb=r[7], n=r[8]) for r, a in zip(rows, adj)]

for name, a, b, scs in [('H2: k1, A5 vs A1', 'A5', 'A1', ['k1']), ('H3: A5 vs A4 (gap channel)', 'A5', 'A4', SC),
                        ('H4: A5 vs A6 (long window)', 'A5', 'A6', ['k1', 'k5', 'irr5']), ('H5: A5 vs A7 (interval-matched)', 'A5', 'A7', ['k2', 'k3', 'k5'])]:
    P(f'\n## {name}  (Δ mean |e| in cycles [95% CI], engines better, p)\n'); P('| Subset | ' + ' | '.join(scs) + ' |'); P('|---|' + '---|' * len(scs))
    for fd in FDS:
        cs = []
        for sc in scs:
            d, ci, nb, n, p = cmp(fd, sc, a, b); cs.append(f'{d:+.2f} [{ci[0]:+.2f},{ci[1]:+.2f}] ({nb}/{n}, p={p:.2g})')
            S.setdefault(name, {})[f'{fd}|{sc}'] = dict(d=d, ci=list(map(float, ci)), nb=nb, n=n, p=p)
        P(f'| {fd} | ' + ' | '.join(cs) + ' |')

# ---------------- N-CMAPSS ----------------
N = [json.load(open(f'{D}/nq3_s{s}.json')) for s in range(3)]
units = sorted(N[0]); NS = ['k1', 'k5', 'irr5']
def uvec(sc, a): return np.array([np.mean([N[s][u][sc][a] for s in range(3)]) for u in units])
P('\n## N-CMAPSS (19 units, leave-one-unit-out): mean over units of seed-averaged unit RMSE; ± s.d. of the unit-mean across seeds\n')
P('| Scenario | ' + ' | '.join(ARMS) + ' |'); P('|---|' + '---|' * len(ARMS))
for sc in NS:
    cells = []
    for a in ARMS:
        if a not in N[0][units[0]][sc]: cells.append('—'); continue
        per_seed = [np.mean([N[s][u][sc][a] for u in units]) for s in range(3)]
        S['ncmapss'][f'{sc}|{a}'] = dict(rmse=float(np.mean(per_seed)), sd=float(np.std(per_seed, ddof=1)))
        cells.append(f'{np.mean(per_seed):.2f}±{np.std(per_seed, ddof=1):.2f}')
    P(f'| {sc} | ' + ' | '.join(cells) + ' |')
nrows = []
for sc in ['k5', 'irr5']:
    best = min(['A1', 'A2', 'A3'], key=lambda a: S['ncmapss'][f'{sc}|{a}']['rmse'])
    x, y = uvec(sc, 'A5'), uvec(sc, best); d = x - y
    nrows.append((sc, best, float(d.mean()), boot(d), int((d < 0).sum()), float(wilcoxon(x, y).pvalue)))
nadj = holm([r[5] for r in nrows])
P('\nN-CMAPSS H1:')
for r, a in zip(nrows, nadj):
    P(f'{r[0]}: best naive {r[1]}, Δ unit RMSE {r[2]:+.2f} [{r[3][0]:+.2f}, {r[3][1]:+.2f}], {r[4]}/19 better, p={r[5]:.2g}, Holm {a:.2g}')
for sc, a, b in [('k1', 'A5', 'A1'), ('k1', 'A5', 'A4'), ('k5', 'A5', 'A4'), ('irr5', 'A5', 'A4'), ('k1', 'A5', 'A6'), ('k5', 'A5', 'A6'), ('irr5', 'A5', 'A6'), ('k5', 'A5', 'A7')]:
    x, y = uvec(sc, a), uvec(sc, b); d = x - y; ci = boot(d)
    P(f'N-CMAPSS {sc} {a} vs {b}: Δ {d.mean():+.2f} [{ci[0]:+.2f}, {ci[1]:+.2f}], {(d<0).sum()}/19 better, p={wilcoxon(x,y).pvalue:.2g}')
S['ncmapss_H1'] = [dict(sc=r[0], best=r[1], d=r[2], ci=list(map(float, r[3])), nb=r[4], p=r[5], p_holm=float(a)) for r, a in zip(nrows, nadj)]
open(f'{OUT}/tables.md', 'w').write('\n'.join(L) + '\n'); json.dump(S, open(f'{OUT}/summary.json', 'w'), indent=1, default=float)
print('\n'.join(L))
