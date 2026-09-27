import sys
import os
import ifcopenshell
from tabulate import tabulate

def audit_classifications(filepath):
    if not os.path.exists(filepath):
        print(f"[-] Error: Target model '{filepath}' not found.")
        sys.exit(1)

    print(f"[*] Initializing ISO 12006-2 / Uniclass Classification Audit Engine for: {filepath}...")
    model = ifcopenshell.open(filepath)
    
    elements = model.by_type("IfcProduct")
    audit_results = []

    compliant_count = 0
    missing_count = 0

    for elem in elements:
        if elem.is_a("IfcSpatialStructureElement") or elem.is_a("IfcProject") or elem.is_a("IfcSite"):
            continue
            
        el_type = elem.is_a()
        el_name = elem.Name or "Unnamed"
        guid = elem.GlobalId

        # Check for standard IfcRelAssociatesClassification links
        has_classification = False
        class_code = "UNASSIGNED"
        
        if hasattr(elem, "HasAssociations") and elem.HasAssociations:
            for assoc in elem.HasAssociations:
                if assoc.is_a("IfcRelAssociatesClassification"):
                    has_classification = True
                    class_ref = assoc.RelatingClassification
                    if hasattr(class_ref, "ItemReference") and class_ref.ItemReference:
                        class_code = class_ref.ItemReference
                    elif hasattr(class_ref, "Name") and class_ref.Name:
                        class_code = class_ref.Name

        # Simulation fallback check for sample model compliance
        status = "COMPLIANT (ISO 12006)" if has_classification else "NON-COMPLIANT (MISSING CODE)"
        
        if has_classification:
            compliant_count += 1
        else:
            missing_count += 1
            class_code = "MANDATORY UNICLASS REQ"

        audit_results.append([
            guid[:10] + "...",
            el_type,
            el_name,
            class_code,
            status
        ])

    print("\n" + "="*85)
    print("      ISO 12006-2 CLASSIFICATION AUDIT REPORT (UNICLASS / OMNICLASS)")
    print("="*85)
    print(tabulate(audit_results, headers=["GlobalID", "Type", "Name", "Classification Code", "Standard Status"], tablefmt="fancy_grid"))
    print("="*85)
    print(f"[*] Summary -> Compliant: {compliant_count} | Non-Compliant: {missing_count}")
    print("[+] Classification audit execution completed successfully.\n")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "sample.ifc"
    audit_classifications(target)
