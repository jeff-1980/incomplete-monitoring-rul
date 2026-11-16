"""Q6 (short history / cold start): recompute from per-engine errors. Conventional RMSE per seed (5 seeds) mean ± sd.
C-MAPSS stats: engine |error| averaged over seeds; N-CMAPSS: unit RMSE (over streamed predictions) averaged over seeds.
Pre-registered: H1 (B2 vs best of A1/A2 at h10,h5 [C-MAPSS] / h5,h3 [N-CMAPSS], Holm), H2 (full history B2 vs A1: not
significantly worse AND bootstrap CI upper < +1.0); appendix H1'/H2' for C8 on N-CMAPSS. C-MAPSS C8/A6L exploratory."""
import json, numpy as np
from scipy.stats import wilcoxon
D = str(__import__('pathlib').Path(__file__).resolve().parents[1]) + '/data/q6'; OUT = str(__import__('pathlib').Path(__file__).resolve().parents[1]) + '/analysis'
FDS = ['FD001', 'FD002', 'FD003', 'FD004']; rm = lambda e: float(np.sqrt(np.mean(np.square(e))))
def boot(d, B=10000):
    r = np.random.default_rng(0); n = len(d); b = [d[r.integers(0, n, n)].mean() for _ in range(B)]; return np.quantile(b, [.025, .975])
def holm(ps):
    ps = np.asarray(ps); o = np.argsort(ps); m = len(ps); adj = np.empty(m); run = 0
    for i, j in enumerate(o): run = max(run, (m - i) * ps[j]); adj[j] = min(1, run)
    return adj
S = {}; L = []; P = lambda *a: L.append(' '.join(map(str, a)))
# ---------------- C-MAPSS ----------------
R = {fd: [json.load(open(f'{D}/q6_{fd}_s{s}.json')) for s in range(5)] for fd in FDS}
X = {fd: [json.load(open(f'{D}/q6x_{fd}_s{s}.json')) for s in range(5)] for fd in FDS}
def E(fd, h, a):
    src = X if a in ('C8', 'A6L') else R
    return np.array([r[h][a] for r in src[fd]])
HS = ['full', 'h20', 'h10', 'h5']; ARMS = ['A1', 'A2', 'B3', 'B2', 'B4', 'C8', 'A6L']
P('## Q6 C-MAPSS RMSE (mean ± sd over 5 seeds)\n'); P('| Subset | History | ' + ' | '.join(ARMS) + ' |'); P('|---|---|' + '---|' * len(ARMS))
for fd in FDS:
    for h in HS:
        c = []
        for a in ARMS:
            try: e = E(fd, h, a)
            except KeyError: c.append('—'); continue
            per = [rm(x) for x in e]; S[f'c|{fd}|{h}|{a}'] = dict(rmse=float(np.mean(per)), sd=float(np.std(per, ddof=1)))
            c.append(f'{np.mean(per):.2f} ± {np.std(per, ddof=1):.2f}')
        P(f'| {fd} | {h} | ' + ' | '.join(c) + ' |')
def cmp(fd, h, a, b):
    x = np.abs(E(fd, h, a)).mean(0); y = np.abs(E(fd, h, b)).mean(0); d = x - y; ci = boot(d)
    return dict(d=float(d.mean()), ci=list(map(float, ci)), nb=int((d < 0).sum()), n=len(d), p=float(wilcoxon(x, y).pvalue))
P('\n### H1 (pre-registered): B2 vs best of A1/A2, Holm over 8')
rows = []
for fd in FDS:
    for h in ('h10', 'h5'):
        best = min(['A1', 'A2'], key=lambda a: S[f'c|{fd}|{h}|{a}']['rmse']); r = cmp(fd, h, 'B2', best); r['best'] = best; rows.append((fd, h, r))
for (fd, h, r), a in zip(rows, holm([r['p'] for _, _, r in rows])):
    r['p_holm'] = float(a); S[f'H1c|{fd}|{h}'] = r
    P(f"{fd} {h}: best {r['best']} {S[f'c|{fd}|{h}|{r['best']}']['rmse']:.2f} vs B2 {S[f'c|{fd}|{h}|B2']['rmse']:.2f}; Δ {r['d']:+.2f} [{r['ci'][0]:+.2f},{r['ci'][1]:+.2f}]; {r['nb']}/{r['n']}; p={r['p']:.2g}; Holm={a:.2g}")
P('\n### H2 (pre-registered): full history, B2 vs A1 (pass = not sig. worse AND CI upper < 1.0)')
for fd in FDS:
    r = cmp(fd, 'full', 'B2', 'A1'); ok = (r['p'] >= 0.05 or r['d'] < 0) and r['ci'][1] < 1.0; r['pass'] = bool(ok); S[f'H2c|{fd}'] = r
    P(f"{fd}: Δ {r['d']:+.2f} [{r['ci'][0]:+.2f},{r['ci'][1]:+.2f}]; p={r['p']:.2g} -> {'pass' if ok else 'FAIL'}")
P('\n### Exploratory (C-MAPSS): C8 vs A1 (full), C8 vs B2 (h10,h5), C8 vs A6L, B2 vs B3, B2 vs B4')
for fd in FDS:
    for a, b, hs in (('C8', 'A1', ['full']), ('C8', 'B2', ['full', 'h10', 'h5']), ('C8', 'A6L', ['full', 'h10', 'h5']), ('B2', 'B3', ['full', 'h10', 'h5']), ('B2', 'B4', ['h20', 'h10', 'h5'])):
        for h in hs:
            r = cmp(fd, h, a, b); S[f'xc|{a}|{b}|{fd}|{h}'] = r
            P(f"{fd} {h} {a} vs {b}: Δ {r['d']:+.2f} [{r['ci'][0]:+.2f},{r['ci'][1]:+.2f}]; {r['nb']}/{r['n']}; p={r['p']:.2g}")
# ---------------- N-CMAPSS ----------------
N = [json.load(open(f'{D}/q6n_s{s}.json')) for s in range(5)]; NX = [json.load(open(f'{D}/q6nx_s{s}.json')) for s in range(5)]
units = sorted(N[0]); NH = ['full', 'h5', 'h3']
def nsrc(a): return NX if a in ('C8', 'A6L') else N
def uv(h, a):  # unit RMSE per seed, averaged over seeds
    return np.array([np.mean([rm(np.array(nsrc(a)[s][u][h][a])) for s in range(5)]) for u in units])
def nrm(h, a):  # mean over units, per seed -> mean ± sd
    per = [np.mean([rm(np.array(nsrc(a)[s][u][h][a])) for u in units]) for s in range(5)]; return float(np.mean(per)), float(np.std(per, ddof=1))
P('\n## Q6 N-CMAPSS (19 units): mean unit RMSE, mean ± sd over 5 seeds')
NA = [a for a in ['A1', 'A2', 'B3', 'B2', 'B4', 'C8', 'A6L'] if a in N[0][units[0]]['h5'] or a in NX[0][units[0]]['h5']]
for h in NH:
    c = []
    for a in NA:
        try: m, sd = nrm(h, a); S[f'n|{h}|{a}'] = dict(rmse=m, sd=sd); c.append(f'{a} {m:.2f}±{sd:.2f}')
        except KeyError: pass
    P(h, ' | '.join(c))
def ncmp(h, a, b):
    x, y = uv(h, a), uv(h, b); d = x - y; ci = boot(d); return dict(d=float(d.mean()), ci=list(map(float, ci)), nb=int((d < 0).sum()), n=len(d), p=float(wilcoxon(x, y).pvalue))
for arm, tag in (('B2', 'H1/H2'), ('C8', "H1'/H2'")):
    rows = []
    for h in ('h5', 'h3'):
        best = min(['A1', 'A2'], key=lambda a: S[f'n|{h}|{a}']['rmse']); r = ncmp(h, arm, best); r['best'] = best; rows.append((h, r))
    for (h, r), a in zip(rows, holm([r['p'] for _, r in rows])):
        r['p_holm'] = float(a); S[f'H1n|{arm}|{h}'] = r
        P(f"N-CMAPSS {tag} {arm} {h}: vs {r['best']} Δ {r['d']:+.2f} [{r['ci'][0]:+.2f},{r['ci'][1]:+.2f}]; {r['nb']}/19; p={r['p']:.2g}; Holm={a:.2g}")
    r = ncmp('full', arm, 'A1'); ok = (r['p'] >= 0.05 or r['d'] < 0) and r['ci'][1] < 1.0; r['pass'] = bool(ok); S[f'H2n|{arm}'] = r
    P(f"N-CMAPSS {tag} {arm} full vs A1: Δ {r['d']:+.2f} [{r['ci'][0]:+.2f},{r['ci'][1]:+.2f}]; p={r['p']:.2g} -> {'pass' if ok else 'FAIL'}")
for h in NH:
    r = ncmp(h, 'C8', 'B2'); S[f'xn|C8|B2|{h}'] = r; P(f"N-CMAPSS {h} C8 vs B2: Δ {r['d']:+.2f} [{r['ci'][0]:+.2f},{r['ci'][1]:+.2f}]; p={r['p']:.2g}")
open(f'{OUT}/tables_q6.md', 'w').write('\n'.join(L) + '\n'); json.dump(S, open(f'{OUT}/summary_q6.json', 'w'), indent=1)
print('\n'.join(L))
