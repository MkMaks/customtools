'''
Check weather placeable elements aren't on the same place and selects those which are redundant.
'''

from pyrevit import revit, DB
from Autodesk.Revit.DB import ElementId
from System.Collections.Generic import List
from Autodesk.Revit.UI import UIApplication

# change context for proper category - check in revit for category
__context__ = 'Selection'

curview = revit.activeview
element_collector = revit.get_selection()
doc = __revit__.ActiveUIDocument.Document
uiapp = UIApplication(doc.Application)

locList = []
redundantList = []

# gettin coordinates for each of selected elements
for element in element_collector:
	location = element.Location
	locPoint = location.Point.ToString()
	# finding the same coordinates to identify 2 instances in same place
	if locPoint in locList:
		redundantList.append(element.Id)
	locList.append(locPoint)


# output window
redundantCount = len(redundantList)
if redundantCount > 0:
	# selecting elements
	try:
		uiapp.ActiveUIDocument.Selection.SetElementIds(List[ElementId](redundantList))
		print(str(redundantCount) + " redundant elements were found.\nAll elements were selected.")
	except:
		print("Error occured.")
else:
	print("No redundant elements were found.")

