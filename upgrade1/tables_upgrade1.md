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
| E1 (confirmatory) | k5 | A5 | A1 | -8.21 [-11.25, -5.24]; 18/19; p = 7.2e-05; Holm 0.00011 | -10.13, -7.02, -8.32, -6.23, -9.36 |
| E1 (confirmatory) | irr5 | A5 | A1 | -5.88 [-8.13, -3.75]; 17/19; p = 5.3e-05; Holm 0.00011 | -7.76, -4.30, -7.60, -2.98, -6.79 |
| E2 (confirmatory) | h5 | S4 | S2 | -1.09 [-2.17, +0.04]; 14/19; p = 0.049; Holm 0.065 | -1.09, -0.34, -2.96, -0.81, -0.23 |
| E2 (confirmatory) | h3 | S4 | S2 | -1.13 [-2.20, +0.03]; 14/19; p = 0.032; Holm 0.065 | -0.59, -0.93, -3.02, -1.05, -0.08 |
| secondary | k5 | A8 | A1 | -6.12 [-9.03, -3.21]; 16/19; p = 0.00064; Holm 0.0013 | -8.16, -6.13, -5.04, -4.32, -6.97 |
| secondary | irr5 | A8 | A1 | -5.01 [-7.44, -2.76]; 16/19; p = 0.00097; Holm 0.0013 | -7.00, -4.21, -4.92, -2.97, -5.96 |
| secondary | h5 | S8 | S2 | +1.40 [+0.28, +2.50]; 6/19; p = 0.04; Holm 0.052 | +1.37, +2.04, +0.70, +1.28, +1.59 |
| secondary | h3 | S8 | S2 | +1.74 [+0.36, +3.08]; 6/19; p = 0.026; Holm 0.052 | +2.63, +2.00, +0.75, +1.38, +1.92 |
| block outage | blk5 | A5 | A1 | -1.70 [-2.66, -0.66]; 17/19; p = 0.0039; Holm 0.0039 | -2.49, -0.45, -2.02, -1.56, -2.00 |
| block outage | blk10 | A5 | A1 | -2.49 [-3.55, -1.39]; 17/19; p = 0.0012; Holm 0.0023 | -3.58, -1.14, -2.81, -1.89, -3.01 |
| block outage | blk5 | A8 | A1 | -2.41 [-4.19, -0.60]; 14/19; p = 0.023; Holm 0.023 | -3.59, -2.03, -2.46, -1.60, -2.35 |
| block outage | blk10 | A8 | A1 | -3.39 [-5.04, -1.71]; 16/19; p = 0.002; Holm 0.004 | -4.63, -2.47, -3.95, -2.09, -3.79 |
| E3 cost, complete records | k1 | A5 | A1 | -0.69 [-1.71, +0.52]; 14/19; p = 0.08; non-inferior (1 cycle): yes | |
| E3 cost, complete records | full | S4 | S1 | -1.65 [-2.47, -0.83]; 17/19; p = 0.0014; non-inferior (1 cycle): yes | |
| E3 cost, complete records | k1 | A8 | A1 | -1.07 [-3.06, +0.72]; 10/19; p = 0.47; non-inferior (1 cycle): yes | |
| E3 cost, complete records | full | S8 | S1 | -1.47 [-2.31, -0.65]; 15/19; p = 0.0082; non-inferior (1 cycle): yes | |
| reference trained with outages | blk5 | A8B | A8 | +0.31 [-0.02, +0.64]; 7/19; p = 0.096 | |
| reference trained with outages | blk10 | A8B | A8 | -0.04 [-0.38, +0.31]; 11/19; p = 0.62 | |
| reference trained with outages | k5 | A8B | A8 | -0.10 [-0.54, +0.36]; 11/19; p = 0.65 | |
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
| A5 | FD001 | blk10 | A1 | -1.92 [-3.41, -0.53]; 58/100; p = 0.048; Holm 0.14 |
| A5 | FD001 | blk20 | A1 | -4.13 [-5.93, -2.44]; 66/100; p = 4.8e-05; Holm 0.00033 |
| A5 | FD002 | blk10 | A1 | -2.14 [-3.04, -1.26]; 148/259; p = 0.00029; Holm 0.0018 |
| A5 | FD002 | blk20 | A1 | -2.47 [-3.43, -1.51]; 165/259; p = 3.5e-06; Holm 2.8e-05 |
| A5 | FD003 | blk10 | A1 | -0.90 [-2.25, +0.45]; 54/100; p = 0.33; Holm 0.65 |
| A5 | FD003 | blk20 | A2 | +0.26 [-2.06, +2.57]; 42/100; p = 0.52; Holm 0.65 |
| A5 | FD004 | blk10 | A1 | -1.15 [-2.02, -0.30]; 134/248; p = 0.028; Holm 0.11 |
| A5 | FD004 | blk20 | A1 | -1.77 [-2.99, -0.56]; 140/248; p = 0.0057; Holm 0.029 |
| A5 | FD002 | reg | A1 | -3.81 [-4.86, -2.85]; 173/259; p = 9e-11; Holm 1.8e-10 |
| A5 | FD004 | reg | A3 | -3.65 [-4.84, -2.47]; 163/248; p = 7.6e-10; Holm 7.6e-10 |
| A8 | FD001 | blk10 | A1 | -2.25 [-3.99, -0.55]; 63/100; p = 0.0077; Holm 0.015 |
| A8 | FD001 | blk20 | A1 | -4.58 [-6.50, -2.74]; 71/100; p = 1.8e-05; Holm 0.00011 |
| A8 | FD002 | blk10 | A1 | -2.55 [-3.63, -1.49]; 149/259; p = 0.00047; Holm 0.0024 |
| A8 | FD002 | blk20 | A1 | -2.16 [-3.41, -0.95]; 149/259; p = 0.0021; Holm 0.0074 |
| A8 | FD003 | blk10 | A1 | -2.00 [-3.53, -0.47]; 56/100; p = 0.048; Holm 0.048 |
| A8 | FD003 | blk20 | A2 | -3.35 [-5.34, -1.50]; 63/100; p = 0.0018; Holm 0.0074 |
| A8 | FD004 | blk10 | A1 | -2.75 [-3.71, -1.78]; 173/248; p = 3e-10; Holm 2.4e-09 |
| A8 | FD004 | blk20 | A1 | -3.12 [-4.24, -2.03]; 156/248; p = 5e-07; Holm 3.5e-06 |
| A8 | FD002 | reg | A1 | -4.25 [-5.29, -3.29]; 178/259; p = 2.8e-14; Holm 4.2e-14 |
| A8 | FD004 | reg | A3 | -4.31 [-5.48, -3.17]; 180/248; p = 2.1e-14; Holm 4.2e-14 |

A5: C-MAPSS block 4/8 significantly better (0 worse); regime 2/2; DS03–DS08 block 2/2. Pre-specified reading 'remains better under an unseen mechanism': False.

A8: C-MAPSS block 8/8 significantly better (0 worse); regime 2/2; DS03–DS08 block 2/2. Pre-specified reading 'remains better under an unseen mechanism': True.

A8B (trained with outages) minus A8, C-MAPSS block scenarios: FD001 blk10 -0.26 (p = 0.49); FD001 blk20 -0.03 (p = 0.81); FD002 blk10 -0.19 (p = 0.52); FD002 blk20 -0.11 (p = 0.38); FD003 blk10 -0.19 (p = 0.16); FD003 blk20 -0.21 (p = 0.31); FD004 blk10 +0.37 (p = 0.0054); FD004 blk20 -0.04 (p = 0.86).

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
