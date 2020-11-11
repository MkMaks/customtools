# -*- coding: UTF-8 -*-
__doc__ = 'Places selected opened View or Schedule on active Sheet. ' \
          'Activate sheet first.'
__title__ = 'Place View On Sheet'
__helpurl__ = 'https://youtu.be/_DVTvM8VVAw'


from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction, XYZ, Viewport, ScheduleSheetInstance
from pyrevit import revit, DB, coreutils, forms, script


doc = __revit__.ActiveUIDocument.Document
selection = revit.get_selection()


selectedSheet = revit.active_view
loc = XYZ(0,0,0)


def placingSchedule(selectedSheet):
    if str(selectedSheet.ViewType) == "DrawingSheet":
        selectedSheetId = selectedSheet.Id
        curview = doc.ActiveView
        try:
	        if str(curview.ViewType) == "Schedule":
	            t = Transaction(doc, "Place schedule on active Sheet")
	            t.Start()
	            ScheduleSheetInstance.Create(doc, selectedSheetId, curview.Id, loc)
	            t.Commit()
	        else:
	            t = Transaction(doc, "Place view on active Sheet")
	            t.Start()
	            Viewport.Create(doc, selectedSheetId, curview.Id, loc)
	            t.Commit()
        except:
        	# if view is already on the sheet
            viewports_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Viewports) \
            	.WhereElementIsNotElementType().ToElements()

            output = script.get_output()
            md_schedule = "| Number | Sheet Name | Owner Sheet |\n| ----------- | ----------- | ----------- |"  
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
            if count > 0:
                output.print_md("# ACTIVE VIEW IS ALREADY ON THIS VIEW")
                output.print_md(md_schedule)
    else:
        print("Activate sheet at first.")


with forms.WarningBar(title='Vyber element vo View:'):
    selection = revit.pick_element()
# print selection

placingSchedule(selectedSheet)