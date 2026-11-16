#!/bin/bash
cd "$(dirname "$0")"
for fd in FD001 FD003 FD002 FD004; do for s in 0 1 2 3 4; do
  [ -f results/q3e_${fd}_s${s}.json ] || python3 q3e.py $fd $s >> results/log.txt 2>&1
done; done
echo DONE >> results/log.txt
