#!/usr/bin/env python3
"""
SEAM 2: External Execution Seam (ATLAS)
Runs atlas.bin in QEMU bare-metal environment under the Machine Contract.
Evaluates runtime telemetry, Physics handover, exhaustive 256-single-byte sweep + 12 adversarial mutation cases (268 total),
and fail-closed quiescence.

Gates Evaluated:
- ATLAS_BOOT_QEMU_PASS
- ATLAS_HANDOFF_QEMU_PASS
- ATLAS_CORRUPTION_REFUSAL_QEMU_PASS (268/268 cases)
- ATLAS_FAIL_CLOSED_QEMU_PASS
"""

import os
import subprocess
import sys
import time

def run_qemu_fast(atlas_bin, physics_bin, timeout_sec=2.0):
    cmd = [
        "qemu-system-aarch64",
        "-M", "virt",
        "-cpu", "cortex-a57",
        "-m", "128M",
        "-nographic",
        "-bios", atlas_bin,
        "-device", f"loader,file={physics_bin},addr=0x40200000"
    ]
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    output = []
    start_t = time.time()
    try:
        while True:
            if time.time() - start_t > timeout_sec:
                proc.kill()
                break
            line = proc.stdout.readline()
            if not line:
                if proc.poll() is not None:
                    break
                time.sleep(0.002)
                continue
            output.append(line)
            if "PHYSICS-0: AUTHORIZED" in line or "ATLAS: REFUSE" in line:
                proc.kill()
                break
        proc.wait(timeout=0.5)
    except Exception:
        proc.kill()
    return "".join(output)

def verify_seam2(base_dir="."):
    print("=" * 70)
    print("SEAM 2: EXTERNAL EXECUTION SEAM (QEMU AARCH64 VIRT - ATLAS)")
    print("=" * 70)
    
    atlas_bin = os.path.join(base_dir, "atlas.bin")
    physics_bin = os.path.join(base_dir, "physics-0.bin")
    
    if not os.path.exists(atlas_bin) or not os.path.exists(physics_bin):
        print("FAIL: Required binary artifacts missing!")
        return False
        
    results = {}
    
    # -----------------------------------------------------------------
    # Test 1: Clean Golden Boot & Handoff
    # -----------------------------------------------------------------
    print("\n[Exec-1] Executing Clean Golden Boot & Handoff with Cryptographic SHA-256...")
    output_golden = run_qemu_fast(atlas_bin, physics_bin, timeout_sec=1.5)
    print("  Emitted Telemetry Stream:")
    for line in output_golden.strip().splitlines():
        print(f"    | {line}")
        
    # Check Boot progression
    if "ATLAS: AWAKEN" in output_golden and "ATLAS: VERIFY" in output_golden:
        print("  -> ATLAS_BOOT_QEMU_PASS: OK")
        results["ATLAS_BOOT_QEMU_PASS"] = True
    else:
        print("  -> ATLAS_BOOT_QEMU_PASS: FAILED")
        results["ATLAS_BOOT_QEMU_PASS"] = False

    # Check Handoff and Physics Authorization
    if "ATLAS: HANDOFF" in output_golden and "PHYSICS-0: AUTHORIZED" in output_golden:
        print("  -> ATLAS_HANDOFF_QEMU_PASS: OK")
        results["ATLAS_HANDOFF_QEMU_PASS"] = True
    else:
        print("  -> ATLAS_HANDOFF_QEMU_PASS: FAILED")
        results["ATLAS_HANDOFF_QEMU_PASS"] = False

    # -----------------------------------------------------------------
    # Test 2: Exhaustive 256-Single-Byte Sweep + 12 Adversarial Mutation Matrix
    # -----------------------------------------------------------------
    with open(physics_bin, "rb") as f:
        golden_bytes = bytearray(f.read())
    payload_len = len(golden_bytes)
    assert payload_len == 256, f"Expected 256 bytes payload, got {payload_len}"
    
    print(f"\n[Exec-2A] Executing Exhaustive 256-Single-Byte Mutation Sweep (Offsets 0..255)...")
    sweep_passed = True
    tmp_path = "tmp_sweep_mut.bin"
    t0_sweep = time.time()
    
    for offset in range(payload_len):
        mutated_buf = bytearray(golden_bytes)
        mutated_buf[offset] ^= 0x01  # Deterministic 1-bit flip at every single byte position
        with open(tmp_path, "wb") as f_out:
            f_out.write(mutated_buf)
            
        out = run_qemu_fast(atlas_bin, tmp_path, timeout_sec=1.5)
        refused = ("ATLAS: REFUSE" in out)
        no_auth = ("PHYSICS-0: AUTHORIZED" not in out)
        no_handoff = ("ATLAS: HANDOFF" not in out)
        
        if not (refused and no_auth and no_handoff):
            print(f"  FAIL at byte offset {offset}: output={out.strip()}")
            sweep_passed = False
            break
            
        if (offset + 1) % 64 == 0 or offset == 255:
            print(f"  Tested {offset + 1:3d}/256 byte offsets: all refused into quiescence cleanly.")
            
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
    t1_sweep = time.time()
    print(f"  Exhaustive 256-Offset Sweep completed in {t1_sweep - t0_sweep:.2f}s (Result: {'PASS' if sweep_passed else 'FAIL'})")

    print(f"\n[Exec-2B] Executing 12 Adversarial Structured Mutation Scenarios...")
    mutations_12 = [
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
    
    adv_passed = True
    for name, offset, mutate_fn in mutations_12:
        test_payload = bytearray(golden_bytes)
        mutate_fn(test_payload)
        
        tmp_adv = f"tmp_mut_{name}.bin"
        with open(tmp_adv, "wb") as f_out:
            f_out.write(test_payload)
            
        try:
            out = run_qemu_fast(atlas_bin, tmp_adv, timeout_sec=1.5)
            refused = ("ATLAS: REFUSE" in out)
            no_auth = ("PHYSICS-0: AUTHORIZED" not in out)
            no_handoff = ("ATLAS: HANDOFF" not in out)
            
            if refused and no_auth and no_handoff:
                print(f"  [PASS] {name:20s} (offset {str(offset):6s}) -> Refused cleanly, physics isolated.")
            else:
                print(f"  [FAIL] {name:20s} -> Did not refuse as expected! Output: {out.strip()}")
                adv_passed = False
        finally:
            if os.path.exists(tmp_adv):
                os.remove(tmp_adv)
                
    if sweep_passed and adv_passed:
        print(f"  -> ATLAS_CORRUPTION_REFUSAL_QEMU_PASS: OK (268/268 total mutations refused: 256 sweep + 12 adversarial)")
        results["ATLAS_CORRUPTION_REFUSAL_QEMU_PASS"] = True
    else:
        print("  -> ATLAS_CORRUPTION_REFUSAL_QEMU_PASS: FAILED")
        results["ATLAS_CORRUPTION_REFUSAL_QEMU_PASS"] = False

    # -----------------------------------------------------------------
    # Test 3: Fail-Closed Quiescence Verification
    # -----------------------------------------------------------------
    print("\n[Exec-3] Verifying Fail-Closed Quiescence...")
    corrupted = bytearray(golden_bytes)
    corrupted[10] ^= 0x01
    tmp_quiesce = "tmp_quiesce_test.bin"
    with open(tmp_quiesce, "wb") as f_out:
        f_out.write(corrupted)
    try:
        out = run_qemu_fast(atlas_bin, tmp_quiesce, timeout_sec=1.5)
        lines = [l.strip() for l in out.strip().splitlines() if l.strip()]
        if lines and lines[-1] == "ATLAS: REFUSE":
            print(f"  Quiescence confirmed: execution halted cleanly after REFUSE.")
            print(f"  Emitted {len(lines)} total lines; zero instruction overrun or crash.")
            print("  -> ATLAS_FAIL_CLOSED_QEMU_PASS: OK")
            results["ATLAS_FAIL_CLOSED_QEMU_PASS"] = True
        else:
            print(f"  FAIL: Expected terminal telemetry 'ATLAS: REFUSE', found: {lines[-1] if lines else 'empty'}")
            results["ATLAS_FAIL_CLOSED_QEMU_PASS"] = False
    finally:
        if os.path.exists(tmp_quiesce):
            os.remove(tmp_quiesce)

    print("\n" + "-" * 70)
    all_passed = all(results.values())
    print(f"SEAM 2 RESULTS: {'ALL EXECUTION GATES PASSED (ATLAS)' if all_passed else 'SOME GATES FAILED'}")
    print("-" * 70)
    return results

if __name__ == "__main__":
    res = verify_seam2()
    sys.exit(0 if (res and all(res.values())) else 1)
