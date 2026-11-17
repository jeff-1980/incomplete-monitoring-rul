#!/bin/bash
# all folds of both data sets; the two data sets run side by side on one GPU
cd "$(dirname "$0")"; EXP=${1:-/mnt/d/audit_data/battery_xjtu/export}; mkdir -p logs results
(for f in 0 1 2 3 4; do python3 rs.py xjtu $f $EXP > logs/xjtu_f$f.log 2>&1; done) &
(for f in 0 1 2 3 4; do python3 rs.py mit $f $EXP > logs/mit_f$f.log 2>&1; done) &
wait; echo ALLDONE
