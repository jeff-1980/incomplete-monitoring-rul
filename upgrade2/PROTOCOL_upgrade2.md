# Protocol, upgrade step 2: other backbones (written 2026-11-16, before any run of bb_c.py or bb_e.py)

Question: does the effect of the training distribution (dense versus deployment-like degraded windows) hold for backbones other than the GRU?

## Backbones
- TCN: five residual blocks of two causal 1-D convolutions (kernel 3, dilations 1, 2, 4, 8, 16), width c, output of the last time step, head c-32-1.
- Transformer: linear embedding to width c, learned positional embedding, two encoder layers (4 heads, feed-forward 2c, dropout 0.1), output of the last position, head c-32-1.
Inputs, windows, degradation laws, targets, loss (MSE on RUL/125), Adam, batch 256, 30 epochs and steps per epoch are those of the GRU experiments.

## Hyperparameters: validation only, same opportunity for every arm
Grid: width c in {32, 64} x learning rate in {1e-3, 3e-4} (four configurations). For each backbone, data set and arm separately, the configuration is chosen once, with seed 0, by the RMSE on validation units held out from the training data (C-MAPSS: a random 20% of training engines, generator seed 12345; DS03-DS08: every fifth eligible development unit), with validation windows built by the arm's own training law. Test data are not read during selection. The chosen configuration is then trained on all training units with seeds 0-4.

## Arms and scenarios
Arms (as defined for the GRU): A1 dense (= S1), A5, A6 dense long input, A8, S4. Test-time remedies use the dense model: A2 interpolation, A3 carry-forward, S2 zero padding.
- C-MAPSS FD001-FD004: case 1 at k = 1, k = 5, irregular 1-5; case 2 with complete history, last 10, last 5.
- External cohort DS03-DS08 (fixed split as in step 1): case 1 at k = 1, k = 5, irregular 1-5; case 2 complete, last 5, last 3.

## Comparisons, per backbone (statistics as before; C-MAPSS exploratory because its test sets were reused; DS03-DS08 group-level)
- G1 (case 1): A5 versus the best of A1, A2, A3 (by RMSE) at k = 5 and irregular 1-5. Holm over 8 C-MAPSS comparisons; Holm over 2 external-cohort comparisons.
- G2 (same input): A8 versus A6 at k = 5 and irregular 1-5, same families.
- G3 (case 2): S4 versus the better of S1, S2 with the last 10 and 5 cycles (C-MAPSS) and the last 5 and 3 (external cohort), same families.
- Cost with complete records: A5 versus A1 at k = 1, S4 versus S1 with the complete history; interval reported.

Reading fixed in advance, per backbone and per comparison G1, G2, G3: the effect "carries over to the backbone" if the degraded-training arm is Holm-significantly better in at least 6 of the 8 C-MAPSS comparisons and in both external-cohort comparisons; "partly" if only one of the two conditions holds; otherwise "does not carry over". Results are reported whatever they show, next to the GRU results.

## Files
bbm.py (models, training), bb_c.py (C-MAPSS), bb_e.py (DS03-DS08), analyse_upgrade2.py. Checksums stored before the first run. A shape test of the models on random tensors was run beforehand; no data were involved.
