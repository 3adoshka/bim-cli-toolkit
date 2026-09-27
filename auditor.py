import sys
import os
import ifcopenshell

def audit_model(filepath):
    if not os.path.exists(filepath):
        print(f"[-] Error: {filepath} not found.")
        sys.exit(1)

    model = ifcopenshell.open(filepath)
    walls = len(model.by_type("IfcWall"))
    slabs = len(model.by_type("IfcSlab"))

    print(f"[*] Running Automated QA/QC Compliance Check on {filepath}...")
    
    errors = 0
    if walls < 1:
        print("[-] FAIL: Missing structural walls in model compliance check.")
        errors += 1
    else:
        print("[+] PASS: Walls threshold verified.")

    if slabs < 1:
        print("[-] FAIL: Missing floor slabs in model compliance check.")
        errors += 1
    else:
        print("[+] PASS: Slabs threshold verified.")

    if errors > 0:
        print(f"\n[-] Audit Result: FAILED with {errors} violation(s).")
        sys.exit(1)
    else:
        print("\n[+] Audit Result: PASSED. Model meets baseline schema rules.")
        sys.exit(0)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "sample.ifc"
    audit_model(target)
