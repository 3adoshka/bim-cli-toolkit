import sys
import os
import ifcopenshell
import ifcopenshell.geom
from tabulate import tabulate

def parse_enterprise_model(filepath):
    if not os.path.exists(filepath):
        print(f"[-] Error: Target model '{filepath}' not found.")
        sys.exit(1)

    print(f"[*] Initializing Enterprise Robust IFC Ingestion Gateway for: {filepath}...")
    
    try:
        model = ifcopenshell.open(filepath)
    except Exception as e:
        print(f"[-] CRITICAL: Failed to parse IFC file structure. Error: {e}")
        sys.exit(1)

    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)

    elements = model.by_type("IfcProduct")
    audit_log = []
    
    success_count = 0
    failure_count = 0

    for elem in elements:
        if elem.is_a("IfcSpatialStructureElement") or elem.is_a("IfcProject") or elem.is_a("IfcSite"):
            continue
            
        el_type = elem.is_a()
        el_name = elem.Name or "Unnamed"
        guid = elem.GlobalId
        
        status = "HEALTHY"
        error_msg = "None"

        # Safe geometric extraction wrapper to catch corruptions
        try:
            shape = ifcopenshell.geom.create_shape(settings, elem)
            if not shape:
                raise ValueError("Empty geometric shape generated.")
            success_count += 1
        except Exception as ex:
            status = "CORRUPT / MISSING GEOMETRY"
            error_msg = str(ex).split('\n')[0] # Keep log clean
            failure_count += 1

        audit_log.append([
            guid[:10] + "...",
            el_type,
            el_name,
            status,
            error_msg
        ])

    print("\n" + "="*80)
    print("      ENTERPRISE REAL-WORLD IFC INGESTION & HEALTH AUDIT")
    print("="*80)
    print(tabulate(audit_log, headers=["GlobalID", "Type", "Name", "Health Status", "Diagnostics Note"], tablefmt="fancy_grid"))
    print("="*80)
    print(f"[*] Summary -> Healthy Elements: {success_count} | Flagged/Corrupt: {failure_count}")
    print("[+] Robust parsing gateway execution completed successfully.\n")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "sample.ifc"
    parse_enterprise_model(target)
