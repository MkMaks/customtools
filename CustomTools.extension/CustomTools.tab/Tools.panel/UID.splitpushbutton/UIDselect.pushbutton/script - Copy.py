'''
selects object with entered Unique IDs.
'''

from pyrevit import revit
from System.Windows.Forms import Clipboard

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory


import clr
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import ElementId
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
clr.AddReference("System")
from System.Collections.Generic import List

doc = DocumentManager.Instance.CurrentDBDocument

guids = []
guids.append('22bd1dbb-ee41-43d1-8eb3-139348a126f0-00000ae3')

if not isinstance(guids, list):
	guids = [guids]
	
elems = []

for g in guids:
	hexid = g[37:]
	id = int(hexid, 16)
	# elem = doc.GetElement(ElementId(id));
	elem = ElementId(id)
	elems.append(elem)


uiapp = DocumentManager.Instance.CurrentUIApplication

ids = elems

# if it's not a list, make it a list
if not isinstance(ids, list):
	ids = [ids]

# convert to element ids
elemIds = []
for id in ids:
    elemIds.append(ElementId(id))
    

# cast to icollection and select
uiapp.ActiveUIDocument.Selection.SetElementIds(List[ElementId](elemIds));