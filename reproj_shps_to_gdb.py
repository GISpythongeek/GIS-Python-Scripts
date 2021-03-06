# Script Name: reproj_shps_to_gdb.py
# Author: Melanie

"""
Description: This relatively simple python script for ArcGIS converts a folder full
of shapefiles into feature class files in a desired geodatabase, keeping
the filename intact minus the '.shp' extension. Then it re-projects these
feature class files into the desired new coordinate system (new files will be created
with a new filename that identifies the new coordinate system, then the old files 
will be deleted).

I created this script because I often have numerous shapefiles that need to be
converted into feature class files, organized into a geodatabase, and then
re-projected into the coordinate system I want to use (and have the old files 
removed from the geodatabase). 

I run this with PythonWin.
"""

# grab 'arcpy' library and 'env' class
import arcpy
from arcpy import env


# create function 'shpTOgdb' to convert the shapefiles to feature class files
	### where '...XXX/XXX...' represents the specific desired directory path
def shpTOgdb():
    env.workspace = "c:/XXX/XXX/XXX"
    geodatabase = "c:/XXX/XXX/XXX.gdb"
    shapefiles = arcpy.ListFeatureClasses()

    for shp_file in shapefiles:
    	arcpy.FeatureClassToFeatureClass_conversion(shp_file, geodatabase, shp_file[:-4])

    print "* - Shapefiles converted to FC files - *"


# create function 'projectUTM' to re-project to new coordinate system,
	# for example, as in this case, to NAD 1983 UTM Zone 10N
def projectUTM():
    env.workspace = "c:/XXX/XXX/XXX.gdb"
    fc_list = arcpy.ListFeatureClasses()

    for fc in fc_list:
        newCoord = arcpy.SpatialReference('NAD 1983 UTM Zone 10N') # <-- ADD desired coord system
        arcpy.Project_management(fc, fc+"_UTM", newCoord) # <-- ADD desired filename ID
        print "* - Feature Class %s has been reprojected to UTM10N - *" % fc # <-- ADD desired message


# create function 'deleteProjSHP' to delete unwanted projected shapefiles
def deleteProjFiles():
    env.workspace = "c:/XXX/XXX/XXX.gdb"
    data_type = ""
    fc_list = arcpy.ListFeatureClasses()

    for fc in fc_list:
        if "UTM" not in fc:
            arcpy.Delete_management(fc, data_type)
            print "Shapefile %s has been deleted." % fc
        else:
            print "Shapefile %s has been kept." % fc
    

# run functions
shpTOgdb()
projectUTM()
deleteProjFiles()

# print a notice of when the script has finished running
print "*** --- Script Complete --- ***"
