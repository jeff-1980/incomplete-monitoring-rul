# Provenance of the two input tables of the battery check

| Input of rslib.py | Source | md5 |
|---|---|---|
| `mit.csv.gz` | merged table `all_cycles.csv.gz` of the MIT export (140 cells, 114,738 rows) | 8dd8ed8f268afff2cd541f9294c16c28 |
| `xjtu.csv.gz` | merged table `all_cycles.csv.gz` of the XJTU export (55 cells, 27,642 rows) | 7ba1b6f9d77c8c32dd4e301f8dd22caa |

Steps of the export (done in an earlier step of the project, not repeated for the paper):

1. MIT: download the three batch files (2017-05-12, 2017-06-30, 2018-04-12) from https://data.matr.io/1/ and run `export_severson.py <batch.mat> <batch label> <out>` for each; this writes one table per cell in `<out>/cycles/`. Then `merge_cycles.py <out> mit.csv.gz` concatenates the 140 tables in the lexicographic order of their names. Nothing is normalised, cut or dropped.
2. XJTU: download `Battery Dataset.zip` from https://doi.org/10.5281/zenodo.10963339 (md5 a635cef9678e0de21f9d5c1f78a4342c), unpack, run `export_xjtu.py`; it writes the per-cell tables and the merged table `all_cycles.csv.gz` directly.

What was checked for the paper: the two inputs are byte-identical to the merged tables kept with the export (md5 above); the cells appear in lexicographic order; one XJTU per-cell table (`sample_Batch-3_R2.5_battery-1.csv`) equals its rows in the merged table (`check_definitions.py`).

What was not checked: the original files were not kept, so the export has not been repeated from them and the tables have not been compared with the original files row by row. `merge_cycles.py` documents the merge of the MIT tables as reconstructed from the order of the cells in the merged table; the original merge command was not kept, and byte identity of its output has not been tested.
