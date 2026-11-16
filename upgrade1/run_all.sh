#!/bin/bash
cd "$(dirname "$0")"
mkdir -p results
for s in 0 1 2 3 4; do [ -f results/ext_s${s}.json ] || python3 ext.py $s >> results/log_ext.txt 2>&1; done
for fd in FD001 FD003 FD002 FD004; do for s in 0 1 2 3 4; do
  [ -f results/cmx_${fd}_s${s}.json ] || python3 cmx.py $fd $s >> results/log_cmx.txt 2>&1
done; done
echo DONE >> results/log_cmx.txt
