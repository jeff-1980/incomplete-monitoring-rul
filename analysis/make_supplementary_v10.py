"""Clean English supplementary material for manuscript v7 (all tables regenerated from saved errors; no internal paths)."""
import json, csv, numpy as np
from scipy.stats import wilcoxon
B = str(__import__('pathlib').Path(__file__).resolve().parents[1]) + ''; D = B + '/data'
S = json.load(open(B + '/analysis/summary.json')); SQ = json.load(open(B + '/analysis/summary_q3d.json'))
S6 = json.load(open(B + '/analysis/summary_q6.json')); RC = json.load(open(B + '/analysis/round3_checks.json'))
FDS = ['FD001', 'FD002', 'FD003', 'FD004']
rm = lambda e: float(np.sqrt(np.mean(np.square(e))))
phm = lambda e: np.where(e < 0, np.exp(-e / 13) - 1, np.exp(e / 10) - 1)
def boot(d, B_=10000):
    r = np.random.default_rng(0); n = len(d); b = [d[r.integers(0, n, n)].mean() for _ in range(B_)]; return np.quantile(b, [.025, .975])
def holm(ps):
    ps = np.asarray(ps); o = np.argsort(ps); m = len(ps); adj = np.empty(m); run = 0
    for i, j in enumerate(o): run = max(run, (m - i) * ps[j]); adj[j] = min(1, run)
    return adj
fmtp = lambda p: f'{p:.2g}'
SC = {'k1': 'k = 1', 'k2': 'k = 2', 'k3': 'k = 3', 'k5': 'k = 5', 'irr5': 'irr 1–5', 'irr10': 'irr 1–10'}
NM = {'B1_GRUD': 'GRU-D', 'B2s_imputer': 'IMP', 'B3_static': 'SNAP', 'B4_PCMambaSDE': 'PC-MambaSDE'}
N6 = {'A1': 'S1', 'A2': 'S2', 'B3': 'S3', 'B2': 'S4', 'B4': 'S5', 'A6L': 'S6', 'C8': 'S8'}
H6 = {'full': 'complete', 'h20': 'last 20', 'h10': 'last 10', 'h5': 'last 5', 'h3': 'last 3'}
L = []; P = L.append
P('# Supplementary material'); P('')
P('## Note S1. Protocols, deviations and naming'); P('')
P('Four protocol documents were written during the study: (1) case 1 on C-MAPSS (arms A1–A7, scenarios, hypotheses H1–H5, decision rule), created 03:24 UTC, before the first results at 05:02 UTC; (2) the case-1 N-CMAPSS confirmation, created 03:41 UTC, before any N-CMAPSS model was trained; (3) the N-CMAPSS evaluation of A8 and GRU-D, written two minutes after a first run had been started and then stopped once the results of one fold (one unit, three seeds) had been seen, after which all folds were rerun with the unchanged script; (4) case 2 on C-MAPSS and N-CMAPSS, written before its runs except for one run-through check whose results were not inspected, with an appendix adding S6 and S8 written after the C-MAPSS case-2 results were known, while the N-CMAPSS runs were in progress (per-unit numbers of two folds of one seed had been seen). The documents were archived publicly after the experiments https://doi.org/10.5281/zenodo.24269036; one line referring to the authors\' unrelated manuscripts was removed from document 1, and a host name was replaced in document 4.')
P(''); P('Deviations. (i) N-CMAPSS twin units: three DS01 units (u2, u5, u10) have DS02 counterparts with identical life and RUL labels and feature correlation of about 0.97; all N-CMAPSS models were retrained with the pairs merged and evaluated by leave-one-group-out validation over 16 groups, which the main text reports; the pre-specified leave-one-unit-out results are in Table S9. (ii) In the case-1 N-CMAPSS confirmation, unit RMSE was saved per seed and averaged over seeds, rather than averaging errors over seeds before computing RMSE. (iii) Pilot studies had used the official C-MAPSS test sets in both cases.')
P(''); P('Naming. The code uses internal names that differ from the paper: GRU-D = B1_GRUD; IMP = B2s_imputer; SNAP = B3_static; PC-MambaSDE = B4_PCMambaSDE; in case 2, S1 = A1, S2 = A2, S3 = B3, S4 = B2, S5 = B4, S6 = A6L, S8 = C8. The case-2 models S1 and S6 produce predictions identical to A1 and A6 of the five-seed case-1 run (same code, seeds and hardware; maximum absolute difference 0.0000 cycles).')
P(''); P('## Note S2. Baselines that were replaced'); P('')
P('GAIN imputer [28]: the regular k = 3 pattern made up 9.9% of its training masks, yet its imputation error on the last 30 cycles of FD001 test engines was 2.55 (k = 3) and 3.19 (k = 5) standardised units, against 0.46 for linear interpolation; with irregular gaps it was comparable to interpolation (0.44). Its adversarial training diverged under regular missingness, and it was replaced by the supervised masked imputer IMP (imputation error 0.37). Single-record regression with parametric rectification after [21]: without rectification, FD001 RMSE was 17.0 in every scenario; with our rectification over the last 10 records it was 18.7/22.1/24.6 at k = 1/3/5 (17.3/18.0/19.1 over the last 3), so rectification was dropped and SNAP is reported without it.')
P('')
# ---------------- Case 1 pre-specified run ----------------
ARMS = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7']
P('## Table S1. Case 1, pre-specified run: RMSE (cycles), mean ± s.d. over three seeds'); P('')
P('| Subset | Scenario | ' + ' | '.join(ARMS) + ' |'); P('|---|---|' + '---|' * len(ARMS))
for fd in FDS:
    for sc in SC:
        P(f'| {fd} | {SC[sc]} | ' + ' | '.join((f"{S['cmapss'][k]['rmse']:.2f} ± {S['cmapss'][k]['sd']:.2f}" if (k := f'{fd}|{sc}|{a}') in S['cmapss'] else '—') for a in ARMS) + ' |')
P(''); P('A1–A3 share models and coincide at k = 1. PHM 2008 scores (sum over engines, mean over seeds) are in the deposited data.'); P('')
def ptab(title, key, scs, note):
    P(f'## {title}'); P(''); P(note); P(''); P('| Subset | ' + ' | '.join(SC[s] for s in scs) + ' |'); P('|---|' + '---|' * len(scs))
    for fd in FDS:
        P(f'| {fd} | ' + ' | '.join((lambda r: f"{r['d']:+.2f} [{r['ci'][0]:+.2f}, {r['ci'][1]:+.2f}]; {r['nb']}/{r['n']}; p = {fmtp(r['p'])}")(S[key][f'{fd}|{s}']) for s in scs) + ' |')
    P('')
note = 'Mean paired difference in seed-averaged absolute error per test engine, A5 minus reference (cycles) [95% bootstrap interval]; engines for which A5 was better; two-sided Wilcoxon p (uncorrected except H2 as specified).'
ptab('Table S2. Case 1, pre-specified run: A5 versus A1 at k = 1 (H2), versus A4 (gap channel) and versus A7 (interval-specific)', 'H2: k1, A5 vs A1', ['k1'], note)
ptab('Table S2 (continued). A5 versus A4', 'H3: A5 vs A4 (gap channel)', list(SC), note)
ptab('Table S2 (continued). A5 versus A7', 'H5: A5 vs A7 (interval-matched)', ['k2', 'k3', 'k5'], note)
ptab('Table S3. Case 1, pre-specified run: A5 versus the long-input dense model A6', 'H4: A5 vs A6 (long window)', ['k1', 'k5', 'irr5'], note)
# sensitivity
R = {fd: [json.load(open(f'{D}/q3_{fd}_s{s}.json')) for s in range(3)] for fd in FDS}
E = lambda fd, sc, a: np.array([r[sc][a] for r in R[fd]])
P('## Table S4. Case 1 sensitivity analyses (added after internal review; see Note S3)'); P('')
P('(a) Reference re-selected by RMSE from {A1, A2, A3, A6}; Holm over eight comparisons.'); P('')
P('| Subset | Scenario | Reference | RMSE ref | RMSE A5 | Δ | Better | p | p (Holm) |'); P('|---|---|---|---|---|---|---|---|---|')
rows = []
for fd in FDS:
    for sc in ('k5', 'irr5'):
        best = min(['A1', 'A2', 'A3', 'A6'], key=lambda a: np.mean([rm(e) for e in E(fd, sc, a)]))
        x = np.abs(E(fd, sc, 'A5')).mean(0); y = np.abs(E(fd, sc, best)).mean(0)
        rows.append((fd, sc, best, np.mean([rm(e) for e in E(fd, sc, best)]), np.mean([rm(e) for e in E(fd, sc, 'A5')]), (x - y).mean(), (x < y).sum(), len(x), wilcoxon(x, y).pvalue))
for r, a in zip(rows, holm([r[8] for r in rows])):
    P(f'| {r[0]} | {SC[r[1]]} | {r[2]} | {r[3]:.2f} | {r[4]:.2f} | {r[5]:+.2f} | {r[6]}/{r[7]} | {fmtp(r[8])} | {fmtp(a)} |')
P(''); P('(b) Pre-specified H1 comparisons tested separately for each seed (Wilcoxon over engines).'); P('')
P('| Subset | Scenario | Reference | p, seed 0 | p, seed 1 | p, seed 2 |'); P('|---|---|---|---|---|---|')
for r in S['H1']:
    P(f"| {r['fd']} | {SC[r['sc']]} | {r['best']} | " + ' | '.join(fmtp(wilcoxon(np.abs(E(r['fd'], r['sc'], 'A5')[s]), np.abs(E(r['fd'], r['sc'], r['best'])[s])).pvalue) for s in range(3)) + ' |')
P(''); P('(c) Out-of-range irregular gaps 1–10: A5 versus the best of A1–A3.'); P('')
P('| Subset | Reference | RMSE ref | RMSE A5 | Δ | Better | p |'); P('|---|---|---|---|---|---|---|')
for fd in FDS:
    best = min(['A1', 'A2', 'A3'], key=lambda a: np.mean([rm(e) for e in E(fd, 'irr10', a)]))
    x = np.abs(E(fd, 'irr10', 'A5')).mean(0); y = np.abs(E(fd, 'irr10', best)).mean(0)
    P(f"| {fd} | {best} | {np.mean([rm(e) for e in E(fd, 'irr10', best)]):.2f} | {np.mean([rm(e) for e in E(fd, 'irr10', 'A5')]):.2f} | {(x-y).mean():+.2f} | {(x<y).sum()}/{len(x)} | {fmtp(wilcoxon(x,y).pvalue)} |")
P('')
# test-time checks (earlier 3-seed post-review run)
BC = json.load(open(B + '/analysis/summary_bc.json'))
P('## Table S5. Case 1: test-time checks of A5 (earlier post-review run, three seeds)'); P('')
P('Gap channel overwritten with 1 at k = 5, and every-cycle data fed to A5 as every third cycle (this second check equals the k = 3 scenario and is shown for completeness). RMSE in cycles; Δ in mean absolute error versus the unmodified A5 of the same run.'); P('')
P('| Subset | A5 at k = 5 | A5 with gap channel = 1 | Δ | p | A5 at k = 1 | A5 fed every third cycle | Δ | p |'); P('|---|---|---|---|---|---|---|---|---|')
for fd in FDS:
    g = BC[f'q3c|{fd}|k5|A5_gap1']; a3 = BC[f'q3c|{fd}|k1|A5_as3']
    P(f"| {fd} | {BC[f'q3c|{fd}|k5|A5']['rmse']:.2f} | {g['rmse']:.2f} | {g['d']:+.2f} | {fmtp(g['p'])} | {BC[f'q3c|{fd}|k1|A5']['rmse']:.2f} | {a3['rmse']:.2f} | {a3['d']:+.2f} | {fmtp(a3['p'])} |")
P('')
P('## Table S6. Case 1, pre-specified run: bias and late predictions at k = 5'); P('')
P('Mean signed error (positive = remaining life over-estimated), PHM 2008 score per seed and its median, and largest late error per seed (cycles).'); P('')
P('| Subset | Arm | Mean signed error | PHM per seed | PHM median | Largest late error per seed |'); P('|---|---|---|---|---|---|')
for fd in FDS:
    for a in ARMS:
        e = E(fd, 'k5', a); s_ = [phm(x).sum() for x in e]
        P(f"| {fd} | {a} | {e.mean():+.2f} | {', '.join(f'{v:.0f}' for v in s_)} | {np.median(s_):.0f} | {', '.join(f'{x.max():.0f}' for x in e)} |")
P('')
# ---------------- same-run batch ----------------
QA = ['A1', 'A2', 'A3', 'A6', 'A5', 'A8', 'B1_GRUD', 'B2s_imputer', 'B3_static', 'B4_PCMambaSDE']
P('## Table S7. Case 1, five-seed run with all models trained together: RMSE (cycles), mean ± s.d. over five seeds'); P('')
P('PC-MambaSDE was trained in a separate run with the same seeds, windows and test engines, with the same budget as the other models (batch size 256, 30 epochs, about one twentieth of the gradient steps of the default in the original code) and without tuning or checkpoint selection; the released code was used with one class-name clash corrected so that the Mamba encoder is used, and the elapsed time since the window start (cycles/150) was given as its time input.'); P('')
P('| Subset | Scenario | ' + ' | '.join(NM.get(a, a) for a in QA) + ' |'); P('|---|---|' + '---|' * len(QA))
for fd in FDS:
    for sc in SC:
        P(f'| {fd} | {SC[sc]} | ' + ' | '.join(f"{SQ[f'{fd}|{sc}|{a}']['rmse']:.2f} ± {SQ[f'{fd}|{sc}|{a}']['sd']:.2f}" for a in QA) + ' |')
P('')
P('## Table S8. Case 1, five-seed run: paired comparisons'); P('')
P('Δ mean absolute error, first model minus second (cycles) [95% bootstrap interval]; engines for which the first model was better; two-sided Wilcoxon p (uncorrected).'); P('')
for a, b in [('A8', 'A6'), ('A8', 'A1'), ('A8', 'A5'), ('B1_GRUD', 'A5'), ('B2s_imputer', 'A5'), ('B3_static', 'A5'), ('A6', 'A5'), ('B4_PCMambaSDE', 'A5'), ('B4_PCMambaSDE', 'A8'), ('B4_PCMambaSDE', 'B1_GRUD'), ('B4_PCMambaSDE', 'A2')]:
    P(f'**{NM.get(a, a)} versus {NM.get(b, b)}**'); P(''); P('| Subset | ' + ' | '.join(SC[s] for s in SC) + ' |'); P('|---|' + '---|' * len(SC))
    for fd in FDS:
        P(f'| {fd} | ' + ' | '.join((lambda r: f"{r['d']:+.2f} [{r['ci'][0]:+.2f}, {r['ci'][1]:+.2f}]; {r['nb']}/{r['n']}; {fmtp(r['p'])}")(SQ[f'cmp|{a}|{b}|{fd}|{s}']) for s in SC) + ' |')
    P('')
P('**Bias, PHM median and largest late error (five-seed run; k = 1 / k = 5 / irr 1–5)**'); P('')
P('| Subset | Arm | Mean signed error | PHM median | Largest late error |'); P('|---|---|---|---|---|')
for fd in FDS:
    for a in ['A1', 'A2', 'A6', 'A5', 'A8', 'B1_GRUD', 'B4_PCMambaSDE']:
        g = [SQ[f'{fd}|{sc}|{a}'] for sc in ('k1', 'k5', 'irr5')]
        P(f"| {fd} | {NM.get(a, a)} | {' / '.join(f'{x['bias']:+.1f}' for x in g)} | {' / '.join(f'{x['phm_med']:.0f}' for x in g)} | {' / '.join(f'{x['maxlate']:.0f}' for x in g)} |")
P('')
# ---------------- N-CMAPSS both schemes ----------------
rows = list(csv.DictReader(open(D + '/twin/unit_scores.csv', encoding='utf-8')))
def vec(an, scheme, sc, arm, level):
    Rr = [r for r in rows if r['analysis'].startswith(an) and r['protocol'].startswith(scheme) and r['scenario'] == sc and r['arm'] == arm]
    if level == 'unit': return {r['unit']: float(r['rmse_seed_avg']) for r in Rr}
    g = {}
    for r in Rr: g.setdefault(r['group'], []).append(float(r['rmse_seed_avg']))
    return {k: float(np.mean(v)) for k, v in g.items()}
P('## Table S9. N-CMAPSS: all confirmatory tests under the pre-specified (leave-one-unit-out, 19 units) and twin-grouped (leave-one-group-out, 16 groups) schemes'); P('')
P('Mean RMSE over units (seed-averaged); Δ = first minus second arm in unit (19) or group (16) RMSE [95% bootstrap interval]; better = units or groups where the first arm was better; Holm within each pair of comparisons where specified. The main text uses the grouped scheme at the group level.'); P('')
P('| Evaluation | Scenario | Comparison | Scheme | Mean RMSE (first / second) | Δ [95% CI] | Better | p | p (Holm) |'); P('|---|---|---|---|---|---|---|---|---|')
TESTS = [('Q3 首次', 'Case 1, A5', [('k5', 'A5', 'A2'), ('irr5', 'A5', 'A2')], [('k1', 'A5', 'A1')]),
         ('Q3 A8', 'Case 1, A8', [('k5', 'A8', 'A2'), ('irr5', 'A8', 'A2')], [('k5', 'A8', 'A5'), ('irr5', 'A8', 'A5'), ('k1', 'A8', 'A1')]),
         ('Q3 A8', 'Case 1, GRU-D', [('k5', 'B1_GRUD', 'A2'), ('irr5', 'B1_GRUD', 'A2')], [('k5', 'B1_GRUD', 'A5'), ('irr5', 'B1_GRUD', 'A5')]),
         ('Q6', 'Case 2, S4', [('h5', 'B2', 'A1'), ('h3', 'B2', 'A1')], [('full', 'B2', 'A1')]),
         ('Q6', 'Case 2, S8', [('h5', 'C8', 'A1'), ('h3', 'C8', 'A1')], [('full', 'C8', 'A1')])]
for an, label, holmset, single in TESTS:
    for scheme, sname, level in (('原', 'unit-out (19)', 'unit'), ('孪生', 'grouped (16)', 'group')):
        res = []
        for sc, a, b in holmset + single:
            x = vec(an, scheme, sc, a, level); y = vec(an, scheme, sc, b, level); k = sorted(x)
            xv = np.array([x[i] for i in k]); yv = np.array([y[i] for i in k]); d = xv - yv; ci = boot(d)
            ma = np.mean(list(vec(an, scheme, sc, a, 'unit').values())); mb = np.mean(list(vec(an, scheme, sc, b, 'unit').values()))
            res.append([sc, a, b, ma, mb, d.mean(), ci, (d < 0).sum(), len(d), wilcoxon(xv, yv).pvalue])
        hp = holm([r[9] for r in res[:2]])
        for i, r in enumerate(res):
            nm = lambda z: (N6.get(z, z) if an == 'Q6' else NM.get(z, z))
            P(f"| {label} | {(H6.get(r[0]) or SC.get(r[0], r[0]))} | {nm(r[1])} vs {nm(r[2])} | {sname} | {r[3]:.2f} / {r[4]:.2f} | {r[5]:+.2f} [{r[6][0]:+.2f}, {r[6][1]:+.2f}] | {r[7]}/{r[8]} | {fmtp(r[9])} | {fmtp(hp[i]) if i < 2 else '—'} |")
P('')
# ---------------- case 2 ----------------
C6 = ['A1', 'A2', 'B3', 'B2', 'B4', 'A6L', 'C8']
P('## Table S10. Case 2, C-MAPSS: RMSE (cycles), mean ± s.d. over five seeds'); P('')
P('| Subset | History | ' + ' | '.join(N6[a] for a in C6) + ' |'); P('|---|---|' + '---|' * len(C6))
for fd in FDS:
    for h in ('full', 'h20', 'h10', 'h5'):
        P(f'| {fd} | {H6[h]} | ' + ' | '.join((f"{S6[k]['rmse']:.2f} ± {S6[k]['sd']:.2f}" if (k := f'c|{fd}|{h}|{a}') in S6 else '—') for a in C6) + ' |')
P('')
P('## Table S11. Case 2, C-MAPSS: paired comparisons'); P('')
P('Δ mean absolute error, first minus second (cycles) [95% bootstrap interval]; engines for which the first was better; two-sided Wilcoxon p; Holm over the eight H1 comparisons.'); P('')
P('| Subset | History | Comparison | Δ [95% CI] | Better | p | p (Holm) |'); P('|---|---|---|---|---|---|---|')
for fd in FDS:
    for h in ('h10', 'h5'):
        r = S6[f'H1c|{fd}|{h}']; P(f"| {fd} | {H6[h]} | S4 vs {N6[r['best']]} (H1) | {r['d']:+.2f} [{r['ci'][0]:+.2f}, {r['ci'][1]:+.2f}] | {r['nb']}/{r['n']} | {fmtp(r['p'])} | {fmtp(r['p_holm'])} |")
    r = S6[f'H2c|{fd}']; P(f"| {fd} | complete | S4 vs S1 (H2) | {r['d']:+.2f} [{r['ci'][0]:+.2f}, {r['ci'][1]:+.2f}] | {r['nb']}/{r['n']} | {fmtp(r['p'])} | {'met' if r['pass'] else 'not met'} |")
    for a, b, hs in (('C8', 'A1', ['full']), ('C8', 'B2', ['full', 'h10', 'h5']), ('C8', 'A6L', ['full', 'h10', 'h5']), ('B2', 'B3', ['full', 'h10', 'h5']), ('B2', 'B4', ['h20', 'h10', 'h5'])):
        for h in hs:
            r = S6[f'xc|{a}|{b}|{fd}|{h}']; P(f"| {fd} | {H6[h]} | {N6[a]} vs {N6[b]} | {r['d']:+.2f} [{r['ci'][0]:+.2f}, {r['ci'][1]:+.2f}] | {r['nb']}/{r['n']} | {fmtp(r['p'])} | — |")
P('')
P('## Table S12. Case 2, C-MAPSS: bias and late predictions'); P('')
P('Mean signed error (positive = over-estimated remaining life), median PHM 2008 score over seeds, largest late error over all seeds (cycles).'); P('')
P('| Subset | Arm | Complete | Last 10 | Last 5 |'); P('|---|---|---|---|---|')
for fd in FDS:
    for a in ('A1', 'A2', 'B2', 'C8', 'A6L'):
        P(f'| {fd} | {N6[a]} | ' + ' | '.join((lambda r: f"bias {r['bias']:+.1f}; PHM {r['phm_med']:.0f}; late {r['maxlate']:.0f}")(RC[f'late2|{fd}|{h}|{a}']) for h in ('full', 'h10', 'h5')) + ' |')
P('')
P('## Table S13. N-CMAPSS mean RMSE of all arms under both validation schemes'); P('')
P('| Evaluation | Scenario | Arm | Unit-out (19) | Grouped (16) |'); P('|---|---|---|---|---|')
for an, label in (('Q3 首次', 'Case 1, pre-specified run'), ('Q3 A8', 'Case 1, A8/GRU-D run'), ('Q6', 'Case 2')):
    keys = sorted({(r['scenario'], r['arm']) for r in rows if r['analysis'].startswith(an)})
    for sc, arm in keys:
        u = np.mean(list(vec(an, '原', sc, arm, 'unit').values())); g = np.mean(list(vec(an, '孪生', sc, arm, 'unit').values()))
        nm = N6.get(arm, arm) if an == 'Q6' else NM.get(arm, arm)
        P(f'| {label} | {H6.get(sc) or SC.get(sc, sc)} | {nm} | {u:.2f} | {g:.2f} |')
P('')
P('## Table S14. End-of-life accuracy: RMSE (and mean signed error) on C-MAPSS test engines with true RUL ≤ 50 cycles'); P('')
P('Case 1: five-seed run; case 2: five seeds. Engines with RUL ≤ 50: FD001 33, FD002 88, FD003 29, FD004 80.'); P('')
P('| Subset | Case | Scenario | ' + ' | '.join(['A1/S1', 'A2/S2', 'A6/S6', 'A5/S4', 'A8/S8', 'GRU-D']) + ' |'); P('|---|---|---|' + '---|' * 6)
for fd in FDS:
    for sc in ('k1', 'k5', 'irr5'):
        P(f'| {fd} | 1 | {SC[sc]} | ' + ' | '.join((lambda r: f"{r['rmse']:.1f} ({r['bias']:+.1f})")(RC[f'eol1|{fd}|{sc}|{a}']) for a in ('A1', 'A2', 'A6', 'A5', 'A8', 'B1_GRUD')) + ' |')
    for h in ('full', 'h10', 'h5'):
        P(f'| {fd} | 2 | {H6[h]} | ' + ' | '.join((lambda r: f"{r['rmse']:.1f} ({r['bias']:+.1f})")(RC[f'eol2|{fd}|{h}|{a}']) for a in ('A1', 'A2', 'A6L', 'B2', 'C8')) + ' | — |')
P('')
P('## Table S15. Case 1: availability of measured records in the C-MAPSS test windows'); P('')
P('Share of test engines whose 30-record window cannot be filled with measured records (padded by repeating the first record; padded rows have gap 0). At k = 5 the median number of measured records is 27–30 in the 30-record window of A5 and in the 150-cycle window of A6 and A8, but 6 in the 30-cycle interpolated window of A2 and A3.'); P('')
P('| Subset | Test engines | Padded at k = 1 | Padded at k = 5 | Padded at irr 1–5 |'); P('|---|---|---|---|---|')
for fd in FDS:
    r = RC[f'pad|{fd}']; P(f"| {fd} | {r['n']} | {r['k1']*100:.0f}% | {r['k5']*100:.0f}% | {r['irr5']*100:.0f}% |")
P('')
X = open(B + '/analysis/supp_v10_extra.md', encoding='utf-8').read().split('\n')
import re as _re
T = open(B + '/analysis/tables_v10.md', encoding='utf-8').read()
T = T.replace('| k5 |', '| k = 5 |').replace('| irr5 |', '| irr 1–5 |')
T = _re.sub(r'(?<![\w])-(?=\d)', '−', T).split('\n')
i = [j for j, l in enumerate(L) if l.startswith('## Table S1.')][0]
L = L[:i] + X + L[i:] + [''] + T
open(B + '/manuscript/supplementary_v10.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('ok', len(L))
