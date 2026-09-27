import sys
import os
import json
import ifcopenshell
from tabulate import tabulate

def run_aec_audit(filepath):
    if not os.path.exists(filepath):
        print(f"[-] Error: {filepath} not found.")
        sys.exit(1)

    print(f"[*] Initializing AEC Industry-Standard Audit on {filepath}...")
    model = ifcopenshell.open(filepath)

    report = {
        "model": filepath,
        "schema": model.schema,
        "checks": []
    }

    # AEC Standard Check 1: Spatial Containment (Every physical element must belong to a storey)
    physical_elements = model.by_type("IfcProduct")
    uncontained_count = 0
    
    for elem in physical_elements:
        # Skip spatial structures themselves
        if elem.is_a("IfcSpatialStructureElement") or elem.is_a("IfcProject") or elem.is_a("IfcSite"):
            continue
        # Check Decomposes / ContainedInSpatialStructure relationship
        contained = False
        if hasattr(elem, "ContainedInStructure") and elem.ContainedInStructure:
            contained = True
        elif hasattr(elem, "Decomposes") and elem.Decomposes:
            contained = True
            
        if not contained:
            uncontained_count += 1

    spatial_status = "PASS" if uncontained_count == 0 else "WARNING"
    report["checks"].append({
        "rule": "ISO 19650 Spatial Containment",
        "status": spatial_status,
        "details": f"{uncontained_count} elements lack spatial assignment."
    })

    # AEC Standard Check 2: Global ID Uniqueness & Integrity
    guids = [e.GlobalId for e in physical_elements if hasattr(e, "GlobalId")]
    duplicate_guids = len(guids) - len(set(guids))
    guid_status = "PASS" if duplicate_guids == 0 else "FAIL"
    report["checks"].append({
        "rule": "IFC GlobalID Integrity",
        "status": guid_status,
        "details": f"{duplicate_guids} duplicate GlobalIDs detected."
    })

    # Display clean CLI Table
    table_data = [[c["rule"], c["status"], c["details"]] for c in report["checks"]]
    print("\n" + "="*70)
    print("      AEC ENTERPRISE COMPLIANCE AUDIT (ISO/BIM STANDARD)")
    print("="*70)
    print(tabulate(table_data, headers=["Compliance Rule", "Status", "Findings"], tablefmt="fancy_grid"))
    print("="*70 + "\n")

    # Export machine-readable audit log for CI/CD pipelines
    output_json = "audit_report.json"
    with open(output_json, "w") as f:
        json.dump(report, f, indent=4)
    print(f"[+] Enterprise audit payload exported to {output_json}\n")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "sample.ifc"
    run_aec_audit(target)
