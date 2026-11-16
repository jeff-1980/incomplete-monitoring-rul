import sys, os, json, glob, numpy as np
from scipy.stats import wilcoxon
R = os.environ.get('Q6_OUT', 'results')
rng = np.random.default_rng(0)
rm = lambda e: float(np.sqrt(np.mean(np.square(e))))


def holm(ps):
    ps = np.asarray(ps); o = np.argsort(ps); m = len(ps); adj = np.empty(m); run = 0
    for i, j in enumerate(o): run = max(run, (m - i) * ps[j]); adj[j] = min(1, run)
    return adj


def boot(d, n=10000):
    i = rng.integers(0, len(d), (n, len(d))); return np.percentile(d[i].mean(1), [2.5, 97.5])


SETS = ['FD001', 'FD002', 'FD003', 'FD004']; HS = ['full', 'h20', 'h10', 'h5']; TEST_H = ['h10', 'h5']
RUNS = {s: [json.load(open(f)) for f in sorted(glob.glob(f'{R}/q6_{s}_s*.json'))] for s in SETS}


def E(s, h, a):
    A = np.array([r[h][a] for r in RUNS[s]]); return A, [rm(x) for x in A]


def eng(s, h, a): return np.abs(E(s, h, a)[0]).mean(0)


ARMS = ['A1', 'A2', 'B3', 'B4', 'B2']
L = []; P = lambda *a: L.append(' '.join(map(str, a)))
P('## Main table: RMSE per seed, mean +- sd (C-MAPSS official test, last window)\n')
P('| set | history | A1 | A2 | B3 | B4 | B2 |'); P('|---|---|---|---|---|---|---|')
for s in SETS:
    for h in HS:
        cells = []
        for a in ARMS:
            if a not in RUNS[s][0][h]: cells.append('-'); continue
            per = E(s, h, a)[1]; cells.append(f'{np.mean(per):.2f} +- {np.std(per):.2f}')
        P(f'| {s} | {h} | ' + ' | '.join(cells) + ' |')
P('\n## H1: B2 vs best naive min(A1,A2), Holm over 8\n')
P('| set | hist | best naive | its RMSE | B2 RMSE | engine diff | B2 better | p | Holm | seeds B2 better |'); P('|---|---|---|---|---|---|---|---|---|---|')
rows = []
for s in SETS:
    for h in TEST_H:
        best = min(['A1', 'A2'], key=lambda a: np.mean(E(s, h, a)[1]))
        x, y = eng(s, h, 'B2'), eng(s, h, best); d = x - y; pb, pn = E(s, h, 'B2')[1], E(s, h, best)[1]
        rows.append((s, h, best, np.mean(pn), np.mean(pb), d.mean(), (d < 0).sum(), len(d), wilcoxon(x, y).pvalue, sum(b < n for b, n in zip(pb, pn)), len(pb)))
adj = holm([r[8] for r in rows]); h1 = 0
for r, q in zip(rows, adj):
    ok = q < 0.05 and r[5] < 0; h1 += ok
    P(f'| {r[0]} | {r[1]} | {r[2]} | {r[3]:.2f} | {r[4]:.2f} | {r[5]:+.2f} | {r[6]}/{r[7]} | {r[8]:.2g} | {q:.2g} | {r[9]}/{r[10]} |')
P(f'\nH1 passed {h1}/8 (need >=7)')
P('\n## H2: full history, B2 vs A1 (bootstrap 95% CI of engine-level |error| diff; pass = not sig. worse AND CI upper < +1.0)\n')
P('| set | A1 RMSE | B2 RMSE | diff | 95% CI | B2 better | p | verdict |'); P('|---|---|---|---|---|---|---|---|'); h2 = 0
for s in SETS:
    x, y = eng(s, 'full', 'B2'), eng(s, 'full', 'A1'); d = x - y; ci = boot(d); p = wilcoxon(x, y).pvalue
    ok = (p >= 0.05 or d.mean() < 0) and ci[1] < 1.0; h2 += ok
    P(f"| {s} | {np.mean(E(s, 'full', 'A1')[1]):.2f} | {np.mean(E(s, 'full', 'B2')[1]):.2f} | {d.mean():+.2f} | [{ci[0]:+.2f}, {ci[1]:+.2f}] | {(d < 0).sum()}/{len(d)} | {p:.2g} | {'pass' if ok else 'fail'} |")
P(f'\nH2 passed {h2}/4 (need 4/4)')
for name, a, b, hs in [('H3: B2 vs B3 (flag channel)', 'B2', 'B3', HS), ('H4: B2 vs B4 (history-length-matched)', 'B2', 'B4', HS[1:])]:
    P(f'\n## {name}\n'); P('| set | ' + ' | '.join(hs) + ' |'); P('|---|' + '---|' * len(hs))
    for s in SETS:
        cs = []
        for h in hs:
            x, y = eng(s, h, a), eng(s, h, b); d = x - y; cs.append(f'{d.mean():+.2f} ({(d < 0).sum()}/{len(d)}, p={wilcoxon(x, y).pvalue:.1g})')
        P(f'| {s} | ' + ' | '.join(cs) + ' |')
P(f'\n**Verdict C-MAPSS: H1 {h1}/8, H2 {h2}/4 -> {"PASS" if h1 >= 7 and h2 == 4 else "FAIL"}**')
open(f'{R}/q6_summary_cmapss.md', 'w').write('\n'.join(L)); print('\n'.join(L))
