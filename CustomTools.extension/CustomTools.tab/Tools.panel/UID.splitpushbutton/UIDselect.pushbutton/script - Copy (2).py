'''
selects object with entered Unique IDs. You need to select text which has Unique ID string pasted as its content.
'''
__context__ = 'Text Notes'

from pyrevit import revit, DB
from Autodesk.Revit.DB import ElementId
from System.Collections.Generic import List
from Autodesk.Revit.UI import UIApplication

selection = revit.get_selection()
doc = __revit__.ActiveUIDocument.Document
uiapp = UIApplication(doc.Application)

guids = []
try:
	for el in selection.elements:
		guids.append(el.Text)

	if not isinstance(guids, list):
		guids = [guids]
		
	elems = []

	for g in guids:
		hexid = g[37:]
		id = int(hexid, 16)
		elem = ElementId(id)
		elems.append(elem)

	# cast to icollection and select
	uiapp.ActiveUIDocument.Selection.SetElementIds(List[ElementId](elems));
except:
	print("Unique ID not found.")
	print("You need to select text which has Unique ID string pasted as its content.")