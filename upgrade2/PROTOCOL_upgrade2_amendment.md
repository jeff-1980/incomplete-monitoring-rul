# Amendment to PROTOCOL_upgrade2.md (written 2026-11-17, after the step-2 results were known)

Problem found in review: for the external cohort, the validation units used to select width and learning rate were "every fifth eligible development unit". Four of these ten units (DS05 u2, DS06 u1, DS06 u6, DS07 u5) share a flight profile with units kept in the selection-training set. The final training set and the test units share no profile, so this is not test leakage, but the validation scores were optimistic and may have affected the choice of configuration.

Correction, fixed before it was run:
- Validation units are whole profile groups: the 35 profile groups of the eligible development units are sorted by name and every fifth group is held out (7 groups, 9 units).
- Selection is repeated for both backbones and all five arms with the same grid, seed and procedure (bb_e2.py).
- An arm whose selected configuration is unchanged keeps its original final models and results. An arm whose configuration changes is retrained with seeds 0-4 on the same training windows as before and its results replace the original ones; the original results are kept in the archive (results/bbe_*.json) and reported as superseded.
- The analysis script and the reading rule are unchanged. C-MAPSS is not affected (engines within a subset are independent) and the GRU was not tuned.
