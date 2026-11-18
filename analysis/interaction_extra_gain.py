"""Post hoc analysis from stored predictions (not in any protocol; no retraining; uncorrected):
is the advantage of deletion in training larger with incomplete than with complete records, on the same devices and at the same prediction times?
Extra gain = [err(deletion-trained, scenario) - err(dense, scenario)] - [err(deletion-trained, complete) - err(dense, complete)]; negative: the advantage is larger in the scenario.
Battery: cell RMSE (seed-averaged), GEN and MIX against DENSE (identical prediction times in all scenarios by design).
C-MAPSS: seed-averaged absolute error of each test engine (one prediction per engine), GEN against the dense long-input model A6, and A5 against A1.
DS03-DS08: profile-group RMSE, complete-record predictions restricted to the prediction times of the scenario; GEN against A6, A5 against A1.
Output: analysis/tables_interaction.md, analysis/summary_interaction.json"""
import json, os, numpy as np
from scipy.stats import wilcoxon
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); rm = lambda e: float(np.sqrt(np.mean(np.square(e)))); FDS = ['FD001', 'FD002', 'FD003', 'FD004']; KMAX = 5
def stat(d):
    d = np.asarray(d, float); bs = np.random.default_rng(0).choice(d, (10000, len(d))).mean(1)
    return dict(d=float(d.mean()), ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], p=float(wilcoxon(d).pvalue), n=len(d), neg=int((d < 0).sum()))
f = lambda r: f"{r['d']:+.2f} [{r['ci'][0]:+.2f}, {r['ci'][1]:+.2f}]; p = {r['p']:.2g}; {r['neg']}/{r['n']}"
S = {}; L = ['## Table S37. Is the advantage of deletion in training larger with incomplete than with complete records? (post hoc)\n',
             'From stored predictions; not part of any protocol, no retraining, p values uncorrected. Same devices and same prediction times in both conditions. "Gain, complete" and "gain, scenario": paired difference of the deletion-trained model minus the dense model '
             '(negative: deletion-trained model better). "Extra gain": gain in the scenario minus gain with complete records (negative: the advantage is larger in the scenario). Mean [95% bootstrap interval]; Wilcoxon p; devices with a negative value.\n']
# ---------------- batteries ----------------
L += ['**Battery data** (cell RMSE in cycles, seed-averaged).\n', '| Data | Models | Scenario | Gain, complete | Gain, scenario | Extra gain |', '|---|---|---|---|---|---|']
for ds in ('mit', 'xjtu'):
    cell = {}
    for k in range(5):
        J = json.load(open(f'{B}/realsys/results/rs_{ds}_f{k}.json')); own = np.array(J['owner'])
        for s, A in J['err'].items():
            for a, E in A.items():
                E = np.array(E)
                for c in J['test']: cell.setdefault((s, a), {})[c] = float(np.mean(np.sqrt((E[:, own == c] ** 2).mean(1))))
    N = sorted(cell[('full', 'DENSE')]); v = lambda s, a: np.array([cell[(s, a)][c] for c in N])
    for arm in ('GEN', 'MIX'):
        g0 = v('full', arm) - v('full', 'DENSE')
        for sc, lab in (('k10', 'one record in 10 cycles'), ('blk', 'outage of 50 cycles')):
            g1 = v(sc, arm) - v(sc, 'DENSE'); r = dict(g0=stat(g0), g1=stat(g1), extra=stat(g1 - g0)); S[f'{ds}|{arm}|{sc}'] = r
            L.append(f"| {ds.upper()} | {arm} vs DENSE | {lab} | {f(r['g0'])} | {f(r['g1'])} | {f(r['extra'])} |")
# ---------------- C-MAPSS ----------------
L += ['', '**C-MAPSS** (seed-averaged absolute error of each test engine, cycles; five seeds).\n', '| Subset | Models | Scenario | Gain, complete | Gain, scenario | Extra gain |', '|---|---|---|---|---|---|']
LAB = {'k5': 'k = 5', 'irr5': 'irr 1–5', 'blk10': 'block 10', 'blk20': 'block 20', 'blk5': 'block 5'}
for fd in FDS:
    R = [json.load(open(f'{B}/upgrade3/results/q3g_{fd}_s{s}.json')) for s in range(5)]; mae = lambda sc, a: np.mean([np.abs(r[sc][a]) for r in R], 0)
    for arm, ref, nm in (('GEN', 'A6', 'GEN vs A6'), ('A5r0.0', 'A1', 'A5 vs A1')):
        g0 = mae('k1', arm) - mae('k1', ref)
        for sc in ('k5', 'irr5', 'blk10', 'blk20'):
            g1 = mae(sc, arm) - mae(sc, ref); r = dict(g0=stat(g0), g1=stat(g1), extra=stat(g1 - g0)); S[f'{fd}|{nm}|{sc}'] = r
            L.append(f"| {fd} | {nm} | {LAB[sc]} | {f(r['g0'])} | {f(r['g1'])} | {f(r['extra'])} |")
# ---------------- external cohort ----------------
L += ['', '**DS03–DS08** (profile-group RMSE in cycles, seed-averaged; complete-record predictions restricted to the prediction times of the scenario).\n', '| Data | Models | Scenario | Gain, complete | Gain, scenario | Extra gain |', '|---|---|---|---|---|---|']
E = [json.load(open(f'{B}/upgrade3/results/extg_s{s}.json')) for s in range(5)]; units = sorted(E[0])
prof = {u: (f"DS05-07_{u.split('_')[1]}" if u.split('_')[0] in ('DS05', 'DS06', 'DS07') else u) for u in units}; groups = sorted(set(prof.values()))
g = lambda x: np.array([np.mean([x[i] for i, u in enumerate(units) if prof[u] == k]) for k in groups])
def times(u, ui, sc):
    T = len(E[0][u]['k1']['A1']) + 10
    if sc.startswith('blk'): return np.arange(10, T)
    if sc == 'k5': obs = np.arange(0, T, 5)
    else: c = np.cumsum(np.r_[0, np.random.default_rng(1000 + ui).integers(1, KMAX + 1, T)]); obs = c[c < T]
    return obs[obs >= 10]
for arm, ref, nm in (('GEN', 'A6', 'GEN vs A6'), ('A5r0.0', 'A1', 'A5 vs A1')):
    for sc in ('k5', 'irr5', 'blk5', 'blk10'):
        u0 = {a: [] for a in (arm, ref)}; u1 = {a: [] for a in (arm, ref)}
        for ui, u in enumerate(units):
            t = times(u, ui, sc); assert len(t) == len(E[0][u][sc][arm]), (u, sc)
            for a in (arm, ref):
                u0[a].append(np.mean([rm(np.array(r[u]['k1'][a])[t - 10]) for r in E])); u1[a].append(np.mean([rm(r[u][sc][a]) for r in E]))
        g0 = g(u0[arm]) - g(u0[ref]); g1 = g(u1[arm]) - g(u1[ref]); r = dict(g0=stat(g0), g1=stat(g1), extra=stat(g1 - g0)); S[f'ext|{nm}|{sc}'] = r
        L.append(f"| DS03–DS08 | {nm} | {LAB[sc]} | {f(r['g0'])} | {f(r['g1'])} | {f(r['extra'])} |")
json.dump(S, open(f'{B}/analysis/summary_interaction.json', 'w'), indent=1); open(f'{B}/analysis/tables_interaction.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('\n'.join(L).replace('–', '-'))
