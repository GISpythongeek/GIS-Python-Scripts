# PUHEtransfer-ScriptTool.py

'''
This ScriptTool is to be used to ensure compliance with the NPS Cultural resources
GIS transfer standard when transfering cultural resources GIS data to any
place outside the specific park unit in which it originated. It creates a new 
transfer project geodatabase, copies the relevant data files (FCs and Tables) 
from the park's Master CR GIS to the new transfer project folder, and creates 
the necessary and compliant feature class files. Finally, it re-projects the feature
class files into NAD83 Geographic Coordinate System (required by the NPS CR GIS
transfer standard). The new transfer project geodatabase is then ready for transfer.

This script was written to aid a National Park Service project I'm currently
working on (from 21 Sept 2015 to present).
'''

# grab 'arcpy' library and 'env' class
import arcpy
from arcpy import env


#-# PARAMETER GLOBAL VARIABLES (set parameter acquisition for Script Tool)
master_gdb = arcpy.GetParameterAsText(0) # <-- ScriptTool "Select Master Geodatabase"
gdb_location = arcpy.GetParameterAsText(1) # <-- ScriptTool "Select Location for Transfer Geodatabase"
gdb_name = arcpy.GetParameterAsText(2) # <-- ScriptTool "Name for Transfer Geodatabase"
which_FCs = arcpy.GetParameterAsText(3) # <-- ScriptTool "Which Feature Class(es) Would You Like to Transfer? (see CR GIS Documentation)"


#-# GLOBAL VARIABLES
# create variable for path to new transfer gdb
trans_gdb = gdb_location + "/" + gdb_name + ".gdb"
germane_FCs = []
germane_tables = []


#-# FUNCTIONS

################################--create gdb--###############################################

### Done (works - 16oct2015 955am)
# create a function that creates a new file geodatabase
def create_gdb():
    arcpy.CreateFileGDB_management(gdb_location, gdb_name)



################################--controler--###############################################

### Done (works 16oct2015 1200noon)
# create controler sub-functions
def gather_any_singleFC(): # <-- Done (works 16oct2015 1130am)
    germane_FCs.append(which_FCs)
    
def gather_any_singleTAB(): # <-- Done (works 16oct2015 1130am)
    if "_pt" in which_FCs:
        germane_tables.append(which_FCs[:-3])
    elif "_line" in which_FCs or "_poly" in which_FCs:
        germane_tables.append(which_FCs[:-5])
        
def gather_any_groupFC(): # <-- Done (works 16oct2015 1145am)
    if which_FCs == "HistoricDistrict":
        germane_FCs.append(which_FCs + "_poly")
    elif which_FCs == "HistoricBuilding":
        germane_FCs.append(which_FCs + "_pt")
        germane_FCs.append(which_FCs + "_poly")
    else:
        germane_FCs.append(which_FCs + "_pt")
        germane_FCs.append(which_FCs + "_line")
        germane_FCs.append(which_FCs + "_poly")

def gather_any_groupTAB(): # <-- Done (works 16oct2015 1145am)
    germane_tables.append(which_FCs)
    
def gather_allFC(): # <-- Done (works 16oct2015 1200noon)
    if which_FCs == "ALL":
        HB = "HistoricBuilding"
        HS = "HistoricStructure"
        HO = "HistoricObject"
        HSite = "HistoricSite"
        HD = "HistoricDistrict"
        CRO = "CultureResourceOther"
        SV = "Survey"
        
        germane_FCs.append(HB + "_pt")
        germane_FCs.append(HB + "_poly")

        germane_FCs.append(HS + "_pt")
        germane_FCs.append(HS + "_line")
        germane_FCs.append(HS + "_poly")

        germane_FCs.append(HO + "_pt")
        germane_FCs.append(HO + "_line")
        germane_FCs.append(HO + "_poly")

        germane_FCs.append(HSite + "_pt")
        germane_FCs.append(HSite + "_line")
        germane_FCs.append(HSite + "_poly")

        germane_FCs.append(HD + "_poly")

        germane_FCs.append(CRO + "_pt")
        germane_FCs.append(CRO + "_line")
        germane_FCs.append(CRO + "_poly")

        germane_FCs.append(SV + "_pt")
        germane_FCs.append(SV + "_line")
        germane_FCs.append(SV + "_poly")

def gather_allTAB(): # <-- Done (works 16oct2015 1200noon)
    if which_FCs == "ALL":
        HB = "HistoricBuilding"
        HS = "HistoricStructure"
        HO = "HistoricObject"
        HSite = "HistoricSite"
        HD = "HistoricDistrict"
        CRO = "CultureResourceOther"
        SV = "Survey"

        germane_tables.append(HB)
        germane_tables.append(HS)
        germane_tables.append(HO)
        germane_tables.append(HSite)
        germane_tables.append(HD)
        germane_tables.append(CRO)
        germane_tables.append(SV)
   
### Done (works 16oct2015 1145am)
# create controler functions
def gather_all(): # <-- Done (works 16oct2015 1145am)
    gather_allFC()
    gather_allTAB()

def gather_group(): # <-- Done (works 16oct2015 1130am)
    gather_any_groupFC()
    gather_any_groupTAB()

def gather_single(): # <-- Done (works 16oct2015 1130am)
    gather_any_singleFC()
    gather_any_singleTAB()

### Done (works - 16oct2015 955am)
# create function that decides what to do next:  ALL, group of FCs in a feature dataset, single FC 
def controler(): # <-- Done (works 16oct2015 1200noon)
    if which_FCs == "ALL":
        gather_all()
    elif which_FCs == "HistoricBuilding":
        gather_group()
    elif which_FCs == "HistoricStructure":
        gather_group()
    elif which_FCs == "HistoricObject":
        gather_group()
    elif which_FCs == "HistoricSite":
        gather_group()
    elif which_FCs == "HistoricDistrict":
        gather_group()
    elif which_FCs == "CultureResourceOther":
        gather_group()
    elif which_FCs == "Survey":
        gather_group()
    elif "_" in which_FCs:
        gather_single()
    
    

################################--copy--###############################################

### Done (works - 16oct2015 135pm)
# create a funtion that copies the relevant FCs and Tables to the new transfer gdb
def copy():
    env.workspace = master_gdb

    for filename in germane_FCs:
        arcpy.FeatureClassToFeatureClass_conversion(filename, trans_gdb, filename)
    for tablename in germane_tables:
        arcpy.TableToTable_conversion(tablename, trans_gdb, tablename)



################################--join--###############################################

### Done (works - 16oct2015 300pm)
# create join function (including deleting redundant fields)
def join():
    env.workspace = trans_gdb

    field = "KEY_ID"
    del_fields = ["SIHP_NO_1", "FEAT_NO_1", "KEY_ID_1"]

    HB = "HistoricBuilding"
    HS = "HistoricStructure"
    HO = "HistoricObject"
    HSite = "HistoricSite"
    HD = "HistoricDistrict"
    CRO = "CultureResourceOther"
    SV = "Survey"

    for filename in germane_FCs:
        if HB in filename:
            arcpy.JoinField_management(filename, field, HB, field)
            arcpy.DeleteField_management(filename, del_fields)
        elif HS in filename:
            arcpy.JoinField_management(filename, field, HS, field)
            arcpy.DeleteField_management(filename, del_fields)
        elif HO in filename:
            arcpy.JoinField_management(filename, field, HO, field)
            arcpy.DeleteField_management(filename, del_fields)
        elif HSite in filename:
            arcpy.JoinField_management(filename, field, HSite, field)
            arcpy.DeleteField_management(filename, del_fields)
        elif HD in filename:
            arcpy.JoinField_management(filename, field, HD, field)
            arcpy.DeleteField_management(filename, del_fields)
        elif CRO in filename:
            arcpy.JoinField_management(filename, field, CRO, field)
            arcpy.DeleteField_management(filename, del_fields)
        elif SV in filename:
            arcpy.JoinField_management(filename, field, SV, field)
            arcpy.DeleteField_management(filename, del_fields)
        


################################--delete tables--#########################################

### Done (works - 16oct2015 310pm)
# create function that deletes redundant tables
def delete1():
    env.workspace = trans_gdb

    tab_list = arcpy.ListTables()

    for tablename in tab_list:
        arcpy.Delete_management(tablename)



################################--re-project FCs--###############################################

### Done (works - 16oct2015 545pm)
# create function that re-projects the FCs to GCS NAD83
def reproject():
    env.workspace = trans_gdb

    fc_list = arcpy.ListFeatureClasses()

    for filename in fc_list:
        newCoord = arcpy.SpatialReference('NAD 1983')
        arcpy.Project_management(filename, filename+"_NAD83", newCoord)



###########################--delete PA11 projected FCs--###################################

### Done (works - 16oct2015 615pm)
# create function that deletes PA11 projected FCs
def delete2():
    env.workspace = trans_gdb

    fc_list = arcpy.ListFeatureClasses()

    for filename in fc_list:
        if "NAD83" not in filename:
            arcpy.Delete_management(filename)



###########################--rename NAD83 FCs--###################################

### Done (works - 16oct2015 615pm)
# create function that deletes redundant tables
def rename():
    env.workspace = trans_gdb

    fc_list = arcpy.ListFeatureClasses()

    for filename in fc_list:
        arcpy.Rename_management(filename, filename[:-6])



##############################---------------#####################################

# -- run functions -- #
create_gdb()
controler()
copy()
join()
delete1()
reproject()
delete2()
rename()
