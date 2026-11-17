# Protocol, upgrade step 3 (written 2026-11-17, before any run of q3g.py or extg.py)

Three questions about deployment-matched window training (DMWT) for sparse records. Base GRU, Adam 1e-3, batch 256, 30 epochs, seeds 0-4, as before. C-MAPSS FD001-FD004 (exploratory: test sets reused) and the external cohort N-CMAPSS DS03-DS08 (fixed split, 19 profile groups). Statistics as before: seed-averaged engine absolute error (C-MAPSS) or group RMSE (external cohort), two-sided Wilcoxon, 95% bootstrap interval, Holm within each family of 8 C-MAPSS comparisons (4 subsets x k = 5 and irregular 1-5) and each family of 2 external-cohort comparisons.

## Q1. Does matching the sampling structure add anything to generic random deletion?
All arms: long every-cycle input (150 cycles; 50 on N-CMAPSS), records interpolated to every cycle, windows covering the full span, same prediction endpoint and target, same budget.
- A6: consecutive cycles (no deletion).
- GEN: generic random deletion. Every cycle of the window except the last is kept independently with probability p; with probability 0.5, p = 1/k with k drawn uniformly from 1-5, otherwise p = 1/3. The expected number of records therefore matches DMWT in both halves of its law, but gaps are geometric and no window is regularly spaced (except p = 1).
- A8F: DMWT gap law (with probability 0.5 one regular interval k from 1-5, otherwise independent gaps from 1-5), as in the span control.
Test scenarios: k = 1, k = 5, irregular 1-5, block outages (as in step 1), and "random deletion" (each cycle but the last kept with probability 1/3; generator seeded by engine or unit).
Comparisons: (a) GEN vs A6, (b) A8F vs GEN, at k = 5 and irregular 1-5.
Reading fixed in advance: "exposure to deletion is enough" if GEN is Holm-significantly better than A6 in at least 6 of 8 C-MAPSS comparisons and A8F is not significantly better than GEN in more than 2 of 8; "matching the sampling structure adds value" if A8F is significantly better than GEN in at least 6 of 8 C-MAPSS comparisons and in both external-cohort comparisons; otherwise "partial", reported by scenario (regular and irregular spacing separately). If GEN and A8F do not differ, the contribution is narrowed accordingly.

## Q2. How should complete and sparsified windows be mixed in training?
Gap-channel model (A5: 30 records, gap channel), the variant that showed a cost with complete records. Each training window is complete with probability r and otherwise drawn from the DMWT gap law; r in {0, 0.25, 0.5, 0.75} (r = 0 is A5; the law itself yields about 10% complete windows).
Evaluation: cost with complete records (k = 1, against the dense model A1), gain with sparse records (k = 5, irregular 1-5, against r = 0 and against the best test-time remedy), block outages.
Selection rule, validation only: on validation units held out from the training data (C-MAPSS: random 20% of training engines, generator seed 12345; external cohort: every fifth profile group), with seed 0, r* is the value minimising the mean of the validation RMSE with complete records and the validation RMSE at k = 5. Test data are not read for selection. All four values are then trained on all training units with seeds 0-4 and all are reported; r* is evaluated as the frozen choice.
Reading fixed in advance: the rule "works" on a data set if the model with r* (i) is non-inferior to A1 with complete records (upper bound of the 95% interval below +1.0 cycle) and (ii) keeps the sparse-record advantage (significantly better than the best test-time remedy at k = 5 and at irregular 1-5). Reported per subset; the trade-off curve over r is reported whatever the outcome, and no claim is made that the complete-record cost can be removed.

## Q3. Does smoothness of the training input explain part of the sparse-record gain?
Hypothesis: interpolated sparse windows are smoother than consecutive-cycle windows, and a model trained on smooth windows handles them better. Arms with the same long input, span, target and budget:
- A6: consecutive cycles.
- A6M: consecutive cycles smoothed without deleting any record: trailing moving average of width m over the window, m drawn like the mean gap of the DMWT law (with probability 0.5 uniform on 1-5, otherwise 3).
- A8F: sparsified and interpolated (DMWT).
Comparisons at k = 5 and irregular 1-5: (a) A6M vs A6, (b) A8F vs A6M; share of the A8F gain over A6 that A6M recovers (ratio of mean differences).
Reading fixed in advance: "smoothing explains part of the gain" if A6M is Holm-significantly better than A6 in at least 6 of 8 C-MAPSS comparisons; "explains most of it" if in addition A8F is significantly better than A6M in at most 2 of 8; "not supported" if A6M is significantly better than A6 in at most 2 of 8, in which case the smoothing explanation is withdrawn from the paper. Smoothing also changes the information in the input, so no claim of a unique mechanism is made.

## Files
q3g.py (C-MAPSS), extg.py (external cohort), analyse_upgrade3.py. Checksums are stored before the first run. Results are reported whatever they show.
