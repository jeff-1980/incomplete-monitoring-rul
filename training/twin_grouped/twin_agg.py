"""Twin-grouped recheck aggregation. Compares original leave-one-unit-out (19 folds) with twin-merged leave-one-group-out (16 groups).
Stats: unit score = per-unit RMSE averaged over seeds; Wilcoxon two-sided; Holm within family; bootstrap 95% CI (10000, seed 0) of mean diff.
Reported at unit level (n=19) and group level (n=16, twin scores averaged)."""
import json, glob, csv, numpy as np
from scipy.stats import wilcoxon
Q3O = 'results'; Q6O = 'results'; G = 'results'
rm = lambda e: float(np.sqrt(np.mean(np.square(e))))
def holm(ps):
    ps = np.asarray(ps); o = np.argsort(ps); m = len(ps); adj = np.empty(m); run = 0
    for i, j in enumerate(o): run = max(run, (m - i) * ps[j]); adj[j] = min(1, run)
    return adj
def boot(d, n=10000):
    r = np.random.default_rng(0); i = r.integers(0, len(d), (n, len(d))); return np.percentile(d[i].mean(1), [2.5, 97.5])
def gid(u): p = u.split('_')[1]; return p if p in ('u2', 'u5', 'u10') else u
L = []; P = lambda *a: L.append(' '.join(map(str, a))); ROWS = []

def load(pattern): return [json.load(open(f)) for f in sorted(glob.glob(pattern))]

def scorer(runs, kind):
    """returns units, f(sc, arm) -> seed-averaged unit score array, pooled(sc, arm) -> per-seed pooled RMSE list (q6 only)"""
    units = sorted(runs[0])
    if kind == 'q3':
        f = lambda sc, a: np.mean([[r[u][sc][a] for u in units] for r in runs], 0); pooled = None
    else:
        f = lambda sc, a: np.mean([[rm(r[u][sc][a]) for u in units] for r in runs], 0)
        pooled = lambda sc, a: [rm(np.concatenate([r[u][sc][a] for u in units])) for r in runs]
    return units, f, pooled

def levels(units, x):
    g = sorted(set(gid(u) for u in units)); return {'unit n=19': x, 'group n=16': np.array([np.mean([x[i] for i, u in enumerate(units) if gid(u) == k]) for k in g])}

def compare(tag, units, f, a, b, sc):
    out = {}
    for lv, xs in levels(units, f(sc, a)).items():
        ys = levels(units, f(sc, b))[lv]; d = xs - ys; ci = boot(d)
        out[lv] = dict(diff=d.mean(), ci=ci, better=int((d < 0).sum()), n=len(d), p=wilcoxon(xs, ys).pvalue)
    return out

def section(title, runs_by_proto, kind, arms, scen, tests):
    """tests: list of (family, label, a, b_or_'BEST:..', sc, type) type in {'sup','ni'}"""
    P(f'\n## {title}\n')
    for proto, runs in runs_by_proto.items():
        units, f, pooled = scorer(runs, kind)
        P(f'\n### 均值表（{proto}；机组 RMSE 种子平均后取机组均值' + ('；括号内为逐种子合并 RMSE 均值±sd' if pooled else '') + '）\n')
        P('| 场景 | ' + ' | '.join(arms) + ' |'); P('|---|' + '---|' * len(arms))
        for sc in scen:
            cells = []
            for a in arms:
                if a not in runs[0][units[0]][sc]: cells.append('—'); continue
                c = f'{f(sc, a).mean():.2f}'
                if pooled: pp = pooled(sc, a); c += f' ({np.mean(pp):.2f}±{np.std(pp):.2f})'
                cells.append(c)
            P(f'| {sc} | ' + ' | '.join(cells) + ' |')
        for sc in scen:
            for a in arms:
                if a in runs[0][units[0]][sc]:
                    for u, v in zip(units, f(sc, a)): ROWS.append([title, proto, sc, a, u, gid(u), round(float(v), 4)])
        fams = {}
        for fam, label, a, b, sc, typ in tests:
            if b.startswith('BEST:'):
                cands = b[5:].split(',')
                key = (lambda c: np.mean(pooled(sc, c))) if pooled else (lambda c: f(sc, c).mean())
                b = min(cands, key=key)
            fams.setdefault(fam, []).append((label, a, b, sc, typ, compare(label, units, f, a, b, sc)))
        for fam, rows in fams.items():
            P(f'\n**{fam}**（{proto}）\n'); P('| 检验 | 对照 | 层级 | 差值(前−后) | 95% CI | 前者更好 | p | Holm p | 判定 |'); P('|---|---|---|---|---|---|---|---|---|')
            for lv in ('unit n=19', 'group n=16'):
                adj = holm([r[5][lv]['p'] for r in rows])
                for (label, a, b, sc, typ, res), q in zip(rows, adj):
                    s = res[lv]
                    if typ == 'sup': ok = q < 0.05 and s['diff'] < 0
                    elif typ == 'ni': ok = s['ci'][1] < 1.0
                    else: ok = (s['p'] >= 0.05 or s['diff'] < 0) and s['ci'][1] < 1.0
                    P(f"| {label} | {a} vs {b} | {lv} | {s['diff']:+.2f} | [{s['ci'][0]:+.2f}, {s['ci'][1]:+.2f}] | {s['better']}/{s['n']} | {s['p']:.2g} | {q:.2g} | {'成立' if ok else '不成立'} |")

# Q3 nq3
section('Q3 首次 N-CMAPSS 确证（nq3：A5 对朴素参照）',
        {'原 19 折留一机组': load(f'{Q3O}/nq3_s*.json'), '孪生合并 16 组留一组': load(f'{G}/nq3g_s*.json')}, 'q3',
        ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7'], ['k1', 'k5', 'irr5'],
        [('H1：A5 优于最好朴素（Holm 2 项）', 'k5', 'A5', 'BEST:A1,A2,A3', 'k5', 'sup'),
         ('H1：A5 优于最好朴素（Holm 2 项）', 'irr5', 'A5', 'BEST:A1,A2,A3', 'irr5', 'sup'),
         ('H2：k1 下 A5 对 A1（原判定为不显著更差；另报 CI）', 'k1', 'A5', 'A1', 'k1', 'h2')])
# Q3 nq3b (naive arms from nq3 of same protocol)
def merge(b, a):
    return [{u: {sc: {**a[i][u][sc], **b[i][u][sc]} for sc in b[i][u]} for u in b[i]} for i in range(len(b))]
section('Q3 A8 / GRU-D 的 N-CMAPSS 确证（nq3b）',
        {'原 19 折留一机组': merge(load(f'{Q3O}/nq3b_s*.json'), load(f'{Q3O}/nq3_s*.json')),
         '孪生合并 16 组留一组': merge(load(f'{G}/nq3bg_s*.json'), load(f'{G}/nq3g_s*.json'))}, 'q3',
        ['A1', 'A2', 'A3', 'A5', 'B1_GRUD', 'A8'], ['k1', 'k5', 'irr5'],
        [('H1-A8 非劣（CI 上界<1.0）', 'k5', 'A8', 'A5', 'k5', 'ni'), ('H1-A8 非劣（CI 上界<1.0）', 'irr5', 'A8', 'A5', 'irr5', 'ni'),
         ('H1-A8 优于最好朴素（Holm 2 项）', 'k5', 'A8', 'BEST:A1,A2,A3', 'k5', 'sup'), ('H1-A8 优于最好朴素（Holm 2 项）', 'irr5', 'A8', 'BEST:A1,A2,A3', 'irr5', 'sup'),
         ('H2-A8 k1 非劣', 'k1', 'A8', 'A1', 'k1', 'ni'),
         ('H3-GRU-D 非劣', 'k5', 'B1_GRUD', 'A5', 'k5', 'ni'), ('H3-GRU-D 非劣', 'irr5', 'B1_GRUD', 'A5', 'irr5', 'ni'),
         ('H3-GRU-D 优于最好朴素（Holm 2 项）', 'k5', 'B1_GRUD', 'BEST:A1,A2,A3', 'k5', 'sup'), ('H3-GRU-D 优于最好朴素（Holm 2 项）', 'irr5', 'B1_GRUD', 'BEST:A1,A2,A3', 'irr5', 'sup')])
# Q6
section('Q6 冷启动的 N-CMAPSS 确证（q6n + 附录 q6nx）',
        {'原 19 折留一机组': merge(load(f'{Q6O}/q6nx_s*.json'), load(f'{Q6O}/q6n_s*.json')),
         '孪生合并 16 组留一组': merge(load(f'{G}/q6nxg_s*.json'), load(f'{G}/q6ng_s*.json'))}, 'q6',
        ['A1', 'A2', 'B3', 'B4', 'B2', 'A6L', 'C8'], ['full', 'h5', 'h3'],
        [('H1：B2 优于 min(A1,A2)（Holm 2 项）', 'h5', 'B2', 'BEST:A1,A2', 'h5', 'sup'), ('H1：B2 优于 min(A1,A2)（Holm 2 项）', 'h3', 'B2', 'BEST:A1,A2', 'h3', 'sup'),
         ('H2：完整历史 B2 对 A1', 'full', 'B2', 'A1', 'full', 'h2'),
         ("H1′：C8 优于 min(A1,A2)（Holm 2 项）", 'h5', 'C8', 'BEST:A1,A2', 'h5', 'sup'), ("H1′：C8 优于 min(A1,A2)（Holm 2 项）", 'h3', 'C8', 'BEST:A1,A2', 'h3', 'sup'),
         ("H2′：完整历史 C8 对 A1", 'full', 'C8', 'A1', 'full', 'h2')])
open('results/twin_recheck_summary.md', 'w').write('\n'.join(L)); print('\n'.join(L))
with open('results/twin_recheck_unit_scores.csv', 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['analysis', 'protocol', 'scenario', 'arm', 'unit', 'group', 'rmse_seed_avg']); w.writerows(ROWS)
