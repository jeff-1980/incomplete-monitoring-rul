## Table S32. Q2 after correction: Holm-adjusted sparse-record comparisons, carry-forward included among the test-time remedies

Correction made after independent verification, without retraining. The best test-time remedy is the one of A1, A2 and A3 with the lowest RMSE (five seeds); the errors of A3 come from the five-seed runs of the same dense models. Holm adjustment within the eight C-MAPSS comparisons and within the two external-cohort comparisons of each row group. Δ in seed-averaged engine absolute error (C-MAPSS) or group RMSE (DS03–DS08), cycles.

RMSE of the remedies (A1 / A2 / A3): FD001 k = 5 24.93 / 21.07 / 21.97, irr 1–5 22.87 / 19.58 / 20.02; FD002 k = 5 20.69 / 21.73 / 22.49, irr 1–5 18.70 / 20.93 / 21.40; FD003 k = 5 35.62 / 16.85 / 18.00, irr 1–5 26.73 / 18.20 / 19.73; FD004 k = 5 29.37 / 24.11 / 23.94, irr 1–5 25.45 / 21.19 / 21.73; DS03–DS08 k = 5 16.56 / 19.44 / 19.70, irr 1–5 15.18 / 18.53 / 18.36.

**Models with the selected share r\*.**

| Data | r* | Gain, k = 5 | Gain, irr 1–5 |
|---|---|---|---|
| FD001 | 0.0 | -5.67 [-8.21, -3.24]; 68/100; p = 2.6e-05; Holm 0.0001; ref. A2 | -4.31 [-6.98, -1.75]; 60/100; p = 0.0078; Holm 0.016; ref. A2 |
| FD002 | 0.0 | -5.52 [-6.74, -4.35]; 185/259; p = 1.9e-16; Holm 1.5e-15; ref. A1 | -4.08 [-5.13, -3.06]; 195/259; p = 1.4e-15; Holm 8.3e-15; ref. A1 |
| FD003 | 0.25 | -2.32 [-4.27, -0.41]; 59/100; p = 0.021; Holm 0.021; ref. A2 | -2.89 [-5.03, -0.95]; 67/100; p = 0.002; Holm 0.0061; ref. A2 |
| FD004 | 0.25 | -6.51 [-8.21, -4.82]; 177/248; p = 2e-16; Holm 1.5e-15; ref. A3 | -4.57 [-6.14, -3.09]; 168/248; p = 9.3e-11; Holm 4.7e-10; ref. A2 |
| DS03–DS08 | 0.5 | -7.64 [-10.44, -4.88]; 18/19; p = 9.5e-05; Holm 0.00019; ref. A1 | -4.92 [-7.22, -2.66]; 14/19; p = 0.0012; Holm 0.0012; ref. A1 |

**All values of r** (Holm within each value of r).

| Data | r | Gain, k = 5 | Gain, irr 1–5 |
|---|---|---|---|
| FD001 | 0.0 (r*) | -5.67 [-8.21, -3.24]; 68/100; p = 2.6e-05; Holm 0.0001; ref. A2 | -4.31 [-6.98, -1.75]; 60/100; p = 0.0078; Holm 0.016; ref. A2 |
| FD001 | 0.25 | -5.67 [-8.20, -3.21]; 65/100; p = 5e-05; Holm 0.0002; ref. A2 | -4.41 [-7.17, -1.72]; 61/100; p = 0.0034; Holm 0.0067; ref. A2 |
| FD001 | 0.5 | -5.77 [-8.27, -3.34]; 65/100; p = 3.3e-05; Holm 0.00013; ref. A2 | -4.28 [-7.08, -1.55]; 56/100; p = 0.013; Holm 0.027; ref. A2 |
| FD001 | 0.75 | -5.29 [-7.62, -3.04]; 67/100; p = 2.4e-05; Holm 9.5e-05; ref. A2 | -4.43 [-7.13, -1.80]; 62/100; p = 0.0017; Holm 0.0051; ref. A2 |
| FD002 | 0.0 (r*) | -5.52 [-6.74, -4.35]; 185/259; p = 1.9e-16; Holm 1.3e-15; ref. A1 | -4.08 [-5.13, -3.06]; 195/259; p = 1.4e-15; Holm 8.3e-15; ref. A1 |
| FD002 | 0.25 | -4.88 [-6.14, -3.66]; 171/259; p = 2.7e-11; Holm 1.9e-10; ref. A1 | -3.53 [-4.61, -2.49]; 169/259; p = 1.3e-09; Holm 6.5e-09; ref. A1 |
| FD002 | 0.5 | -4.56 [-5.79, -3.36]; 167/259; p = 7e-11; Holm 4.9e-10; ref. A1 | -3.28 [-4.24, -2.31]; 164/259; p = 2.6e-09; Holm 1.6e-08; ref. A1 |
| FD002 | 0.75 | -4.40 [-5.54, -3.29]; 170/259; p = 1.3e-11; Holm 9.4e-11; ref. A1 | -3.01 [-3.95, -2.09]; 165/259; p = 4e-09; Holm 2.4e-08; ref. A1 |
| FD003 | 0.0 | -2.43 [-4.43, -0.45]; 62/100; p = 0.013; Holm 0.016; ref. A2 | -3.11 [-5.42, -1.07]; 67/100; p = 0.0022; Holm 0.0065; ref. A2 |
| FD003 | 0.25 (r*) | -2.32 [-4.27, -0.41]; 59/100; p = 0.021; Holm 0.021; ref. A2 | -2.89 [-5.03, -0.95]; 67/100; p = 0.002; Holm 0.0061; ref. A2 |
| FD003 | 0.5 | -1.85 [-3.82, +0.07]; 57/100; p = 0.061; Holm 0.061; ref. A2 | -2.79 [-4.95, -0.84]; 65/100; p = 0.0047; Holm 0.014; ref. A2 |
| FD003 | 0.75 | -1.03 [-3.05, +0.95]; 55/100; p = 0.33; Holm 0.33; ref. A2 | -2.49 [-4.74, -0.50]; 60/100; p = 0.038; Holm 0.075; ref. A2 |
| FD004 | 0.0 | -6.63 [-8.27, -4.96]; 187/248; p = 2e-17; Holm 1.6e-16; ref. A3 | -4.61 [-6.20, -3.14]; 163/248; p = 7.2e-11; Holm 3.6e-10; ref. A2 |
| FD004 | 0.25 (r*) | -6.51 [-8.21, -4.82]; 177/248; p = 2e-16; Holm 1.6e-15; ref. A3 | -4.57 [-6.14, -3.09]; 168/248; p = 9.3e-11; Holm 5.6e-10; ref. A2 |
| FD004 | 0.5 | -6.30 [-7.99, -4.62]; 186/248; p = 7.3e-16; Holm 5.8e-15; ref. A3 | -4.30 [-5.86, -2.85]; 162/248; p = 2.6e-09; Holm 1.6e-08; ref. A2 |
| FD004 | 0.75 | -5.96 [-7.57, -4.35]; 182/248; p = 8.9e-15; Holm 7.1e-14; ref. A3 | -3.99 [-5.51, -2.56]; 154/248; p = 2.9e-08; Holm 1.4e-07; ref. A2 |
| DS03–DS08 | 0.0 | -7.96 [-10.98, -5.05]; 18/19; p = 9.5e-05; Holm 0.00011; ref. A1 | -5.76 [-8.19, -3.59]; 17/19; p = 5.3e-05; Holm 0.00011; ref. A1 |
| DS03–DS08 | 0.25 | -7.79 [-10.83, -4.86]; 18/19; p = 7.2e-05; Holm 0.00014; ref. A1 | -5.24 [-7.71, -2.88]; 15/19; p = 0.00079; Holm 0.00079; ref. A1 |
| DS03–DS08 | 0.5 (r*) | -7.64 [-10.44, -4.88]; 18/19; p = 9.5e-05; Holm 0.00019; ref. A1 | -4.92 [-7.22, -2.66]; 14/19; p = 0.0012; Holm 0.0012; ref. A1 |
| DS03–DS08 | 0.75 | -6.88 [-9.65, -4.08]; 16/19; p = 0.00034; Holm 0.00067; ref. A1 | -4.69 [-6.98, -2.45]; 16/19; p = 0.0017; Holm 0.0017; ref. A1 |

Reading for Q2 with the corrected comparisons: FD001: r* = 0.0, non-inferior with complete records no, keeps sparse-record advantage (Holm) yes; FD002: r* = 0.0, non-inferior with complete records yes, keeps sparse-record advantage (Holm) yes; FD003: r* = 0.25, non-inferior with complete records yes, keeps sparse-record advantage (Holm) yes; FD004: r* = 0.25, non-inferior with complete records yes, keeps sparse-record advantage (Holm) yes; DS03–DS08: r* = 0.5, non-inferior with complete records yes, keeps sparse-record advantage (Holm) yes. The rule held on 4 of 5 data sources.

Actual share of complete training windows: r is the probability of the additional complete branch; the gap law itself yields a complete window with probability 0.10. r = 0.0: 10.0%; r = 0.25: 32.5%; r = 0.5: 55.0%; r = 0.75: 77.5%.
