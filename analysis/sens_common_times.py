"""Sensitivity analysis from stored predictions (no retraining): on N-CMAPSS the streamed prediction times differ between scenarios
(complete records: every cycle t >= 10; k = 5: record cycles 10, 15, ...; irregular: the unit's record cycles; block outage: every t >= 10).
Here the complete-record errors are restricted to the prediction times of the sparse scenario, so that both refer to the same times and targets.
External cohort DS03-DS08, five seeds; mean over units of the seed-averaged unit RMSE. Output: analysis/tables_common_times.md"""
import json, os, numpy as np
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); rm = lambda e: float(np.sqrt(np.mean(np.square(e)))); KMAX = 5
E = [json.load(open(f'{B}/upgrade1/results/ext_s{s}.json')) for s in range(5)]; units = sorted(E[0])   # sorted(TEST) is the order used for the generator seeds in ext.py
def times(u, ui, sc):
    T = len(E[0][u]['k1']['y']) + 10                       # complete records: one prediction at every t = 10 .. T-1
    if sc == 'k5': obs = np.arange(0, T, 5)
    else: c = np.cumsum(np.r_[0, np.random.default_rng(1000 + ui).integers(1, KMAX + 1, T)]); obs = c[c < T]
    return obs[obs >= 10]
L = ['## Table S36. N-CMAPSS external cohort: complete-record and sparse-record errors at the same prediction times\n',
     'From stored predictions, no retraining. Streamed prediction times differ between scenarios: every cycle from the tenth with complete records and under block outages, the record cycles with sparse records. '
     'The columns "complete, same times" restrict the complete-record predictions to the prediction times of the sparse scenario (identical times and targets, checked). Mean unit RMSE in cycles, five seeds.\n',
     '| Arm | Complete, all times | Complete, times of k = 5 | k = 5 | Complete, times of irr 1–5 | irr 1–5 |', '|---|---|---|---|---|---|']
S = {}
for arm in ('A1', 'A2', 'A3', 'A5', 'A6', 'A8'):
    row = [float(np.mean([np.mean([rm(r[u]['k1'][arm]) for r in E]) for u in units]))]
    for sc in ('k5', 'irr5'):
        sub = []; full = []
        for ui, u in enumerate(units):
            t = times(u, ui, sc); assert len(t) == len(E[0][u][sc][arm]), (u, sc, len(t), len(E[0][u][sc][arm]))
            assert np.allclose(np.array(E[0][u]['k1']['y'])[t - 10], E[0][u][sc]['y'])          # same targets
            sub.append(np.mean([rm(np.array(r[u]['k1'][arm])[t - 10]) for r in E])); full.append(np.mean([rm(r[u][sc][arm]) for r in E]))
        row += [float(np.mean(sub)), float(np.mean(full))]
    S[arm] = row; L.append(f'| {arm} | ' + ' | '.join(f'{x:.2f}' for x in row) + ' |')
d = S['A1']; best5 = min(S[a][2] for a in ('A1', 'A2', 'A3')); besti = min(S[a][4] for a in ('A1', 'A2', 'A3'))
L.append(f"\nDense model A1: {d[0]:.2f} cycles with complete records at all times, {d[1]:.2f} at the times of k = 5 and {d[3]:.2f} at the times of irr 1–5; best test-time remedy {best5:.2f} at k = 5 and {besti:.2f} at irr 1–5. "
         f"The increase of the error from complete to sparse records at identical prediction times is {best5 - d[1]:+.2f} and {besti - d[3]:+.2f} cycles (with all complete-record times: {best5 - d[0]:+.2f} and {besti - d[0]:+.2f}). "
         'Comparisons between arms within a scenario (E1, E2 and all paired tests) use identical prediction times and are not affected.')
json.dump(S, open(f'{B}/analysis/summary_common_times.json', 'w'), indent=1); open(f'{B}/analysis/tables_common_times.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('\n'.join(L).replace('–', '-'))
