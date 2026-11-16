## Table S16. Confirmatory comparisons by training seed

Case 1, C-MAPSS (three seeds): A5 minus the best test-time remedy. ΔRMSE per seed; ΔMAE per seed; mean ΔRMSE with 95% engine-bootstrap interval (conditional on the trained models).

| Subset | Scenario | Reference | ΔRMSE per seed | ΔMAE per seed | Seeds A5 better | Mean ΔRMSE [95% CI] |
|---|---|---|---|---|---|---|
| FD001 | k5 | A2 | -7.69, -8.99, -7.19 | -5.69, -5.82, -5.20 | 3/3 | -7.96 [-11.16, -4.55] |
| FD001 | irr5 | A2 | -5.74, -7.46, -6.29 | -4.29, -5.29, -3.53 | 3/3 | -6.49 [-10.36, -2.61] |
| FD002 | k5 | A1 | -6.92, -9.21, -7.07 | -5.11, -6.80, -5.05 | 3/3 | -7.74 [-9.35, -6.12] |
| FD002 | irr5 | A1 | -5.43, -7.08, -5.18 | -4.07, -5.25, -3.50 | 3/3 | -5.90 [-7.20, -4.62] |
| FD003 | k5 | A2 | -2.57, -2.30, -3.05 | -2.64, -2.46, -2.55 | 3/3 | -2.64 [-4.97, -0.43] |
| FD003 | irr5 | A2 | -4.68, -4.39, -5.08 | -2.48, -3.49, -3.42 | 3/3 | -4.72 [-8.34, -1.34] |
| FD004 | k5 | A2 | -8.70, -9.85, -6.26 | -6.58, -6.76, -4.91 | 3/3 | -8.27 [-11.13, -5.41] |
| FD004 | irr5 | A2 | -8.08, -7.84, -6.41 | -5.14, -5.16, -3.77 | 3/3 | -7.44 [-10.50, -4.65] |

Case 1, N-CMAPSS (twins grouped, three seeds): A5 minus A2; per-seed difference of the equal-weight group mean of unit RMSE.

| Scenario | Δ per seed | Seeds A5 better | Unit-weighted means A5 / A2 | Equal-group-weight means A5 / A2 | Δ (group, seed-averaged) |
|---|---|---|---|---|---|
| k5 | -2.97, -2.14, -2.72 | 3/3 | 7.88 / 10.34 | 8.01 / 10.62 | -2.61 |
| irr5 | -2.31, -1.55, -2.15 | 3/3 | 7.96 / 9.87 | 8.10 / 10.10 | -2.00 |

Case 2, C-MAPSS (five seeds): S4 minus the better of S1/S2.

| Subset | History | Reference | ΔRMSE per seed | Seeds S4 better | Mean ΔRMSE [95% CI] |
|---|---|---|---|---|---|
| FD001 | last 10 | S2 | -9.87, -8.55, -8.23, -7.13, -8.46 | 5/5 | -8.45 [-12.12, -4.41] |
| FD001 | last 5 | S1 | -9.22, -7.65, -9.12, -8.16, -8.12 | 5/5 | -8.45 [-12.31, -4.76] |
| FD002 | last 10 | S2 | -4.83, -7.41, -3.34, -5.48, -4.37 | 5/5 | -5.09 [-6.87, -3.32] |
| FD002 | last 5 | S2 | -6.70, -4.81, -2.32, -3.48, -1.52 | 5/5 | -3.76 [-5.26, -2.26] |
| FD003 | last 10 | S1 | -12.28, -12.71, -12.44, -9.92, -12.13 | 5/5 | -11.90 [-14.95, -8.86] |
| FD003 | last 5 | S2 | -16.81, -14.54, -11.58, -13.83, -11.69 | 5/5 | -13.69 [-17.72, -10.04] |
| FD004 | last 10 | S1 | -7.47, -4.57, -6.35, -9.99, -9.98 | 5/5 | -7.67 [-10.05, -5.34] |
| FD004 | last 5 | S2 | -2.81, -4.50, -5.30, -9.20, -4.09 | 5/5 | -5.18 [-7.14, -3.23] |

Case 2, N-CMAPSS (twins grouped, five seeds): S4 minus the better of S1/S2 (chosen on unit-weighted mean RMSE).

| History | Reference | Δ per seed | Seeds S4 better | Unit-weighted means S4 / ref | Equal-group-weight means S4 / ref | Δ (group, seed-averaged) |
|---|---|---|---|---|---|---|
| last 5 | S1 | -2.43, -1.73, -2.40, -2.70, -1.99 | 5/5 | 8.15 / 10.15 | 8.23 / 10.48 | -2.25 |
| last 3 | S1 | -3.47, -2.44, -3.36, -3.50, -2.91 | 5/5 | 8.53 / 11.40 | 8.65 / 11.79 | -3.14 |

## Table S17. Complete records: long-input variants against the dense model (exploratory non-inferiority)

ΔMAE: seed-averaged engine absolute error, variant minus dense model, 95% engine-bootstrap interval. ΔRMSE: mean over seeds of the RMSE difference, 95% engine-bootstrap interval. "Within 1 cycle": upper bound of the interval below +1.0 cycle.

| Subset | Comparison | ΔMAE [95% CI] | ΔRMSE [95% CI] | Within 1 cycle (MAE / RMSE) |
|---|---|---|---|---|
| FD001 | A8 vs A1 | -0.93 [-3.22, +1.22] | -1.78 [-4.83, +1.07] | no / no |
| FD001 | S8 vs S1 | -1.57 [-3.12, -0.18] | -2.25 [-4.55, +0.07] | yes / yes |
| FD001 | A5 vs A1 | -0.38 [-1.71, +0.90] | -1.33 [-2.94, +0.29] | yes / yes |
| FD001 | S4 vs S1 | -0.55 [-1.94, +0.84] | -1.03 [-2.97, +0.94] | yes / yes |
| FD002 | A8 vs A1 | -2.58 [-3.69, -1.53] | -4.72 [-6.27, -3.16] | yes / yes |
| FD002 | S8 vs S1 | -1.42 [-2.42, -0.44] | -2.09 [-3.61, -0.57] | yes / yes |
| FD002 | A5 vs A1 | -1.33 [-2.10, -0.56] | -2.63 [-3.69, -1.57] | yes / yes |
| FD002 | S4 vs S1 | +0.57 [-0.18, +1.29] | +0.23 [-0.78, +1.20] | no / no |
| FD003 | A8 vs A1 | -0.66 [-2.02, +0.65] | -1.17 [-3.54, +1.01] | yes / no |
| FD003 | S8 vs S1 | -0.35 [-1.43, +0.67] | -0.57 [-2.61, +1.18] | yes / no |
| FD003 | A5 vs A1 | +1.66 [+0.84, +2.53] | +1.60 [+0.61, +2.67] | no / no |
| FD003 | S4 vs S1 | +0.89 [+0.03, +1.77] | +0.43 [-1.07, +2.02] | no / no |
| FD004 | A8 vs A1 | -2.89 [-3.90, -1.86] | -4.25 [-5.61, -2.87] | yes / yes |
| FD004 | S8 vs S1 | -2.12 [-3.10, -1.12] | -2.66 [-4.06, -1.26] | yes / yes |
| FD004 | A5 vs A1 | -1.17 [-1.97, -0.39] | -2.21 [-3.45, -1.03] | yes / yes |
| FD004 | S4 vs S1 | -0.90 [-1.62, -0.18] | -1.47 [-2.54, -0.40] | yes / yes |

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
