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

# function for gettin levels from generic models and other elements
def GetLevel(item):
	#if hasattr(item, "LevelId"): return item.Document.GetElement(item.LevelId)
	if hasattr(item, "Level"): return item.Level
	elif hasattr(item, "GenLevel"): return item.GenLevel
	else:
		try: return item.Document.GetElement(item.get_Parameter(BuiltInParameter.INSTANCE_REFERENCE_LEVEL_PARAM).AsElementId())
		except: 
			try: return item.Document.GetElement(item.get_Parameter(BuiltInParameter.INSTANCE_SCHEDULE_ONLY_LEVEL_PARAM).AsElementId())
			except: pass

for element in windows_collector:
		
		try:
			level = element.LevelId
			#level_ids_list.append(level)
			levelElement = Document.GetElement(doc,level)
			# levelName = levelElement.LookupParameter('Name').AsString()
			levelName = levelElement.LookupParameter('Name').AsString()

			index = levelName.index(".")
			levelNumber = levelName[0:index]
			#indexlist.append(levelNumber)
			levelNameP = element.LookupParameter("Poschodie")
			#level_name_list.append(levelName)
			if levelNameP:
				levelNameP.Set(levelNumber)
		except:
			skipped_items.append(element.Id.IntegerValue)

for element in genericModel_collector:
	try:
		#if GetLevel(element) != None:
		levelElement = GetLevel(element)
		levelName = levelElement.LookupParameter('Name').AsString()
		level_name_list.append(levelName)

		index = levelName.index(".")
		levelNumber = levelName[0:index]
		indexlist.append(levelNumber)
		levelNameP = element.LookupParameter("Poschodie")
		if levelNameP:
				levelNameP.Set(levelNumber)
			
		else:
			if levelNameP:
				levelNameP.Set("no level data")
	except:
		skipped_items.append(element.Id.IntegerValue)

t.Commit()
				
print(level_ids_list)
print(level_name_list)
print(indexlist)
print(skipped_items)

