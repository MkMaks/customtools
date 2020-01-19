import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction
doc = __revit__.ActiveUIDocument.Document

# collecting generic models
genericModel_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel) \
	.WhereElementIsNotElementType() \
	.ToElements()

# geting levels from windows
level_ids_list=[]
level_name_list=[]
indexlist=[]
hostlist=[]

t = Transaction(doc, "Automaticka vyska prierazov")
t.Start()

skipped_items=[]
# function to treat generic models and windows by same code
for element in genericModel_collector:
		
		# level = element.LevelId
		# level_ids_list.append(level)
		# levelElement = Document.GetElement(doc,level)

		# levelName = levelElement.LookupParameter('Name').AsString()
		# levelName = levelElement.LookupParameter('Name').AsString()
		# host = element.LookupParameter('Host').AsString()

		level_param_id = DB.ElementId(DB.BuiltInParameter.SCHEDULE_LEVEL_PARAM)
		level_param_prov = DB.ParameterValueProvider(level_param_id).GetElementIdValue
		# host = element.LookupParameter('Host')
		print(level_param_prov)
		# hostlist.append(level_param_prov)

		# # index = levelName.index(".")
		# levelNumber = levelName[0:index]
		# indexlist.append(levelNumber)
		# levelNameP = element.LookupParameter("Poschodie")
		# level_name_list.append(levelName)
		# if levelNameP:
		# 	levelNameP.Set(levelNumber)

t.Commit()
				
print(level_ids_list)
print(level_name_list)
print(indexlist)
print(skipped_items)
print(hostlist)

