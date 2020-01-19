'''
Sets distance of Sill Height from Project zero to SH prierazu parameter.
'''
# for timing------
from pyrevit.coreutils import Timer
timer = Timer()
# ----------------

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction, Document
from pyrevit import revit, DB

__title__ = 'Automaticka\nvyska prierazov'

doc = __revit__.ActiveUIDocument.Document

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

notprocessed = []
# creating lists - just for debugging
sill_height_values_list=[]
sill_height_values_list=[]
level_ids_list=[]
level_elevation_list=[]
sill_height_zeroMM_list=[]
offset_shared_values_list=[]

# getting window parameters
for window in windows_collector:
	# filter by Type Comments == stavebne upravy
	elementTypeId = window.GetTypeId()
	elementType = Document.GetElement(doc,elementTypeId)
	filterp = elementType.LookupParameter('Type Comments')

	if filterp and filterp.AsString() == "stavebne upravy":
		try:
			try:
				# hosted elements with Sill Height
				# geting Sill Height from windows
				sillHeightFt = window.LookupParameter('Sill Height')
				# sillHeightMM = feet2mm(sillHeightFt.AsDouble())
				# sill_height_values_list.append(round(sillHeightMM))
				# sill_height_values_list.append(round(sillHeightFt.AsDouble()))
				sill_height_value = sillHeightFt.AsDouble()
				sill_height_values_list.append(feet2mm(sill_height_value))

			except:
				# nonhosted elements with Offset Shared
				# geting Offset Shared from windows
				OffsetSharedFt = window.LookupParameter('Offset Shared')
				offset_shared_value = OffsetSharedFt.AsDouble()
				offset_shared_values_list.append(feet2mm(offset_shared_value))

			# geting levels from windows
			level = window.LevelId
			level_ids_list.append(level)

			# getting elevation of levels from project zero +0.000
			level_element = Document.GetElement(doc,level)
			level_elevation = level_element.Elevation
			level_elevation_list.append(feet2mm(level_elevation))

			# add Level Height Values to Sill Height Values of windows
			try:
				sill_height_zero = level_elevation + sill_height_value
				sill_height_zeroMM = round(feet2mm(sill_height_zero))
				sill_height_zeroMM_list.append(sill_height_zeroMM)
			except:
				sill_height_zero = level_elevation + offset_shared_value

			# changing parameters
			# custom_param2 = window.LookupParameter('Sill Height')
			custom_param = window.LookupParameter('SH prierazu')
			if custom_param:
				custom_param.Set(sill_height_zero)

		except:
			notprocessed.append(window.Id.IntegerValue)

t.Commit()



# just for debuging
# print("control lists for debugging")
# print(sill_height_values_list)
# print(level_ids_list)
# print(level_elevation_list)
# print(sill_height_zeroMM_list)
# print(offset_shared_values_list)

# Final Claim
print("Ids of skipped elements:")
print(notprocessed)

# for timing------
endtime = timer.get_time()
endtimeRound = round(endtime*1000)/1000
print("\nTime "+str(endtimeRound)+" seconds")
# --------------