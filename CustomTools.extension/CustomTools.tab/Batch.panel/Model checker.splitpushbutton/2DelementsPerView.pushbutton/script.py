# -*- coding: UTF-8 -*-

__title__ = '2D Elements\nper View'
__author__ = 'David Vadkerti'
__doc__ = 'Lists all Elements of selected Type per View'

from pyrevit import revit, DB
from pyrevit import script
from pyrevit import output, forms

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
from Autodesk.Revit.DB import View

from stringFormating import accents2ascii

doc = __revit__.ActiveUIDocument.Document

output = script.get_output()

def findDetailItems(Lines,selected_option):
    output.print_md("# "+ selected_option.upper() +" PER VIEW SCHEDULE")
    md_schedule = "| Number | View Name | View ID | Number of Elements \n| ----------- | ----------- | ----------- | ----------- |"

    # graph colors
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

    viewNames = []
    viewNamesAcc = []
    viewIds = []
    graphViewsData = []
    for line in Lines:
        OwnerViewId = line.OwnerViewId
        try:
            viewId = OwnerViewId
            viewNameAcc = doc.GetElement(OwnerViewId).Name
            # unaccented
            viewName = accents2ascii(viewNameAcc)

            # elements by workset graph
            if viewNameAcc not in viewNamesAcc:
                viewNamesAcc.append(viewNameAcc)
                # nonaccented version for chart
                viewNames.append(viewName)
                viewIds.append(viewId)
            graphViewsData.append(viewName)
        except:
            pass

    lineCountSet=[]
    count = 0
    for i in viewNames:
        lineCount=graphViewsData.count(i)   
        lineCountSet.append(lineCount)
        count += 1
        newScheduleLine = " \n| "+str(count)+" | "+viewNamesAcc[count-1]+" | "+output.linkify(viewIds[count-1])+" | "+ str(lineCountSet[count-1]) +" |"
        md_schedule += newScheduleLine

    output.print_md(md_schedule)

    # chart
    chartWorksets = output.make_doughnut_chart()
    chartWorksets.options.title = {'display': True, 'text': selected_option +' per View', 'fontSize': 18, 'fontColor': '#000', 'fontStyle': 'bold'}
    chartWorksets.data.labels = viewNames
    set_a = chartWorksets.data.new_dataset('Not Standard')
    set_a.data = lineCountSet

    set_a.backgroundColor = colors

    worksetsCount = len(viewNames)
    if worksetsCount < 50:
        chartWorksets.set_height(180)
    elif worksetsCount < 100:
        chartWorksets.set_height(250)
    elif worksetsCount < 300:
        chartWorksets.set_height(500)
    elif worksetsCount < 500:
        chartWorksets.set_height(800)
    elif worksetsCount < 1000:
        chartWorksets.set_height(1000)
    else:
        chartWorksets.set_height(2000)

    chartWorksets.draw()

selected_option = \
    forms.CommandSwitchWindow.show(
        ['Detail Lines',
         'Text Notes',
         'Dimensions',],
        message='Schedule items:'
        )

if selected_option == 'Detail Lines':    
    Lines = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Lines).WhereElementIsNotElementType().ToElements()
    findDetailItems(Lines,selected_option)
if selected_option == 'Text Notes':    
    TextNotes = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TextNotes).WhereElementIsNotElementType().ToElements()
    findDetailItems(TextNotes,selected_option)
if selected_option == 'Dimensions':    
    Dimensions = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Dimensions).WhereElementIsNotElementType().ToElements()
    findDetailItems(Dimensions,selected_option)