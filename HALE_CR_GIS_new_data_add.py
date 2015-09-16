# Script Name: HALE_CR_GIS_new_data_add.py
# Author: Melanie

"""
Description: This python script incorporates new data (and new data only - not updates
to existing data) into a park-specific cultural resources GIS. A common situation in
which to use this Script Tool is after a new survey where only new sites were recorded.

Note: All new sites must already have SIHP numbers.


I created this python script to make the integration of new cultural resources
data significantly easier, particularly for users with only basic familiarity with GIS.


I run this as a Script Tool in ArcGIS.
"""


# grab 'arcpy' library and 'env' class
import arcpy
from arcpy import env

# set parameter acquisition for Script Tool
geodatabase = arcpy.GetParameterAsText(0) # <-- ScriptTool "HALE CR GIS geodatabase"
excels = arcpy.GetParameterAsText(1) # <-- ScriptTool "Folder of new data Excel spreadsheets"

#use when hard-coding (and comment off the above ArcGIS Script Tool "get parameters")
#excels = "C:/Users/Melanie/Desktop/python/fullHALE"
#geodatabase = "C:/Users/Melanie/Desktop/python/fullHALE.gdb"

# create function to convert excel files to tables
# ******converting to dBASE files truncates field names longer than 10 characters!!! hiss!***
def excelTOtable():
	env.workspace = excels

	excel_list = arcpy.ListFiles()
	for filename in excel_list:
		arcpy.ExcelToTable_conversion(filename, filename) 
		print "File %s converted to DBASE file." % filename

	DBASEs = arcpy.ListTables()
	for filename in DBASEs:
		arcpy.TableToTable_conversion(filename, geodatabase, filename[:-4]+"_tempTable")
		print "File %s converted to Table." % filename
		arcpy.Delete_management(filename)
		print "Redundant DBASE files deleted."


# create function to calculate field for "Sites_point" FC, fields Easting and Northing
def calcXY():
	env.workspace = geodatabase
	files_list = arcpy.ListFeatureClasses()

	for filename in files_list:
		if "Sites_point" in filename and "tempFC" in filename:
			arcpy.CalculateField_management(filename, "UTM_Easting", "!SHAPE.CENTROID.X!", "PYTHON_9.3")
			arcpy.CalculateField_management(filename, "UTM_Northing", "!SHAPE.CENTROID.Y!", "PYTHON_9.3")
			print "\nThe Easting and Northing in %s have been calculated.\n" % filename


# create function to correct field names in table
def alterFields():
	env.workspace = geodatabase
	tables_list = arcpy.ListTables()
	
	for table in tables_list:
		if "Labs_table" in table and "tempTable" in table:
			arcpy.AlterField_management(table, "Full_Lab_N", "Full_Lab_Name")
			arcpy.AlterField_management(table, "Lab_Addres", "Lab_Address")
			print "\nField names in %s have been synced.\n" % table

		elif "OtherSitesTable" in table and "tempTable" in table:
			arcpy.AlterField_management(table, "Site_ID_Ke", "Site_ID_Key")
			arcpy.AlterField_management(table, "Full_Site_", "Full_Site_No")
			arcpy.AlterField_management(table, "No_Feature", "No_Features")
			arcpy.AlterField_management(table, "Radiocarbo", "Radiocarbon_ID")
			arcpy.AlterField_management(table, "Notable_Fi", "Notable_Finds")
			print "\nField names in %s have been synced.\n" % table

		elif "Radiocarbon_table" in table and "tempTable" in table:
			arcpy.AlterField_management(table, "Radiocarbo", "Radiocarbon_ID")
			arcpy.AlterField_management(table, "ANalysis_M", "ANalysis_Method")
			arcpy.AlterField_management(table, "Material_T", "Material_Type")
			print "\nField names in %s have been synced.\n" % table

		elif "Reports_table" in table and "tempTable" in table:
			arcpy.AlterField_management(table, "Prepared_B", "Prepared_By")
			arcpy.AlterField_management(table, "Prepared_F", "Prepared_For")
			arcpy.AlterField_management(table, "Where_Avai", "Where_Available")
			arcpy.AlterField_management(table, "Associated", "Associated_Survey_Name")
			print "\nField names in %s have been synced.\n" % table

		elif "Sites_Table" in table and "tempTable" in table:
			arcpy.AlterField_management(table, "Site_ID_Ke", "Site_ID_Key")
			arcpy.AlterField_management(table, "Full_Site_", "Full_Site_No")
			arcpy.AlterField_management(table, "No_Feature", "No_Features")
			arcpy.AlterField_management(table, "Radiocarbo", "Radiocarbon_ID")
			arcpy.AlterField_management(table, "Notable_Fi", "Notable_Finds")
			arcpy.AlterField_management(table, "Other_Site", "Other_Site_Designations")
			print "\nField names in %s have been synced.\n" % table

		elif "Surveys_table" in table and "tempTable" in table:
			arcpy.AlterField_management(table, "Survey_Nam", "Survey_Name")
			arcpy.AlterField_management(table, "Survey_Lev", "Survey_Level")
			arcpy.AlterField_management(table, "No_of_Feat", "No_of_Features")
			arcpy.AlterField_management(table, "No_of_Site", "No_of_Sites")
			print "\nField names in %s have been synced.\n" % table

		elif "TempSitesTable" in table and "tempTable" in table:
			arcpy.AlterField_management(table, "Site_ID_Ke", "Site_ID_Key")
			arcpy.AlterField_management(table, "Full_Site_", "Full_Site_No")
			arcpy.AlterField_management(table, "No_Feature", "No_Features")
			arcpy.AlterField_management(table, "Radiocarbo", "Radiocarbon_ID")
			arcpy.AlterField_management(table, "Notable_Fi", "Notable_Finds")
			print "\nField names in %s have been synced.\n" % table

		elif "TUs_table" in table and "tempTable" in table:
			print "\nAs of 14 Sept 2015, the TUs_table is not populated.\n"


# create function to append each FC and Table file in the HALE CR GIS geodatabase
def append_new_sitesFC_data():
	env.workspace = geodatabase
	files_list = arcpy.ListFeatureClasses()

	for filename in files_list:
		if "Sites_point" in filename and "tempFC" in filename:
			arcpy.Append_management(filename,geodatabase+"/Sites_point", "TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase.\n" % filename
			
		elif "Sites_polygon" in filename and "tempFC" in filename:
			arcpy.Append_management(filename,geodatabase+"/Sites_polygon", "TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase.\n" % filename
					
		elif "Sites_point_nonSHPD" in filename and "tempFC" in filename:
			arcpy.Append_management(filename,geodatabase+"/Sites_point_nonSHPD", "TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase.\n" % filename
			
		elif "Sites_polygon_nonSHPD" in filename and "tempFC" in filename:
			arcpy.Append_management(filename,geodatabase+"/Sites_polygon_nonSHPD", "TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase.\n" % filename


'''
# !ALERT! --> this needs to be updated for features files
def append_new_featFC_data():
	env.workspace = geodatabase
	files_list = arcpy.ListFeatureClasses()

	for filename in files_list:
		if "Sites_point" in filename and "tempFC" in filename:
			arcpy.Append_management(filename, geodatabase+"/Sites_point", "TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase.\n" % filename
			
		elif "Sites_polygon" in filename and "tempFC" in filename:
			arcpy.Append_management(filename, geodatabase+"/Sites_polygon", "TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase.\n" % filename
					
		elif "Sites_point_nonSHPD" in filename and "tempFC" in filename:
			arcpy.Append_management(filename, geodatabase+"/Sites_point_nonSHPD", "TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase.\n" % filename
			
		elif "Sites_polygon_nonSHPD" in filename and "tempFC" in filename:
			arcpy.Append_management(filename, geodatabase+"/Sites_polygon_nonSHPD", "TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase.\n" % filename
'''


def append_new_FC_data():
	env.workspace = geodatabase
	files_list = arcpy.ListFeatureClasses()
	
	for filename in files_list:
		if "Districts_polygon" in filename and "tempFC" in filename:
			arcpy.Append_management(filename,geodatabase+"/Districts_polygon", "TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase.\n" % filename
			
		elif "Surveys_polygon" in filename and "tempFC" in filename:
			arcpy.Append_management(filename,geodatabase+"/Surveys_polygon", "TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase.\n" % filename
			
		elif "TUs_polygon" in filename and "tempFC" in filename:
			arcpy.Append_management(filename,geodatabase+"/TUs_polygon", "TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase.\n" % filename


def append_new_Table_data():
	env.workspace = geodatabase
	tables_list = arcpy.ListTables()
	
	for table in tables_list:
		if "Sites_Table" in table and "tempTable" in table:
			arcpy.Append_management(table, geodatabase+"/Sites_Table", "NO_TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase." % table

		elif "OtherSitesTable" in table and "tempTable" in table:
			arcpy.Append_management(table, geodatabase+"/Other_Sites_Table", "NO_TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase.\n" % table
			
		elif "TempSitesTable" in table and "tempTable" in table:
			arcpy.Append_management(table, geodatabase+"/Temp_Sites_Table", "NO_TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase.\n" % table
			
		elif "Surveys_table" in table and "tempTable" in table:
			arcpy.Append_management(table, geodatabase+"/Surveys_table", "NO_TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase.\n" % table
			
		elif "TUs_table" in table and "tempTable" in table:
			arcpy.Append_management(table, geodatabase+"/TUs_table", "NO_TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase.\n" % table
			
		elif "Reports_table" in table and "tempTable" in table:
			arcpy.Append_management(table, geodatabase+"/Reports_table", "NO_TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase.\n" % table
			
		elif "Radiocarbon_table" in table and "tempTable" in table:
			arcpy.Append_management(table, geodatabase+"/Radiocarbon_table", "NO_TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase.\n" % table
			
		elif "Labs_table" in table and "tempTable" in table:
			arcpy.Append_management(table, geodatabase+"/Labs_table", "NO_TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase.\n" % table


'''
# !ALERT! --> this needs to be updated for features files
def append_new_featTable_data():
	env.workspace = geodatabase
	tables_list = arcpy.ListTables()
	
	for table in tables_list:
		if "Features_table" in table and "tempTable" in table:
			arcpy.Append_management(table, geodatabase+"/Features_table", "NO_TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase." % table

		elif "Temp_Features_table" in table and "tempTable" in table:
			arcpy.Append_management(table, geodatabase+"/Temp_Features_table", "NO_TEST")
			print "\nThe new data in %s was added to the HALE CR GIS geodatabase." % table
'''

# create function to delete tables created from excel files
def delete():
	env.workspace = geodatabase
	tables_list = arcpy.ListTables()
	files_list = arcpy.ListFeatureClasses()

	for table in tables_list:
		if "tempTable" in table:
			arcpy.Delete_management(table)

	print "Redundant table files deleted."

	for filename in files_list:
		if "tempFC" in filename:
			arcpy.Delete_management(filename)

	print "Redundant FC files deleted."


### --- run functions --- ###

excelTOtable() 
calcXY() 
alterFields() 

append_new_sitesFC_data()
###### --- append_new_featFC_data()
append_new_FC_data() 
append_new_Table_data() 
###### --- append_new_featTable_data()

delete()

print "*** --- New Data Appended to HALE CR GIS Complete --- ***"
