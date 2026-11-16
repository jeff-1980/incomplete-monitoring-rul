# Protocol: A8 history-span control (written 2026-11-16, before any run of q3e.py)

## Why
Source-code audit: A8's training windows hold 30 sparse records interpolated to every cycle (span 30-150 cycles, padded to 150 by repeating the first record), whereas A6's hold up to 150 consecutive cycles. A8 vs A6 therefore confounds sparsification with a shorter, padded training history.

## Arms (C-MAPSS FD001-FD004, seeds 0-4, same base GRU, Adam 1e-3, batch 256, 30 epochs; all trained in one run)
- A1: dense, 30 consecutive cycles (reference for complete records).
- A6: dense, up to 150 consecutive cycles, padded only at trajectory start (as before).
- A8: as before (30 sparse records, interpolated, padded to 150).
- A8F (new): sparse records drawn with the same gap law (probability 0.5 one regular k from 1-5, else iid 1-5) but as many records as needed to cover the 150-cycle window; interpolated; padded only at trajectory start. Sparsified, full span.
- A6S (new): for each example the gaps of an A8 window are drawn as for A8, giving its span L; the window holds the last L consecutive cycles (no sparsification) padded to 150. Dense, A8's span and padding.

Test-time input for A6, A8, A8F, A6S: the available records interpolated to every cycle, last 150 cycles (identical inputs). A1 receives the last 30 records. Test gap patterns as in all earlier runs (irregular: generator seeded by engine number).

## Comparisons
Exploratory; engine-level seed-averaged absolute error, two-sided Wilcoxon, 95% bootstrap CI; Holm within each family of 8 (4 subsets x k = 5 and irregular 1-5).
- C1 sparsification with full span: A8F vs A6.
- C2 sparsification with A8's span and padding: A8 vs A6S.
- C3 shorter padded windows without sparsification: A6S vs A6.
- C4 span with sparsification: A8F vs A8.
All six scenarios and complete records (k = 1, including A8F and A6S vs A1) are reported; RMSE mean and s.d. over seeds.

## Interpretation fixed in advance
- C1 and C2 both favour the sparsified arm (at least 6 of 8 Holm-significant each): sparsification itself carries the gain; the paper may say so.
- C3 favours A6S while C1 and C2 do not: the gain comes mainly from short padded training windows; the paper must say so.
- Mixed results: reported as such; no claim that either component explains the gain.

Results are reported whatever they show, in the supplement and in section 4.3.
