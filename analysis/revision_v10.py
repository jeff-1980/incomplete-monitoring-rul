"""Revision v10 analyses (from saved per-engine / per-unit errors; no retraining).
1. Per-seed effects of the confirmatory H1 comparisons (seed = training run) and engine-bootstrap CI of the RMSE difference.
2. N-CMAPSS: equal-group-weight means next to unit-weighted means; formula check.
3. Exploratory non-inferiority of long-input variants with complete records (MAE and RMSE differences, 1-cycle bound).
4. Exploratory mixture analysis: RMSE when a fraction w of predictions uses complete records and 1-w degraded input."""
import json, glob, numpy as np
from scipy.stats import wilcoxon
B = str(__import__('pathlib').Path(__file__).resolve().parents[1]) + ''; D = B + '/data'
FDS = ['FD001', 'FD002', 'FD003', 'FD004']
rm = lambda e: float(np.sqrt(np.mean(np.square(e))))
S = json.load(open(B + '/analysis/summary.json'))
out = {}; L = []; P = lambda *a: L.append(' '.join(map(str, a)))
rng = np.random.default_rng(0)

def boot_rmse_diff(E1, E2, nb=10000):
    """E1, E2: seeds x engines signed errors. Statistic: mean over seeds of RMSE difference. Resample engines (conditional on trained models)."""
    n = E1.shape[1]; r = np.random.default_rng(0); vals = np.empty(nb)
    for b in range(nb):
        i = r.integers(0, n, n)
        vals[b] = np.mean(np.sqrt((E1[:, i] ** 2).mean(1)) - np.sqrt((E2[:, i] ** 2).mean(1)))
    return [float(x) for x in np.percentile(vals, [2.5, 97.5])]

def perseed(E1, E2):
    dr = [rm(a) - rm(b) for a, b in zip(E1, E2)]; dm = [np.abs(a).mean() - np.abs(b).mean() for a, b in zip(E1, E2)]
    return dict(d_rmse=[float(x) for x in dr], d_mae=[float(x) for x in dm], better=int(sum(x < 0 for x in dr)), n=len(dr))

# ---------- 1a. case 1, C-MAPSS pre-specified (3 seeds) ----------
R = {fd: [json.load(open(f'{D}/q3_{fd}_s{s}.json')) for s in range(3)] for fd in FDS}
P('## Table S16. Confirmatory comparisons by training seed\n')
P('Case 1, C-MAPSS (three seeds): A5 minus the best test-time remedy. ΔRMSE per seed; ΔMAE per seed; mean ΔRMSE with 95% engine-bootstrap interval (conditional on the trained models).\n')
P('| Subset | Scenario | Reference | ΔRMSE per seed | ΔMAE per seed | Seeds A5 better | Mean ΔRMSE [95% CI] |'); P('|---|---|---|---|---|---|---|')
for h in S['H1']:
    fd, sc, ref = h['fd'], h['sc'], h['best']
    E1 = np.array([r[sc]['A5'] for r in R[fd]]); E2 = np.array([r[sc][ref] for r in R[fd]])
    ps = perseed(E1, E2); ci = boot_rmse_diff(E1, E2); out[f'c1|{fd}|{sc}'] = dict(ps, ci=ci, ref=ref)
    P(f"| {fd} | {sc} | {ref} | {', '.join(f'{x:+.2f}' for x in ps['d_rmse'])} | {', '.join(f'{x:+.2f}' for x in ps['d_mae'])} | {ps['better']}/{ps['n']} | {np.mean(ps['d_rmse']):+.2f} [{ci[0]:+.2f}, {ci[1]:+.2f}] |")

# ---------- 1b. case 1, N-CMAPSS grouped (3 seeds) ----------
gid = lambda u: u.split('_')[1] if u.split('_')[1] in ('u2', 'u5', 'u10') else u
G = [json.load(open(f'{D}/twin/nq3g_s{s}.json')) for s in range(3)]
units = sorted(G[0]); groups = sorted(set(gid(u) for u in units))
def gvec(x):  # unit vector -> equal-weight group vector
    return np.array([np.mean([x[i] for i, u in enumerate(units) if gid(u) == g]) for g in groups])
P('\nCase 1, N-CMAPSS (twins grouped, three seeds): A5 minus A2; per-seed difference of the equal-weight group mean of unit RMSE.\n')
P('| Scenario | Δ per seed | Seeds A5 better | Unit-weighted means A5 / A2 | Equal-group-weight means A5 / A2 | Δ (group, seed-averaged) |'); P('|---|---|---|---|---|---|')
for sc in ('k5', 'irr5'):
    per = []
    for g in G:
        a = gvec([g[u][sc]['A5'] for u in units]); b = gvec([g[u][sc]['A2'] for u in units]); per.append(float((a - b).mean()))
    ua = np.mean([[g[u][sc]['A5'] for u in units] for g in G], 0); ub = np.mean([[g[u][sc]['A2'] for u in units] for g in G], 0)
    ga, gb = gvec(ua), gvec(ub)
    out[f'n1|{sc}'] = dict(per=per, unit=[float(ua.mean()), float(ub.mean())], group=[float(ga.mean()), float(gb.mean())], d=float((ga - gb).mean()))
    P(f"| {sc} | {', '.join(f'{x:+.2f}' for x in per)} | {sum(x < 0 for x in per)}/3 | {ua.mean():.2f} / {ub.mean():.2f} | {ga.mean():.2f} / {gb.mean():.2f} | {(ga - gb).mean():+.2f} |")

# ---------- 1c. case 2, C-MAPSS (5 seeds) ----------
Q = {fd: [json.load(open(f'{D}/q6/q6_{fd}_s{s}.json')) for s in range(5)] for fd in FDS}
SQ6 = json.load(open(B + '/analysis/summary_q6.json'))
P('\nCase 2, C-MAPSS (five seeds): S4 minus the better of S1/S2.\n')
P('| Subset | History | Reference | ΔRMSE per seed | Seeds S4 better | Mean ΔRMSE [95% CI] |'); P('|---|---|---|---|---|---|')
NM6 = {'A1': 'S1', 'A2': 'S2'}
for fd in FDS:
    for h in ('h10', 'h5'):
        ref = SQ6[f'H1c|{fd}|{h}']['best']
        E1 = np.array([r[h]['B2'] for r in Q[fd]]); E2 = np.array([r[h][ref] for r in Q[fd]])
        ps = perseed(E1, E2); ci = boot_rmse_diff(E1, E2); out[f'c2|{fd}|{h}'] = dict(ps, ci=ci, ref=ref)
        P(f"| {fd} | last {h[1:]} | {NM6[ref]} | {', '.join(f'{x:+.2f}' for x in ps['d_rmse'])} | {ps['better']}/{ps['n']} | {np.mean(ps['d_rmse']):+.2f} [{ci[0]:+.2f}, {ci[1]:+.2f}] |")

# ---------- 1d. case 2, N-CMAPSS grouped (5 seeds) ----------
QG = [json.load(open(f'{D}/twin/q6ng_s{s}.json')) for s in range(5)]
u6 = sorted(QG[0]); gid6 = lambda u: gid('_'.join(u.split('_')[:2])); g6 = sorted(set(gid6(u) for u in u6))
def gvec6(x): return np.array([np.mean([x[i] for i, u in enumerate(u6) if gid6(u) == g]) for g in g6])
P('\nCase 2, N-CMAPSS (twins grouped, five seeds): S4 minus the better of S1/S2 (chosen on unit-weighted mean RMSE).\n')
P('| History | Reference | Δ per seed | Seeds S4 better | Unit-weighted means S4 / ref | Equal-group-weight means S4 / ref | Δ (group, seed-averaged) |'); P('|---|---|---|---|---|---|---|')
for h in ('h5', 'h3'):
    U = {a: np.mean([[rm(g[u][h][a]) for u in u6] for g in QG], 0) for a in ('A1', 'A2', 'B2')}
    ref = min(('A1', 'A2'), key=lambda a: U[a].mean())
    per = [float((gvec6([rm(g[u][h]['B2']) for u in u6]) - gvec6([rm(g[u][h][ref]) for u in u6])).mean()) for g in QG]
    ga, gb = gvec6(U['B2']), gvec6(U[ref])
    out[f'n2|{h}'] = dict(per=per, ref=ref, unit=[float(U['B2'].mean()), float(U[ref].mean())], group=[float(ga.mean()), float(gb.mean())], d=float((ga - gb).mean()), ngroups=len(g6))
    P(f"| last {h[1:]} | {NM6[ref]} | {', '.join(f'{x:+.2f}' for x in per)} | {sum(x < 0 for x in per)}/5 | {U['B2'].mean():.2f} / {U[ref].mean():.2f} | {ga.mean():.2f} / {gb.mean():.2f} | {(ga - gb).mean():+.2f} |")

# ---------- 3. exploratory non-inferiority, complete records ----------
SQ = json.load(open(B + '/analysis/summary_q3d.json'))
Rd = {fd: [json.load(open(f'{D}/q3d_{fd}_s{s}.json')) for s in range(5)] for fd in FDS}
Rx = {fd: [json.load(open(f'{D}/q6/q6x_{fd}_s{s}.json')) for s in range(5)] for fd in FDS}
P('\n## Table S17. Complete records: long-input variants against the dense model (exploratory non-inferiority)\n')
P('ΔMAE: seed-averaged engine absolute error, variant minus dense model, 95% engine-bootstrap interval. ΔRMSE: mean over seeds of the RMSE difference, 95% engine-bootstrap interval. "Within 1 cycle": upper bound of the interval below +1.0 cycle. Source runs: A8 and A5 rows use the five-seed case-1 exploratory run (Table 3); S8 and S4 rows use the five-seed case-2 run. The A5 rows therefore differ from the three-seed pre-specified H2 analysis in section 4.2 and Table S2 (for example FD001: −0.38 here, −0.14 there) and do not replace it.\n')
P('| Subset | Comparison | ΔMAE [95% CI] | ΔRMSE [95% CI] | Within 1 cycle (MAE / RMSE) |'); P('|---|---|---|---|---|')
for fd in FDS:
    for lab, E1, E2 in (('A8 vs A1', np.array([r['k1']['A8'] for r in Rd[fd]]), np.array([r['k1']['A1'] for r in Rd[fd]])),
                        ('S8 vs S1', np.array([r['full']['C8'] for r in Rx[fd]]), np.array([r['full']['A1'] for r in Q[fd]])),
                        ('A5 vs A1', np.array([r['k1']['A5'] for r in Rd[fd]]), np.array([r['k1']['A1'] for r in Rd[fd]])),
                        ('S4 vs S1', np.array([r['full']['B2'] for r in Q[fd]]), np.array([r['full']['A1'] for r in Q[fd]]))):
        d = np.abs(E1).mean(0) - np.abs(E2).mean(0); r_ = np.random.default_rng(0)
        cm_ = np.percentile([d[r_.integers(0, len(d), len(d))].mean() for _ in range(10000)], [2.5, 97.5])
        cr = boot_rmse_diff(E1, E2); dr = np.mean([rm(a) - rm(b) for a, b in zip(E1, E2)])
        out[f'ni|{fd}|{lab}'] = dict(dmae=float(d.mean()), ci_mae=[float(x) for x in cm_], drmse=float(dr), ci_rmse=cr)
        P(f"| {fd} | {lab} | {d.mean():+.2f} [{cm_[0]:+.2f}, {cm_[1]:+.2f}] | {dr:+.2f} [{cr[0]:+.2f}, {cr[1]:+.2f}] | {'yes' if cm_[1] < 1 else 'no'} / {'yes' if cr[1] < 1 else 'no'} |")

# ---------- 4. exploratory mixture analysis ----------
P('\n## Table S18. Mixed deployment: RMSE when a fraction w of predictions has complete records (exploratory)\n')
P('RMSE_mix(w) = sqrt(w·MSE_complete + (1−w)·MSE_degraded), per seed, averaged over seeds. Case 1: degraded = one record every five cycles (k = 5); A2 is the densely trained model with interpolation (identical to A1 with complete records). Case 2: degraded = last 5 cycles. Entries: arm with the lowest RMSE_mix at each w.\n')
W = [0.0, 0.25, 0.5, 0.75, 0.9, 1.0]
P('| Subset | Case | ' + ' | '.join(f'w = {w}' for w in W) + ' |'); P('|---|---|' + '---|' * len(W))
mix = {}
for fd in FDS:
    arms1 = {'A2': ('A2', 'A2'), 'A5': ('A5', 'A5'), 'A8': ('A8', 'A8')}
    def mse(run, sc, a): return float(np.mean(np.square(run[sc][a])))
    row = []
    for w in W:
        v = {a: np.mean([np.sqrt(w * mse(r, 'k1', a) + (1 - w) * mse(r, 'k5', a)) for r in Rd[fd]]) for a in arms1}
        best = min(v, key=v.get); row.append(f"{best} {v[best]:.1f}"); mix[f'{fd}|c1|{w}'] = {k: float(x) for k, x in v.items()}
    P(f'| {fd} | 1 | ' + ' | '.join(row) + ' |')
    row = []
    for w in W:
        v = {}
        for a, src in (('S1', ('Q', 'A1')), ('S4', ('Q', 'B2')), ('S8', ('X', 'C8'))):
            runs = Q[fd] if src[0] == 'Q' else Rx[fd]
            v[a] = np.mean([np.sqrt(w * np.mean(np.square(r['full'][src[1]])) + (1 - w) * np.mean(np.square(r['h5'][src[1]]))) for r in runs])
        best = min(v, key=v.get); row.append(f"{best} {v[best]:.1f}"); mix[f'{fd}|c2|{w}'] = {k: float(x) for k, x in v.items()}
    P(f'| {fd} | 2 | ' + ' | '.join(row) + ' |')
out['mix'] = mix
json.dump(out, open(B + '/analysis/summary_v10.json', 'w'), indent=1)
open(B + '/analysis/tables_v10.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('\n'.join(L))
