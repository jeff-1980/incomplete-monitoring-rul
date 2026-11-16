"""Appendix A aggregation (C8 / A6L). Usage: python3 q6x_agg.py [ncm|cmapss]"""
import sys, os, json, glob, numpy as np
from scipy.stats import wilcoxon
R = os.environ.get('Q6_OUT', 'results'); which = sys.argv[1] if len(sys.argv) > 1 else 'ncm'
rng = np.random.default_rng(0); rm = lambda e: float(np.sqrt(np.mean(np.square(e))))
def holm(ps):
    ps = np.asarray(ps); o = np.argsort(ps); m = len(ps); adj = np.empty(m); run = 0
    for i, j in enumerate(o): run = max(run, (m - i) * ps[j]); adj[j] = min(1, run)
    return adj
def boot(d, n=10000):
    i = rng.integers(0, len(d), (n, len(d))); return np.percentile(d[i].mean(1), [2.5, 97.5])
L = []; P = lambda *a: L.append(' '.join(map(str, a)))
if which == 'ncm':
    main = [json.load(open(f)) for f in sorted(glob.glob(f'{R}/q6n_s*.json'))]
    ext = [json.load(open(f)) for f in sorted(glob.glob(f'{R}/q6nx_s*.json'))]
    assert len(main) == len(ext) == 5
    units = sorted(main[0]); SETS = {'N-CMAPSS': None}; HS = ['full', 'h5', 'h3']; TEST = ['h5', 'h3']
    def get(s, h, a):
        src = ext if a in ('C8', 'A6L') else main
        A = np.array([[rm(r[u][h][a]) for u in units] for r in src])
        per = [rm(np.concatenate([r[u][h][a] for u in units])) for r in src]
        return A.mean(0), per
else:
    SETS = {s: None for s in ['FD001', 'FD002', 'FD003', 'FD004']}; HS = ['full', 'h20', 'h10', 'h5']; TEST = ['h10', 'h5']
    def get(s, h, a):
        fs = sorted(glob.glob(f'{R}/q6x_{s}_s*.json' if a in ('C8', 'A6L') else f'{R}/q6_{s}_s*.json'))
        A = np.array([json.load(open(f))[h][a] for f in fs]); return np.abs(A).mean(0), [rm(x) for x in A]
tag = '（预先写定）' if which == 'ncm' else '（探索性：C-MAPSS 结果已知后补跑，不进判定）'
P(f'## 附录 A 主表 RMSE（逐种子，均值 ± 标准差）{tag}\n')
arms = ['A1', 'A2', 'B2', 'A6L', 'C8']
P('| 数据 | 历史 | ' + ' | '.join(arms) + ' |'); P('|---|---|' + '---|' * len(arms))
for s in SETS:
    for h in HS:
        P(f'| {s} | {h} | ' + ' | '.join(f'{np.mean(get(s,h,a)[1]):.2f} ± {np.std(get(s,h,a)[1]):.2f}' for a in arms) + ' |')
P(f'\n## H1′：C8 对 min(A1, A2)，Holm\n'); P('| 数据 | 历史 | 最好朴素 | 机组级差 | C8 更好机组 | p | Holm p |'); P('|---|---|---|---|---|---|---|')
rows = []
for s in SETS:
    for h in TEST:
        best = min(['A1', 'A2'], key=lambda a: np.mean(get(s, h, a)[1])); x, y = get(s, h, 'C8')[0], get(s, h, best)[0]
        rows.append((s, h, best, (x - y).mean(), ((x - y) < 0).sum(), len(x), wilcoxon(x, y).pvalue))
adj = holm([r[6] for r in rows]); n1 = 0
for r, q in zip(rows, adj):
    n1 += (q < 0.05 and r[3] < 0); P(f'| {r[0]} | {r[1]} | {r[2]} | {r[3]:+.2f} | {r[4]}/{r[5]} | {r[6]:.2g} | {q:.2g} |')
P(f'\nH1′ {n1}/{len(rows)}')
P('\n## H2′：完整历史 C8 对 A1\n'); P('| 数据 | 机组级差 | 95% CI | C8 更好机组 | p | 判定 |'); P('|---|---|---|---|---|---|'); n2 = 0
for s in SETS:
    x, y = get(s, 'full', 'C8')[0], get(s, 'full', 'A1')[0]; d = x - y; ci = boot(d); p = wilcoxon(x, y).pvalue
    ok = (p >= 0.05 or d.mean() < 0) and ci[1] < 1.0; n2 += ok
    P(f'| {s} | {d.mean():+.2f} | [{ci[0]:+.2f}, {ci[1]:+.2f}] | {(d<0).sum()}/{len(d)} | {p:.2g} | {"通过" if ok else "未通过"} |')
P(f'\nH2′ {n2}/{len(SETS)}')
for nm, a, b in [('C8 对 B2', 'C8', 'B2'), ('C8 对 A6L', 'C8', 'A6L'), ('A6L 对 A1（窗口变长本身的作用）', 'A6L', 'A1')]:
    P(f'\n## 描述性：{nm}（机组级差，负=前者更好）\n'); P('| 数据 | ' + ' | '.join(HS) + ' |'); P('|---|' + '---|' * len(HS))
    for s in SETS:
        cs = []
        for h in HS:
            x, y = get(s, h, a)[0], get(s, h, b)[0]; d = x - y; cs.append(f'{d.mean():+.2f} ({(d<0).sum()}/{len(d)}, p={wilcoxon(x,y).pvalue:.1g})')
        P(f'| {s} | ' + ' | '.join(cs) + ' |')
open(f'{R}/q6x_summary_{which}.md', 'w').write('\n'.join(L)); print('\n'.join(L))
