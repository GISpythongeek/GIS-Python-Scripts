# PUHEtfgpsDATAtoGDB.py

'''
This ScriptTool converts PUHE Temporary Feature (TF) GPS shapefiles to feature 
classes in the "PUHEfieldworkCRGIS" geodatabase, then defines the original GPS
(Trimble) coordinate system ("NAD 1983"), then projects them to the desired
projection ("NAD 1983 (PA11) UTM Zone 5N") in order to match 
existing PUHE CR GIS files, then deletes the unwanted feature classes 
(those in GCS NAD 1983). It then appends the features to the appropriate
"Master_reconn_xxx" feature class, and deletes the gps feature class files.

This script was written to aid a National Park Service project I'm currently
working on (from 21 Sept 2015 to present).
'''

# grab 'arcpy' library and 'env' class
import arcpy
from arcpy import env


# create function to move shapefiles to the geodatabase
def shpTOgdb():
    env.workspace = "c:/XXX/XXX/XXX"
    geodatabase = "c:/XXX/XXX/XXX.gdb"
    shapefiles = arcpy.ListFeatureClasses()

    for shp in shapefiles:
        if "GDB" not in shp:
            arcpy.FeatureClassToFeatureClass_conversion(shp, geodatabase, shp[:-4])
            arcpy.Rename_management(shp, shp[:-4]+"_GDB")
            

# create function to define GPS (Trimble) projection ('NAD 1983')
def defproj():
    env.workspace = "c:/XXX/XXX/XXX.gdb"
    fc_list = arcpy.ListFeatureClasses()
    
    for filename in fc_list:
        spatialREF = arcpy.Describe(filename).spatialReference
        
        if spatialREF.name == "Unknown":
            coord = arcpy.SpatialReference('NAD 1983')
            arcpy.DefineProjection_management(filename, coord)


# create funtion to re-project to 'NAD 1983 (PA11) UTM Zone 5N'
def reproj():
    env.workspace = "c:/XXX/XXX/XXX.gdb"
    fc_list = arcpy.ListFeatureClasses()

    for filename in fc_list:
        spatialREF = arcpy.Describe(filename).spatialReference
        
        if spatialREF.name != "NAD_1983_PA11_UTM_Zone_5N" and spatialREF.name != "Unknown":
            newCoord = arcpy.SpatialReference('NAD 1983 (PA11) UTM Zone 5N')
            arcpy.Project_management(filename, filename+"_PA11", newCoord)


# create function 'deleteProjSHP' to delete unwanted projected shapefiles
def delete1():
    env.workspace = "c:/XXX/XXX/XXX.gdb"
    fc_list = arcpy.ListFeatureClasses()

    for filename in fc_list:
        if "Master" not in filename and "PA11" not in filename:
            arcpy.Delete_management(filename)


# create function to append new GPS fcs to master reconn fc
def append():
    env.workspace = "c:/XXX/XXX/XXX.gdb"
    fc_list = arcpy.ListFeatureClasses()

    for filename in fc_list:
        if "Master" not in filename and "TF_poly" in filename:
            arcpy.Append_management(filename, "Master_TF_poly", "NO_TEST")

        elif "Master" not in filename and "TF_line" in filename:
            arcpy.Append_management(filename, "Master_TF_line", "NO_TEST")

        elif "Master" not in filename and "TF_pt" in filename:
            arcpy.Append_management(filename, "Master_TF_pt", "NO_TEST")


# create function 'deleteProjSHP' to delete unwanted projected shapefiles
def delete2():
    env.workspace = "c:/XXX/XXX/XXX.gdb"
    fc_list = arcpy.ListFeatureClasses()

    for filename in fc_list:
        if "PA11" in filename:
            arcpy.Delete_management(filename)


# run functions
shpTOgdb()
defproj()
reproj()
delete1()
append()
delete2()


print "*** --- Script Complete --- ***\n"
