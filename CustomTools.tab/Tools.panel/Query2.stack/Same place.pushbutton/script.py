# -*- coding: utf-8 -*-
__title__ = 'Same place'
__doc__ = """Check whether elements aren't on the same place ± tolerance and selects those which are redundant.
Element is considered as redundant if at least one of its coordinates differs more than set tolerance.

You can change system families in Groups for running the scripts as Groups are valid elements."""

from pyrevit import revit, DB, forms
from Autodesk.Revit.DB import ElementId, Transaction
from System.Collections.Generic import List
from Autodesk.Revit.UI import UIApplication

# change context for proper category - check in revit for category
__context__ = 'Selection'

curview = revit.active_view
element_collector = revit.get_selection()
doc = __revit__.ActiveUIDocument.Document
uiapp = UIApplication(doc.Application)

locList = []
redundantList = []

# /////// UI WINDOW /////////
class getToleranceWindow(forms.WPFWindow):
    def __init__(self, xaml_file_name):
        forms.WPFWindow.__init__(self, xaml_file_name)

    def process_text(self, sender, args):
        self.Close()
        tolerance =  float(self.sheets_tb.Text)

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
	def deltaCheck(a, tolerance):
		sumList = []
		for i in a:
			if i<=mm2feet(tolerance):
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
	t = Transaction(doc, "Same Place")
	t.Start()
	for element in element_collector:
		try:
			# for loadable families
			location = element.Location
			locPoint = location.Point.ToString()
			# locPoint = location.ToString()
			#removing brackets
			locPointlist = locPoint[1:-1]
			locPointlist = toList(locPointlist)
			for i in locList:
				redundant = deltaCheck(listCompare(locPointlist,i), tolerance)
				if redundant == 1:
					redundantList.append(element.Id)
			locList.append(locPointlist)
		except:
			# for system families there is need to make groups
			elid = []
			elid.append(element.Id)
			iCol = List[ElementId](elid)

			group=doc.Create.NewGroup(iCol)

			location = group.Location
			locPoint = location.Point.ToString()
			locPointlist = locPoint[1:-1]
			locPointlist = toList(locPointlist)
			for i in locList:
				redundant = deltaCheck(listCompare(locPointlist,i), tolerance)
				if redundant == 1:
					redundantList.append(element.Id)
			locList.append(locPointlist)

			group.UngroupMembers()

	t.Commit()


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

getToleranceWindow('getToleranceWindow.xaml').ShowDialog()