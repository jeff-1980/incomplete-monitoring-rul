"""Analysis of upgrade step 3, as fixed in PROTOCOL_upgrade3.md. Written before the results were inspected."""
import json, os, numpy as np
from scipy.stats import wilcoxon
H = os.path.dirname(os.path.abspath(__file__)); FDS = ['FD001', 'FD002', 'FD003', 'FD004']; RS = ['0.0', '0.25', '0.5', '0.75']
rm = lambda e: float(np.sqrt(np.mean(np.square(e))))
def boot(d, n=10000):
    r = np.random.default_rng(0); d = np.asarray(d); return [float(v) for v in np.percentile([d[r.integers(0, len(d), len(d))].mean() for _ in range(n)], [2.5, 97.5])]
def holm(ps):
    ps = np.asarray(ps); o = np.argsort(ps); adj = np.empty(len(ps)); run = 0
    for r, i in enumerate(o): run = max(run, (len(ps) - r) * ps[i]); adj[i] = min(1, run)
    return adj
def pair(x, y):
    d = np.asarray(x) - np.asarray(y); return dict(d=float(d.mean()), ci=boot(d), nb=int((d < 0).sum()), n=len(d), p=1.0 if np.allclose(d, 0) else float(wilcoxon(x, y).pvalue))
def fmt(r): return f"{r['d']:+.2f} [{r['ci'][0]:+.2f}, {r['ci'][1]:+.2f}]; {r['nb']}/{r['n']}; p = {r['p']:.2g}" + (f"; Holm {r['holm']:.2g}" if 'holm' in r else '')
S = {}; L = []; P = lambda *a: L.append(' '.join(map(str, a)))
R = {fd: [json.load(open(f'{H}/results/q3g_{fd}_s{s}.json')) for s in range(5)] for fd in FDS}
E = [json.load(open(f'{H}/results/extg_s{s}.json')) for s in range(5)]; units = sorted(E[0])
prof = {u: (f"DS05-07_{u.split('_')[1]}" if u.split('_')[0] in ('DS05', 'DS06', 'DS07') else u) for u in units}; groups = sorted(set(prof.values()))
g = lambda x: np.array([np.mean([x[i] for i, u in enumerate(units) if prof[u] == k]) for k in groups])
us = lambda sc, a: np.mean([[rm(r[u][sc][a]) for u in units] for r in E], 0)
mae = lambda fd, sc, a: np.mean([np.abs(r[sc][a]) for r in R[fd]], 0)
rms = lambda fd, sc, a: [rm(r[sc][a]) for r in R[fd]]
SEL = {fd: json.load(open(f'{H}/results/selr_{fd}.json')) for fd in FDS}; SEL['ext'] = json.load(open(f'{H}/results/selr_ext.json'))
CS = ['k1', 'k5', 'irr5', 'blk10', 'blk20', 'bern']; ES = ['k1', 'k5', 'irr5', 'blk5', 'blk10', 'bern']
LAB = {'k1': 'k = 1', 'k5': 'k = 5', 'irr5': 'irr 1–5', 'blk5': 'block 5', 'blk10': 'block 10', 'blk20': 'block 20', 'bern': 'random deletion'}
ARMS = ['A1', 'A2', 'A6', 'A6M', 'GEN', 'A8F'] + [f'A5r{r}' for r in RS]
NM = {'A1': 'A1', 'A2': 'A2', 'A6': 'A6', 'A6M': 'A6M', 'GEN': 'GEN', 'A8F': 'A8F', 'A5r0.0': 'A5 r=0', 'A5r0.25': 'A5 r=0.25', 'A5r0.5': 'A5 r=0.5', 'A5r0.75': 'A5 r=0.75'}
P('## Table S28. Generic deletion, training mixture and smoothing: RMSE (cycles)\n')
P('C-MAPSS: mean ± s.d. over five seeds. DS03–DS08: mean unit RMSE, fixed models. GEN: generic random deletion matched in expected number of records; A6M: consecutive cycles with moving-average smoothing; A8F: DMWT gap law (all three: long every-cycle input, full span). A5 r: gap-channel model trained with a share r of complete windows.\n')
P('| Data | Scenario | ' + ' | '.join(NM[a] for a in ARMS) + ' |'); P('|---|---|' + '---|' * len(ARMS))
for fd in FDS:
    for sc in CS:
        for a in ARMS: S[f'c|{fd}|{sc}|{a}'] = dict(rmse=float(np.mean(rms(fd, sc, a))), sd=float(np.std(rms(fd, sc, a), ddof=1)))
        P(f'| {fd} | {LAB[sc]} | ' + ' | '.join(f"{S[f'c|{fd}|{sc}|{a}']['rmse']:.2f} ± {S[f'c|{fd}|{sc}|{a}']['sd']:.2f}" for a in ARMS) + ' |')
for sc in ES:
    for a in ARMS: S[f'e|{sc}|{a}'] = float(us(sc, a).mean())
    P(f'| DS03–DS08 | {LAB[sc]} | ' + ' | '.join(f"{S[f'e|{sc}|{a}']:.2f}" for a in ARMS) + ' |')
def fam(a, b, tag, scs=('k5', 'irr5')):
    rows = [dict(pair(mae(fd, sc, a), mae(fd, sc, b)), data=fd, sc=sc) for fd in FDS for sc in scs]
    for r, h in zip(rows, holm([r['p'] for r in rows])): r['holm'] = float(h)
    erows = [dict(pair(g(us(sc, a)), g(us(sc, b))), data='DS03–DS08', sc=sc) for sc in scs]
    for r, h in zip(erows, holm([r['p'] for r in erows])): r['holm'] = float(h)
    S[tag] = dict(a=a, b=b, c=rows, e=erows, c_better=int(sum(r['holm'] < 0.05 and r['d'] < 0 for r in rows)), c_worse=int(sum(r['holm'] < 0.05 and r['d'] > 0 for r in rows)),
                  e_better=int(sum(r['holm'] < 0.05 and r['d'] < 0 for r in erows)), e_worse=int(sum(r['holm'] < 0.05 and r['d'] > 0 for r in erows)))
    return rows + erows
def show(title, a, b, tag, scs=('k5', 'irr5')):
    P(f'\n**{title}: {NM[a]} minus {NM[b]}.**\n'); P('| Data | Scenario | Δ [95% CI]; units better; p; Holm |'); P('|---|---|---|')
    for r in fam(a, b, tag, scs): P(f"| {r['data']} | {LAB[r['sc']]} | {fmt(r)} |")
    t = S[tag]; P(f"\nHolm-significant in favour of {NM[a]}: C-MAPSS {t['c_better']}/8, DS03–DS08 {t['e_better']}/2; in favour of {NM[b]}: {t['c_worse']}/8, {t['e_worse']}/2.")
# ---------------- Q1 ----------------
P('\n## Table S29. Q1: generic random deletion versus the DMWT gap law\n')
show('Q1a exposure to deletion', 'GEN', 'A6', 'Q1a'); show('Q1b matching the sampling structure', 'A8F', 'GEN', 'Q1b')
q1 = ('exposure to deletion is enough' if S['Q1a']['c_better'] >= 6 and S['Q1b']['c_better'] <= 2 else
      'matching the sampling structure adds value' if S['Q1b']['c_better'] >= 6 and S['Q1b']['e_better'] == 2 else 'partial')
S['Q1_reading'] = q1
for sc in ('k5', 'irr5'):
    rows = [r for r in S['Q1b']['c'] if r['sc'] == sc]; P(f"A8F vs GEN at {LAB[sc]} on C-MAPSS: Δ {min(r['d'] for r in rows):+.2f} to {max(r['d'] for r in rows):+.2f}; significantly better in {sum(r['holm'] < 0.05 and r['d'] < 0 for r in rows)}/4, worse in {sum(r['holm'] < 0.05 and r['d'] > 0 for r in rows)}/4.")
other = []
for sc_c, sc_e in (('bern', 'bern'), ('blk10', 'blk5'), ('blk20', 'blk10'), ('k1', 'k1')):
    rc = [pair(mae(fd, sc_c, 'A8F'), mae(fd, sc_c, 'GEN')) for fd in FDS]; re_ = pair(g(us(sc_e, 'A8F')), g(us(sc_e, 'GEN')))
    S[f'Q1b_other|{sc_c}'] = dict(c=rc, e=re_); other.append(f"{LAB[sc_c]}: C-MAPSS Δ " + ', '.join(f"{r['d']:+.2f} (p = {r['p']:.2g})" for r in rc) + f"; DS03–DS08 ({LAB[sc_e]}) {re_['d']:+.2f} (p = {re_['p']:.2g})")
P('\nA8F minus GEN in the other scenarios (uncorrected): ' + '; '.join(other) + '.'); P(f'\nPre-specified reading for Q1: {q1}.')
# ---------------- Q2 ----------------
P('\n## Table S30. Q2: share r of complete windows in training (gap-channel model)\n')
P('Selection on validation units only (seed 0): validation RMSE with complete records / at k = 5 / score, and the selected r*.\n')
P('| Data | ' + ' | '.join(f'r = {r}' for r in RS) + ' | r* |'); P('|---|' + '---|' * (len(RS) + 1))
for k in FDS + ['ext']:
    sc = SEL[k]['scores']; P(f"| {'DS03–DS08' if k == 'ext' else k} | " + ' | '.join(f"{sc[r]['k1']:.2f} / {sc[r]['k5']:.2f} / {sc[r]['score']:.2f}" for r in RS) + f" | {SEL[k]['rstar']} |")
P('\nTest results. Cost: Δ against the dense model A1 with complete records. Gain: Δ against the best test-time remedy (A1 or A2, by RMSE) at k = 5 and irregular 1–5. Δ in seed-averaged engine absolute error (C-MAPSS) or group RMSE (DS03–DS08) with 95% interval and uncorrected p.\n')
P('| Data | r | Cost, complete records | Gain, k = 5 | Gain, irr 1–5 | RMSE block (10 / 20 or 5 / 10) |'); P('|---|---|---|---|---|---|')
Q2 = {}
for k in FDS + ['ext']:
    for r in RS:
        a = f'A5r{r}'
        if k == 'ext':
            cost = pair(g(us('k1', a)), g(us('k1', 'A1'))); gains = []
            for sc in ('k5', 'irr5'):
                ref = min(('A1', 'A2'), key=lambda b: S[f'e|{sc}|{b}']); gains.append(dict(pair(g(us(sc, a)), g(us(sc, ref))), ref=ref))
            blk = f"{S[f'e|blk5|{a}']:.2f} / {S[f'e|blk10|{a}']:.2f}"
        else:
            cost = pair(mae(k, 'k1', a), mae(k, 'k1', 'A1')); gains = []
            for sc in ('k5', 'irr5'):
                ref = min(('A1', 'A2'), key=lambda b: S[f'c|{k}|{sc}|{b}']['rmse']); gains.append(dict(pair(mae(k, sc, a), mae(k, sc, ref)), ref=ref))
            blk = f"{S[f'c|{k}|blk10|{a}']['rmse']:.2f} / {S[f'c|{k}|blk20|{a}']['rmse']:.2f}"
        Q2[f'{k}|{r}'] = dict(cost=cost, gains=gains)
        star = ' (r*)' if float(r) == float(SEL[k]['rstar']) else ''
        P(f"| {'DS03–DS08' if k == 'ext' else k} | {r}{star} | {fmt(cost)} | {fmt(gains[0])} | {fmt(gains[1])} | {blk} |")
S['Q2'] = Q2; verdict = {}
for k in FDS + ['ext']:
    q = Q2[f"{k}|{SEL[k]['rstar']}"]; ok_cost = q['cost']['ci'][1] < 1.0; ok_gain = all(x['p'] < 0.05 and x['d'] < 0 for x in q['gains'])
    q0 = Q2[f'{k}|0.0']; verdict[k] = dict(rstar=SEL[k]['rstar'], noninferior=bool(ok_cost), keeps_gain=bool(ok_gain), works=bool(ok_cost and ok_gain), noninferior_r0=bool(q0['cost']['ci'][1] < 1.0))
S['Q2_reading'] = verdict
P('\nPre-specified reading for Q2 (model with r*): ' + '; '.join(f"{'DS03–DS08' if k == 'ext' else k}: r* = {v['rstar']}, non-inferior with complete records {'yes' if v['noninferior'] else 'no'} (r = 0: {'yes' if v['noninferior_r0'] else 'no'}), keeps sparse-record advantage {'yes' if v['keeps_gain'] else 'no'}" for k, v in verdict.items()) + '.')
loss = []
for k in FDS + ['ext']:
    a = f"A5r{SEL[k]['rstar']}"
    if float(SEL[k]['rstar']) == 0: loss.append(f"{'DS03–DS08' if k == 'ext' else k}: r* = 0"); continue
    rr = [pair(g(us(sc, a)), g(us(sc, 'A5r0.0'))) if k == 'ext' else pair(mae(k, sc, a), mae(k, sc, 'A5r0.0')) for sc in ('k5', 'irr5')]
    loss.append(f"{'DS03–DS08' if k == 'ext' else k}: {rr[0]['d']:+.2f} (p = {rr[0]['p']:.2g}) and {rr[1]['d']:+.2f} (p = {rr[1]['p']:.2g})")
P('\nModel with r* minus r = 0 at k = 5 and irregular 1–5: ' + '; '.join(loss) + '.')
# ---------------- Q3 ----------------
P('\n## Table S31. Q3: smoothing of the training input\n')
show('Q3a smoothing without deletion', 'A6M', 'A6', 'Q3a'); show('Q3b sparsification beyond smoothing', 'A8F', 'A6M', 'Q3b'); fam('A8F', 'A6', 'Q3ref')
share = []
for i, r in enumerate(S['Q3a']['c'] + S['Q3a']['e']):
    ref = (S['Q3ref']['c'] + S['Q3ref']['e'])[i]; share.append(r['d'] / ref['d'] if ref['d'] < 0 else float('nan'))
S['Q3_share'] = [float(x) for x in share]
q3 = ('not supported' if S['Q3a']['c_better'] <= 2 else ('explains most of the gain' if S['Q3b']['c_better'] <= 2 else 'explains part of the gain') if S['Q3a']['c_better'] >= 6 else 'inconclusive')
S['Q3_reading'] = q3
P(f"\nShare of the A8F gain over A6 recovered by A6M (ratio of mean differences), ten comparisons: {', '.join(f'{x:.2f}' for x in share)}; median {np.nanmedian(share):.2f}.")
P(f'\nPre-specified reading for Q3: {q3}.')
json.dump(S, open(f'{H}/summary_upgrade3.json', 'w'), indent=1, default=float); open(f'{H}/tables_upgrade3.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('\n'.join(L))
