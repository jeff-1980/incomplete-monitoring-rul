"""MIT/Stanford/TRI fast-charging dataset (Severson et al. 2019, Nature Energy 4:383; data.matr.io, CC BY 4.0) -> cycle-level tables
in the XJTU export format, one batch .mat at a time. Usage: python3 -I export_severson.py <batch.mat> <batch_label> <out dir>
Nothing normalised, no end-of-life cut, no cycles dropped (cycle 0 placeholder rows of the summary are kept as they are).
Protocol parsed from policy_readable, e.g. '5.4C(40%)-3.6C': CC1 = 5.4C until 40% SOC, then CC2 = 3.6C to 80% SOC, then 1C CC-CV
to 3.6 V; discharge 4C to 2.0 V; chamber 30 degC. Attia 2020 batches use 'CC1-CC2-CC3-CC4' policies; A123 APR18650M1A, LFP/graphite, nominal 1.1 Ah (all from the paper)."""
import sys, os, re, json, h5py, numpy as np, pandas as pd
MAT, LAB, OUT = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(f'{OUT}/cycles', exist_ok=True)
f = h5py.File(MAT, 'r'); b = f['batch']; n = b['summary'].shape[0]
txt = lambda ref: ''.join(chr(int(x)) for x in f[ref][:].flatten() if 0 < int(x) < 0x110000)
index = {}
for i in range(n):
    pol = txt(b['policy_readable'][i, 0]); bid = f'{LAB}_c{i}'
    m = re.match(r'([\d.]+)C\((\d+)%\)-([\d.]+)C', pol); cc = [float(x) for x in re.findall(r'[\d.]+', pol)]
    c1, soc, c2 = (float(m[1]), int(m[2]), float(m[3])) if m else (np.nan, np.nan, np.nan)
    if m: ptxt = (f'charge {c1}C to 80% SOC' if soc == 80 else f'charge {c1}C to {soc}% SOC, {c2}C to 80% SOC') + ', 1C CC-CV to 3.6 V; discharge 4C to 2.0 V'
    elif len(cc) == 4: ptxt = f'charge CC1-CC4 = {cc[0]}/{cc[1]}/{cc[2]}/{cc[3]}C over 0-20/20-40/40-60/60-80% SOC (Attia 2020), then 1C CC-CV to 3.6 V; discharge 4C to 2.0 V'
    else: ptxt = f'policy {pol} (not parsed); 1C CC-CV to 3.6 V; discharge 4C to 2.0 V'
    cc4 = cc if (not m and len(cc) == 4) else [np.nan] * 4
    s = f[b['summary'][i, 0]]; S = {k: s[k][0, :] for k in s}; cy = f[b['cycles'][i, 0]]; nc = cy['I'].shape[0]
    life = float(f[b['cycle_life'][i, 0]][:].flatten()[0]) if f[b['cycle_life'][i, 0]].size else np.nan
    rows = []
    for j in range(len(S['cycle'])):
        r = dict(source='Severson2019_datamatr', batch=LAB, battery_id=bid, chemistry='LFP/graphite (A123 APR18650M1A)', nominal_capacity_Ah=1.1,
                 protocol_code=pol, protocol=ptxt,
                 ambient_C=30, charge_C1=c1, charge_switch_soc_pct=soc, charge_C2=c2, CC1=cc4[0], CC2=cc4[1], CC3=cc4[2], CC4=cc4[3], discharge_rate_C=4.0,
                 cycle=int(S['cycle'][j]), charge_capacity_Ah=S['QCharge'][j], discharge_capacity_Ah=S['QDischarge'][j],
                 internal_resistance_ohm=S['IR'][j], temp_mean_C=S['Tavg'][j], temp_max_C=S['Tmax'][j], temp_min_C=S['Tmin'][j],
                 charge_time_min=S['chargetime'][j])
        if j < nc:
            I = f[cy['I'][j, 0]][:].flatten(); V = f[cy['V'][j, 0]][:].flatten(); t = f[cy['t'][j, 0]][:].flatten() * 60  # t in minutes -> s
            if len(I) > 1:
                dt = np.diff(t, prepend=t[0]); ch, dc = I > 1e-3, I < -1e-3; P = np.abs(V * I * dt) / 3600
                r.update(charge_energy_Wh=P[ch].sum(), discharge_energy_Wh=P[dc].sum(),
                         charge_median_voltage=np.median(V[ch]) if ch.any() else np.nan, discharge_median_voltage=np.median(V[dc]) if dc.any() else np.nan,
                         charge_mean_voltage=V[ch].mean() if ch.any() else np.nan, discharge_mean_voltage=V[dc].mean() if dc.any() else np.nan,
                         n_samples=len(I), duration_min=(t[-1] - t[0]) / 60)
        rows.append(r)
    df = pd.DataFrame(rows); df.to_csv(f'{OUT}/cycles/{bid}.csv', index=False)
    index[bid] = dict(batch=LAB, policy=pol, charge_C1=c1, charge_switch_soc_pct=soc, charge_C2=c2, CC1_4=cc4, cycle_life_official=life,
                      n_summary_cycles=len(df), n_raw_cycles=int(nc), barcode=txt(b['barcode'][i, 0]), channel=txt(b['channel_id'][i, 0]))
    print(bid, pol, len(df), life, flush=True)
json.dump(index, open(f'{OUT}/battery_index_{LAB}.json', 'w'), indent=1)
