#!/bin/sh
# Offline host-only controls for m1tool and the KAT gate. No QEMU or receipt writes.
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd -P)
T=$(mktemp -d "${TMPDIR:-/tmp}/atlas-host-security.XXXXXXXX")
trap 'rm -rf "$T"' EXIT
trap 'exit 1' INT TERM
: "${CC:=gcc}"
"$CC" -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer -std=c11 -Wall -Wextra -Werror \
  -o "$T/m1tool" "$ROOT/tools/m1tool.c" "$ROOT/sha256_clean.c"
export ASAN_OPTIONS=detect_leaks=0

audit() {
  "$T/m1tool" audit-verify "$ROOT/atlas.bin" "$ROOT/atlas.sha256" \
    "$ROOT/atlas.manifest" "$ROOT/machine_contract.json" "$ROOT/atlas.audit" "$1"
}
audit "$ROOT/atlas.decode" > "$T/golden.log"
for operand in 'x19, 160' 'x0, 138'; do
  case $operand in x19*) f=target ;; *) f=stack ;; esac
  sed "s/ldr[[:space:]]$operand/ldr\t${operand%%,*}, fffffffffffffffc/" \
    "$ROOT/atlas.decode" > "$T/$f.decode"
  grep -q fffffffffffffffc "$T/$f.decode"
  if audit "$T/$f.decode" > "$T/$f.log" 2>&1; then
    echo "unexpected PASS: malformed $f offset" >&2; exit 1
  fi
  grep -q 'FAIL:' "$T/$f.log"
  if grep -q AddressSanitizer "$T/$f.log"; then
    echo "sanitizer abort: $f offset" >&2; exit 1
  fi
done
marker="$T/shell-marker"
if "$T/m1tool" gen-audit "$ROOT/atlas.bin" \
    "missing; touch $marker; #" "$T/audit" "$T/decode" > "$T/injection.log" 2>&1; then
  echo 'unexpected PASS: nonexistent ELF' >&2; exit 1
fi
[ ! -e "$marker" ] || { echo 'shell interpreted artifact path' >&2; exit 1; }

# A deterministic inert QEMU stand-in exercises the complete mutation path
# without asserting anything about an actual emulated boot.
cat > "$T/qemu-system-aarch64" <<'EOF'
#!/bin/sh
case "$*" in
  *atlas_sweep_*) echo 'ATLAS: REFUSE' ;;
  *) echo 'ATLAS: HANDOFF'; echo 'PHYSICS-0: AUTHORIZED' ;;
esac
EOF
chmod 700 "$T/qemu-system-aarch64"
printf KEEP_ME > "$T/victim"
PATH="$T:$PATH" sh -c '
  printf "%s" "$$" > "$5"
  ln -s "$1" "/tmp/atlas_sweep_$$.bin"
  exec "$2" qemu-matrix "$3" "$4"
' sh "$T/victim" "$T/m1tool" "$ROOT/atlas.bin" "$ROOT/physics-0.bin" "$T/pid" > "$T/matrix.log"
rm -f "/tmp/atlas_sweep_$(cat "$T/pid").bin"
[ "$(cat "$T/victim")" = KEEP_ME ] || { echo 'predictable temp clobbered victim' >&2; exit 1; }
grep -q 'SEAM 2 RESULTS: ALL EXECUTION GATES PASSED' "$T/matrix.log"

# Replace only the freshly built ignored KAT executable with a failing
# surrogate; the runner must stop before printing any gate PASS summary.
REAL_CC=$(command -v gcc)
export REAL_CC ROOT
cat > "$T/gcc" <<'EOF'
#!/bin/sh
"$REAL_CC" "$@" || exit $?
case " $* " in
  *test_sha256_kat*) printf '#!/bin/sh\necho "[PASS] misleading KAT output"\nexit 17\n' > "$ROOT/test_sha256_kat"; chmod 700 "$ROOT/test_sha256_kat" ;;
esac
EOF
chmod 700 "$T/gcc"
if PATH="$T:$PATH" "$ROOT/run_m1_gates.sh" > "$T/kat.log" 2>&1; then
  echo 'unexpected PASS: failed SHA-256 KAT' >&2; exit 1
else
  rc=$?
fi
[ "$rc" -eq 17 ] || { echo "wrong KAT refusal status: $rc" >&2; exit 1; }
grep -q 'known-answer test exited 17' "$T/kat.log"
if grep -q 'Overall Result: MILESTONE 1 QUALIFIED' "$T/kat.log"; then
  echo 'qualification summary printed after KAT failure' >&2; exit 1
fi
printf 'ATLAS-HOST-SECURITY PASS (sanitizer bounds, argv, private temp, failed KAT)\n'
