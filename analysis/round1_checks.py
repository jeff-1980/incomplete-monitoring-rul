"""Round-1 reviewer checks that need no retraining (all labelled exploratory / sensitivity)."""
import json, numpy as np
from scipy.stats import wilcoxon
D = str(__import__('pathlib').Path(__file__).resolve().parents[1]) + '/data'
FDS = ['FD001', 'FD002', 'FD003', 'FD004']
rm = lambda e: float(np.sqrt(np.mean(np.square(e))))
phm = lambda e: np.where(e < 0, np.exp(-e / 13) - 1, np.exp(e / 10) - 1)
def holm(ps):
    ps = np.asarray(ps); o = np.argsort(ps); m = len(ps); adj = np.empty(m); run = 0
    for i, j in enumerate(o): run = max(run, (m - i) * ps[j]); adj[j] = min(1, run)
    return adj
R = {fd: [json.load(open(f'{D}/q3_{fd}_s{s}.json')) for s in range(3)] for fd in FDS}
E = lambda fd, sc, a: np.array([r[sc][a] for r in R[fd]])
L = []; P = lambda *a: L.append(' '.join(map(str, a)))

P('## 1. H1 sensitivity: best naive chosen from {A1, A2, A3, A6} (A6 = interpolation over 150 cycles, i.e. history-matched)')
rows = []
for fd in FDS:
    for sc in ['k5', 'irr5']:
        cand = ['A1', 'A2', 'A3', 'A6']
        best = min(cand, key=lambda a: np.mean([rm(e) for e in E(fd, sc, a)]))
        x = np.abs(E(fd, sc, 'A5')).mean(0); y = np.abs(E(fd, sc, best)).mean(0)
        rows.append((fd, sc, best, np.mean([rm(e) for e in E(fd, sc, best)]), np.mean([rm(e) for e in E(fd, sc, 'A5')]), (x - y).mean(), (x < y).sum(), len(x), wilcoxon(x, y).pvalue))
for r, a in zip(rows, holm([r[8] for r in rows])):
    P(f'{r[0]} {r[1]}: best={r[2]} {r[3]:.2f} vs A5 {r[4]:.2f}; d={r[5]:+.2f}; {r[6]}/{r[7]}; p={r[8]:.2g}; Holm={a:.2g}')

P('\n## 2. Seed-level H1: Wilcoxon per seed (no seed averaging), A5 vs pre-registered best naive')
best_pre = {('FD001','k5'):'A2',('FD001','irr5'):'A2',('FD002','k5'):'A1',('FD002','irr5'):'A1',('FD003','k5'):'A2',('FD003','irr5'):'A2',('FD004','k5'):'A2',('FD004','irr5'):'A2'}
for (fd, sc), b in best_pre.items():
    ps = [wilcoxon(np.abs(E(fd, sc, 'A5')[s]), np.abs(E(fd, sc, b)[s])).pvalue for s in range(3)]
    P(f'{fd} {sc} vs {b}: per-seed p = ' + ', '.join(f'{p:.2g}' for p in ps))

P('\n## 3. Out-of-range irr 1–10 (exploratory): A5 vs best naive {A1,A2,A3}')
for fd in FDS:
    best = min(['A1', 'A2', 'A3'], key=lambda a: np.mean([rm(e) for e in E(fd, 'irr10', a)]))
    x = np.abs(E(fd, 'irr10', 'A5')).mean(0); y = np.abs(E(fd, 'irr10', best)).mean(0)
    P(f'{fd}: best={best}; d={(x-y).mean():+.2f}; {(x<y).sum()}/{len(x)}; p={wilcoxon(x,y).pvalue:.2g}')

P('\n## 4. PHM score robustness: per seed sum, median over seeds, and worst single engine')
for fd in FDS:
    for sc in ['k1', 'k5', 'irr5']:
        for a in ['A1', 'A2', 'A4', 'A5', 'A6', 'A7']:
            if a not in R[fd][0][sc]: continue
            s = [phm(e).sum() for e in E(fd, sc, a)]; w = [(round(float(e.max()), 1)) for e in E(fd, sc, a)]
            P(f'{fd} {sc} {a}: per-seed {[round(x) for x in s]}, median {np.median(s):.0f}, max late error per seed {w}')

P('\n## 5. Bias (mean signed error, + = late/over-estimate) of A5 vs A1/A2 at k5')
for fd in FDS:
    P(fd, ' '.join(f"{a}:{E(fd,'k5',a).mean():+.2f}" for a in ['A1', 'A2', 'A5', 'A6', 'A7']))
out = '\n'.join(L); open(str(__import__('pathlib').Path(__file__).resolve().parents[1]) + '/analysis/round1_checks.md', 'w').write(out + '\n'); print(out)
