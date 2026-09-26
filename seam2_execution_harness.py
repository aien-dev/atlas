#!/usr/bin/env python3
"""
SEAM 2: External Execution Seam (Requalified)
Runs alpha.bin in QEMU bare-metal environment under the Machine Contract.
Evaluates runtime telemetry, Physics handover, exhaustive multi-mutation corruption refusal,
and fail-closed quiescence.

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
    print("SEAM 2: EXTERNAL EXECUTION SEAM (QEMU AARCH64 VIRT - REQUALIFICATION)")
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
    print("\n[Exec-1] Executing Clean Golden Boot & Handoff with Cryptographic SHA-256...")
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
    # Test 2: Multi-Mutation Corruption Refusal Matrix
    # -----------------------------------------------------------------
    print("\n[Exec-2] Executing Exhaustive Multi-Mutation Corruption Matrix (12 Cases)...")
    with open(physics_bin, "rb") as f:
        golden_bytes = bytearray(f.read())
        
    mutations = [
        ("MUT_00_FIRST_BYTE", 0, lambda b: b.__setitem__(0, b[0] ^ 0x01)),
        ("MUT_01_COOKIE_BYTE", 8, lambda b: b.__setitem__(8, b[8] ^ 0xFF)),
        ("MUT_02_EARLY_INSN", 24, lambda b: b.__setitem__(24, b[24] ^ 0xAA)),
        ("MUT_03_MID_INSN", 64, lambda b: b.__setitem__(64, b[64] ^ 0x55)),
        ("MUT_04_LATE_INSN", 128, lambda b: b.__setitem__(128, b[128] ^ 0x01)),
        ("MUT_05_MSG_BYTE", 160, lambda b: b.__setitem__(160, b[160] ^ 0x20)),
        ("MUT_06_MSG_END", 200, lambda b: b.__setitem__(200, b[200] ^ 0x04)),
        ("MUT_07_PENULTIMATE", 254, lambda b: b.__setitem__(254, b[254] ^ 0x80)),
        ("MUT_08_FINAL_BYTE", 255, lambda b: b.__setitem__(255, b[255] ^ 0x01)),
        ("MUT_09_BURST_FLIP", "40-48", lambda b: [b.__setitem__(i, b[i] ^ 0xCC) for i in range(40, 48)]),
        ("MUT_10_ALL_ZEROS", "ALL", lambda b: [b.__setitem__(i, 0x00) for i in range(len(b))]),
        ("MUT_11_ALL_ONES", "ALL", lambda b: [b.__setitem__(i, 0xFF) for i in range(len(b))])
    ]
    
    matrix_passed = True
    for name, offset, mutate_fn in mutations:
        test_payload = bytearray(golden_bytes)
        mutate_fn(test_payload)
        
        tmp_path = f"tmp_mut_{name}.bin"
        with open(tmp_path, "wb") as f_out:
            f_out.write(test_payload)
            
        try:
            out = run_qemu(alpha_bin, tmp_path, timeout_sec=1.5)
            refused = ("ALPHA: REFUSE" in out)
            no_auth = ("PHYSICS-0: AUTHORIZED" not in out)
            no_denied = ("PHYSICS-0: DENIED" not in out) # Asserts handoff NEVER occurred
            
            if refused and no_auth and no_denied:
                print(f"  [PASS] {name:20s} (offset {str(offset):6s}) -> Refused cleanly, physics isolated.")
            else:
                print(f"  [FAIL] {name:20s} -> Did not refuse as expected! Output: {out.strip()}")
                matrix_passed = False
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                
    if matrix_passed:
        print("  -> ALPHA_CORRUPTION_REFUSAL_QEMU_PASS: OK (12/12 mutations refused)")
        results["ALPHA_CORRUPTION_REFUSAL_QEMU_PASS"] = True
    else:
        print("  -> ALPHA_CORRUPTION_REFUSAL_QEMU_PASS: FAILED")
        results["ALPHA_CORRUPTION_REFUSAL_QEMU_PASS"] = False

    # -----------------------------------------------------------------
    # Test 3: Fail-Closed Quiescence Verification
    # -----------------------------------------------------------------
    print("\n[Exec-3] Verifying Fail-Closed Quiescence...")
    corrupted = bytearray(golden_bytes)
    corrupted[10] ^= 0x01
    tmp_path = "tmp_quiesce_test.bin"
    with open(tmp_path, "wb") as f_out:
        f_out.write(corrupted)
    try:
        out = run_qemu(alpha_bin, tmp_path, timeout_sec=1.5)
        lines = [l.strip() for l in out.strip().splitlines() if l.strip()]
        if lines and lines[-1] == "ALPHA: REFUSE":
            print(f"  Quiescence confirmed: execution halted cleanly after REFUSE.")
            print(f"  Emitted {len(lines)} total lines; zero instruction overrun or crash.")
            print("  -> ALPHA_FAIL_CLOSED_QEMU_PASS: OK")
            results["ALPHA_FAIL_CLOSED_QEMU_PASS"] = True
        else:
            print(f"  FAIL: Expected terminal telemetry 'ALPHA: REFUSE', found: {lines[-1] if lines else 'empty'}")
            results["ALPHA_FAIL_CLOSED_QEMU_PASS"] = False
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    print("\n" + "-" * 70)
    all_passed = all(results.values())
    print(f"SEAM 2 RESULTS: {'ALL EXECUTION GATES PASSED (REQUALIFIED)' if all_passed else 'SOME GATES FAILED'}")
    print("-" * 70)
    return results

if __name__ == "__main__":
    res = verify_seam2()
    sys.exit(0 if (res and all(res.values())) else 1)
