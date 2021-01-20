# -*- coding: UTF-8 -*-
__author__ = 'David Vadkerti'
__doc__ = 'Creates schedule with links to owner sheets for active view.'
__helpurl__ = 'https://youtu.be/bdR_gaLdbW0'

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Viewport
from pyrevit import revit, DB, coreutils, forms, script
from customOutput import ct_icon


doc = __revit__.ActiveUIDocument.Document
curview = revit.active_view

output = script.get_output()
# changing icon
ct_icon(output)

output.print_md("# OWNER SHEET FOR ACTIVE VIEW")
md_schedule = "| Number | Sheet Name | Owner Sheet |\n| ----------- | ----------- | ----------- |"  

viewports_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Viewports) \
.WhereElementIsNotElementType().ToElements()

# views not on sheets
viewsOnSheet = []
count = 0
for viewport in viewports_collector:
    view_id = viewport.ViewId
    if curview.Id == view_id:
        count += 1
        sheet_id = viewport.SheetId
        sheetName = doc.GetElement(sheet_id).Name
        newScheduleLine = " \n| "+str(count)+" | "+sheetName+" | "+output.linkify(sheet_id)+" |"
        md_schedule += newScheduleLine

    # viewsOnSheet.append(view_id)
    # sheets.append(sheet_id)
if count == 0:
    print("Active sheet is not on any Sheet.")
else:
    output.print_md(md_schedule)