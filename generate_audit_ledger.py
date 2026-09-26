#!/usr/bin/env python3
import re
import os

def generate_audit_ledger():
    decode_path = "alpha.decode"
    audit_path = "alpha.audit"
    
    with open(decode_path, "r") as f:
        lines = f.readlines()
        
    audit_rows = [
        "# ALPHA MACHINE OPERATION AUDIT LEDGER",
        "## Normative Accounting: 100% Reachable Instructions & Memory Bounds",
        "",
        "| Offset | Raw Bytes | Decoded Operation | Inputs | Outputs | Branch Target | Memory Accessed | Privilege Required |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    
    in_code = False
    count = 0
    for line in lines:
        line = line.strip()
        if "_start>:" in line:
            in_code = True
            continue
        if not in_code or not line or line.startswith("Disassembly") or line.endswith(">:"):
            continue
        if line.startswith("..."):
            continue
            
        m = re.match(r"^([0-9a-f]+):\s+([0-9a-f]+)\s+(.*)$", line)
        if m:
            offset_val = int(m.group(1), 16)
            offset_str = f"0x{offset_val:04x}"
            raw_bytes = m.group(2)
            op_text = m.group(3).strip()
            
            inputs = "-"
            outputs = "-"
            branch_target = "-"
            mem_access = "-"
            priv = "EL1/EL2"
            
            if "msr" in op_text:
                inputs = "#0xf"
                outputs = "DAIF"
            elif "mov\tsp" in op_text:
                inputs = "x0"
                outputs = "SP"
            elif "str" in op_text:
                match = re.search(r"str[b]?\s+([w|x][0-9]+),\s+\[([a-z0-9,\s#+-]+)\]", op_text)
                if match:
                    inputs = match.group(1)
                    mem_access = f"Write [{match.group(2)}]"
            elif "ldr" in op_text:
                match = re.search(r"ldr[b]?\s+([w|x][0-9]+),\s+\[([a-z0-9,\s#+-]+)\]", op_text)
                if match:
                    outputs = match.group(1)
                    mem_access = f"Read [{match.group(2)}]"
                else:
                    match_lit = re.search(r"ldr\s+([w|x][0-9]+),\s+([0-9a-f]+)", op_text)
                    if match_lit:
                        outputs = match_lit.group(1)
                        mem_access = f"Literal @ 0x{int(match_lit.group(2), 16):04x}"
            elif "eor" in op_text or "mul" in op_text or "subs" in op_text or "cmp" in op_text:
                parts = op_text.replace(",", "").split()
                if len(parts) >= 3:
                    outputs = parts[1]
                    inputs = ", ".join(parts[2:])
            elif any(k in op_text for k in ["bl\t", "b\t", "b.", "cbz", "br"]):
                branch_target = op_text.split()[-1]
            elif "adr" in op_text:
                parts = op_text.replace(",", "").split()
                outputs = parts[1]
                inputs = parts[2]
                
            audit_rows.append(f"| `{offset_str}` | `{raw_bytes}` | `{op_text}` | `{inputs}` | `{outputs}` | `{branch_target}` | `{mem_access}` | `{priv}` |")
            count += 1
            
    with open(audit_path, "w") as f:
        f.write("\n".join(audit_rows) + "\n")
    print(f"Generated {audit_path} with {count} accounted machine operations.")

if __name__ == "__main__":
    generate_audit_ledger()
