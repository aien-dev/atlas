# Sovereign Tooling Transition Plan: Milestone 1 (ATLAS)
Tracking: aien-dev/aien-architecture#12, aien-dev/atlas#2

## Context & Sovereignty Rule
Per the Sovereign Machine doctrine, qualification and build tooling must be local, in-house, and offline, with zero Python in the trusted path.
Milestone 1 previously used Python for static audit, execution harness, and gate orchestration (`run_milestone1_gates.py`, `seam1_artifact_audit.py`, `seam2_execution_harness.py`, `generate_audit_ledger.py`).

## Implementation Summary
A complete, pure C (C11) and POSIX shell replacement suite has been designed and implemented in `aien-dev/atlas`:
1. `tools/m1tool.c`: Pure C host qualification tool compiled via host `gcc` and linked directly with audited `sha256_clean.c`.
   - Subcommands: `sha256`, `hexfield`, `bytes`, `audit-verify`, `gen-audit`, `mutate-sweep`, `mutate-adv`, `qemu-run`, `qemu-matrix`.
2. `run_m1_gates.sh` (symlinked as `run_milestone1_gates.sh`): Master POSIX shell gate runner orchestrating KAT verification, Seam 1 static audits, and Seam 2 QEMU execution harness.

## Artifact Integrity & Receipt Preservation
- The canonical binary artifact `atlas.bin` (SHA-256 `f7802501b410a0c19eff7b8fca8865c9ba9c96bfa4f8065ca8f508b67748b9a5`, 1480 bytes) is **not modified**.
- The existing qualification receipt `qualification_receipt.json` remains **untouched** as historical evidence for the Python-based qualification.
- The new C/shell tooling was verified to produce 100% gate pass rate across all 8 gates:
  1. `ATLAS_ARTIFACT_IDENTITY_PASS`
  2. `ATLAS_MACHINE_CONTRACT_PASS`
  3. `ATLAS_AUDIT_PASS`
  4. `ATLAS_STACK_DESCRIPTOR_DISJOINT_PASS`
  5. `ATLAS_BOOT_QEMU_PASS`
  6. `ATLAS_HANDOFF_QEMU_PASS`
  7. `ATLAS_CORRUPTION_REFUSAL_QEMU_PASS` (268/268 refused: 256 sweep + 12 adversarial)
  8. `ATLAS_FAIL_CLOSED_QEMU_PASS`

## Transition Phasing
1. **Phase 1 (Dual-Track Availability - Present)**:
   - Pure C and shell tooling (`tools/m1tool.c`, `run_m1_gates.sh`) are introduced.
   - Developers and automated CI can verify gates using `./run_m1_gates.sh` without any Python runtime installed.
   - Legacy Python scripts remain available as historical reference.
2. **Phase 2 (Formal Requalification Decision)**:
   - When recorded in `aien-architecture#12`, `run_m1_gates.sh --write-receipt` generates a refreshed receipt reflecting the pure C/shell verification toolchain.
3. **Phase 3 (Python Retirement & Archival)**:
   - Legacy Python files are moved to `history/legacy-python/` or deleted, completing total retirement of Python from the sovereign path.
