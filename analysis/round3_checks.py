"""Round-3 checks without retraining:
(1) padding at k=5 / irregular for C-MAPSS test engines (records available vs 30-record window)
(2) end-of-life accuracy (true RUL <= 50) and bias for both cases
(3) case-2 late-prediction profile (bias, PHM median, largest late error)
(4) identity check: case-2 dense/A6L models vs post-review A1/A6
(5) grouped N-CMAPSS per-arm means from the twin re-analysis CSV (for tables/figures)"""
import json, csv, numpy as np
from scipy.stats import wilcoxon
B = str(__import__('pathlib').Path(__file__).resolve().parents[1]) + ''; D = B + '/data'; RAW = __import__('os').environ.get('CMAPSS_DIR', 'data/cmapss')
FDS = ['FD001', 'FD002', 'FD003', 'FD004']; CAP = 125
rm = lambda e: float(np.sqrt(np.mean(np.square(e)))) if len(e) else float('nan')
phm = lambda e: np.where(e < 0, np.exp(-e / 13) - 1, np.exp(e / 10) - 1)
L = []; P = lambda *a: L.append(' '.join(map(str, a))); OUT = {}
def test_len(fd):
    a = np.loadtxt(f'{RAW}/test_{fd}.txt'); return np.array([int((a[:, 0] == u).sum()) for u in np.unique(a[:, 0])])
def yt(fd): return np.minimum(np.loadtxt(f'{RAW}/RUL_{fd}.txt'), CAP)
P('## (1) Padding: share of test engines whose 30-record window is not filled by measured records')
for fd in FDS:
    T = test_len(fd); rec5 = (T - 1) // 5 + 1; rec1 = np.minimum(T, 30)
    rng_irr = [1 + int((np.cumsum(np.random.default_rng(1000 + u).integers(1, 6, 400)) <= T[u - 1] - 1).sum()) for u in range(1, len(T) + 1)]
    P(f'{fd}: n={len(T)}, length min/median {T.min()}/{int(np.median(T))}; padded at k=1: {np.mean(T < 30)*100:.0f}%; at k=5: {np.mean(rec5 < 30)*100:.0f}% (median records {int(np.median(np.minimum(rec5,30)))}); irr1-5: {np.mean(np.array(rng_irr) < 30)*100:.0f}%; at k=5 the 30-cycle interpolated window of A2 contains median {int(np.median(np.minimum((np.minimum(T,30)-1)//5+1, 30)))} measured records; A6/A8 150-cycle window median {int(np.median(np.minimum((np.minimum(T,150)-1)//5+1,30)))} records')
    OUT[f'pad|{fd}'] = dict(n=int(len(T)), k5=float(np.mean(rec5 < 30)), k1=float(np.mean(T < 30)), irr5=float(np.mean(np.array(rng_irr) < 30)))
P('\n## (2) End-of-life accuracy: RMSE and bias on test engines with true RUL <= 50 (case 1 same-run batch, 5 seeds; case 2, 5 seeds)')
for fd in FDS:
    y = yt(fd); m = y <= 50; P(f'{fd}: {m.sum()} engines with RUL <= 50')
    R = [json.load(open(f'{D}/q3d_{fd}_s{s}.json')) for s in range(5)]
    for sc in ('k1', 'k5', 'irr5'):
        row = []
        for a in ('A1', 'A2', 'A6', 'A5', 'A8', 'B1_GRUD'):
            e = np.array([r[sc][a] for r in R]); per = [rm(x[m]) for x in e]; b = float(e[:, m].mean())
            OUT[f'eol1|{fd}|{sc}|{a}'] = dict(rmse=float(np.mean(per)), bias=b); row.append(f'{a} {np.mean(per):.1f} ({b:+.1f})')
        P(f'  case1 {sc}: ' + '; '.join(row))
    Q = [json.load(open(f'{D}/q6/q6_{fd}_s{s}.json')) for s in range(5)]; X = [json.load(open(f'{D}/q6/q6x_{fd}_s{s}.json')) for s in range(5)]
    for h in ('full', 'h10', 'h5'):
        row = []
        for a in ('A1', 'A2', 'B2', 'C8', 'A6L'):
            src = X if a in ('C8', 'A6L') else Q
            e = np.array([r[h][a] for r in src]); per = [rm(x[m]) for x in e]; b = float(e[:, m].mean())
            OUT[f'eol2|{fd}|{h}|{a}'] = dict(rmse=float(np.mean(per)), bias=b); row.append(f'{a} {np.mean(per):.1f} ({b:+.1f})')
        P(f'  case2 {h}: ' + '; '.join(row))
P('\n## (3) Case 2: bias, PHM median over seeds, largest late error (all test engines)')
for fd in FDS:
    Q = [json.load(open(f'{D}/q6/q6_{fd}_s{s}.json')) for s in range(5)]; X = [json.load(open(f'{D}/q6/q6x_{fd}_s{s}.json')) for s in range(5)]
    for a in ('A1', 'A2', 'B2', 'C8', 'A6L'):
        src = X if a in ('C8', 'A6L') else Q; cells = []
        for h in ('full', 'h10', 'h5'):
            e = np.array([r[h][a] for r in src]); s_ = [phm(x).sum() for x in e]
            OUT[f'late2|{fd}|{h}|{a}'] = dict(bias=float(e.mean()), phm_med=float(np.median(s_)), maxlate=float(e.max()))
            cells.append(f'{h}: bias {e.mean():+.1f}, PHM med {np.median(s_):.0f}, max late {e.max():.0f}')
        P(f'{fd} {a}: ' + ' | '.join(cells))
P('\n## (4) Identity: case-2 dense (A1, full history) vs post-review A1 (k=1); A6L (full) vs post-review A6 (k=1)')
for fd in FDS:
    q = np.array(json.load(open(f'{D}/q6/q6_{fd}_s0.json'))['full']['A1']); d = np.array(json.load(open(f'{D}/q3d_{fd}_s0.json'))['k1']['A1'])
    x = np.array(json.load(open(f'{D}/q6/q6x_{fd}_s0.json'))['full']['A6L']); a6 = np.array(json.load(open(f'{D}/q3d_{fd}_s0.json'))['k1']['A6'])
    P(f'{fd}: max |A1 diff| {np.abs(q-d).max():.4f}; max |A6L-A6| {np.abs(x-a6).max():.4f}')
P('\n## (5) Grouped (twins merged) N-CMAPSS per-arm means (mean over units of seed-averaged unit RMSE)')
rows = list(csv.DictReader(open(D + '/twin/unit_scores.csv', encoding='utf-8')))
for an in ('Q3 首次', 'Q3 A8', 'Q6'):
    sub = [r for r in rows if r['analysis'].startswith(an) and r['protocol'].startswith('孪生')]
    keys = sorted({(r['scenario'], r['arm']) for r in sub})
    for sc, arm in keys:
        v = [float(r['rmse_seed_avg']) for r in sub if r['scenario'] == sc and r['arm'] == arm]
        OUT[f'grp|{an}|{sc}|{arm}'] = float(np.mean(v))
    P(an, ' '.join(f'{sc}/{arm}={OUT[f"grp|{an}|{sc}|{arm}"]:.2f}' for sc, arm in keys))
open(B + '/analysis/round3_checks.md', 'w').write('\n'.join(L) + '\n'); json.dump(OUT, open(B + '/analysis/round3_checks.json', 'w'), indent=1)
print('\n'.join(L))
