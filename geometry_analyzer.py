import sys
import os
import ifcopenshell
import ifcopenshell.geom
from tabulate import tabulate

def analyze_geometry(filepath):
    if not os.path.exists(filepath):
        print(f"[-] Error: {filepath} not found.")
        sys.exit(1)

    print(f"[*] Initializing Advanced Geometric & Mesh Analysis on {filepath}...")
    model = ifcopenshell.open(filepath)

    # Initialize IfcOpenShell geometry processing settings
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)

    elements = model.by_type("IfcProduct")
    geo_data = []

    for elem in elements:
        if elem.is_a("IfcSpatialStructureElement") or elem.is_a("IfcProject") or elem.is_a("IfcSite"):
            continue
        
        try:
            # Generate mesh representation using IfcOpenShell geometry engine
            shape = ifcopenshell.geom.create_shape(settings, elem)
            verts = shape.geometry.verts
            faces = shape.geometry.faces
            
            num_verts = len(verts) // 3
            num_faces = len(faces) // 3
            
            geo_data.append([
                elem.is_a(),
                elem.Name or "Unnamed",
                f"{num_verts} vertices",
                f"{num_faces} faces",
                "MESH GENERATED"
            ])
        except Exception:
            geo_data.append([
                elem.is_a(),
                elem.Name or "Unnamed",
                "N/A",
                "N/A",
                "NO GEOMETRY"
            ])

    print("\n" + "="*70)
    print("      ADVANCED BIM GEOMETRY & MESH ANALYSIS REPORT")
    print("="*70)
    print(tabulate(geo_data, headers=["Element Type", "Name", "Vertices", "Faces", "Status"], tablefmt="fancy_grid"))
    print("="*70 + "\n")

    print("[+] Geometric analysis matrix compiled successfully.")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "sample.ifc"
    analyze_geometry(target)
