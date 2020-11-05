# -*- coding: UTF-8 -*-
from __future__ import division
import clr
import System
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
from Autodesk.Revit.DB import *

import revit_script_util
from revit_script_util import Output

sessionId = revit_script_util.GetSessionId()
uiapp = revit_script_util.GetUIApplication()
app = uiapp.Application
doc = revit_script_util.GetScriptDocument()
# revitFilePath = revit_script_util.GetRevitFilePath()


import os.path as op
import math
from datetime import datetime

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, ImportInstance
# from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.DB import LinePatternElement, Family, TextNoteType, ScheduleSheetInstance, WorksetTable, TextNote, ReferencePlane


# returns file name - everything in path from "\" to the end
# def nameFromPath(path):
#     try:
#         index = path.rindex("\\") + 1
#     except:
#         index = path.rindex("/") + 1        
#     return path[index:]

# # printing file name and heading
# name = doc.PathName
# if len(name) == 0:
#     name = "Not saved file"
# try:
#     printedName = nameFromPath(name)
# except:
#     printedName = name



# returns file name - everything in path from "\\" or "/" to the end
def path2fileName(file_path,divider):
  # file_path_split = file_path.split("\\")
  file_path_split = file_path.split(divider)
  file_name = file_path_split[-1]
  # file_name = file_name[:-4]
  # print file_name
  return file_name

def userNamePurge(file_name):
    def centralPathSplitter(new_file_name):
        file_path_split = new_file_name.split("/")
        new_file_name = file_path_split[-1]
        return new_file_name + extension

    def pathSplitter(new_file_name):
        file_path_split = file_name.split("\\")
        new_file_name = file_path_split[-1]
        return new_file_name

    # userName and detached purge
    revit_user_name = "davidv"
    file_path_split_name = file_name.split("_")

    # extension extraction
    file_path_split_ext = file_name.split(".")
    extension = "."+file_path_split_ext[-1]

    if file_path_split_name[-1] == "detached.rvt" and file_path_split_name[-2] == revit_user_name:
        file_name_list = file_path_split_name[0:-2]
        new_file_name = "_".join(file_name_list)
        centralPath = centralPathSplitter(new_file_name)
    elif file_path_split_name[-1] == "detached.rvt":
        file_name_list = file_path_split_name[0:-1]
        new_file_name = "_".join(file_name_list)
        centralPath = centralPathSplitter(new_file_name)
    elif file_path_split_name[-1] == revit_user_name + ".rvt":
        file_name_list = file_path_split_name[0:-1]
        new_file_name = "_".join(file_name_list)
        centralPath = centralPathSplitter(new_file_name)
    else:
        file_name_list = file_path_split_name
        new_file_name = "_".join(file_name_list)
        centralPath = pathSplitter(new_file_name)

    return centralPath


# printing file name and heading
name = doc.PathName
if len(name) == 0:
    name = "Not saved file"
# workshared file
printedName = userNamePurge(name)


# sheets
sheets_id_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets) \
.WhereElementIsNotElementType() \
.ToElementIds()
sheetCount = len(sheets_id_collector)
# print(str(sheetCount)+" Sheets")


# schedules
schedules_id_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Schedules) \
.WhereElementIsNotElementType() \
.ToElements()
scheduleCount = 0
for schedule in schedules_id_collector:
    if schedule.Name[:19] != "<Revision Schedule>":
        scheduleCount += 1
# print(str(scheduleCount)+" Schedules")


# views
views_id_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views) \
.WhereElementIsNotElementType()
view_elements = views_id_collector.ToElements()
viewCount = len(view_elements)

copiedView = 0
for view in view_elements:
    viewName = view.LookupParameter('View Name')
    try:
        viewNameString = viewName.AsString()
        # print(viewNameString)
        if viewNameString[-6:-2] == "Copy" or viewNameString[-4:] == "Copy" or viewNameString[:7] == "Section":
        # if viewNameString[:7] == "Section":
            copiedView += 1
    except:
        pass

sheets_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets) \
.WhereElementIsNotElementType().ToElements()

# views not on sheets
viewsOnSheet = []
# schedulesOnSheet = []
for sheet in sheets_collector:
    try:        
        # scheduleslist = list()
        for item in sheet.GetAllPlacedViews():
            if item not in viewsOnSheet:
                viewsOnSheet.append(item)
    except:
        pass
viewsNotOnSheet = viewCount-len(viewsOnSheet)

# schedules not on sheets
schedulesOnSheet = []
scheduleCollector1 = FilteredElementCollector(doc).OfClass(ScheduleSheetInstance).WhereElementIsNotElementType()
scheduleCollector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Schedules) \
.WhereElementIsNotElementType()
# there is need to iterate class and category filter to get all schedule
# it is something with schedules on more sheets maybe...
for schedule in scheduleCollector:
    schedName = schedule.Name
    if schedName[:19] != "<Revision Schedule>":
        if schedName not in schedulesOnSheet:
            if schedule.OwnerViewId.IntegerValue != -1:
                # print schedName
                # print schedule.Id
                schedulesOnSheet.append(schedName)

# there is need to iterate class and category filter to get all schedule - UnionWith didn't work
for schedule in scheduleCollector1:
    schedName = schedule.Name
    if schedName[:19] != "<Revision Schedule>":
        if schedName not in schedulesOnSheet:
            if schedule.OwnerViewId.IntegerValue != -1:
                # print schedName
                # print schedule.Id
                schedulesOnSheet.append(schedName)
scheduleNotOnSheet = scheduleCount-len(schedulesOnSheet)

# warnings
allWarnings_collector = doc.GetWarnings()
allWarningsCount = len(allWarnings_collector)
# print(str(allWarningsCount)+" Warnings")


# critical warnings
# list of Warnings rated as critical
criticalWarnings = ['Elements have duplicate "Type Mark" values',
    'There are identical instances in the same place',
    'Room Tag is outside of its Room',
    'Multiple Rooms are in the same enclosed region',
    'Multiple Areas are in the same enclosed region',
    'One element is completely inside another',
    'Room is not in a properly enclosed region',
    'Room separation line is slightly off axis and may cause inaccuracies',
    'Area is not in a properly enclosed region',
    "Rectangular opening doesn't cut its host",
    'Elements have duplicate "Number" values',]
    
criticalWarningCount = 0
for criticalWarning in allWarnings_collector:
    description = criticalWarning.GetDescriptionText()
    # for warning type heading
    try:
        descLen = description.index(".")
    # Few warnings have mistakenly no dot in the end.
    except:
        descLen = len(description)
    descHeading = description[:descLen]
    if descHeading in criticalWarnings:
        criticalWarningCount += 1


# materials
materialCount = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Materials).GetElementCount()
# print(str(materialCount)+" Materials")


# line patterns
linePatternCount = FilteredElementCollector(doc).OfClass(LinePatternElement).GetElementCount()
# print(str(linePatternCount)+" Line Patterns")


# DWGs
# Change to this?
# dwg_collector = FilteredElementCollector(doc).OfClass(DB.ImportInstance).WhereElementIsNotElementType().ToElements()
dwg_collector = FilteredElementCollector(doc).OfClass(ImportInstance).WhereElementIsNotElementType().ToElements()
importedDwg = 0
dwgNotCurrentView = 0
for dwg in dwg_collector:
    if dwg.IsLinked != True:
        importedDwg += 1
    if dwg.ViewSpecific == False:
        dwgNotCurrentView += 1

# print("\nDWGs")
# print(str(importedDwg)+" Imported DWG files")

# dwgCount = dwg_collector.GetElementCount()
dwgCount = len(dwg_collector)
linkedDwg = (dwgCount-importedDwg)


# families
graphFCatHeadings = []
graphFCatData = []
families = FilteredElementCollector(doc).OfClass(Family)
inPlaceFamilyCount = 0
NotParamFamiliesCount = 0
for family in families:
    if family.IsInPlace == True:
        inPlaceFamilyCount += 1
        # for graph
        inPlaceFCategory = family.FamilyCategory.Name
        if inPlaceFCategory not in graphFCatHeadings:
            graphFCatHeadings.append(inPlaceFCategory)
        graphFCatData.append(inPlaceFCategory)
    if family.IsParametric == False:
        NotParamFamiliesCount += 1
familyCount = families.GetElementCount()


# print(str(familyCount)+" Families")
# print(str(inPlaceFamilyCount)+" In Place Families")

# print(str(NotParamFamiliesCount)+" Families are not parametric")


# Text notes width factor != 1
textNoteType_collector = FilteredElementCollector(doc).OfClass(TextNoteType).ToElements()
textnoteWFcount = 0
for textnote in textNoteType_collector:
    widthFactor = textnote.LookupParameter('Width Factor').AsDouble()
    if widthFactor != 1:
        textnoteWFcount += 1

# Text notes with allCaps applied in Revit
textNote_collector = FilteredElementCollector(doc).OfClass(TextNote).ToElements()
capsCount = 0
for textN in textNote_collector:
    capsStatus = textN.GetFormattedText().GetAllCapsStatus()
    if str(capsStatus) != "None":
        capsCount +=1

# Ramps
ramp_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Ramps).WhereElementIsNotElementType().GetElementCount()

# Architecural columns
archColumn_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Columns).WhereElementIsNotElementType().GetElementCount()

# detail groups
detailGroupCount = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_IOSDetailGroups).WhereElementIsNotElementType().GetElementCount()
detailGroupTypeCount = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_IOSDetailGroups).GetElementCount() - detailGroupCount
# print(str(detailGroupTypeCount)+" Detail Group Types")
# print(str(detailGroupCount)+" Detail Groups")


# model groups
modelGroupCount = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_IOSModelGroups).WhereElementIsNotElementType().GetElementCount()
modelGroupTypeCount = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_IOSModelGroups).GetElementCount() - modelGroupCount
# print(str(modelGroupTypeCount)+" Model Group Types")
# print(str(modelGroupCount)+" Model Groups")

# reference plane without name
refPlaneCollector = FilteredElementCollector(doc).OfClass(ReferencePlane).ToElements()
noNameRefPCount = 0
for refPlane in refPlaneCollector:
    if refPlane.Name == "Reference Plane":
        noNameRefPCount += 1

# Element Count
elementCount = FilteredElementCollector(doc).WhereElementIsNotElementType().GetElementCount()
# _2DelementCount = FilteredElementCollector(doc).OwnedByView().GetElementCount()

# print(str(elementCount)+" Elements")

# View Dependent element count
all_elements = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()

_2d_elements = 0
_3d_elements = 0
other_elements = 0

for element in all_elements:
    # filtering just element with location
    if element.Location:
        # 2D elements
        if element.ViewSpecific:
            _2d_elements += 1
        # 3D elements
        else:
            _3d_elements += 1
    # other elements
    else:
        other_elements += 1

# print("_3d_elements " + str(_3d_elements))
# print("_2d_elements " + str(_2d_elements))
# print("other_elements " + str(other_elements))

# calculating percentage
if _2d_elements > 0:
    # _2d_elements_perc = round(_2d_elements/elementCount*100)
    _2d_elements_perc = int(round(_2d_elements/elementCount*100,0))
else:
    _2d_elements_perc = 0
# print("_2D_elements_perc " + str(_2d_elements_perc))



# tabulator between data to easy import to excel schedule
separator = "\t"

datestamp = str(datetime.now())
table_header = ("fileName" + separator
    + "datestamp" + separator
    + "viewCount" + separator
    + "copiedView" + separator
    + "sheetCount" + separator
    + "scheduleCount" + separator
    + "viewsNotOnSheet" + separator
    + "scheduleNotOnSheet" + separator
    + "allWarningsCount" + separator
    + "criticalWarningCount" + separator
    + "materialCount" + separator
    + "linePatternCount" + separator
    + "importedDwg" + separator
    + "linkedDwg" + separator
    + "dwgNotCurrentView" + separator
    + "familyCount" + separator
    + "inPlaceFamilyCount" + separator
    + "NotParamFamiliesCount" + separator
    + "textnoteWFcount" + separator
    + "capsCount" + separator
    + "ramp_collector" + separator
    + "archColumn_collector" + separator
    + "detailGroupTypeCount" + separator
    + "detailGroupCount " + separator
    + "modelGroupTypeCount" + separator
    + "modelGroupCount" + separator
    + "noNameRefPCount" + separator
    + "elementCount" + separator
    + "_2d_elements" + separator
    + "_3d_elements" + separator
    + "_2d_elements_perc" + separator
    + "other_elements" + separator)

table_content = (printedName + separator
    + datestamp[0:16] + separator
    + str(viewCount) + separator
    + str(copiedView) + separator
    + str(sheetCount) + separator
    + str(scheduleCount) + separator
    + str(viewsNotOnSheet) + separator
    + str(scheduleNotOnSheet) + separator
    + str(allWarningsCount) + separator
    + str(criticalWarningCount) + separator
    + str(materialCount) + separator
    + str(linePatternCount) + separator
    + str(importedDwg) + separator
    + str(linkedDwg) + separator
    + str(dwgNotCurrentView) + separator
    + str(familyCount) + separator
    + str(inPlaceFamilyCount) + separator
    + str(NotParamFamiliesCount) + separator
    + str(textnoteWFcount) + separator
    + str(capsCount) + separator
    + str(ramp_collector) + separator
    + str(archColumn_collector) + separator
    + str(detailGroupTypeCount) + separator
    + str(detailGroupCount ) + separator
    + str(modelGroupTypeCount) + separator
    + str(modelGroupCount) + separator
    + str(noNameRefPCount) + separator
    + str(elementCount) + separator
    + str(_2d_elements) + separator
    + str(_3d_elements) + separator
    + str(_2d_elements_perc) + separator
    + str(other_elements) + separator)


def model_checker_logger(printedName):
    # One log file per revit file
    # if file exists
    log_location = "L:\\customToolslogs\\model_checker"
    log_file_name = log_location + printedName
    try:    
        # check wether file exists
        f = open(log_file_name + ".log", "r")
        # appending the file
        f = open(log_file_name + ".log", "a")
        f.write(table_content + "\n")
    # if file does not exist
    except:
        f = open(log_file_name + ".log", "a")
        f.write( table_header+ "\n" + table_content + "\n")
    f.close()

# Common log file to comparing all models in batch in separate folder
model_checker_logger("\\families\\family_checker_"+ datestamp[0:10])