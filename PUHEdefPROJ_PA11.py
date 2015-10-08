# PUHEdefPROJ_PA11.py

'''
This ScriptTool defines the original GPS (Trimble) coordinate system 
("NAD 1983 PA11 UTM5N"). This script was written to aid a National Park 
Service project I'm currently working on (from 21 Sept 2015 to present).
'''

# grab 'arcpy' library and 'env' class
import arcpy
from arcpy import env


# create function to define GPS (Trimble) projection ('NAD 1983 PA11 UTM5N')
def defproj():
    env.workspace = "c:/XXX/XXX/XXX"
    shapefiles = arcpy.ListFeatureClasses()
    
    for shp in shapefiles:
                
        if "PA11" in shp:
            coord = arcpy.SpatialReference('NAD 1983 (PA11) UTM Zone 5N')
            arcpy.DefineProjection_management(shp, coord)


# run functions
defproj()


print "*** --- Script Complete --- ***\n"
