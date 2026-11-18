# Provenance of the two input tables of the battery check

| Input of rslib.py | Source | md5 |
|---|---|---|
| `mit.csv.gz` | merged table `all_cycles.csv.gz` of the MIT export (140 cells, 114,738 rows) | 8dd8ed8f268afff2cd541f9294c16c28 |
| `xjtu.csv.gz` | merged table `all_cycles.csv.gz` of the XJTU export (55 cells, 27,642 rows) | 7ba1b6f9d77c8c32dd4e301f8dd22caa |

Steps of the export (done in an earlier step of the project and repeated from the original files on 2026-11-18, see below):

1. MIT: download the three batch files (2017-05-12, 2017-06-30, 2018-04-12) from https://data.matr.io/1/ and run `export_severson.py <batch.mat> <batch label> <out>` for each; this writes one table per cell in `<out>/cycles/`. Then `merge_cycles.py <out> mit.csv.gz` concatenates the 140 tables in the lexicographic order of their names. Nothing is normalised, cut or dropped.
2. XJTU: download `Battery Dataset.zip` from https://doi.org/10.5281/zenodo.10963339 (md5 a635cef9678e0de21f9d5c1f78a4342c), unpack, run `export_xjtu.py`; it writes the per-cell tables and the merged table `all_cycles.csv.gz` directly.

What was checked for the paper: the two inputs are byte-identical to the merged tables kept with the export (md5 above); the cells appear in lexicographic order; one XJTU per-cell table (`sample_Batch-3_R2.5_battery-1.csv`) equals its rows in the merged table (`check_definitions.py`).

Re-export from the original files (2026-11-18). The four original files were downloaded again (XJTU `Battery Dataset.zip`, 2,438,769,934 bytes, md5 a635cef9678e0de21f9d5c1f78a4342c as given by Zenodo; MIT batch files of 3,025,320,241, 2,007,331,155 and 3,236,690,412 bytes, sizes as given by the server, md5 1d30ad79d3980c2b2c6cb47783ba27eb, f0430a8506ed9e4e326c8579d6be58b4 and a57522980f1bd823c9fe90b142e5b8b7; the MIT host publishes no checksums). `export_xjtu.py` (only the input and output paths changed), `export_severson.py` (unchanged) and `merge_cycles.py` were run on them. The decompressed merged tables are byte-identical to the tables used in the experiments: XJTU 27,642 rows and 20 columns (md5 of the decompressed content 6d0777e79e3b883383bca2b3a60377c2), MIT 114,738 rows and 32 columns (md5 55a8d62c45926644c2845f71287e520d). The .gz files themselves differ because gzip stores a time stamp. `merge_cycles.py`, which had been reconstructed, is thereby confirmed. Reports: `realsys/reexport_check/compare_xjtu.md`, `compare_mit.md`, produced by `compare_tables.py`.

Not covered: the models were not retrained from the re-exported tables (unnecessary, as the tables are identical), and the last step of `export_xjtu.py`, which exports the separate room-temperature record and is not used here, failed on the machine used for the re-export.
