# Supplementary material

## Note S1. Protocols, deviations and naming

Four protocol documents were written during the study: (1) case 1 on C-MAPSS (arms A1–A7, scenarios, hypotheses H1–H5, decision rule), created 03:24 UTC, before the first results at 05:02 UTC; (2) the case-1 N-CMAPSS confirmation, created 03:41 UTC, before any N-CMAPSS model was trained; (3) the N-CMAPSS evaluation of A8 and GRU-D, written two minutes after a first run had been started and then stopped once the results of one fold (one unit, three seeds) had been seen, after which all folds were rerun with the unchanged script; (4) case 2 on C-MAPSS and N-CMAPSS, written before its runs except for one run-through check whose results were not inspected, with an appendix adding S6 and S8 written after the C-MAPSS case-2 results were known, while the N-CMAPSS runs were in progress (per-unit numbers of two folds of one seed had been seen). The documents were archived publicly after the experiments https://doi.org/10.5281/zenodo.24269036; one line referring to the authors' unrelated manuscripts was removed from document 1, and a host name was replaced in document 4.

Deviations. (i) N-CMAPSS twin units: three DS01 units (u2, u5, u10) have DS02 counterparts with identical life and RUL labels and feature correlation of about 0.97; all N-CMAPSS models were retrained with the pairs merged and evaluated by leave-one-group-out validation over 16 groups, which the main text reports; the pre-specified leave-one-unit-out results are in Table S9. (ii) In the case-1 N-CMAPSS confirmation, unit RMSE was saved per seed and averaged over seeds, rather than averaging errors over seeds before computing RMSE. (iii) Pilot studies had used the official C-MAPSS test sets in both cases.

Naming. The paper calls the strategy sparsified-window training (SWT). The protocols, scripts and result files call it deployment-matched training (in places DMWT), and the gap law of the main experiments the deployment or mixed-interval law; these names were not changed after the fact. The code also uses internal arm names that differ from the paper: GRU-D = B1_GRUD; IMP = B2s_imputer; SNAP = B3_static; PC-MambaSDE = B4_PCMambaSDE; in case 2, S1 = A1, S2 = A2, S3 = B3, S4 = B2, S5 = B4, S6 = A6L, S8 = C8. The case-2 models S1 and S6 produce predictions identical to A1 and A6 of the five-seed case-1 run (same code, seeds and hardware; maximum absolute difference 0.0000 cycles).

## Note S2. Baselines that were replaced

GAIN imputer [52]: the regular k = 3 pattern made up 9.9% of its training masks, yet its imputation error on the last 30 cycles of FD001 test engines was 2.55 (k = 3) and 3.19 (k = 5) standardised units, against 0.46 for linear interpolation; with irregular gaps it was comparable to interpolation (0.44). Its training failed under regular missingness. A later code check found that the hint vector was built from two independent random draws, so that about 9% of hint entries took the value 1.5, instead of from one random mask and its complement as in [52]; the failure therefore reflects our implementation and is not evidence about GAIN. It was replaced by the supervised masked imputer IMP (imputation error 0.37). Single-record regression with parametric rectification after [35]: without rectification, FD001 RMSE was 17.0 in every scenario; with our rectification over the last 10 records it was 18.7/22.1/24.6 at k = 1/3/5 (17.3/18.0/19.1 over the last 3), so rectification was dropped and SNAP is reported without it.

## Note S3. Protocol hypotheses and where they are reported

| Protocol | Hypothesis | Status | Where reported |
|---|---|---|---|
| Case 1, C-MAPSS | H1: A5 better than min(A1, A2, A3) at k = 5 and irregular 1–5 | Confirmatory | Section 4.1, Table 3, Table S16 |
| Case 1, C-MAPSS | H2: A5 not significantly worse than A1 at k = 1 | Confirmatory (no-detected-difference rule) | Section 4.2, Table S17 |
| Case 1, C-MAPSS | H3: A5 vs A4 (gap channel) | Secondary, uncorrected | Section 4.2, Table S5 |
| Case 1, C-MAPSS | H4: A5 vs A6 at k = 1 (history length) | Secondary, uncorrected | Section 4.2 |
| Case 1, C-MAPSS | H5: A5 not worse than interval-specific A7 at k = 2–5 | Secondary, uncorrected | Section 4.2 |
| Case 1, N-CMAPSS | H1, H2 as above (two H1 comparisons) | Confirmatory | Sections 4.1–4.2, Tables 3, S9, S16 |
| Case 1, N-CMAPSS (A8, GRU-D) | A8 non-inferior to A5 and better than min(A1, A2, A3); A8 non-inferior to A1 at k = 1; GRU-D as A8 (secondary) | Protocol-guided (written after one fold of a stopped run) | Section 4.4, Table S9 |
| Case 2 | H1: S4 better than min(S1, S2); H2: S4 not worse than S1 with complete history (CI upper bound < 1.0) | Confirmatory | Sections 4.5–4.6, Tables 5, S9, S16, S17 |
| Case 2 | H3: S4 vs S3 (indicator); H4: S4 vs S5 (length-specific models) | Secondary, uncorrected | Section 4.5, Table S11 |
| Case 2, appendix | H1′, H2′ for S8 on N-CMAPSS | Written after the C-MAPSS results | Section 4.6 |
| Case 1, A8 history-span control | C1 A8F vs A6, C2 A8 vs A6S, C3 A6S vs A6, C4 A8F vs A8; reading rule fixed in advance | Exploratory; protocol written and checksummed before the run, after a source-code audit had found the A8 span and padding difference | Section 4.3, Tables S19–S20 |
| Upgrade protocol (external cohort, new missingness, padding) | E1, E2 on DS03–DS08 (confirmatory, fixed split and models); E3 complete-record cost; block and regime-dependent missingness with a reading rule; padding experiment with predicted ordering S3E > S3 > S3L | Protocol, training and analysis scripts written and checksummed before the runs; DS03–DS08 screened on features only beforehand | Sections 4.8–4.10, Tables 6, S21–S25 |
| Backbone protocol | G1 A5 vs best remedy, G2 A8 vs A6, G3 S4 vs better padding, for a TCN and a Transformer; carry-over rule | Protocol and training scripts checksummed before the runs; hyperparameters selected on validation units only | Section 4.11, Table 7, Tables S26–S27 |
| Amendment to the backbone protocol | External-cohort hyperparameter selection repeated with whole profile groups held out; changed arms retrained | Written after the step-2 results were known and before the repeated selection was run (Note S5) | Section 3.1, Tables S26–S27 |
| Real-data protocol | R1 generic deletion vs dense training with one record in 10 cycles, R2 the same under an outage not seen in training, R3 rule for adding complete windows; two battery data sets, five folds over cells | Protocol, training and analysis scripts checksummed before the runs; only the structure of the data was inspected beforehand | Section 4.13, Table 9, Table S33 |
| Step-3 protocol | Q1 generic random deletion (GEN) vs the deployment-like gap law (A8F); Q2 share of complete training windows chosen on validation units; Q3 smoothed dense training (A6M) | Protocol and training scripts checksummed before the runs; analysis script written before the results were inspected | Section 4.12, Table 8, Tables S28–S32. The sparse-record comparisons of Q2 were corrected after an independent check (Holm adjustment; carry-forward A3 included among the remedies), without retraining; the first analysis is kept as Table S30 |

"Added after review" in Table S4 refers to analyses added after the authors' internal simulated reviews during manuscript preparation, not to journal review.

## Note S5. Correction of the validation split used for the other backbones on the external cohort

For the TCN and the Transformer on the external cohort, width and learning rate were first selected on ten development units taken as every fifth unit. Four of them (DS05 u2, DS06 u1, DS06 u6, DS07 u5) share a flight profile with units used for fitting during selection. The final training units and the test units share no profile, so no test information was involved, but the validation scores were optimistic. The selection was therefore repeated with whole profile groups held out (every fifth of the 35 profile groups of the eligible development units; 7 groups, 9 units), following an amendment written before the repetition. The selected configuration changed for A1 and A8 of the TCN and for A1, A6 and S4 of the Transformer; these arms were retrained with seeds 0–4 on the same training windows, and all other arms kept their models. Tables S26 and S27 and all results in the paper are those after the correction. With the original selection the pre-specified readings had been: TCN G1 partly, G2 carries over, G3 partly; Transformer G1 and G2 carry over, G3 partly. After the correction the only change is TCN G2, which became 'partly' because the external-cohort comparison with irregular spacing was no longer significant (Δ −2.70, Holm-adjusted p = 0.08, against −3.38, p = 0.026 before). The superseded result files are kept in the archive.

## Note S4. Reproduction map

- Seeds: 0, 1, 2 for the case-1 pre-specified C-MAPSS run and the case-1 N-CMAPSS runs; 0–4 for the case-1 five-seed run, PC-MambaSDE and case 2. The seed sets the PyTorch initialisation and the random degradation of training windows.
- Test patterns: regular spacing is deterministic; the irregular C-MAPSS gap sequence of test engine u is drawn from a NumPy generator seeded with 1000 + u and is identical for all arms and seeds.
- C-MAPSS inputs: sensors 2, 3, 4, 7, 8, 9, 11, 12, 13, 14, 15, 17, 20 and 21 (numbering of the original data files, in this order); the three operating settings are not model inputs and are used only to assign operating regimes for standardisation (FD002, FD004).
- N-CMAPSS features (32 per flight cycle): within-cycle mean and standard deviation of the 14 measured signals of the X_s block (T24, T30, T48, T50, P15, P2, P21, P24, Ps30, P40, P50, Nf, Nc, Wf) and the means of the four scenario descriptors of the W block (altitude, Mach number, throttle-resolver angle, fan-inlet temperature).
- Twin groups: DS01 u2 with DS02 u2, DS01 u5 with DS02 u5, DS01 u10 with DS02 u10; the other 13 units form one group each (16 groups).
- Scripts and files (repository folders): case-1 C-MAPSS pre-specified run training/case1/q3.py → data/q3_FD00x_s*.json (Tables 3, S1–S6); five-seed run training/case1/q3d_full.py → data/q3d_*.json (Table 4, S7, S8); PC-MambaSDE training/pcmambasde/q3m.py → data/pcm/; case-1 N-CMAPSS training/case1/nq3.py, nq3b.py (19 folds) and training/twin_grouped/nq3g.py, nq3bg.py (16 groups) → data/nq3*_s*.json, data/twin/; case 2 training/case2/q6.py, q6x.py, q6n.py, q6nx.py and training/twin_grouped/q6ng.py, q6nxg.py → data/q6/, data/twin/. Tables and figures: analysis/make_tables*.py, round1_checks.py, round3_checks.py, revision_v10.py (Tables S16–S18), make_figures_v8.py, make_supplementary_v25.py. Other backbones: upgrade2/PROTOCOL_upgrade2.md and PROTOCOL_upgrade2_amendment.md, bbm.py, bb_c.py, bb_e.py, bb_e2.py (seeds 0–4; selected configurations in upgrade2/results/sel_*.json, corrected external-cohort selection in sel_*_ext_g.json, corrected results bbe2_*.json) → upgrade2/results/, analyse_upgrade2b.py (Tables S26–S27). Generic deletion, training mixture and smoothing: upgrade3/PROTOCOL_upgrade3.md, q3g.py (C-MAPSS), extg.py (external cohort; seeds 0–4; selected shares in upgrade3/results/selr_*.json) → upgrade3/results/, analyse_upgrade3.py (Tables S28–S31). Flight-profile screening: upgrade1/profile_screen.py → upgrade1/profile_groups.json. External cohort, new missingness and padding experiment: upgrade1/PROTOCOL_upgrade1.md, ext.py (DS03–DS08; seeds 0–4), cmx.py (C-MAPSS) → upgrade1/results/, analyse_upgrade1.py (Tables S21–S25), analysis/make_fig6.py; DS03–DS08 features from training/ncmapss_prep/fetch_prep_ds03_08.py. Excluded units: training DS03 u5; test DS03 u10, u11, u14, u15 and DS08a u14. Test profile groups: DS05/DS06/DS07 u7, u8, u9 and u10 (three units each); all other test units single. A8 history-span control: control_a8/PROTOCOL_A8_control.md, q3e.py → control_a8/results/q3e_*.json, analyse_q3e.py (Tables S19–S20).
- Shared predictions: the case-2 models S1 and S6 are the case-1 five-seed models A1 and A6 (identical predictions), not additional replicates.


## Table S1. Case 1, pre-specified run: RMSE (cycles), mean ± s.d. over three seeds

| Subset | Scenario | A1 | A2 | A3 | A4 | A5 | A6 | A7 |
|---|---|---|---|---|---|---|---|---|
| FD001 | k = 1 | 16.03 ± 0.17 | 16.03 ± 0.17 | 16.03 ± 0.17 | 17.68 ± 0.92 | 14.88 ± 0.50 | 15.22 ± 0.71 | — |
| FD001 | k = 2 | 20.70 ± 1.59 | 19.69 ± 0.77 | 19.23 ± 0.30 | 14.25 ± 0.46 | 13.98 ± 0.43 | 15.68 ± 0.44 | 14.84 ± 0.22 |
| FD001 | k = 3 | 24.91 ± 2.19 | 18.52 ± 0.58 | 18.68 ± 0.35 | 15.15 ± 0.15 | 14.44 ± 0.40 | 16.96 ± 0.95 | 15.13 ± 0.50 |
| FD001 | k = 5 | 26.50 ± 2.62 | 21.14 ± 0.93 | 21.72 ± 0.88 | 16.25 ± 0.39 | 13.19 ± 0.31 | 18.43 ± 0.77 | 15.22 ± 0.89 |
| FD001 | irr 1–5 | 23.99 ± 2.08 | 20.00 ± 0.64 | 20.30 ± 0.70 | 14.22 ± 0.47 | 13.51 ± 0.34 | 16.61 ± 0.76 | — |
| FD001 | irr 1–10 | 28.21 ± 3.15 | 22.49 ± 0.38 | 26.38 ± 0.22 | 17.69 ± 0.20 | 13.92 ± 0.85 | 18.48 ± 0.94 | — |
| FD002 | k = 1 | 18.18 ± 0.84 | 18.18 ± 0.84 | 18.18 ± 0.84 | 15.79 ± 0.15 | 14.93 ± 0.65 | 15.74 ± 0.80 | — |
| FD002 | k = 2 | 19.18 ± 1.97 | 18.14 ± 0.54 | 18.47 ± 0.37 | 13.22 ± 0.16 | 12.89 ± 0.44 | 18.67 ± 0.93 | 14.81 ± 0.81 |
| FD002 | k = 3 | 19.17 ± 0.65 | 20.22 ± 0.74 | 20.13 ± 0.40 | 13.71 ± 0.40 | 13.41 ± 0.30 | 19.47 ± 1.89 | 15.75 ± 0.36 |
| FD002 | k = 5 | 21.03 ± 1.26 | 22.02 ± 0.20 | 23.13 ± 0.10 | 15.89 ± 0.95 | 13.29 ± 0.21 | 22.67 ± 2.88 | 16.27 ± 1.48 |
| FD002 | irr 1–5 | 19.33 ± 1.09 | 21.14 ± 0.49 | 21.53 ± 0.75 | 14.80 ± 0.30 | 13.43 ± 0.08 | 19.66 ± 1.94 | — |
| FD002 | irr 1–10 | 22.15 ± 1.38 | 22.94 ± 0.40 | 24.23 ± 0.39 | 16.86 ± 0.57 | 13.80 ± 0.12 | 23.12 ± 2.49 | — |
| FD003 | k = 1 | 12.98 ± 0.34 | 12.98 ± 0.34 | 12.98 ± 0.34 | 20.18 ± 2.19 | 14.65 ± 0.27 | 13.27 ± 0.69 | — |
| FD003 | k = 2 | 19.78 ± 0.64 | 15.13 ± 0.59 | 15.30 ± 0.52 | 15.02 ± 1.53 | 12.99 ± 0.27 | 16.26 ± 1.83 | 13.79 ± 0.59 |
| FD003 | k = 3 | 26.95 ± 0.26 | 17.82 ± 0.89 | 18.16 ± 0.77 | 14.36 ± 0.42 | 13.51 ± 0.49 | 15.72 ± 0.51 | 13.74 ± 0.16 |
| FD003 | k = 5 | 35.71 ± 0.95 | 16.64 ± 0.73 | 17.77 ± 1.21 | 17.80 ± 1.03 | 14.00 ± 0.69 | 16.40 ± 0.33 | 14.24 ± 0.34 |
| FD003 | irr 1–5 | 26.92 ± 0.95 | 17.72 ± 0.41 | 19.29 ± 0.83 | 14.08 ± 0.46 | 13.01 ± 0.22 | 17.01 ± 0.71 | — |
| FD003 | irr 1–10 | 35.18 ± 0.55 | 18.06 ± 1.06 | 19.90 ± 1.12 | 16.75 ± 0.89 | 13.42 ± 0.96 | 17.05 ± 0.52 | — |
| FD004 | k = 1 | 16.97 ± 0.46 | 16.97 ± 0.46 | 16.97 ± 0.46 | 18.62 ± 1.07 | 15.35 ± 0.41 | 16.65 ± 1.53 | — |
| FD004 | k = 2 | 20.63 ± 0.40 | 19.93 ± 0.38 | 20.03 ± 0.68 | 15.23 ± 0.57 | 13.67 ± 0.23 | 20.37 ± 0.85 | 16.21 ± 0.88 |
| FD004 | k = 3 | 25.45 ± 0.07 | 21.21 ± 0.42 | 21.03 ± 0.92 | 14.46 ± 0.22 | 13.60 ± 0.35 | 20.91 ± 2.37 | 15.49 ± 0.48 |
| FD004 | k = 5 | 30.64 ± 0.61 | 23.87 ± 1.66 | 24.66 ± 2.25 | 17.82 ± 0.39 | 15.60 ± 0.61 | 23.72 ± 1.66 | 17.37 ± 0.43 |
| FD004 | irr 1–5 | 26.52 ± 0.83 | 21.59 ± 0.66 | 21.96 ± 0.67 | 15.31 ± 0.19 | 14.14 ± 0.38 | 22.12 ± 2.06 | — |
| FD004 | irr 1–10 | 30.24 ± 1.13 | 25.73 ± 0.52 | 27.09 ± 1.43 | 17.85 ± 0.92 | 14.70 ± 1.12 | 23.64 ± 2.24 | — |

A1–A3 share models and coincide at k = 1. PHM 2008 scores (sum over engines, mean over seeds) are in the deposited data.

## Table S2. Case 1, pre-specified run: A5 versus A1 at k = 1 (H2), versus A4 (gap channel) and versus A7 (interval-specific)

Mean paired difference in seed-averaged absolute error per test engine, A5 minus reference (cycles) [95% bootstrap interval]; engines for which A5 was better; two-sided Wilcoxon p (uncorrected except H2 as specified).

| Subset | k = 1 |
|---|---|
| FD001 | -0.14 [-1.37, +1.05]; 51/100; p = 0.83 |
| FD002 | -1.90 [-2.80, -1.02]; 152/259; p = 0.00011 |
| FD003 | +1.34 [+0.37, +2.33]; 44/100; p = 0.023 |
| FD004 | -1.04 [-1.93, -0.18]; 147/248; p = 0.0028 |

## Table S2 (continued). A5 versus A4

Mean paired difference in seed-averaged absolute error per test engine, A5 minus reference (cycles) [95% bootstrap interval]; engines for which A5 was better; two-sided Wilcoxon p (uncorrected except H2 as specified).

| Subset | k = 1 | k = 2 | k = 3 | k = 5 | irr 1–5 | irr 1–10 |
|---|---|---|---|---|---|---|
| FD001 | -1.78 [-3.10, -0.56]; 57/100; p = 0.017 | -0.45 [-1.59, +0.69]; 53/100; p = 0.6 | -0.70 [-1.60, +0.23]; 58/100; p = 0.068 | -2.04 [-3.42, -0.74]; 64/100; p = 0.015 | -0.77 [-1.68, +0.13]; 57/100; p = 0.05 | -2.96 [-4.46, -1.58]; 68/100; p = 2.6e-05 |
| FD002 | -0.95 [-1.77, -0.12]; 148/259; p = 0.024 | -0.54 [-1.11, +0.05]; 150/259; p = 0.01 | -0.07 [-0.55, +0.43]; 137/259; p = 0.27 | -1.42 [-2.29, -0.57]; 139/259; p = 0.039 | -1.04 [-1.63, -0.49]; 146/259; p = 0.00052 | -1.66 [-2.60, -0.71]; 149/259; p = 0.0015 |
| FD003 | -4.07 [-5.97, -2.28]; 60/100; p = 0.0007 | -1.50 [-2.84, -0.24]; 60/100; p = 0.069 | -0.71 [-1.73, +0.26]; 62/100; p = 0.18 | -3.21 [-4.55, -1.93]; 74/100; p = 1.7e-06 | -0.46 [-1.53, +0.53]; 52/100; p = 0.41 | -2.45 [-4.18, -0.79]; 68/100; p = 0.0027 |
| FD004 | -2.50 [-3.61, -1.39]; 157/248; p = 5.2e-06 | -1.31 [-1.97, -0.67]; 148/248; p = 0.00025 | -0.68 [-1.24, -0.11]; 139/248; p = 0.012 | -1.87 [-2.86, -0.91]; 140/248; p = 0.0019 | -0.84 [-1.50, -0.19]; 144/248; p = 0.016 | -2.36 [-3.42, -1.32]; 141/248; p = 0.0008 |

## Table S2 (continued). A5 versus A7

Mean paired difference in seed-averaged absolute error per test engine, A5 minus reference (cycles) [95% bootstrap interval]; engines for which A5 was better; two-sided Wilcoxon p (uncorrected except H2 as specified).

| Subset | k = 2 | k = 3 | k = 5 |
|---|---|---|---|
| FD001 | -0.68 [-1.59, +0.22]; 58/100; p = 0.077 | -0.72 [-1.94, +0.51]; 57/100; p = 0.27 | -1.47 [-2.58, -0.40]; 57/100; p = 0.016 |
| FD002 | -0.77 [-1.50, -0.06]; 120/259; p = 0.51 | -1.13 [-1.80, -0.45]; 142/259; p = 0.0092 | -1.67 [-2.54, -0.83]; 150/259; p = 0.0016 |
| FD003 | -0.10 [-0.80, +0.59]; 48/100; p = 0.96 | +0.11 [-0.64, +0.87]; 47/100; p = 0.57 | +0.26 [-0.71, +1.25]; 52/100; p = 0.8 |
| FD004 | -1.55 [-2.20, -0.91]; 150/248; p = 0.0001 | -1.10 [-1.80, -0.40]; 138/248; p = 0.024 | -1.05 [-1.84, -0.30]; 136/248; p = 0.019 |

## Table S3. Case 1, pre-specified run: A5 versus the long-input dense model A6

Mean paired difference in seed-averaged absolute error per test engine, A5 minus reference (cycles) [95% bootstrap interval]; engines for which A5 was better; two-sided Wilcoxon p (uncorrected except H2 as specified).

| Subset | k = 1 | k = 5 | irr 1–5 |
|---|---|---|---|
| FD001 | +0.21 [-1.71, +2.21]; 46/100; p = 0.76 | -3.32 [-5.07, -1.77]; 61/100; p = 0.00082 | -2.50 [-4.08, -0.87]; 63/100; p = 0.0023 |
| FD002 | +0.31 [-1.03, +1.65]; 117/259; p = 0.29 | -6.40 [-8.01, -4.84]; 168/259; p = 5.5e-13 | -3.94 [-5.29, -2.60]; 158/259; p = 1.3e-07 |
| FD003 | +1.44 [-0.01, +2.92]; 46/100; p = 0.073 | -1.56 [-3.15, +0.09]; 62/100; p = 0.0046 | -2.20 [-3.69, -0.82]; 55/100; p = 0.012 |
| FD004 | -0.56 [-1.90, +0.73]; 109/248; p = 0.78 | -5.73 [-7.29, -4.22]; 166/248; p = 1.5e-12 | -5.45 [-6.97, -3.98]; 163/248; p = 5.7e-12 |

## Table S4. Case 1 sensitivity analyses (added after internal review; see Note S3)

(a) Reference re-selected by RMSE from {A1, A2, A3, A6}; Holm over eight comparisons.

| Subset | Scenario | Reference | RMSE ref | RMSE A5 | Δ | Better | p | p (Holm) |
|---|---|---|---|---|---|---|---|---|
| FD001 | k = 5 | A6 | 18.43 | 13.19 | -3.32 | 61/100 | 0.00082 | 0.0033 |
| FD001 | irr 1–5 | A6 | 16.61 | 13.51 | -2.50 | 63/100 | 0.0023 | 0.0069 |
| FD002 | k = 5 | A1 | 21.03 | 13.29 | -5.65 | 180/259 | 2.8e-14 | 2.2e-13 |
| FD002 | irr 1–5 | A1 | 19.33 | 13.43 | -4.27 | 165/259 | 2.9e-11 | 1.7e-10 |
| FD003 | k = 5 | A6 | 16.40 | 14.00 | -1.56 | 62/100 | 0.0046 | 0.0092 |
| FD003 | irr 1–5 | A6 | 17.01 | 13.01 | -2.20 | 55/100 | 0.012 | 0.012 |
| FD004 | k = 5 | A6 | 23.72 | 15.60 | -5.73 | 166/248 | 1.5e-12 | 1e-11 |
| FD004 | irr 1–5 | A2 | 21.59 | 14.14 | -4.69 | 165/248 | 2.6e-10 | 1.3e-09 |

(b) Pre-specified H1 comparisons tested separately for each seed (Wilcoxon over engines).

| Subset | Scenario | Reference | p, seed 0 | p, seed 1 | p, seed 2 |
|---|---|---|---|---|---|
| FD001 | k = 5 | A2 | 0.00025 | 0.0015 | 0.00075 |
| FD001 | irr 1–5 | A2 | 0.0039 | 0.00073 | 0.23 |
| FD002 | k = 5 | A1 | 2.4e-09 | 4e-12 | 1.8e-07 |
| FD002 | irr 1–5 | A1 | 4.9e-08 | 1.9e-09 | 9.6e-06 |
| FD003 | k = 5 | A2 | 0.0056 | 0.024 | 0.022 |
| FD003 | irr 1–5 | A2 | 0.12 | 0.0024 | 0.022 |
| FD004 | k = 5 | A2 | 9.8e-11 | 3.6e-06 | 8e-08 |
| FD004 | irr 1–5 | A2 | 3.2e-09 | 2.1e-07 | 1.3e-05 |

(c) Out-of-range irregular gaps 1–10: A5 versus the best of A1–A3.

| Subset | Reference | RMSE ref | RMSE A5 | Δ | Better | p |
|---|---|---|---|---|---|---|
| FD001 | A2 | 22.49 | 13.92 | -5.80 | 62/100 | 0.0012 |
| FD002 | A1 | 22.15 | 13.80 | -5.98 | 184/259 | 5.7e-14 |
| FD003 | A2 | 18.06 | 13.42 | -3.52 | 57/100 | 0.03 |
| FD004 | A2 | 25.73 | 14.70 | -7.15 | 166/248 | 2.1e-12 |

## Table S5. Case 1: test-time checks of A5 (earlier post-review run, three seeds)

Gap channel overwritten with 1 at k = 5, and every-cycle data fed to A5 as every third cycle (this second check equals the k = 3 scenario and is shown for completeness). RMSE in cycles; Δ in mean absolute error versus the unmodified A5 of the same run.

| Subset | A5 at k = 5 | A5 with gap channel = 1 | Δ | p | A5 at k = 1 | A5 fed every third cycle | Δ | p |
|---|---|---|---|---|---|---|---|---|
| FD001 | 13.12 | 21.69 | +6.39 | 1.4e-06 | 14.70 | 14.67 | -0.38 | 0.37 |
| FD002 | 13.31 | 21.33 | +5.46 | 5.9e-11 | 14.90 | 13.41 | -1.00 | 0.046 |
| FD003 | 14.66 | 27.89 | +12.51 | 1.3e-11 | 15.18 | 13.82 | -1.18 | 0.06 |
| FD004 | 14.99 | 27.00 | +8.92 | 4e-15 | 14.95 | 13.58 | -1.57 | 6e-05 |

## Table S6. Case 1, pre-specified run: bias and late predictions at k = 5

Mean signed error (positive = remaining life over-estimated), PHM 2008 score per seed and its median, and largest late error per seed (cycles).

| Subset | Arm | Mean signed error | PHM per seed | PHM median | Largest late error per seed |
|---|---|---|---|---|---|
| FD001 | A1 | -12.89 | 2691, 1322, 1038 | 1322 | 41, 40, 42 |
| FD001 | A2 | +6.12 | 1401, 2399, 1299 | 1401 | 56, 63, 55 |
| FD001 | A3 | +5.26 | 1390, 2488, 1225 | 1390 | 52, 61, 49 |
| FD001 | A4 | -3.65 | 416, 387, 428 | 416 | 34, 37, 40 |
| FD001 | A5 | -0.99 | 252, 270, 273 | 270 | 37, 37, 30 |
| FD001 | A6 | +1.93 | 846, 1627, 1093 | 1093 | 49, 69, 65 |
| FD001 | A7 | -0.80 | 378, 368, 367 | 368 | 29, 38, 40 |
| FD002 | A1 | -1.39 | 3653, 4162, 3246 | 3653 | 61, 63, 63 |
| FD002 | A2 | +6.58 | 5761, 9035, 6741 | 6741 | 65, 81, 71 |
| FD002 | A3 | +4.90 | 9592, 18039, 6936 | 9592 | 81, 94, 70 |
| FD002 | A4 | -0.50 | 1381, 1658, 1613 | 1613 | 52, 55, 54 |
| FD002 | A5 | +0.39 | 1019, 766, 908 | 908 | 49, 43, 48 |
| FD002 | A6 | +10.29 | 3556, 9004, 14899 | 9004 | 65, 76, 76 |
| FD002 | A7 | +1.14 | 1570, 1774, 2493 | 1774 | 61, 60, 63 |
| FD003 | A1 | -21.22 | 4401, 4210, 4489 | 4401 | 63, 66, 65 |
| FD003 | A2 | +3.81 | 511, 872, 835 | 835 | 41, 51, 53 |
| FD003 | A3 | +3.95 | 646, 1317, 1256 | 1256 | 53, 59, 61 |
| FD003 | A4 | -1.73 | 977, 1364, 1127 | 1127 | 60, 62, 60 |
| FD003 | A5 | +1.96 | 425, 784, 421 | 425 | 51, 58, 47 |
| FD003 | A6 | +2.20 | 1113, 1363, 911 | 1113 | 65, 67, 62 |
| FD003 | A7 | +2.61 | 396, 685, 764 | 685 | 43, 52, 58 |
| FD004 | A1 | -13.19 | 12613, 11994, 12183 | 12183 | 63, 67, 75 |
| FD004 | A2 | +7.67 | 11803, 19608, 8194 | 11803 | 81, 88, 77 |
| FD004 | A3 | +7.24 | 15545, 53385, 5438 | 15545 | 88, 105, 67 |
| FD004 | A4 | -1.10 | 1868, 2027, 2544 | 2027 | 60, 59, 63 |
| FD004 | A5 | +0.97 | 1532, 1576, 31933 | 1576 | 58, 58, 103 |
| FD004 | A6 | +7.30 | 47667, 22243, 17104 | 22243 | 106, 91, 91 |
| FD004 | A7 | -0.60 | 2015, 2851, 2462 | 2462 | 57, 63, 63 |

## Table S7. Case 1, five-seed run with all models trained together: RMSE (cycles), mean ± s.d. over five seeds

PC-MambaSDE was trained in a separate run with the same seeds, windows and test engines, with the same budget as the other models (batch size 256, 30 epochs, about one twentieth of the gradient steps of the default in the original code) and without tuning or checkpoint selection; the released code was used with one class-name clash corrected so that the Mamba encoder is used, and the elapsed time since the window start (cycles/150) was given as its time input.

| Subset | Scenario | A1 | A2 | A3 | A6 | A5 | A8 | GRU-D | IMP | SNAP | PC-MambaSDE |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FD001 | k = 1 | 16.04 ± 0.39 | 16.04 ± 0.39 | 16.04 ± 0.39 | 15.74 ± 0.82 | 14.71 ± 0.69 | 14.26 ± 1.55 | 14.28 ± 1.08 | 16.04 ± 0.39 | 16.80 ± 0.09 | 20.45 ± 1.48 |
| FD001 | k = 2 | 20.05 ± 0.72 | 19.10 ± 0.34 | 18.70 ± 0.23 | 16.02 ± 1.29 | 14.11 ± 0.19 | 13.14 ± 0.80 | 13.81 ± 0.64 | 19.40 ± 0.98 | 16.80 ± 0.09 | 17.17 ± 1.17 |
| FD001 | k = 3 | 23.44 ± 0.72 | 17.97 ± 0.32 | 18.34 ± 0.21 | 17.19 ± 1.25 | 14.52 ± 0.21 | 13.53 ± 0.65 | 14.46 ± 0.44 | 19.65 ± 0.62 | 16.80 ± 0.09 | 17.45 ± 0.92 |
| FD001 | k = 5 | 24.93 ± 0.91 | 21.07 ± 1.02 | 21.97 ± 0.98 | 18.20 ± 1.03 | 12.67 ± 0.70 | 14.58 ± 0.98 | 13.47 ± 0.50 | 21.01 ± 0.69 | 16.80 ± 0.09 | 17.67 ± 0.78 |
| FD001 | irr 1–5 | 22.87 ± 1.02 | 19.58 ± 0.54 | 20.02 ± 0.74 | 16.58 ± 1.44 | 12.82 ± 0.47 | 12.89 ± 0.46 | 13.28 ± 0.41 | 20.04 ± 0.82 | 16.80 ± 0.09 | 16.76 ± 1.19 |
| FD001 | irr 1–10 | 26.00 ± 0.72 | 22.18 ± 0.86 | 26.10 ± 0.56 | 18.99 ± 0.89 | 13.92 ± 0.38 | 14.87 ± 0.65 | 14.43 ± 1.31 | 22.32 ± 0.68 | 16.80 ± 0.09 | 19.64 ± 1.01 |
| FD002 | k = 1 | 17.50 ± 0.36 | 17.50 ± 0.36 | 17.50 ± 0.36 | 15.66 ± 0.65 | 14.87 ± 0.41 | 12.79 ± 0.97 | 14.72 ± 0.26 | 17.50 ± 0.36 | 17.84 ± 0.17 | 17.97 ± 0.48 |
| FD002 | k = 2 | 18.44 ± 1.02 | 17.94 ± 0.62 | 18.40 ± 0.76 | 17.68 ± 0.43 | 12.76 ± 0.31 | 11.75 ± 0.27 | 12.81 ± 0.16 | 17.23 ± 0.49 | 17.84 ± 0.17 | 15.70 ± 0.67 |
| FD002 | k = 3 | 19.29 ± 0.49 | 20.34 ± 0.46 | 20.63 ± 0.97 | 19.42 ± 0.95 | 13.12 ± 0.57 | 13.13 ± 0.21 | 13.30 ± 0.35 | 18.55 ± 0.53 | 17.84 ± 0.17 | 16.15 ± 0.15 |
| FD002 | k = 5 | 20.69 ± 0.58 | 21.73 ± 0.69 | 22.49 ± 0.42 | 23.33 ± 1.15 | 13.25 ± 0.18 | 13.75 ± 0.51 | 13.35 ± 0.31 | 18.73 ± 0.18 | 17.84 ± 0.17 | 17.13 ± 0.40 |
| FD002 | irr 1–5 | 18.70 ± 0.48 | 20.93 ± 0.90 | 21.40 ± 1.21 | 19.89 ± 0.68 | 13.60 ± 0.38 | 13.40 ± 0.16 | 13.62 ± 0.12 | 19.07 ± 0.65 | 17.84 ± 0.17 | 16.03 ± 0.39 |
| FD002 | irr 1–10 | 21.92 ± 0.77 | 22.29 ± 0.62 | 24.59 ± 0.55 | 23.48 ± 1.00 | 14.13 ± 0.40 | 14.40 ± 0.38 | 15.73 ± 1.86 | 19.60 ± 0.47 | 17.84 ± 0.17 | 18.11 ± 0.26 |
| FD003 | k = 1 | 13.27 ± 0.76 | 13.27 ± 0.76 | 13.27 ± 0.76 | 13.27 ± 0.92 | 14.87 ± 0.58 | 12.10 ± 0.97 | 14.07 ± 0.51 | 13.27 ± 0.76 | 19.96 ± 0.53 | 22.80 ± 1.59 |
| FD003 | k = 2 | 19.98 ± 0.40 | 15.46 ± 0.99 | 15.56 ± 0.87 | 16.56 ± 1.32 | 13.14 ± 0.31 | 13.11 ± 0.92 | 13.31 ± 0.06 | 16.13 ± 1.59 | 19.96 ± 0.53 | 17.15 ± 1.12 |
| FD003 | k = 3 | 26.91 ± 0.73 | 17.59 ± 1.01 | 18.01 ± 0.72 | 15.83 ± 0.65 | 13.66 ± 0.40 | 13.54 ± 0.71 | 14.19 ± 0.06 | 18.41 ± 1.72 | 19.96 ± 0.53 | 16.51 ± 0.78 |
| FD003 | k = 5 | 35.62 ± 1.42 | 16.85 ± 1.22 | 18.00 ± 1.32 | 15.79 ± 0.44 | 14.49 ± 0.51 | 14.80 ± 0.40 | 14.99 ± 0.32 | 20.80 ± 1.45 | 19.96 ± 0.53 | 18.39 ± 0.34 |
| FD003 | irr 1–5 | 26.73 ± 0.79 | 18.20 ± 0.95 | 19.73 ± 0.78 | 17.07 ± 0.88 | 13.35 ± 0.33 | 13.88 ± 0.82 | 13.92 ± 0.11 | 18.88 ± 1.61 | 19.96 ± 0.53 | 15.94 ± 0.90 |
| FD003 | irr 1–10 | 34.91 ± 1.56 | 18.08 ± 0.83 | 19.90 ± 1.15 | 16.80 ± 0.80 | 13.83 ± 0.83 | 14.09 ± 1.03 | 15.66 ± 0.98 | 20.07 ± 1.67 | 19.96 ± 0.53 | 17.94 ± 0.69 |
| FD004 | k = 1 | 17.70 ± 0.70 | 17.70 ± 0.70 | 17.70 ± 0.70 | 16.74 ± 0.86 | 15.49 ± 0.75 | 13.45 ± 0.65 | 15.40 ± 0.93 | 17.70 ± 0.70 | 20.43 ± 0.23 | 19.18 ± 0.71 |
| FD004 | k = 2 | 20.41 ± 0.66 | 20.21 ± 0.90 | 20.38 ± 0.83 | 18.91 ± 1.24 | 13.93 ± 0.34 | 13.31 ± 0.64 | 14.31 ± 0.94 | 19.97 ± 0.59 | 20.43 ± 0.23 | 16.87 ± 0.36 |
| FD004 | k = 3 | 24.22 ± 1.54 | 21.39 ± 0.95 | 21.06 ± 0.76 | 19.94 ± 1.43 | 13.62 ± 0.19 | 13.46 ± 0.74 | 13.84 ± 0.39 | 20.87 ± 0.43 | 20.43 ± 0.23 | 16.25 ± 0.65 |
| FD004 | k = 5 | 29.37 ± 2.47 | 24.11 ± 0.68 | 23.94 ± 0.82 | 22.83 ± 1.29 | 15.09 ± 0.35 | 16.38 ± 0.48 | 15.25 ± 0.44 | 23.05 ± 0.73 | 20.43 ± 0.23 | 18.61 ± 0.31 |
| FD004 | irr 1–5 | 25.45 ± 1.22 | 21.19 ± 0.65 | 21.73 ± 0.28 | 21.12 ± 1.59 | 14.33 ± 0.22 | 14.40 ± 0.61 | 14.34 ± 1.00 | 21.17 ± 0.77 | 20.43 ± 0.23 | 17.14 ± 0.77 |
| FD004 | irr 1–10 | 28.92 ± 1.86 | 25.19 ± 1.02 | 25.96 ± 1.21 | 21.79 ± 2.51 | 14.29 ± 0.24 | 15.74 ± 0.92 | 15.92 ± 1.64 | 23.82 ± 0.55 | 20.43 ± 0.23 | 19.02 ± 0.73 |

## Table S8. Case 1, five-seed run: paired comparisons

Δ mean absolute error, first model minus second (cycles) [95% bootstrap interval]; engines for which the first model was better; two-sided Wilcoxon p (uncorrected).

**A8 versus A6**

| Subset | k = 1 | k = 2 | k = 3 | k = 5 | irr 1–5 | irr 1–10 |
|---|---|---|---|---|---|---|
| FD001 | -0.67 [-2.39, +1.03]; 50/100; 0.75 | -2.05 [-3.44, -0.73]; 61/100; 0.0041 | -2.42 [-3.99, -0.96]; 67/100; 0.0014 | -2.42 [-4.03, -0.94]; 58/100; 0.0078 | -2.49 [-3.85, -1.20]; 66/100; 0.00012 | -3.18 [-4.82, -1.51]; 64/100; 0.00039 |
| FD002 | -0.75 [-1.90, +0.38]; 125/259; 0.75 | -2.95 [-4.19, -1.74]; 148/259; 0.00035 | -3.29 [-4.50, -2.15]; 157/259; 3.1e-05 | -6.58 [-8.04, -5.17]; 185/259; 1.9e-17 | -3.93 [-5.18, -2.74]; 165/259; 2.2e-09 | -6.12 [-7.56, -4.74]; 183/259; 4.4e-15 |
| FD003 | -0.69 [-1.88, +0.46]; 54/100; 0.39 | -1.91 [-3.59, -0.44]; 52/100; 0.13 | -1.32 [-2.70, +0.02]; 59/100; 0.1 | -1.17 [-2.50, +0.21]; 61/100; 0.0082 | -2.12 [-3.64, -0.70]; 60/100; 0.01 | -1.95 [-3.45, -0.49]; 65/100; 0.0024 |
| FD004 | -1.74 [-2.82, -0.70]; 135/248; 0.0022 | -3.54 [-4.64, -2.43]; 147/248; 1.8e-08 | -4.38 [-5.56, -3.26]; 171/248; 3.8e-13 | -4.41 [-5.71, -3.15]; 164/248; 1.4e-11 | -4.59 [-5.81, -3.42]; 162/248; 2.6e-12 | -4.53 [-5.69, -3.42]; 164/248; 1.4e-12 |

**A8 versus A1**

| Subset | k = 1 | k = 2 | k = 3 | k = 5 | irr 1–5 | irr 1–10 |
|---|---|---|---|---|---|---|
| FD001 | -0.93 [-3.22, +1.22]; 54/100; 0.62 | -5.17 [-6.85, -3.58]; 73/100; 3e-07 | -7.90 [-10.08, -5.81]; 77/100; 4.9e-10 | -8.38 [-11.00, -5.92]; 73/100; 1.2e-08 | -7.49 [-9.91, -5.16]; 72/100; 9.7e-08 | -8.53 [-11.34, -5.97]; 72/100; 2.5e-08 |
| FD002 | -2.58 [-3.69, -1.53]; 156/259; 2.8e-05 | -4.47 [-5.55, -3.46]; 180/259; 5.8e-15 | -4.34 [-5.49, -3.22]; 177/259; 2.1e-12 | -4.90 [-6.12, -3.69]; 172/259; 7.9e-13 | -3.65 [-4.73, -2.62]; 173/259; 7.2e-11 | -5.33 [-6.66, -4.04]; 176/259; 3.4e-13 |
| FD003 | -0.66 [-2.02, +0.65]; 60/100; 0.21 | -6.61 [-8.83, -4.43]; 73/100; 4e-08 | -12.55 [-15.61, -9.59]; 83/100; 4.4e-12 | -20.00 [-23.78, -16.31]; 89/100; 4.9e-15 | -12.03 [-15.18, -8.99]; 79/100; 5.5e-11 | -19.08 [-23.11, -15.12]; 84/100; 1.2e-13 |
| FD004 | -2.89 [-3.90, -1.86]; 162/248; 3.2e-08 | -5.18 [-6.45, -3.95]; 184/248; 2.6e-16 | -8.38 [-10.12, -6.71]; 180/248; 5e-19 | -10.20 [-12.42, -8.01]; 180/248; 3.7e-17 | -8.63 [-10.55, -6.76]; 176/248; 1.6e-15 | -10.46 [-12.62, -8.39]; 186/248; 1.2e-20 |

**A8 versus A5**

| Subset | k = 1 | k = 2 | k = 3 | k = 5 | irr 1–5 | irr 1–10 |
|---|---|---|---|---|---|---|
| FD001 | -0.55 [-2.78, +1.64]; 54/100; 0.7 | -0.66 [-1.73, +0.34]; 56/100; 0.17 | -0.72 [-1.42, -0.03]; 59/100; 0.05 | +1.16 [+0.26, +2.12]; 48/100; 0.081 | +0.17 [-0.55, +0.88]; 51/100; 0.87 | +0.19 [-1.02, +1.52]; 49/100; 0.79 |
| FD002 | -1.24 [-2.12, -0.37]; 138/259; 0.029 | -0.47 [-1.02, +0.05]; 139/259; 0.35 | +0.09 [-0.38, +0.54]; 125/259; 0.6 | +0.30 [-0.28, +0.89]; 131/259; 0.42 | +0.23 [-0.33, +0.79]; 112/259; 0.08 | +0.07 [-0.59, +0.73]; 127/259; 0.93 |
| FD003 | -2.32 [-3.64, -1.05]; 73/100; 0.00012 | -0.26 [-0.91, +0.43]; 60/100; 0.05 | -0.07 [-0.71, +0.57]; 47/100; 0.92 | +0.31 [-0.73, +1.30]; 43/100; 0.16 | +0.33 [-0.37, +1.05]; 46/100; 0.48 | +0.18 [-0.83, +1.20]; 48/100; 0.62 |
| FD004 | -1.72 [-2.62, -0.82]; 149/248; 0.00024 | -0.52 [-1.13, +0.08]; 149/248; 0.0046 | -0.29 [-0.72, +0.13]; 140/248; 0.12 | +0.46 [-0.19, +1.15]; 132/248; 0.79 | -0.18 [-0.64, +0.28]; 148/248; 0.059 | +0.42 [-0.31, +1.16]; 132/248; 0.67 |

**GRU-D versus A5**

| Subset | k = 1 | k = 2 | k = 3 | k = 5 | irr 1–5 | irr 1–10 |
|---|---|---|---|---|---|---|
| FD001 | -0.49 [-1.20, +0.25]; 59/100; 0.053 | -0.15 [-0.61, +0.27]; 50/100; 0.93 | +0.11 [-0.38, +0.60]; 40/100; 0.21 | +0.54 [-0.01, +1.12]; 46/100; 0.16 | +0.33 [-0.17, +0.86]; 45/100; 0.27 | +0.09 [-1.00, +1.21]; 54/100; 0.7 |
| FD002 | -0.21 [-0.62, +0.20]; 128/259; 0.38 | +0.09 [-0.22, +0.39]; 119/259; 0.61 | +0.14 [-0.20, +0.48]; 127/259; 0.38 | +0.15 [-0.22, +0.50]; 114/259; 0.21 | +0.19 [-0.10, +0.49]; 118/259; 0.11 | +1.61 [+0.95, +2.26]; 100/259; 1.2e-06 |
| FD003 | -0.56 [-1.10, -0.03]; 58/100; 0.034 | +0.07 [-0.37, +0.50]; 47/100; 0.64 | +0.62 [+0.17, +1.08]; 34/100; 0.0014 | +0.51 [+0.09, +0.92]; 43/100; 0.045 | +0.50 [+0.02, +0.99]; 41/100; 0.044 | +1.54 [+0.72, +2.39]; 30/100; 0.00013 |
| FD004 | -0.06 [-0.43, +0.31]; 131/248; 0.74 | +0.10 [-0.20, +0.41]; 133/248; 0.77 | +0.05 [-0.24, +0.35]; 118/248; 0.51 | +0.00 [-0.32, +0.33]; 120/248; 0.88 | -0.09 [-0.41, +0.23]; 143/248; 0.1 | +1.48 [+0.84, +2.12]; 94/248; 1.3e-05 |

**IMP versus A5**

| Subset | k = 1 | k = 2 | k = 3 | k = 5 | irr 1–5 | irr 1–10 |
|---|---|---|---|---|---|---|
| FD001 | +0.38 [-0.90, +1.71]; 50/100; 0.93 | +4.02 [+1.99, +6.11]; 36/100; 0.00013 | +3.16 [+0.44, +5.90]; 39/100; 0.018 | +6.46 [+3.57, +9.38]; 30/100; 1.1e-05 | +5.21 [+2.55, +7.93]; 32/100; 0.00029 | +5.55 [+2.93, +8.35]; 38/100; 0.0006 |
| FD002 | +1.33 [+0.56, +2.10]; 107/259; 0.00058 | +2.58 [+1.41, +3.77]; 104/259; 0.00022 | +3.08 [+1.82, +4.39]; 105/259; 1.7e-05 | +3.32 [+1.92, +4.72]; 102/259; 9.4e-06 | +3.47 [+2.09, +4.87]; 93/259; 6.2e-07 | +3.24 [+1.79, +4.77]; 108/259; 0.00046 |
| FD003 | -1.66 [-2.53, -0.84]; 61/100; 0.00031 | +2.04 [+0.56, +3.57]; 45/100; 0.014 | +3.64 [+1.70, +5.63]; 35/100; 0.00015 | +4.23 [+1.84, +6.78]; 37/100; 0.0019 | +3.76 [+1.75, +5.98]; 32/100; 0.00035 | +4.22 [+2.26, +6.36]; 35/100; 0.00023 |
| FD004 | +1.17 [+0.39, +1.97]; 105/248; 0.0031 | +3.70 [+2.47, +5.00]; 99/248; 1.6e-07 | +4.36 [+2.91, +5.94]; 103/248; 1.2e-06 | +4.79 [+3.08, +6.53]; 93/248; 5.3e-07 | +3.83 [+2.33, +5.42]; 101/248; 3e-06 | +5.46 [+3.70, +7.34]; 96/248; 2.9e-08 |

**SNAP versus A5**

| Subset | k = 1 | k = 2 | k = 3 | k = 5 | irr 1–5 | irr 1–10 |
|---|---|---|---|---|---|---|
| FD001 | +0.97 [-0.77, +2.73]; 44/100; 0.38 | +1.86 [-0.19, +3.97]; 45/100; 0.21 | +1.46 [-0.88, +3.80]; 41/100; 0.27 | +3.06 [+0.71, +5.56]; 42/100; 0.025 | +2.66 [+0.40, +4.99]; 41/100; 0.06 | +1.57 [-0.46, +3.70]; 49/100; 0.65 |
| FD002 | +2.34 [+1.17, +3.58]; 108/259; 0.00056 | +4.03 [+2.61, +5.50]; 90/259; 2.7e-08 | +3.72 [+2.39, +5.11]; 93/259; 3.3e-07 | +3.76 [+2.36, +5.20]; 96/259; 2e-07 | +3.77 [+2.38, +5.22]; 98/259; 1.3e-07 | +3.03 [+1.58, +4.53]; 98/259; 4.2e-05 |
| FD003 | +3.65 [+1.48, +5.91]; 38/100; 0.0084 | +5.23 [+2.75, +7.93]; 37/100; 0.00064 | +4.88 [+2.36, +7.56]; 39/100; 0.0071 | +4.72 [+2.25, +7.37]; 36/100; 0.0025 | +4.97 [+2.57, +7.53]; 36/100; 0.0012 | +4.92 [+2.67, +7.34]; 36/100; 0.00034 |
| FD004 | +4.23 [+2.94, +5.56]; 82/248; 1.9e-09 | +5.77 [+4.32, +7.24]; 67/248; 4.7e-15 | +6.06 [+4.60, +7.56]; 70/248; 1e-14 | +4.71 [+3.23, +6.22]; 86/248; 4.3e-09 | +5.42 [+3.93, +6.92]; 73/248; 2e-13 | +5.30 [+3.86, +6.77]; 79/248; 1.2e-11 |

**A6 versus A5**

| Subset | k = 1 | k = 2 | k = 3 | k = 5 | irr 1–5 | irr 1–10 |
|---|---|---|---|---|---|---|
| FD001 | +0.12 [-1.97, +2.12]; 52/100; 0.98 | +1.39 [-0.24, +3.01]; 47/100; 0.066 | +1.70 [+0.08, +3.41]; 43/100; 0.12 | +3.58 [+2.13, +5.22]; 39/100; 7.3e-05 | +2.66 [+1.16, +4.16]; 42/100; 0.0006 | +3.37 [+1.72, +5.06]; 40/100; 0.0015 |
| FD002 | -0.49 [-1.71, +0.77]; 139/259; 0.26 | +2.47 [+1.18, +3.77]; 115/259; 0.0047 | +3.38 [+2.20, +4.63]; 115/259; 2e-05 | +6.89 [+5.43, +8.42]; 79/259; 2.5e-17 | +4.16 [+2.97, +5.39]; 98/259; 4.5e-10 | +6.19 [+4.64, +7.80]; 84/259; 7e-13 |
| FD003 | -1.62 [-3.05, -0.21]; 67/100; 0.0041 | +1.65 [+0.19, +3.27]; 48/100; 0.35 | +1.25 [-0.06, +2.62]; 44/100; 0.091 | +1.48 [+0.01, +2.86]; 43/100; 0.0075 | +2.45 [+1.08, +3.93]; 44/100; 0.015 | +2.13 [+0.41, +3.75]; 39/100; 0.0036 |
| FD004 | +0.02 [-1.12, +1.23]; 135/248; 0.18 | +3.02 [+1.77, +4.30]; 106/248; 3.2e-05 | +4.09 [+2.91, +5.34]; 84/248; 3.7e-11 | +4.87 [+3.56, +6.18]; 85/248; 1.7e-12 | +4.41 [+3.19, +5.69]; 91/248; 8.5e-10 | +4.95 [+3.78, +6.17]; 86/248; 1.1e-12 |

**PC-MambaSDE versus A5**

| Subset | k = 1 | k = 2 | k = 3 | k = 5 | irr 1–5 | irr 1–10 |
|---|---|---|---|---|---|---|
| FD001 | +5.26 [+3.51, +7.00]; 31/100; 9e-07 | +3.19 [+1.88, +4.51]; 32/100; 1.4e-05 | +2.85 [+1.65, +4.04]; 32/100; 1.8e-05 | +5.12 [+3.74, +6.58]; 19/100; 6.1e-10 | +3.88 [+2.81, +4.95]; 23/100; 3.8e-09 | +5.46 [+3.92, +7.07]; 19/100; 1.1e-09 |
| FD002 | +2.77 [+2.01, +3.55]; 76/259; 3.6e-13 | +2.44 [+1.71, +3.17]; 74/259; 1.1e-11 | +2.33 [+1.63, +3.02]; 74/259; 1.5e-12 | +2.82 [+1.96, +3.69]; 88/259; 9.7e-10 | +2.22 [+1.49, +2.93]; 74/259; 1.8e-11 | +2.81 [+1.88, +3.79]; 85/259; 3.7e-08 |
| FD003 | +6.79 [+4.50, +9.19]; 30/100; 2.4e-07 | +3.55 [+2.07, +5.14]; 31/100; 4.2e-05 | +2.60 [+1.33, +3.97]; 32/100; 8.9e-05 | +4.11 [+2.68, +5.63]; 21/100; 1.3e-08 | +2.26 [+1.00, +3.56]; 36/100; 0.001 | +3.90 [+2.33, +5.51]; 22/100; 1.4e-07 |
| FD004 | +3.24 [+2.27, +4.27]; 78/248; 6.9e-11 | +2.40 [+1.63, +3.16]; 87/248; 1.3e-09 | +2.31 [+1.62, +3.03]; 73/248; 1.7e-10 | +2.81 [+1.95, +3.74]; 92/248; 2.4e-08 | +2.25 [+1.48, +3.02]; 86/248; 2.8e-09 | +3.75 [+2.72, +4.84]; 78/248; 1e-11 |

**PC-MambaSDE versus A8**

| Subset | k = 1 | k = 2 | k = 3 | k = 5 | irr 1–5 | irr 1–10 |
|---|---|---|---|---|---|---|
| FD001 | +5.81 [+2.90, +8.68]; 35/100; 0.0004 | +3.85 [+2.27, +5.46]; 31/100; 8.3e-06 | +3.56 [+2.41, +4.75]; 32/100; 3.2e-07 | +3.96 [+2.36, +5.60]; 27/100; 1.1e-06 | +3.70 [+2.55, +4.88]; 27/100; 4.2e-08 | +5.27 [+3.52, +7.03]; 25/100; 1.4e-07 |
| FD002 | +4.01 [+2.92, +5.17]; 77/259; 1.1e-12 | +2.91 [+2.13, +3.67]; 78/259; 2e-13 | +2.24 [+1.55, +2.93]; 85/259; 2.7e-10 | +2.52 [+1.67, +3.37]; 86/259; 7.5e-09 | +1.98 [+1.19, +2.79]; 93/259; 9.7e-08 | +2.74 [+1.85, +3.66]; 90/259; 6.1e-09 |
| FD003 | +9.11 [+6.67, +11.64]; 20/100; 1.6e-10 | +3.82 [+2.45, +5.24]; 34/100; 8.8e-07 | +2.67 [+1.48, +3.93]; 30/100; 2e-05 | +3.79 [+2.29, +5.41]; 28/100; 7.5e-07 | +1.92 [+0.76, +3.15]; 36/100; 0.0012 | +3.72 [+2.11, +5.38]; 26/100; 4.2e-07 |
| FD004 | +4.95 [+3.61, +6.36]; 78/248; 3.8e-12 | +2.91 [+1.98, +3.88]; 78/248; 2.6e-10 | +2.60 [+1.78, +3.43]; 73/248; 7e-12 | +2.36 [+1.30, +3.41]; 87/248; 6e-07 | +2.43 [+1.56, +3.32]; 71/248; 2.2e-10 | +3.34 [+2.34, +4.39]; 71/248; 3.3e-11 |

**PC-MambaSDE versus GRU-D**

| Subset | k = 1 | k = 2 | k = 3 | k = 5 | irr 1–5 | irr 1–10 |
|---|---|---|---|---|---|---|
| FD001 | +5.75 [+3.80, +7.67]; 28/100; 2.2e-07 | +3.34 [+2.07, +4.64]; 32/100; 6.1e-06 | +2.74 [+1.68, +3.81]; 30/100; 5e-06 | +4.58 [+3.10, +6.07]; 18/100; 5.7e-08 | +3.54 [+2.51, +4.57]; 22/100; 3e-09 | +5.37 [+3.61, +7.09]; 23/100; 1.3e-07 |
| FD002 | +2.98 [+2.18, +3.80]; 70/259; 8e-14 | +2.35 [+1.60, +3.12]; 80/259; 3.7e-10 | +2.19 [+1.47, +2.91]; 88/259; 7.4e-10 | +2.68 [+1.79, +3.56]; 87/259; 3.3e-08 | +2.02 [+1.26, +2.78]; 89/259; 9e-09 | +1.21 [+0.01, +2.41]; 113/259; 0.08 |
| FD003 | +7.36 [+4.98, +9.86]; 24/100; 2.8e-08 | +3.49 [+2.03, +5.02]; 33/100; 4.1e-05 | +1.98 [+0.72, +3.34]; 34/100; 0.0039 | +3.60 [+2.18, +5.08]; 24/100; 3.1e-07 | +1.76 [+0.51, +3.04]; 40/100; 0.012 | +2.36 [+0.64, +4.08]; 38/100; 0.005 |
| FD004 | +3.30 [+2.31, +4.33]; 68/248; 2e-11 | +2.29 [+1.52, +3.06]; 87/248; 4e-09 | +2.26 [+1.55, +2.98]; 85/248; 3.5e-09 | +2.81 [+1.93, +3.75]; 89/248; 1.1e-08 | +2.34 [+1.53, +3.15]; 80/248; 1.8e-09 | +2.28 [+1.26, +3.35]; 110/248; 0.00036 |

**PC-MambaSDE versus A2**

| Subset | k = 1 | k = 2 | k = 3 | k = 5 | irr 1–5 | irr 1–10 |
|---|---|---|---|---|---|---|
| FD001 | +4.88 [+2.68, +7.01]; 30/100; 3.3e-05 | -0.52 [-2.34, +1.29]; 44/100; 0.86 | +0.20 [-1.79, +2.15]; 43/100; 0.48 | -0.88 [-3.44, +1.61]; 47/100; 0.49 | -0.81 [-3.41, +1.73]; 39/100; 0.5 | +0.07 [-2.96, +3.00]; 38/100; 0.26 |
| FD002 | +1.43 [+0.47, +2.43]; 101/259; 0.00096 | -0.79 [-1.97, +0.33]; 121/259; 0.73 | -1.98 [-3.26, -0.72]; 136/259; 0.019 | -2.70 [-4.33, -1.16]; 141/259; 0.012 | -3.11 [-4.51, -1.73]; 153/259; 5.9e-05 | -2.11 [-3.60, -0.66]; 142/259; 0.043 |
| FD003 | +8.45 [+5.91, +11.18]; 23/100; 1.7e-09 | +2.02 [+0.33, +3.81]; 39/100; 0.012 | -0.20 [-2.23, +1.92]; 41/100; 0.43 | +1.66 [-0.49, +3.82]; 38/100; 0.029 | -0.86 [-3.35, +1.44]; 50/100; 0.71 | +0.40 [-2.07, +2.91]; 42/100; 0.31 |
| FD004 | +2.07 [+0.81, +3.32]; 92/248; 4.3e-05 | -1.77 [-3.05, -0.52]; 131/248; 0.067 | -2.70 [-4.29, -1.18]; 130/248; 0.014 | -3.20 [-4.88, -1.53]; 139/248; 0.0013 | -2.02 [-3.61, -0.50]; 130/248; 0.075 | -2.98 [-4.92, -1.12]; 131/248; 0.071 |

**Bias, PHM median and largest late error (five-seed run; k = 1 / k = 5 / irr 1–5)**

| Subset | Arm | Mean signed error | PHM median | Largest late error |
|---|---|---|---|---|
| FD001 | A1 | +2.2 / -11.7 / -12.1 | 609 / 1298 / 816 | 55 / 41 / 37 |
| FD001 | A2 | +2.2 / +6.2 / +8.1 | 609 / 1764 / 1542 | 55 / 65 / 67 |
| FD001 | A6 | +1.4 / +1.2 / +2.2 | 454 / 928 / 463 | 48 / 64 / 45 |
| FD001 | A5 | +4.6 / -0.1 / -0.9 | 433 / 263 / 234 | 49 / 37 / 39 |
| FD001 | A8 | -5.4 / -1.0 / -0.6 | 229 / 335 / 233 | 28 / 32 / 36 |
| FD001 | GRU-D | +2.6 / -1.0 / -0.4 | 322 / 289 / 253 | 45 / 38 / 40 |
| FD001 | PC-MambaSDE | +8.0 / +2.4 / +1.5 | 1164 / 538 / 510 | 59 / 43 / 51 |
| FD002 | A1 | -0.1 / -0.6 / -3.3 | 2363 / 3734 / 2653 | 67 / 64 / 66 |
| FD002 | A2 | -0.1 / +6.1 / +4.9 | 2363 / 6871 / 4949 | 67 / 94 / 70 |
| FD002 | A6 | +0.7 / +10.3 / +6.8 | 1551 / 9801 / 4581 | 58 / 91 / 66 |
| FD002 | A5 | +0.7 / +1.1 / +1.0 | 1036 / 937 / 1017 | 58 / 51 / 56 |
| FD002 | A8 | -3.7 / +1.9 / +0.7 | 596 / 1045 / 886 | 46 / 58 / 47 |
| FD002 | GRU-D | +0.4 / +1.6 / +0.8 | 1028 / 996 / 993 | 59 / 53 / 53 |
| FD002 | PC-MambaSDE | +2.5 / +2.1 / +0.1 | 2302 / 1792 / 1386 | 72 / 59 / 67 |
| FD003 | A1 | +3.6 / -20.1 / -14.3 | 458 / 4366 / 1534 | 61 / 69 / 67 |
| FD003 | A2 | +3.6 / +4.8 / +6.5 | 458 / 889 / 2116 | 61 / 60 / 72 |
| FD003 | A6 | +3.1 / +1.7 / +4.3 | 404 / 920 / 976 | 43 / 70 / 61 |
| FD003 | A5 | +7.1 / +3.1 / +3.9 | 533 / 676 / 420 | 53 / 57 / 53 |
| FD003 | A8 | +1.8 / +3.4 / +4.2 | 297 / 766 / 424 | 54 / 59 / 60 |
| FD003 | GRU-D | +5.8 / +2.6 / +3.5 | 477 / 716 / 443 | 54 / 58 / 52 |
| FD003 | PC-MambaSDE | +12.7 / +4.6 / +5.7 | 2700 / 1333 / 731 | 69 / 66 / 62 |
| FD004 | A1 | +1.4 / -12.1 / -12.2 | 2033 / 9823 / 4841 | 85 / 78 / 78 |
| FD004 | A2 | +1.4 / +7.8 / +6.6 | 2033 / 33814 / 29784 | 85 / 111 / 107 |
| FD004 | A6 | +0.7 / +5.0 / +4.7 | 1798 / 17982 / 5615 | 67 / 104 / 84 |
| FD004 | A5 | +2.8 / +1.1 / +1.7 | 1398 / 1342 / 1202 | 63 / 61 / 65 |
| FD004 | A8 | -3.0 / +2.7 / +1.7 | 790 / 2953 / 1427 | 51 / 77 / 62 |
| FD004 | GRU-D | +2.4 / +1.5 / +1.7 | 1519 / 1284 / 1060 | 87 / 65 / 93 |
| FD004 | PC-MambaSDE | +5.4 / +2.0 / +1.3 | 3344 / 2336 / 1449 | 76 / 62 / 53 |

## Table S9. N-CMAPSS: all confirmatory tests under the pre-specified (leave-one-unit-out, 19 units) and twin-grouped (leave-one-group-out, 16 groups) schemes

Mean RMSE over units (seed-averaged); Δ = first minus second arm in unit (19) or group (16) RMSE [95% bootstrap interval]; better = units or groups where the first arm was better; Holm within each pair of comparisons where specified. The main text uses the grouped scheme at the group level.

| Evaluation | Scenario | Comparison | Scheme | Mean RMSE (first / second) | Δ [95% CI] | Better | p | p (Holm) |
|---|---|---|---|---|---|---|---|---|
| Case 1, A5 | k = 5 | A5 vs A2 | unit-out (19) | 7.71 / 10.39 | -2.69 [-4.52, -0.81] | 15/19 | 0.016 | 0.032 |
| Case 1, A5 | irr 1–5 | A5 vs A2 | unit-out (19) | 7.65 / 9.86 | -2.21 [-3.95, -0.53] | 13/19 | 0.032 | 0.032 |
| Case 1, A5 | k = 1 | A5 vs A1 | unit-out (19) | 7.58 / 7.76 | -0.18 [-1.04, +0.68] | 9/19 | 0.83 | — |
| Case 1, A5 | k = 5 | A5 vs A2 | grouped (16) | 7.88 / 10.34 | -2.61 [-4.53, -0.59] | 11/16 | 0.034 | 0.067 |
| Case 1, A5 | irr 1–5 | A5 vs A2 | grouped (16) | 7.96 / 9.87 | -2.00 [-3.68, -0.33] | 12/16 | 0.051 | 0.067 |
| Case 1, A5 | k = 1 | A5 vs A1 | grouped (16) | 7.74 / 8.09 | -0.38 [-1.31, +0.54] | 9/16 | 0.53 | — |
| Case 1, A8 | k = 5 | A8 vs A2 | unit-out (19) | 7.97 / 10.39 | -2.42 [-3.98, -0.75] | 17/19 | 0.0053 | 0.011 |
| Case 1, A8 | irr 1–5 | A8 vs A2 | unit-out (19) | 7.62 / 9.86 | -2.24 [-4.00, -0.55] | 13/19 | 0.032 | 0.032 |
| Case 1, A8 | k = 5 | A8 vs A5 | unit-out (19) | 7.97 / 7.72 | +0.25 [-0.79, +1.45] | 10/19 | 0.98 | — |
| Case 1, A8 | irr 1–5 | A8 vs A5 | unit-out (19) | 7.62 / 7.60 | +0.02 [-0.92, +0.98] | 9/19 | 0.89 | — |
| Case 1, A8 | k = 1 | A8 vs A1 | unit-out (19) | 7.68 / 7.76 | -0.08 [-1.08, +0.86] | 9/19 | 0.98 | — |
| Case 1, A8 | k = 5 | A8 vs A2 | grouped (16) | 8.15 / 10.34 | -2.59 [-4.16, -0.91] | 13/16 | 0.018 | 0.036 |
| Case 1, A8 | irr 1–5 | A8 vs A2 | grouped (16) | 7.64 / 9.87 | -2.50 [-4.36, -0.71] | 10/16 | 0.039 | 0.039 |
| Case 1, A8 | k = 5 | A8 vs A5 | grouped (16) | 8.15 / 7.77 | +0.17 [-0.77, +1.15] | 8/16 | 0.74 | — |
| Case 1, A8 | irr 1–5 | A8 vs A5 | grouped (16) | 7.64 / 7.83 | -0.36 [-1.23, +0.54] | 8/16 | 0.38 | — |
| Case 1, A8 | k = 1 | A8 vs A1 | grouped (16) | 7.98 / 8.09 | -0.34 [-1.48, +0.72] | 9/16 | 0.74 | — |
| Case 1, GRU-D | k = 5 | GRU-D vs A2 | unit-out (19) | 7.78 / 10.39 | -2.61 [-4.62, -0.50] | 13/19 | 0.026 | 0.052 |
| Case 1, GRU-D | irr 1–5 | GRU-D vs A2 | unit-out (19) | 7.89 / 9.86 | -1.97 [-3.57, -0.37] | 14/19 | 0.036 | 0.052 |
| Case 1, GRU-D | k = 5 | GRU-D vs A5 | unit-out (19) | 7.78 / 7.72 | +0.06 [-0.62, +0.77] | 10/19 | 0.92 | — |
| Case 1, GRU-D | irr 1–5 | GRU-D vs A5 | unit-out (19) | 7.89 / 7.60 | +0.29 [-0.20, +0.77] | 7/19 | 0.28 | — |
| Case 1, GRU-D | k = 5 | GRU-D vs A2 | grouped (16) | 7.89 / 10.34 | -2.51 [-4.48, -0.36] | 11/16 | 0.044 | 0.067 |
| Case 1, GRU-D | irr 1–5 | GRU-D vs A2 | grouped (16) | 7.98 / 9.87 | -2.01 [-3.61, -0.36] | 12/16 | 0.034 | 0.067 |
| Case 1, GRU-D | k = 5 | GRU-D vs A5 | grouped (16) | 7.89 / 7.77 | +0.26 [-0.41, +0.92] | 7/16 | 0.53 | — |
| Case 1, GRU-D | irr 1–5 | GRU-D vs A5 | grouped (16) | 7.98 / 7.83 | +0.13 [-0.37, +0.61] | 6/16 | 0.6 | — |
| Case 2, S4 | last 5 | S4 vs S1 | unit-out (19) | 7.98 / 10.05 | -2.07 [-2.91, -1.19] | 15/19 | 0.00064 | 0.00064 |
| Case 2, S4 | last 3 | S4 vs S1 | unit-out (19) | 8.47 / 11.36 | -2.88 [-3.81, -1.90] | 17/19 | 9.5e-05 | 0.00019 |
| Case 2, S4 | complete | S4 vs S1 | unit-out (19) | 7.71 / 7.78 | -0.07 [-0.71, +0.47] | 9/19 | 0.89 | — |
| Case 2, S4 | last 5 | S4 vs S1 | grouped (16) | 8.15 / 10.15 | -2.25 [-3.14, -1.25] | 13/16 | 0.0017 | 0.0017 |
| Case 2, S4 | last 3 | S4 vs S1 | grouped (16) | 8.53 / 11.40 | -3.14 [-4.11, -2.03] | 15/16 | 0.00021 | 0.00043 |
| Case 2, S4 | complete | S4 vs S1 | grouped (16) | 8.10 / 8.19 | -0.19 [-0.84, +0.39] | 10/16 | 0.74 | — |
| Case 2, S8 | last 5 | S8 vs S1 | unit-out (19) | 9.15 / 10.05 | -0.90 [-1.27, -0.51] | 15/19 | 0.00052 | 0.00052 |
| Case 2, S8 | last 3 | S8 vs S1 | unit-out (19) | 9.69 / 11.36 | -1.67 [-2.18, -1.15] | 17/19 | 2.7e-05 | 5.3e-05 |
| Case 2, S8 | complete | S8 vs S1 | unit-out (19) | 7.37 / 7.78 | -0.40 [-1.02, +0.22] | 12/19 | 0.29 | — |
| Case 2, S8 | last 5 | S8 vs S1 | grouped (16) | 9.32 / 10.15 | -0.93 [-1.31, -0.54] | 13/16 | 0.00076 | 0.00076 |
| Case 2, S8 | last 3 | S8 vs S1 | grouped (16) | 9.80 / 11.40 | -1.73 [-2.28, -1.19] | 14/16 | 0.00015 | 0.00031 |
| Case 2, S8 | complete | S8 vs S1 | grouped (16) | 7.78 / 8.19 | -0.40 [-1.08, +0.32] | 10/16 | 0.25 | — |

## Table S10. Case 2, C-MAPSS: RMSE (cycles), mean ± s.d. over five seeds

| Subset | History | S1 | S2 | S3 | S4 | S5 | S6 | S8 |
|---|---|---|---|---|---|---|---|---|
| FD001 | complete | 16.04 ± 0.39 | 16.04 ± 0.39 | 15.04 ± 0.85 | 15.01 ± 0.78 | — | 15.74 ± 0.82 | 13.80 ± 0.58 |
| FD001 | last 20 | 23.51 ± 0.87 | 23.94 ± 0.65 | 16.97 ± 1.24 | 16.61 ± 0.72 | 17.42 ± 0.88 | 36.18 ± 2.65 | 18.08 ± 0.67 |
| FD001 | last 10 | 28.85 ± 0.57 | 27.81 ± 1.00 | 19.46 ± 0.73 | 19.36 ± 0.86 | 19.38 ± 0.66 | 36.26 ± 2.53 | 21.18 ± 0.25 |
| FD001 | last 5 | 26.29 ± 0.25 | 29.76 ± 0.68 | 18.00 ± 0.86 | 17.83 ± 0.59 | 16.86 ± 0.32 | 32.84 ± 3.38 | 19.34 ± 1.32 |
| FD002 | complete | 17.50 ± 0.36 | 17.49 ± 0.36 | 17.77 ± 0.46 | 17.73 ± 1.00 | — | 15.66 ± 0.65 | 15.41 ± 0.69 |
| FD002 | last 20 | 21.78 ± 0.80 | 23.43 ± 0.68 | 17.92 ± 0.49 | 18.13 ± 0.55 | 19.31 ± 0.23 | 38.53 ± 2.02 | 17.72 ± 0.76 |
| FD002 | last 10 | 24.66 ± 0.40 | 23.66 ± 1.25 | 18.41 ± 0.33 | 18.58 ± 0.49 | 18.94 ± 0.65 | 36.16 ± 1.54 | 18.55 ± 0.71 |
| FD002 | last 5 | 23.96 ± 1.13 | 21.55 ± 2.32 | 17.73 ± 0.67 | 17.79 ± 0.56 | 17.00 ± 0.22 | 32.43 ± 1.67 | 17.70 ± 0.81 |
| FD003 | complete | 13.27 ± 0.76 | 13.27 ± 0.76 | 14.01 ± 0.64 | 13.70 ± 0.42 | — | 13.27 ± 0.92 | 12.70 ± 0.84 |
| FD003 | last 20 | 20.53 ± 0.85 | 32.81 ± 2.51 | 15.33 ± 0.19 | 14.48 ± 0.83 | 14.52 ± 0.43 | 43.76 ± 3.48 | 18.13 ± 0.59 |
| FD003 | last 10 | 31.96 ± 1.16 | 40.06 ± 2.95 | 21.17 ± 0.47 | 20.07 ± 1.02 | 19.06 ± 0.67 | 46.18 ± 3.93 | 23.39 ± 0.75 |
| FD003 | last 5 | 35.83 ± 0.97 | 33.34 ± 2.01 | 20.61 ± 0.75 | 19.65 ± 0.53 | 19.03 ± 0.28 | 43.12 ± 3.89 | 22.72 ± 0.86 |
| FD004 | complete | 17.70 ± 0.70 | 18.43 ± 0.64 | 17.64 ± 0.79 | 16.23 ± 0.57 | — | 16.74 ± 0.86 | 15.04 ± 0.40 |
| FD004 | last 20 | 22.12 ± 0.75 | 29.73 ± 1.68 | 18.28 ± 0.66 | 17.87 ± 0.49 | 18.76 ± 1.14 | 38.49 ± 1.39 | 18.76 ± 0.39 |
| FD004 | last 10 | 27.44 ± 2.17 | 29.62 ± 1.00 | 20.16 ± 0.68 | 19.77 ± 0.36 | 20.30 ± 0.24 | 35.23 ± 1.72 | 20.71 ± 0.49 |
| FD004 | last 5 | 27.22 ± 0.99 | 25.55 ± 2.22 | 20.09 ± 0.48 | 20.37 ± 0.52 | 19.70 ± 0.22 | 33.32 ± 1.46 | 21.18 ± 0.48 |

## Table S11. Case 2, C-MAPSS: paired comparisons

Δ mean absolute error, first minus second (cycles) [95% bootstrap interval]; engines for which the first was better; two-sided Wilcoxon p; Holm over the eight H1 comparisons.

| Subset | History | Comparison | Δ [95% CI] | Better | p | p (Holm) |
|---|---|---|---|---|---|---|
| FD001 | last 10 | S4 vs S2 (H1) | -7.38 [-10.31, -4.39] | 73/100 | 4e-07 | 2e-06 |
| FD001 | last 5 | S4 vs S1 (H1) | -6.72 [-9.49, -4.04] | 70/100 | 7.8e-07 | 3.1e-06 |
| FD001 | complete | S4 vs S1 (H2) | -0.55 [-1.94, +0.84] | 48/100 | 0.99 | met |
| FD001 | complete | S8 vs S1 | -1.57 [-3.12, -0.18] | 54/100 | 0.16 | — |
| FD001 | complete | S8 vs S4 | -1.03 [-2.25, +0.18] | 59/100 | 0.072 | — |
| FD001 | last 10 | S8 vs S4 | +1.02 [-0.23, +2.29] | 44/100 | 0.15 | — |
| FD001 | last 5 | S8 vs S4 | +1.19 [+0.26, +2.11] | 35/100 | 0.0078 | — |
| FD001 | complete | S8 vs S6 | -1.31 [-2.86, +0.28] | 56/100 | 0.17 | — |
| FD001 | last 10 | S8 vs S6 | -11.49 [-15.29, -7.74] | 78/100 | 1.9e-09 | — |
| FD001 | last 5 | S8 vs S6 | -10.31 [-13.56, -7.20] | 77/100 | 1.3e-09 | — |
| FD001 | complete | S4 vs S3 | +0.10 [-0.60, +0.79] | 50/100 | 0.67 | — |
| FD001 | last 10 | S4 vs S3 | -0.13 [-0.81, +0.53] | 47/100 | 0.58 | — |
| FD001 | last 5 | S4 vs S3 | -0.14 [-0.70, +0.41] | 56/100 | 0.42 | — |
| FD001 | last 20 | S4 vs S5 | -0.67 [-1.45, +0.09] | 51/100 | 0.18 | — |
| FD001 | last 10 | S4 vs S5 | -0.14 [-0.88, +0.58] | 52/100 | 0.92 | — |
| FD001 | last 5 | S4 vs S5 | +0.54 [-0.16, +1.25] | 41/100 | 0.12 | — |
| FD002 | last 10 | S4 vs S2 (H1) | -3.57 [-5.10, -2.05] | 154/259 | 1.4e-05 | 2.7e-05 |
| FD002 | last 5 | S4 vs S2 (H1) | -2.37 [-3.60, -1.15] | 163/259 | 5.9e-05 | 5.9e-05 |
| FD002 | complete | S4 vs S1 (H2) | +0.57 [-0.18, +1.29] | 118/259 | 0.06 | not met |
| FD002 | complete | S8 vs S1 | -1.42 [-2.42, -0.44] | 152/259 | 0.001 | — |
| FD002 | complete | S8 vs S4 | -2.00 [-3.06, -0.93] | 162/259 | 0.00011 | — |
| FD002 | last 10 | S8 vs S4 | -0.23 [-0.88, +0.44] | 142/259 | 0.39 | — |
| FD002 | last 5 | S8 vs S4 | -0.53 [-1.13, +0.07] | 148/259 | 0.038 | — |
| FD002 | complete | S8 vs S6 | +0.40 [-0.75, +1.57] | 118/259 | 0.24 | — |
| FD002 | last 10 | S8 vs S6 | -12.56 [-15.46, -9.82] | 176/259 | 2.7e-15 | — |
| FD002 | last 5 | S8 vs S6 | -10.39 [-12.73, -8.17] | 173/259 | 3.4e-15 | — |
| FD002 | complete | S4 vs S3 | +0.41 [-0.19, +0.98] | 115/259 | 0.064 | — |
| FD002 | last 10 | S4 vs S3 | +0.52 [-0.04, +1.08] | 116/259 | 0.034 | — |
| FD002 | last 5 | S4 vs S3 | +0.25 [-0.19, +0.71] | 125/259 | 0.56 | — |
| FD002 | last 20 | S4 vs S5 | -0.31 [-0.97, +0.32] | 125/259 | 0.97 | — |
| FD002 | last 10 | S4 vs S5 | -0.14 [-0.75, +0.44] | 121/259 | 0.9 | — |
| FD002 | last 5 | S4 vs S5 | +0.39 [-0.08, +0.84] | 117/259 | 0.043 | — |
| FD003 | last 10 | S4 vs S1 (H1) | -9.53 [-12.46, -6.73] | 79/100 | 5.9e-10 | 4.1e-09 |
| FD003 | last 5 | S4 vs S2 (H1) | -13.10 [-16.19, -10.09] | 81/100 | 1.5e-11 | 1.2e-10 |
| FD003 | complete | S4 vs S1 (H2) | +0.89 [+0.03, +1.77] | 33/100 | 0.0059 | not met |
| FD003 | complete | S8 vs S1 | -0.35 [-1.43, +0.67] | 48/100 | 0.87 | — |
| FD003 | complete | S8 vs S4 | -1.25 [-2.14, -0.35] | 67/100 | 0.0027 | — |
| FD003 | last 10 | S8 vs S4 | +2.23 [+1.14, +3.33] | 35/100 | 0.00073 | — |
| FD003 | last 5 | S8 vs S4 | +2.44 [+1.21, +3.75] | 39/100 | 0.00045 | — |
| FD003 | complete | S8 vs S6 | -0.39 [-1.64, +0.80] | 48/100 | 0.63 | — |
| FD003 | last 10 | S8 vs S6 | -19.09 [-24.12, -14.26] | 77/100 | 6.7e-12 | — |
| FD003 | last 5 | S8 vs S6 | -16.40 [-20.68, -12.34] | 80/100 | 3.3e-12 | — |
| FD003 | complete | S4 vs S3 | -0.27 [-1.19, +0.66] | 46/100 | 1 | — |
| FD003 | last 10 | S4 vs S3 | -0.78 [-1.35, -0.20] | 65/100 | 0.0026 | — |
| FD003 | last 5 | S4 vs S3 | -0.92 [-1.67, -0.21] | 62/100 | 0.012 | — |
| FD003 | last 20 | S4 vs S5 | +0.00 [-0.67, +0.69] | 53/100 | 0.64 | — |
| FD003 | last 10 | S4 vs S5 | +0.24 [-0.50, +1.00] | 52/100 | 0.74 | — |
| FD003 | last 5 | S4 vs S5 | +0.18 [-0.45, +0.83] | 55/100 | 0.98 | — |
| FD004 | last 10 | S4 vs S1 (H1) | -4.83 [-6.68, -3.04] | 159/248 | 6.3e-08 | 3.8e-07 |
| FD004 | last 5 | S4 vs S2 (H1) | -4.09 [-5.69, -2.47] | 156/248 | 2.1e-06 | 6.2e-06 |
| FD004 | complete | S4 vs S1 (H2) | -0.90 [-1.62, -0.18] | 138/248 | 0.0056 | met |
| FD004 | complete | S8 vs S1 | -2.12 [-3.10, -1.12] | 153/248 | 8.8e-06 | — |
| FD004 | complete | S8 vs S4 | -1.22 [-2.01, -0.43] | 148/248 | 0.002 | — |
| FD004 | last 10 | S8 vs S4 | +0.42 [-0.32, +1.20] | 117/248 | 0.44 | — |
| FD004 | last 5 | S8 vs S4 | +0.26 [-0.37, +0.88] | 118/248 | 0.29 | — |
| FD004 | complete | S8 vs S6 | -0.97 [-1.94, -0.06] | 127/248 | 0.17 | — |
| FD004 | last 10 | S8 vs S6 | -9.55 [-12.19, -6.99] | 157/248 | 2.9e-11 | — |
| FD004 | last 5 | S8 vs S6 | -7.87 [-10.10, -5.76] | 159/248 | 3.2e-11 | — |
| FD004 | complete | S4 vs S3 | -1.23 [-1.79, -0.65] | 140/248 | 0.00025 | — |
| FD004 | last 10 | S4 vs S3 | -0.27 [-0.86, +0.29] | 123/248 | 0.76 | — |
| FD004 | last 5 | S4 vs S3 | +0.14 [-0.27, +0.54] | 117/248 | 0.57 | — |
| FD004 | last 20 | S4 vs S5 | -0.71 [-1.25, -0.18] | 146/248 | 0.014 | — |
| FD004 | last 10 | S4 vs S5 | -0.47 [-0.94, -0.01] | 133/248 | 0.15 | — |
| FD004 | last 5 | S4 vs S5 | +0.31 [-0.06, +0.66] | 109/248 | 0.037 | — |

## Table S12. Case 2, C-MAPSS: bias and late predictions

Mean signed error (positive = over-estimated remaining life), median PHM 2008 score over seeds, largest late error over all seeds (cycles).

| Subset | Arm | Complete | Last 10 | Last 5 |
|---|---|---|---|---|
| FD001 | S1 | bias +2.2; PHM 609; late 55 | bias +14.7; PHM 40441; late 103 | bias +16.4; PHM 17713; late 97 |
| FD001 | S2 | bias +2.2; PHM 609; late 55 | bias +10.0; PHM 8438; late 91 | bias +16.1; PHM 17432; late 90 |
| FD001 | S4 | bias +1.4; PHM 412; late 50 | bias +3.2; PHM 1168; late 65 | bias +4.0; PHM 933; late 59 |
| FD001 | S8 | bias -0.1; PHM 323; late 44 | bias +6.8; PHM 2346; late 75 | bias +7.7; PHM 1437; late 65 |
| FD001 | S6 | bias +1.4; PHM 454; late 48 | bias +23.1; PHM 82351; late 109 | bias +20.2; PHM 15998; late 105 |
| FD002 | S1 | bias -0.1; PHM 2363; late 67 | bias +11.9; PHM 53383; late 117 | bias +11.5; PHM 37045; late 106 |
| FD002 | S2 | bias -0.1; PHM 2362; late 67 | bias +1.4; PHM 8128; late 86 | bias +10.0; PHM 8392; late 83 |
| FD002 | S4 | bias -0.3; PHM 3258; late 74 | bias +0.5; PHM 3859; late 98 | bias +1.0; PHM 3189; late 74 |
| FD002 | S8 | bias -1.9; PHM 1143; late 60 | bias +0.8; PHM 4507; late 87 | bias +1.8; PHM 2406; late 68 |
| FD002 | S6 | bias +0.7; PHM 1551; late 58 | bias +22.2; PHM 143793; late 111 | bias +18.6; PHM 83848; late 102 |
| FD003 | S1 | bias +3.6; PHM 458; late 61 | bias +22.1; PHM 19183; late 89 | bias +26.5; PHM 22164; late 90 |
| FD003 | S2 | bias +3.6; PHM 458; late 61 | bias -16.1; PHM 15814; late 92 | bias -2.3; PHM 11285; late 95 |
| FD003 | S4 | bias +3.3; PHM 417; late 58 | bias +7.4; PHM 2111; late 72 | bias +7.5; PHM 2448; late 71 |
| FD003 | S8 | bias +3.3; PHM 338; late 55 | bias +11.2; PHM 5468; late 81 | bias +11.9; PHM 4319; late 78 |
| FD003 | S6 | bias +3.1; PHM 404; late 43 | bias +34.2; PHM 147450; late 135 | bias +30.8; PHM 83553; late 109 |
| FD004 | S1 | bias +1.4; PHM 2033; late 85 | bias +12.9; PHM 43132; late 101 | bias +13.3; PHM 31658; late 100 |
| FD004 | S2 | bias +1.1; PHM 2600; late 85 | bias -5.6; PHM 10335; late 75 | bias +8.5; PHM 10830; late 84 |
| FD004 | S4 | bias +0.5; PHM 1658; late 66 | bias +1.9; PHM 4507; late 75 | bias +2.7; PHM 4588; late 75 |
| FD004 | S8 | bias +0.3; PHM 1279; late 60 | bias +4.1; PHM 4507; late 82 | bias +5.2; PHM 6460; late 88 |
| FD004 | S6 | bias +0.7; PHM 1798; late 67 | bias +20.9; PHM 139684; late 111 | bias +18.2; PHM 107286; late 109 |

## Table S13. N-CMAPSS mean RMSE of all arms under both validation schemes

| Evaluation | Scenario | Arm | Unit-out (19) | Grouped (16) |
|---|---|---|---|---|
| Case 1, pre-specified run | irr 1–5 | A1 | 11.08 | 11.07 |
| Case 1, pre-specified run | irr 1–5 | A2 | 9.86 | 9.87 |
| Case 1, pre-specified run | irr 1–5 | A3 | 10.08 | 10.05 |
| Case 1, pre-specified run | irr 1–5 | A4 | 8.36 | 8.39 |
| Case 1, pre-specified run | irr 1–5 | A5 | 7.65 | 7.96 |
| Case 1, pre-specified run | irr 1–5 | A6 | 15.08 | 14.96 |
| Case 1, pre-specified run | k = 1 | A1 | 7.76 | 8.09 |
| Case 1, pre-specified run | k = 1 | A2 | 7.76 | 8.09 |
| Case 1, pre-specified run | k = 1 | A3 | 7.76 | 8.09 |
| Case 1, pre-specified run | k = 1 | A4 | 7.67 | 7.87 |
| Case 1, pre-specified run | k = 1 | A5 | 7.58 | 7.74 |
| Case 1, pre-specified run | k = 1 | A6 | 9.20 | 9.38 |
| Case 1, pre-specified run | k = 5 | A1 | 12.52 | 12.31 |
| Case 1, pre-specified run | k = 5 | A2 | 10.39 | 10.34 |
| Case 1, pre-specified run | k = 5 | A3 | 11.83 | 11.64 |
| Case 1, pre-specified run | k = 5 | A4 | 7.98 | 7.69 |
| Case 1, pre-specified run | k = 5 | A5 | 7.71 | 7.88 |
| Case 1, pre-specified run | k = 5 | A6 | 16.59 | 16.34 |
| Case 1, pre-specified run | k = 5 | A7 | 8.08 | 8.42 |
| Case 1, A8/GRU-D run | irr 1–5 | A1 | 11.08 | 11.07 |
| Case 1, A8/GRU-D run | irr 1–5 | A2 | 9.86 | 9.87 |
| Case 1, A8/GRU-D run | irr 1–5 | A3 | 10.08 | 10.05 |
| Case 1, A8/GRU-D run | irr 1–5 | A5 | 7.60 | 7.83 |
| Case 1, A8/GRU-D run | irr 1–5 | A8 | 7.62 | 7.64 |
| Case 1, A8/GRU-D run | irr 1–5 | GRU-D | 7.89 | 7.98 |
| Case 1, A8/GRU-D run | k = 1 | A1 | 7.76 | 8.09 |
| Case 1, A8/GRU-D run | k = 1 | A2 | 7.76 | 8.09 |
| Case 1, A8/GRU-D run | k = 1 | A3 | 7.76 | 8.09 |
| Case 1, A8/GRU-D run | k = 1 | A5 | 7.58 | 7.64 |
| Case 1, A8/GRU-D run | k = 1 | A8 | 7.68 | 7.98 |
| Case 1, A8/GRU-D run | k = 1 | GRU-D | 8.49 | 8.57 |
| Case 1, A8/GRU-D run | k = 5 | A1 | 12.52 | 12.31 |
| Case 1, A8/GRU-D run | k = 5 | A2 | 10.39 | 10.34 |
| Case 1, A8/GRU-D run | k = 5 | A3 | 11.83 | 11.64 |
| Case 1, A8/GRU-D run | k = 5 | A5 | 7.72 | 7.77 |
| Case 1, A8/GRU-D run | k = 5 | A8 | 7.97 | 8.15 |
| Case 1, A8/GRU-D run | k = 5 | GRU-D | 7.78 | 7.89 |
| Case 2 | complete | S1 | 7.78 | 8.19 |
| Case 2 | complete | S2 | 7.78 | 8.19 |
| Case 2 | complete | S6 | 9.33 | 9.51 |
| Case 2 | complete | S4 | 7.71 | 8.10 |
| Case 2 | complete | S3 | 7.68 | 7.77 |
| Case 2 | complete | S8 | 7.37 | 7.78 |
| Case 2 | last 3 | S1 | 11.36 | 11.40 |
| Case 2 | last 3 | S2 | 20.58 | 20.65 |
| Case 2 | last 3 | S6 | 18.12 | 18.19 |
| Case 2 | last 3 | S4 | 8.47 | 8.53 |
| Case 2 | last 3 | S3 | 8.55 | 8.54 |
| Case 2 | last 3 | S5 | 7.67 | 7.97 |
| Case 2 | last 3 | S8 | 9.69 | 9.80 |
| Case 2 | last 5 | S1 | 10.05 | 10.15 |
| Case 2 | last 5 | S2 | 15.35 | 15.45 |
| Case 2 | last 5 | S6 | 17.74 | 17.84 |
| Case 2 | last 5 | S4 | 7.98 | 8.15 |
| Case 2 | last 5 | S3 | 8.08 | 8.09 |
| Case 2 | last 5 | S5 | 7.92 | 8.14 |
| Case 2 | last 5 | S8 | 9.15 | 9.32 |

## Table S14. End-of-life accuracy: RMSE (and mean signed error) on C-MAPSS test engines with true RUL ≤ 50 cycles

Case 1: five-seed run; case 2: five seeds. Engines with RUL ≤ 50: FD001 33, FD002 88, FD003 29, FD004 80.

| Subset | Case | Scenario | A1/S1 | A2/S2 | A6/S6 | A5/S4 | A8/S8 | GRU-D |
|---|---|---|---|---|---|---|---|---|
| FD001 | 1 | k = 1 | 6.2 (+2.4) | 6.2 (+2.4) | 7.2 (+2.3) | 7.1 (+4.3) | 4.5 (+0.1) | 7.0 (+3.8) |
| FD001 | 1 | k = 5 | 12.0 (-9.0) | 12.9 (+6.2) | 12.1 (+3.9) | 6.7 (+3.4) | 7.3 (+2.8) | 7.7 (+3.0) |
| FD001 | 1 | irr 1–5 | 10.6 (-7.3) | 9.6 (+4.1) | 8.6 (+3.0) | 6.3 (+1.8) | 5.6 (+1.7) | 7.4 (+2.0) |
| FD001 | 2 | complete | 6.2 (+2.4) | 6.2 (+2.4) | 7.2 (+2.3) | 5.7 (+0.9) | 5.4 (+1.1) | — |
| FD001 | 2 | last 10 | 32.0 (+18.7) | 27.6 (-1.5) | 45.2 (+27.1) | 13.8 (+5.6) | 19.0 (+9.3) | — |
| FD001 | 2 | last 5 | 25.4 (+14.9) | 30.5 (+10.9) | 36.0 (+17.2) | 13.2 (+5.5) | 15.1 (+7.1) | — |
| FD002 | 1 | k = 1 | 7.6 (+0.7) | 7.6 (+0.7) | 7.2 (+1.6) | 7.7 (+1.8) | 5.5 (-0.8) | 7.9 (+2.8) |
| FD002 | 1 | k = 5 | 12.1 (-3.8) | 15.3 (+5.8) | 23.1 (+13.5) | 5.7 (+2.0) | 6.1 (+1.7) | 6.3 (+2.5) |
| FD002 | 1 | irr 1–5 | 9.3 (-5.4) | 13.4 (+4.2) | 16.3 (+7.9) | 6.2 (+1.8) | 5.7 (+1.4) | 6.3 (+2.2) |
| FD002 | 2 | complete | 7.6 (+0.7) | 7.6 (+0.7) | 7.2 (+1.6) | 9.0 (+2.7) | 5.4 (+0.7) | — |
| FD002 | 2 | last 10 | 24.2 (+11.0) | 16.4 (-7.5) | 43.9 (+24.5) | 13.4 (+4.8) | 11.6 (+3.0) | — |
| FD002 | 2 | last 5 | 22.3 (+9.2) | 16.7 (+8.3) | 35.4 (+14.8) | 12.5 (+4.4) | 12.3 (+2.9) | — |
| FD003 | 1 | k = 1 | 4.8 (-0.4) | 4.8 (-0.4) | 5.0 (+1.2) | 6.6 (+3.9) | 5.5 (+1.5) | 6.1 (+2.6) |
| FD003 | 1 | k = 5 | 30.8 (-28.3) | 7.5 (+0.2) | 5.9 (-0.1) | 5.2 (+1.4) | 5.4 (+0.6) | 6.1 (+0.7) |
| FD003 | 1 | irr 1–5 | 21.9 (-19.7) | 5.7 (+1.2) | 7.6 (+1.5) | 5.1 (+2.1) | 6.7 (+1.6) | 5.7 (+1.1) |
| FD003 | 2 | complete | 4.8 (-0.4) | 4.8 (-0.4) | 5.0 (+1.2) | 6.9 (-2.8) | 5.1 (+1.2) | — |
| FD003 | 2 | last 10 | 35.8 (+25.1) | 33.0 (-21.8) | 61.9 (+48.6) | 17.1 (+6.2) | 22.0 (+11.0) | — |
| FD003 | 2 | last 5 | 41.7 (+31.2) | 39.1 (-22.5) | 54.3 (+38.9) | 17.9 (+7.1) | 21.3 (+11.7) | — |
| FD004 | 1 | k = 1 | 12.0 (+5.4) | 12.0 (+5.4) | 11.5 (+4.7) | 11.0 (+6.0) | 6.2 (+1.7) | 11.9 (+6.6) |
| FD004 | 1 | k = 5 | 19.9 (-8.0) | 22.9 (+10.9) | 23.4 (+11.6) | 10.0 (+5.2) | 12.4 (+5.4) | 9.9 (+5.2) |
| FD004 | 1 | irr 1–5 | 14.6 (-6.2) | 21.6 (+9.1) | 18.4 (+8.4) | 9.5 (+4.8) | 9.4 (+4.2) | 10.0 (+4.4) |
| FD004 | 2 | complete | 12.0 (+5.4) | 12.0 (+5.4) | 11.5 (+4.7) | 10.5 (+3.9) | 8.3 (+2.8) | — |
| FD004 | 2 | last 10 | 31.6 (+18.4) | 21.5 (-4.8) | 45.5 (+27.5) | 15.9 (+7.7) | 16.7 (+8.7) | — |
| FD004 | 2 | last 5 | 30.7 (+17.0) | 27.7 (+13.7) | 40.8 (+21.4) | 16.4 (+8.0) | 18.7 (+8.2) | — |

## Table S15. Case 1: availability of measured records in the C-MAPSS test windows

Share of test engines whose 30-record window cannot be filled with measured records (padded by repeating the first record; padded rows have gap 0). At k = 5 the median number of measured records is 27–30 in the 30-record window of A5 and in the 150-cycle window of A6 and A8, but 6 in the 30-cycle interpolated window of A2 and A3.

| Subset | Test engines | Padded at k = 1 | Padded at k = 5 | Padded at irr 1–5 |
|---|---|---|---|---|
| FD001 | 100 | 0% | 58% | 25% |
| FD002 | 259 | 2% | 57% | 30% |
| FD003 | 100 | 0% | 47% | 16% |
| FD004 | 248 | 4% | 46% | 19% |


## Table S16. Confirmatory comparisons by training seed

Case 1, C-MAPSS (three seeds): A5 minus the best test-time remedy. ΔRMSE per seed; ΔMAE per seed; mean ΔRMSE with 95% engine-bootstrap interval (conditional on the trained models).

| Subset | Scenario | Reference | ΔRMSE per seed | ΔMAE per seed | Seeds A5 better | Mean ΔRMSE [95% CI] |
|---|---|---|---|---|---|---|
| FD001 | k = 5 | A2 | −7.69, −8.99, −7.19 | −5.69, −5.82, −5.20 | 3/3 | −7.96 [−11.16, −4.55] |
| FD001 | irr 1–5 | A2 | −5.74, −7.46, −6.29 | −4.29, −5.29, −3.53 | 3/3 | −6.49 [−10.36, −2.61] |
| FD002 | k = 5 | A1 | −6.92, −9.21, −7.07 | −5.11, −6.80, −5.05 | 3/3 | −7.74 [−9.35, −6.12] |
| FD002 | irr 1–5 | A1 | −5.43, −7.08, −5.18 | −4.07, −5.25, −3.50 | 3/3 | −5.90 [−7.20, −4.62] |
| FD003 | k = 5 | A2 | −2.57, −2.30, −3.05 | −2.64, −2.46, −2.55 | 3/3 | −2.64 [−4.97, −0.43] |
| FD003 | irr 1–5 | A2 | −4.68, −4.39, −5.08 | −2.48, −3.49, −3.42 | 3/3 | −4.72 [−8.34, −1.34] |
| FD004 | k = 5 | A2 | −8.70, −9.85, −6.26 | −6.58, −6.76, −4.91 | 3/3 | −8.27 [−11.13, −5.41] |
| FD004 | irr 1–5 | A2 | −8.08, −7.84, −6.41 | −5.14, −5.16, −3.77 | 3/3 | −7.44 [−10.50, −4.65] |

Case 1, N-CMAPSS (twins grouped, three seeds): A5 minus A2; per-seed difference of the equal-weight group mean of unit RMSE.

| Scenario | Δ per seed | Seeds A5 better | Unit-weighted means A5 / A2 | Equal-group-weight means A5 / A2 | Δ (group, seed-averaged) |
|---|---|---|---|---|---|
| k = 5 | −2.97, −2.14, −2.72 | 3/3 | 7.88 / 10.34 | 8.01 / 10.62 | −2.61 |
| irr 1–5 | −2.31, −1.55, −2.15 | 3/3 | 7.96 / 9.87 | 8.10 / 10.10 | −2.00 |

Case 2, C-MAPSS (five seeds): S4 minus the better of S1/S2.

| Subset | History | Reference | ΔRMSE per seed | Seeds S4 better | Mean ΔRMSE [95% CI] |
|---|---|---|---|---|---|
| FD001 | last 10 | S2 | −9.87, −8.55, −8.23, −7.13, −8.46 | 5/5 | −8.45 [−12.12, −4.41] |
| FD001 | last 5 | S1 | −9.22, −7.65, −9.12, −8.16, −8.12 | 5/5 | −8.45 [−12.31, −4.76] |
| FD002 | last 10 | S2 | −4.83, −7.41, −3.34, −5.48, −4.37 | 5/5 | −5.09 [−6.87, −3.32] |
| FD002 | last 5 | S2 | −6.70, −4.81, −2.32, −3.48, −1.52 | 5/5 | −3.76 [−5.26, −2.26] |
| FD003 | last 10 | S1 | −12.28, −12.71, −12.44, −9.92, −12.13 | 5/5 | −11.90 [−14.95, −8.86] |
| FD003 | last 5 | S2 | −16.81, −14.54, −11.58, −13.83, −11.69 | 5/5 | −13.69 [−17.72, −10.04] |
| FD004 | last 10 | S1 | −7.47, −4.57, −6.35, −9.99, −9.98 | 5/5 | −7.67 [−10.05, −5.34] |
| FD004 | last 5 | S2 | −2.81, −4.50, −5.30, −9.20, −4.09 | 5/5 | −5.18 [−7.14, −3.23] |

Case 2, N-CMAPSS (twins grouped, five seeds): S4 minus the better of S1/S2 (chosen on unit-weighted mean RMSE).

| History | Reference | Δ per seed | Seeds S4 better | Unit-weighted means S4 / ref | Equal-group-weight means S4 / ref | Δ (group, seed-averaged) |
|---|---|---|---|---|---|---|
| last 5 | S1 | −2.43, −1.73, −2.40, −2.70, −1.99 | 5/5 | 8.15 / 10.15 | 8.23 / 10.48 | −2.25 |
| last 3 | S1 | −3.47, −2.44, −3.36, −3.50, −2.91 | 5/5 | 8.53 / 11.40 | 8.65 / 11.79 | −3.14 |

## Table S17. Complete records: long-input variants against the dense model (exploratory non-inferiority)

ΔMAE: seed-averaged engine absolute error, variant minus dense model, 95% engine-bootstrap interval. ΔRMSE: mean over seeds of the RMSE difference, 95% engine-bootstrap interval. "Within 1 cycle": upper bound of the interval below +1.0 cycle. Source runs: A8 and A5 rows use the five-seed case-1 exploratory run (Table 4); S8 and S4 rows use the five-seed case-2 run. The A5 rows therefore differ from the three-seed pre-specified H2 analysis in section 4.2 and Table S2 (for example FD001: −0.38 here, −0.14 there) and do not replace it.

| Subset | Comparison | ΔMAE [95% CI] | ΔRMSE [95% CI] | Within 1 cycle (MAE / RMSE) |
|---|---|---|---|---|
| FD001 | A8 vs A1 | −0.93 [−3.22, +1.22] | −1.78 [−4.83, +1.07] | no / no |
| FD001 | S8 vs S1 | −1.57 [−3.12, −0.18] | −2.25 [−4.55, +0.07] | yes / yes |
| FD001 | A5 vs A1 | −0.38 [−1.71, +0.90] | −1.33 [−2.94, +0.29] | yes / yes |
| FD001 | S4 vs S1 | −0.55 [−1.94, +0.84] | −1.03 [−2.97, +0.94] | yes / yes |
| FD002 | A8 vs A1 | −2.58 [−3.69, −1.53] | −4.72 [−6.27, −3.16] | yes / yes |
| FD002 | S8 vs S1 | −1.42 [−2.42, −0.44] | −2.09 [−3.61, −0.57] | yes / yes |
| FD002 | A5 vs A1 | −1.33 [−2.10, −0.56] | −2.63 [−3.69, −1.57] | yes / yes |
| FD002 | S4 vs S1 | +0.57 [−0.18, +1.29] | +0.23 [−0.78, +1.20] | no / no |
| FD003 | A8 vs A1 | −0.66 [−2.02, +0.65] | −1.17 [−3.54, +1.01] | yes / no |
| FD003 | S8 vs S1 | −0.35 [−1.43, +0.67] | −0.57 [−2.61, +1.18] | yes / no |
| FD003 | A5 vs A1 | +1.66 [+0.84, +2.53] | +1.60 [+0.61, +2.67] | no / no |
| FD003 | S4 vs S1 | +0.89 [+0.03, +1.77] | +0.43 [−1.07, +2.02] | no / no |
| FD004 | A8 vs A1 | −2.89 [−3.90, −1.86] | −4.25 [−5.61, −2.87] | yes / yes |
| FD004 | S8 vs S1 | −2.12 [−3.10, −1.12] | −2.66 [−4.06, −1.26] | yes / yes |
| FD004 | A5 vs A1 | −1.17 [−1.97, −0.39] | −2.21 [−3.45, −1.03] | yes / yes |
| FD004 | S4 vs S1 | −0.90 [−1.62, −0.18] | −1.47 [−2.54, −0.40] | yes / yes |

## Table S18. Mixed deployment: RMSE when a fraction w of predictions has complete records (exploratory)

RMSE_mix(w) = sqrt(w·MSE_complete + (1−w)·MSE_degraded), per seed, averaged over seeds. Case 1: degraded = one record every five cycles (k = 5); A2 is the densely trained model with interpolation (identical to A1 with complete records). Case 2: degraded = last 5 cycles. Entries: arm with the lowest RMSE_mix at each w.

| Subset | Case | w = 0.0 | w = 0.25 | w = 0.5 | w = 0.75 | w = 0.9 | w = 1.0 |
|---|---|---|---|---|---|---|---|
| FD001 | 1 | A5 12.7 | A5 13.2 | A5 13.7 | A5 14.2 | A8 14.3 | A8 14.3 |
| FD001 | 2 | S4 17.8 | S4 17.2 | S4 16.5 | S8 15.4 | S8 14.5 | S8 13.8 |
| FD002 | 1 | A5 13.3 | A8 13.5 | A8 13.3 | A8 13.0 | A8 12.9 | A8 12.8 |
| FD002 | 2 | S8 17.7 | S8 17.2 | S8 16.6 | S8 16.0 | S8 15.7 | S8 15.4 |
| FD003 | 1 | A5 14.5 | A8 14.2 | A8 13.5 | A8 12.8 | A8 12.4 | A8 12.1 |
| FD003 | 2 | S4 19.6 | S4 18.3 | S4 16.9 | S4 15.4 | S8 14.0 | S8 12.7 |
| FD004 | 1 | A5 15.1 | A5 15.2 | A8 15.0 | A8 14.2 | A8 13.8 | A8 13.4 |
| FD004 | 2 | S4 20.4 | S4 19.4 | S8 18.4 | S8 16.8 | S8 15.8 | S8 15.0 |

## Table S19. A8 history-span control (C-MAPSS, five seeds, all arms trained together): RMSE (cycles), mean ± s.d.

A8F: sparse records covering the full 150-cycle window. A6S: consecutive cycles over the span of an A8 window, padded to 150. All four long-input arms receive the same interpolated 150-cycle test input. Protocol written before the run (control_a8/PROTOCOL_A8_control.md).

| Subset | Scenario | A1 | A6 | A8 | A8F | A6S |
|---|---|---|---|---|---|---|
| FD001 | k = 1 | 16.04 ± 0.39 | 15.74 ± 0.82 | 13.98 ± 1.24 | 13.59 ± 0.33 | 14.69 ± 0.46 |
| FD001 | k = 2 | 20.05 ± 0.72 | 16.02 ± 1.29 | 13.15 ± 0.63 | 14.04 ± 0.36 | 18.04 ± 1.28 |
| FD001 | k = 3 | 23.44 ± 0.72 | 17.19 ± 1.25 | 13.69 ± 0.49 | 14.64 ± 0.33 | 17.45 ± 1.42 |
| FD001 | k = 5 | 24.93 ± 0.91 | 18.20 ± 1.03 | 14.56 ± 0.79 | 15.37 ± 0.58 | 19.90 ± 2.09 |
| FD001 | irr 1–5 | 22.87 ± 1.02 | 16.58 ± 1.44 | 13.05 ± 0.57 | 13.55 ± 0.41 | 18.59 ± 1.12 |
| FD001 | irr 1–10 | 26.00 ± 0.72 | 18.99 ± 0.89 | 14.64 ± 0.42 | 14.65 ± 0.49 | 20.02 ± 1.71 |
| FD002 | k = 1 | 17.50 ± 0.36 | 15.66 ± 0.65 | 12.30 ± 0.97 | 13.13 ± 0.35 | 16.06 ± 0.80 |
| FD002 | k = 2 | 18.44 ± 1.02 | 17.68 ± 0.43 | 11.88 ± 0.31 | 12.99 ± 0.39 | 16.82 ± 0.44 |
| FD002 | k = 3 | 19.29 ± 0.49 | 19.42 ± 0.95 | 13.43 ± 0.54 | 14.46 ± 0.62 | 19.22 ± 0.84 |
| FD002 | k = 5 | 20.69 ± 0.58 | 23.33 ± 1.15 | 13.98 ± 0.16 | 15.33 ± 0.36 | 21.30 ± 0.69 |
| FD002 | irr 1–5 | 18.70 ± 0.48 | 19.89 ± 0.68 | 13.71 ± 0.22 | 13.79 ± 0.49 | 19.82 ± 0.51 |
| FD002 | irr 1–10 | 21.92 ± 0.77 | 23.48 ± 1.00 | 14.33 ± 0.09 | 14.98 ± 0.22 | 23.05 ± 0.86 |
| FD003 | k = 1 | 13.27 ± 0.76 | 13.27 ± 0.92 | 11.97 ± 0.51 | 12.05 ± 0.93 | 12.76 ± 1.09 |
| FD003 | k = 2 | 19.98 ± 0.40 | 16.56 ± 1.32 | 13.30 ± 0.52 | 12.77 ± 1.27 | 14.04 ± 0.81 |
| FD003 | k = 3 | 26.91 ± 0.73 | 15.83 ± 0.65 | 13.61 ± 0.44 | 12.68 ± 0.75 | 15.68 ± 1.31 |
| FD003 | k = 5 | 35.62 ± 1.42 | 15.79 ± 0.44 | 14.73 ± 0.62 | 14.39 ± 0.92 | 15.35 ± 0.69 |
| FD003 | irr 1–5 | 26.73 ± 0.79 | 17.07 ± 0.88 | 13.84 ± 0.35 | 14.36 ± 0.87 | 14.29 ± 1.09 |
| FD003 | irr 1–10 | 34.91 ± 1.56 | 16.80 ± 0.80 | 13.63 ± 0.73 | 13.58 ± 0.75 | 15.63 ± 0.80 |
| FD004 | k = 1 | 17.70 ± 0.70 | 16.74 ± 0.86 | 13.34 ± 0.41 | 13.79 ± 0.60 | 14.68 ± 0.45 |
| FD004 | k = 2 | 20.41 ± 0.66 | 18.91 ± 1.24 | 13.29 ± 0.24 | 13.72 ± 0.48 | 19.28 ± 1.39 |
| FD004 | k = 3 | 24.22 ± 1.54 | 19.94 ± 1.43 | 13.28 ± 0.54 | 14.02 ± 0.56 | 19.80 ± 1.48 |
| FD004 | k = 5 | 29.37 ± 2.47 | 22.83 ± 1.29 | 16.14 ± 0.37 | 16.55 ± 0.42 | 22.71 ± 1.21 |
| FD004 | irr 1–5 | 25.45 ± 1.22 | 21.12 ± 1.59 | 14.54 ± 0.57 | 16.14 ± 1.13 | 21.21 ± 1.86 |
| FD004 | irr 1–10 | 28.92 ± 1.86 | 21.79 ± 2.51 | 15.81 ± 0.90 | 16.31 ± 0.50 | 23.88 ± 1.37 |

## Table S20. A8 history-span control: paired comparisons

Δ: seed-averaged engine absolute error, first minus second arm (cycles) [95% bootstrap CI]; engines for which the first arm was better; Wilcoxon p; Holm-adjusted p within the 8 comparisons at k = 5 and irregular 1–5.

**C1: A8F versus A6 (sparsification, full span).** Holm-significant in favour of A8F: 8 of 8; in favour of A6: 0 of 8.

| Subset | k = 1 | k = 2 | k = 3 | k = 5 | irr 1–5 | irr 1–10 |
|---|---|---|---|---|---|---|
| FD001 | −1.08 [−2.24, +0.01]; 51/100; p = 0.29 | −1.20 [−2.39, −0.03]; 57/100; p = 0.038 | −1.84 [−3.21, −0.53]; 66/100; p = 0.0011 | −1.69 [−3.20, −0.30]; 58/100; p = 0.045; Holm 0.045 | −1.99 [−3.20, −0.82]; 59/100; p = 0.0032; Holm 0.0065 | −3.22 [−4.77, −1.70]; 67/100; p = 0.00019 |
| FD002 | −1.41 [−2.20, −0.62]; 144/259; p = 0.00091 | −2.70 [−3.79, −1.62]; 153/259; p = 2.6e-06 | −2.83 [−4.05, −1.62]; 155/259; p = 5e-06 | −5.94 [−7.35, −4.58]; 183/259; p = 3.6e-15; Holm 2.9e-14 | −4.08 [−5.32, −2.87]; 166/259; p = 1.3e-11; Holm 7.8e-11 | −5.86 [−7.32, −4.45]; 180/259; p = 3.8e-14 |
| FD003 | −0.93 [−1.86, −0.10]; 54/100; p = 0.21 | −2.23 [−3.63, −0.99]; 56/100; p = 0.021 | −2.07 [−3.27, −0.99]; 60/100; p = 0.00029 | −1.79 [−2.95, −0.57]; 65/100; p = 6.9e-05; Holm 0.00028 | −2.12 [−3.36, −0.97]; 65/100; p = 0.00033; Holm 0.00099 | −2.35 [−3.57, −1.17]; 68/100; p = 4.5e-05 |
| FD004 | −2.07 [−2.85, −1.32]; 151/248; p = 3.8e-06 | −3.51 [−4.50, −2.54]; 160/248; p = 3.3e-11 | −4.26 [−5.28, −3.29]; 174/248; p = 3.1e-15 | −4.59 [−5.92, −3.33]; 169/248; p = 9.2e-13; Holm 6.4e-12 | −3.77 [−4.94, −2.65]; 168/248; p = 3.6e-11; Holm 1.8e-10 | −4.21 [−5.37, −3.09]; 163/248; p = 2.1e-12 |

**C2: A8 versus A6S (sparsification, A8's span and padding).** Holm-significant in favour of A8: 6 of 8; in favour of A6S: 0 of 8.

| Subset | k = 1 | k = 2 | k = 3 | k = 5 | irr 1–5 | irr 1–10 |
|---|---|---|---|---|---|---|
| FD001 | +0.17 [−1.59, +1.83]; 51/100; p = 0.89 | −3.18 [−5.16, −1.28]; 59/100; p = 0.0036 | −2.12 [−4.02, −0.32]; 55/100; p = 0.11 | −3.77 [−5.55, −2.12]; 68/100; p = 3.1e-05; Holm 0.00012 | −3.50 [−5.60, −1.58]; 65/100; p = 0.0014; Holm 0.0043 | −3.69 [−5.65, −1.84]; 69/100; p = 3.5e-05 |
| FD002 | −2.00 [−2.89, −1.15]; 146/259; p = 0.00014 | −2.75 [−3.71, −1.86]; 161/259; p = 9.2e-07 | −3.61 [−4.64, −2.59]; 170/259; p = 1.8e-11 | −4.84 [−6.05, −3.68]; 180/259; p = 7.3e-16; Holm 5.9e-15 | −3.56 [−4.62, −2.55]; 175/259; p = 2.5e-11; Holm 1.3e-10 | −5.80 [−7.19, −4.48]; 184/259; p = 3.5e-16 |
| FD003 | −0.42 [−1.41, +0.62]; 56/100; p = 0.26 | −0.90 [−1.99, +0.21]; 59/100; p = 0.028 | −1.19 [−2.21, −0.22]; 56/100; p = 0.029 | −0.64 [−2.01, +0.80]; 55/100; p = 0.31; Holm 0.61 | −0.55 [−1.66, +0.69]; 49/100; p = 0.33; Holm 0.61 | −1.38 [−2.74, +0.09]; 58/100; p = 0.018 |
| FD004 | −0.88 [−1.68, −0.09]; 138/248; p = 0.028 | −3.91 [−5.08, −2.78]; 158/248; p = 2.1e-10 | −4.19 [−5.41, −2.98]; 172/248; p = 1.3e-12 | −4.69 [−6.05, −3.39]; 174/248; p = 1.6e-14; Holm 1.1e-13 | −4.41 [−5.68, −3.22]; 174/248; p = 7e-13; Holm 4.2e-12 | −5.08 [−6.62, −3.61]; 165/248; p = 3.6e-11 |

**C3: A6S versus A6 (short padded windows, no sparsification).** Holm-significant in favour of A6S: 0 of 8; in favour of A6: 0 of 8.

| Subset | k = 1 | k = 2 | k = 3 | k = 5 | irr 1–5 | irr 1–10 |
|---|---|---|---|---|---|---|
| FD001 | −0.87 [−2.45, +0.76]; 50/100; p = 0.28 | +1.21 [−0.80, +3.32]; 48/100; p = 0.44 | −0.24 [−2.17, +1.74]; 54/100; p = 0.49 | +1.36 [−0.88, +3.60]; 41/100; p = 0.071; Holm 0.42 | +1.09 [−0.98, +3.30]; 52/100; p = 0.78; Holm 1 | +0.36 [−1.82, +2.58]; 54/100; p = 0.89 |
| FD002 | +0.78 [−0.34, +1.89]; 112/259; p = 0.012 | −0.25 [−1.52, +1.03]; 113/259; p = 0.11 | +0.38 [−0.84, +1.52]; 111/259; p = 0.031 | −1.60 [−3.28, +0.07]; 134/259; p = 0.23; Holm 1 | −0.22 [−1.48, +1.04]; 124/259; p = 0.6; Holm 1 | −0.33 [−1.80, +1.13]; 132/259; p = 0.83 |
| FD003 | −0.20 [−1.22, +0.78]; 53/100; p = 0.97 | −0.83 [−2.55, +0.75]; 46/100; p = 0.8 | −0.01 [−1.41, +1.38]; 54/100; p = 0.75 | −0.54 [−1.96, +1.01]; 56/100; p = 0.031; Holm 0.25 | −1.50 [−2.93, −0.10]; 57/100; p = 0.039; Holm 0.27 | −0.77 [−2.35, +0.79]; 52/100; p = 0.25 |
| FD004 | −0.96 [−1.91, −0.07]; 115/248; p = 0.5 | +0.28 [−0.82, +1.38]; 114/248; p = 0.56 | −0.32 [−1.69, +0.98]; 124/248; p = 0.54 | +0.19 [−1.38, +1.62]; 118/248; p = 0.42; Holm 1 | −0.10 [−1.38, +1.18]; 112/248; p = 0.65; Holm 1 | +0.68 [−0.72, +2.12]; 117/248; p = 0.57 |

**C4: A8F versus A8 (full span vs short span, both sparsified).** Holm-significant in favour of A8F: 0 of 8; in favour of A8: 0 of 8.

| Subset | k = 1 | k = 2 | k = 3 | k = 5 | irr 1–5 | irr 1–10 |
|---|---|---|---|---|---|---|
| FD001 | −0.37 [−1.63, +0.84]; 50/100; p = 0.82 | +0.77 [−0.20, +1.73]; 45/100; p = 0.1 | +0.52 [−0.29, +1.35]; 42/100; p = 0.074 | +0.72 [−0.21, +1.70]; 47/100; p = 0.36; Holm 1 | +0.43 [−0.54, +1.37]; 45/100; p = 0.11; Holm 0.78 | +0.12 [−0.94, +1.12]; 47/100; p = 0.34 |
| FD002 | −0.18 [−1.05, +0.71]; 155/259; p = 0.04 | +0.31 [−0.41, +1.03]; 142/259; p = 0.54 | +0.40 [−0.23, +1.07]; 131/259; p = 0.65 | +0.50 [−0.19, +1.20]; 131/259; p = 0.57; Holm 1 | −0.30 [−1.03, +0.44]; 130/259; p = 0.85; Holm 1 | +0.27 [−0.32, +0.87]; 140/259; p = 0.53 |
| FD003 | −0.32 [−1.23, +0.66]; 60/100; p = 0.2 | −0.49 [−1.26, +0.24]; 57/100; p = 0.16 | −0.86 [−1.66, −0.12]; 55/100; p = 0.035 | −0.61 [−1.28, +0.07]; 61/100; p = 0.032; Holm 0.26 | −0.06 [−0.80, +0.75]; 54/100; p = 0.51; Holm 1 | −0.20 [−1.01, +0.60]; 55/100; p = 0.45 |
| FD004 | −0.23 [−1.05, +0.58]; 136/248; p = 0.22 | +0.13 [−0.48, +0.73]; 134/248; p = 0.65 | +0.25 [−0.41, +0.96]; 123/248; p = 0.84 | −0.09 [−0.74, +0.58]; 125/248; p = 0.48; Holm 1 | +0.75 [+0.07, +1.45]; 128/248; p = 0.53; Holm 1 | +0.19 [−0.42, +0.79]; 131/248; p = 0.82 |

**Complete records (k = 1) against the dense model A1:** FD001: A8F −1.34 [−3.42, +0.59], A6S −1.13 [−2.78, +0.39]; FD002: A8F −3.24 [−4.35, −2.11], A6S −1.05 [−2.13, +0.00]; FD003: A8F −0.90 [−2.42, +0.57], A6S −0.16 [−1.23, +0.89]; FD004: A8F −3.22 [−4.36, −2.08], A6S −2.11 [−3.19, −1.06].

Pre-specified reading: sparsification carries the gain (C1 8/8, C2 6/8, C3 0/8).

## Table S21. External cohort N-CMAPSS DS03–DS08: fixed split, fixed models (27 test units, 19 groups, five seeds)

Mean unit RMSE in cycles (unit-weighted).

| Case | Scenario | A1 | A2 | A3 | A4 | A5 | A6 | A8 | A8B |
|---|---|---|---|---|---|---|---|---|---|
| 1 | k = 1 | 13.78 | 13.78 | 13.78 | 13.04 | 12.72 | 12.25 | 12.71 | 13.04 |
| 1 | k = 5 | 16.56 | 19.44 | 19.70 | 10.54 | 8.59 | 23.02 | 10.63 | 10.40 |
| 1 | irr 1–5 | 15.18 | 18.53 | 18.36 | 10.35 | 9.42 | 20.04 | 10.20 | 10.14 |
| 1 | block 5 | 14.57 | 18.02 | 18.78 | 12.75 | 12.27 | 12.83 | 11.84 | 12.00 |
| 1 | block 10 | 15.06 | 19.61 | 20.97 | 11.89 | 11.88 | 14.47 | 11.18 | 11.03 |

| Case | History | S1 | S2 | S3 | S4 | S6 | S8 |
|---|---|---|---|---|---|---|---|
| 2 | complete | 13.78 | 13.78 | 12.27 | 11.76 | 12.25 | 12.17 |
| 2 | last 5 | 17.65 | 13.71 | 12.74 | 12.14 | 26.50 | 14.87 |
| 2 | last 3 | 19.92 | 14.35 | 13.08 | 12.62 | 27.36 | 15.70 |

## Table S22. External cohort: tests

Δ: mean paired difference of group RMSE (arm minus reference) [95% bootstrap CI]; groups better; Wilcoxon p; Holm within family; Δ per seed.

| Hypothesis | Scenario | Arm | Reference | Δ | Δ per seed |
|---|---|---|---|---|---|
| E1 (confirmatory) | k = 5 | A5 | A1 | −8.21 [−11.25, −5.24]; 18/19; p = 7.2e-05; Holm 0.00011 | −10.13, −7.02, −8.32, −6.23, −9.36 |
| E1 (confirmatory) | irr 1–5 | A5 | A1 | −5.88 [−8.13, −3.75]; 17/19; p = 5.3e-05; Holm 0.00011 | −7.76, −4.30, −7.60, −2.98, −6.79 |
| E2 (confirmatory) | h5 | S4 | S2 | −1.09 [−2.17, +0.04]; 14/19; p = 0.049; Holm 0.065 | −1.09, −0.34, −2.96, −0.81, −0.23 |
| E2 (confirmatory) | h3 | S4 | S2 | −1.13 [−2.20, +0.03]; 14/19; p = 0.032; Holm 0.065 | −0.59, −0.93, −3.02, −1.05, −0.08 |
| secondary | k = 5 | A8 | A1 | −6.12 [−9.03, −3.21]; 16/19; p = 0.00064; Holm 0.0013 | −8.16, −6.13, −5.04, −4.32, −6.97 |
| secondary | irr 1–5 | A8 | A1 | −5.01 [−7.44, −2.76]; 16/19; p = 0.00097; Holm 0.0013 | −7.00, −4.21, −4.92, −2.97, −5.96 |
| secondary | h5 | S8 | S2 | +1.40 [+0.28, +2.50]; 6/19; p = 0.04; Holm 0.052 | +1.37, +2.04, +0.70, +1.28, +1.59 |
| secondary | h3 | S8 | S2 | +1.74 [+0.36, +3.08]; 6/19; p = 0.026; Holm 0.052 | +2.63, +2.00, +0.75, +1.38, +1.92 |
| block outage | blk5 | A5 | A1 | −1.70 [−2.66, −0.66]; 17/19; p = 0.0039; Holm 0.0039 | −2.49, −0.45, −2.02, −1.56, −2.00 |
| block outage | blk10 | A5 | A1 | −2.49 [−3.55, −1.39]; 17/19; p = 0.0012; Holm 0.0023 | −3.58, −1.14, −2.81, −1.89, −3.01 |
| block outage | blk5 | A8 | A1 | −2.41 [−4.19, −0.60]; 14/19; p = 0.023; Holm 0.023 | −3.59, −2.03, −2.46, −1.60, −2.35 |
| block outage | blk10 | A8 | A1 | −3.39 [−5.04, −1.71]; 16/19; p = 0.002; Holm 0.004 | −4.63, −2.47, −3.95, −2.09, −3.79 |
| E3 cost, complete records | k1 | A5 | A1 | −0.69 [−1.71, +0.52]; 14/19; p = 0.08; non-inferior (1 cycle): yes | |
| E3 cost, complete records | full | S4 | S1 | −1.65 [−2.47, −0.83]; 17/19; p = 0.0014; non-inferior (1 cycle): yes | |
| E3 cost, complete records | k1 | A8 | A1 | −1.07 [−3.06, +0.72]; 10/19; p = 0.47; non-inferior (1 cycle): yes | |
| E3 cost, complete records | full | S8 | S1 | −1.47 [−2.31, −0.65]; 15/19; p = 0.0082; non-inferior (1 cycle): yes | |
| reference trained with outages | blk5 | A8B | A8 | +0.31 [−0.02, +0.64]; 7/19; p = 0.096 | |
| reference trained with outages | blk10 | A8B | A8 | −0.04 [−0.38, +0.31]; 11/19; p = 0.62 | |
| reference trained with outages | k = 5 | A8B | A8 | −0.10 [−0.54, +0.36]; 11/19; p = 0.65 | |
| reference trained with outages | k1 | A8B | A8 | +0.49 [+0.12, +0.88]; 4/19; p = 0.026 | |

E1 confirmed: True. E2 confirmed: False.

## Table S23. C-MAPSS, missingness mechanisms not seen in training: RMSE (cycles), mean ± s.d. over five seeds

Block: the last 5 cycles recorded, the 10 or 20 cycles before them missing. Regime: cycles in the three highest operating regimes missing with probability 0.9, others 0.1 (median number of records in the last column).

| Subset | Scenario | A1 | A2 | A3 | A5 | A6 | A8 | A8B | Records |
|---|---|---|---|---|---|---|---|---|---|
| FD001 | k1 | 16.04 ± 0.39 | 16.04 ± 0.39 | 16.04 ± 0.39 | 14.71 ± 0.69 | 15.74 ± 0.82 | 14.26 ± 1.55 | 13.46 ± 1.00 | 133 |
| FD001 | blk10 | 17.14 ± 0.65 | 19.03 ± 0.49 | 21.93 ± 0.53 | 14.48 ± 0.61 | 16.66 ± 0.69 | 13.56 ± 1.03 | 13.16 ± 0.51 | 123 |
| FD001 | blk20 | 18.91 ± 0.69 | 22.69 ± 0.31 | 24.59 ± 0.75 | 14.10 ± 0.42 | 16.59 ± 0.67 | 12.65 ± 1.16 | 12.60 ± 0.58 | 113 |
| FD002 | k1 | 17.50 ± 0.36 | 17.50 ± 0.36 | 17.50 ± 0.36 | 14.87 ± 0.41 | 15.66 ± 0.65 | 12.79 ± 0.97 | 12.26 ± 0.49 | 132 |
| FD002 | blk10 | 18.35 ± 0.45 | 20.56 ± 0.91 | 22.64 ± 0.57 | 14.88 ± 0.50 | 16.19 ± 0.59 | 13.59 ± 0.40 | 13.47 ± 0.28 | 122 |
| FD002 | blk20 | 18.76 ± 0.86 | 21.03 ± 1.00 | 25.61 ± 0.70 | 15.35 ± 0.69 | 17.82 ± 0.67 | 15.06 ± 0.42 | 14.79 ± 0.53 | 112 |
| FD002 | reg | 18.69 ± 0.33 | 19.40 ± 0.39 | 20.81 ± 0.67 | 13.04 ± 0.45 | 19.46 ± 0.58 | 12.70 ± 0.25 | 12.47 ± 0.34 | 63 |
| FD003 | k1 | 13.27 ± 0.76 | 13.27 ± 0.76 | 13.27 ± 0.76 | 14.87 ± 0.58 | 13.27 ± 0.92 | 12.10 ± 0.97 | 11.78 ± 0.86 | 148 |
| FD003 | blk10 | 14.97 ± 0.44 | 16.25 ± 0.73 | 18.60 ± 0.95 | 15.31 ± 0.42 | 14.59 ± 0.90 | 13.50 ± 0.75 | 13.11 ± 0.84 | 138 |
| FD003 | blk20 | 18.94 ± 0.83 | 17.62 ± 1.08 | 20.45 ± 1.57 | 18.51 ± 1.10 | 15.34 ± 0.82 | 13.29 ± 0.57 | 12.75 ± 0.77 | 128 |
| FD004 | k1 | 17.70 ± 0.70 | 17.70 ± 0.70 | 17.70 ± 0.70 | 15.49 ± 0.75 | 16.74 ± 0.86 | 13.45 ± 0.65 | 13.98 ± 0.57 | 153 |
| FD004 | blk10 | 17.84 ± 0.17 | 21.00 ± 0.89 | 22.46 ± 1.05 | 16.28 ± 1.01 | 17.10 ± 1.17 | 14.08 ± 0.48 | 14.33 ± 0.27 | 143 |
| FD004 | blk20 | 19.12 ± 0.73 | 23.10 ± 0.82 | 27.94 ± 1.66 | 17.21 ± 1.34 | 18.74 ± 0.62 | 14.91 ± 0.22 | 14.77 ± 0.24 | 133 |
| FD004 | reg | 22.06 ± 1.10 | 20.01 ± 1.01 | 19.41 ± 0.93 | 14.43 ± 0.39 | 19.19 ± 1.83 | 13.75 ± 0.28 | 13.49 ± 0.28 | 71 |

## Table S24. C-MAPSS, unseen mechanisms: degraded-training arms against the best test-time remedy

Δ: seed-averaged engine absolute error, arm minus best of A1/A2/A3 (by RMSE) [95% CI]; engines better; Wilcoxon p; Holm within the arm's family (8 block comparisons; 2 regime comparisons).

| Arm | Subset | Scenario | Reference | Δ |
|---|---|---|---|---|
| A5 | FD001 | blk10 | A1 | −1.92 [−3.41, −0.53]; 58/100; p = 0.048; Holm 0.14 |
| A5 | FD001 | blk20 | A1 | −4.13 [−5.93, −2.44]; 66/100; p = 4.8e-05; Holm 0.00033 |
| A5 | FD002 | blk10 | A1 | −2.14 [−3.04, −1.26]; 148/259; p = 0.00029; Holm 0.0018 |
| A5 | FD002 | blk20 | A1 | −2.47 [−3.43, −1.51]; 165/259; p = 3.5e-06; Holm 2.8e-05 |
| A5 | FD003 | blk10 | A1 | −0.90 [−2.25, +0.45]; 54/100; p = 0.33; Holm 0.65 |
| A5 | FD003 | blk20 | A2 | +0.26 [−2.06, +2.57]; 42/100; p = 0.52; Holm 0.65 |
| A5 | FD004 | blk10 | A1 | −1.15 [−2.02, −0.30]; 134/248; p = 0.028; Holm 0.11 |
| A5 | FD004 | blk20 | A1 | −1.77 [−2.99, −0.56]; 140/248; p = 0.0057; Holm 0.029 |
| A5 | FD002 | reg | A1 | −3.81 [−4.86, −2.85]; 173/259; p = 9e-11; Holm 1.8e-10 |
| A5 | FD004 | reg | A3 | −3.65 [−4.84, −2.47]; 163/248; p = 7.6e-10; Holm 7.6e-10 |
| A8 | FD001 | blk10 | A1 | −2.25 [−3.99, −0.55]; 63/100; p = 0.0077; Holm 0.015 |
| A8 | FD001 | blk20 | A1 | −4.58 [−6.50, −2.74]; 71/100; p = 1.8e-05; Holm 0.00011 |
| A8 | FD002 | blk10 | A1 | −2.55 [−3.63, −1.49]; 149/259; p = 0.00047; Holm 0.0024 |
| A8 | FD002 | blk20 | A1 | −2.16 [−3.41, −0.95]; 149/259; p = 0.0021; Holm 0.0074 |
| A8 | FD003 | blk10 | A1 | −2.00 [−3.53, −0.47]; 56/100; p = 0.048; Holm 0.048 |
| A8 | FD003 | blk20 | A2 | −3.35 [−5.34, −1.50]; 63/100; p = 0.0018; Holm 0.0074 |
| A8 | FD004 | blk10 | A1 | −2.75 [−3.71, −1.78]; 173/248; p = 3e-10; Holm 2.4e-09 |
| A8 | FD004 | blk20 | A1 | −3.12 [−4.24, −2.03]; 156/248; p = 5e-07; Holm 3.5e-06 |
| A8 | FD002 | reg | A1 | −4.25 [−5.29, −3.29]; 178/259; p = 2.8e-14; Holm 4.2e-14 |
| A8 | FD004 | reg | A3 | −4.31 [−5.48, −3.17]; 180/248; p = 2.1e-14; Holm 4.2e-14 |

A5: C-MAPSS block 4/8 significantly better (0 worse); regime 2/2; DS03–DS08 block 2/2. Pre-specified reading 'remains better under an unseen mechanism': False.

A8: C-MAPSS block 8/8 significantly better (0 worse); regime 2/2; DS03–DS08 block 2/2. Pre-specified reading 'remains better under an unseen mechanism': True.

A8B (trained with outages) minus A8, C-MAPSS block scenarios: FD001 blk10 −0.26 (p = 0.49); FD001 blk20 −0.03 (p = 0.81); FD002 blk10 −0.19 (p = 0.52); FD002 blk20 −0.11 (p = 0.38); FD003 blk10 −0.19 (p = 0.16); FD003 blk20 −0.21 (p = 0.31); FD004 blk10 +0.37 (p = 0.0054); FD004 blk20 −0.04 (p = 0.86).

## Table S25. Padding-shortcut experiment: mean signed error (cycles) near end of life with short histories

C-MAPSS: test engines with true RUL ≤ 50, five seeds averaged. DS03–DS08: predictions with true RUL ≤ 20, unit means averaged within groups. S3E: only windows with RUL above the threshold truncated in training; S3L: only windows at or below it.

| Data | History | n | S1 | S3E | S3 | S3L | S3E − S3L [95% CI]; p; Holm |
|---|---|---|---|---|---|---|---|
| FD001 | last 10 | 33 | +18.7 | +17.0 | +6.3 | +4.2 | +12.77 [+9.10, +16.85]; p = 5.8e-09; Holm 1.7e-08 |
| FD001 | last 5 | 33 | +14.9 | +14.7 | +5.5 | +3.5 | +11.11 [+7.42, +15.03]; p = 5.5e-07; Holm 5.5e-07 |
| FD002 | last 10 | 88 | +11.0 | +16.4 | +3.6 | +2.7 | +13.75 [+10.82, +16.76]; p = 1.2e-13; Holm 7.1e-13 |
| FD002 | last 5 | 88 | +9.2 | +15.2 | +2.5 | +2.4 | +12.75 [+9.91, +15.65]; p = 3e-12; Holm 1.5e-11 |
| FD003 | last 10 | 29 | +25.1 | +20.7 | +6.2 | +3.6 | +17.07 [+13.40, +20.77]; p = 3.7e-09; Holm 1.5e-08 |
| FD003 | last 5 | 29 | +31.2 | +24.3 | +8.5 | +4.3 | +19.98 [+15.28, +24.62]; p = 1.1e-08; Holm 2.2e-08 |
| FD004 | last 10 | 80 | +18.4 | +34.6 | +7.6 | +3.3 | +31.29 [+26.30, +36.40]; p = 7.8e-15; Holm 6.3e-14 |
| FD004 | last 5 | 80 | +17.0 | +32.6 | +7.8 | +4.1 | +28.56 [+23.59, +33.57]; p = 1.1e-14; Holm 8e-14 |
| DS03–DS08 | last 5 | 19 | +12.6 | +13.8 | +8.5 | +7.5 | +6.33 [+4.39, +8.51]; p = 3.8e-06; Holm 7.6e-06 |
| DS03–DS08 | last 3 | 19 | +13.7 | +14.7 | +8.5 | +6.8 | +7.90 [+5.61, +10.45]; p = 3.8e-06; Holm 7.6e-06 |

S3E − S3L positive and Holm-significant: C-MAPSS 8/8, DS03–DS08 2/2; ordering S3E > S3 > S3L in 10/10. Pre-specified reading 'shortcut hypothesis supported': True.

RMSE of the mechanism arms (C-MAPSS, last 5 cycles / complete): FD001 S1 26.3/16.0, S3E 21.2/15.8, S3 17.6/14.8, S3L 24.4/15.6; FD002 S1 24.0/17.5, S3E 20.8/17.6, S3 17.4/17.8, S3L 30.0/18.5; FD003 S1 35.8/13.3, S3E 26.2/13.5, S3 20.4/13.9, S3L 19.9/13.9; FD004 S1 27.2/17.7, S3E 28.8/16.9, S3 20.4/17.5, S3L 27.8/20.3.

## Table S26. Other backbones, TCN: RMSE (cycles) and comparisons

C-MAPSS: mean ± s.d. over five seeds. DS03–DS08: mean unit RMSE, fixed models, five seeds.

| Data | Scenario | A1 | A2 | A3 | A5 | A6 | A8 |
|---|---|---|---|---|---|---|---|
| FD001 | k = 1 | 13.54 ± 0.65 | 13.54 ± 0.65 | 13.54 ± 0.65 | 15.19 ± 0.93 | 15.97 ± 0.90 | 14.12 ± 1.13 |
| FD001 | k = 5 | 27.21 ± 2.97 | 20.34 ± 0.85 | 21.07 ± 0.57 | 14.59 ± 0.25 | 18.21 ± 2.05 | 15.20 ± 0.70 |
| FD001 | irr 1–5 | 25.63 ± 1.50 | 17.06 ± 0.79 | 17.88 ± 1.20 | 13.69 ± 0.55 | 16.75 ± 1.41 | 13.37 ± 0.17 |
| FD002 | k = 1 | 15.69 ± 0.88 | 15.69 ± 0.88 | 15.69 ± 0.88 | 14.72 ± 0.54 | 17.93 ± 0.50 | 16.63 ± 1.29 |
| FD002 | k = 5 | 20.99 ± 0.49 | 20.53 ± 0.43 | 21.97 ± 0.46 | 13.81 ± 0.44 | 19.59 ± 0.25 | 13.82 ± 0.22 |
| FD002 | irr 1–5 | 18.73 ± 0.78 | 19.20 ± 0.62 | 20.14 ± 0.84 | 13.28 ± 0.49 | 18.68 ± 1.23 | 13.58 ± 0.39 |
| FD003 | k = 1 | 13.17 ± 0.49 | 13.17 ± 0.49 | 13.17 ± 0.49 | 16.35 ± 0.88 | 14.71 ± 1.31 | 13.79 ± 0.71 |
| FD003 | k = 5 | 33.94 ± 2.10 | 16.84 ± 0.79 | 17.95 ± 0.53 | 16.66 ± 0.21 | 17.47 ± 1.48 | 15.37 ± 0.64 |
| FD003 | irr 1–5 | 25.85 ± 1.61 | 16.83 ± 0.40 | 18.19 ± 0.50 | 14.18 ± 0.26 | 16.57 ± 2.07 | 14.61 ± 0.76 |
| FD004 | k = 1 | 15.57 ± 0.45 | 15.57 ± 0.45 | 15.57 ± 0.45 | 15.49 ± 0.44 | 16.15 ± 0.75 | 15.55 ± 1.54 |
| FD004 | k = 5 | 28.10 ± 1.41 | 19.77 ± 1.04 | 20.11 ± 0.92 | 15.10 ± 0.43 | 21.13 ± 1.37 | 15.61 ± 0.31 |
| FD004 | irr 1–5 | 23.86 ± 1.44 | 19.72 ± 0.81 | 19.98 ± 0.85 | 14.31 ± 0.28 | 19.20 ± 1.05 | 14.43 ± 0.38 |
| DS03–DS08 | k = 1 | 14.27 | 14.27 | 14.27 | 14.40 | 10.85 | 14.54 |
| DS03–DS08 | k = 5 | 16.49 | 19.45 | 19.59 | 9.08 | 16.88 | 10.94 |
| DS03–DS08 | irr 1–5 | 14.64 | 17.75 | 17.29 | 11.05 | 13.97 | 11.52 |

| Data | History | S1 | S2 | S4 |
|---|---|---|---|---|
| FD001 | complete | 13.54 ± 0.65 | 13.54 ± 0.65 | 15.03 ± 0.68 |
| FD001 | last 10 | 27.73 ± 1.89 | 25.69 ± 1.46 | 19.31 ± 1.04 |
| FD001 | last 5 | 28.43 ± 1.98 | 25.27 ± 1.06 | 18.61 ± 0.42 |
| FD002 | complete | 15.69 ± 0.88 | 15.67 ± 0.86 | 15.61 ± 0.19 |
| FD002 | last 10 | 26.25 ± 1.26 | 24.12 ± 1.07 | 17.10 ± 0.60 |
| FD002 | last 5 | 28.19 ± 1.33 | 19.94 ± 0.71 | 16.71 ± 0.47 |
| FD003 | complete | 13.17 ± 0.49 | 13.17 ± 0.49 | 15.71 ± 0.93 |
| FD003 | last 10 | 35.49 ± 0.90 | 42.45 ± 5.42 | 21.49 ± 0.95 |
| FD003 | last 5 | 42.83 ± 2.11 | 28.22 ± 1.81 | 20.70 ± 2.38 |
| FD004 | complete | 15.57 ± 0.45 | 16.20 ± 0.46 | 15.90 ± 0.32 |
| FD004 | last 10 | 27.08 ± 1.82 | 29.29 ± 1.75 | 19.54 ± 0.23 |
| FD004 | last 5 | 28.03 ± 2.15 | 21.95 ± 1.11 | 19.67 ± 0.47 |
| DS03–DS08 | complete | 14.27 | 14.27 | 13.96 |
| DS03–DS08 | last 5 | 18.20 | 13.72 | 13.79 |
| DS03–DS08 | last 3 | 20.72 | 14.29 | 13.89 |

**TCN: comparisons**

Δ: arm minus reference; C-MAPSS seed-averaged engine absolute error, DS03–DS08 group RMSE; [95% CI]; units better; Wilcoxon p; Holm within family.

| Comparison | Data | Scenario | Arm | Reference | Δ |
|---|---|---|---|---|---|
| G1 | FD001 | k = 5 | A5 | A2 | −3.34 [−5.58, −1.24]; 53/100; p = 0.061; Holm 0.18 |
| G1 | FD001 | irr 1–5 | A5 | A2 | −2.47 [−4.58, −0.45]; 56/100; p = 0.038; Holm 0.15 |
| G1 | FD002 | k = 5 | A5 | A2 | −4.39 [−5.83, −2.96]; 162/259; p = 1e-08; Holm 6e-08 |
| G1 | FD002 | irr 1–5 | A5 | A1 | −3.96 [−5.06, −2.88]; 175/259; p = 6.3e-12; Holm 5e-11 |
| G1 | FD003 | k = 5 | A5 | A2 | −1.14 [−3.25, +0.91]; 54/100; p = 0.21; Holm 0.43 |
| G1 | FD003 | irr 1–5 | A5 | A2 | −1.33 [−3.44, +0.59]; 53/100; p = 0.34; Holm 0.43 |
| G1 | FD004 | k = 5 | A5 | A2 | −3.39 [−4.80, −2.02]; 152/248; p = 7.9e-06; Holm 3.9e-05 |
| G1 | FD004 | irr 1–5 | A5 | A2 | −3.68 [−5.03, −2.43]; 158/248; p = 6.8e-09; Holm 4.8e-08 |
| G1 | DS03–DS08 | k = 5 | A5 | A1 | −6.99 [−9.67, −4.18]; 17/19; p = 0.00027; Holm 0.00053 |
| G1 | DS03–DS08 | irr 1–5 | A5 | A1 | −3.33 [−5.30, −1.48]; 14/19; p = 0.0095; Holm 0.0095 |
| G2 | FD001 | k = 5 | A8 | A6 | −2.54 [−3.85, −1.23]; 67/100; p = 0.00018; Holm 0.00054 |
| G2 | FD001 | irr 1–5 | A8 | A6 | −2.61 [−3.89, −1.40]; 68/100; p = 9.5e-06; Holm 3.8e-05 |
| G2 | FD002 | k = 5 | A8 | A6 | −3.54 [−4.87, −2.30]; 160/259; p = 1.8e-07; Holm 1.1e-06 |
| G2 | FD002 | irr 1–5 | A8 | A6 | −2.80 [−3.93, −1.74]; 153/259; p = 5.5e-06; Holm 2.8e-05 |
| G2 | FD003 | k = 5 | A8 | A6 | −1.63 [−2.92, −0.36]; 52/100; p = 0.061; Holm 0.12 |
| G2 | FD003 | irr 1–5 | A8 | A6 | −1.03 [−2.36, +0.30]; 55/100; p = 0.15; Holm 0.15 |
| G2 | FD004 | k = 5 | A8 | A6 | −4.45 [−5.83, −3.06]; 165/248; p = 4.4e-10; Holm 3.1e-09 |
| G2 | FD004 | irr 1–5 | A8 | A6 | −3.69 [−4.81, −2.60]; 172/248; p = 6.1e-12; Holm 4.9e-11 |
| G2 | DS03–DS08 | k = 5 | A8 | A6 | −5.86 [−8.11, −3.45]; 18/19; p = 0.00021; Holm 0.00042 |
| G2 | DS03–DS08 | irr 1–5 | A8 | A6 | −2.70 [−5.18, −0.19]; 12/19; p = 0.08; Holm 0.08 |
| G3 | FD001 | last 10 | S4 | S2 | −6.43 [−8.56, −4.25]; 80/100; p = 2.6e-08; Holm 1.1e-07 |
| G3 | FD001 | last 5 | S4 | S2 | −6.40 [−8.19, −4.57]; 82/100; p = 4.6e-10; Holm 2.3e-09 |
| G3 | FD002 | last 10 | S4 | S2 | −5.04 [−6.55, −3.54]; 176/259; p = 3.1e-10; Holm 1.9e-09 |
| G3 | FD002 | last 5 | S4 | S2 | −1.79 [−2.79, −0.79]; 153/259; p = 0.0016; Holm 0.0032 |
| G3 | FD003 | last 10 | S4 | S1 | −13.09 [−16.50, −9.73]; 78/100; p = 3.9e-11; Holm 2.7e-10 |
| G3 | FD003 | last 5 | S4 | S2 | −7.73 [−11.48, −4.04]; 73/100; p = 8.9e-06; Holm 2.7e-05 |
| G3 | FD004 | last 10 | S4 | S1 | −5.70 [−7.46, −3.97]; 174/248; p = 3.3e-11; Holm 2.6e-10 |
| G3 | FD004 | last 5 | S4 | S2 | −1.17 [−2.12, −0.23]; 135/248; p = 0.016; Holm 0.016 |
| G3 | DS03–DS08 | last 5 | S4 | S2 | −0.09 [−0.93, +0.65]; 7/19; p = 0.59; Holm 1 |
| G3 | DS03–DS08 | last 3 | S4 | S2 | −0.18 [−1.17, +0.80]; 12/19; p = 0.71; Holm 1 |

Complete records: FD001 A5 vs A1 +1.38 [+0.42, +2.38] (p = 0.014); FD001 S4 vs S1 +0.88 [+0.07, +1.73] (p = 0.056); FD002 A5 vs A1 −0.15 [−0.82, +0.52] (p = 0.95); FD002 S4 vs S1 +0.45 [−0.19, +1.12] (p = 0.042); FD003 A5 vs A1 +3.14 [+1.83, +4.49] (p = 1e-06); FD003 S4 vs S1 +2.26 [+1.11, +3.43] (p = 9.3e-06); FD004 A5 vs A1 +0.38 [−0.21, +0.95] (p = 0.046); FD004 S4 vs S1 +0.45 [−0.15, +1.05] (p = 0.17); DS03–DS08 A5 vs A1 +0.31 [−0.54, +1.43] (p = 0.57); DS03–DS08 S4 vs S1 −0.37 [−0.82, +0.09] (p = 0.14).

Pre-specified reading: G1 partly (C-MAPSS 4/8, DS03–DS08 2/2, significantly worse 0); G2 partly (C-MAPSS 6/8, DS03–DS08 1/2, significantly worse 0); G3 partly (C-MAPSS 8/8, DS03–DS08 0/2, significantly worse 0).

Selected configurations (width, learning rate): FD001: A1 (32, 0.0003), A5 (32, 0.0003), A6 (64, 0.0003), A8 (32, 0.0003), S4 (32, 0.0003); FD002: A1 (32, 0.0003), A5 (32, 0.0003), A6 (64, 0.0003), A8 (32, 0.0003), S4 (32, 0.0003); FD003: A1 (32, 0.0003), A5 (32, 0.0003), A6 (32, 0.001), A8 (32, 0.0003), S4 (32, 0.001); FD004: A1 (32, 0.0003), A5 (32, 0.0003), A6 (64, 0.001), A8 (32, 0.0003), S4 (32, 0.0003); ext: A1 (32, 0.0003), A5 (32, 0.0003), A6 (64, 0.001), A8 (32, 0.001), S4 (32, 0.001).

## Table S27. Other backbones, Transformer: RMSE (cycles) and comparisons

C-MAPSS: mean ± s.d. over five seeds. DS03–DS08: mean unit RMSE, fixed models, five seeds.

| Data | Scenario | A1 | A2 | A3 | A5 | A6 | A8 |
|---|---|---|---|---|---|---|---|
| FD001 | k = 1 | 14.73 ± 0.15 | 14.73 ± 0.15 | 14.73 ± 0.15 | 15.82 ± 1.01 | 15.28 ± 0.74 | 14.58 ± 0.78 |
| FD001 | k = 5 | 24.80 ± 0.85 | 19.31 ± 0.51 | 19.29 ± 0.71 | 13.32 ± 0.26 | 17.20 ± 1.38 | 15.25 ± 0.70 |
| FD001 | irr 1–5 | 22.69 ± 1.34 | 19.23 ± 0.68 | 19.73 ± 0.60 | 13.81 ± 0.42 | 15.12 ± 0.78 | 13.54 ± 0.42 |
| FD002 | k = 1 | 14.62 ± 0.32 | 14.62 ± 0.32 | 14.62 ± 0.32 | 14.47 ± 0.63 | 14.94 ± 0.44 | 13.59 ± 0.75 |
| FD002 | k = 5 | 19.78 ± 0.38 | 20.24 ± 0.82 | 21.20 ± 0.63 | 14.40 ± 0.33 | 18.92 ± 1.19 | 13.74 ± 0.30 |
| FD002 | irr 1–5 | 17.81 ± 0.71 | 18.43 ± 0.40 | 19.11 ± 0.40 | 12.99 ± 0.30 | 17.80 ± 0.69 | 13.31 ± 0.36 |
| FD003 | k = 1 | 14.37 ± 0.68 | 14.37 ± 0.68 | 14.37 ± 0.68 | 16.90 ± 2.03 | 13.84 ± 0.57 | 13.20 ± 0.53 |
| FD003 | k = 5 | 26.40 ± 0.97 | 18.54 ± 0.79 | 19.17 ± 1.11 | 15.90 ± 0.62 | 17.29 ± 0.64 | 14.54 ± 0.60 |
| FD003 | irr 1–5 | 20.64 ± 0.87 | 19.17 ± 1.05 | 19.36 ± 0.87 | 13.45 ± 0.40 | 15.62 ± 0.54 | 13.73 ± 0.54 |
| FD004 | k = 1 | 15.56 ± 0.19 | 15.56 ± 0.19 | 15.56 ± 0.19 | 15.92 ± 0.66 | 17.09 ± 1.13 | 14.41 ± 0.36 |
| FD004 | k = 5 | 26.39 ± 1.08 | 21.90 ± 0.57 | 22.49 ± 0.62 | 15.42 ± 0.41 | 20.37 ± 0.98 | 15.24 ± 0.32 |
| FD004 | irr 1–5 | 23.26 ± 1.00 | 20.00 ± 0.70 | 19.75 ± 0.77 | 14.63 ± 0.47 | 17.88 ± 1.53 | 14.40 ± 0.20 |
| DS03–DS08 | k = 1 | 13.06 | 13.06 | 13.06 | 13.36 | 12.74 | 11.47 |
| DS03–DS08 | k = 5 | 14.95 | 17.51 | 17.36 | 8.56 | 18.39 | 10.66 |
| DS03–DS08 | irr 1–5 | 13.56 | 16.22 | 15.85 | 9.70 | 15.06 | 10.27 |

| Data | History | S1 | S2 | S4 |
|---|---|---|---|---|
| FD001 | complete | 14.73 ± 0.15 | 14.73 ± 0.15 | 15.23 ± 0.74 |
| FD001 | last 10 | 29.94 ± 0.79 | 30.62 ± 2.56 | 20.10 ± 0.57 |
| FD001 | last 5 | 30.46 ± 1.24 | 31.67 ± 1.92 | 19.24 ± 0.72 |
| FD002 | complete | 14.62 ± 0.32 | 14.62 ± 0.33 | 14.78 ± 0.58 |
| FD002 | last 10 | 24.68 ± 0.63 | 24.15 ± 0.30 | 16.49 ± 0.39 |
| FD002 | last 5 | 28.05 ± 1.03 | 21.83 ± 0.34 | 16.57 ± 0.14 |
| FD003 | complete | 14.37 ± 0.68 | 14.37 ± 0.68 | 16.47 ± 1.25 |
| FD003 | last 10 | 36.00 ± 1.48 | 29.88 ± 1.52 | 21.25 ± 0.71 |
| FD003 | last 5 | 42.20 ± 1.38 | 28.41 ± 2.34 | 22.02 ± 0.57 |
| FD004 | complete | 15.56 ± 0.19 | 16.28 ± 0.22 | 16.59 ± 0.40 |
| FD004 | last 10 | 29.47 ± 1.06 | 30.78 ± 1.72 | 19.91 ± 0.57 |
| FD004 | last 5 | 32.71 ± 1.30 | 27.49 ± 2.33 | 19.97 ± 0.40 |
| DS03–DS08 | complete | 13.06 | 13.06 | 11.70 |
| DS03–DS08 | last 5 | 16.32 | 14.53 | 12.53 |
| DS03–DS08 | last 3 | 18.45 | 15.26 | 12.88 |

**Transformer: comparisons**

Δ: arm minus reference; C-MAPSS seed-averaged engine absolute error, DS03–DS08 group RMSE; [95% CI]; units better; Wilcoxon p; Holm within family.

| Comparison | Data | Scenario | Arm | Reference | Δ |
|---|---|---|---|---|---|
| G1 | FD001 | k = 5 | A5 | A3 | −4.74 [−7.02, −2.46]; 65/100; p = 0.0002; Holm 0.00063 |
| G1 | FD001 | irr 1–5 | A5 | A2 | −4.42 [−6.86, −2.11]; 62/100; p = 0.00073; Holm 0.0015 |
| G1 | FD002 | k = 5 | A5 | A1 | −4.05 [−5.21, −2.95]; 176/259; p = 1.9e-11; Holm 1.5e-10 |
| G1 | FD002 | irr 1–5 | A5 | A1 | −3.68 [−4.75, −2.62]; 174/259; p = 5.4e-10; Holm 3.2e-09 |
| G1 | FD003 | k = 5 | A5 | A2 | −2.02 [−4.17, +0.12]; 64/100; p = 0.022; Holm 0.022 |
| G1 | FD003 | irr 1–5 | A5 | A2 | −4.09 [−6.28, −2.04]; 67/100; p = 0.00016; Holm 0.00063 |
| G1 | FD004 | k = 5 | A5 | A2 | −4.62 [−6.21, −3.10]; 162/248; p = 1.6e-09; Holm 8e-09 |
| G1 | FD004 | irr 1–5 | A5 | A3 | −3.73 [−5.06, −2.43]; 168/248; p = 1.3e-10; Holm 9.3e-10 |
| G1 | DS03–DS08 | k = 5 | A5 | A1 | −5.90 [−8.84, −3.29]; 17/19; p = 0.00042; Holm 0.00084 |
| G1 | DS03–DS08 | irr 1–5 | A5 | A1 | −3.55 [−5.64, −1.64]; 16/19; p = 0.0017; Holm 0.0017 |
| G2 | FD001 | k = 5 | A8 | A6 | −1.86 [−3.08, −0.70]; 65/100; p = 0.0013; Holm 0.0027 |
| G2 | FD001 | irr 1–5 | A8 | A6 | −1.75 [−2.81, −0.75]; 68/100; p = 0.00055; Holm 0.0016 |
| G2 | FD002 | k = 5 | A8 | A6 | −3.21 [−4.28, −2.17]; 164/259; p = 2.9e-09; Holm 2.1e-08 |
| G2 | FD002 | irr 1–5 | A8 | A6 | −2.38 [−3.35, −1.46]; 158/259; p = 1.4e-06; Holm 7e-06 |
| G2 | FD003 | k = 5 | A8 | A6 | −2.08 [−3.06, −1.19]; 66/100; p = 2.9e-05; Holm 0.00011 |
| G2 | FD003 | irr 1–5 | A8 | A6 | −1.39 [−2.30, −0.50]; 63/100; p = 0.0023; Holm 0.0027 |
| G2 | FD004 | k = 5 | A8 | A6 | −2.85 [−3.95, −1.79]; 180/248; p = 7.6e-10; Holm 6.1e-09 |
| G2 | FD004 | irr 1–5 | A8 | A6 | −2.08 [−2.90, −1.26]; 173/248; p = 1.5e-08; Holm 9.1e-08 |
| G2 | DS03–DS08 | k = 5 | A8 | A6 | −6.82 [−9.72, −3.72]; 16/19; p = 0.00097; Holm 0.0019 |
| G2 | DS03–DS08 | irr 1–5 | A8 | A6 | −4.30 [−7.07, −1.41]; 16/19; p = 0.0071; Holm 0.0071 |
| G3 | FD001 | last 10 | S4 | S1 | −9.59 [−12.14, −7.12]; 82/100; p = 1.9e-11; Holm 1.1e-10 |
| G3 | FD001 | last 5 | S4 | S1 | −10.45 [−13.04, −7.84]; 83/100; p = 8.8e-12; Holm 6.2e-11 |
| G3 | FD002 | last 10 | S4 | S2 | −4.81 [−6.30, −3.30]; 166/259; p = 8.8e-09; Holm 4.4e-08 |
| G3 | FD002 | last 5 | S4 | S2 | −2.92 [−4.12, −1.70]; 153/259; p = 8.8e-06; Holm 2.6e-05 |
| G3 | FD003 | last 10 | S4 | S2 | −6.94 [−11.11, −2.99]; 65/100; p = 0.00018; Holm 0.00036 |
| G3 | FD003 | last 5 | S4 | S2 | −4.72 [−8.59, −1.18]; 64/100; p = 0.0038; Holm 0.0038 |
| G3 | FD004 | last 10 | S4 | S1 | −7.58 [−9.62, −5.60]; 160/248; p = 5.6e-12; Holm 4.4e-11 |
| G3 | FD004 | last 5 | S4 | S2 | −5.19 [−7.01, −3.39]; 162/248; p = 3.1e-08; Holm 1.2e-07 |
| G3 | DS03–DS08 | last 5 | S4 | S2 | −1.55 [−3.36, +0.26]; 11/19; p = 0.17; Holm 0.17 |
| G3 | DS03–DS08 | last 3 | S4 | S2 | −1.77 [−3.85, +0.43]; 14/19; p = 0.08; Holm 0.16 |

Complete records: FD001 A5 vs A1 +0.84 [−0.19, +1.88] (p = 0.092); FD001 S4 vs S1 −0.16 [−1.17, +0.85] (p = 0.74); FD002 A5 vs A1 −0.06 [−0.63, +0.55] (p = 0.85); FD002 S4 vs S1 +0.52 [−0.16, +1.19] (p = 0.085); FD003 A5 vs A1 +1.90 [+0.72, +3.16] (p = 0.011); FD003 S4 vs S1 +1.56 [+0.26, +2.99] (p = 0.053); FD004 A5 vs A1 +0.39 [−0.25, +1.04] (p = 0.21); FD004 S4 vs S1 +1.20 [+0.54, +1.84] (p = 1.8e-05); DS03–DS08 A5 vs A1 +0.53 [−0.45, +1.54] (p = 0.35); DS03–DS08 S4 vs S1 −1.16 [−1.72, −0.62] (p = 0.00079).

Pre-specified reading: G1 carries over (C-MAPSS 8/8, DS03–DS08 2/2, significantly worse 0); G2 carries over (C-MAPSS 8/8, DS03–DS08 2/2, significantly worse 0); G3 partly (C-MAPSS 8/8, DS03–DS08 0/2, significantly worse 0).

Selected configurations (width, learning rate): FD001: A1 (32, 0.0003), A5 (64, 0.0003), A6 (32, 0.0003), A8 (32, 0.001), S4 (32, 0.0003); FD002: A1 (32, 0.0003), A5 (32, 0.0003), A6 (32, 0.0003), A8 (32, 0.0003), S4 (32, 0.0003); FD003: A1 (32, 0.0003), A5 (32, 0.0003), A6 (32, 0.0003), A8 (32, 0.0003), S4 (32, 0.0003); FD004: A1 (32, 0.0003), A5 (32, 0.0003), A6 (32, 0.0003), A8 (32, 0.0003), S4 (32, 0.0003); ext: A1 (32, 0.001), A5 (32, 0.001), A6 (32, 0.001), A8 (32, 0.001), S4 (64, 0.0003).


## Table S28. Generic deletion, training mixture and smoothing: RMSE (cycles)

C-MAPSS: mean ± s.d. over five seeds. DS03–DS08: mean unit RMSE, fixed models. GEN: generic random deletion with about the same expected number of records; A6M: consecutive cycles with moving-average smoothing; A8F: deployment-like gap law (all three: long every-cycle input, full span). A5 r: gap-channel model trained with an additional complete window with probability r (actual share of complete windows about 0.10 + 0.90 r).

| Data | Scenario | A1 | A2 | A6 | A6M | GEN | A8F | A5 r=0 | A5 r=0.25 | A5 r=0.5 | A5 r=0.75 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FD001 | k = 1 | 16.04 ± 0.39 | 16.04 ± 0.39 | 15.74 ± 0.82 | 15.63 ± 0.53 | 12.62 ± 0.78 | 13.36 ± 0.55 | 15.40 ± 1.54 | 14.53 ± 0.72 | 14.25 ± 0.63 | 15.44 ± 0.57 |
| FD001 | k = 5 | 24.93 ± 0.91 | 21.07 ± 1.02 | 18.20 ± 1.03 | 18.51 ± 1.41 | 14.47 ± 0.52 | 14.98 ± 0.70 | 13.21 ± 0.76 | 12.95 ± 0.42 | 12.93 ± 0.82 | 13.36 ± 0.83 |
| FD001 | irr 1–5 | 22.87 ± 1.02 | 19.58 ± 0.54 | 16.58 ± 1.44 | 17.05 ± 1.15 | 12.87 ± 0.41 | 13.60 ± 0.40 | 13.29 ± 0.84 | 13.21 ± 0.61 | 13.51 ± 0.56 | 13.59 ± 0.59 |
| FD001 | block 10 | 17.14 ± 0.65 | 19.03 ± 0.49 | 16.66 ± 0.69 | 16.95 ± 0.44 | 12.69 ± 0.90 | 13.58 ± 0.71 | 15.36 ± 1.32 | 14.74 ± 0.42 | 14.84 ± 0.30 | 15.44 ± 0.23 |
| FD001 | block 20 | 18.91 ± 0.69 | 22.69 ± 0.31 | 16.59 ± 0.67 | 17.15 ± 0.44 | 12.26 ± 0.60 | 13.42 ± 0.51 | 14.84 ± 0.99 | 14.28 ± 0.44 | 14.94 ± 0.49 | 15.53 ± 0.56 |
| FD001 | random deletion | 23.27 ± 1.15 | 18.68 ± 0.45 | 17.63 ± 1.18 | 16.83 ± 1.31 | 15.19 ± 0.55 | 15.82 ± 0.43 | 14.93 ± 0.80 | 14.25 ± 0.49 | 14.37 ± 0.57 | 14.63 ± 0.74 |
| FD002 | k = 1 | 17.50 ± 0.36 | 17.50 ± 0.36 | 15.66 ± 0.65 | 14.98 ± 0.75 | 12.59 ± 0.59 | 13.14 ± 0.63 | 14.64 ± 0.25 | 14.94 ± 0.32 | 16.37 ± 0.85 | 16.64 ± 0.50 |
| FD002 | k = 5 | 20.69 ± 0.58 | 21.73 ± 0.69 | 23.33 ± 1.15 | 18.77 ± 0.97 | 13.78 ± 0.58 | 15.22 ± 0.35 | 13.11 ± 0.27 | 13.32 ± 0.22 | 13.74 ± 0.54 | 14.20 ± 0.38 |
| FD002 | irr 1–5 | 18.70 ± 0.48 | 20.93 ± 0.90 | 19.89 ± 0.68 | 17.30 ± 0.38 | 13.13 ± 0.35 | 14.00 ± 0.58 | 13.50 ± 0.31 | 13.87 ± 0.41 | 14.16 ± 0.42 | 14.50 ± 0.72 |
| FD002 | block 10 | 18.35 ± 0.45 | 20.56 ± 0.91 | 16.19 ± 0.59 | 15.66 ± 0.75 | 13.54 ± 0.47 | 13.89 ± 0.64 | 14.67 ± 0.36 | 14.95 ± 0.35 | 16.00 ± 0.44 | 16.27 ± 0.39 |
| FD002 | block 20 | 18.76 ± 0.86 | 21.03 ± 1.00 | 17.82 ± 0.67 | 17.37 ± 0.44 | 14.55 ± 0.32 | 14.93 ± 0.61 | 15.36 ± 0.39 | 15.33 ± 0.42 | 16.67 ± 0.56 | 17.14 ± 0.66 |
| FD002 | random deletion | 18.13 ± 0.95 | 20.09 ± 1.12 | 20.52 ± 0.91 | 18.12 ± 0.39 | 13.91 ± 0.40 | 14.71 ± 0.31 | 12.78 ± 0.35 | 13.05 ± 0.19 | 13.73 ± 0.62 | 13.90 ± 0.65 |
| FD003 | k = 1 | 13.27 ± 0.76 | 13.27 ± 0.76 | 13.27 ± 0.92 | 13.50 ± 1.10 | 11.91 ± 0.82 | 11.97 ± 0.58 | 14.79 ± 1.42 | 13.32 ± 0.45 | 13.29 ± 0.88 | 13.18 ± 1.23 |
| FD003 | k = 5 | 35.62 ± 1.42 | 16.85 ± 1.22 | 15.79 ± 0.44 | 15.43 ± 0.60 | 14.10 ± 0.95 | 14.34 ± 0.44 | 14.46 ± 0.84 | 14.60 ± 0.84 | 15.14 ± 0.76 | 16.01 ± 0.86 |
| FD003 | irr 1–5 | 26.73 ± 0.79 | 18.20 ± 0.95 | 17.07 ± 0.88 | 16.83 ± 0.95 | 14.05 ± 1.05 | 14.58 ± 0.45 | 13.31 ± 0.29 | 13.65 ± 0.72 | 13.65 ± 0.87 | 13.78 ± 1.04 |
| FD003 | block 10 | 14.97 ± 0.44 | 16.25 ± 0.73 | 14.59 ± 0.90 | 14.70 ± 1.09 | 12.63 ± 0.89 | 12.54 ± 0.59 | 15.82 ± 0.95 | 15.51 ± 0.80 | 15.51 ± 1.13 | 15.53 ± 1.04 |
| FD003 | block 20 | 18.94 ± 0.83 | 17.62 ± 1.08 | 15.34 ± 0.82 | 15.26 ± 1.37 | 12.88 ± 1.04 | 12.82 ± 0.54 | 18.36 ± 1.52 | 18.59 ± 1.27 | 18.75 ± 1.87 | 18.63 ± 1.79 |
| FD003 | random deletion | 26.17 ± 1.08 | 17.09 ± 0.87 | 13.91 ± 0.70 | 13.68 ± 1.31 | 11.86 ± 0.38 | 12.08 ± 0.54 | 13.23 ± 0.44 | 13.27 ± 0.53 | 13.40 ± 0.88 | 14.04 ± 1.09 |
| FD004 | k = 1 | 17.70 ± 0.70 | 17.70 ± 0.70 | 16.74 ± 0.86 | 15.24 ± 0.62 | 13.38 ± 0.62 | 14.09 ± 0.98 | 15.56 ± 0.45 | 15.18 ± 0.52 | 15.56 ± 0.37 | 16.30 ± 0.21 |
| FD004 | k = 5 | 29.37 ± 2.47 | 24.11 ± 0.68 | 22.83 ± 1.29 | 20.22 ± 0.84 | 16.02 ± 0.46 | 16.75 ± 0.55 | 15.10 ± 0.51 | 15.22 ± 0.32 | 15.43 ± 0.71 | 15.51 ± 0.38 |
| FD004 | irr 1–5 | 25.45 ± 1.22 | 21.19 ± 0.65 | 21.12 ± 1.59 | 18.90 ± 0.77 | 14.85 ± 0.33 | 15.88 ± 0.37 | 14.11 ± 0.46 | 14.21 ± 0.27 | 14.41 ± 0.62 | 14.81 ± 0.58 |
| FD004 | block 10 | 17.84 ± 0.17 | 21.00 ± 0.89 | 17.10 ± 1.17 | 15.91 ± 0.82 | 14.19 ± 0.46 | 14.84 ± 1.20 | 16.07 ± 0.53 | 15.89 ± 0.55 | 16.26 ± 0.56 | 16.88 ± 0.55 |
| FD004 | block 20 | 19.12 ± 0.73 | 23.10 ± 0.82 | 18.74 ± 0.62 | 17.85 ± 1.21 | 15.17 ± 0.49 | 16.04 ± 0.93 | 17.24 ± 0.42 | 17.28 ± 1.14 | 17.23 ± 0.80 | 18.14 ± 1.34 |
| FD004 | random deletion | 24.35 ± 1.60 | 21.75 ± 0.59 | 20.09 ± 1.19 | 18.06 ± 1.23 | 13.92 ± 0.39 | 14.26 ± 0.90 | 14.13 ± 0.36 | 14.71 ± 0.45 | 14.59 ± 0.44 | 14.77 ± 0.45 |
| DS03–DS08 | k = 1 | 13.78 | 13.78 | 12.25 | 11.22 | 9.20 | 9.50 | 12.75 | 12.30 | 12.29 | 12.59 |
| DS03–DS08 | k = 5 | 16.56 | 19.44 | 23.02 | 14.72 | 10.22 | 10.59 | 8.60 | 8.90 | 9.08 | 10.21 |
| DS03–DS08 | irr 1–5 | 15.18 | 18.53 | 20.04 | 13.02 | 9.66 | 9.73 | 9.43 | 10.06 | 10.30 | 10.97 |
| DS03–DS08 | block 5 | 14.57 | 18.02 | 12.83 | 12.03 | 9.64 | 9.70 | 12.31 | 12.03 | 12.13 | 12.58 |
| DS03–DS08 | block 10 | 15.06 | 19.61 | 14.47 | 12.82 | 9.88 | 10.15 | 12.00 | 11.63 | 11.78 | 12.37 |
| DS03–DS08 | random deletion | 16.38 | 19.22 | 20.46 | 14.27 | 10.86 | 10.83 | 10.83 | 11.10 | 11.61 | 12.29 |

## Table S29. Q1: generic random deletion versus the deployment-like gap law


**Q1a exposure to deletion: GEN minus A6.**

| Data | Scenario | Δ [95% CI]; units better; p; Holm |
|---|---|---|
| FD001 | k = 5 | −2.22 [−3.76, −0.86]; 55/100; p = 0.013; Holm 0.013 |
| FD001 | irr 1–5 | −2.31 [−3.59, −1.09]; 65/100; p = 0.0008; Holm 0.0016 |
| FD002 | k = 5 | −6.75 [−8.17, −5.37]; 177/259; p = 5.5e-18; Holm 4.4e-17 |
| FD002 | irr 1–5 | −4.43 [−5.62, −3.25]; 182/259; p = 4.4e-13; Holm 2.6e-12 |
| FD003 | k = 5 | −1.88 [−3.07, −0.68]; 66/100; p = 0.00013; Holm 0.00052 |
| FD003 | irr 1–5 | −2.13 [−3.35, −0.99]; 65/100; p = 0.00037; Holm 0.0011 |
| FD004 | k = 5 | −4.64 [−5.94, −3.35]; 165/248; p = 3.3e-13; Holm 2.3e-12 |
| FD004 | irr 1–5 | −4.41 [−5.58, −3.29]; 167/248; p = 4.6e-13; Holm 2.6e-12 |
| DS03–DS08 | k = 5 | −13.61 [−16.90, −9.93]; 18/19; p = 2.7e-05; Holm 5.3e-05 |
| DS03–DS08 | irr 1–5 | −11.68 [−15.34, −7.67]; 17/19; p = 7.2e-05; Holm 7.2e-05 |

Holm-significant in favour of GEN: C-MAPSS 8/8, DS03–DS08 2/2; in favour of A6: 0/8, 0/2.

**Q1b matching the sampling structure: A8F minus GEN.**

| Data | Scenario | Δ [95% CI]; units better; p; Holm |
|---|---|---|
| FD001 | k = 5 | +0.19 [−0.26, +0.66]; 46/100; p = 0.27; Holm 1 |
| FD001 | irr 1–5 | +0.56 [−0.03, +1.15]; 42/100; p = 0.05; Holm 0.3 |
| FD002 | k = 5 | +0.91 [+0.54, +1.32]; 110/259; p = 0.00024; Holm 0.0019 |
| FD002 | irr 1–5 | +0.42 [−0.00, +0.86]; 119/259; p = 0.21; Holm 1 |
| FD003 | k = 5 | +0.11 [−0.35, +0.57]; 49/100; p = 0.59; Holm 1 |
| FD003 | irr 1–5 | +0.24 [−0.22, +0.70]; 52/100; p = 0.53; Holm 1 |
| FD004 | k = 5 | +0.19 [−0.32, +0.71]; 112/248; p = 0.25; Holm 1 |
| FD004 | irr 1–5 | +0.66 [+0.30, +1.03]; 110/248; p = 0.0038; Holm 0.026 |
| DS03–DS08 | k = 5 | −0.09 [−0.95, +0.82]; 11/19; p = 0.8; Holm 1 |
| DS03–DS08 | irr 1–5 | −0.22 [−1.03, +0.68]; 11/19; p = 0.54; Holm 1 |

Holm-significant in favour of A8F: C-MAPSS 0/8, DS03–DS08 0/2; in favour of GEN: 2/8, 0/2.
A8F vs GEN at k = 5 on C-MAPSS: Δ +0.11 to +0.91; significantly better in 0/4, worse in 1/4.
A8F vs GEN at irr 1–5 on C-MAPSS: Δ +0.24 to +0.66; significantly better in 0/4, worse in 1/4.

A8F minus GEN in the other scenarios (uncorrected): random deletion: C-MAPSS Δ +0.38 (p = 0.23), +0.35 (p = 0.12), +0.12 (p = 0.91), +0.32 (p = 0.097); DS03–DS08 (random deletion) +0.03 (p = 1); block 10: C-MAPSS Δ +0.51 (p = 0.11), +0.07 (p = 0.78), −0.06 (p = 0.78), +0.37 (p = 0.089); DS03–DS08 (block 5) −0.00 (p = 0.71); block 20: C-MAPSS Δ +0.87 (p = 0.013), +0.11 (p = 0.74), +0.09 (p = 0.56), +0.51 (p = 0.019); DS03–DS08 (block 10) +0.21 (p = 0.54); k = 1: C-MAPSS Δ +0.52 (p = 0.066), +0.18 (p = 0.58), −0.14 (p = 0.39), +0.40 (p = 0.064); DS03–DS08 (k = 1) +0.24 (p = 0.4).

Pre-specified reading for Q1: exposure to deletion is enough.

## Table S30. Q2: probability r of an additional complete window in training (gap-channel model); first analysis, with unadjusted p values and the best remedy among A1 and A2 only (corrected comparisons: Table S32)

Selection on validation units only (seed 0): validation RMSE with complete records / at k = 5 / score, and the selected r*.

| Data | r = 0.0 | r = 0.25 | r = 0.5 | r = 0.75 | r* |
|---|---|---|---|---|---|
| FD001 | 14.45 / 13.28 / 13.86 | 14.84 / 13.02 / 13.93 | 14.77 / 13.85 / 14.31 | 14.88 / 15.60 / 15.24 | 0.0 |
| FD002 | 15.01 / 13.23 / 14.12 | 15.20 / 13.67 / 14.43 | 15.78 / 13.63 / 14.70 | 16.26 / 14.37 / 15.32 | 0.0 |
| FD003 | 11.83 / 11.18 / 11.51 | 11.00 / 10.46 / 10.73 | 11.80 / 10.86 / 11.33 | 11.71 / 12.30 / 12.01 | 0.25 |
| FD004 | 14.94 / 14.23 / 14.58 | 14.70 / 13.60 / 14.15 | 15.97 / 14.24 / 15.11 | 14.89 / 14.18 / 14.53 | 0.25 |
| DS03–DS08 | 14.66 / 12.87 / 13.77 | 13.97 / 12.35 / 13.16 | 14.41 / 11.74 / 13.08 | 16.34 / 13.13 / 14.73 | 0.5 |

Test results. Cost: Δ against the dense model A1 with complete records. Gain: Δ against the best test-time remedy (A1 or A2, by RMSE) at k = 5 and irregular 1–5. Δ in seed-averaged engine absolute error (C-MAPSS) or group RMSE (DS03–DS08) with 95% interval and uncorrected p.

| Data | r | Cost, complete records | Gain, k = 5 | Gain, irr 1–5 | RMSE block (10 / 20 or 5 / 10) |
|---|---|---|---|---|---|
| FD001 | 0.0 (r*) | +0.00 [−1.30, +1.26]; 45/100; p = 0.51 | −5.67 [−8.21, −3.24]; 68/100; p = 2.6e-05 | −4.31 [−6.98, −1.75]; 60/100; p = 0.0078 | 15.36 / 14.84 |
| FD001 | 0.25 | −0.42 [−1.28, +0.42]; 51/100; p = 0.63 | −5.67 [−8.20, −3.21]; 65/100; p = 5e-05 | −4.41 [−7.17, −1.72]; 61/100; p = 0.0034 | 14.74 / 14.28 |
| FD001 | 0.5 | −0.90 [−1.66, −0.19]; 56/100; p = 0.047 | −5.77 [−8.27, −3.34]; 65/100; p = 3.3e-05 | −4.28 [−7.08, −1.55]; 56/100; p = 0.013 | 14.84 / 14.94 |
| FD001 | 0.75 | −0.36 [−1.08, +0.33]; 54/100; p = 0.26 | −5.29 [−7.62, −3.04]; 67/100; p = 2.4e-05 | −4.43 [−7.13, −1.80]; 62/100; p = 0.0017 | 15.44 / 15.53 |
| FD002 | 0.0 (r*) | −1.49 [−2.29, −0.70]; 155/259; p = 0.00074 | −5.52 [−6.74, −4.35]; 185/259; p = 1.9e-16 | −4.08 [−5.13, −3.06]; 195/259; p = 1.4e-15 | 14.67 / 15.36 |
| FD002 | 0.25 | −1.34 [−2.04, −0.63]; 135/259; p = 0.0044 | −4.88 [−6.14, −3.66]; 171/259; p = 2.7e-11 | −3.53 [−4.61, −2.49]; 169/259; p = 1.3e-09 | 14.95 / 15.33 |
| FD002 | 0.5 | −0.50 [−1.12, +0.12]; 142/259; p = 0.11 | −4.56 [−5.79, −3.36]; 167/259; p = 7e-11 | −3.28 [−4.24, −2.31]; 164/259; p = 2.6e-09 | 16.00 / 16.67 |
| FD002 | 0.75 | −0.63 [−1.23, −0.06]; 147/259; p = 0.023 | −4.40 [−5.54, −3.29]; 170/259; p = 1.3e-11 | −3.01 [−3.95, −2.09]; 165/259; p = 4e-09 | 16.27 / 17.14 |
| FD003 | 0.0 | +1.63 [+0.74, +2.56]; 33/100; p = 0.00035 | −2.43 [−4.43, −0.45]; 62/100; p = 0.013 | −3.11 [−5.42, −1.07]; 67/100; p = 0.0022 | 15.82 / 18.36 |
| FD003 | 0.25 (r*) | +0.29 [−0.23, +0.80]; 44/100; p = 0.17 | −2.32 [−4.27, −0.41]; 59/100; p = 0.021 | −2.89 [−5.03, −0.95]; 67/100; p = 0.002 | 15.51 / 18.59 |
| FD003 | 0.5 | +0.15 [−0.28, +0.60]; 46/100; p = 0.61 | −1.85 [−3.82, +0.07]; 57/100; p = 0.061 | −2.79 [−4.95, −0.84]; 65/100; p = 0.0047 | 15.51 / 18.75 |
| FD003 | 0.75 | +0.08 [−0.32, +0.49]; 50/100; p = 0.84 | −1.03 [−3.05, +0.95]; 55/100; p = 0.33 | −2.49 [−4.74, −0.50]; 60/100; p = 0.038 | 15.53 / 18.63 |
| FD004 | 0.0 | −1.36 [−2.26, −0.49]; 148/248; p = 8.8e-05 | −6.21 [−7.95, −4.48]; 169/248; p = 9.2e-13 | −4.61 [−6.20, −3.14]; 163/248; p = 7.2e-11 | 16.07 / 17.24 |
| FD004 | 0.25 (r*) | −1.45 [−2.11, −0.79]; 163/248; p = 2.6e-07 | −6.10 [−7.88, −4.33]; 169/248; p = 5.8e-12 | −4.57 [−6.14, −3.09]; 168/248; p = 9.3e-11 | 15.89 / 17.28 |
| FD004 | 0.5 | −1.38 [−1.98, −0.76]; 160/248; p = 6.4e-07 | −5.88 [−7.68, −4.12]; 170/248; p = 2.3e-11 | −4.30 [−5.86, −2.85]; 162/248; p = 2.6e-09 | 16.26 / 17.23 |
| FD004 | 0.75 | −0.78 [−1.32, −0.24]; 145/248; p = 0.0022 | −5.54 [−7.26, −3.87]; 165/248; p = 2.7e-10 | −3.99 [−5.51, −2.56]; 154/248; p = 2.9e-08 | 16.88 / 18.14 |
| DS03–DS08 | 0.0 | −0.68 [−1.63, +0.40]; 14/19; p = 0.13 | −7.96 [−10.98, −5.05]; 18/19; p = 9.5e-05 | −5.76 [−8.19, −3.59]; 17/19; p = 5.3e-05 | 12.31 / 12.00 |
| DS03–DS08 | 0.25 | −1.17 [−1.82, −0.49]; 14/19; p = 0.0053 | −7.79 [−10.83, −4.86]; 18/19; p = 7.2e-05 | −5.24 [−7.71, −2.88]; 15/19; p = 0.00079 | 12.03 / 11.63 |
| DS03–DS08 | 0.5 (r*) | −1.26 [−1.86, −0.65]; 15/19; p = 0.0014 | −7.64 [−10.44, −4.88]; 18/19; p = 9.5e-05 | −4.92 [−7.22, −2.66]; 14/19; p = 0.0012 | 12.13 / 11.78 |
| DS03–DS08 | 0.75 | −1.18 [−1.82, −0.66]; 18/19; p = 0.00021 | −6.88 [−9.65, −4.08]; 16/19; p = 0.00034 | −4.69 [−6.98, −2.45]; 16/19; p = 0.0017 | 12.58 / 12.37 |

Pre-specified reading for Q2 (model with r*): FD001: r* = 0.0, non-inferior with complete records no (r = 0: no), keeps sparse-record advantage yes; FD002: r* = 0.0, non-inferior with complete records yes (r = 0: yes), keeps sparse-record advantage yes; FD003: r* = 0.25, non-inferior with complete records yes (r = 0: no), keeps sparse-record advantage yes; FD004: r* = 0.25, non-inferior with complete records yes (r = 0: yes), keeps sparse-record advantage yes; DS03–DS08: r* = 0.5, non-inferior with complete records yes (r = 0: yes), keeps sparse-record advantage yes.

Model with r* minus r = 0 at k = 5 and irregular 1–5: FD001: r* = 0; FD002: r* = 0; FD003: +0.10 (p = 0.75) and +0.22 (p = 0.65); FD004: +0.11 (p = 0.59) and +0.04 (p = 0.95); DS03–DS08: +0.32 (p = 0.23) and +0.84 (p = 0.0082).

## Table S31. Q3: smoothing of the training input


**Q3a smoothing without deletion: A6M minus A6.**

| Data | Scenario | Δ [95% CI]; units better; p; Holm |
|---|---|---|
| FD001 | k = 5 | +0.29 [−0.54, +1.11]; 49/100; p = 0.55; Holm 1 |
| FD001 | irr 1–5 | +0.42 [−0.42, +1.30]; 49/100; p = 0.76; Holm 1 |
| FD002 | k = 5 | −3.26 [−4.55, −2.00]; 155/259; p = 6.3e-06; Holm 5.1e-05 |
| FD002 | irr 1–5 | −1.65 [−2.64, −0.62]; 146/259; p = 0.0032; Holm 0.023 |
| FD003 | k = 5 | −0.37 [−0.95, +0.22]; 58/100; p = 0.12; Holm 0.47 |
| FD003 | irr 1–5 | −0.07 [−0.83, +0.68]; 49/100; p = 0.68; Holm 1 |
| FD004 | k = 5 | −1.77 [−2.88, −0.66]; 135/248; p = 0.0062; Holm 0.037 |
| FD004 | irr 1–5 | −1.57 [−2.51, −0.63]; 140/248; p = 0.0089; Holm 0.045 |
| DS03–DS08 | k = 5 | −8.73 [−11.80, −5.43]; 16/19; p = 0.00027; Holm 0.00053 |
| DS03–DS08 | irr 1–5 | −8.39 [−11.83, −4.50]; 15/19; p = 0.0014; Holm 0.0014 |

Holm-significant in favour of A6M: C-MAPSS 4/8, DS03–DS08 2/2; in favour of A6: 0/8, 0/2.

**Q3b sparsification beyond smoothing: A8F minus A6M.**

| Data | Scenario | Δ [95% CI]; units better; p; Holm |
|---|---|---|
| FD001 | k = 5 | −2.32 [−3.94, −0.82]; 61/100; p = 0.0052; Holm 0.0052 |
| FD001 | irr 1–5 | −2.17 [−3.39, −0.95]; 66/100; p = 0.00095; Holm 0.0038 |
| FD002 | k = 5 | −2.57 [−3.40, −1.78]; 166/259; p = 2.1e-09; Holm 1.7e-08 |
| FD002 | irr 1–5 | −2.36 [−3.28, −1.45]; 168/259; p = 1.1e-08; Holm 7.8e-08 |
| FD003 | k = 5 | −1.40 [−2.54, −0.18]; 64/100; p = 0.00098; Holm 0.0038 |
| FD003 | irr 1–5 | −1.82 [−2.94, −0.76]; 63/100; p = 0.0011; Holm 0.0038 |
| FD004 | k = 5 | −2.68 [−3.59, −1.80]; 158/248; p = 2.8e-08; Holm 1.7e-07 |
| FD004 | irr 1–5 | −2.18 [−3.11, −1.24]; 160/248; p = 2.5e-07; Holm 1.3e-06 |
| DS03–DS08 | k = 5 | −4.98 [−6.43, −3.35]; 17/19; p = 7.2e-05; Holm 0.00014 |
| DS03–DS08 | irr 1–5 | −3.52 [−4.70, −2.32]; 17/19; p = 9.5e-05; Holm 0.00014 |

Holm-significant in favour of A8F: C-MAPSS 8/8, DS03–DS08 2/2; in favour of A6M: 0/8, 0/2.

Share of the A8F gain over A6 recovered by A6M (ratio of mean differences), ten comparisons: −0.14, −0.24, 0.56, 0.41, 0.21, 0.04, 0.40, 0.42, 0.64, 0.70; median 0.40.

Pre-specified reading for Q3: inconclusive.

## Table S32. Q2 after correction: Holm-adjusted sparse-record comparisons, carry-forward included among the test-time remedies

Correction made after independent verification, without retraining. The best test-time remedy is the one of A1, A2 and A3 with the lowest RMSE (five seeds); the errors of A3 come from the five-seed runs of the same dense models. Holm adjustment within the eight C-MAPSS comparisons and within the two external-cohort comparisons of each row group. Δ in seed-averaged engine absolute error (C-MAPSS) or group RMSE (DS03–DS08), cycles.

RMSE of the remedies (A1 / A2 / A3): FD001 k = 5 24.93 / 21.07 / 21.97, irr 1–5 22.87 / 19.58 / 20.02; FD002 k = 5 20.69 / 21.73 / 22.49, irr 1–5 18.70 / 20.93 / 21.40; FD003 k = 5 35.62 / 16.85 / 18.00, irr 1–5 26.73 / 18.20 / 19.73; FD004 k = 5 29.37 / 24.11 / 23.94, irr 1–5 25.45 / 21.19 / 21.73; DS03–DS08 k = 5 16.56 / 19.44 / 19.70, irr 1–5 15.18 / 18.53 / 18.36.

**Models with the selected share r\*.**

| Data | r* | Gain, k = 5 | Gain, irr 1–5 |
|---|---|---|---|
| FD001 | 0.0 | −5.67 [−8.21, −3.24]; 68/100; p = 2.6e-05; Holm 0.0001; ref. A2 | −4.31 [−6.98, −1.75]; 60/100; p = 0.0078; Holm 0.016; ref. A2 |
| FD002 | 0.0 | −5.52 [−6.74, −4.35]; 185/259; p = 1.9e-16; Holm 1.5e-15; ref. A1 | −4.08 [−5.13, −3.06]; 195/259; p = 1.4e-15; Holm 8.3e-15; ref. A1 |
| FD003 | 0.25 | −2.32 [−4.27, −0.41]; 59/100; p = 0.021; Holm 0.021; ref. A2 | −2.89 [−5.03, −0.95]; 67/100; p = 0.002; Holm 0.0061; ref. A2 |
| FD004 | 0.25 | −6.51 [−8.21, −4.82]; 177/248; p = 2e-16; Holm 1.5e-15; ref. A3 | −4.57 [−6.14, −3.09]; 168/248; p = 9.3e-11; Holm 4.7e-10; ref. A2 |
| DS03–DS08 | 0.5 | −7.64 [−10.44, −4.88]; 18/19; p = 9.5e-05; Holm 0.00019; ref. A1 | −4.92 [−7.22, −2.66]; 14/19; p = 0.0012; Holm 0.0012; ref. A1 |

**All values of r** (Holm within each value of r).

| Data | r | Gain, k = 5 | Gain, irr 1–5 |
|---|---|---|---|
| FD001 | 0.0 (r*) | −5.67 [−8.21, −3.24]; 68/100; p = 2.6e-05; Holm 0.0001; ref. A2 | −4.31 [−6.98, −1.75]; 60/100; p = 0.0078; Holm 0.016; ref. A2 |
| FD001 | 0.25 | −5.67 [−8.20, −3.21]; 65/100; p = 5e-05; Holm 0.0002; ref. A2 | −4.41 [−7.17, −1.72]; 61/100; p = 0.0034; Holm 0.0067; ref. A2 |
| FD001 | 0.5 | −5.77 [−8.27, −3.34]; 65/100; p = 3.3e-05; Holm 0.00013; ref. A2 | −4.28 [−7.08, −1.55]; 56/100; p = 0.013; Holm 0.027; ref. A2 |
| FD001 | 0.75 | −5.29 [−7.62, −3.04]; 67/100; p = 2.4e-05; Holm 9.5e-05; ref. A2 | −4.43 [−7.13, −1.80]; 62/100; p = 0.0017; Holm 0.0051; ref. A2 |
| FD002 | 0.0 (r*) | −5.52 [−6.74, −4.35]; 185/259; p = 1.9e-16; Holm 1.3e-15; ref. A1 | −4.08 [−5.13, −3.06]; 195/259; p = 1.4e-15; Holm 8.3e-15; ref. A1 |
| FD002 | 0.25 | −4.88 [−6.14, −3.66]; 171/259; p = 2.7e-11; Holm 1.9e-10; ref. A1 | −3.53 [−4.61, −2.49]; 169/259; p = 1.3e-09; Holm 6.5e-09; ref. A1 |
| FD002 | 0.5 | −4.56 [−5.79, −3.36]; 167/259; p = 7e-11; Holm 4.9e-10; ref. A1 | −3.28 [−4.24, −2.31]; 164/259; p = 2.6e-09; Holm 1.6e-08; ref. A1 |
| FD002 | 0.75 | −4.40 [−5.54, −3.29]; 170/259; p = 1.3e-11; Holm 9.4e-11; ref. A1 | −3.01 [−3.95, −2.09]; 165/259; p = 4e-09; Holm 2.4e-08; ref. A1 |
| FD003 | 0.0 | −2.43 [−4.43, −0.45]; 62/100; p = 0.013; Holm 0.016; ref. A2 | −3.11 [−5.42, −1.07]; 67/100; p = 0.0022; Holm 0.0065; ref. A2 |
| FD003 | 0.25 (r*) | −2.32 [−4.27, −0.41]; 59/100; p = 0.021; Holm 0.021; ref. A2 | −2.89 [−5.03, −0.95]; 67/100; p = 0.002; Holm 0.0061; ref. A2 |
| FD003 | 0.5 | −1.85 [−3.82, +0.07]; 57/100; p = 0.061; Holm 0.061; ref. A2 | −2.79 [−4.95, −0.84]; 65/100; p = 0.0047; Holm 0.014; ref. A2 |
| FD003 | 0.75 | −1.03 [−3.05, +0.95]; 55/100; p = 0.33; Holm 0.33; ref. A2 | −2.49 [−4.74, −0.50]; 60/100; p = 0.038; Holm 0.075; ref. A2 |
| FD004 | 0.0 | −6.63 [−8.27, −4.96]; 187/248; p = 2e-17; Holm 1.6e-16; ref. A3 | −4.61 [−6.20, −3.14]; 163/248; p = 7.2e-11; Holm 3.6e-10; ref. A2 |
| FD004 | 0.25 (r*) | −6.51 [−8.21, −4.82]; 177/248; p = 2e-16; Holm 1.6e-15; ref. A3 | −4.57 [−6.14, −3.09]; 168/248; p = 9.3e-11; Holm 5.6e-10; ref. A2 |
| FD004 | 0.5 | −6.30 [−7.99, −4.62]; 186/248; p = 7.3e-16; Holm 5.8e-15; ref. A3 | −4.30 [−5.86, −2.85]; 162/248; p = 2.6e-09; Holm 1.6e-08; ref. A2 |
| FD004 | 0.75 | −5.96 [−7.57, −4.35]; 182/248; p = 8.9e-15; Holm 7.1e-14; ref. A3 | −3.99 [−5.51, −2.56]; 154/248; p = 2.9e-08; Holm 1.4e-07; ref. A2 |
| DS03–DS08 | 0.0 | −7.96 [−10.98, −5.05]; 18/19; p = 9.5e-05; Holm 0.00011; ref. A1 | −5.76 [−8.19, −3.59]; 17/19; p = 5.3e-05; Holm 0.00011; ref. A1 |
| DS03–DS08 | 0.25 | −7.79 [−10.83, −4.86]; 18/19; p = 7.2e-05; Holm 0.00014; ref. A1 | −5.24 [−7.71, −2.88]; 15/19; p = 0.00079; Holm 0.00079; ref. A1 |
| DS03–DS08 | 0.5 (r*) | −7.64 [−10.44, −4.88]; 18/19; p = 9.5e-05; Holm 0.00019; ref. A1 | −4.92 [−7.22, −2.66]; 14/19; p = 0.0012; Holm 0.0012; ref. A1 |
| DS03–DS08 | 0.75 | −6.88 [−9.65, −4.08]; 16/19; p = 0.00034; Holm 0.00067; ref. A1 | −4.69 [−6.98, −2.45]; 16/19; p = 0.0017; Holm 0.0017; ref. A1 |

Reading for Q2 with the corrected comparisons: FD001: r* = 0.0, non-inferior with complete records no, keeps sparse-record advantage (Holm) yes; FD002: r* = 0.0, non-inferior with complete records yes, keeps sparse-record advantage (Holm) yes; FD003: r* = 0.25, non-inferior with complete records yes, keeps sparse-record advantage (Holm) yes; FD004: r* = 0.25, non-inferior with complete records yes, keeps sparse-record advantage (Holm) yes; DS03–DS08: r* = 0.5, non-inferior with complete records yes, keeps sparse-record advantage (Holm) yes. The rule held on 4 of 5 data sources.

Actual share of complete training windows: r is the probability of the additional complete branch; the gap law itself yields a complete window with probability 0.10. r = 0.0: 10.0%; r = 0.25: 32.5%; r = 0.5: 55.0%; r = 0.75: 77.5%.

## Table S33. Missingness simulation on real battery-ageing records (section 4.13)

Protocol (checksummed before the runs). Data: MIT fast-charging cells (end of life: first of three consecutive discharge capacities below 0.88 Ah, or the last recorded cycle if the last capacity is at most 0.885 Ah; 12 of 140 cells that never reached this level excluded; as implemented, 43 cells end by the first criterion and 85 by the second, their records stopping at 0.8800-0.8834 Ah; invalid source values replaced by the previous valid value of the cell, and those in the leading rows of 36 cells (324 of 375 invalid values) by the next valid value; 13 per-cycle features) and XJTU batches 1-4 (pre-programmed constant-current protocols; in batches 3 and 4 the discharge rate cycles through preset values; batches 5 and 6, with programmed variable loads not contained in the per-cycle table, excluded a priori; first characterisation cycle dropped; end of life: last recorded cycle; 10 per-cycle features, standardised per cycle type). Target: remaining cycles capped at 450 (MIT) and 250 (XJTU). GRU with an every-cycle input of 200 cycles, linearly interpolated from the available records. DENSE: complete windows; GEN: every earlier cycle kept with probability p (p = 1/m, m uniform in 1 to 10, for half of the windows, p = 2/11 for the others); MIX: GEN with a complete window with additional probability r, chosen per fold on validation cells from 0.25, 0.5 and 0.75. Scenarios at prediction times 30, 40, 50, ...: full (all records), k10 (one record every 10 cycles), blk (records up to t - 53, outage of 50 cycles, last three cycles; at t = 30, 40 and 50, 4.0% of the MIT and 7.2% of the XJTU predictions, there is no record before the outage and only the last three records are available). Five folds over cells, stratified by batch; seeds 0-4. Cell RMSE averaged over seeds; two-sided Wilcoxon; bootstrap interval; Holm over R1-R3 per data set. R3 holds if MIX is significantly better than DENSE in k10 and non-inferior with complete records (margin 0.8% of the cap). Before the protocol was frozen, only the structure of the tables was inspected and one smoke run (one epoch, shapes and timing only) was made.

**MIT: 128 cells, selected share per fold [0.75, 0.5, 0.25, 0.75, 0.75]**

| Scenario | DENSE | GEN | MIX |
|---|---|---|---|
| full | 34.6 ± 2.5 | 33.6 ± 1.6 | 34.1 ± 1.9 |
| k10 | 34.0 ± 2.7 | 33.3 ± 1.6 | 33.8 ± 1.7 |
| blk | 35.5 ± 2.4 | 33.7 ± 1.5 | 34.6 ± 1.9 |

Paired differences in cell RMSE (cycles; negative: first arm better); non-inferiority margin 3.6 cycles

| Comparison | Δ | 95% CI | p | Holm | cells better |
|---|---|---|---|---|---|
| R1 GEN vs DENSE, k10 | −1.28 | −2.56 to +0.04 | 0.0088 | 0.018 | 73/128 |
| R2 GEN vs DENSE, blk | −2.41 | −3.68 to −1.12 | 1.7e-05 | 5.1e-05 | 83/128 |
| R3 MIX vs DENSE, k10 | −0.72 | −1.68 to +0.33 | 0.047 | 0.047 | 76/128 |
| cost GEN vs DENSE, full | −1.13 | −2.39 to +0.17 | 0.033 | — | 74/128 |
| cost MIX vs DENSE, full | −0.61 | −1.60 to +0.42 | 0.21 | — | 71/128 |
| MIX vs GEN, k10 | +0.56 | −0.27 to +1.44 | 0.36 | — | 62/128 |
| MIX vs DENSE, blk | −1.45 | −2.44 to −0.43 | 0.0036 | — | 79/128 |

Pre-specified readings R1, R2 and R3: all hold.

**XJTU: 39 cells, selected share per fold [0.75, 0.75, 0.25, 0.75, 0.75]**

| Scenario | DENSE | GEN | MIX |
|---|---|---|---|
| full | 24.9 ± 0.8 | 23.7 ± 0.8 | 23.5 ± 0.7 |
| k10 | 25.1 ± 0.7 | 23.8 ± 0.7 | 23.7 ± 0.6 |
| blk | 26.1 ± 0.4 | 24.1 ± 0.9 | 24.1 ± 0.8 |

Paired differences in cell RMSE (cycles; negative: first arm better); non-inferiority margin 2.0 cycles

| Comparison | Δ | 95% CI | p | Holm | cells better |
|---|---|---|---|---|---|
| R1 GEN vs DENSE, k10 | −2.50 | −4.76 to −0.61 | 0.014 | 0.027 | 27/39 |
| R2 GEN vs DENSE, blk | −3.72 | −6.28 to −1.58 | 2.6e-05 | 7.7e-05 | 32/39 |
| R3 MIX vs DENSE, k10 | −2.30 | −4.56 to −0.41 | 0.031 | 0.031 | 25/39 |
| cost GEN vs DENSE, full | −2.19 | −4.17 to −0.57 | 0.012 | — | 26/39 |
| cost MIX vs DENSE, full | −2.11 | −4.14 to −0.38 | 0.043 | — | 24/39 |
| MIX vs GEN, k10 | +0.19 | −0.60 to +0.89 | 0.22 | — | 15/39 |
| MIX vs DENSE, blk | −3.48 | −6.08 to −1.34 | 0.00016 | — | 31/39 |

Pre-specified readings R1, R2 and R3: all hold.

Overall reading: R1, R2 and R3 carried over (held on both data sets).

**Deviation noticed after the runs, and sensitivity analysis (not in the protocol).** Five MIT cells of batch 2017-06-30 (c7, c8, c9, c15, c16) continue cells c0-c4 of batch 2017-05-12; the first parts were excluded because they did not reach the end of life within their batch, and the protocol did not join the parts, so the five cells enter as late-life fragments. No cell is shared between training and test data. The lines below repeat the MIT comparisons without these five cells in the test statistics (no retraining; the cells remain in the training folds). Holm-adjusted p of R1, R2, R3 without them: 0.024, 3.3e-05, 0.048. The per-cycle tables were produced from the original files by the export scripts in realsys/export_scripts; this export was not repeated for the present work.

- MIT, paired differences in cell RMSE: all 128 cells; without the five cells: without the five continuation cells (123)
- R1 GEN vs DENSE, k10: −1.28 [−2.56, +0.04] p = 0.0088; without the five cells: −1.24 [−2.53, +0.08] p = 0.012
- R2 GEN vs DENSE, blk: −2.41 [−3.68, −1.12] p = 1.7e-05; without the five cells: −2.51 [−3.80, −1.19] p = 1.1e-05
- R3 MIX vs DENSE, k10: −0.72 [−1.68, +0.33] p = 0.047; without the five cells: −0.72 [−1.69, +0.35] p = 0.048
- cost GEN vs DENSE, full: −1.13 [−2.39, +0.17] p = 0.033; without the five cells: −1.18 [−2.46, +0.15] p = 0.028
- cost MIX vs DENSE, full: −0.61 [−1.60, +0.42] p = 0.21; without the five cells: −0.65 [−1.66, +0.40] p = 0.18
- RMSE of the five cells (DENSE/GEN, full): c15 22.1/22.4; c16 32.2/40.4; c7 25.5/29.6; c8 13.7/9.5; c9 21.2/12.9

**Provenance of the input tables and checks of the definitions (added after the runs).** The two input tables are byte-identical to the merged tables of the export (md5 8dd8ed8f268afff2cd541f9294c16c28 for MIT, 7ba1b6f9d77c8c32dd4e301f8dd22caa for XJTU; realsys/export_scripts/README_provenance.md). The original files were not kept, so the export has not been repeated from them.

- MIT end of life: 43 cells by three consecutive capacities below 0.88 Ah; 85 cells by the last recorded cycle (record ends at 0.8800-0.8834 Ah, never three values below 0.88 Ah); 12 excluded.
- MIT invalid values among 1282723 feature values of the included cells: 324 in leading rows of 36 cells (filled with the next valid value, i.e. backward), 51 later (filled with the previous valid value).
- mit: 9540 prediction times; at t = 30, 40, 50 (384 predictions, 4.0%) the blk scenario has no record before the outage: only the last three records are available, and the outage is the whole earlier history (27, 37, 47 cycles) rather than 50 cycles.
- xjtu: 1624 prediction times; at t = 30, 40, 50 (117 predictions, 7.2%) the blk scenario has no record before the outage: only the last three records are available, and the outage is the whole earlier history (27, 37, 47 cycles) rather than 50 cycles.
- XJTU per-cell table Batch-3 R2.5_battery-1 (592 rows) equals its rows in the merged table: True.

**Cleaning before deletion (check added after the runs).** MIT: 9540 prediction times. Windows containing a record whose filled value comes from a cycle that is not among the available records of the scenario: complete records 4, one record in 10 cycles 711 (7.5%), outage 8 (0.1%). Filled values taken from a cycle after the prediction time: 0. The battery check is therefore a missingness simulation on pre-cleaned tables.

## Table S34. Trade-off between the candidate training recipes: RMSE (cycles) by data source and scenario

From stored errors, no new experiment. C-MAPSS: mean over five seeds; DS03–DS08: mean unit RMSE. Best dense model: lowest RMSE among the densely trained models with or without test-time repair (A1, A2, A3 and the long-input model A6; A1 and A6 with complete records). Block outages: 10 and 20 cycles on C-MAPSS, 5 and 10 on DS03–DS08. The lowest value of a row is in bold.

| Data | Scenario | Best dense model | A5 (r = 0) | A5 (r*) | A8 | GEN |
|---|---|---|---|---|---|---|
| FD001 | complete records | 15.74 | 15.40 | 15.40 | 14.26 | **12.62** |
| FD001 | k = 5 | 18.20 | **13.21** | **13.21** | 14.58 | 14.47 |
| FD001 | irregular 1–5 | 16.58 | 13.29 | 13.29 | 12.89 | **12.87** |
| FD001 | block outage, shorter | 16.66 | 15.36 | 15.36 | 13.56 | **12.69** |
| FD001 | block outage, longer | 16.59 | 14.84 | 14.84 | 12.65 | **12.26** |
| FD002 | complete records | 15.66 | 14.64 | 14.64 | 12.79 | **12.59** |
| FD002 | k = 5 | 20.69 | **13.11** | **13.11** | 13.75 | 13.78 |
| FD002 | irregular 1–5 | 18.70 | 13.50 | 13.50 | 13.40 | **13.13** |
| FD002 | block outage, shorter | 16.19 | 14.67 | 14.67 | 13.59 | **13.54** |
| FD002 | block outage, longer | 17.82 | 15.36 | 15.36 | 15.06 | **14.55** |
| FD003 | complete records | 13.27 | 14.79 | 13.32 | 12.10 | **11.91** |
| FD003 | k = 5 | 15.79 | 14.46 | 14.60 | 14.80 | **14.10** |
| FD003 | irregular 1–5 | 17.07 | **13.31** | 13.65 | 13.88 | 14.05 |
| FD003 | block outage, shorter | 14.59 | 15.82 | 15.51 | 13.50 | **12.63** |
| FD003 | block outage, longer | 15.34 | 18.36 | 18.59 | 13.29 | **12.88** |
| FD004 | complete records | 16.74 | 15.56 | 15.18 | 13.45 | **13.38** |
| FD004 | k = 5 | 22.83 | **15.10** | 15.22 | 16.38 | 16.02 |
| FD004 | irregular 1–5 | 21.12 | **14.11** | 14.21 | 14.40 | 14.85 |
| FD004 | block outage, shorter | 17.10 | 16.07 | 15.89 | **14.08** | 14.19 |
| FD004 | block outage, longer | 18.74 | 17.24 | 17.28 | **14.91** | 15.17 |
| DS03–DS08 | complete records | 12.25 | 12.75 | 12.29 | 12.71 | **9.20** |
| DS03–DS08 | k = 5 | 16.56 | **8.60** | 9.08 | 10.63 | 10.22 |
| DS03–DS08 | irregular 1–5 | 15.18 | **9.43** | 10.30 | 10.20 | 9.66 |
| DS03–DS08 | block outage, shorter | 12.83 | 12.31 | 12.13 | 11.84 | **9.64** |
| DS03–DS08 | block outage, longer | 14.47 | 12.00 | 11.78 | 11.18 | **9.88** |

Lowest RMSE in the 25 rows: Best dense model 0, A5 (r = 0) 7, A5 (r*) 0, A8 2, GEN 16. Largest excess over the best arm of a row (cycles): Best dense model 7.95, A5 (r = 0) 5.47, A5 (r*) 5.70, A8 3.51, GEN 1.61.

## Table S35. All comparison arms

P: specified in the protocol before the experiment; E: exploratory. The main text (Table 1) lists the main arms only; Table 2 of the main text gives the exact generation rules.

| Case | Arm | Training windows | Test-time input | Status |
|---|---|---|---|---|
| 1 | A1 dense | consecutive cycles, 30 | last 30 records as they are | P |
| 1 | A2 dense + interpolation | as A1 (same models) | records interpolated to every cycle; last 30 cycles | P |
| 1 | A3 dense + carry-forward | as A1 | last record carried forward; last 30 cycles | P |
| 1 | A4 matched, no channel | sparse, 30 records | last 30 records | P |
| 1 | **A5 matched + gap channel** | sparse, 30 records, gap to previous record / 5 as extra channel | last 30 records + gaps | P (proposed) |
| 1 | A6 dense, long input | consecutive cycles, 150 | interpolated to every cycle; last 150 cycles | P |
| 1 | A7 interval-specific | one model per k | last 30 records | P |
| 1 | A8 matched, long input | 31 sparse records (30 gaps) interpolated to every cycle (span 30–150 cycles), padded to 150 | as A6 | E |
| 1 | A8F sparse, full span | sparse records interpolated to every cycle, covering 150 cycles | as A6 | E (control protocol) |
| 1 | A6S dense, A8's span | consecutive cycles over the span of an A8 window, padded to 150 | as A6 | E (control protocol) |
| 1 | A8B outage-aware | as A8; with probability 0.3 one gap lengthened by 5–20 cycles (3–10 on N-CMAPSS) | as A6 | E (upgrade protocol) |
| 1 | GEN generic deletion | every cycle but the last kept at random with a probability chosen to give about the record density of the deployment-like gap law; interpolated to every cycle, 150 | as A6 | E (step-3 protocol) |
| 1 | A6M smoothed dense | consecutive cycles, 150, trailing moving average of random width 1–5 | as A6 | E (step-3 protocol) |
| 1 | A5 with share r | as A5, with an additional complete window with probability r (0, 0.25, 0.5, 0.75); the gap law itself gives about 10% complete windows, so the actual shares are about 10%, 32.5%, 55% and 77.5% | as A5 | E (step-3 protocol) |
| 1 | GRU-D (adapted) | as A5; adaptation of [28]: decayed previous record and gap as extra inputs, hidden-state decay | as A5 | E |
| 1 | IMP imputer + dense | supervised masked imputer filling 30-cycle grids, then A1 | imputed grid | E |
| 1 | SNAP single record | one record → RUL (multilayer perceptron), after [35] without rectification | last record | E |
| 1 | PC-MambaSDE | authors' code [34], trained on A5's sparse windows with elapsed time as input | as A5 | E |
| 2 | S1 dense, repeat pad | consecutive cycles, 30 (= A1) | window filled by repeating the first available record | P |
| 2 | S2 dense, zero pad | as S1 | window filled with zeros (regime mean) | P |
| 2 | S3 truncation | last m cycles kept, repeat pad | as S1 | P |
| 2 | **S4 truncation + indicator** | as S3, plus a channel marking filled rows | as S1 + indicator | P (proposed) |
| 2 | S5 length-specific | one model per m | as S1 | P |
| 2 | S6 dense, long input | consecutive cycles, 150 (= A6) | as S1, 150 cycles | E (protocol appendix) |
| 2 | S8 truncation, long input | last m cycles kept, m from {3, …, 150}, 150-cycle input, no indicator | as S6 | E (protocol appendix) |
| 2 | S3E, S3L | as S3, but only windows with RUL above (S3E) or at or below (S3L) 60 cycles truncated (40 on N-CMAPSS) | as S1 | E (upgrade protocol) |
