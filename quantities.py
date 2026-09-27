import sys
import os
import ifcopenshell
from tabulate import tabulate

def calculate_quantities(filepath):
    if not os.path.exists(filepath):
        print(f"[-] Error: {filepath} not found.")
        sys.exit(1)

    model = ifcopenshell.open(filepath)
    print(f"[*] Running Automated Quantity Takeoff (QTO) on {filepath}...")

    elements = {
        "Walls": model.by_type("IfcWall"),
        "Columns": model.by_type("IfcColumn"),
        "Slabs": model.by_type("IfcSlab"),
        "Beams": model.by_type("IfcBeam"),
        "Doors": model.by_type("IfcDoor"),
        "Windows": model.by_type("IfcWindow")
    }

    qto_data = []
    for cat, items in elements.items():
        # Simulating automated metric estimation per element count
        qto_data.append([cat, len(items)])

    print("\n" + "="*45)
    print("      AUTOMATED QUANTITY TAKEOFF (QTO)")
    print("="*45)
    print(tabulate(qto_data, headers=["Category", "Total Count"], tablefmt="fancy_grid"))
    print("="*45 + "\n")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "sample.ifc"
    calculate_quantities(target)
