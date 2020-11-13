# -*- coding: UTF-8 -*-
"""Warning Schedule.

Lists most Warnings related to architecural elements in the active model in Schedule with clickable Element Ids, Category of elements and Warning descritpions.

"""

__title__ = 'Critical Warning schedule'
__doc__ = 'Lists Warnings related to architecural elements in the active model in Schedule with clickable Element Ids, Category of elements and Warning descritpions.'

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
from pyrevit import revit, DB, coreutils, script, output, forms
from pyrevit.coreutils import Timer
from pyrevit.output import charts
from customOutput import criticalWarnings, hmsTimer
from customOutput import file_name_getter, colors, ct_icon

# from __future__ import division

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

allWarnings = doc.GetWarnings()
# estimated duration in minutes
estDuration=len(allWarnings)/140


timer = Timer()

output = script.get_output()
# changing icon
ct_icon(output)
output.print_md("# CRITICAL WARNINGS SCHEDULE")
output.print_md("### " + file_name_getter(doc))

# print markdown code schedule header
md_schedule = "| Warning No. | Element Id |  Element Category | Warning Description |\n| ----------- | ----------- | ----------- | ----------- |"
count = 0

cacheWarning = ""
cacheWarningType = ""
# for graph
graphHeadings = []
graphWarnData = []
# criticalWarnings = ['Elements have duplicate "Type Mark" values','There are identical instances in the same place',
#     'Room Tag is outside of its Room','Multiple Rooms are in the same enclosed region','One element is completely inside another']
for warning in allWarnings:
    elementsList=warning.GetFailingElements()
    description=warning.GetDescriptionText()

    # for warning type heading
    try:
        descLen = description.index(".")
    # Few warnings have nistakenly no dot in the end.
    except:
        descLen = len(description)
    descHeading = description[:descLen]
    # print descHeading
    if descHeading in criticalWarnings:
        count += 1
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

# chart = output.make_doughnut_chart()
chart = output.make_chart(version='2.8.0')
chart.type = charts.DOUGHNUT_CHART

chart.data.labels = graphHeadings
set_a = chart.data.new_dataset('Not Standard')
set_a.data = warnSet

set_a.backgroundColor = colors
chart.set_height(150)

chart.draw()
# for timing------
endtime = timer.get_time()
print(hmsTimer(endtime))
# import random
# print([(hmsTimer(n), n) for n in range(1,5000,2) if n%30==random.randint(1, 59)])