"""Screen all N-CMAPSS units (DS01-DS08) for shared flight profiles, using features only (no labels, no models).
Rule: two units are linked if the median over the 32 features of their Pearson correlation over the first min(T1, T2) cycles is >= 0.80.
Profile groups are the connected components. Writes profile_groups.json. Needs ncm_cycles.npz and ncm_cycles_ds03_08.npz."""
import numpy as np, itertools, json, os
H = os.path.dirname(os.path.abspath(__file__)); D = {}
for f in ('ncm_cycles.npz', 'ncm_cycles_ds03_08.npz'):
    z = np.load(os.path.join(H, f))
    for k in z.files:
        if k.endswith('_X'): D[k[:-2]] = z[k]
A = np.concatenate(list(D.values())); mu, sd = A.mean(0), A.std(0) + 1e-6
Z = {k: (v - mu) / sd for k, v in D.items()}; names = sorted(Z); C = {}
for a, b in itertools.combinations(names, 2):
    n = min(len(Z[a]), len(Z[b])); C[(a, b)] = float(np.median([np.corrcoef(Z[a][:n, j], Z[b][:n, j])[0, 1] for j in range(Z[a].shape[1])]))
par = {n: n for n in names}
def find(x):
    while par[x] != x: x = par[x]
    return x
for (a, b), c in C.items():
    if c >= 0.80: par[find(a)] = find(b)
G = {}
for n in names: G.setdefault(find(n), []).append(n)
vals = np.array(list(C.values()))
out = dict(n_units=len(names), n_pairs=len(C), n_linked_pairs=int((vals >= 0.80).sum()), max_unlinked_correlation=float(vals[vals < 0.80].max()),
           min_linked_correlation=float(vals[vals >= 0.80].min()), groups=[sorted(g) for g in G.values() if len(g) > 1],
           linked_pairs=[[a, b, round(c, 3)] for (a, b), c in sorted(C.items(), key=lambda kv: -kv[1]) if c >= 0.80])
json.dump(out, open(os.path.join(H, 'profile_groups.json'), 'w'), indent=1)
print(out['n_units'], 'units;', out['n_linked_pairs'], 'linked pairs; lowest linked', round(out['min_linked_correlation'], 3), '; highest unlinked', round(out['max_unlinked_correlation'], 3), ';', len(out['groups']), 'groups with more than one unit')
