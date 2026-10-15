#!/usr/bin/env bash
# Flags em dashes and banned phrasing in publishable copy.
# Usage: scripts/copycheck.sh [paths...]   (defaults to identity site profiles content outbox press)
set -u
paths=("$@"); [ ${#paths[@]} -eq 0 ] && paths=(identity site profiles content outbox press)
existing=(); for p in "${paths[@]}"; do [ -e "$p" ] && existing+=("$p"); done
[ ${#existing[@]} -eq 0 ] && { echo "nothing to check"; exit 0; }
pattern='—|revolutioni[sz]e|leverag|unlock|seamless|delve|game[- ]changer|at the intersection of|fast-paced world|it.s not .{1,40}, it.s'
if grep -rniE --exclude=copycheck.sh "$pattern" "${existing[@]}"; then
  echo "copycheck: FAIL (rewrite the lines above)"; exit 1
fi
echo "copycheck: clean"
