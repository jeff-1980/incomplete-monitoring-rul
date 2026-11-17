"""Analysis of the battery check, written before the runs (PROTOCOL_realsys.md). Usage: python3 analyse_realsys.py"""
import json, numpy as np
from scipy.stats import wilcoxon
CAPS = {'mit': 450.0, 'xjtu': 250.0}; MARGIN = 0.008          # non-inferiority margin: 0.8% of the RUL cap (1 cycle of 125 in step 3)
S = {}; out = []
P = lambda *a: out.append(' '.join(str(x) for x in a))


def holm(p):
    o = np.argsort(p); adj = np.empty(len(p)); run = 0
    for i, j in enumerate(o): run = max(run, (len(p) - i) * p[j]); adj[j] = min(1.0, run)
    return adj.tolist()


def pair(a, b):
    d = a - b; rng = np.random.default_rng(0); bs = rng.choice(d, (10000, len(d))).mean(1)
    return dict(d=float(d.mean()), ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], p=float(wilcoxon(a, b).pvalue), n=len(d), better=int((d < 0).sum()))


for ds in ('mit', 'xjtu'):
    cell = {}; pooled = {}; rst = []
    for f in range(5):
        J = json.load(open(f'results/rs_{ds}_f{f}.json')); own = np.array(J['owner']); rst.append(J['rstar'])
        for s, A in J['err'].items():
            for a, E in A.items():
                E = np.array(E)                                              # seeds x predictions
                pooled.setdefault((s, a), []).append(E)
                for c in J['test']: cell.setdefault((s, a), {})[c] = float(np.mean(np.sqrt((E[:, own == c] ** 2).mean(1))))   # seed-averaged cell RMSE
    names = sorted(cell[('full', 'DENSE')]); v = lambda s, a: np.array([cell[(s, a)][c] for c in names])
    P(f'## {ds}: {len(names)} cells, selected share per fold {rst}'); P('| Scenario | DENSE | GEN | MIX |'); P('|---|---|---|---|')
    tab = {}
    for s in ('full', 'k10', 'blk'):
        row = []
        for a in ('DENSE', 'GEN', 'MIX'):
            E = np.concatenate(pooled[(s, a)], 1); r = np.sqrt((E ** 2).mean(1)); row.append(f'{r.mean():.1f} ± {r.std(ddof=1):.1f}'); tab[f'{s}|{a}'] = [float(r.mean()), float(r.std(ddof=1))]
        P(f'| {s} | ' + ' | '.join(row) + ' |')
    T = {'R1 GEN vs DENSE, k10': pair(v('k10', 'GEN'), v('k10', 'DENSE')), 'R2 GEN vs DENSE, blk': pair(v('blk', 'GEN'), v('blk', 'DENSE')), 'R3 MIX vs DENSE, k10': pair(v('k10', 'MIX'), v('k10', 'DENSE'))}
    for k, h in zip(T, holm([T[k]['p'] for k in T])): T[k]['holm'] = h; T[k]['sig_better'] = bool(h < 0.05 and T[k]['d'] < 0)
    C = {'cost GEN vs DENSE, full': pair(v('full', 'GEN'), v('full', 'DENSE')), 'cost MIX vs DENSE, full': pair(v('full', 'MIX'), v('full', 'DENSE')),
         'MIX vs GEN, k10': pair(v('k10', 'MIX'), v('k10', 'GEN')), 'MIX vs DENSE, blk': pair(v('blk', 'MIX'), v('blk', 'DENSE'))}
    m = MARGIN * CAPS[ds]
    for k in list(C)[:2]: C[k]['noninferior'] = bool(C[k]['ci'][1] < m)
    P(''); P(f'Paired differences in cell RMSE (cycles; negative: first arm better); non-inferiority margin {m:.1f} cycles'); P('| Comparison | Δ | 95% CI | p | Holm | cells better |'); P('|---|---|---|---|---|---|')
    for k, r in {**T, **C}.items(): P(f"| {k} | {r['d']:+.2f} | {r['ci'][0]:+.2f} to {r['ci'][1]:+.2f} | {r['p']:.2g} | {r.get('holm', float('nan')):.2g} | {r['better']}/{r['n']} |")
    S[ds] = dict(n=len(names), rstar=rst, table=tab, tests=T, descr=C, margin=m,
                 reading=dict(R1=T['R1 GEN vs DENSE, k10']['sig_better'], R2=T['R2 GEN vs DENSE, blk']['sig_better'],
                              R3=bool(T['R3 MIX vs DENSE, k10']['sig_better'] and C['cost MIX vs DENSE, full']['noninferior'])))
    P(''); P('Reading:', S[ds]['reading']); P('')
rd = lambda k: {2: 'carried over', 1: 'carried over in part', 0: 'did not carry over'}[sum(S[d]['reading'][k] for d in S)]
S['overall'] = {k: rd(k) for k in ('R1', 'R2', 'R3')}; P('Overall:', S['overall'])
open('tables_realsys.md', 'w', encoding='utf-8').write('\n'.join(out) + '\n'); json.dump(S, open('summary_realsys.json', 'w'), indent=1); print('\n'.join(out))
