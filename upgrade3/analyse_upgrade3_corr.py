"""Correction of the Q2 analysis of step 3 after independent verification (2026-11-17). No model is retrained.
(1) Holm correction of the sparse-record comparisons, as the general rule of the protocol requires (families: 8 C-MAPSS, 2 external cohort).
(2) The best test-time remedy is taken among A1, A2 and A3 (carry-forward). A3 was not stored by q3g.py/extg.py; its errors come from the five-seed runs
    of the same dense models (data/q3d_*.json, upgrade1/results/ext_s*.json), after checking that the A1 errors of both runs are identical.
(3) Actual share of complete training windows for each r.
analyse_upgrade3.py and its output are left as they were."""
import json, os, numpy as np
from scipy.stats import wilcoxon
H = os.path.dirname(os.path.abspath(__file__)); B = os.path.dirname(H); FDS = ['FD001', 'FD002', 'FD003', 'FD004']; RS = ['0.0', '0.25', '0.5', '0.75']
rm = lambda e: float(np.sqrt(np.mean(np.square(e))))
def boot(d, n=10000):
    r = np.random.default_rng(0); d = np.asarray(d); return [float(v) for v in np.percentile([d[r.integers(0, len(d), len(d))].mean() for _ in range(n)], [2.5, 97.5])]
def holm(ps):
    ps = np.asarray(ps); o = np.argsort(ps); adj = np.empty(len(ps)); run = 0
    for r, i in enumerate(o): run = max(run, (len(ps) - r) * ps[i]); adj[i] = min(1, run)
    return adj
def pair(x, y):
    d = np.asarray(x) - np.asarray(y); return dict(d=float(d.mean()), ci=boot(d), nb=int((d < 0).sum()), n=len(d), p=float(wilcoxon(x, y).pvalue))
fmt = lambda r: f"{r['d']:+.2f} [{r['ci'][0]:+.2f}, {r['ci'][1]:+.2f}]; {r['nb']}/{r['n']}; p = {r['p']:.2g}; Holm {r['holm']:.2g}; ref. {r['ref']}"
R = {fd: [json.load(open(f'{H}/results/q3g_{fd}_s{s}.json')) for s in range(5)] for fd in FDS}
D = {fd: [json.load(open(f'{B}/data/q3d_{fd}_s{s}.json')) for s in range(5)] for fd in FDS}
E = [json.load(open(f'{H}/results/extg_s{s}.json')) for s in range(5)]; E1 = [json.load(open(f'{B}/upgrade1/results/ext_s{s}.json')) for s in range(5)]; units = sorted(E[0])
for fd in FDS:
    for s in range(5):
        for sc in ('k5', 'irr5'):
            for a in ('A1', 'A2'): assert np.allclose(R[fd][s][sc][a], D[fd][s][sc][a], atol=1e-3), (fd, s, sc, a)
            R[fd][s][sc]['A3'] = D[fd][s][sc]['A3']
for s in range(5):
    assert sorted(E1[s]) == units
    for u in units:
        for sc in ('k5', 'irr5'):
            for a in ('A1', 'A2'): assert np.allclose(E[s][u][sc][a], E1[s][u][sc][a], atol=1e-3), (s, u, sc, a)
            E[s][u][sc]['A3'] = E1[s][u][sc]['A3']
prof = {u: (f"DS05-07_{u.split('_')[1]}" if u.split('_')[0] in ('DS05', 'DS06', 'DS07') else u) for u in units}; groups = sorted(set(prof.values()))
g = lambda x: np.array([np.mean([x[i] for i, u in enumerate(units) if prof[u] == k]) for k in groups])
us = lambda sc, a: np.mean([[rm(r[u][sc][a]) for u in units] for r in E], 0)
mae = lambda fd, sc, a: np.mean([np.abs(r[sc][a]) for r in R[fd]], 0)
rms = lambda fd, sc, a: float(np.mean([rm(r[sc][a]) for r in R[fd]]))
SEL = {fd: json.load(open(f'{H}/results/selr_{fd}.json'))['rstar'] for fd in FDS}; SEL['ext'] = json.load(open(f'{H}/results/selr_ext.json'))['rstar']
REM = ('A1', 'A2', 'A3'); S = {}; L = []; P = lambda *a: L.append(' '.join(map(str, a)))
ref = {}
for sc in ('k5', 'irr5'):
    for fd in FDS: ref[(fd, sc)] = min(REM, key=lambda b: rms(fd, sc, b)); S[f'remedy|{fd}|{sc}'] = {b: rms(fd, sc, b) for b in REM}
    ref[('ext', sc)] = min(REM, key=lambda b: float(us(sc, b).mean())); S[f'remedy|ext|{sc}'] = {b: float(us(sc, b).mean()) for b in REM}
def gain(k, sc, a):
    b = ref[(k, sc)]; return dict(pair(g(us(sc, a)), g(us(sc, b))) if k == 'ext' else pair(mae(k, sc, a), mae(k, sc, b)), ref=b, data=k, sc=sc)
def family(arm_of):
    c = [gain(fd, sc, arm_of(fd)) for fd in FDS for sc in ('k5', 'irr5')]; e = [gain('ext', sc, arm_of('ext')) for sc in ('k5', 'irr5')]
    for rows in (c, e):
        for r, h in zip(rows, holm([r['p'] for r in rows])): r['holm'] = float(h)
    return {(r['data'], r['sc']): r for r in c + e}
NAME = lambda k: 'DS03–DS08' if k == 'ext' else k
P('## Table S32. Q2 after correction: Holm-adjusted sparse-record comparisons, carry-forward included among the test-time remedies\n')
P('Correction made after independent verification, without retraining. The best test-time remedy is the one of A1, A2 and A3 with the lowest RMSE (five seeds); the errors of A3 come from the five-seed runs of the same dense models. '
  'Holm adjustment within the eight C-MAPSS comparisons and within the two external-cohort comparisons of each row group. Δ in seed-averaged engine absolute error (C-MAPSS) or group RMSE (DS03–DS08), cycles.\n')
P('RMSE of the remedies (A1 / A2 / A3): ' + '; '.join(f"{NAME(k)} k = 5 {' / '.join(f'{S[f'remedy|{k}|k5'][b]:.2f}' for b in REM)}, irr 1–5 {' / '.join(f'{S[f'remedy|{k}|irr5'][b]:.2f}' for b in REM)}" for k in FDS + ['ext']) + '.\n')
P('**Models with the selected share r\\*.**\n'); P('| Data | r* | Gain, k = 5 | Gain, irr 1–5 |'); P('|---|---|---|---|')
star = family(lambda k: f'A5r{SEL[k]}'); S['rstar'] = {}
for k in FDS + ['ext']:
    P(f"| {NAME(k)} | {SEL[k]} | {fmt(star[(k, 'k5')])} | {fmt(star[(k, 'irr5')])} |"); S['rstar'][k] = dict(r=SEL[k], gains=[star[(k, 'k5')], star[(k, 'irr5')]])
P('\n**All values of r** (Holm within each value of r).\n'); P('| Data | r | Gain, k = 5 | Gain, irr 1–5 |'); P('|---|---|---|---|'); S['all'] = {}
allr = {r: family(lambda k, r=r: f'A5r{r}') for r in RS}
for k in FDS + ['ext']:
    for r in RS:
        P(f"| {NAME(k)} | {r}{' (r*)' if float(r) == float(SEL[k]) else ''} | {fmt(allr[r][(k, 'k5')])} | {fmt(allr[r][(k, 'irr5')])} |"); S['all'][f'{k}|{r}'] = [allr[r][(k, 'k5')], allr[r][(k, 'irr5')]]
old = json.load(open(f'{H}/summary_upgrade3.json'))['Q2']; verdict = {}
for k in FDS + ['ext']:
    cost = old[f'{k}|{SEL[k]}']['cost']; ok_gain = all(x['holm'] < 0.05 and x['d'] < 0 for x in S['rstar'][k]['gains'])
    verdict[k] = dict(rstar=SEL[k], noninferior=bool(cost['ci'][1] < 1.0), keeps_gain=bool(ok_gain), works=bool(cost['ci'][1] < 1.0 and ok_gain))
S['reading'] = verdict
P('\nReading for Q2 with the corrected comparisons: ' + '; '.join(f"{NAME(k)}: r* = {v['rstar']}, non-inferior with complete records {'yes' if v['noninferior'] else 'no'}, keeps sparse-record advantage (Holm) {'yes' if v['keeps_gain'] else 'no'}" for k, v in verdict.items())
  + f". The rule held on {sum(v['works'] for v in verdict.values())} of 5 data sources.")
# actual share of complete windows: the gap law itself gives a complete window when its regular half draws k = 1 (0.5 x 1/5) or all independent gaps equal 1 (0.5 x 5^-30, negligible)
base = 0.5 / 5 + 0.5 * 5.0 ** -30; S['actual_share'] = {r: float(float(r) + (1 - float(r)) * base) for r in RS}
P('\nActual share of complete training windows: r is the probability of the additional complete branch; the gap law itself yields a complete window with probability 0.10. '
  + '; '.join(f"r = {r}: {100 * v:.1f}%" for r, v in S['actual_share'].items()) + '.')
json.dump({k: v for k, v in S.items()}, open(f'{H}/summary_upgrade3_corr.json', 'w'), indent=1, default=float); open(f'{H}/tables_upgrade3_corr.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('\n'.join(L))
