import ifcopenshell
import ifcopenshell.api

# Create a blank IFC file (IFC4 schema)
model = ifcopenshell.file(schema="IFC4")

# 1. Create Project and Site structure
project = model.create_entity("IfcProject", GlobalId=ifcopenshell.guid.new(), Name="AEC Enterprise Project")
site = model.create_entity("IfcSite", GlobalId=ifcopenshell.guid.new(), Name="Jeddah Site")
building = model.create_entity("IfcBuilding", GlobalId=ifcopenshell.guid.new(), Name="Main Facility")
storey = model.create_entity("IfcBuildingStorey", GlobalId=ifcopenshell.guid.new(), Name="Ground Floor")

# Aggregate spatial hierarchy
model.create_entity("IfcRelAggregates", GlobalId=ifcopenshell.guid.new(), RelatingObject=project, RelatedObjects=[site])
model.create_entity("IfcRelAggregates", GlobalId=ifcopenshell.guid.new(), RelatingObject=site, RelatedObjects=[building])
model.create_entity("IfcRelAggregates", GlobalId=ifcopenshell.guid.new(), RelatingObject=building, RelatedObjects=[storey])

# 2. Setup Geometric Context (Axis 3D & Representation Context)
world_coords = model.create_entity("IfcCartesianPoint", Coordinates=(0.0, 0.0, 0.0))
axis_placement = model.create_entity("IfcAxis2Placement3D", Location=world_coords)
local_placement = model.create_entity("IfcLocalPlacement", PlacementRelTo=None, RelativePlacement=axis_placement)

# Geometric representation context for 3D shapes
context = model.create_entity("IfcGeometricRepresentationContext", 
    ContextIdentifier="Model", 
    ContextType="Model", 
    CoordinateSpaceDimension=3, 
    Precision=0.00001, 
    WorldCoordinateSystem=axis_placement
)

# Helper function to create a simple extruded box representation
def create_box_representation(width, depth, height):
    # Profile definition (rectangle)
    profile_pos = model.create_entity("IfcCartesianPoint", Coordinates=(0.0, 0.0))
    profile_placement = model.create_entity("IfcAxis2Placement2D", Location=profile_pos)
    profile = model.create_entity("IfcRectangleProfileDef", 
        ProfileType="AREA", 
        ProfileName="Rect", 
        Position=profile_placement, 
        XDim=width, 
        YDim=depth
    )
    
    # Extrusion direction
    direction = model.create_entity("IfcDirection", DirectionRatios=(0.0, 0.0, 1.0))
    extruded_solid = model.create_entity("IfcExtrudedAreaSolid", 
        SweptArea=profile, 
        Position=axis_placement, 
        ExtrudedDirection=direction, 
        Depth=height
    )
    
    shape_repr = model.create_entity("IfcShapeRepresentation", 
        ContextOfItems=context, 
        RepresentationIdentifier="Body", 
        RepresentationType="SweptSolid", 
        Items=[extruded_solid]
    )
    
    product_repr = model.create_entity("IfcProductDefinitionShape", Representations=[shape_repr])
    return product_repr

# 3. Create Structural Elements with Geometry
elements_data = [
    ("IfcWall", "Wall 1", 5.0, 0.3, 3.0),
    ("IfcWall", "Wall 2", 0.3, 5.0, 3.0),
    ("IfcColumn", "Column 1", 0.4, 0.4, 3.0),
    ("IfcSlab", "Slab 1", 5.0, 5.0, 0.2),
    ("IfcBeam", "Beam 1", 5.0, 0.4, 0.5)
]

for el_type, name, w, d, h in elements_data:
    geom = create_box_representation(w, d, h)
    element = model.create_entity(el_type, 
        GlobalId=ifcopenshell.guid.new(), 
        Name=name, 
        ObjectPlacement=local_placement, 
        Representation=geom
    )
    # Contain element in storey
    model.create_entity("IfcRelContainedInSpatialStructure", 
        GlobalId=ifcopenshell.guid.new(), 
        RelatingStructure=storey, 
        RelatedElements=[element]
    )

# Save file
model.write("sample.ifc")
print("[+] Successfully generated geometric sample.ifc with 3D mesh representations.")
if __name__ == "__main__":
    pass
