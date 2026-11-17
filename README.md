# Code and results: training on deployment-like incomplete monitoring data for RUL prediction

Code, per-engine results and analysis scripts for the manuscript

> Wang Y and Tang Y, "Training on deployment-like incomplete monitoring data for remaining useful life prediction: two case studies with pre-specified protocols", submitted to *Measurement Science and Technology*.

The protocol documents are archived separately: https://doi.org/10.5281/zenodo.24269036.

## Contents

| Folder | What it holds |
|---|---|
| `training/case1/` | Case 1 (sparse and irregular records) on C-MAPSS: shared code `cm.py`, `q3lib.py`; pre-specified run `q3.py`; exploratory baselines `q3b.py`, `q3c.py`; five-seed run with all models trained together `q3d_full.py`; N-CMAPSS confirmation `nq3.py`, `nq3b.py` (19-unit leave-one-unit-out); aggregation scripts used during the study |
| `training/case2/` | Case 2 (short histories): `q6.py`, `q6x.py` (C-MAPSS), `q6n.py`, `q6nx.py` (N-CMAPSS), aggregation scripts |
| `training/twin_grouped/` | N-CMAPSS re-runs with near-duplicate units grouped (16-group leave-one-group-out), used for the main N-CMAPSS results, and `twin_agg.py` |
| `training/ncmapss_prep/` | Download and reduction of N-CMAPSS DS01 and DS02 to cycle-level features (`ncm_cycles.npz`) |
| `control_a8/` | A8 history-span control: protocol (written and checksummed before the run), training script q3e.py, results, analysis (Tables S19-S20) |
| `upgrade1/` | External cohort (N-CMAPSS DS03-DS08, fixed split), missingness mechanisms not seen in training, padding experiment: protocol (checksummed before the runs), ext.py, cmx.py, results, analysis (Tables S21-S25, Figure 6); flight-profile screening (profile_screen.py, profile_groups.json). ext.py needs `ncm_cycles_ds03_08.npz`, produced by `training/ncmapss_prep/fetch_prep_ds03_08.py` from the NASA files |
| `upgrade2/` | Other backbones (TCN, Transformer): protocol (checksummed before the runs), bbm.py, bb_c.py, bb_e.py, selected configurations, results, analysis (Table 6, Tables S26-S27); amendment with selection by flight-profile group on the external cohort (bb_e2.py, analyse_upgrade2b.py; superseded results kept) |
| `training/pcmambasde/` | Wrapper used to train PC-MambaSDE under the case-1 protocol (the model code itself is not redistributed, see below) |
| `data/` | Signed prediction errors per test engine (C-MAPSS) or per unit (N-CMAPSS), for every model, scenario and seed, as JSON; `twin/` holds the 16-group N-CMAPSS runs per seed (`nq3g`, `nq3bg`, `q6ng`, `q6nxg`) and `unit_scores.csv` |
| `analysis/` | Scripts that recompute every table, statistic and figure of the paper and supplement from `data/`; their outputs are included |
| `figures/`, `manuscript/` | Output folders of the figure and supplement scripts |

Internal arm names in the code differ from the paper; the mapping is given in Supplementary Note S1, and Supplementary Note S4 maps seeds, features, twin groups, scripts and result files to the tables (for example GRU-D = `B1_GRUD`, IMP = `B2s_imputer`, SNAP = `B3_static`, PC-MambaSDE = `B4_PCMambaSDE`; case 2: S1 = `A1`, S2 = `A2`, S3 = `B3`, S4 = `B2`, S5 = `B4`, S6 = `A6L`, S8 = `C8`).

## Reproducing the tables and figures (no training needed)

```
pip install -r requirements.txt
python analysis/make_tables.py
python analysis/make_tables_bc.py
python analysis/make_tables_q3d.py
python analysis/make_tables_q6.py
python analysis/round1_checks.py
CMAPSS_DIR=path/to/CMAPSSData python analysis/round3_checks.py
python analysis/make_figures_v8.py
python analysis/revision_v10.py
python control_a8/analyse_q3e.py
python upgrade1/analyse_upgrade1.py
python upgrade2/analyse_upgrade2b.py
python analysis/make_fig1_fig67_v19.py   # Figures 1, 6 and 7 of the final manuscript
python analysis/make_supplementary_v17.py
```

Tested with Python 3.12, NumPy 2.4, SciPy 1.17, scikit-learn 1.8 and Matplotlib 3.10. `round3_checks.py` reads the raw C-MAPSS test files to count padded windows.

## Re-training

1. Download C-MAPSS and N-CMAPSS from the NASA Prognostics Center of Excellence Data Set Repository. Set `CMAPSS_DIR` to the folder with `train_FD00x.txt`, `test_FD00x.txt` and `RUL_FD00x.txt`, and `NCMAPSS_DIR` to the folder with the N-CMAPSS `.h5` files.
2. For N-CMAPSS, run `training/ncmapss_prep/ncm_prep.py` to create `ncm_cycles.npz` in the working directory.
3. Run the training scripts from their folder, for example `python q3d_full.py FD001 0` (subset, seed). Results are written as JSON to `RESULTS_DIR` (default `results/`).

Models were trained with PyTorch 2.11.0 (CUDA 13.0) on an NVIDIA RTX A5000 Laptop GPU (five-seed runs) and on CPU (pre-specified case-1 run). GPU training is not bit-for-bit deterministic across hardware.

## PC-MambaSDE

`training/pcmambasde/q3m.py` trains PC-MambaSDE (reference [20] of the paper) under the case-1 protocol. The model code is the authors' public release and is not included here. In that release two classes share the name `Encoder`, so the class defined last replaces the Mamba encoder described in the paper; we renamed the classes so that the Mamba encoder is used, and changed nothing else. Set `PCMAMBA_DIR` to the patched copy. The model was trained with the same budget as the other arms (batch size 256, 30 epochs), without tuning and without checkpoint selection on test data.

## Licences

Code: MIT licence (`LICENSE`). Result files in `data/`: CC BY 4.0 (`data/LICENSE-DATA.txt`). C-MAPSS and N-CMAPSS are provided by NASA and are not redistributed here.

## Citation

Please cite the paper and this archive: https://doi.org/10.5281/zenodo.24269263.
