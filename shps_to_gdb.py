# Script Name: shps_to_gdb.py
# Created By: Melanie
# Date Created: 31 Aug 2015
# Version: 1.0

# Modifications: None

"""
Description: This simple python script for ArcGIS converts a folder full
of shapefiles into feature class files in a desired geodatabase, keeping
the filename intact minus the '.shp' extension.

I created this script because I often have numerous shapefiles that need to be
converted into feature class files and organized into a geodatabase. (Plus,
this is my first crack at automating my workflow using a python script, so
even though it's super simple, I'm still very proud of it!)

I run this with PythonWin.  I also created a Script Tool by re-setting my 
variables to get them from the Script Tool dialog box using the 'arcpy.
GetParameterAsTex(x)' function, as follows:

	shp_folder = arcpy.GetParameterAsText(0)
	geodatabase = arcpy.GetParameterAsText(1)
	env.workspace = shp_folder

I then of course had to cut the code where I originally set the env.workspace
and where I set the geodatabase. This Script Tool makes running this script
in ArcGIS super convenient and easy.
"""

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
