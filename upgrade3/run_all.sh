#!/bin/bash
cd "$(dirname "$0")"
mkdir -p results
for s in 0 1 2 3 4; do [ -f results/extg_s${s}.json ] || python3 extg.py $s >> results/log_ext.txt 2>&1; done
for fd in FD001 FD003 FD002 FD004; do for s in 0 1 2 3 4; do
  [ -f results/q3g_${fd}_s${s}.json ] || python3 q3g.py $fd $s >> results/log_c.txt 2>&1
done; done
echo DONE >> results/log_c.txt
