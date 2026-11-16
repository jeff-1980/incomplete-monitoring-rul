"""PC-MambaSDE (B4) vs same-batch q3d arms. Usage: python3 q3m_agg.py DIR  (DIR holds q3d_*.json and q3m_*.json)"""
import sys, json, numpy as np
from scipy.stats import wilcoxon
D = sys.argv[1]; FD = ['FD001', 'FD002', 'FD003', 'FD004']; SC = ['k1', 'k2', 'k3', 'k5', 'irr5', 'irr10']; S = range(5)
rm = lambda e: float(np.sqrt(np.mean(np.square(e))))
def holm(p):
    o = np.argsort(p); m = len(p); adj = np.empty(m); run = 0
    for r, i in enumerate(o): run = max(run, (m - r) * p[i]); adj[i] = min(1, run)
    return adj
E = {}
for fd in FD:
    q = [json.load(open(f'{D}/q3d_{fd}_s{s}.json')) for s in S]; m = [json.load(open(f'{D}/q3m_{fd}_s{s}.json')) for s in S]
    for sc in SC:
        for a in ['A1', 'A2', 'A5', 'A8', 'B1_GRUD']: E[fd, sc, a] = np.array([x[sc][a] for x in q])
        E[fd, sc, 'B4'] = np.array([x[sc]['B4_PCMambaSDE'] for x in m])
out = ['# PC-MambaSDE 同协议对比汇总\n', '## RMSE（5 种子平均的逐种子 RMSE）\n', '| 子集 | 场景 | A1 | A2 | A5 | A8 | GRU-D | PC-MambaSDE |', '|---|---|---|---|---|---|---|---|']
for fd in FD:
    for sc in SC:
        out.append(f'| {fd} | {sc} | ' + ' | '.join(f"{np.mean([rm(e) for e in E[fd, sc, a]]):.2f}" for a in ['A1', 'A2', 'A5', 'A8', 'B1_GRUD', 'B4']) + ' |')
for ref in ['A8', 'A5', 'B1_GRUD']:
    out += [f'\n## PC-MambaSDE 对 {ref}（机组级，|误差| 先在 5 种子上平均；Holm 族 = 4 子集 × k5、irr5）\n', '| 子集 | 场景 | 差值(B4−ref) | B4 更好的机组 | p | Holm p |', '|---|---|---|---|---|---|']
    rows = []
    for fd in FD:
        for sc in SC:
            a = np.abs(E[fd, sc, 'B4']).mean(0); b = np.abs(E[fd, sc, ref]).mean(0); d = a - b
            rows.append((fd, sc, d.mean(), (d < 0).sum(), len(d), wilcoxon(a, b).pvalue))
    fam = [i for i, r in enumerate(rows) if r[1] in ('k5', 'irr5')]; adj = dict(zip(fam, holm(np.array([rows[i][5] for i in fam]))))
    for i, (fd, sc, dm, nb, n, p) in enumerate(rows):
        out.append(f'| {fd} | {sc} | {dm:+.2f} | {nb}/{n} | {p:.2g} | {adj[i]:.2g} |' if i in adj else f'| {fd} | {sc} | {dm:+.2f} | {nb}/{n} | {p:.2g} | — |')
open(f'{D}/q3m_summary.md', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
