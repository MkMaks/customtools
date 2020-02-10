# -*- coding: UTF-8 -*-

__title__ = '2D Elements per View'
__author__ = 'David Vadkerti'
__doc__ = 'Lists all Elements of selected Type per View'

from pyrevit import revit, DB
from pyrevit import script
from pyrevit import output, forms

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
from Autodesk.Revit.DB import View
from customOutput import colors

from stringFormating import accents2ascii

doc = __revit__.ActiveUIDocument.Document

output = script.get_output()

def findDetailItems(Lines,selected_option):
    output.print_md("# "+ selected_option.upper() +" PER VIEW SCHEDULE")
    md_schedule = "| Number | View Name | View ID | Number of Elements \n| ----------- | ----------- | ----------- | ----------- |"

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
    try:
        chartWorksets = output.make_doughnut_chart()
        chartWorksets.options.title = {'display': True, 'text': selected_option +' per View', 'fontSize': 18, 'fontColor': '#000', 'fontStyle': 'bold'}
        chartWorksets.data.labels = viewNames
        set_a = chartWorksets.data.new_dataset('Not Standard')
        set_a.data = lineCountSet

        set_a.backgroundColor = colors

        # chart size
        viewCount = len(viewNames)
        viewCountChar = len(str(viewNames))
        legendSize = viewCount*5 + viewCountChar
        # print legendSize
        if legendSize < 1500:
            chartWorksets.set_height(180)
        elif legendSize < 10000:
            chartWorksets.set_height(legendSize/8)
        else:
            chartWorksets.set_height(legendSize/12)

        chartWorksets.draw()
    except:
        print("There was not allowed character in the data. Creation of graph was skipped. Scroll up for the schedule.")

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