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
