"""Analysis of upgrade step 1, as fixed in PROTOCOL_upgrade1.md. Written before the results were inspected."""
import json, os, numpy as np
from scipy.stats import wilcoxon
H = os.path.dirname(os.path.abspath(__file__)); FDS = ['FD001', 'FD002', 'FD003', 'FD004']
rm = lambda e: float(np.sqrt(np.mean(np.square(e))))
def boot(d, n=10000):
    r = np.random.default_rng(0); d = np.asarray(d); return [float(v) for v in np.percentile([d[r.integers(0, len(d), len(d))].mean() for _ in range(n)], [2.5, 97.5])]
def holm(ps):
    ps = np.asarray(ps); o = np.argsort(ps); adj = np.empty(len(ps)); run = 0
    for r, i in enumerate(o): run = max(run, (len(ps) - r) * ps[i]); adj[i] = min(1, run)
    return adj
def wil(x, y):
    d = np.asarray(x) - np.asarray(y); return 1.0 if np.allclose(d, 0) else float(wilcoxon(x, y).pvalue)
def pair(x, y):
    d = np.asarray(x) - np.asarray(y); return dict(d=float(d.mean()), ci=boot(d), nb=int((d < 0).sum()), n=len(d), p=wil(x, y))
def fmt(r, h=None): return f"{r['d']:+.2f} [{r['ci'][0]:+.2f}, {r['ci'][1]:+.2f}]; {r['nb']}/{r['n']}; p = {r['p']:.2g}" + (f"; Holm {h:.2g}" if h is not None else '')
S = {}; L = []; P = lambda *a: L.append(' '.join(map(str, a)))

# ================= A. DS03-DS08 external cohort =================
E = [json.load(open(f'{H}/results/ext_s{s}.json')) for s in range(5)]; units = sorted(E[0])
PROFILE = {}
for u in units:
    ds, un = u.split('_')[0], u.split('_')[1]; PROFILE[u] = f'DS05-07_{un}' if ds in ('DS05', 'DS06', 'DS07') else u
groups = sorted(set(PROFILE.values()))
def uscore(sc, a): return np.mean([[rm(r[u][sc][a]) for u in units] for r in E], 0)           # unit RMSE, seed-averaged
def g(x): return np.array([np.mean([x[i] for i, u in enumerate(units) if PROFILE[u] == k]) for k in groups])
S['ext_units'] = len(units); S['ext_groups'] = len(groups)
P(f'## Table S21. External cohort N-CMAPSS DS03–DS08: fixed split, fixed models ({len(units)} test units, {len(groups)} groups, five seeds)\n')
P('Mean unit RMSE in cycles (unit-weighted).\n')
C1 = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A8B']; C2 = ['S1', 'S2', 'S3', 'S4', 'S6', 'S8']
P('| Case | Scenario | ' + ' | '.join(C1) + ' |'); P('|---|---|' + '---|' * len(C1))
for sc, lab in (('k1', 'k = 1'), ('k5', 'k = 5'), ('irr5', 'irr 1–5'), ('blk5', 'block 5'), ('blk10', 'block 10')):
    for a in C1: S[f'ext|{sc}|{a}'] = float(uscore(sc, a).mean())
    P(f'| 1 | {lab} | ' + ' | '.join(f"{S[f'ext|{sc}|{a}']:.2f}" for a in C1) + ' |')
P(''); P('| Case | History | ' + ' | '.join(C2) + ' |'); P('|---|---|' + '---|' * len(C2))
for sc, lab in (('full', 'complete'), ('h5', 'last 5'), ('h3', 'last 3')):
    for a in C2: S[f'ext|{sc}|{a}'] = float(uscore(sc, a).mean())
    P(f'| 2 | {lab} | ' + ' | '.join(f"{S[f'ext|{sc}|{a}']:.2f}" for a in C2) + ' |')
def family(arm, cands, scs, tag):
    rows = []
    for sc in scs:
        ref = min(cands, key=lambda a: uscore(sc, a).mean()); r = pair(g(uscore(sc, arm)), g(uscore(sc, ref))); r['ref'] = ref; r['sc'] = sc
        r['per_seed'] = [float((g(np.array([rm(run[u][sc][arm]) for u in units])) - g(np.array([rm(run[u][sc][ref]) for u in units]))).mean()) for run in E]
        rows.append(r)
    adj = holm([r['p'] for r in rows])
    for r, a in zip(rows, adj): r['holm'] = float(a)
    S[tag] = rows; S[tag + '_confirmed'] = bool(all(r['holm'] < 0.05 and r['d'] < 0 for r in rows)); return rows
P('\n## Table S22. External cohort: tests\n')
P('Δ: mean paired difference of group RMSE (arm minus reference) [95% bootstrap CI]; groups better; Wilcoxon p; Holm within family; Δ per seed.\n')
P('| Hypothesis | Scenario | Arm | Reference | Δ | Δ per seed |'); P('|---|---|---|---|---|---|')
for tag, arm, cands, scs, name in (('E1', 'A5', ['A1', 'A2', 'A3'], ['k5', 'irr5'], 'E1 (confirmatory)'), ('E2', 'S4', ['S1', 'S2'], ['h5', 'h3'], 'E2 (confirmatory)'),
                                   ('E1_A8', 'A8', ['A1', 'A2', 'A3'], ['k5', 'irr5'], 'secondary'), ('E2_S8', 'S8', ['S1', 'S2'], ['h5', 'h3'], 'secondary'),
                                   ('B_A5', 'A5', ['A1', 'A2', 'A3'], ['blk5', 'blk10'], 'block outage'), ('B_A8', 'A8', ['A1', 'A2', 'A3'], ['blk5', 'blk10'], 'block outage')):
    for r in family(arm, cands, scs, tag):
        P(f"| {name} | {r['sc']} | {arm} | {r['ref']} | {fmt(r, r['holm'])} | {', '.join(f'{v:+.2f}' for v in r['per_seed'])} |")
for tag, a, b, sc in (('E3_A5', 'A5', 'A1', 'k1'), ('E3_S4', 'S4', 'S1', 'full'), ('E3_A8', 'A8', 'A1', 'k1'), ('E3_S8', 'S8', 'S1', 'full'),
                      ('A8B_blk5', 'A8B', 'A8', 'blk5'), ('A8B_blk10', 'A8B', 'A8', 'blk10'), ('A8B_k5', 'A8B', 'A8', 'k5'), ('A8B_k1', 'A8B', 'A8', 'k1')):
    r = pair(g(uscore(sc, a)), g(uscore(sc, b))); S[tag] = r
    P(f"| {'E3 cost, complete records' if tag.startswith('E3') else 'reference trained with outages'} | {sc} | {a} | {b} | {fmt(r)}{'; non-inferior (1 cycle): ' + ('yes' if r['ci'][1] < 1 else 'no') if tag.startswith('E3') else ''} | |")
P(f"\nE1 confirmed: {S['E1_confirmed']}. E2 confirmed: {S['E2_confirmed']}.")

# ================= B. C-MAPSS unseen mechanisms =================
R = {fd: [json.load(open(f'{H}/results/cmx_{fd}_s{s}.json')) for s in range(5)] for fd in FDS}
CA = ['A1', 'A2', 'A3', 'A5', 'A6', 'A8', 'A8B']
P('\n## Table S23. C-MAPSS, missingness mechanisms not seen in training: RMSE (cycles), mean ± s.d. over five seeds\n')
P('Block: the last 5 cycles recorded, the 10 or 20 cycles before them missing. Regime: cycles in the three highest operating regimes missing with probability 0.9, others 0.1 (median number of records in the last column).\n')
P('| Subset | Scenario | ' + ' | '.join(CA) + ' | Records |'); P('|---|---|' + '---|' * (len(CA) + 1))
def mae(fd, sc, a): return np.mean([np.abs(r[sc][a]) for r in R[fd]], 0)
def rmses(fd, sc, a): return [rm(r[sc][a]) for r in R[fd]]
for fd in FDS:
    for sc in ['k1', 'blk10', 'blk20'] + (['reg'] if 'reg' in R[fd][0] else []):
        for a in CA: S[f'c|{fd}|{sc}|{a}'] = dict(rmse=float(np.mean(rmses(fd, sc, a))), sd=float(np.std(rmses(fd, sc, a), ddof=1)))
        P(f"| {fd} | {sc} | " + ' | '.join(f"{S[f'c|{fd}|{sc}|{a}']['rmse']:.2f} ± {S[f'c|{fd}|{sc}|{a}']['sd']:.2f}" for a in CA) + f" | {int(np.median(R[fd][0][sc]['n_rec']))} |")
P('\n## Table S24. C-MAPSS, unseen mechanisms: degraded-training arms against the best test-time remedy\n')
P('Δ: seed-averaged engine absolute error, arm minus best of A1/A2/A3 (by RMSE) [95% CI]; engines better; Wilcoxon p; Holm within the arm\'s family (8 block comparisons; 2 regime comparisons).\n')
P('| Arm | Subset | Scenario | Reference | Δ |'); P('|---|---|---|---|---|')
for arm in ('A5', 'A8'):
    for fam, keys in (('blk', [(fd, sc) for fd in FDS for sc in ('blk10', 'blk20')]), ('reg', [(fd, 'reg') for fd in ('FD002', 'FD004')])):
        rows = []
        for fd, sc in keys:
            ref = min(['A1', 'A2', 'A3'], key=lambda a: S[f'c|{fd}|{sc}|{a}']['rmse']); r = pair(mae(fd, sc, arm), mae(fd, sc, ref)); r.update(ref=ref, fd=fd, sc=sc); rows.append(r)
        adj = holm([r['p'] for r in rows])
        for r, a in zip(rows, adj):
            r['holm'] = float(a); P(f"| {arm} | {r['fd']} | {r['sc']} | {r['ref']} | {fmt(r, r['holm'])} |")
        S[f'B_c_{arm}_{fam}'] = rows; S[f'B_c_{arm}_{fam}_nsig'] = int(sum(r['holm'] < 0.05 and r['d'] < 0 for r in rows)); S[f'B_c_{arm}_{fam}_nworse'] = int(sum(r['holm'] < 0.05 and r['d'] > 0 for r in rows))
for arm in ('A5', 'A8'):
    ok = S[f'B_c_{arm}_blk_nsig'] >= 6 and all(r['holm'] < 0.05 and r['d'] < 0 for r in S[f'B_{arm}'])
    S[f'B_reading_{arm}'] = ok
    P(f"\n{arm}: C-MAPSS block {S[f'B_c_{arm}_blk_nsig']}/8 significantly better ({S[f'B_c_{arm}_blk_nworse']} worse); regime {S[f'B_c_{arm}_reg_nsig']}/2; DS03–DS08 block {sum(r['holm'] < 0.05 and r['d'] < 0 for r in S[f'B_{arm}'])}/2. Pre-specified reading 'remains better under an unseen mechanism': {ok}.")
rows = [dict(pair(mae(fd, sc, 'A8B'), mae(fd, sc, 'A8')), fd=fd, sc=sc) for fd in FDS for sc in ('blk10', 'blk20')]; S['A8B_c'] = rows
P('\nA8B (trained with outages) minus A8, C-MAPSS block scenarios: ' + '; '.join(f"{r['fd']} {r['sc']} {r['d']:+.2f} (p = {r['p']:.2g})" for r in rows) + '.')

# ================= C. Mechanism =================
P('\n## Table S25. Padding-shortcut experiment: mean signed error (cycles) near end of life with short histories\n')
P('C-MAPSS: test engines with true RUL ≤ 50, five seeds averaged. DS03–DS08: predictions with true RUL ≤ 20, unit means averaged within groups. S3E: only windows with RUL above the threshold truncated in training; S3L: only windows at or below it.\n')
P('| Data | History | n | S1 | S3E | S3 | S3L | S3E − S3L [95% CI]; p; Holm |'); P('|---|---|---|---|---|---|---|---|')
mrows = []
for fd in FDS:
    y = np.array(R[fd][0]['y']); m = y <= 50
    for h in ('h10', 'h5'):
        v = {a: np.mean([np.array(r[h][a])[m] for r in R[fd]], 0) for a in ('S1', 'S3E', 'S3', 'S3L')}
        mrows.append(dict(data=fd, h=h, n=int(m.sum()), means={a: float(x.mean()) for a, x in v.items()}, r=pair(v['S3E'], v['S3L']), order=bool(v['S3E'].mean() > v['S3'].mean() > v['S3L'].mean())))
adj = holm([r['r']['p'] for r in mrows])
for r, a in zip(mrows, adj): r['holm'] = float(a)
erows = []
def ubias(h, a):
    return np.mean([[np.mean(np.array(run[u][h][a])[np.array(run[u][h]['y']) <= 20]) for u in units] for run in E], 0)
for h in ('h5', 'h3'):
    v = {a: g(ubias(h, a)) for a in ('S1', 'S3E', 'S3', 'S3L')}
    erows.append(dict(data='DS03–DS08', h=h, n=len(groups), means={a: float(x.mean()) for a, x in v.items()}, r=pair(v['S3E'], v['S3L']), order=bool(v['S3E'].mean() > v['S3'].mean() > v['S3L'].mean())))
adj = holm([r['r']['p'] for r in erows])
for r, a in zip(erows, adj): r['holm'] = float(a)
for r in mrows + erows:
    mm = r['means']; P(f"| {r['data']} | last {r['h'][1:]} | {r['n']} | {mm['S1']:+.1f} | {mm['S3E']:+.1f} | {mm['S3']:+.1f} | {mm['S3L']:+.1f} | {r['r']['d']:+.2f} [{r['r']['ci'][0]:+.2f}, {r['r']['ci'][1]:+.2f}]; p = {r['r']['p']:.2g}; Holm {r['holm']:.2g} |")
nc = sum(r['holm'] < 0.05 and r['r']['d'] > 0 for r in mrows); ne = sum(r['holm'] < 0.05 and r['r']['d'] > 0 for r in erows)
S['mech'] = dict(c=mrows, e=erows, n_c=int(nc), n_e=int(ne), supported=bool(nc >= 6 and ne == 2), order_all=bool(all(r['order'] for r in mrows + erows)))
P(f"\nS3E − S3L positive and Holm-significant: C-MAPSS {nc}/8, DS03–DS08 {ne}/2; ordering S3E > S3 > S3L in {sum(r['order'] for r in mrows + erows)}/10. Pre-specified reading 'shortcut hypothesis supported': {S['mech']['supported']}.")
P('\nRMSE of the mechanism arms (C-MAPSS, last 5 cycles / complete): ' + '; '.join(f"{fd} " + ', '.join(f"{a} {np.mean([rm(r['h5'][a]) for r in R[fd]]):.1f}/{np.mean([rm(r['full'][a]) for r in R[fd]]):.1f}" for a in ('S1', 'S3E', 'S3', 'S3L')) for fd in FDS) + '.')
json.dump(S, open(f'{H}/summary_upgrade1.json', 'w'), indent=1, default=float); open(f'{H}/tables_upgrade1.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('\n'.join(L))
