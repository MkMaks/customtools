'''
Check whether placeable elements aren't on the same place and selects those which are redundant.
Element is considered as redundant if at least one of its coordinates differs at most 200mm.
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

# /////// FUNCTIONS /////////
#converts milimeters to feets
def mm2feet(a):
	b = a*0.00328084
	return b

#prepares point for difference calculation - first with first, second with second
def listCompare(a,b):
	zipList = zip(a,b)
	deltaList = []
	for i in zipList:
		delta = abs(i[0]-i[1])
		deltaList.append(delta)
	return deltaList

#chcecks whether difference is smaller than set limit
def deltaCheck(a):
	sumList = []
	for i in a:
		if i<=mm2feet(200):
			#id smaller than limit
			sumList.append(1)
	# at most two identical coordinates within limits
	if len(sumList) > 2:
		return 1
	else:
		return 0

#converting string to list
def toList(stringlist):
	splitList = stringlist.split(",")
	returnedList=[]
	for i in splitList:
		returnedList.append(float(i))
	return returnedList

# getting coordinates for each of selected elements
for element in element_collector:
	location = element.Location
	locPoint = location.Point.ToString()
	#removing brackets
	locPointlist = locPoint[1:-1]
	locPointlist = toList(locPointlist)
	for i in locList:
		redundant = deltaCheck(listCompare(locPointlist,i))
		if redundant == 1:
			redundantList.append(element.Id)
	locList.append(locPointlist)

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

