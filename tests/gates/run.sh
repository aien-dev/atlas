#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
step="${1:?usage: tests/gates/run.sh <step>}"
obs() { printf 'AIEN-OBS %s %s\n' "$1" "$2"; }
case "$step" in
  zero-disk-secrets)
    found=false
    if find . -type f \( -name '.env' -o -name '.env.*' \) \
         ! -name '*.example' ! -name '*.sample' | head -1 | grep -q .; then
      found=true
    fi
    obs env_files_found "$found"
    [ "$found" = false ]
    ;;
  no-python) sh scripts/check-no-python.sh ;;
  m1-gates)  ./run_m1_gates.sh ;;
  *) echo "run.sh: unknown step $step" >&2; exit 2 ;;
esac
