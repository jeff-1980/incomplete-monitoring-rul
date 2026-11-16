import json, numpy as np
from scipy.stats import wilcoxon
FDS=['FD001','FD002','FD003','FD004']; SC=['k1','k2','k3','k5','irr5','irr10']
R={}
for fd in FDS:
    runs=[json.load(open(f'results/q3_{fd}_s{s}.json')) for s in range(3)]
    R[fd]={sc:{a:np.array([r[sc][a] for r in runs]) for a in runs[0][sc]} for sc in SC}   # seeds x engines (signed err)
rm=lambda e: float(np.sqrt(np.mean(e**2)))
def holm(ps):
    o=np.argsort(ps); m=len(ps); adj=np.empty(m); run=0
    for i,j in enumerate(o): run=max(run,(m-i)*ps[j]); adj[j]=min(1,run)
    return adj
L=[]; P=lambda *a: L.append(' '.join(map(str,a)))
P('## RMSE（3 种子误差平均后的机组级 RMSE；括号内为逐种子 RMSE 范围）\n')
P('| 子集 | 场景 | A1 密集 | A2 插值 | A3 前值 | A4 混合无通道 | **A5 本方法** | A6 长窗口 | A7 按间隔 |'); P('|---|---|---|---|---|---|---|---|---|')
for fd in FDS:
    for sc in SC:
        cells=[]
        for a in ['A1','A2','A3','A4','A5','A6','A7']:
            if a not in R[fd][sc]: cells.append('—'); continue
            E=R[fd][sc][a]; ae=np.abs(E).mean(0); per=[rm(e) for e in E]
            cells.append(f'{rm(ae):.2f}' if a!='A5' else f'**{rm(ae):.2f}**')
        P(f'| {fd} | {sc} | '+' | '.join(cells)+' |')
def cmp(fd,sc,a,b):
    x=np.abs(R[fd][sc][a]).mean(0); y=np.abs(R[fd][sc][b]).mean(0); d=x-y
    return d.mean(), (d<0).sum(), len(d), wilcoxon(x,y).pvalue
P('\n## H1：A5 对最好的朴素参照（S4=k5、S5=irr5），Holm 校正 8 个比较\n')
P('| 子集 | 场景 | 最好朴素 | 其 RMSE | A5 RMSE | 平均绝对误差差 | A5 更好机组 | p | Holm p | 逐种子 A5<朴素 |'); P('|---|---|---|---|---|---|---|---|---|---|')
rows=[]
for fd in FDS:
    for sc in ['k5','irr5']:
        best=min(['A1','A2','A3'],key=lambda a: rm(np.abs(R[fd][sc][a]).mean(0)))
        d,nb,n,p=cmp(fd,sc,'A5',best)
        seeds=sum(rm(R[fd][sc]['A5'][s])<rm(R[fd][sc][best][s]) for s in range(3))
        rows.append([fd,sc,best,rm(np.abs(R[fd][sc][best]).mean(0)),rm(np.abs(R[fd][sc]['A5']).mean(0)),d,nb,n,p,seeds])
adj=holm(np.array([r[8] for r in rows])); passed=0
for r,a in zip(rows,adj):
    ok=a<0.05 and r[5]<0; passed+=ok
    P(f'| {r[0]} | {r[1]} | {r[2]} | {r[3]:.2f} | {r[4]:.2f} | {r[5]:+.2f} | {r[6]}/{r[7]} | {r[8]:.2g} | {a:.2g} | {r[9]}/3 |')
P(f'\nH1 通过比较数：{passed}/8（标准 ≥7）')
P('\n## H2：k=1 标准设置，A5 对 A1（双侧，不显著差于即通过）\n')
P('| 子集 | A1 | A5 | 差 | A5 更好机组 | p | 判定 |'); P('|---|---|---|---|---|---|---|'); h2=0
for fd in FDS:
    d,nb,n,p=cmp(fd,'k1','A5','A1'); ok=(p>=0.05) or d<0; h2+=ok
    P(f"| {fd} | {rm(np.abs(R[fd]['k1']['A1']).mean(0)):.2f} | {rm(np.abs(R[fd]['k1']['A5']).mean(0)):.2f} | {d:+.2f} | {nb}/{n} | {p:.2g} | {'通过' if ok else '未通过'} |")
P(f'\nH2 通过子集：{h2}/4（标准 4/4）')
for name,a,b,scs in [('H3：A5 对 A4（间隔通道是否必要）','A5','A4',SC),('H4：A5 对 A6（是否只是看得更远）','A5','A6',['k1','k5','irr5']),('H5：A5 对 A7（按间隔单独训练）','A5','A7',['k2','k3','k5'])]:
    P(f'\n## {name}\n'); P('| 子集 | '+' | '.join(scs)+' |'); P('|---|'+'---|'*len(scs))
    for fd in FDS:
        cs=[]
        for sc in scs:
            d,nb,n,p=cmp(fd,sc,a,b); cs.append(f'{d:+.2f} ({nb}/{n}, p={p:.1g})')
        P(f'| {fd} | '+' | '.join(cs)+' |')
open('results/q3_summary.md','w').write('\n'.join(L)); print('\n'.join(L))
