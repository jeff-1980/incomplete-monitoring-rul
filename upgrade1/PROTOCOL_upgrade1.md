# Protocol, upgrade step 1 (written 2026-11-16, before any run of ext.py or cmx.py)

Three questions, all with the unchanged base GRU and training settings (Adam 1e-3, batch 256, 30 epochs, no tuning), seeds 0-4.

## A. External cohort: N-CMAPSS DS03-DS08 (not used in this study so far)

Data inspection done before writing this protocol used features only, no model and no labels: across all 99 units of DS01-DS08, the median per-feature correlation over the first min(T1, T2) cycles is bimodal (43 pairs at 0.80 or above, all others below 0.40). Units linked by a correlation of 0.80 or above share a flight profile and form a profile group (21 groups with more than one unit; within DS01+DS02 only the three known twin pairs).

Design: fixed split, fixed models, no cross-validation.
- Training units: the official development units of DS03-DS08, except units in a profile group with any test unit (DS03 u5).
- Test units: the official test units of DS03-DS08, except units in a profile group with a DS01 or DS02 unit (DS03 u10, u11, u14, u15; DS08a u14), because DS01 and DS02 were used earlier. This leaves 27 test units.
- Experimental unit: the profile group among test units (DS05/DS06/DS07 u7, u8, u9, u10 form four groups of three), 19 groups.
- Features, window (10 records; long input 50), standardisation on training units, streaming predictions at every available record from cycle 10 on: as in the DS01+DS02 analyses.
- Score: RMSE of a unit over its predictions, averaged over the five seeds; group score = mean of its units. Tests: two-sided Wilcoxon signed-rank over the 19 groups, mean paired difference with 95% percentile bootstrap interval (10,000 resamples), Holm within each family.

Confirmatory hypotheses:
- E1 (case 1): A5 has lower error than the best of A1, A2, A3 (chosen by mean unit RMSE) at k = 5 and at irregular 1-5. Family of 2.
- E2 (case 2): S4 has lower error than the best of S1, S2 with the last 5 and the last 3 cycles. Family of 2.
- E3 (cost with complete records): A5 vs A1 at k = 1 and S4 vs S1 with the complete history; reported with interval; non-inferiority if the upper bound is below +1.0 cycle.
E1 (E2) is confirmed if both comparisons are Holm-significant in favour of A5 (S4). Results are reported whatever they show.

Secondary, uncorrected unless stated: A4, A6, A8, S3, S6, S8 in the same scenarios.

## B. Missingness mechanisms not seen in training

Block outage. All cycles are recorded except one block of B consecutive cycles just before the most recent records.
- C-MAPSS: the last 5 cycles are recorded, the B = 10 or 20 cycles before them are missing, earlier cycles are recorded.
- DS03-DS08: at prediction time t, cycles t-2..t are recorded, the B = 5 or 10 cycles before them are missing, earlier cycles are recorded; predictions at every t from cycle 10 on.
Regime-dependent missingness (C-MAPSS FD002 and FD004 only): the six operating regimes are ordered by the first operating setting of their cluster centre; a cycle in the three highest regimes is missing with probability 0.9, otherwise with probability 0.1 (generator seeded with 2000 + engine number); the last cycle is always recorded.

Arms: A1 (raw), A2 (interpolation), A3 (carry-forward), A5, A6, A8, all trained exactly as before (none saw such gaps), and A8B, a reference trained with knowledge of the mechanism: A8's gap law, and with probability 0.3 one gap of the window is lengthened by U{5..20} cycles (C-MAPSS) or U{3..10} (N-CMAPSS).

Comparisons (exploratory on C-MAPSS, whose test sets have been reused; DS03-DS08 as in part A): A5 and A8 each against the best of A1, A2, A3 (by RMSE); Holm over the 8 C-MAPSS block comparisons per arm (4 subsets x 2 block lengths), over the 2 regime comparisons per arm, and over the 2 DS03-DS08 block comparisons per arm. A8B vs A8 is reported.
Reading fixed in advance: "degraded training remains better under an unseen mechanism" if the arm is Holm-significantly better in at least 6 of 8 C-MAPSS block comparisons and in both DS03-DS08 block comparisons; if it is significantly worse than the best remedy anywhere, this is reported as a failure of transfer.

## C. Mechanism: does a dense model learn that padding means a healthy unit?

In standard training, padded windows occur only at the start of a trajectory, where RUL is high. Hypothesis: the model associates padding with high RUL, which produces over-estimation with short histories.
Manipulation of the association only (window 30 on C-MAPSS, 10 on N-CMAPSS; truncation length m drawn as for S3; no indicator channel):
- S1: no truncation (as before).
- S3: every training window truncated.
- S3E: only training windows with RUL above THR truncated (padding still tied to high RUL).
- S3L: only training windows with RUL at or below THR truncated (padding tied to low RUL).
THR = 60 cycles on C-MAPSS, 40 on N-CMAPSS.
Outcome: mean signed error (prediction minus truth) on units near end of life (true RUL at most 50 on C-MAPSS, at most 20 on N-CMAPSS) with short histories (last 10 and 5 cycles on C-MAPSS; last 5 and 3 on DS03-DS08), seed-averaged per engine (C-MAPSS) or per group (DS03-DS08, mean over the unit's predictions with RUL at most 20).
Prediction of the hypothesis: S3E > S3 > S3L in signed error. Supported if S3E minus S3L is positive and Holm-significant (two-sided Wilcoxon) in at least 6 of the 8 C-MAPSS comparisons and in both DS03-DS08 comparisons. If S3L over-estimates as much as S3E, the hypothesis is rejected. Reported whatever the result.

## Files
ext.py (DS03-DS08, parts A, B, C), cmx.py (C-MAPSS, parts B, C), analyse_upgrade1.py written before results are inspected. Checksums of this protocol and both training scripts are stored before the first run.
