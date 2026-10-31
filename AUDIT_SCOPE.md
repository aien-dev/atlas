# Audit scope

Written for an outside, independent security audit. Revision described:
`c624eb489275bc046cec3686af3010b8dcc7eec0` on `master`, 2026-10-26. Everything below is taken from the repository's own files at
that revision; items marked NOT_RUN were not executed while writing this document.

## What this repository is

Atlas is the first software in the AIEN boot chain: a 1,480-byte AArch64 binary, `atlas.bin`
(SHA-256 `f7802501b410a0c19eff7b8fca8865c9ba9c96bfa4f8065ca8f508b67748b9a5`), that checks the next
boot stage against a pinned SHA-256 digest
(`e1d89bb1e0854ebaccd2be5c756c8a2ff8c5ecc8c0f90b4abd461fb7bf98374c`), hands control to it, and
refuses and halts if the check fails. Its source is `atlas.s`. The repository also holds its audit
artifacts, `machine_contract.json` (`CONTRACT-QEMU-VIRT-AARCH64-M1`), the Milestone 1 receipt
`qualification_receipt.json`, a 256-byte test payload `physics-0.bin` (source `physics_0.s`), and a
C and POSIX shell gate runner. Status: QEMU qualified, native run pending, quiet (the seed and its
gate runner last changed on 2026-09-26). Licence Apache 2.0.

## What to review, in priority order

1. `atlas.s` and `atlas.bin`. The seed: masks interrupts, sets the stack at `0x401FC000`, writes
   a boot descriptor at `0x401FE000`, hashes the payload, compares with the pinned digest, and
   either branches to `0x40200000` (`ldr x19, =0x40200000; br x19`) or halts. Check the compare is
   over the full digest, that the hashed range equals the executed range, and that every failure
   path reaches the halt.
2. `sha256_clean.s` and `sha256_clean.c`. The SHA-256 used by the seed and by the host tools.
   `test_sha256_kat.c` runs NIST FIPS 180-4 known-answer tests against the C implementation.
3. `atlas.memory-map`, `atlas.control-flow`, `atlas.audit`, `atlas.decode`, `atlas.manifest`,
   `machine_contract.json`. Static descriptions that Seam 1 checks against the binary (301
   instructions, 69 rodata words, 0 discrepancy; 8 KiB guard gap between stack and descriptor).
   Check they describe the binary, not each other.
4. `tools/m1tool.c` (1,150 lines). Host tool: `sha256`, `hexfield`, `bytes`, `audit-verify`,
   `gen-audit`, `mutate-sweep`, `mutate-adv`, `qemu-run`, `qemu-matrix`. It parses the audit and
   decode text files, forks `aarch64-linux-gnu-objdump` (in `gen-audit`) and
   `qemu-system-aarch64 -M virt` (in `qemu-run` and `qemu-matrix`) with `execvp`/`execlp`, kills
   QEMU after a timeout (default 1500 ms), and writes mutated payloads into a `mkdtemp` directory.
   Check parser bounds, argument handling and temporary file safety.
5. `run_m1_gates.sh`. Builds the host tools with `gcc -O2 ... -Werror`, runs the KAT, Seam 1 and
   Seam 2 under `set -eu`. Note that the final summary prints fixed `[PASSED]` lines; it relies on
   `set -e` stopping the script when any earlier step fails. With `--write-receipt` it overwrites
   `qualification_receipt.json`.
6. `scripts/test-host-security.sh`. Offline host-only controls: builds `m1tool` with
   AddressSanitizer and UndefinedBehaviorSanitizer, feeds malformed decode offsets, checks that an
   artifact path is not interpreted by a shell, that a symlink at a predictable temp name is not
   clobbered, and that a failing KAT stops the runner with its exit status.
7. `scripts/check-no-python.sh`. Fails on any tracked Python file or Python shebang.

There is no `.github/workflows/` directory. AGENTS.md: "There is no hosted CI. Testing runs on the
project's own machines; GitHub-hosted test workflows were removed on purpose."

## Trust boundaries

- Seed input: the next-stage payload in memory at boot. Untrusted until its digest matches.
- Trusted at boot: the pinned digest embedded in `atlas.bin`, and whatever firmware loads Atlas.
- Host tooling input: the committed artifact files and command-line paths given to `m1tool`.
- Trusted host oracles: `gcc`, `qemu-system-aarch64`, `aarch64-linux-gnu-objdump` (for
  `gen-audit` only).

## Threat model summary

- Assets: boot integrity (only the pinned next stage runs); honesty of the qualification receipt.
- Attackers considered: a corrupted or substituted next-stage payload (256 single-byte mutations
  and 12 structured mutations are tested); a malformed audit or decode file; a hostile path argument;
  a predictable temporary file.
- Defended: digest check with fail-closed halt; Seam 1 static reconciliation; Seam 2 corruption
  matrix (268 of 268 refused per the receipt); host sanitizer controls.
- Not defended / explicitly out of scope: QEMU qualification is not native qualification;
  `ATLAS_BOOT_NATIVE_PASS` needs a physical NVIDIA DGX Spark and has no runner here. Firmware below
  Atlas is out of scope. No constant-time claim is made for the SHA-256 comparison.

## Build from source at a pin

Requirements (AGENTS.md): a POSIX shell, `gcc`, `git`, and `qemu-system-aarch64` (machine `virt`)
for the execution seam. No Python and no package manager. `gen-audit` also needs
`aarch64-linux-gnu-objdump`. Toolchain versions are not pinned in the repository.

The host tools are built by the gate runner:

```sh
gcc -O2 -std=c11 -Wall -Wextra -Werror -o tools/m1tool tools/m1tool.c sha256_clean.c
gcc -O2 -o test_sha256_kat test_sha256_kat.c sha256_clean.c
```

The command that assembles `atlas.s` into `atlas.bin` is unknown from the repository; the committed
`atlas.bin` is the canonical artifact, identified by `atlas.sha256`.

## Run every test

NOT_RUN while writing this document. In order:

```sh
sh scripts/check-no-python.sh        # no tracked Python
sh scripts/test-host-security.sh     # host-only sanitizer and fail-closed controls, no QEMU
./run_m1_gates.sh                    # KAT, Seam 1, Seam 2 (needs qemu-system-aarch64)
```

Expected summary lines: `ATLAS-HOST-SECURITY PASS (sanitizer bounds, argv, private temp, failed
KAT)` from the host-security script, and `Overall Result: MILESTONE 1 QUALIFIED (QEMU)` followed by
the eight gate names from `run_m1_gates.sh`. Do not pass `--write-receipt`: it overwrites the
committed receipt and is reserved for an approved requalification. `run_milestone1_gates.sh` is the
same runner under its old name. Native hardware gates: NOT_RUN, no runner exists.

## Known limitations and NOT_RUN

- Native DGX Spark qualification pending (`native_hardware_qualification_status`:
  `PENDING_SEPARATE_NATIVE_GATES` in the receipt).
- The seed assembly command is not recorded.
- `TRANSITION_PLAN_M1.md`: the committed `qualification_receipt.json` "remains untouched as
  historical evidence for the Python-based qualification". A refreshed receipt from the C and shell
  runner is generated only when the requalification decision is recorded in `aien-architecture#12`.
- The runner's summary lines are static text gated by `set -e`.
- `physics-0.bin` is a test payload; the real next stage is in `aien-dev/physics`.

## Dependencies and provenance

- No lockfile and no package dependencies. `sha256_clean.c` is in-tree.
- Host tools: gcc, QEMU, binutils objdump, POSIX shell; versions unpinned.
- No network access at build or test time is required by the scripts.
- No GitHub Actions.
- `HISTORICAL-PYTHON.md` explains how the removed Python scripts can be retrieved from history.

## Evidence

`qualification_receipt.json` is the Milestone 1 receipt. `history/alpha/` holds pre-rename
artifacts. AGENTS.md: historical evidence is not edited to match today's standards; do not modify
the receipt, the seed or its pins without an explicit maintainer decision. Receipts are append-only.
