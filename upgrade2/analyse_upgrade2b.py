"""Analysis of upgrade step 2 after the amendment (external-cohort selection by profile group). Identical to analyse_upgrade2.py except for the input and output files."""
import json, os, numpy as np
from scipy.stats import wilcoxon
H = os.path.dirname(os.path.abspath(__file__)); FDS = ['FD001', 'FD002', 'FD003', 'FD004']; BBS = [('tcn', 'TCN'), ('tf', 'Transformer')]
rm = lambda e: float(np.sqrt(np.mean(np.square(e))))
def boot(d, n=10000):
    r = np.random.default_rng(0); d = np.asarray(d); return [float(v) for v in np.percentile([d[r.integers(0, len(d), len(d))].mean() for _ in range(n)], [2.5, 97.5])]
def holm(ps):
    ps = np.asarray(ps); o = np.argsort(ps); adj = np.empty(len(ps)); run = 0
    for r, i in enumerate(o): run = max(run, (len(ps) - r) * ps[i]); adj[i] = min(1, run)
    return adj
def pair(x, y):
    d = np.asarray(x) - np.asarray(y); return dict(d=float(d.mean()), ci=boot(d), nb=int((d < 0).sum()), n=len(d), p=1.0 if np.allclose(d, 0) else float(wilcoxon(x, y).pvalue))
fmt = lambda r: f"{r['d']:+.2f} [{r['ci'][0]:+.2f}, {r['ci'][1]:+.2f}]; {r['nb']}/{r['n']}; p = {r['p']:.2g}; Holm {r['holm']:.2g}"
S = {}; L = []; P = lambda *a: L.append(' '.join(map(str, a)))
LAB = {'k1': 'k = 1', 'k5': 'k = 5', 'irr5': 'irr 1–5', 'full': 'complete', 'h10': 'last 10', 'h5': 'last 5', 'h3': 'last 3'}
C1 = ['A1', 'A2', 'A3', 'A5', 'A6', 'A8']; C2 = ['S1', 'S2', 'S4']
for bb, name in BBS:
    R = {fd: [json.load(open(f'{H}/results/bbc_{bb}_{fd}_s{s}.json')) for s in range(5)] for fd in FDS}
    E = [json.load(open(f'{H}/results/bbe2_{bb}_s{s}.json')) for s in range(5)]; units = sorted(E[0])
    prof = {u: (f"DS05-07_{u.split('_')[1]}" if u.split('_')[0] in ('DS05', 'DS06', 'DS07') else u) for u in units}; groups = sorted(set(prof.values()))
    g = lambda x: np.array([np.mean([x[i] for i, u in enumerate(units) if prof[u] == k]) for k in groups])
    us = lambda sc, a: np.mean([[rm(r[u][sc][a]) for u in units] for r in E], 0)
    mae = lambda fd, sc, a: np.mean([np.abs(r[sc][a]) for r in R[fd]], 0)
    rms = lambda fd, sc, a: [rm(r[sc][a]) for r in R[fd]]
    sel = {d_: json.load(open(f'{H}/results/sel_{bb}_{d_}.json')) for d_ in FDS}; sel['ext'] = json.load(open(f'{H}/results/sel_{bb}_ext_g.json')); S[f'{bb}|sel'] = {d_: {a: v['cfg'] for a, v in s_.items()} for d_, s_ in sel.items()}
    P(f'## {name}: RMSE (cycles)\n'); P('C-MAPSS: mean ± s.d. over five seeds. DS03–DS08: mean unit RMSE, fixed models, five seeds.\n')
    P('| Data | Scenario | ' + ' | '.join(C1) + ' |'); P('|---|---|' + '---|' * len(C1))
    for fd in FDS:
        for sc in ('k1', 'k5', 'irr5'):
            for a in C1: S[f'{bb}|{fd}|{sc}|{a}'] = dict(rmse=float(np.mean(rms(fd, sc, a))), sd=float(np.std(rms(fd, sc, a), ddof=1)))
            P(f'| {fd} | {LAB[sc]} | ' + ' | '.join(f"{S[f'{bb}|{fd}|{sc}|{a}']['rmse']:.2f} ± {S[f'{bb}|{fd}|{sc}|{a}']['sd']:.2f}" for a in C1) + ' |')
    for sc in ('k1', 'k5', 'irr5'):
        for a in C1: S[f'{bb}|ext|{sc}|{a}'] = dict(rmse=float(us(sc, a).mean()))
        P(f'| DS03–DS08 | {LAB[sc]} | ' + ' | '.join(f"{S[f'{bb}|ext|{sc}|{a}']['rmse']:.2f}" for a in C1) + ' |')
    P(''); P('| Data | History | ' + ' | '.join(C2) + ' |'); P('|---|---|' + '---|' * len(C2))
    for fd in FDS:
        for sc in ('full', 'h10', 'h5'):
            for a in C2: S[f'{bb}|{fd}|{sc}|{a}'] = dict(rmse=float(np.mean(rms(fd, sc, a))), sd=float(np.std(rms(fd, sc, a), ddof=1)))
            P(f'| {fd} | {LAB[sc]} | ' + ' | '.join(f"{S[f'{bb}|{fd}|{sc}|{a}']['rmse']:.2f} ± {S[f'{bb}|{fd}|{sc}|{a}']['sd']:.2f}" for a in C2) + ' |')
    for sc in ('full', 'h5', 'h3'):
        for a in C2: S[f'{bb}|ext|{sc}|{a}'] = dict(rmse=float(us(sc, a).mean()))
        P(f'| DS03–DS08 | {LAB[sc]} | ' + ' | '.join(f"{S[f'{bb}|ext|{sc}|{a}']['rmse']:.2f}" for a in C2) + ' |')
    P(f'\n### {name}: comparisons\n'); P('Δ: arm minus reference; C-MAPSS seed-averaged engine absolute error, DS03–DS08 group RMSE; [95% CI]; units better; Wilcoxon p; Holm within family.\n')
    P('| Comparison | Data | Scenario | Arm | Reference | Δ |'); P('|---|---|---|---|---|---|')
    for tag, arm, cands, csc, esc in (('G1', 'A5', ['A1', 'A2', 'A3'], ['k5', 'irr5'], ['k5', 'irr5']), ('G2', 'A8', ['A6'], ['k5', 'irr5'], ['k5', 'irr5']), ('G3', 'S4', ['S1', 'S2'], ['h10', 'h5'], ['h5', 'h3'])):
        rows = []
        for fd in FDS:
            for sc in csc:
                ref = min(cands, key=lambda a: S[f'{bb}|{fd}|{sc}|{a}']['rmse']); r = pair(mae(fd, sc, arm), mae(fd, sc, ref)); r.update(ref=ref, data=fd, sc=sc); rows.append(r)
        for r, a in zip(rows, holm([r['p'] for r in rows])): r['holm'] = float(a)
        erows = []
        for sc in esc:
            ref = min(cands, key=lambda a: S[f'{bb}|ext|{sc}|{a}']['rmse']); r = pair(g(us(sc, arm)), g(us(sc, ref))); r.update(ref=ref, data='DS03–DS08', sc=sc); erows.append(r)
        for r, a in zip(erows, holm([r['p'] for r in erows])): r['holm'] = float(a)
        for r in rows + erows: P(f"| {tag} | {r['data']} | {LAB[r['sc']]} | {arm} | {r['ref']} | {fmt(r)} |")
        nc = int(sum(r['holm'] < 0.05 and r['d'] < 0 for r in rows)); ne = int(sum(r['holm'] < 0.05 and r['d'] < 0 for r in erows))
        nw = int(sum(r['holm'] < 0.05 and r['d'] > 0 for r in rows + erows))
        verdict = 'carries over' if nc >= 6 and ne == 2 else 'partly' if (nc >= 6 or ne == 2) else 'does not carry over'
        S[f'{bb}|{tag}'] = dict(c=rows, e=erows, n_c=nc, n_e=ne, n_worse=nw, verdict=verdict)
    cost = []
    for fd in FDS:
        cost.append(dict(pair(mae(fd, 'k1', 'A5'), mae(fd, 'k1', 'A1')), data=fd, cmp='A5 vs A1')); cost.append(dict(pair(mae(fd, 'full', 'S4'), mae(fd, 'full', 'S1')), data=fd, cmp='S4 vs S1'))
    cost.append(dict(pair(g(us('k1', 'A5')), g(us('k1', 'A1'))), data='DS03–DS08', cmp='A5 vs A1')); cost.append(dict(pair(g(us('full', 'S4')), g(us('full', 'S1'))), data='DS03–DS08', cmp='S4 vs S1'))
    S[f'{bb}|cost'] = cost
    P('\nComplete records: ' + '; '.join(f"{c['data']} {c['cmp']} {c['d']:+.2f} [{c['ci'][0]:+.2f}, {c['ci'][1]:+.2f}] (p = {c['p']:.2g})" for c in cost) + '.')
    P('\nPre-specified reading: ' + '; '.join(f"{t} {S[f'{bb}|{t}']['verdict']} (C-MAPSS {S[f'{bb}|{t}']['n_c']}/8, DS03–DS08 {S[f'{bb}|{t}']['n_e']}/2, significantly worse {S[f'{bb}|{t}']['n_worse']})" for t in ('G1', 'G2', 'G3')) + '.')
    P('\nSelected configurations (width, learning rate): ' + '; '.join(f"{d_}: " + ', '.join(f"{a} {tuple(c)}" for a, c in v.items()) for d_, v in S[f'{bb}|sel'].items()) + '.\n')
json.dump(S, open(f'{H}/summary_upgrade2b.json', 'w'), indent=1, default=float); open(f'{H}/tables_upgrade2b.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('\n'.join(L))
