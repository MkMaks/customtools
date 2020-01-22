# -*- coding: utf-8 -*-
__title__ = 'UID select'
__doc__ = """selects object with entered Unique IDs. Separate Unique IDs by comma."""


from pyrevit import revit, DB, forms
from Autodesk.Revit.DB import ElementId
from System.Collections.Generic import List
from Autodesk.Revit.UI import UIApplication

selection = revit.get_selection()
doc = __revit__.ActiveUIDocument.Document
uiapp = UIApplication(doc.Application)

class UIDselectWindow(forms.WPFWindow):
    def __init__(self, xaml_file_name):
        forms.WPFWindow.__init__(self, xaml_file_name)

    def process_text(self, sender, args):
        self.Close()
        uidString =  str(self.sheets_tb.Text)
        guids = uidString.split(",")


	try:
		if not isinstance(guids, list):
			guids = [guids]
			
		elems = []

		for g in guids:
			# treating spaces in list after comma
			spaceLessG=""
			for i in g:
				if i!=" ":
					spaceLessG=spaceLessG+i
				else:
					pass
			hexid = spaceLessG[37:]
			id = int(hexid, 16)
			elem = ElementId(id)
			elems.append(elem)

		# cast to icollection and select
		uiapp.ActiveUIDocument.Selection.SetElementIds(List[ElementId](elems));
	except:
		print("Unique ID not found.")
		print("You need to use UID getter tool at first.")

UIDselectWindow('UIDselectWindow.xaml').ShowDialog()