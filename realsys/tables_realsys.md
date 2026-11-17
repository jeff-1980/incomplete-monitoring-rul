## mit: 128 cells, selected share per fold [0.75, 0.5, 0.25, 0.75, 0.75]
| Scenario | DENSE | GEN | MIX |
|---|---|---|---|
| full | 34.6 ± 2.5 | 33.6 ± 1.6 | 34.1 ± 1.9 |
| k10 | 34.0 ± 2.7 | 33.3 ± 1.6 | 33.8 ± 1.7 |
| blk | 35.5 ± 2.4 | 33.7 ± 1.5 | 34.6 ± 1.9 |

Paired differences in cell RMSE (cycles; negative: first arm better); non-inferiority margin 3.6 cycles
| Comparison | Δ | 95% CI | p | Holm | cells better |
|---|---|---|---|---|---|
| R1 GEN vs DENSE, k10 | -1.28 | -2.56 to +0.04 | 0.0088 | 0.018 | 73/128 |
| R2 GEN vs DENSE, blk | -2.41 | -3.68 to -1.12 | 1.7e-05 | 5.1e-05 | 83/128 |
| R3 MIX vs DENSE, k10 | -0.72 | -1.68 to +0.33 | 0.047 | 0.047 | 76/128 |
| cost GEN vs DENSE, full | -1.13 | -2.39 to +0.17 | 0.033 | nan | 74/128 |
| cost MIX vs DENSE, full | -0.61 | -1.60 to +0.42 | 0.21 | nan | 71/128 |
| MIX vs GEN, k10 | +0.56 | -0.27 to +1.44 | 0.36 | nan | 62/128 |
| MIX vs DENSE, blk | -1.45 | -2.44 to -0.43 | 0.0036 | nan | 79/128 |

Reading: {'R1': True, 'R2': True, 'R3': True}

## xjtu: 39 cells, selected share per fold [0.75, 0.75, 0.25, 0.75, 0.75]
| Scenario | DENSE | GEN | MIX |
|---|---|---|---|
| full | 24.9 ± 0.8 | 23.7 ± 0.8 | 23.5 ± 0.7 |
| k10 | 25.1 ± 0.7 | 23.8 ± 0.7 | 23.7 ± 0.6 |
| blk | 26.1 ± 0.4 | 24.1 ± 0.9 | 24.1 ± 0.8 |

Paired differences in cell RMSE (cycles; negative: first arm better); non-inferiority margin 2.0 cycles
| Comparison | Δ | 95% CI | p | Holm | cells better |
|---|---|---|---|---|---|
| R1 GEN vs DENSE, k10 | -2.50 | -4.76 to -0.61 | 0.014 | 0.027 | 27/39 |
| R2 GEN vs DENSE, blk | -3.72 | -6.28 to -1.58 | 2.6e-05 | 7.7e-05 | 32/39 |
| R3 MIX vs DENSE, k10 | -2.30 | -4.56 to -0.41 | 0.031 | 0.031 | 25/39 |
| cost GEN vs DENSE, full | -2.19 | -4.17 to -0.57 | 0.012 | nan | 26/39 |
| cost MIX vs DENSE, full | -2.11 | -4.14 to -0.38 | 0.043 | nan | 24/39 |
| MIX vs GEN, k10 | +0.19 | -0.60 to +0.89 | 0.22 | nan | 15/39 |
| MIX vs DENSE, blk | -3.48 | -6.08 to -1.34 | 0.00016 | nan | 31/39 |

Reading: {'R1': True, 'R2': True, 'R3': True}

Overall: {'R1': 'carried over', 'R2': 'carried over', 'R3': 'carried over'}
