"""Structure only, part 2 (no model). Usage: python3 inspect_structure2.py <export_dir>"""
import sys, pandas as pd, numpy as np
d = sys.argv[1]; pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 90); pd.set_option('display.max_rows', 300)
x = pd.read_csv(f'{d}/xjtu.csv.gz')
for b, g in x.groupby('batch'):
    print('==', b, g.protocol.iloc[0]); print(g.cycle_description.value_counts().to_string())
    c = g[g.battery_id == g.battery_id.iloc[0]]; print(c[['cycle', 'cycle_description', 'discharge_capacity_Ah', 'duration_min']].head(14).to_string())
m = pd.read_csv(f'{d}/mit.csv.gz', low_memory=False)
rows = []
for k, g in m.groupby('battery_id'):
    g = g.sort_values('cycle'); q = g.discharge_capacity_Ah.values; c = g.cycle.values
    sust = next((int(c[i]) for i in range(10, len(q) - 2) if (q[i:i + 3] < 0.88).all()), -1)
    rows.append(dict(batch=g.batch.iloc[0], cell=k, n=len(g), q_last=q[-1], sust=sust, zero=int((q <= 0).sum()), big=int((q > 1.3).sum()), ir0=int((g.internal_resistance_ohm <= 0).sum()),
                     t0=int((g.temp_mean_C <= 0).sum()), ct_big=int((g.charge_time_min > 60).sum())))
r = pd.DataFrame(rows); r['eol'] = np.where(r.sust > 0, r.sust, np.where(r.q_last <= 0.885, r.n, -1))
print(r.groupby('batch').agg(cells=('n', 'size'), reached=('eol', lambda v: int((v > 0).sum())), zero=('zero', 'sum'), big=('big', 'sum'), ir0=('ir0', 'sum'), t0=('t0', 'sum'), ct_big=('ct_big', 'sum')))
e = r[r.eol > 0]; print('MIT eol quantiles', e.eol.quantile([0, .1, .25, .5, .75, .9, 1]).round(0).tolist(), 'cells', len(e))
print(e.groupby('batch').eol.describe().round(0))
print('excluded:', r[r.eol < 0][['cell', 'n', 'q_last']].to_string())
print('policies per cell unique:', m.groupby('battery_id').protocol_code.first().nunique(), ' cells per policy max', m.groupby('battery_id').protocol_code.first().value_counts().max())
