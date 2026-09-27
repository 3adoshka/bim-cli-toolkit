import sys
import os
import ifcopenshell
import pandas as pd
from tabulate import tabulate

def generate_server_qto(filepath):
    if not os.path.exists(filepath):
        print(f"[-] Error: {filepath} not found.")
        sys.exit(1)

    print(f"[*] Initializing Server-Side QTO Dataframe Pipeline on {filepath}...")
    model = ifcopenshell.open(filepath)
    
    elements = model.by_type("IfcProduct")
    data = []

    for elem in elements:
        if elem.is_a("IfcSpatialStructureElement") or elem.is_a("IfcProject") or elem.is_a("IfcSite"):
            continue
            
        data.append({
            "GlobalID": elem.GlobalId,
            "ElementType": elem.is_a(),
            "Name": elem.Name or "Unnamed",
            "Phase": "New Construction"
        })

    # Convert raw IFC data into a Pandas DataFrame for data engineering analytics
    df = pd.DataFrame(data)

    print("\n" + "="*70)
    print("      SERVER-SIDE QUANTITY TAKEOFF (QTO) DATAFRAME SUMMARY")
    print("="*70)
    
    # Group by Element Type to calculate quantities and counts
    summary_df = df.groupby("ElementType").size().reset_index(name="Total Count")
    print(tabulate(summary_df, headers=["Element Type", "Total Count"], tablefmt="fancy_grid", showindex=False))
    print("="*70 + "\n")

    # Export capability for enterprise cost estimation sheets
    output_csv = "qto_export.csv"
    df.to_csv(output_csv, index=False)
    print(f"[+] Server-side QTO dataframe compiled and exported to {output_csv}.")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "sample.ifc"
    generate_server_qto(target)
