"""Export XJTU battery dataset (Zenodo 10963339) to per-battery cycle tables + raw curves of cycles 1/10/50/100. No normalisation, no EOL labelling."""
import scipy.io as sio, numpy as np, pandas as pd, glob, os, json
SRC = '/root/dl/battery/ex/Battery Dataset'; OUT = '/root/work/battery/out'; os.makedirs(f'{OUT}/cycles', exist_ok=True); os.makedirs(f'{OUT}/raw_curves', exist_ok=True)
PROTO = {'Batch-1': ('2C', 'CC-CV 2C(4A) charge; 1C(2A) full discharge to 2.5V'),
         'Batch-2': ('3C', 'CC-CV 3C(6A) charge; 1C(2A) full discharge to 2.5V'),
         'Batch-3': ('R2.5', 'CC-CV 2C charge; discharge at x C to 2.5V, x cycles {0.5,1,2,3,5}'),
         'Batch-4': ('R3', 'CC-CV 2C charge; discharge at x C to 3.0V, x cycles {0.5,1,2,3,5}; capacity test (2C charge, 1C to 2.5V) after each cycle'),
         'Batch-5': ('RW', 'random-walk partial discharge (x A for y min, stop at 3.0V); capacity test (1C/1C to 2.5V) every 11th cycle from cycle 21'),
         'Batch-6': ('Sim_satellite', 'GEO-satellite profile: CC-CV 2C charge, 0.667C discharge of varying duration; capacity test (1C charge, 0.5C to 2.5V) about every 5 cycles')}
SUMK = ['charge_capacity_Ah', 'discharge_capacity_Ah', 'charge_power_Wh', 'discharge_power_Wh', 'charge_median_voltage', 'discharge_median_voltage', 'charge_mean_voltage', 'discharge_mean_voltage']
allrows = []; log = []
for f in sorted(glob.glob(f'{SRC}/Batch-*/*.mat')):
    batch = f.split('/')[-2]; bid = os.path.basename(f)[:-4]
    m = sio.loadmat(f, simplify_cells=True); d = m['data']; s = m['summary']
    n = len(d); ns = len(s['discharge_capacity_Ah'])
    rows = []
    for i, c in enumerate(d):
        T = np.asarray(c['temperature_C'], float); t = np.asarray(c['relative_time_min'], float)
        r = {'source': 'XJTU (Zenodo 10963339)', 'batch': batch, 'battery_id': bid, 'protocol_code': PROTO[batch][0], 'protocol': PROTO[batch][1],
             'ambient': 'room temperature (uncontrolled)', 'cycle': i + 1, 'cycle_description': str(c['description']).strip(),
             'n_samples': len(t), 'duration_min': float(t[-1] - t[0]) if len(t) else np.nan,
             'temp_mean_C': float(np.nanmean(T)) if len(T) else np.nan, 'temp_max_C': float(np.nanmax(T)) if len(T) else np.nan}
        for k in SUMK: r[k] = float(s[k][i]) if i < ns else np.nan
        rows.append(r)
    df = pd.DataFrame(rows); df.to_csv(f'{OUT}/cycles/{batch}_{bid}.csv', index=False); allrows.append(df)
    raw = []
    for cy in (1, 10, 50, 100):
        if cy <= n:
            c = d[cy - 1]
            raw.append(pd.DataFrame({'cycle': cy, 'system_time': [str(x) for x in c['system_time']], 'relative_time_min': c['relative_time_min'], 'voltage_V': c['voltage_V'],
                                     'current_A': c['current_A'], 'capacity_Ah': c['capacity_Ah'], 'power_Wh': c['power_Wh'], 'temperature_C': c['temperature_C']}))
    pd.concat(raw).to_csv(f'{OUT}/raw_curves/{batch}_{bid}_cycles_1_10_50_100.csv.gz', index=False)
    log.append({'batch': batch, 'battery_id': bid, 'n_cycles_data': n, 'n_cycles_summary': ns, 'cycle_life_field': int(s['cycle_life']), 'description': str(s['description'])})
    print(batch, bid, n, ns, s['cycle_life'], flush=True)
pd.concat(allrows).to_csv(f'{OUT}/all_cycles.csv.gz', index=False)
tc = sio.loadmat(f'{SRC}/Temperature_Compensation_Data.mat', simplify_cells=True)['Temperature_Compensation']
tk = []
for j, e in enumerate(tc):
    if isinstance(e, dict):
        tk.append(pd.DataFrame({k: (np.asarray(v).astype(str) if np.asarray(v).dtype == object else np.asarray(v)) for k, v in e.items() if np.ndim(v) == 1}).assign(entry=j + 1))
        print('tempcomp', j, {k: np.shape(v) for k, v in e.items()})
if tk: pd.concat(tk).to_csv(f'{OUT}/temperature_compensation.csv.gz', index=False)
json.dump(log, open(f'{OUT}/battery_index.json', 'w'), indent=1)
