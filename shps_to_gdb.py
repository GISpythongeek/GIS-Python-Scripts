Script Name: shps_to_gdb.py

##### --- Converts Multiple Shapefiles (.shp) to FCs in a Geodatabase (.gdb) --- #####

# grab 'arcpy' library and 'env' class
import arcpy
from arcpy import env

# set current workspace and environment,
	# where '...XXX/XXX...' represents the desired directory path
env.workspace = "c:/XXX/XXX/XXX"
#-optional--->  env.overwriteOutput = True

# create a variable 'geodatabase' for target geodatabase (.gdb)
geodatabase = "c:/XXX/XXX/XXX.gdb"

# create a list of desired shapefiles (.shp) to convert
shapefiles = arcpy.ListFeatureClasses()

# create a loop through 'shapefiles' list to convert each shapefile to a
	# feature class in the target geodatabase (.gdb) with a new filename
	# minus the '.shp' extension
for shp_file in shapefiles:
	arcpy.FeatureClassToFeatureClass_conversion(shp_file, geodatabase, shp_file[:-4])

# print a notice of when the script has finished running
print "*** --- Script Complete --- ***"

##### --- end script --- #####
