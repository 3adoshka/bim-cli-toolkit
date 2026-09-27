import sys
import os
import ifcopenshell
from tabulate import tabulate

def simulate_cloud_stream(filepath):
    if not os.path.exists(filepath):
        print(f"[-] Error: {filepath} not found.")
        sys.exit(1)

    print(f"[*] Initializing Speckle Cloud Interoperability Layer for {filepath}...")
    model = ifcopenshell.open(filepath)
    
    elements = model.by_type("IfcProduct")
    stream_payload = []

    for elem in elements:
        if elem.is_a("IfcSpatialStructureElement") or elem.is_a("IfcProject") or elem.is_a("IfcSite"):
            continue
            
        stream_payload.append([
            elem.GlobalId,
            elem.is_a(),
            elem.Name or "Unnamed",
            "READY FOR CLOUD SYNC"
        ])

    print("\n" + "="*70)
    print("      SPECKLE CLOUD INTEROPERABILITY STREAM PAYLOAD")
    print("="*70)
    print(tabulate(stream_payload, headers=["GlobalID", "Element Type", "Name", "Cloud Status"], tablefmt="fancy_grid"))
    print("="*70 + "\n")

    print("[+] Cloud stream payload compiled successfully. Ready for Speckle transport.")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "sample.ifc"
    simulate_cloud_stream(target)
