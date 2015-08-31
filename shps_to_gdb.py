# Script Name: shps_to_gdb.py
# Created By: Melanie
# Date Created: 31 Aug 2015
# Version: 1.0

"""
Description: This simple python script for ArcGIS converts a folder full
of shapefiles into feature class files in a desired geodatabase, keeping
the filename intact minus the '.shp' extension.

I created this script because I often have numerous shapefiles that need to be
converted into feature class files and organized into a geodatabase. (Plus,
this is my first crack at automating my workflow using a python script, so
even though it's super simple, I'm still very proud of it!)

I run this with PythonWin.
"""

##### --- Converts Multiple Shapefiles (.shp) to FCs in a Geodatabase (.gdb) --- #####

# grab 'arcpy' library and 'env' class
import arcpy
from arcpy import env

# set current workspace and environment,
	# where '...XXX/XXX...' represents the specific desired directory path
env.workspace = "c:/XXX/XXX/XXX"
#-optional, depending on the situation --->  env.overwriteOutput = True

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
