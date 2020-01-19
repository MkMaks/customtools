'''
deletes active view
'''

from Autodesk.Revit.DB import Transaction, Viewport, ElementId
from pyrevit import revit, DB, coreutils, forms
# from pyrevit import revit, coreutils, forms


doc = __revit__.ActiveUIDocument.Document
curview = revit.activeview

with forms.WarningBar(title='Prepni na iny View:'):
    a = revit.pick_element()

t = Transaction(doc, "Deleting active View")
t.Start()
# try:
doc.Delete(curview.Id)
# doc.Delete(ElementId(1589))
# except:
# 	print("error")

t.Commit()
