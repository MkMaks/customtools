# -*- coding: UTF-8 -*-
__title__ = 'Shared Parameter Schedule'
__author__ = 'David Vadkerti'
__doc__ = 'Lists all Shared Parameters from text config file.You can sort parameters by Parameter Name or by Group. For Search open html file in your browser.'

from pyrevit import script
from pyrevit import output, forms
from pyrevit.coreutils import Timer
from customOutput import hmsTimer
import io

timer = Timer()

output = script.get_output()

def showParamSchedule(sortByParamName):
    output.print_md("# SHARED PARAMETERS SCHEDULE")

    def parseSharedParamFile(filePath,encodingType):
        scheduleData = []
        f = io.open(filePath, mode="r", encoding=encodingType)

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

                scheduleData.append(paramList)

        # sort by parameter name
        if sortByParamName == "Parameter Name":
        	sortedScheduleData = sorted(scheduleData, key=lambda x: x[0].lower())
        # sort by parameter group
        elif sortByParamName == "Group Name":
           	sortedScheduleData = sorted(scheduleData, key=lambda x: x[2].lower())
        else:
        	sortedScheduleData = scheduleData
        # sortedScheduleData = sorted(scheduleData, key=lambda x: x[index])
        output.print_table(table_data=sortedScheduleData,
                           title = filePath,
                           columns=["Name", "Data Type", "Group", "Description"],
                           formats=['', '', '', ''])

        # for timing------
        endtime = timer.get_time()
        print(hmsTimer(endtime))

    filePath = "U:\\REVIT\\Kniznica_REVIT\\4_Parametre\\GFI-shared-parametre.txt"

    try:
        parseSharedParamFile(filePath,"utf-16")
    except:
        try:
            parseSharedParamFile(filePath,"utf-8")
        except:
            print("Source file should be saved with unicode UTF-16 encoding.")


selected_option = \
    forms.CommandSwitchWindow.show(
        ['Parameter Name',
         'Group Name',
         "Do Not Sort"],
        message='Sort by:'
        )

if selected_option:
    showParamSchedule(selected_option)