'''
Places selected opened View or Schedule on active Sheet.
'''

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction, XYZ, Viewport, ScheduleSheetInstance
from pyrevit import revit, DB, coreutils, forms
# from pyrevit import revit, coreutils, forms


doc = __revit__.ActiveUIDocument.Document
selection = revit.get_selection()


selectedSheet = revit.active_view
loc = XYZ(0,0,0)


def placingSchedule(selectedSheet):
	if str(selectedSheet.ViewType) == "DrawingSheet":
		selectedSheetId = selectedSheet.Id
		curview = revit.active_view
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
	else:
		print("Activate sheet at first.")


with forms.WarningBar(title='Vyber element vo View:'):
    selection = revit.pick_element()
# print selection

placingSchedule(selectedSheet)