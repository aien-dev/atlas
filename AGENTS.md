# Atlas (the AIEN boot seed)

> Atlas is a 1,480-byte AArch64 binary, `atlas.bin`, that checks the next boot stage against a pinned SHA-256 digest, hands control to it, and refuses and halts if the check fails. This repository holds the seed, its audit artifacts, its qualification receipt and the C and POSIX shell gate runner that requalifies it. Milestone 1 is qualified in QEMU only; native DGX Spark qualification is pending. The default branch is `master`.

Shared rules: read https://www.aienos.com/agents/RULES.md first. This file adds what is specific to this repository; where the two differ, this file wins here.

## Scope

- Applies to the whole repository.
- The canonical artifact is `atlas.bin` (SHA-256 `f7802501b410a0c19eff7b8fca8865c9ba9c96bfa4f8065ca8f508b67748b9a5`). `atlas.s` is its source; `atlas.sha256`, `atlas.manifest`, `atlas.memory-map`, `atlas.control-flow`, `atlas.audit`, `atlas.decode` and `machine_contract.json` describe and pin it.
- `physics-0.bin` (source `physics_0.s`) is the 256-byte test payload that Atlas hands off to. The real next-stage boot artifacts live in `aien-dev/physics`, not here.
- `qualification_receipt.json` is the Milestone 1 receipt. `history/alpha/` holds the pre-rename Alpha artifacts as a historical record; no gate reads them.
- `HISTORICAL-PYTHON.md` and `TRANSITION_PLAN_M1.md` record the retired Python tooling. Historical evidence is not edited to match today's standards.
- The repository is quiet: the seed and its gate runner last changed on 2026-09-26.

## Installation

```bash
git clone https://github.com/aien-dev/atlas.git
cd atlas
```

Requirements, from `run_m1_gates.sh` and `tools/m1tool.c`: a POSIX shell, `gcc`, `git`, and `qemu-system-aarch64` (machine `virt`) for the execution seam. No Python and no package manager.

## Usage

```bash
# All 8 Milestone 1 gates: builds tools/m1tool and test_sha256_kat with gcc,
# runs the NIST SHA-256 known-answer tests, Seam 1 (static artifact audit)
# and Seam 2 (QEMU boot, handoff, 268-case corruption matrix, fail-closed halt)
./run_m1_gates.sh

# Keep Python out of the tree
sh scripts/check-no-python.sh
```

- `run_milestone1_gates.sh` is the same runner under its old name.
- The runner uses `set -eu`, so a failing build, Seam 1 or Seam 2 step stops it with a nonzero exit, and the summary block at the end is printed only when those steps succeeded. The known-answer test output is piped through `sed`, which hides its exit code: check that every KAT line reads `[PASS]` as well as the final exit code.
- `./run_m1_gates.sh --write-receipt` overwrites `qualification_receipt.json`. Do not pass it unless the change is an approved requalification.
- QEMU qualification is not native qualification. `ATLAS_BOOT_NATIVE_PASS` needs a physical NVIDIA DGX Spark and has no runner in this repository.
- `tools/m1tool` also exposes `sha256`, `hexfield`, `bytes`, `audit-verify`, `gen-audit`, `mutate-sweep`, `mutate-adv`, `qemu-run` and `qemu-matrix`; each prints its usage when called with wrong arguments.

## Conventions

- No Python anywhere: `scripts/check-no-python.sh` fails on any tracked Python file or Python shebang.
- There is no hosted CI. Testing runs on the project's own machines; GitHub-hosted test workflows were removed on purpose. Put the gate runner's output in the pull request.
- Build products are ignored by `.gitignore` (`tools/m1tool`, `test_sha256_kat`, `*.o`, `*.elf`, `build/`, corruption test files). Do not commit them.
- Every claim about the seed names the gate that proves it, using the gate names in `run_m1_gates.sh`.

## Safety and approvals

- Do not modify `atlas.bin`, `atlas.sha256`, `physics-0.bin`, the pinned physics digest, `machine_contract.json` or `qualification_receipt.json` without an explicit maintainer decision. Changing the seed invalidates the audit artifacts and the receipt and requires a full requalification with a new receipt.
- Do not weaken a gate or the corruption matrix to make a run pass. A refusal that stops working is a failure of the seed, not of the test.
- Do not edit `history/alpha/` or the historical records in `HISTORICAL-PYTHON.md`.
- `master` rejects deletion and non-fast-forward pushes. Work on a branch and merge through a pull request.

## Further reading

- `README.md`: the seed, its invariants, artifacts and the two verification seams.
- `HISTORICAL-PYTHON.md`: why the Python scripts were removed and how to retrieve them from history.
- `TRANSITION_PLAN_M1.md`: the move from Python to C and shell tooling.
- `aien-dev/physics`: the boot artifacts and GB10 hardware path that follow Atlas.
