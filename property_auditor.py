import sys
import os
import ifcopenshell
from tabulate import tabulate

def audit_properties(filepath):
    if not os.path.exists(filepath):
        print(f"[-] Error: {filepath} not found.")
        sys.exit(1)

    print(f"[*] Initializing Automated Property & Metadata Audit on {filepath}...")
    model = ifcopenshell.open(filepath)
    
    elements = model.by_type("IfcProduct")
    audit_data = []

    for elem in elements:
        if elem.is_a("IfcSpatialStructureElement") or elem.is_a("IfcProject") or elem.is_a("IfcSite"):
            continue
            
        # Check for associated property definitions
        has_psets = False
        pset_names = []
        
        if hasattr(elem, "IsDefinedBy") and elem.IsDefinedBy:
            for def_rel in elem.IsDefinedBy:
                if def_rel.is_a("IfcRelDefinesByProperties"):
                    prop_def = def_rel.RelatingPropertyDefinition
                    if prop_def.is_a("IfcPropertySet"):
                        has_psets = True
                        pset_names.append(prop_def.Name)

        status = "COMPLIANT" if has_psets else "MISSING METADATA"
        pset_str = ", ".join(pset_names) if pset_names else "None"
        
        audit_data.append([
            elem.is_a(),
            elem.Name or "Unnamed",
            status,
            pset_str
        ])

    print("\n" + "="*75)
    print("      AUTOMATED BIM PROPERTY & METADATA COMPLIANCE REPORT")
    print("="*75)
    print(tabulate(audit_data, headers=["Element Type", "Name", "Metadata Status", "Assigned Property Sets"], tablefmt="fancy_grid"))
    print("="*75 + "\n")

    print("[+] Property audit matrix compiled successfully.")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "sample.ifc"
    audit_properties(target)
