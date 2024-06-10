from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection
import arcpy
import pandas as pd

# Connect to ArcGIS Online
gis = GIS("https://osugisci.maps.arcgis.com")

# Define item id numbers to search through OSU data gallery (content was made public)
newton_id = "7fdddd823f2541138bd1472a9179e394"
laporte_id = "b936b3486b7e49a09c957fc8adecfbe1"

# Retrieve items
newton_item = gis.content.get(newton_id)
laporte_item = gis.content.get(laporte_id)

# Print item details
print("Newton Item:", newton_item)
print("LaPorte Item:", laporte_item)

# Access the feature layers
newton_feature_layer = newton_item.layers[0]
laporte_feature_layer = laporte_item.layers[0]

# Get the list of fields
fields_newton = [field.name for field in newton_feature_layer.properties.fields if field.name.startswith('F') and int(field.name[1:]) >= 2000 and int(field.name[1:]) <= 2020]
fields_laporte = [field.name for field in laporte_feature_layer.properties.fields if field.name.startswith('F') and int(field.name[1:]) >= 2000 and int(field.name[1:]) <= 2020]

print("Fields in Newton: ", fields_newton)
print("Fields in LaPorte: ", fields_laporte)

# Set workspace 
arcpy.env.workspace = r"C:\Users\benja\OneDrive\Desktop\GEOG-582 Programming\Programming Project\Project_Geodatabase\Project_Geodatabase\Project_Geodatabase.gdb"
print("local workspace set")

# Allow overwriting outputs
arcpy.env.overwriteOutput = True
print("allowing workspace overwrite")

# Define the names of the new feature classes
fc_newton = "Newton_USGS_Groundwater"
fc_laporte = "LaPorte_USGS_Groundwater"

# Define the geometry type (e.g., "POINT", "LINE", "POLYGON")
geometry_type = "POINT"
print("geometery type established")

# Define the spatial reference (if needed)
spatial_reference = arcpy.SpatialReference(4326)  # For example, WGS 1984
print("spatial reference set to WGS 1984")

# Create the feature classes
arcpy.CreateFeatureclass_management(out_path=arcpy.env.workspace,
                                    out_name=fc_newton,
                                    geometry_type=geometry_type,
                                    spatial_reference=spatial_reference)

arcpy.CreateFeatureclass_management(out_path=arcpy.env.workspace,
                                    out_name=fc_laporte,
                                    geometry_type=geometry_type,
                                    spatial_reference=spatial_reference)

print("Feature classes created")

# Field type mapping
field_type_mapping = {
    "esriFieldTypeSmallInteger": "SHORT",
    "esriFieldTypeInteger": "LONG",
    "esriFieldTypeSingle": "FLOAT",
    "esriFieldTypeDouble": "DOUBLE",
    "esriFieldTypeString": "TEXT",
    "esriFieldTypeDate": "DATE",
    "esriFieldTypeOID": "OID",
    "esriFieldTypeGeometry": "GEOMETRY",
    "esriFieldTypeBlob": "BLOB",
    "esriFieldTypeGlobalID": "GUID",
    "esriFieldTypeGUID": "GUID",
    "esriFieldTypeRaster": "RASTER",
    "esriFieldTypeXML": "XML"
}

# Add fields to the new feature classes based on the AGOL feature layers
for field in newton_feature_layer.properties.fields:
    if field.name.startswith('F') and int(field.name[1:]) >= 2000 and int(field.name[1:]) <= 2020:
        field_type = field_type_mapping.get(field.type, "TEXT")
        arcpy.AddField_management(fc_newton, field.name, field_type)

for field in laporte_feature_layer.properties.fields:
    if field.name.startswith('F') and int(field.name[1:]) >= 2000 and int(field.name[1:]) <= 2020:
        field_type = field_type_mapping.get(field.type, "TEXT")
        arcpy.AddField_management(fc_laporte, field.name, field_type)
print("Fields added to feature classes")



# Copy data from the feature layers to the local feature classes
newton_features = newton_feature_layer.query(where="1=1", out_fields="*").features
laporte_features = laporte_feature_layer.query(where="1=1", out_fields="*").features

# Insert data into the new feature classes
with arcpy.da.InsertCursor(fc_newton, fields_newton) as cursor:
    for feature in newton_features:
        cursor.insertRow([feature.attributes[field] for field in fields_newton])

with arcpy.da.InsertCursor(fc_laporte, fields_laporte) as cursor:
    for feature in laporte_features:
        cursor.insertRow([feature.attributes[field] for field in fields_laporte])


# Define the path to the new output file geodatabase
output_gdb_path = r"C:\Users\benja\OneDrive\Desktop\GEOG-582 Programming\Programming Project\Project_Geodatabase\Project_Geodatabase\NewOutput.gdb"

# Create a new output file geodatabase
arcpy.CreateFileGDB_management(r"C:\Users\benja\OneDrive\Desktop\GEOG-582 Programming\Programming Project\Project_Geodatabase\Project_Geodatabase", "NewOutput.gdb")

# Convert local feature classes to file geodatabase
arcpy.FeatureClassToFeatureClass_conversion(fc_newton, output_gdb_path, "Newton_USGS_Groundwater")
arcpy.FeatureClassToFeatureClass_conversion(fc_laporte, output_gdb_path, "LaPorte_USGS_Groundwater")

print("Local output updated successfully")