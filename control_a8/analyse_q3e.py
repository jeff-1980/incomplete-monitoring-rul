"""Analysis of the A8 history-span control, as fixed in PROTOCOL_A8_control.md."""
import json, numpy as np, os
from scipy.stats import wilcoxon
H = os.path.dirname(os.path.abspath(__file__))
FDS = ['FD001', 'FD002', 'FD003', 'FD004']; SC = ['k1', 'k2', 'k3', 'k5', 'irr5', 'irr10']; ARMS = ['A1', 'A6', 'A8', 'A8F', 'A6S']
LAB = {'k1': 'k = 1', 'k2': 'k = 2', 'k3': 'k = 3', 'k5': 'k = 5', 'irr5': 'irr 1–5', 'irr10': 'irr 1–10'}
rm = lambda e: float(np.sqrt(np.mean(np.square(e))))
R = {fd: [json.load(open(f'{H}/results/q3e_{fd}_s{s}.json')) for s in range(5)] for fd in FDS}
def boot(d, n=10000):
    r = np.random.default_rng(0); return np.percentile([d[r.integers(0, len(d), len(d))].mean() for _ in range(n)], [2.5, 97.5])
def holm(ps):
    o = np.argsort(ps); adj = np.empty(len(ps)); m = len(ps); run = 0
    for r, i in enumerate(o): run = max(run, (m - r) * ps[i]); adj[i] = min(1, run)
    return adj
def cmp(fd, sc, a, b):
    x = np.mean([np.abs(r[sc][a]) for r in R[fd]], 0); y = np.mean([np.abs(r[sc][b]) for r in R[fd]], 0); d = x - y
    return dict(d=float(d.mean()), ci=[float(v) for v in boot(d)], nb=int((d < 0).sum()), n=len(d), p=float(wilcoxon(x, y).pvalue))
S = {}; L = []; P = lambda *a: L.append(' '.join(map(str, a)))
P('## Table S19. A8 history-span control (C-MAPSS, five seeds, all arms trained together): RMSE (cycles), mean ± s.d.\n')
P('A8F: sparse records covering the full 150-cycle window. A6S: consecutive cycles over the span of an A8 window, padded to 150. All four long-input arms receive the same interpolated 150-cycle test input. Protocol written before the run (control_a8/PROTOCOL_A8_control.md).\n')
P('| Subset | Scenario | ' + ' | '.join(ARMS) + ' |'); P('|---|---|' + '---|' * len(ARMS))
for fd in FDS:
    for sc in SC:
        c = []
        for a in ARMS:
            per = [rm(r[sc][a]) for r in R[fd]]; S[f'{fd}|{sc}|{a}'] = dict(rmse=float(np.mean(per)), sd=float(np.std(per, ddof=1))); c.append(f'{np.mean(per):.2f} ± {np.std(per, ddof=1):.2f}')
        P(f'| {fd} | {LAB[sc]} | ' + ' | '.join(c) + ' |')
FAM = [(fd, sc) for fd in FDS for sc in ('k5', 'irr5')]
P('\n## Table S20. A8 history-span control: paired comparisons\n')
P('Δ: seed-averaged engine absolute error, first minus second arm (cycles) [95% bootstrap CI]; engines for which the first arm was better; Wilcoxon p; Holm-adjusted p within the 8 comparisons at k = 5 and irregular 1–5.\n')
for tag, a, b, what in (('C1', 'A8F', 'A6', 'sparsification, full span'), ('C2', 'A8', 'A6S', "sparsification, A8's span and padding"),
                        ('C3', 'A6S', 'A6', 'short padded windows, no sparsification'), ('C4', 'A8F', 'A8', 'full span vs short span, both sparsified')):
    rows = {(fd, sc): cmp(fd, sc, a, b) for fd in FDS for sc in SC}
    adj = holm([rows[k]['p'] for k in FAM]); nsig = int(sum((adj[i] < 0.05) and rows[k]['d'] < 0 for i, k in enumerate(FAM)))
    nsig_rev = int(sum((adj[i] < 0.05) and rows[k]['d'] > 0 for i, k in enumerate(FAM)))
    S[tag] = dict(a=a, b=b, rows={f'{k[0]}|{k[1]}': v for k, v in rows.items()}, holm={f'{k[0]}|{k[1]}': float(adj[i]) for i, k in enumerate(FAM)}, n_sig_first_better=nsig, n_sig_first_worse=nsig_rev)
    P(f'**{tag}: {a} versus {b} ({what}).** Holm-significant in favour of {a}: {nsig} of 8; in favour of {b}: {nsig_rev} of 8.\n')
    P('| Subset | ' + ' | '.join(LAB[s] for s in SC) + ' |'); P('|---|' + '---|' * len(SC))
    for fd in FDS:
        cells = []
        for sc in SC:
            r = rows[(fd, sc)]; h = f"; Holm {S[tag]['holm'][f'{fd}|{sc}']:.2g}" if (fd, sc) in FAM else ''
            cells.append(f"{r['d']:+.2f} [{r['ci'][0]:+.2f}, {r['ci'][1]:+.2f}]; {r['nb']}/{r['n']}; p = {r['p']:.2g}{h}")
        P(f'| {fd} | ' + ' | '.join(cells) + ' |')
    P('')
P('**Complete records (k = 1) against the dense model A1:** ' + '; '.join(f"{fd}: A8F {cmp(fd, 'k1', 'A8F', 'A1')['d']:+.2f} [{cmp(fd, 'k1', 'A8F', 'A1')['ci'][0]:+.2f}, {cmp(fd, 'k1', 'A8F', 'A1')['ci'][1]:+.2f}], A6S {cmp(fd, 'k1', 'A6S', 'A1')['d']:+.2f} [{cmp(fd, 'k1', 'A6S', 'A1')['ci'][0]:+.2f}, {cmp(fd, 'k1', 'A6S', 'A1')['ci'][1]:+.2f}]" for fd in FDS) + '.')
c1, c2, c3 = S['C1']['n_sig_first_better'], S['C2']['n_sig_first_better'], S['C3']['n_sig_first_better']
verdict = ('sparsification carries the gain' if c1 >= 6 and c2 >= 6 else
           'gain mainly from short padded windows' if c3 >= 6 and c1 < 6 and c2 < 6 else 'mixed')
S['verdict'] = verdict; P(f'\nPre-specified reading: {verdict} (C1 {c1}/8, C2 {c2}/8, C3 {c3}/8).')
json.dump(S, open(f'{H}/summary_q3e.json', 'w'), indent=1); open(f'{H}/tables_q3e.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('\n'.join(L))
