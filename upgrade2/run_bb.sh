#!/bin/bash
# usage: run_bb.sh tcn|tf
cd "$(dirname "$0")"
mkdir -p results
bb=$1
for s in 0 1 2 3 4; do [ -f results/bbe_${bb}_s${s}.json ] || python3 bb_e.py $bb $s >> results/log_${bb}.txt 2>&1; done
for fd in FD001 FD003 FD002 FD004; do for s in 0 1 2 3 4; do
  [ -f results/bbc_${bb}_${fd}_s${s}.json ] || python3 bb_c.py $bb $fd $s >> results/log_${bb}.txt 2>&1
done; done
echo DONE >> results/log_${bb}.txt
