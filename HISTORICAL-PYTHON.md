# HISTORICAL — NOT PART OF ACTIVE AIEN EXECUTION

The four Python files listed below are retained, byte for byte, as frozen historical evidence for the Milestone 1 (ATLAS) QEMU qualification receipt. They are not part of any active AIEN build, qualification run, CI workflow, or runtime.

## Decision

Operator decision, Drake, 2026-10-09 (recorded against aien-dev/aien-architecture#12, aien-dev/atlas#2): Option 1 approved. Preserve legacy Python qualification scripts as frozen historical evidence. This does not relax the prohibition on Python in AIEN's active runtime or trusted tooling.

1. The retained files are marked HISTORICAL — NOT PART OF ACTIVE AIEN EXECUTION (this file).
2. Original source bytes, qualification receipts, hashes, and historical test outcomes are preserved. The `.py` files, `qualification_receipt.json`, `atlas.bin` and the audit artifacts are unchanged by this marking.
3. No production entry point, active build, CI qualification workflow, or current runtime depends on these files (verified 2026-10-09; see the PR for the evidence).
4. Historical evidence is not altered to conform to today's standards.
5. Scoped claim: the enforceable claim is that AIEN's **active trusted execution path** is Python-free. This repository is **not** claimed to be Python-free.
6. Reactivating, replacing, or requalifying any of these files needs a separate task and new evidence. No Rust rewrite and no deletion is made or implied here.

`TRANSITION_PLAN_M1.md` (Phase 3: move or delete the legacy Python) is superseded by this decision. The files stay where they are, unmodified.

## File table

| Path | SHA-256 | Git blob | What it was for | Evidence it backs |
|---|---|---|---|---|
| `generate_audit_ledger.py` | `092716bab5b070dbc7d9bafad1cb150ed9432c1b049459bebca26b860e15c096` | `abebd6917829456ed4379b7aca88a1ee3eca7ada` | Generated the reconciled Atlas machine-operation audit ledger (instructions x 4 + rodata words x 4 = 1480 bytes) | `atlas.audit`; `qualification_receipt.json` field `audit_ledger_reconciliation` (301 instructions, 69 rodata, 0 discrepancy) |
| `run_milestone1_gates.py` | `3af1e2af136bdf868a100906b3d034897b5f6a4d10bbf8c43947d8c44fdff569` | `1a12ae0ffaf9120166fb33dcdeb6fdbe0fb17e64` | Master M1 gate runner: SHA-256 KAT, Seam 1, Seam 2, summary | `qualification_receipt.json` field `gates` (8 gates true), `duration_seconds` 9.48 |
| `seam1_artifact_audit.py` | `7cc590ebc0b3976dc2d155da5c950bd65b2f550dbfea5fa666ff952f9109c546` | `c9a6d70a073aa358508cf31271e9ac08c84a4873` | Seam 1: static artifact audit (identity, contract, audit reconciliation, static target proof, stack/descriptor disjointness) | `qualification_receipt.json` fields `static_target_proof`, `disjoint_separation_proof`, gates `ATLAS_ARTIFACT_IDENTITY_PASS`, `ATLAS_MACHINE_CONTRACT_PASS`, `ATLAS_AUDIT_PASS`, `ATLAS_STACK_DESCRIPTOR_DISJOINT_PASS` |
| `seam2_execution_harness.py` | `270d5837b70e47261fc374ed631493c072311cd8b936ee36a096bf947a5a206e` | `9c58a196e0d7e5a72e549a610ed2f57789f0e8c6` | Seam 2: QEMU execution harness, 256-byte sweep + 12 adversarial mutations (268 cases), fail-closed check | `qualification_receipt.json` field `corruption_refusal_matrix` (268/268), gates `ATLAS_BOOT_QEMU_PASS`, `ATLAS_HANDOFF_QEMU_PASS`, `ATLAS_CORRUPTION_REFUSAL_QEMU_PASS`, `ATLAS_FAIL_CLOSED_QEMU_PASS` |

Receipt: `qualification_receipt.json`, canonical artifact `atlas.bin` (SHA-256 `f7802501b410a0c19eff7b8fca8865c9ba9c96bfa4f8065ca8f508b67748b9a5`, 1480 bytes). The receipt does not embed digests of these scripts; the binding is by gate names and results.

Hashes are of the files at repository commit `7e6b836` (default branch `master`). Anything that needs to confirm them can run `sha256sum` and `git rev-parse HEAD:<path>`.

## Active replacement (separate, already present)

`run_m1_gates.sh` (symlinked as `run_milestone1_gates.sh`) and `tools/m1tool.c` (pure C11 and POSIX shell, commit `0ec17d4`) are the current Python-free gate runner. They are not requalified by this marking and no new receipt is issued here (see decision item 6).
