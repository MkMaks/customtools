from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction, Document
doc = __revit__.ActiveUIDocument.Document

# collecting windows
windows_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows) \
	.WhereElementIsNotElementType() \
	.ToElements()

# geting levels from windows
level_ids_list=[]
for window in windows_collector:
		level = window.LevelId
		#level = window.LevelId.ToString()
		level_ids_list.append(level)
print(level_ids_list)

# getting elevation of levels from project zero +0.000
level_elevation_list=[]
for i in level_ids_list:
	level_element = Document.GetElement(doc,i)
	level_elevation = level_element.Elevation
	level_elevation_list.append(level_elevation)
print(level_elevation_list)

