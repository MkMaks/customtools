'''
places active view on sheet. Select TitleBlock of Sheet and open view
'''

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction, XYZ, Viewport
from pyrevit import revit, DB
from pyrevit import revit, coreutils


doc = __revit__.ActiveUIDocument.Document
curview = revit.activeview
selection = revit.get_selection()

for el in selection:
	selectedSheetId = el.OwnerViewId
	selectedSheet = doc.GetElement(selectedSheetId)
loc = XYZ(0,0,0)

t = Transaction(doc, "Place active view on selected Sheet")
t.Start()

try:		
	Viewport.Create(doc, selectedSheetId, curview.Id, loc)	
except:
	print("error")
t.Commit()