## Table S36. N-CMAPSS external cohort: complete-record and sparse-record errors at the same prediction times

From stored predictions, no retraining. Streamed prediction times differ between scenarios: every cycle from the tenth with complete records and under block outages, the record cycles with sparse records. The columns "complete, same times" restrict the complete-record predictions to the prediction times of the sparse scenario (identical times and targets, checked). Mean unit RMSE in cycles, five seeds.

| Arm | Complete, all times | Complete, times of k = 5 | k = 5 | Complete, times of irr 1–5 | irr 1–5 |
|---|---|---|---|---|---|
| A1 | 13.78 | 14.05 | 16.56 | 13.74 | 15.18 |
| A2 | 13.78 | 14.05 | 19.44 | 13.74 | 18.53 |
| A3 | 13.78 | 14.05 | 19.70 | 13.74 | 18.36 |
| A5 | 12.72 | 12.65 | 8.59 | 12.56 | 9.42 |
| A6 | 12.25 | 12.48 | 23.02 | 12.29 | 20.04 |
| A8 | 12.71 | 12.93 | 10.63 | 12.75 | 10.20 |

Dense model A1: 13.78 cycles with complete records at all times, 14.05 at the times of k = 5 and 13.74 at the times of irr 1–5; best test-time remedy 16.56 at k = 5 and 15.18 at irr 1–5. The increase of the error from complete to sparse records at identical prediction times is +2.51 and +1.44 cycles (with all complete-record times: +2.78 and +1.40). Comparisons between arms within a scenario (E1, E2 and all paired tests) use identical prediction times and are not affected.
