# Script Name: inundation_analysis.py
# Author: Melanie

"""
Description: This python script generates feature class files and excel (.xls) 
spreadsheets listing the sites affected by different sea level inundation 
scenarios (e.g., inundation of 0.5m, 1.0m, 1.5m, etc.), including area inundated 
(e.g., m2, acres) and percentage of site area inundated (e.g., 25.40%, 72.56%, 99.99%). 

I created this script in preparation for additional and/or updated inundation 
data for a climate change impact study.  The project consists of identifying
coastal archaeological and cultural sites that are likely to be impacted by sea 
level rise in a National Park in Hawaii.

I run this with PythonWin.
"""

# grab 'arcpy' library and 'env' class
import arcpy
from arcpy import env

# create function 'shpTOgdb' to convert shapefiles to feature class files
    # where '...XXX/XXX...' represents the specific desired directory path
def shpTOgdb():
    env.workspace = "c:/XXX/XXX/XXX"
    geodatabase = "c:/XXX/XXX/XXX .gdb"
    shapefiles = arcpy.ListFeatureClasses()

    for shp_file in shapefiles:
        arcpy.FeatureClassToFeatureClass_conversion(shp_file, geodatabase, shp_file[:-4])

    print "* - Shapefiles converted to FC files - *"


# create function 'projectUTM' to re-project to new coordinate system,
    # in this case UTM Zone 5N
def projectUTM():
    fc_list = arcpy.ListFeatureClasses()

    for fc_file in fc_list:
        newCoord = arcpy.SpatialReference('NAD 1983 (PA11) UTM Zone 5N') # <-- ADD desired coord system
        arcpy.Project_management(fc_file, fc_file+"_UTM", newCoord) # <-- ADD desired filename ID
        print "* - Feature Class %s reprojected to UTM5N - *" % fc_file # <-- ADD desired message  # <-- MODIFY as needed (change to different coordinate system)


# create function 'deleteProjFiles' to delete unwanted files
def deleteProjFiles():
    data_type = ""
    fcs = arcpy.ListFeatureClasses()

    for fc in fcs:
        if "UTM" not in fc:  # <-- MODIFY as needed
            arcpy.Delete_management(fc, data_type)
            print "File %s has been deleted." % fc
        else:
            print "File %s has been kept." % fc
    

# create function 'intersect' to obtain inundation area
def intersect():
    master_list = arcpy.ListFeatureClasses()
    
    list1 = []
    list2 = []

    for name in master_list:
        if "Kona" in name:  # <-- MODIFY as needed
            list1.append(name)
            print "List1 now includes:", list1
        elif "site" in name:  # <-- MODIFY as needed
            list2.append(name)
            print "List2 now includes:", list2

    for filename in list1:
        arcpy.Intersect_analysis([filename,list2], filename+"_intSites")  # <-- MODIFY as needed
        print "File %s has been processed." % filename


# create function 'add_field' to add area inundated info
def add_field():
    master_list = arcpy.ListFeatureClasses()
    
    list1 = []
    field_name = "Inundation_Percent"  # <-- MODIFY as needed
        
    for name in master_list:
        if "intSites" in name:  # <-- MODIFY as needed
            list1.append(name)
            print "List1 now includes:", list1
        else:
            print "File %s has been excluded from List1." % name

    for filename in list1:
        arcpy.AddField_management(filename, field_name, "FLOAT")  # <-- MODIFY as needed
        print "%s has been added to %s." % (field_name, filename)


# create function 'calc_field' to calculate percent of area inundated
def calc_field():
    master_list = arcpy.ListFeatureClasses()
    
    list1 = []
    field_name = "Inundation_Percent"  # <-- MODIFY as needed
    expression = "(!Shape_Area!/!Area!)*100" # <-- MODIFY as needed

    for name in master_list:
        if "intSites" in name:  # <-- MODIFY as needed
            list1.append(name)
            print "List1 now includes:", list1
        else:
            print "File %s has been excluded from List1." % name

    for filename in list1:
        arcpy.CalculateField_management(filename, field_name, expression, "PYTHON_9.3")  # <-- MODIFY as needed
        print "File %s has now had it's field calculated." % filename


# create function 'dissolve' to dissolve inundated areas by site number
def dissolve():
    master_list = arcpy.ListFeatureClasses()
    
    list1 = []
    diss_field = "SITE_NO" # <-- MODIFY as needed

    for name in master_list:
        if "intSites" in name:  # <-- MODIFY as needed
            list1.append(name)
            print "List1 now includes:", list1
        else:
            print "File %s has been excluded from List1." % name

    for filename in list1:
        arcpy.Dissolve_management(filename, filename+"_final", diss_field,  # <-- MODIFY as needed
            [["Inundation_Percent","SUM"],["AREA","SUM"],["ACRES","SUM"]])  # <-- MODIFY as needed
        print "File %s has been processed." % filename


# create function 'to_excel' to export sites impacted table to Excel file
def to_excel():
    excel_folder = "c:/XXX/XXX/XXX/"  # <-- MODIFY as needed

    master_list = arcpy.ListFeatureClasses()
    list1 = []
    
    for name in master_list:
        if "final" in name:  # <-- MODIFY as needed
            list1.append(name)
            print "List1 now includes:", list1
        else:
            print "File %s has been excluded from List1." % name

    for filename in list1:
        arcpy.TableToExcel_conversion(filename, excel_folder+filename+"_excel.xls")  # <-- MODIFY as needed
        print "File %s's table has now been converted to an Excel table." % filename



### --- run functions --- ###
shpTOgdb() 

env.workspace = "c:/XXX/XXX/XXX.gdb"  # <-- MODIFY as needed
projectUTM() 
deleteProjFiles() 

intersect() 
add_field() 
calc_field() 
dissolve() 
to_excel()  


# print a notice of when the script has finished running
print "*** --- Script Complete --- ***\n"
