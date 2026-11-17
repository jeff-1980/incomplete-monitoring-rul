"""Structure of the battery tables only (no model is trained here). Usage: python3 -I inspect_structure.py <export_dir>"""
import sys, pandas as pd, numpy as np
d = sys.argv[1]
for name, nom in (('mit', 1.1), ('xjtu', 2.0)):
    df = pd.read_csv(f'{d}/{name}.csv.gz', low_memory=False)
    print('=====', name, df.shape, 'cells', df.battery_id.nunique() if name == 'mit' else df.groupby(['batch', 'battery_id']).ngroups)
    print(df.isna().mean().round(3).to_dict())
    key = ['batch', 'battery_id']
    rows = []
    for k, g in df.groupby(key):
        g = g.sort_values('cycle'); q = g.discharge_capacity_Ah.values; c = g.cycle.values
        below = np.where(q < 0.8 * nom)[0]; ok = (q > 0.5 * nom) & (q < 1.3 * nom)
        rows.append(dict(batch=k[0], cell=k[1], n=len(g), cmin=c.min(), cmax=c.max(), contiguous=bool((np.diff(c) == 1).all()), bad=int((~ok).sum()),
                         q_first=float(np.median(q[ok][:5])) if ok.sum() > 5 else np.nan, q_last=float(q[-1]), first_below=int(c[below[0]]) if len(below) else -1,
                         first_below_sust=int(next((c[i] for i in range(len(q) - 2) if (q[i:i + 3] < 0.8 * nom).all()), -1))))
    r = pd.DataFrame(rows); pd.set_option('display.width', 250); pd.set_option('display.max_rows', 300)
    print(r.groupby('batch').agg(cells=('n', 'size'), n_min=('n', 'min'), n_med=('n', 'median'), n_max=('n', 'max'), bad=('bad', 'sum'), contig=('contiguous', 'mean'),
                                 qlast_med=('q_last', 'median'), no_eol=('first_below_sust', lambda x: int((x < 0).sum()))))
    print(r.describe().round(2))
    print(r[(r.first_below_sust < 0) | (r.bad > 5) | (~r.contiguous)].to_string())
    if name == 'xjtu': print(df.groupby('batch').cycle_description.agg(lambda x: x.value_counts().head(4).to_dict()).to_string())
    num = df.select_dtypes('number').columns; print(df[num].describe().T[['min', '50%', 'max']].round(3))
