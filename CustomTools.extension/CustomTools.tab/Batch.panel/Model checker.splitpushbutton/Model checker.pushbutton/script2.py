# -*- coding: UTF-8 -*-
"""Model Checker.
Revit file quality control.
"""

__title__ = 'Model\nChecker'
__doc__ = 'Revit file quality control'

from pyrevit import revit, DB
from pyrevit import forms
from pyrevit import script, coreutils
from pyrevit import output
import os.path as op
import math

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
from Autodesk.Revit.UI import UIApplication
from pyrevit.coreutils import Timer
from custom_output import hmsTimer
from Autodesk.Revit.DB import LinePatternElement, Family, TextNoteType, ScheduleSheetInstance, WorksetTable, TextNote, ReferencePlane

doc = __revit__.ActiveUIDocument.Document
uiapp = UIApplication(doc.Application)

timer = Timer()

wikiArticle = "Postupy, ktorým je potrebné sa vyhnúť - Revit"
# dashboard HTMl maker - rectangle with large number
def dashboardRectMaker(value,description,treshold,wikiArticle):
        content = str(value)
        if value <= treshold:
            html_code = "<a class='dashboardLink' title='OK - maximum value "+str(int(treshold))+"'><p class='dashboardRectNormal'>"+content+"<br><span class='dashboardSmall'>"+description+"</span>""</p>"
            return coreutils.prepare_html_str(html_code)
        elif value < treshold*2:
            html_code = "<a class='dashboardLink' href='https://gfi.miraheze.org/wiki/"+wikiArticle+"' title='Mediocre - goal value "+str(int(treshold)) \
            	+"'><p class='dashboardRectMediocre'>" + content + "<br><span class='dashboardSmall'>"+description+"</span>""</p></a>"
            return coreutils.prepare_html_str(html_code)
        else:
            html_code = "<a class='dashboardLink' href='https://gfi.miraheze.org/wiki/"+wikiArticle+"' title='Critical - goal value "+str(int(treshold)) \
                +"'><p class='dashboardRectCritical'>" + content + "<br><span class='dashboardSmall'>"+description+"</span>""</p></a>"
            return coreutils.prepare_html_str(html_code)


# dashboard HTMl maker - div for center aligning
def dashboardCenterMaker(value):
        content = str(value)
        html_code = "<div class='dashboardCenter'>"+content+"</div>"
        print(coreutils.prepare_html_str(html_code))

# returns file name - everything in path from "\" to the end
def nameFromPath(path):
	try:
		index = path.rindex("\\") + 1
	except:
		index = path.rindex("/") + 1		
	return path[index:]

# printing file name
name = doc.PathName
try:
	print(nameFromPath(name))
except:
	print(name)


output = script.get_output()

# first JS to avoid error in IE output window when at first run
try:
	chartOuputError = output.make_doughnut_chart()
	chartOuputError.data.labels = []
	set_E = chartOuputError.data.new_dataset('Not Standard')
	set_E.data = []
	set_E.backgroundColor = ["#fff"]
	chartOuputError.set_height(1)
	chartOuputError.draw()
except:
	pass

colors = ["#fff0e6","#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb",
            "#4d4d4d","#000000","#fff0f2","#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb","#e97800","#a6c844",
            "#4d4d4d","#fff0d9","#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb","#4d4d4d","#e97800","#a6c844",
            "#fff0e6","#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb","#4d4d4d","#fff0e6","#e97800","#a6c844",
            "#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb","#4d4d4d","#9988bb","#4d4d4d","#e97800","#a6c844",
            "#4d4d4d","#fff0d9","#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb","#4d4d4d","#e97800","#a6c844",
            "#4d4d4d","#fff0d9","#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb","#4d4d4d","#e97800","#a6c844",
            "#4d4d4d","#fff0d9","#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb","#4d4d4d","#e97800","#a6c844",
            "#4d4d4d","#fff0d9","#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb","#4d4d4d","#e97800","#a6c844",
            "#4d4d4d","#fff0d9","#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb","#4d4d4d","#e97800","#a6c844",]


# sheets
sheets_id_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets) \
.WhereElementIsNotElementType() \
.ToElementIds()
sheetCount = len(sheets_id_collector)
# print(str(sheetCount)+" Sheets")


# schedules
schedules_id_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Schedules) \
.WhereElementIsNotElementType() \
.ToElements()
scheduleCount = 0
for schedule in schedules_id_collector:
    if schedule.Name[:19] != "<Revision Schedule>":
        scheduleCount += 1
# print(str(scheduleCount)+" Schedules")


# views
views_id_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views) \
.WhereElementIsNotElementType()
view_elements = views_id_collector.ToElements()
viewCount = len(view_elements)

copiedView = 0
for view in view_elements:
    viewName = view.LookupParameter('View Name')
    try:
        viewNameString = viewName.AsString()
        # print(viewNameString)
        if viewNameString[-6:-2] == "Copy" or viewNameString[-4:] == "Copy" or viewNameString[:7] == "Section":
        # if viewNameString[:7] == "Section":
            copiedView += 1
    except:
        pass

sheets_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets) \
.WhereElementIsNotElementType().ToElements()

# views not on sheets
viewsOnSheet = []
# schedulesOnSheet = []
for sheet in sheets_collector:
    try:        
        # scheduleslist = list()
        for item in sheet.GetAllPlacedViews():
            if item not in viewsOnSheet:
                viewsOnSheet.append(item)
    except:
        pass
viewsNotOnSheet = viewCount-len(viewsOnSheet)

# schedules not on sheets
schedulesOnSheet = []
scheduleCollector1 = FilteredElementCollector(doc).OfClass(ScheduleSheetInstance).WhereElementIsNotElementType()
scheduleCollector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Schedules) \
.WhereElementIsNotElementType()
# there is need to iterate class and category fitler to get all schedule
# it is something with schedules on more sheets maybe...
for schedule in scheduleCollector:
    schedName = schedule.Name
    if schedName[:19] != "<Revision Schedule>":
        if schedName not in schedulesOnSheet:
            if schedule.OwnerViewId.IntegerValue != -1:
                # print schedName
                # print schedule.Id
                schedulesOnSheet.append(schedName)

# there is need to iterate class and category fitler to get all schedule - UnionWith didn't work
for schedule in scheduleCollector1:
    schedName = schedule.Name
    if schedName[:19] != "<Revision Schedule>":
        if schedName not in schedulesOnSheet:
            if schedule.OwnerViewId.IntegerValue != -1:
                # print schedName
                # print schedule.Id
                schedulesOnSheet.append(schedName)
scheduleNotOnSheet = scheduleCount-len(schedulesOnSheet)

# tresholds
viewTres = 500
viewNotOnSheetTres = viewCount*0.2
copiedViewTres = viewCount*0.2
sheetsTres = 500
scheduleTres = 500
schedulesNotOnSheetTres = scheduleCount*0.3
# scheduleNotOnSheetTres = scheduleCount*0.3

htmlRow1 = (dashboardRectMaker(viewCount,"Views",viewTres,wikiArticle) + dashboardRectMaker(copiedView,"Copied Views",copiedViewTres,wikiArticle) + dashboardRectMaker(sheetCount,"Sheets",sheetsTres,wikiArticle)
 + dashboardRectMaker(scheduleCount,"Schedules",scheduleTres,wikiArticle) + dashboardRectMaker(viewsNotOnSheet,"Views not on Sheet",viewNotOnSheetTres,wikiArticle) 
 + dashboardRectMaker(scheduleNotOnSheet,"Schedules not on Sheet",schedulesNotOnSheetTres,wikiArticle))
dashboardCenterMaker(htmlRow1)

# CHART VIEWS OUTPUT
output = script.get_output()

badColor = "#e97800"
goodColor = "#a6c844"

chartCopiedViews = output.make_doughnut_chart()
chartCopiedViews.data.labels = ["Views with name ending 'Copy #' or or starts with 'Section'","Other Views"]
set_a = chartCopiedViews.data.new_dataset('Not Standard')
set_a.data = [copiedView,viewCount-copiedView]

set_a.backgroundColor = [badColor,goodColor]
chartCopiedViews.set_height(80)

chartCopiedViews.draw()

# warnings
allWarnings_collector = doc.GetWarnings()
allWarningsCount = len(allWarnings_collector)
# print(str(allWarningsCount)+" Warnings")


# critical warnings
criticalWarnings = ['Elements have duplicate "Type Mark" values','There are identical instances in the same place',
    'Room Tag is outside of its Room','Multiple Rooms are in the same enclosed region','One element is completely inside another']
criticalWarningCount = 0
for criticalWarning in allWarnings_collector:
    description = criticalWarning.GetDescriptionText()
    # for warning type heading
    try:
	    descLen = description.index(".")
	# Few warnings have nistakenly no dot in the end.
    except:
		descLen = len(description)
    descHeading = description[:descLen]
    if descHeading in criticalWarnings:
        criticalWarningCount += 1


# materials
materialCount = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Materials).GetElementCount()
# print(str(materialCount)+" Materials")


# line patterns
linePatternCount = FilteredElementCollector(doc).OfClass(LinePatternElement).GetElementCount()
# print(str(linePatternCount)+" Line Patterns")


# DWGs
dwg_collector = DB.FilteredElementCollector(revit.doc).OfClass(DB.ImportInstance).WhereElementIsNotElementType().ToElements()
importedDwg = 0
dwgNotCurrentView = 0
for dwg in dwg_collector:
    if dwg.IsLinked == False:
        importedDwg += 1
    if dwg.ViewSpecific == False:
        dwgNotCurrentView += 1

# print("\nDWGs")
# print(str(importedDwg)+" Imported DWG files")

# dwgCount = dwg_collector.GetElementCount()
dwgCount = len(dwg_collector)
linkedDwg = (dwgCount-importedDwg)


# tresholds
warningsTres = 500
criticalWarningsTres = 0
materialsTres = 150
linePatternsTres = 100
importedDwgTres = 0
linkedDwgTres = viewCount/2
dwgNotCurrentViewTres = 0

# dashboard row 2
htmlRow2 = (dashboardRectMaker(allWarningsCount,"Warnings",warningsTres,"Revit Warnings") + dashboardRectMaker(criticalWarningCount,"Critical Warnings",criticalWarningsTres,"Revit Warnings")
    + dashboardRectMaker(materialCount,"Materials",materialsTres,wikiArticle) + dashboardRectMaker(linePatternCount,"Line Patterns",linePatternsTres,"Linknutie DWG súboru do Revitu")
    + dashboardRectMaker(importedDwg,"Imported DWGs",importedDwgTres,"Kurz Revitu 2017 - Mierne pokročilí - 02-03C -Vkladanie (linkovanie) DWG a RVT súborov")
    + dashboardRectMaker(linkedDwg,"Linked DWGs",linkedDwgTres,"Linknutie DWG súboru do Revitu")
    + dashboardRectMaker(dwgNotCurrentView,"DWGs in 3D",dwgNotCurrentViewTres,wikiArticle))
dashboardCenterMaker(htmlRow2)


# CHART INPORTED DWGS OUTPUT
output = script.get_output()

chartImportedDWGs = output.make_doughnut_chart()
chartImportedDWGs.data.labels = ["imported DWG instances","linked DWG instances"]
set_a = chartImportedDWGs.data.new_dataset('Not Standard')
set_a.data = [importedDwg,dwgCount-importedDwg]

set_a.backgroundColor = [badColor,goodColor]
chartImportedDWGs.set_height(80)

chartImportedDWGs.draw()


# families
graphFCatHeadings = []
graphFCatData = []
families = FilteredElementCollector(doc).OfClass(Family)
inPlaceFamilyCount = 0
NotParamFamiliesCount = 0
for family in families:
    if family.IsInPlace == True:
        inPlaceFamilyCount += 1
        # for graph
        inPlaceFCategory = family.FamilyCategory.Name
        if inPlaceFCategory not in graphFCatHeadings:
            graphFCatHeadings.append(inPlaceFCategory)
        graphFCatData.append(inPlaceFCategory)
    if family.IsParametric == False:
        NotParamFamiliesCount += 1
familyCount = families.GetElementCount()


# print(str(familyCount)+" Families")
# print(str(inPlaceFamilyCount)+" In Place Families")

# print(str(NotParamFamiliesCount)+" Families are not parametric")

# tresholds
familiesTres = 500
inPlaceFamilyTres = familyCount*0.2
notParamFamiliesTres = familyCount*0.3
textnoteWFtres = 0
textnoteCaps = 0


# Text notes width factor != 1
textNoteType_collector = FilteredElementCollector(doc).OfClass(TextNoteType).ToElements()
textnoteWFcount = 0
for textnote in textNoteType_collector:
    widthFactor = textnote.LookupParameter('Width Factor').AsDouble()
    if widthFactor != 1:
        textnoteWFcount += 1

# Text notes with allCaps applied in Revit
textNote_collector = FilteredElementCollector(doc).OfClass(TextNote).ToElements()
capsCount = 0
for textN in textNote_collector:
	capsStatus = textN.GetFormattedText().GetAllCapsStatus()
	if str(capsStatus) != "None":
		capsCount +=1


# dashboard
# htmlRow3 = (dashboardRectMaker(familyCount,"Families",familiesTres) + dashboardRectMaker(inPlaceFamilyCount,"In Place Families",inPlaceFamilyTres) 
#     + dashboardRectMaker(NotParamFamiliesCount,"Families are not parametric",notParamFamiliesTres))
htmlRow3 = (dashboardRectMaker(familyCount,"Families",familiesTres,wikiArticle) + dashboardRectMaker(inPlaceFamilyCount,"In Place Families",inPlaceFamilyTres,wikiArticle)
        + dashboardRectMaker(NotParamFamiliesCount,"Families not parametric",notParamFamiliesTres,wikiArticle)
        + dashboardRectMaker(textnoteWFcount,"Text - Width Factor changed",textnoteWFtres,"Problémy s textom pri exporte z Revitu do DWG")
        + dashboardRectMaker(capsCount,"Text - AllCaps",textnoteCaps,"Problémy s textom pri exporte z Revitu do DWG"))
dashboardCenterMaker(htmlRow3)

# CHART INPLACE FAMILIES OUTPUT
output = script.get_output()

chartInPlaceFam = output.make_doughnut_chart()
chartInPlaceFam.data.labels = ["In Place Families","Loadable Families"]
set_a = chartInPlaceFam.data.new_dataset('Not Standard')
set_a.data = [inPlaceFamilyCount,familyCount-inPlaceFamilyCount]

set_a.backgroundColor = [badColor,goodColor]
chartInPlaceFam.set_height(80)

chartInPlaceFam.draw()

# CHART PARAMETRIC FAMILIES OUTPUT
output = script.get_output()

chartParamFam = output.make_doughnut_chart()
chartParamFam.data.labels = ["not parametric Families","Families with at least one dimensional parameter"]
set_a = chartParamFam.data.new_dataset('Not Standard')
set_a.data = [NotParamFamiliesCount,familyCount-NotParamFamiliesCount]

set_a.backgroundColor = [badColor,goodColor]
chartParamFam.set_height(80)

chartParamFam.draw()

# detail groups
detailGroupCount = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_IOSDetailGroups).WhereElementIsNotElementType().GetElementCount()
detailGroupTypeCount = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_IOSDetailGroups).GetElementCount() - detailGroupCount
# print(str(detailGroupTypeCount)+" Detail Group Types")
# print(str(detailGroupCount)+" Detail Groups")


# # CHART DETAIL GROUPS OUTPUT
# output = script.get_output()

# chartDetailGroups = output.make_doughnut_chart()
# chartDetailGroups.data.labels = ["Avg Detail Groups repeatability","Avg Detail Groups nonrepeatability"]
# set_a = chartDetailGroups.data.new_dataset('Detail Groups')
# set_a.data = [detailGroupCount-detailGroupTypeCount,detailGroupTypeCount]

# set_a.backgroundColor = [badColor,goodColor]
# chartDetailGroups.set_height(80)

# chartDetailGroups.draw()

# model groups
modelGroupCount = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_IOSModelGroups).WhereElementIsNotElementType().GetElementCount()
modelGroupTypeCount = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_IOSModelGroups).GetElementCount() - modelGroupCount
# print(str(modelGroupTypeCount)+" Model Group Types")
# print(str(modelGroupCount)+" Model Groups")

# # CHART MODEL GROUPS OUTPUT
# output = script.get_output()

# chartModelGroups = output.make_doughnut_chart()
# chartModelGroups.data.labels = ["Avg Model Groups repeatability","Avg Model Groups nonrepeatability"]
# set_a = chartModelGroups.data.new_dataset('Not Standard')
# set_a.data = [modelGroupCount-modelGroupTypeCount,modelGroupTypeCount]

# set_a.backgroundColor = [badColor,goodColor]
# chartModelGroups.set_height(80)

# chartModelGroups.draw()

# reference plane without name
refPlaneCollector = FilteredElementCollector(doc).OfClass(ReferencePlane).ToElements()
noNameRefPCount = 0
for refPlane in refPlaneCollector:
	if refPlane.Name == "Reference Plane":
		noNameRefPCount += 1

# Element Count
elementCount = FilteredElementCollector(doc).WhereElementIsNotElementType().GetElementCount()
# _2DelementCount = FilteredElementCollector(doc).OwnedByView().GetElementCount()

# print(str(elementCount)+" Elements")

# tresholds
detailGroupTypeTres = 30
detailGroupTres = 500
modelGroupTypeTres = 30
modelGroupTres = 200
noNameRefPTres = 0
elementsTres = 1000000

# dashboard
htmlRow4 = (dashboardRectMaker(detailGroupTypeCount,"Detail Group Types",detailGroupTypeTres,wikiArticle) + dashboardRectMaker(detailGroupCount,"Detail Groups",detailGroupTres,wikiArticle) 
    + dashboardRectMaker(modelGroupTypeCount,"Model Group Types",modelGroupTypeTres,wikiArticle)+dashboardRectMaker(modelGroupCount,"Model Groups",modelGroupTres,wikiArticle) 
    + dashboardRectMaker(noNameRefPCount,"NoName Ref Planes",noNameRefPTres,wikiArticle)+ dashboardRectMaker(elementCount,"Elements",elementsTres,wikiArticle))
dashboardCenterMaker(htmlRow4)


# divider
print("\n\n\n\n")

# data for category graph
graphCatHeadings = []
graphCatData = []
elements = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()
# categories to skip
catBanlist = ['Shared Site','Project Information','Structural Load Cases','Sun Path','Color Fill Schema','HVAC Zones','HVAC Load Schedules','Building Type Settings',
	'Space Type Settings','Survey Point','Project Base Point','Electrical Demand Factor Definitions','Electrical Load Classifications','Panel Schedule Templates - Branch Panel',
	'Panel Schedule Templates - Data Panel','Panel Schedule Templates - Switchboard','Electrical Load Classification Parameter Element','Automatic Sketch Dimensions',]
for i in elements:
    try:
    	category = i.Category.Name
        if category[-4:] != ".dwg" and category[-4:] != ".DWG" and category[0] != "<" and category[-1] != ")" and category not in catBanlist:
            if category not in graphCatHeadings:
                graphCatHeadings.append(category)
            graphCatData.append(category)
    except:
        pass

catSet=[]
# sorting results in chart legend
graphCatHeadings.sort()
for i in graphCatHeadings:
    count=graphCatData.count(i)        
    catSet.append(count)

# for debugging
# print graphCatHeadings
# print catSet

# categories OUTPUT
chartCategories = output.make_doughnut_chart()
chartCategories.options.title = {'display': True, 'text':'Element Count by Category', 'fontSize': 18, 'fontColor': '#000', 'fontStyle': 'bold'}
chartCategories.data.labels = graphCatHeadings
set_a = chartCategories.data.new_dataset('Not Standard')
set_a.data = catSet

set_a.backgroundColor = colors
# chartCategories.randomize_colors()
# scaling graph according to categories count - size of graph is measured with legend which can be quite complex
catCount = len(graphCatHeadings)
if catCount < 60:
    chartCategories.set_height(150)
elif catCount < 85:
    chartCategories.set_height(200)
elif catCount < 100:
    chartCategories.set_height(250)
else:
    chartCategories.set_height(300)

chartCategories.draw()

# divider
print("\n\n\n\n")


# elements by workset graph
worksetIds = []
worksetNames = []
graphWorksetsData = []
# elcollector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()
elcollector = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()
worksetTable = doc.GetWorksetTable()
for element in elcollector:
	worksetId = element.WorksetId
	worksetKind = str(worksetTable.GetWorkset(worksetId).Kind)
	if worksetKind == "UserWorkset":
		worksetName = worksetTable.GetWorkset(worksetId).Name
		if worksetName not in worksetNames:
			worksetNames.append(worksetName)
		graphWorksetsData.append(worksetName)
# print worksetNames
# sorting results in chart legend
worksetNames.sort()
worksetsSet=[]
for i in worksetNames:
    count=graphWorksetsData.count(i)        
    worksetsSet.append(count)

# Worksets OUTPUT print chart only when file is workshared
if len(worksetNames) > 0:
	chartWorksets = output.make_doughnut_chart()
	chartWorksets.options.title = {'display': True, 'text':'Element Count by Workset', 'fontSize': 18, 'fontColor': '#000', 'fontStyle': 'bold'}
	chartWorksets.data.labels = worksetNames
	set_a = chartWorksets.data.new_dataset('Not Standard')
	set_a.data = worksetsSet

	set_a.backgroundColor = colors

	worksetsCount = len(worksetNames)
	if worksetsCount < 15:
	    chartWorksets.set_height(100)
	elif worksetsCount < 30:
	    chartWorksets.set_height(160)
	else:
	    chartWorksets.set_height(200)

	chartWorksets.draw()

# divider
print("\n\n\n\n")

# INPLACE CATEGORY GRAPH
fCatSet=[]
# sorting results in chart legend
graphFCatHeadings.sort()
for i in graphFCatHeadings:
    count=graphFCatData.count(i)        
    fCatSet.append(count)


# categories OUTPUT
chartFCategories = output.make_doughnut_chart()
chartFCategories.options.title = {'display': True, 'text':'InPlace Family Count by Category', 'fontSize': 18, 'fontColor': '#000', 'fontStyle': 'bold'}
chartFCategories.data.labels = graphFCatHeadings
set_a = chartFCategories.data.new_dataset('Not Standard')
set_a.data = fCatSet

set_a.backgroundColor = colors
# chartFCategories.randomize_colors()
# scaling graph according to categories count - size of graph is measured with legend which can be quite complex
catFCount = len(graphFCatHeadings)
if catFCount < 15:
    chartFCategories.set_height(100)
elif catFCount < 30:
    chartFCategories.set_height(160)
else:
    chartFCategories.set_height(200)

chartFCategories.draw()


# for timing------
endtime = timer.get_time()
print(hmsTimer(endtime))