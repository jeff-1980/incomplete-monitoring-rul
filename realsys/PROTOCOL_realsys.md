# Protocol: missingness simulation on real degradation data (lithium-ion cells)

Written 2026-11-17, before any model of this experiment was trained on these data for an accuracy figure. Before this file was frozen, only the structure of the tables was inspected (`inspect_structure.py`, `inspect_structure2.py`: columns, cycle counts, cycle types, invalid values, end-of-life coverage) and one smoke run was made (`rs.py ... smoke`: one epoch, prints array shapes and timing only, no error value). Checksums of this file and of the scripts are in `checksums_before_run.txt`.

## Purpose and name

A small closed check of whether the main findings obtained on simulated turbofan data carry over to run-to-failure records of real devices. The records are real; the missingness is simulated by deleting whole per-cycle records. It is therefore called a **missingness simulation on real degradation data**, not a field validation. Deleting a record means that the whole measurement of one charge–discharge cycle is unavailable; the raw signals within a cycle are not down-sampled.

## Data

Per-cycle summary tables exported earlier in this project from the public data sets.

* **MIT** (Severson et al. 2019; A123 LFP/graphite 1.1 Ah cells, 30 °C, 72 fast-charging policies, three batches). End of life: the first cycle from which three consecutive discharge capacities are below 0.88 Ah (80% of nominal); if this never occurs and the last recorded capacity is at most 0.885 Ah, the last recorded cycle. Cells that never reached this level are excluded (12 of 140; 128 cells remain, lives 148–1934 cycles, median 730). Records after the end of life are dropped. Source artefacts (any feature ≤ 0, capacity outside 0.55–1.43 Ah, charge time above 60 min) are replaced by the previous valid value of that cell. Features (13): discharge and charge capacity, internal resistance, mean, maximum and minimum temperature, charge time, charge and discharge energy, median and mean voltage of charge and of discharge.
* **XJTU** (Zenodo 10963339; 2.0 Ah NCM cells). Batches 1–4 (fixed-rate protocols; 39 cells, lives 131–799 cycles). Batches 5 and 6 are excluded a priori: their cycles follow a programmed variable load (random walk, satellite profile) that is not contained in the per-cycle table. The first cycle (initial capacity characterisation) is dropped. End of life: the last recorded cycle (the tests ended at 80% of nominal capacity). Features (10): discharge and charge capacity, mean and maximum temperature, charge and discharge energy, median and mean voltage of charge and of discharge.

Standardisation: z-score with the statistics of the training cells of the fit, for XJTU separately for each cycle type (batch × cycle description; the known operating condition, as the regime-wise standardisation of C-MAPSS), for MIT globally; clipped to ±10.

Target: remaining cycles to the end of life, capped at 450 (MIT) and 250 (XJTU), about 0.6 of the median life as the cap of 125 on C-MAPSS.

## Model and input (one backbone)

GRU(64) with the head, optimiser, batch size, 30 epochs and step rule of the paper. All models receive the same input: an every-cycle window of the last L = 200 cycles, obtained by linear interpolation between the available records (left-padded with the first value). One training window per cell and cycle.

## Three ways of training

* **DENSE**: complete windows.
* **GEN** (generic random deletion; the rule of step 3 with the largest gap doubled to 10): in each window every earlier cycle is kept independently with probability p, where p = 1/m with m uniform in 1…10 for half of the windows and p = 2/11 for the other half; the last cycle is kept.
* **MIX**: as GEN, but each window is complete with probability r. r is chosen again for each data set and fold from {0.25, 0.5, 0.75} on validation cells only (seed 0), by the mean of the validation RMSE with complete records and with one record every 10 cycles. The value 0.25 found on C-MAPSS is not carried over.

## Three evaluations

Predictions at cycles t = 30, 40, 50, … of every test cell, the same times in all scenarios.

* **full**: all records up to t.
* **k10** (sparse, at about the density of training): one record every 10 cycles. For DENSE this is the usual test-time remedy (linear interpolation).
* **blk** (missingness not seen in training): all records up to t − 53, then an outage of 50 cycles, then the last three cycles.

The density of one record in 10 cycles gives about 15–190 records per life, of the order of the 26–72 records per engine at one record in 5 cycles on C-MAPSS.

## Split by device

Five folds over cells, stratified by batch, assigned once with a fixed random seed (20261117). For test fold f, fold f+1 is the validation set for r; the final models are trained on the four non-test folds with seeds 0–4. No cell contributes to the training or the selection of a model that predicts it.

## Statistics and reading rules (fixed here)

Unit: the cell. For each cell, scenario and model the RMSE over its prediction times, averaged over the five seeds. Paired two-sided Wilcoxon tests over cells, percentile bootstrap intervals (10,000) for the mean difference. Per data set, Holm correction over three tests:

* R1: GEN against DENSE in k10 (does the gain carry over).
* R2: GEN against DENSE in blk (missingness not seen in training).
* R3a: MIX against DENSE in k10.

R3 (the mixture rule) holds on a data set if R3a is significant in favour of MIX and MIX is non-inferior to DENSE with complete records: upper limit of the 95% interval of the difference below 0.8% of the cap (3.6 cycles MIT, 2.0 cycles XJTU; the relative margin of step 3). The cost of GEN with complete records, MIX against GEN in k10 and MIX against DENSE in blk are reported descriptively. Pooled RMSE per seed (mean ± s.d.) is tabulated.

Overall reading for each of R1, R2, R3: "carried over" if it holds on both data sets, "carried over in part" if on one, "did not carry over" if on none. Inference is conditional on the trained models; the five folds use different models.

## Reporting

All results are reported whatever their direction. If there is no gain, the experiment is reported as a boundary of the findings; nothing is re-run with other settings, and no further variants are added to search for significance. Any deviation is recorded as an amendment with its reason.

Analysis script written before the runs: `analyse_realsys.py`.
