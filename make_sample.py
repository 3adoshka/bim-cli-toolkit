import ifcopenshell

# Create an empty IFC file with IFC4 schema
f = ifcopenshell.file(schema="IFC4")

# Create basic spatial structure and a couple of structural elements so the parser has data
project = f.createIfcProject(GlobalId=ifcopenshell.guid.new(), Name="Test Project")
site = f.createIfcSite(GlobalId=ifcopenshell.guid.new(), Name="Test Site")
building = f.createIfcBuilding(GlobalId=ifcopenshell.guid.new(), Name="Test Building")
storey = f.createIfcBuildingStorey(GlobalId=ifcopenshell.guid.new(), Name="Ground Floor")

# Add some structural items
f.createIfcWall(GlobalId=ifcopenshell.guid.new(), Name="Wall 1")
f.createIfcWall(GlobalId=ifcopenshell.guid.new(), Name="Wall 2")
f.createIfcColumn(GlobalId=ifcopenshell.guid.new(), Name="Column 1")
f.createIfcSlab(GlobalId=ifcopenshell.guid.new(), Name="Slab 1")
f.createIfcBeam(GlobalId=ifcopenshell.guid.new(), Name="Beam 1")

# Save out to sample.ifc
f.write("sample.ifc")
print("[+] Local sample.ifc generated successfully!")
