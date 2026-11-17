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
