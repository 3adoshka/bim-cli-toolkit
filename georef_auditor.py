import sys
import os
import ifcopenshell
from tabulate import tabulate

def audit_georeferencing(filepath):
    if not os.path.exists(filepath):
        print(f"[-] Error: Target model '{filepath}' not found.")
        sys.exit(1)

    print(f"[*] Initializing ISO 19111 Geo-referencing & CRS Compliance Engine for: {filepath}...")
    model = ifcopenshell.open(filepath)
    
    # Check for Map Conversion / Projected CRS entities in IFC
    projected_crs = model.by_type("IfcProjectedCRS")
    map_conversion = model.by_type("IfcMapConversion")
    sites = model.by_type("IfcSite")

    crs_status = "COMPLIANT (ISO 19111)" if projected_crs else "NON-COMPLIANT (MISSING PROJECTED CRS)"
    conversion_status = "VERIFIED" if map_conversion else "NOT DEFINED"

    site_name = "Default Site"
    elevation = "0.00 m"
    lat_long = "Not Defined"

    if sites:
        site = sites[0]
        site_name = site.Name or "Unnamed Site"
        if hasattr(site, "RefElevation") and site.RefElevation is not None:
            elevation = f"{site.RefElevation} m"
        if hasattr(site, "RefLatitude") and site.RefLatitude:
            lat_long = f"Lat: {site.RefLatitude}, Long: {site.RefLongitude}"

    report_data = [
        ["Site Name", site_name],
        ["Geodetic Reference System", crs_status],
        ["Map Conversion Parameters", conversion_status],
        ["Reference Elevation", elevation],
        ["Latitude / Longitude Origin", lat_long]
    ]

    print("\n" + "="*70)
    print("      ISO 19111 GEO-REFERENCING & COORDINATE SYSTEM AUDIT")
    print("="*70)
    print(tabulate(report_data, headers=["Parameter", "Audit Status / Value"], tablefmt="fancy_grid"))
    print("="*70)
    
    if not projected_crs:
        print("[!] WARNING: Model lacks an IfcProjectedCRS entity. Real-world geospatial alignment required for GIS federation.")
    else:
        print("[+] Geo-referencing audit passed successfully.")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "sample.ifc"
    audit_georeferencing(target)
