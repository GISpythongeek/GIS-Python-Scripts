# PUHEgpsDATAtoGDB_PA11.py

'''
This ScriptTool converts PUHE GPS shapefiles to feature classes in the
"PUHEfieldworkCRGIS" geodatabase, then appends the features to the appropriate
"Master_reconn_xxx" feature class, and deletes the gps feature class files. 
This is to be used for shapefiles that are alaready projected in the desired
PA11 coordinate system.

This script was written to aid a National Park Service project I'm currently
working on (from 21 Sept 2015 to present).
'''

# grab 'arcpy' library and 'env' class
import arcpy
from arcpy import env


# create function to create re-projected shapefiles
def shpTOgdb():
    env.workspace = "c:/XXX/XXX/XXX"
    geodatabase = "c:/XXX/XXX/XXX.gdb"
    shapefiles = arcpy.ListFeatureClasses()

    for shp in shapefiles:
        if "GDB" not in shp:
            arcpy.FeatureClassToFeatureClass_conversion(shp, geodatabase, shp[:-4])
            arcpy.Rename_management(shp, shp[:-4]+"_GDB")


# create function to append new GPS fcs to master reconn fc
def append():
    env.workspace = "c:/XXX/XXX/XXX.gdb"
    fc_list = arcpy.ListFeatureClasses()

    for filename in fc_list:
        if "Master" not in filename and "poly" in filename:
            arcpy.Append_management(filename, "Master_reconn_poly", "NO_TEST")

        elif "Master" not in filename and "line" in filename:
            arcpy.Append_management(filename, "Master_reconn_line", "NO_TEST")

        elif "Master" not in filename and "pt" in filename:
            arcpy.Append_management(filename, "Master_reconn_pt", "NO_TEST")


# create function 'deleteProjSHP' to delete unwanted projected shapefiles
def delete2():
    env.workspace = "c:/XXX/XXX/XXX.gdb"
    fc_list = arcpy.ListFeatureClasses()

    for filename in fc_list:
        if "PA11" in filename:
            arcpy.Delete_management(filename)


# run functions
shpTOgdb()
append()
delete2()


print "*** --- Script Complete --- ***\n"
