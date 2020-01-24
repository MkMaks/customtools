# -*- coding: UTF-8 -*-
__title__ = 'Shared Parameter Schedule'
__author__ = 'David Vadkerti'
__doc__ = 'Lists all Shared Parameters'

from pyrevit import script
from pyrevit import output
from pyrevit.coreutils import Timer
from customOutput import hmsTimer
import io

timer = Timer()

output = script.get_output()

output.print_md("# SHARED PARAMETERS SCHEDULE")

# md_schedule = "| Number | View Name | View ID | Author | View Type |\n| ----------- | ----------- | ----------- | ----------- | ----------- |"
scheduleData = []
filePath = "L:\\REVIT\\Kniznica_REVIT\\4_Parametre\\GFI-shared-parametre.txt"
try:
	f = io.open(filePath, mode="r", encoding="utf-16")
	# f = open("L:\\REVIT\\Kniznica_REVIT\\4_Parametre\\forCustomTools\\GFI-shared-parametre.txt", "rU", encoding="utf-8")

	groupDict = {}
	groupNo = 1
	for line in f:
	    # Creating Parameter group dictionary
	    diff = line[0:5]
	    if diff =="GROUP":
	        # deleting GROUP in the begining
	        strippedGroup = line[6:]
	        # name is after Tab
	        groupName = strippedGroup.split("\t")[1]
	        # cutting ending \n sign in each groupName end
	        groupName = groupName[:-1]
	        groupDict[str(groupNo)] = groupName
	        groupNo += 1
	    elif diff == "PARAM":
	        strippedParam = line[5:]        
	        # split to list by columns - tabs
	        paramPartList = line.split("\t")
	        # param name is in 3rd column
	        paramName = paramPartList[2]
	        paramDataType = paramPartList[3]
	        paramGroupNo = str(paramPartList[5])
	        paramGroupName = groupDict.get(paramGroupNo)
	        paramDescription = paramPartList[7][:200]
	        paramList = [paramName, paramDataType, paramGroupName, paramDescription]
	        # paramList = [paramName, paramDataType, paramGroupName]

	        scheduleData.append(paramList)
	        # print "\t".join(paramList)

	    # countLines += 1
	# print(groupDict)

	   
	output.print_table(table_data=scheduleData,
	                   title = filePath,
	                   columns=["Name", "Data Type", "Group", "Description"],
	                   formats=['', '', '', ''])

	# for timing------
	endtime = timer.get_time()
	print(hmsTimer(endtime))
except:
    print("Source file should be saved with unicode (UTF-16) encoding.")