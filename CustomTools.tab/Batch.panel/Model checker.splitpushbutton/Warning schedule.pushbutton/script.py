# -*- coding: UTF-8 -*-
"""All Warning Schedule.

Lists most Warnings related to architecural elements in the active model in Schedule with clickable Element Ids, Category of elements and Warning descritpions.

"""

__title__ = 'All Warnings\nschedule'
__doc__ = 'Lists Warnings related to architecural elements in the active model in Schedule with clickable Element Ids, Category of elements and Warning descriptions.'

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
from pyrevit import revit, DB, coreutils, script, output, forms
from pyrevit.coreutils import Timer
from custom_output import hmsTimer
from customOutput import colors
from customOutput import file_name_getter

# from __future__ import division

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

allWarnings = doc.GetWarnings()
# estimated duration in minutes
estDuration=len(allWarnings)/140


# dialogue box only when 1 minute or longer
if estDuration > 0:
    res = forms.alert("Táto operácia môže na väčšom projekte bežať dlhšie.\n\n"
                  "Odhadovaný čas je " +str(estDuration)+" minút.\n"
                  "Prajete si pokračovať?",
                  ok=False, yes=True, no=True)
else:
    res = True
if res:
    timer = Timer()

    output = script.get_output()
    output.print_md("# WARNINGS SCHEDULE")
    output.print_md("### " + file_name_getter(doc))

    # print markdown code schedule header
    md_schedule = "| Warning No. | Element Id |  Element Category | Warning Description |\n| ----------- | ----------- | ----------- | ----------- |"
    count = 0

    cacheWarning = ""
    cacheWarningType = ""
    # for graph
    graphHeadings = []
    graphWarnData = []
    for warning in allWarnings:
        count += 1
        elementsList=warning.GetFailingElements()
        description=warning.GetDescriptionText()
        # for warning type heading
        try:
            descLen = description.index(".")
        # Few warnings have nistakenly no dot in the end.
        except:
            descLen = len(description)
        descHeading = description[:descLen]
        # print description
        # print elementsList
        

        for elemID in elementsList:
                # elem = doc.GetElement(elemID)
                # catName = elem.Category.Name
                try:
                    elem = doc.GetElement(elemID)
                except:
                    elem = "NA"
                try:
                    catName = elem.Category.Name
                except:
                    catName = "NA"
                idString = str(elemID.IntegerValue)
                # print(idString + " " +catName)
                # print(elemID)
                # print idString
                newScheduleLine = " \n| "+str(count)+" | "+output.linkify(elemID)+" | "+catName+" | "+description+" |"
                # new line when new warning number to visualy divide warnings
                if cacheWarningType == descHeading:
                    if cacheWarning == count:                    
                        md_schedule += newScheduleLine
                    else:
                        newScheduleLine = " \n| " + newScheduleLine
                        md_schedule += newScheduleLine
                else:
                        newScheduleLine = " \n <td colspan=3>**"+descHeading+".**<td colspan=3>" + newScheduleLine
                        # newScheduleLine = " \n| **"+description.upper()+"** |" + newScheduleLine
                        md_schedule += newScheduleLine
                cacheWarning = count
                cacheWarningType = descHeading
        # for graph headings
        if descHeading not in graphHeadings:
            graphHeadings.append(descHeading)
        # for graph warnings dataset
        graphWarnData.append(descHeading)
    # graph Headings
    warnSet=[]
    for i in graphHeadings:
        count=graphWarnData.count(i)        
        warnSet.append(count)


    # print markdown code
    output.print_md(md_schedule)


    # CHART OUTPUT
    output = script.get_output()

    chart = output.make_doughnut_chart()
    chart.data.labels = graphHeadings
    set_a = chart.data.new_dataset('Not Standard')
    set_a.data = warnSet

    set_a.backgroundColor = colors
    chart.set_height(200)

    chart.draw()
    # for timing------
    endtime = timer.get_time()
    print(hmsTimer(endtime))