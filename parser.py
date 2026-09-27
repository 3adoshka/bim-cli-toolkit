import sys
import os
import ifcopenshell
from tabulate import tabulate

def analyze_ifc(filepath):
    if not os.path.exists(filepath):
        print(f"[-] Error: File '{filepath}' not found.")
        return

    print(f"[*] Loading BIM model: {filepath} ...")
    try:
        model = ifcopenshell.open(filepath)
    except Exception as e:
        print(f"[-] Failed to parse IFC file: {e}")
        return

    # Extract core structural elements
    walls = model.by_type("IfcWall")
    columns = model.by_type("IfcColumn")
    slabs = model.by_type("IfcSlab")
    beams = model.by_type("IfcBeam")

    summary_data = [
        ["Walls", len(walls)],
        ["Columns", len(columns)],
        ["Slabs", len(slabs)],
        ["Beams", len(beams)],
        ["Total Structural Elements", len(walls) + len(columns) + len(slabs) + len(beams)]
    ]

    print("\n" + "="*40)
    print("      BIM MODEL AUTOMATED AUDIT REPORT")
    print("="*40)
    print(tabulate(summary_data, headers=["Element Category", "Count"], tablefmt="fancy_grid"))
    print("="*40 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parser.py <path_to_model.ifc>")
    else:
        analyze_ifc(sys.argv[1])
