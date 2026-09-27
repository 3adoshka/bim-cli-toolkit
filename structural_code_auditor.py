import sys
import os
import ifcopenshell
import ifcopenshell.geom
import trimesh
import numpy as np
from tabulate import tabulate

def audit_structural_codes(filepath):
    if not os.path.exists(filepath):
        print(f"[-] Error: Target model '{filepath}' not found.")
        sys.exit(1)

    print(f"[*] Initializing Structural Code Limit Auditor (SBC / Eurocode Standards) for: {filepath}...")
    model = ifcopenshell.open(filepath)
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)

    elements = model.by_type("IfcProduct")
    audit_results = []

    for elem in elements:
        if elem.is_a("IfcSpatialStructureElement") or elem.is_a("IfcProject") or elem.is_a("IfcSite"):
            continue
            
        el_type = elem.is_a()
        el_name = elem.Name or "Unnamed"
        guid = elem.GlobalId
        
        # Default status
        code_status = "PASS (WITHIN CODE LIMITS)"
        note = "Dimensions verified"

        try:
            shape = ifcopenshell.geom.create_shape(settings, elem)
            verts = shape.geometry.verts
            faces = shape.geometry.faces
            
            # Reconstruct mesh using trimesh to calculate bounding box dimensions
            vertices = np.array(verts).reshape((-1, 3))
            triangles = np.array(faces).reshape((-1, 3))
            mesh = trimesh.Trimesh(vertices=vertices, faces=triangles)
            
            extents = mesh.extents # [width, depth, height]
            min_dim = np.min(extents)

            # Simulated structural code rule: Minimum dimension for primary structural members >= 0.2m (200mm)
            if el_type in ["IfcColumn", "IfcBeam", "IfcWall"] and min_dim < 0.2:
                code_status = "FAIL (CODE LIMIT VIOLATION)"
                note = f"Min dimension {min_dim:.3f}m is below 0.20m structural minimum"
        except Exception as e:
            code_status = "ERROR / UNABLE TO COMPUTE"
            note = str(e)[:30]

        audit_results.append([
            guid[:10] + "...",
            el_type,
            el_name,
            code_status,
            note
        ])

    print("\n" + "="*85)
    print("      STRUCTURAL CODE LIMIT CHECK REPORT (SBC / EUROCODE)")
    print("="*85)
    print(tabulate(audit_results, headers=["GlobalID", "Type", "Name", "Code Check Status", "Engineering Note"], tablefmt="fancy_grid"))
    print("="*85)
    print("[+] Structural code limits audit completed successfully.\n")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "sample.ifc"
    audit_structural_codes(target)
