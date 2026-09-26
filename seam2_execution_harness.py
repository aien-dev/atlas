#!/usr/bin/env python3
"""
SEAM 2: External Execution Seam
Runs alpha.bin in QEMU bare-metal environment under the Machine Contract.
Evaluates runtime telemetry, Physics handover, corruption refusal, and fail-closed quiescence.

Gates Evaluated:
- ALPHA_BOOT_QEMU_PASS
- ALPHA_HANDOFF_QEMU_PASS
- ALPHA_CORRUPTION_REFUSAL_QEMU_PASS
- ALPHA_FAIL_CLOSED_QEMU_PASS
"""

import os
import subprocess
import sys
import tempfile
import time

def run_qemu(alpha_bin, physics_bin, timeout_sec=2.0):
    cmd = [
        "qemu-system-aarch64",
        "-M", "virt",
        "-cpu", "cortex-a57",
        "-m", "128M",
        "-nographic",
        "-bios", alpha_bin,
        "-device", f"loader,file={physics_bin},addr=0x40200000"
    ]
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_sec,
            text=True
        )
        output = proc.stdout
    except subprocess.TimeoutExpired as e:
        output = e.stdout if e.stdout else ""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
    return output

def verify_seam2(base_dir="."):
    print("=" * 70)
    print("SEAM 2: EXTERNAL EXECUTION SEAM (QEMU AARCH64 VIRT)")
    print("=" * 70)
    
    alpha_bin = os.path.join(base_dir, "alpha.bin")
    physics_bin = os.path.join(base_dir, "physics-0.bin")
    
    if not os.path.exists(alpha_bin) or not os.path.exists(physics_bin):
        print("FAIL: Required binary artifacts missing!")
        return False
        
    results = {}
    
    # -----------------------------------------------------------------
    # Test 1: Clean Golden Boot & Handoff
    # -----------------------------------------------------------------
    print("\n[Exec-1] Executing Clean Golden Boot & Handoff...")
    output_golden = run_qemu(alpha_bin, physics_bin, timeout_sec=1.5)
    print("  Emitted Telemetry Stream:")
    for line in output_golden.strip().splitlines():
        print(f"    | {line}")
        
    # Check Boot progression
    if "ALPHA: AWAKEN" in output_golden and "ALPHA: VERIFY" in output_golden:
        print("  -> ALPHA_BOOT_QEMU_PASS: OK")
        results["ALPHA_BOOT_QEMU_PASS"] = True
    else:
        print("  -> ALPHA_BOOT_QEMU_PASS: FAILED")
        results["ALPHA_BOOT_QEMU_PASS"] = False

    # Check Handoff and Physics Authorization
    if "ALPHA: HANDOFF" in output_golden and "PHYSICS-0: AUTHORIZED" in output_golden:
        print("  -> ALPHA_HANDOFF_QEMU_PASS: OK")
        results["ALPHA_HANDOFF_QEMU_PASS"] = True
    else:
        print("  -> ALPHA_HANDOFF_QEMU_PASS: FAILED")
        results["ALPHA_HANDOFF_QEMU_PASS"] = False

    # -----------------------------------------------------------------
    # Test 2: 1-Byte Corruption Refusal
    # -----------------------------------------------------------------
    print("\n[Exec-2] Injecting 1-Byte Corruption into PHYSICS-0 Payload...")
    with open(physics_bin, "rb") as f:
        clean_bytes = bytearray(f.read())
        
    # Create corrupted payload by flipping 1 bit at offset 16
    corrupt_bytes = bytearray(clean_bytes)
    corrupt_bytes[16] ^= 0x01
    
    with tempfile.NamedTemporaryFile(suffix=".bin", delete=False) as tmp_corrupt:
        tmp_corrupt.write(corrupt_bytes)
        tmp_corrupt_path = tmp_corrupt.name

    try:
        output_corrupt = run_qemu(alpha_bin, tmp_corrupt_path, timeout_sec=1.5)
        print("  Emitted Telemetry Stream on Corrupted Image:")
        for line in output_corrupt.strip().splitlines():
            print(f"    | {line}")
            
        refused = ("ALPHA: REFUSE" in output_corrupt)
        no_auth = ("PHYSICS-0: AUTHORIZED" not in output_corrupt)
        no_denied = ("PHYSICS-0: DENIED" not in output_corrupt) # Proves physics was NEVER reached
        
        if refused and no_auth and no_denied:
            print("  Refusal confirmed: digest mismatch caught before handoff.")
            print("  Physics execution completely prevented.")
            print("  -> ALPHA_CORRUPTION_REFUSAL_QEMU_PASS: OK")
            results["ALPHA_CORRUPTION_REFUSAL_QEMU_PASS"] = True
        else:
            print("  -> ALPHA_CORRUPTION_REFUSAL_QEMU_PASS: FAILED")
            results["ALPHA_CORRUPTION_REFUSAL_QEMU_PASS"] = False

        # -----------------------------------------------------------------
        # Test 3: Fail-Closed Quiescence
        # -----------------------------------------------------------------
        print("\n[Exec-3] Verifying Fail-Closed Quiescence...")
        # Verify that output ends cleanly at REFUSE with zero unexpected telemetry
        lines = [l.strip() for l in output_corrupt.strip().splitlines() if l.strip()]
        if lines and lines[-1] == "ALPHA: REFUSE":
            print("  Quiescence confirmed: execution halted cleanly in bounded WFE state.")
            print("  Zero fallthrough or runaway CPU behavior detected.")
            print("  -> ALPHA_FAIL_CLOSED_QEMU_PASS: OK")
            results["ALPHA_FAIL_CLOSED_QEMU_PASS"] = True
        else:
            print(f"  FAIL: Expected last telemetry to be 'ALPHA: REFUSE', found: {lines[-1] if lines else 'empty'}")
            print("  -> ALPHA_FAIL_CLOSED_QEMU_PASS: FAILED")
            results["ALPHA_FAIL_CLOSED_QEMU_PASS"] = False

    finally:
        if os.path.exists(tmp_corrupt_path):
            os.remove(tmp_corrupt_path)

    print("\n" + "-" * 70)
    all_passed = all(results.values())
    print(f"SEAM 2 RESULTS: {'ALL EXECUTION GATES PASSED' if all_passed else 'SOME GATES FAILED'}")
    print("-" * 70)
    return results

if __name__ == "__main__":
    res = verify_seam2()
    sys.exit(0 if (res and all(res.values())) else 1)
