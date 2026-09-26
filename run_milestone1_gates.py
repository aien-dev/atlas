#!/usr/bin/env python3
"""
MASTER QUALIFICATION RUNNER FOR MILESTONE 1 (ALPHA)
Executes both independent verification seams:
- Seam 1: Independent Artifact-Audit Seam (Static)
- Seam 2: External Execution Seam (Dynamic QEMU Virt)

Evaluates all 7 Milestone 1 Qualification Gates:
1. ALPHA_ARTIFACT_IDENTITY_PASS
2. ALPHA_AUDIT_PASS
3. ALPHA_MACHINE_CONTRACT_PASS
4. ALPHA_BOOT_QEMU_PASS
5. ALPHA_HANDOFF_QEMU_PASS
6. ALPHA_CORRUPTION_REFUSAL_QEMU_PASS
7. ALPHA_FAIL_CLOSED_QEMU_PASS
"""

import json
import os
import sys
import time

from seam1_artifact_audit import verify_seam1
from seam2_execution_harness import verify_seam2

def run_milestone1_gates():
    print("#" * 70)
    print("SOVEREIGN MACHINE MASTER PLAN — MILESTONE 1 QUALIFICATION RUNNER")
    print("Target: The Irreducible Bootstrap Seed (alpha.bin) & Dual Verification Seams")
    print("#" * 70)
    
    start_time = time.time()
    
    # Run Seam 1
    seam1_results = verify_seam1(".")
    if not seam1_results:
        print("\nFATAL: Seam 1 failed critically.")
        sys.exit(1)
        
    print()
    # Run Seam 2
    seam2_results = verify_seam2(".")
    if not seam2_results:
        print("\nFATAL: Seam 2 failed critically.")
        sys.exit(1)
        
    all_gates = {}
    all_gates.update(seam1_results)
    all_gates.update(seam2_results)
    
    duration = time.time() - start_time
    
    # Generate formal report
    print("\n" + "=" * 70)
    print("MILESTONE 1 GATE AUDIT SUMMARY REPORT")
    print("=" * 70)
    
    all_passed = True
    gate_table = []
    for gate_name, passed in all_gates.items():
        status = "PASSED" if passed else "FAILED"
        if not passed:
            all_passed = False
        gate_table.append(f"  [{status:6s}]  {gate_name}")
        
    print("\n".join(gate_table))
    print("-" * 70)
    print(f"Overall Result: {'MILESTONE 1 QUALIFIED' if all_passed else 'QUALIFICATION FAILED'}")
    print(f"Execution Duration: {duration:.2f} seconds")
    print("=" * 70)
    
    # Write qualification receipt
    receipt = {
        "milestone": "MILESTONE_1_ALPHA",
        "timestamp_epoch": time.time(),
        "canonical_artifact": "alpha.bin",
        "sha256": "88035c7f3a5549b082580e73fdbe220552dd7f1828f1b6e7018423148e6322d5",
        "duration_seconds": duration,
        "gates": all_gates,
        "qualified": all_passed,
        "native_hardware_qualification_status": "PENDING_SEPARATE_NATIVE_GATES"
    }
    
    with open("qualification_receipt.json", "w") as f:
        json.dump(receipt, f, indent=2)
    print("Qualification receipt written to qualification_receipt.json")
    
    return all_passed

if __name__ == "__main__":
    success = run_milestone1_gates()
    sys.exit(0 if success else 1)
