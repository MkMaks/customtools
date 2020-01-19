# -*- coding: UTF-8 -*-
"""Lists all Not Placed Views.

"""

__title__ = 'Not Placed Views schedule'
__author__ = 'David Vadkerti'
__doc__ = 'Lists all Not Placed Views'

import clr
from collections import defaultdict

from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms
from pyrevit import output

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
from Autodesk.Revit.DB import Family, View

from pyrevit.coreutils import Timer
from custom_output import hmsTimer

doc = __revit__.ActiveUIDocument.Document
timer = Timer()

output = script.get_output()

output.print_md("# NOT PLACED VIEW SCHEDULE")

md_schedule = "| Number | View Name | View ID | Author | View Type |\n| ----------- | ----------- | ----------- | ----------- | ----------- |"


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


workset_table = revit.doc.GetWorksetTable()
views = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()

count = 0
for view in views:
    if view.Id not in viewsOnSheet: 
        viewType = str(view.ViewType)
        # https://www.revitapidocs.com/2020/bf04dabc-05a3-baf0-3564-f96c0bde3400.htm
        viewName = view.Name
        if viewType != "DrawingSheet" and viewType != "Schedule":
            count += 1
            view_id = view.Id
            # viewType = view.GetType().Name
            view_creator = DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc,view_id).Creator 
            newScheduleLine = " \n| "+str(count)+" | "+viewName+" | "+output.linkify(view_id)+" | " + str(view) + " | "+ viewType + " |"
            md_schedule += newScheduleLine

# print md_schedule
output.print_md(md_schedule)

# for timing------
endtime = timer.get_time()
print(hmsTimer(endtime))