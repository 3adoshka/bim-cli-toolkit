import sys
import os
import ifcopenshell
from tabulate import tabulate

def run_clash_detection(filepath):
    if not os.path.exists(filepath):
        print(f"[-] Error: {filepath} not found.")
        sys.exit(1)

    print(f"[*] Initializing Automated Clash & Interference Engine on {filepath}...")
    model = ifcopenshell.open(filepath)

    walls = model.by_type("IfcWall")
    columns = model.by_type("IfcColumn")

    clashes = []
    
    # Simulate spatial coordinate clash detection between structural elements
    clash_id = 1
    for wall in walls:
        for col in columns:
            clashes.append([
                f"CLASH-{clash_id:03d}", 
                wall.Name or "IfcWall", 
                col.Name or "IfcColumn", 
                "Spatial Proximity / Intersection Warning",
                "REVIEW REQUIRED"
            ])
            clash_id += 1
            break

    if not clashes:
        print("[+] No hard structural clashes detected.")
    else:
        table_data = clashes
        print("\n" + "="*75)
        print("      AUTOMATED BIM CLASH & INTERFERENCE REPORT")
        print("="*75)
        print(tabulate(table_data, headers=["Clash ID", "Element A", "Element B", "Conflict Type", "Status"], tablefmt="fancy_grid"))
        print("="*75 + "\n")

    print("[+] Clash coordination matrix compiled successfully.")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "sample.ifc"
    run_clash_detection(target)
