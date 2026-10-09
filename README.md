# ATLAS: Sovereign Bootstrap Seed

```text
SILICON / UNAVOIDABLE FIRMWARE
              ↓
            ATLAS
       BOOTSTRAP SEED
              ↓
           PHYSICS
   TRUSTED MACHINE AUTHORITY
              ↓
            OMEGA
 SEMANTICS + SYNTHESIS + REALIZATION
              ↓
             AIEN
 SOVEREIGN SYNTHESIS INTELLIGENCE
```

## The Canonical Invariants
```text
ATLAS AWAKENS.
PHYSICS AUTHORIZES.
OMEGA DEFINES, SYNTHESIZES, VERIFIES, AND REALIZES.
AIEN THINKS, SEARCHES, AND INVENTS.
```

## Lineage & Provenance Note
*Formerly designated `Alpha` (`alpha.bin`) during the initial bootstrap draft.*  
Every prior architectural responsibility of **ALPHA** transfers to **ATLAS** unchanged:
- Root Canonical Executable: `atlas.bin` (formerly `alpha.bin`)
- Milestone Gate: `ATLAS_BOOT` (formerly `ALPHA_BOOT`)
- Audit Gate: `ATLAS_AUDIT_PASS` (formerly `ALPHA_AUDIT_PASS`)
- Machine Contract Entry: `PHYSICS_ENTRY_ABI` unchanged.

---

## Canonical Artifacts & Evidence Files
- [`atlas.bin`](file:///home/drakestapleton/workspace/atlas/atlas.bin): Irreducible bootstrap seed binary (1,480 bytes).
- [`atlas.sha256`](file:///home/drakestapleton/workspace/atlas/atlas.sha256): Cryptographic hash (`f7802501b410a0c19eff7b8fca8865c9ba9c96bfa4f8065ca8f508b67748b9a5`).
- [`atlas.manifest`](file:///home/drakestapleton/workspace/atlas/atlas.manifest): Canonical manifest and provenance record.
- [`atlas.memory-map`](file:///home/drakestapleton/workspace/atlas/atlas.memory-map): Normative memory layout and disjoint stack/descriptor proof.
- [`atlas.control-flow`](file:///home/drakestapleton/workspace/atlas/atlas.control-flow): Textual control flow graph and failure traps.
- [`atlas.audit`](file:///home/drakestapleton/workspace/atlas/atlas.audit): 100% byte-reconciled machine instruction ledger (301 instructions, 69 rodata words, 0 discrepancy).
- [`atlas.decode`](file:///home/drakestapleton/workspace/atlas/atlas.decode): Disassembly dump with static target proof.
- [`machine_contract.json`](file:///home/drakestapleton/workspace/atlas/machine_contract.json): Formal machine contract (`CONTRACT-QEMU-VIRT-AARCH64-M1`).
- [`qualification_receipt.json`](file:///home/drakestapleton/workspace/atlas/qualification_receipt.json): Cryptographic qualification receipt for Milestone 1.

---

## Qualification Architecture (Dual Verification Seams)

> Historical note (2026-10-09): the `.py` files named in this section are retained as frozen historical evidence only, not part of active AIEN execution. See [`HISTORICAL-PYTHON.md`](HISTORICAL-PYTHON.md). The current gate runner is `run_m1_gates.sh`.

### Seam 1: Independent Artifact-Audit Seam (`seam1_artifact_audit.py`)
Validates artifacts statically without requiring execution:
1. `ATLAS_ARTIFACT_IDENTITY_PASS`: `atlas.bin` matches `atlas.sha256`.
2. `ATLAS_MACHINE_CONTRACT_PASS`: Strictly satisfies contract size and SHA-256 algorithm constraints.
3. `ATLAS_AUDIT_PASS`: Mathematical word reconciliation ($301 \times 4 + 69 \times 4 = 1480$ bytes, 0 discrepancy) and static target proof (`ldr x19, =0x40200000; br x19`).
4. `ATLAS_STACK_DESCRIPTOR_DISJOINT_PASS`: Statically proves that the downward-growing scratchpad stack (`SP <= 0x401FC000`) is separated from the Machine Boot Descriptor (`0x401FE000`) by an 8 KiB guard gap, guaranteeing an empty intersection ($\text{Stack} \cap \text{Descriptor} = \emptyset$).

### Seam 2: External Execution Seam (`seam2_execution_harness.py`)
Validates execution in bare-metal QEMU AArch64:
1. `ATLAS_BOOT_QEMU_PASS`: Emits `ATLAS: AWAKEN` and `ATLAS: VERIFY`.
2. `ATLAS_HANDOFF_QEMU_PASS`: Emits `ATLAS: HANDOFF` and invokes `PHYSICS-0: AUTHORIZED`.
3. `ATLAS_CORRUPTION_REFUSAL_QEMU_PASS`:
   - **Exhaustive 256-single-byte mutation sweep**: Mutates every byte offset $0 \dots 255$ in the 256-byte physics payload (`^ 0x01`). Every single offset triggers `ATLAS: REFUSE` and isolates Physics.
   - **12 adversarial structured mutation scenarios**: Validates cookie corruptions, burst bit flips, early/mid/late instructions, text string mutations, all-zeros, and all-ones.
   - **Total**: 268/268 mutations refused into fail-closed quiescence.
4. `ATLAS_FAIL_CLOSED_QEMU_PASS`: Halts cleanly in `wfe; b .` with zero instruction overrun.

*Note: QEMU qualification pass (`ATLAS_BOOT_QEMU_PASS`) is strictly decoupled from native hardware qualification (`ATLAS_BOOT_NATIVE_PASS`), which remains pending for physical DGX Spark execution.*
