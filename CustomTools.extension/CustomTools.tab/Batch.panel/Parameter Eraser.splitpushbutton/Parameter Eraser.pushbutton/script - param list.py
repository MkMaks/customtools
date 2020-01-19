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

typeParamList=['Type Comments','Model','Manufacturer','URL','Description','Type Mark','Fire Rating']
roomParamList=['Name','Number','Base Finish','Wall Finish','Floor Finish','Ceiling Finish','Department','Occupancy']
instParamList=['Comments','Mark']

def ParamEraser(el,paramList):
		for paramname in paramList:
			filterp = el.LookupParameter(paramname)
			if filterp:
				filterp.Set("")			

t= Transaction(doc, "Full Parameter Value Eraser")
t.Start()

for element in element_collector:
	try:
		ParamEraser(element,instParamList)
	except:
		pass

for type in type_collector:
	try:
		ParamEraser(type,typeParamList)
	except:
		pass

for room in room_collector:
	try:
		ParamEraser(room,roomParamList)
	except:
		pass

t.Commit()

# for timing------
endtime = timer.get_time()
print(endtime)
# ----------------