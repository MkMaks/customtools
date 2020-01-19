'''
Deletes all Views, Sheets and windows in Project
'''
# for timing------
from pyrevit.coreutils import Timer
timer = Timer()
# ----------------

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction, Document
from pyrevit import revit, DB

__title__ = 'Automaticka\nvyska prierazov'

doc = __revit__.ActiveUIDocument.Document

windows_id_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows) \
	.WhereElementIsNotElementType() \
	.ToElementIds()

# collecting windows
windows_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows) \
	.WhereElementIsNotElementType() \
	.ToElements()

def mm2feet(a):
	b = a*0.00328084
	return b

def feet2mm(a):
	b = a/0.00328084
	return b

t = Transaction(doc, "Automaticka vyska prierazov")
t.Start()

# creating lists
sill_height_values_list=[]
level_ids_list=[]
sill_height_zero_values = []
level_elevation_list=[]

def sill_height_zero_values(level_ids_list,sill_height_values_list):
	# getting elevation of levels from project zero +0.000
	for i in level_ids_list:
		try:
			level_element = Document.GetElement(doc,i)
			level_elevation = level_element.Elevation
			level_elevation_list.append(level_elevation)
		except:
			pass

	# add Level Height Values to Sill Height Values of windows
	c = [a+b for a,b in zip(level_elevation_list,sill_height_values_list)]

	for i in c:
		sillHeightZero = feet2mm(i)
		sill_height_zero_values.append(round(sillHeightZero))

# getting window parameters
for window in windows_collector:
	try:
		# geting Sill Height from windows
		sillHeightFt = window.LookupParameter('Sill Height')
		# sillHeightMM = feet2mm(sillHeightFt.AsDouble())
		# sill_height_values_list.append(round(sillHeightMM))
		sill_height_values_list.append(round(sillHeightFt.AsDouble()))

		# geting levels from windows
		level = window.LevelId
		level_ids_list.append(level)

		# SH prierazu setter
		# custom_param2 = window.LookupParameter('Sill Height')
		custom_param = window.LookupParameter('SH prierazu')
		sill_height_zero_values(level_ids_list,sill_height_values_list)
		if custom_param:
			# custom_param.Set(0)
			custom_param.Set(custom_param2.AsDouble())
	except:
		pass

t.Commit()



print(sill_height_values_list)
# print(level_ids_list)
print(level_elevation_list)
print(sill_height_zero_values)

# for timing------
endtime = timer.get_time()
print(endtime)
# --------------