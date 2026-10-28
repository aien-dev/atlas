# Atlas: the boot seed

Atlas is the first software in the AIEN chain: one small AArch64 binary (`atlas.bin`, 1,480 bytes) that checks the next boot stage against a pinned SHA-256 digest, hands control to it, and refuses and halts if the check fails. Milestone 1 is qualified in QEMU only. Native DGX Spark qualification is still pending.

Belongs to AIEN; start at [Aienix](https://github.com/aien-dev/aienix), the core tree of AIEN, for the whole project. Atlas is milestone M1 (`ATLAS_BOOT`) in the AIEN roadmap ([`doctrine/ROADMAP.md`](https://github.com/aien-dev/aien-architecture/blob/main/doctrine/ROADMAP.md) in aien-architecture). It is not one of the components Aienix lists today: the boot artifacts and the GB10 hardware path continue in [physics](https://github.com/aien-dev/physics). This repository holds only the seed and its evidence.

**Status (2026-10-18): QEMU qualified, native run pending, quiet.** The seed and its gate runner last changed on 2026-09-26. Since then: a relicense (2026-10-04) and the removal of the old Python scripts with a check that keeps Python out (2026-10-15). Run the gates with `./run_m1_gates.sh`.

```text
SILICON / UNAVOIDABLE FIRMWARE
              ↓
            ATLAS
       BOOTSTRAP SEED
              ↓
       NEXT BOOT STAGE
 (here: the 256-byte test payload
  physics-0.bin; the PHYSICS boot
  artifacts live in aien-dev/physics)
```

## The Canonical Invariants
```text
ATLAS AWAKENS.
AIEN PROPOSES.
OMEGA DEFINES.
FORGE REALIZES.
AEGIS VERIFIES.
HARDWARE ACTS.
EVIDENCE TEACHES.
```

These are the doctrine lines accepted in ADR 0014 (aien-dev/aien-architecture). The machine-realization role once called PHYSICS is now FORGE. The PHYSICS boot artifacts that Atlas hands off to stay in [aien-dev/physics](https://github.com/aien-dev/physics).

## Lineage & Provenance Note
*Formerly designated `Alpha` (`alpha.bin`) during the initial bootstrap draft.*  
Every prior architectural responsibility of **ALPHA** transfers to **ATLAS** unchanged:
- Root Canonical Executable: `atlas.bin` (formerly `alpha.bin`)
- Milestone Gate: `ATLAS_BOOT` (formerly `ALPHA_BOOT`)
- Audit Gate: `ATLAS_AUDIT_PASS` (formerly `ALPHA_AUDIT_PASS`)
- Machine Contract Entry: `PHYSICS_ENTRY_ABI` unchanged.
- The pre-rename Alpha artifacts are kept in [`history/alpha/`](history/alpha/) as a historical record only; no gate reads them.

---

## Canonical Artifacts & Evidence Files
- [`atlas.bin`](atlas.bin): Irreducible bootstrap seed binary (1,480 bytes).
- [`atlas.sha256`](atlas.sha256): Cryptographic hash (`f7802501b410a0c19eff7b8fca8865c9ba9c96bfa4f8065ca8f508b67748b9a5`).
- [`atlas.manifest`](atlas.manifest): Canonical manifest and provenance record.
- [`atlas.memory-map`](atlas.memory-map): Normative memory layout and disjoint stack/descriptor proof.
- [`atlas.control-flow`](atlas.control-flow): Textual control flow graph and failure traps.
- [`atlas.audit`](atlas.audit): 100% byte-reconciled machine instruction ledger (301 instructions, 69 rodata words, 0 discrepancy).
- [`atlas.decode`](atlas.decode): Disassembly dump with static target proof.
- [`machine_contract.json`](machine_contract.json): Formal machine contract (`CONTRACT-QEMU-VIRT-AARCH64-M1`).
- [`qualification_receipt.json`](qualification_receipt.json): Cryptographic qualification receipt for Milestone 1.

---

## Qualification Architecture (Dual Verification Seams)

> Historical note (2026-10-15): the `.py` files named in this section were the original Milestone 1 scripts; they were removed from the tree under the no-Python rule and remain in git history. See [`HISTORICAL-PYTHON.md`](HISTORICAL-PYTHON.md). The current gate runner is `run_m1_gates.sh`, which builds `tools/m1tool.c` with the host `gcc`, runs the NIST SHA-256 known-answer tests, then both seams (the QEMU seam needs `qemu-system-aarch64`). It leaves the committed `qualification_receipt.json` untouched unless `--write-receipt` is passed.

### Seam 1: Independent Artifact-Audit Seam (`m1tool audit-verify`; originally `seam1_artifact_audit.py`)
Validates artifacts statically without requiring execution:
1. `ATLAS_ARTIFACT_IDENTITY_PASS`: `atlas.bin` matches `atlas.sha256`.
2. `ATLAS_MACHINE_CONTRACT_PASS`: Strictly satisfies contract size and SHA-256 algorithm constraints.
3. `ATLAS_AUDIT_PASS`: Mathematical word reconciliation ($301 \times 4 + 69 \times 4 = 1480$ bytes, 0 discrepancy) and static target proof (`ldr x19, =0x40200000; br x19`).
4. `ATLAS_STACK_DESCRIPTOR_DISJOINT_PASS`: Statically proves that the downward-growing scratchpad stack (`SP <= 0x401FC000`) is separated from the Machine Boot Descriptor (`0x401FE000`) by an 8 KiB guard gap, guaranteeing an empty intersection ($\text{Stack} \cap \text{Descriptor} = \emptyset$).

### Seam 2: External Execution Seam (`m1tool qemu-matrix`; originally `seam2_execution_harness.py`)
Validates execution in bare-metal QEMU AArch64:
1. `ATLAS_BOOT_QEMU_PASS`: Emits `ATLAS: AWAKEN` and `ATLAS: VERIFY`.
2. `ATLAS_HANDOFF_QEMU_PASS`: Emits `ATLAS: HANDOFF`, after which the handed-off payload emits `PHYSICS-0: AUTHORIZED`.
3. `ATLAS_CORRUPTION_REFUSAL_QEMU_PASS`:
   - **Exhaustive 256-single-byte mutation sweep**: Mutates every byte offset $0 \dots 255$ in the 256-byte physics payload (`^ 0x01`). Every single offset triggers `ATLAS: REFUSE` and isolates Physics.
   - **12 adversarial structured mutation scenarios**: Validates cookie corruptions, burst bit flips, early/mid/late instructions, text string mutations, all-zeros, and all-ones.
   - **Total**: 268/268 mutations refused into fail-closed quiescence.
4. `ATLAS_FAIL_CLOSED_QEMU_PASS`: Halts cleanly in `wfe; b .` with zero instruction overrun.

*Note: QEMU qualification pass (`ATLAS_BOOT_QEMU_PASS`) is strictly decoupled from native hardware qualification (`ATLAS_BOOT_NATIVE_PASS`), which remains pending for physical DGX Spark execution.*

## Human-Directed Agentic Engineering

Development follows Human-Directed Agentic Engineering (HDAE): humans define goals,
architecture, constraints, acceptance criteria, and stopping points; agents implement,
execute checks, diagnose failures, and revise within those boundaries. Human review
retains responsibility for claims, acceptance, and release decisions. This describes
current development, not a retrospective claim about the historical qualification.

For the documented method and a systems-software case study, see Gregory M. Kurtzer,
*Ginux: Building an Independent Kernel That Runs Linux Userspace through Human-Directed
Agentic Engineering* (2026), https://doi.org/10.5281/zenodo.23682548.
