"""Merge the per-cell tables written by export_severson.py into one table (the input mit.csv.gz of rslib.py).
Usage: python3 merge_cycles.py <dir with cycles/*.csv of all three batches> <out.csv.gz>
The cells are concatenated in the lexicographic order of their file names (2017-05-12_c0, 2017-05-12_c1, 2017-05-12_c10, ...), rows in file order.
export_xjtu.py writes its merged table (all_cycles.csv.gz, the input xjtu.csv.gz) itself, in the same order."""
import sys, glob, pandas as pd
files = sorted(glob.glob(f'{sys.argv[1]}/cycles/*.csv')); pd.concat([pd.read_csv(f) for f in files]).to_csv(sys.argv[2], index=False); print(len(files), 'cells')
