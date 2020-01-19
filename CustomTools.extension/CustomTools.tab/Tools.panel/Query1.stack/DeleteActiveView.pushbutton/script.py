# -*- coding: UTF-8 -*-
'''
deletes active view
'''

from Autodesk.Revit.DB import Transaction, Viewport, ElementId
from pyrevit import revit, DB, coreutils, forms
# from pyrevit import revit, coreutils, forms
# from Autodesk.Revit.UI import UIView

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
curview = revit.active_view

ui_viewCount = 0
for ui_view in uidoc.GetOpenUIViews():
	ui_viewCount += 1

# dialogue box only when just one view active
if ui_viewCount == 1:
	res = forms.alert("Revit nemôže vymazať posledný otvorený View.\n\nOtvorte prosím aspoň jedno ďalšie okno.\n",
                  exitscript=True)
else:
	res = True

if res:
	for ui_view in uidoc.GetOpenUIViews():
	    if ui_view.ViewId == curview.Id:
	        ui_view.Close()

	t = Transaction(doc, "Deleting active View")
	t.Start()

	doc.Delete(curview.Id)

	t.Commit()
