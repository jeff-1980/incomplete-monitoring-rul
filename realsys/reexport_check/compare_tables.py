"""Row-by-row comparison of a re-exported merged table with the table used in the experiments. Usage: python3 compare_tables.py <new.csv.gz> <used.csv.gz> <id columns, comma separated> <out.md>"""
import sys, gzip, hashlib, numpy as np, pandas as pd
new, used, ids, outp = sys.argv[1], sys.argv[2], sys.argv[3].split(','), sys.argv[4]; out = []
ra, rb = gzip.open(new, 'rb').read(), gzip.open(used, 'rb').read()
out.append(f'Decompressed content: re-export {len(ra)} bytes, md5 {hashlib.md5(ra).hexdigest()}; table used {len(rb)} bytes, md5 {hashlib.md5(rb).hexdigest()}; byte-identical: {ra == rb}.')
a, b = pd.read_csv(new, low_memory=False), pd.read_csv(used, low_memory=False)
out.append(f'Shape: re-export {a.shape}, table used {b.shape}; same columns in the same order: {list(a.columns) == list(b.columns)}.')
if a.shape == b.shape and list(a.columns) == list(b.columns):
    key = (a[ids].astype(str).values == b[ids].astype(str).values).all(); out.append(f'Identifiers and cycle numbers ({", ".join(ids)}) equal in every row: {bool(key)}.')
    worst = []
    for c in a.columns:
        if pd.api.types.is_numeric_dtype(a[c]) and pd.api.types.is_numeric_dtype(b[c]):
            x, y = a[c].to_numpy(float), b[c].to_numpy(float); nan = np.isnan(x) != np.isnan(y); d = np.abs(x - y); d[np.isnan(d)] = 0
            exact = int((x != y).sum() - (np.isnan(x) & np.isnan(y)).sum()); rel = float(np.nanmax(d / np.maximum(np.abs(y), 1e-12))) if len(d) else 0.0
            worst.append((c, int(nan.sum()), exact, float(d.max()), rel))
        else:
            neq = int((a[c].astype(str) != b[c].astype(str)).sum()); worst.append((c, 0, neq, float('nan'), float('nan')))
    out.append(''); out.append('| Column | NaN pattern differs | values not exactly equal | max abs difference | max relative difference |'); out.append('|---|---|---|---|---|')
    for c, n, e, d, r in worst: out.append(f'| {c} | {n} | {e} | {d:.3g} | {r:.3g} |')
    out.append(''); out.append(f'Columns with any value not exactly equal: {sum(1 for w in worst if w[2] > 0)} of {len(worst)}; largest absolute difference over all numeric columns: {max((w[3] for w in worst if w[3] == w[3]), default=0):.3g}.')
open(outp, 'w', encoding='utf-8').write('\n'.join(out) + '\n'); print('\n'.join(out))
