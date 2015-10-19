# PUHE_MAP_TF_date_update.py

'''
This script updates the date, both in the filename and in the map layout, 
when I add new GPS data to the Temporary Feature (TF) Map. It then creates 
a PDF of this updated map. This script was written to aid a National Park 
Service project I'm currently working on (from 21 Sept 2015 to present).
'''


# grab 'arcpy' library, operating system library, and 'datetime' class
import arcpy
import os
from datetime import date



# create function that converts today's date to the format I like
def format_today():
	months = {'1':'january', 
		'2':'february',
		'3':'march',
		'4':'april',
		'5':'may',
		'6':'june',
		'7':'july',
		'8':'august',
		'9':'september',
		'10':'october',
		'11':'november',
		'12':'december'}

	rawtoday = str(date.today())
	rawmonth = rawtoday[5:7]
	day = rawtoday[-2:]
	month = months[rawmonth]
	year = rawtoday[:4]

	today = day + month[:3] + year
	return today

	

# create a function that updates the date in the TF Map layout
def layout_update():
	folder = "c:/Users/Melanie/Desktop/PUHE/0-PUHEfireCRGIS/MAPS"
	all_files = os.listdir(folder)
	TF_map_file = ""
	
	for filename in all_files:
		if "MAP_TF_as of" in filename and ".mxd" in filename:
			TF_map_file = filename

	TF_map = folder + "/" + TF_map_file
	TF_mxd = arcpy.mapping.MapDocument(TF_map)

	eleList = arcpy.mapping.ListLayoutElements(TF_mxd, "TEXT_ELEMENT")
		
	for ele in eleList:
		if "Last Updated" in ele.text:
			ele.text = "Last Updated: " + today
			
	TF_mxd.save()
			
					

# create function that updates the TF Map filename
def filename_update():
	folder = "c:/Users/Melanie/Desktop/PUHE/0-PUHEfireCRGIS/MAPS"
	all_files = os.listdir(folder)
	TF_map = ""
	
	for filename in all_files:
		if ".mxd" in filename and "MAP_TF_as of" in filename:
			TF_map = filename

	file1 = TF_map[:-12]  # stores all the characters in the filename that
		# come before the date as variable 'file1'
	file3 = TF_map[-4:]  # stores all the characters in the filename that
		# come after the date as variable 'file3'
	new_name = file1 + today + file3  # stores our new, updated filename by
		# concatenating our 'file1' variable with our 'new_date' variable with our
		# 'file3' variable
	os.rename(os.path.join(folder,TF_map),os.path.join(folder,new_name))  # takes
		# our old filename and replaces it with the new filename



# create function that exports this date-updated map to PDF
def create_PDF():
	folder = "c:/Users/Melanie/Desktop/PUHE/0-PUHEfireCRGIS/MAPS"
	all_files = os.listdir(folder)
	TF_map_file = ""
	
	for filename in all_files:
		if "MAP_TF_as of" in filename and ".mxd" in filename:
			TF_map_file = filename


	TF_map = folder + "/" + TF_map_file
	TF_mxd = arcpy.mapping.MapDocument(TF_map)

	pdf_name = TF_map[:-4] + ".pdf"
	
	arcpy.mapping.ExportToPDF(TF_mxd, pdf_name)



# set global variables
today = format_today()

# - # Run Functions
layout_update()
filename_update()
create_PDF()  

print "*** --- Script Complete --- ***\n"
