'''
Erases most common Instance and Type parameters values.
'''
# for timing------
from pyrevit.coreutils import Timer
timer = Timer()
# ----------------

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction

__title__ = 'Full Parameter\nValue Eraser'

# uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

#Creating collector category
element_collector = FilteredElementCollector(doc).WhereElementIsNotElementType()
type_collector = FilteredElementCollector(doc).WhereElementIsElementType()
room_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType()

def ParamEraser(el,paramname):
		filterp = el.LookupParameter(paramname)
		if filterp:
			filterp.Set("")

t= Transaction(doc, "Full Parameter Value Eraser")
t.Start()

for element in element_collector:
	try:
		ParamEraser(element,'Comments')
		ParamEraser(element,'Mark')
	except:
		pass

for type in type_collector:
	try:
		ParamEraser(type,'Type Comments')
		ParamEraser(type,'Model')
		ParamEraser(type,'Manufacturer')
		ParamEraser(type,'URL')
		ParamEraser(type,'Description')
		ParamEraser(type,'Type Mark')
		ParamEraser(type,'Fire Rating')
	except:
		pass

for room in room_collector:
	try:
		ParamEraser(room,'Name')
		ParamEraser(room,'Number')
		ParamEraser(room,'Base Finish')
		ParamEraser(room,'Wall Finish')
		ParamEraser(room,'Floor Finish')
		ParamEraser(room,'Ceiling Finish')
		ParamEraser(room,'Department')
		ParamEraser(room,'Occupancy')
	except:
		pass

t.Commit()

# for timing------
endtime = timer.get_time()
print(endtime)
# ----------------