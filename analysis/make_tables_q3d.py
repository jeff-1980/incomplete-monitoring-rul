"""Same-run, 5-seed GPU batch (q3d): all arms trained in one run. Conventional RMSE (per seed, mean ± sd over 5 seeds).
Paired comparisons: engine |error| averaged over seeds, two-sided Wilcoxon, 95% bootstrap CI (exploratory, uncorrected)."""
import json, numpy as np
from scipy.stats import wilcoxon
D = str(__import__('pathlib').Path(__file__).resolve().parents[1]) + '/data'; OUT = str(__import__('pathlib').Path(__file__).resolve().parents[1]) + '/analysis'
FDS = ['FD001', 'FD002', 'FD003', 'FD004']; SC = ['k1', 'k2', 'k3', 'k5', 'irr5', 'irr10']
ARMS = ['A1', 'A2', 'A3', 'A6', 'A5', 'A8', 'B1_GRUD', 'B2s_imputer', 'B3_static', 'B4_PCMambaSDE']
rm = lambda e: float(np.sqrt(np.mean(np.square(e))))
phm = lambda e: np.where(e < 0, np.exp(-e / 13) - 1, np.exp(e / 10) - 1)
def boot(d, B=10000):
    r = np.random.default_rng(0); n = len(d); b = [d[r.integers(0, n, n)].mean() for _ in range(B)]; return np.quantile(b, [.025, .975])
S = {}; L = []; P = lambda *a: L.append(' '.join(map(str, a)))
R = {fd: [json.load(open(f'{D}/q3d_{fd}_s{s}.json')) for s in range(5)] for fd in FDS}
for fd in FDS:  # PC-MambaSDE: separate GPU run, same seeds and test engines
    for s_, r in enumerate(R[fd]):
        m = json.load(open(f'{D}/pcm/q3m_{fd}_s{s_}.json'))
        for sc in SC:
            assert len(m[sc]['B4_PCMambaSDE']) == len(r[sc]['A5']); r[sc]['B4_PCMambaSDE'] = m[sc]['B4_PCMambaSDE']
E = lambda fd, sc, a: np.array([r[sc][a] for r in R[fd]])
P('## Table S14. Same-run 5-seed batch: RMSE (cycles), mean ± s.d. over 5 seeds\n')
P('| Subset | Scenario | ' + ' | '.join(ARMS) + ' |'); P('|---|---|' + '---|' * len(ARMS))
for fd in FDS:
    for sc in SC:
        c = []
        for a in ARMS:
            e = E(fd, sc, a); per = [rm(x) for x in e]
            S[f'{fd}|{sc}|{a}'] = dict(rmse=float(np.mean(per)), sd=float(np.std(per, ddof=1)), bias=float(e.mean()),
                                       phm_med=float(np.median([phm(x).sum() for x in e])), maxlate=float(e.max()))
            c.append(f'{np.mean(per):.2f} ± {np.std(per, ddof=1):.2f}')
        P(f'| {fd} | {sc} | ' + ' | '.join(c) + ' |')
def cmp(fd, sc, a, b):
    x = np.abs(E(fd, sc, a)).mean(0); y = np.abs(E(fd, sc, b)).mean(0); d = x - y; ci = boot(d)
    return dict(d=float(d.mean()), ci=list(map(float, ci)), nb=int((d < 0).sum()), n=len(d), p=float(wilcoxon(x, y).pvalue))
for a, b, title in [('A8', 'A6', 'A8 vs A6 (same history, differ only in training sparsification)'), ('A8', 'A1', 'A8 vs A1 (dense model)'),
                    ('A8', 'A5', 'A8 vs A5'), ('B1_GRUD', 'A5', 'GRU-D vs A5'), ('B2s_imputer', 'A5', 'supervised imputer + dense GRU vs A5'),
                    ('B3_static', 'A5', 'single-snapshot vs A5'), ('A5', 'A1', 'A5 vs A1'), ('A5', 'A2', 'A5 vs A2'), ('A6', 'A5', 'A6 vs A5'), ('B4_PCMambaSDE', 'A5', 'PC-MambaSDE vs A5'), ('B4_PCMambaSDE', 'A8', 'PC-MambaSDE vs A8'), ('B4_PCMambaSDE', 'B1_GRUD', 'PC-MambaSDE vs GRU-D'), ('B4_PCMambaSDE', 'A2', 'PC-MambaSDE vs A2')]:
    P(f'\n## {title}: Δ mean |e| [95% CI]; engines better; p\n'); P('| Subset | ' + ' | '.join(SC) + ' |'); P('|---|' + '---|' * len(SC))
    for fd in FDS:
        c = []
        for sc in SC:
            r = cmp(fd, sc, a, b); S[f'cmp|{a}|{b}|{fd}|{sc}'] = r
            c.append(f"{r['d']:+.2f} [{r['ci'][0]:+.2f},{r['ci'][1]:+.2f}]; {r['nb']}/{r['n']}; p={r['p']:.2g}")
        P(f'| {fd} | ' + ' | '.join(c) + ' |')
P('\n## Table S15. Bias, PHM median and largest late error (same-run batch, k=1 / k=5 / irr5)\n')
P('| Subset | Arm | bias k1/k5/irr5 | PHM median k1/k5/irr5 | largest late error k1/k5/irr5 |'); P('|---|---|---|---|---|')
for fd in FDS:
    for a in ['A1', 'A2', 'A6', 'A5', 'A8', 'B1_GRUD', 'B4_PCMambaSDE']:
        g = [S[f'{fd}|{sc}|{a}'] for sc in ('k1', 'k5', 'irr5')]
        P(f"| {fd} | {a} | {'/'.join(f'{x['bias']:+.1f}' for x in g)} | {'/'.join(f'{x['phm_med']:.0f}' for x in g)} | {'/'.join(f'{x['maxlate']:.0f}' for x in g)} |")
open(f'{OUT}/tables_q3d.md', 'w').write('\n'.join(L) + '\n'); json.dump(S, open(f'{OUT}/summary_q3d.json', 'w'), indent=1)
print('\n'.join(L))
