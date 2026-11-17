"""Descriptive check of three definitions of the battery protocol as implemented in rslib.py (added after the runs; no model is trained).
Usage: python3 check_definitions.py <export_dir> [<per-cell csv of one XJTU cell from the export>]"""
import sys, numpy as np, pandas as pd, rslib as R
exp = sys.argv[1]; out = []
df = pd.read_csv(f'{exp}/mit.csv.gz', low_memory=False); route = {'sustained': 0, 'last_record': 0, 'excluded': 0}; first = 0; later = 0; ncell = 0; nval = 0; qend = []
for (b, c), g in df.groupby(['batch', 'battery_id']):
    g = g.sort_values('cycle'); X = g[R.FEATS['mit']].to_numpy(float); q = X[:, 0]
    eol = next((i for i in range(10, len(q) - 2) if (q[i:i + 3] < 0.88).all()), None)
    if eol is None:
        if q[-1] > 0.885: route['excluded'] += 1; continue
        eol = len(q) - 1; route['last_record'] += 1; qend.append(q[-1])
    else: route['sustained'] += 1
    X = X[:eol + 1]; bad = X <= 0
    bad[:, 0] |= (X[:, 0] < 0.55) | (X[:, 0] > 1.43); bad[:, 1] |= (X[:, 1] < 0.55) | (X[:, 1] > 1.43); bad[:, 6] |= X[:, 6] > 60
    lead = 0
    while lead < len(X) and bad[lead].any(): lead += 1
    first += int(bad[:lead].sum()); later += int(bad[lead:].sum()); ncell += int(lead > 0); nval += X.size
out.append(f"MIT end of life: {route['sustained']} cells by three consecutive capacities below 0.88 Ah; {route['last_record']} cells by the last recorded cycle (record ends at {min(qend):.4f}-{max(qend):.4f} Ah, never three values below 0.88 Ah); {route['excluded']} excluded.")
out.append(f"MIT invalid values among {nval} feature values of the included cells: {first} in leading rows of {ncell} cells (filled with the next valid value, i.e. backward), {later} later (filled with the previous valid value).")
for ds in ('mit', 'xjtu'):
    cells = R.load(ds, exp); n = {30: 0, 40: 0, 50: 0}; tot = 0
    for v in cells.values():
        ts = list(range(R.T0, len(v['X']), R.K)); tot += len(ts)
        for t in n: n[t] += int(t in ts)
    out.append(f"{ds}: {tot} prediction times; at t = 30, 40, 50 ({sum(n.values())} predictions, {100 * sum(n.values()) / tot:.1f}%) the blk scenario has no record before the outage: only the last three records are available, and the outage is the whole earlier history (27, 37, 47 cycles) rather than 50 cycles.")
if len(sys.argv) > 2:
    a = pd.read_csv(sys.argv[2]); x = pd.read_csv(f'{exp}/xjtu.csv.gz'); b = x[(x.batch == a.batch.iloc[0]) & (x.battery_id == a.battery_id.iloc[0])].reset_index(drop=True)
    same = a.shape == b.shape and all((a[c].astype(str) == b[c].astype(str)).all() if not pd.api.types.is_numeric_dtype(a[c]) else np.allclose(a[c], b[c], equal_nan=True) for c in a.columns)
    out.append(f"XJTU per-cell table {a.batch.iloc[0]} {a.battery_id.iloc[0]} ({len(a)} rows) equals its rows in the merged table: {same}.")
open('check_definitions.md', 'w', encoding='utf-8').write('\n'.join(out) + '\n'); print('\n'.join(out))
