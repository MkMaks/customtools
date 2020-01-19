from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction
doc = __revit__.ActiveUIDocument.Document

# collecting windows
windows_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows) \
	.WhereElementIsNotElementType() \
	.ToElements()

# collecting generic models
genericModel_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel) \
	.WhereElementIsNotElementType() \
	.ToElements()

# geting levels from windows
level_ids_list=[]
level_name_list=[]
indexlist=[]

t = Transaction(doc, "Automaticka vyska prierazov")
t.Start()

skipped_items=[]
# function to treat generic models and windows by same code
def levelNamePSetter(collector):
	for element in collector:
		
		try:
			level = element.LevelId
			level_ids_list.append(level)
			levelElement = Document.GetElement(doc,level)
			levelName = levelElement.LookupParameter('Name').AsString()

			index = levelName.index(".")
			levelNumber = levelName[0:index]
			indexlist.append(levelNumber)
			levelNameP = element.LookupParameter("Poschodie")
			level_name_list.append(levelName)
			if levelNameP:
				levelNameP.Set(levelNumber)
		except:
			skipped_items.append(element.Id.IntegerValue)
#levelNamePSetter(windows_collector)
levelNamePSetter(genericModel_collector)

t.Commit()
				
print(level_ids_list)
print(level_name_list)
print(indexlist)
print(skipped_items)

