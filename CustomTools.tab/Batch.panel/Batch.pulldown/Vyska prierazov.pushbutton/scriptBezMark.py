'''
Sets distance of Sill Height of Windows from Project zero to parameter "SH prierazu".
Sets Level number to parameter "Poschodie" to Windows and Generic Models
Sets Level elevation to parameter "ref od 0" to Windows.

Only Windows and Generic Models with Type Comments == "stavebne upravy" are processed.
'''
# for timing------
from pyrevit.coreutils import Timer
from pyrevit import coreutils
timer = Timer()
# ----------------

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, \
				Transaction, Document, BuiltInParameter
from pyrevit import revit, DB

__title__ = 'Automaticka\nvyska prierazov'

doc = __revit__.ActiveUIDocument.Document

# /////// COLLECTORS /////////
# collecting windows
windows_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows) \
	.WhereElementIsNotElementType() \
	.ToElements()

# collecting generic models
genericModel_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel) \
	.WhereElementIsNotElementType() \
	.ToElements()

# /////// FUNCTIONS /////////
#converts milimeters to feets
def mm2feet(a):
	b = a*0.00328084
	return b

#converts feets to milimeters
def feet2mm(a):
	b = a/0.00328084
	return b

# highlights text using html string with css
def text_highligter(a):
		content = str(a)
		html_code = "<p class='elementlink'>"+content+"</p>"
		return coreutils.prepare_html_str(html_code)

# error handling
def skipped(element,parameterName):
	notprocessed.append(element.Id.IntegerValue)
	parameter = element.LookupParameter(parameterName)
	if parameter:
		parameter.Set("no data")

# level number extraction
def levelNameExtraction(levelName):
	# searching for dot in name of level
	try:
		index = levelName.index(".")
		levelNumber = levelName[0:index]
	# when there is no dot in name returns frist 2 characters
	except:
		levelNumber = levelName[0:2]
	return levelNumber

# adding 0 to one digit numbers in level names
def zeros(levelNumber):
	try:
		# positive numbers
		if int(levelNumber) < 10 and int(levelNumber) >= 0:
			levelNumberSet = "0" + levelNumber
		# negative numbers
		else:
			levelNumberSet = levelNumber
	# strings - non numbers
	except:
		levelNumberSet = levelNumber
	return levelNumberSet

def poschodieSetter(element,levelElement):
	elementTypeId = element.GetTypeId()
	elementType = Document.GetElement(doc,elementTypeId)
	# filtering elements
	filterp = elementType.LookupParameter('Type Comments')
	if filterp and filterp.AsString() == "stavebne upravy":	
		try:
			# setting parameters
			levelName = levelElement.LookupParameter('Name').AsString()
			# getting Number string from Level Name
			levelNumber = levelNameExtraction(levelName)
			# adding 0 to one digit numbers
			levelNumberSet = zeros(levelNumber)
			# setting parameter "Poschodie"
			levelNameP = element.LookupParameter("Poschodie")
			if levelNameP:
					levelNameP.Set(levelNumberSet)
			else:
				skipped(element,"Poschodie")
		except:
			skipped(element,"Poschodie")

# getting levels from generic models and other elements
def GetLevel(item):
	#if hasattr(item, "LevelId"): return item.Document.GetElement(item.LevelId)
	if hasattr(item, "Level"): return item.Level
	elif hasattr(item, "GenLevel"): return item.GenLevel
	else:
		try: return item.Document.GetElement(item.get_Parameter(BuiltInParameter.INSTANCE_REFERENCE_LEVEL_PARAM).AsElementId())
		except: 
			try: return item.Document.GetElement(item.get_Parameter(BuiltInParameter.INSTANCE_SCHEDULE_ONLY_LEVEL_PARAM).AsElementId())
			except: pass

t = Transaction(doc, "Automaticka vyska prierazov")
t.Start()

notprocessed = []
# creating lists - just for debugging
# sill_height_values_list=[]
# sill_height_values_list=[]
# level_ids_list=[]
# level_elevation_list=[]
# sill_height_zeroMM_list=[]
# offset_shared_values_list=[]

# creating lists - just for debugging
# level_ids_list=[]
# level_name_list=[]
# indexlist=[]

# /////// WINDOW SILL HEIGHT /////////
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
				sill_height_value = sillHeightFt.AsDouble()
				# sill_height_values_list.append(feet2mm(sill_height_value))

			except:
				# nonhosted elements with Offset Shared
				# geting Offset Shared from windows
				OffsetSharedFt = window.LookupParameter('Offset Shared')
				offset_shared_value = OffsetSharedFt.AsDouble()
				# offset_shared_values_list.append(feet2mm(offset_shared_value))

			# geting levels from windows
			level = window.LevelId
			# level_ids_list.append(level)

			# getting elevation of levels from project zero +0.000
			level_element = Document.GetElement(doc,level)
			level_elevation = level_element.Elevation
			# level_elevation_list.append(feet2mm(level_elevation))

			# write Level Height Values to "ref od 0" parameter of windows
			level_height_param = window.LookupParameter('ref od 0')
			if level_height_param:
					level_height_param.Set(level_elevation)

			# add Level Height Values to Sill Height Values of windows
			try:
				sill_height_zero = level_elevation + sill_height_value
				# sill_height_zeroMM = round(feet2mm(sill_height_zero))
				# sill_height_zeroMM_list.append(sill_height_zeroMM)
			except:
				sill_height_zero = level_elevation + offset_shared_value

			# writing "SH prierazu" parameters
			custom_param = window.LookupParameter('SH prierazu')
			if custom_param:
				custom_param.Set(sill_height_zero)

		except:
			# notprocessed.append(window.Id.IntegerValue)
			# custom_param = window.LookupParameter('SH prierazu')
			skipped(window,'SH prierazu')

# /////// POSCHODIE PARAMETER ASIGNMENT /////////
for window in windows_collector:
	try:
		level = window.LevelId
		levelElement = Document.GetElement(doc,level)
		# setting parameters
		poschodieSetter(window,levelElement)
	except:
		skipped(window,"Poschodie")

for element in genericModel_collector:
		try:
			levelElement = GetLevel(element)
			# setting parameters
			poschodieSetter(element,levelElement)
		except:
			skipped(element,"Poschodie")

# /////// UNIQUE MARK PARAMETER ASIGNMENT /////////
for window in windows_collector:
	# try:
		width_param = window.LookupParameter('Width').AsString()
		height_param = window.LookupParameter('Height')
		mark_param = window.LookupParameter('Mark')
		# mark_param.Set("processed")
		mark_param.Set(width_param)
	# except:
	# 	mark_param.Set("not processed")

t.Commit()

# just for debuging window sill height
# print("control lists for debugging")
# print(sill_height_values_list)
# print(level_ids_list)
# print(level_elevation_list)
# print(sill_height_zeroMM_list)
# print(offset_shared_values_list)

# debuging poschodie
# print(level_name_list)
# print(indexlist)

# Final Claims
countOfSkippedElms = str(len(notprocessed)) +" elements were skipped"
print(text_highligter(countOfSkippedElms))
print("Ids of skipped elements:")
print(notprocessed)

# for timing------
endtime = timer.get_time()
endtimeRound = round(endtime*1000)/1000
print("\nTime "+str(endtimeRound)+" seconds.")
# --------------