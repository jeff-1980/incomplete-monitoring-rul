"""Post-review experiments (q3b: GRU-D, GAIN+dense, PSR-lite; q3c: A8, A5 test-time checks), conventional RMSE.
Every comparison is against the A5 re-trained in the SAME run (GPU), paired by engine; engine |error| seed-averaged;
two-sided Wilcoxon; exploratory (not pre-registered). Also compares A8 with the original dense model A1 (k=1) and with
the best naive remedies of the pre-registered run (sparse), noting that those come from a different run (CPU)."""
import json, numpy as np
from scipy.stats import wilcoxon
D = str(__import__('pathlib').Path(__file__).resolve().parents[1]) + '/data'; OUT = str(__import__('pathlib').Path(__file__).resolve().parents[1]) + '/analysis'
FDS = ['FD001', 'FD002', 'FD003', 'FD004']
rm = lambda e: float(np.sqrt(np.mean(np.square(e))))
def boot(d, B=10000, seed=0):
    r = np.random.default_rng(seed); n = len(d); b = [d[r.integers(0, n, n)].mean() for _ in range(B)]; return np.quantile(b, [.025, .975])
L = []; P = lambda *a: L.append(' '.join(map(str, a))); S = {}
for tag, arms, scs in [('q3b', ['A5', 'B1_GRUD', 'B2_GAIN', 'B3_PSR'], ['k1', 'k3', 'k5', 'irr5']),
                       ('q3c', ['A5', 'A8'], ['k1', 'k2', 'k3', 'k5', 'irr5', 'irr10'])]:
    P(f'\n## {tag}: conventional RMSE mean±sd over seeds; [Δ mean |e| vs same-run A5, 95% CI, engines better, p]\n')
    P('| Subset | Scenario | ' + ' | '.join(arms) + ' |'); P('|---|---|' + '---|' * len(arms))
    for fd in FDS:
        R = [json.load(open(f'{D}/{tag}_{fd}_s{s}.json')) for s in range(3)]
        for sc in scs:
            E = {a: np.array([r[sc][a] for r in R]) for a in arms}
            cells = []
            for a in arms:
                per = [rm(e) for e in E[a]]; m, sd = np.mean(per), np.std(per, ddof=1)
                key = f'{tag}|{fd}|{sc}|{a}'; S[key] = dict(rmse=float(m), sd=float(sd), bias=float(E[a].mean()))
                if a == 'A5': cells.append(f'{m:.2f}±{sd:.2f}'); continue
                x = np.abs(E[a]).mean(0); y = np.abs(E['A5']).mean(0); d = x - y; ci = boot(d); p = wilcoxon(x, y).pvalue
                S[key].update(d=float(d.mean()), ci=list(map(float, ci)), nb=int((d < 0).sum()), n=len(d), p=float(p))
                cells.append(f'{m:.2f}±{sd:.2f} [{d.mean():+.2f} ({ci[0]:+.2f},{ci[1]:+.2f}); {(d<0).sum()}/{len(d)}; p={p:.2g}]')
            P(f'| {fd} | {sc} | ' + ' | '.join(cells) + ' |')
        if tag == 'q3c':
            for extra, sc in (('A5_gap1', 'k5'), ('A5_as3', 'k1')):
                E = {a: np.array([r[sc][a] for r in R]) for a in ('A5', extra)}
                x = np.abs(E[extra]).mean(0); y = np.abs(E['A5']).mean(0); d = x - y
                S[f'q3c|{fd}|{sc}|{extra}'] = dict(rmse=float(np.mean([rm(e) for e in E[extra]])), sd=float(np.std([rm(e) for e in E[extra]], ddof=1)), d=float(d.mean()), p=float(wilcoxon(x, y).pvalue), nb=int((d<0).sum()), n=len(d))
                P(f'  {fd} {extra} ({sc}): RMSE {S[f"q3c|{fd}|{sc}|{extra}"]["rmse"]:.2f}±{S[f"q3c|{fd}|{sc}|{extra}"]["sd"]:.2f}; Δ vs A5 {d.mean():+.2f}, {(d<0).sum()}/{len(d)}, p={wilcoxon(x,y).pvalue:.2g}')
# A8 vs original dense A1 at k=1 and vs original best naive (different runs; engines are the same test engines)
P('\n## A8 (q3c run) vs pre-registered-run references (different training runs; same test engines)\n')
for fd in FDS:
    Rc = [json.load(open(f'{D}/q3c_{fd}_s{s}.json')) for s in range(3)]; Rq = [json.load(open(f'{D}/q3_{fd}_s{s}.json')) for s in range(3)]
    for sc, ref in (('k1', 'A1'), ('k5', 'A2'), ('irr5', 'A2'), ('k5', 'A6'), ('irr5', 'A6')):
        if fd == 'FD002' and sc in ('k5', 'irr5') and ref == 'A2': ref = 'A1'
        x = np.abs(np.array([r[sc]['A8'] for r in Rc])).mean(0); y = np.abs(np.array([r[sc][ref] for r in Rq])).mean(0); d = x - y; ci = boot(d)
        S[f'A8vs|{fd}|{sc}|{ref}'] = dict(d=float(d.mean()), ci=list(map(float, ci)), nb=int((d<0).sum()), n=len(d), p=float(wilcoxon(x, y).pvalue))
        P(f'{fd} {sc} A8 vs {ref}: Δ {d.mean():+.2f} [{ci[0]:+.2f}, {ci[1]:+.2f}], {(d<0).sum()}/{len(d)}, p={wilcoxon(x,y).pvalue:.2g}')
# reproducibility: A5 CPU (pre-registered run) vs A5 GPU (q3c run)
P('\n## A5 reproducibility: pre-registered run (CPU) vs re-run (GPU), conventional RMSE\n')
for fd in FDS:
    S_ = []
    for sc in ('k1', 'k5', 'irr5'):
        a = np.mean([rm(np.array(json.load(open(f'{D}/q3_{fd}_s{s}.json'))[sc]['A5'])) for s in range(3)])
        b = np.mean([rm(np.array(json.load(open(f'{D}/q3c_{fd}_s{s}.json'))[sc]['A5'])) for s in range(3)])
        S_.append(f'{sc}: {a:.2f} -> {b:.2f}')
    P(fd, '; '.join(S_))
open(f'{OUT}/tables_bc.md', 'w').write('\n'.join(L) + '\n'); json.dump(S, open(f'{OUT}/summary_bc.json', 'w'), indent=1)
print('\n'.join(L))
