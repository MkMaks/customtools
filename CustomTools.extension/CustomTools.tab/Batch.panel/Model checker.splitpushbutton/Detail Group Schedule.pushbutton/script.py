# -*- coding: UTF-8 -*-
"""Detail Group Schedule.
Lists all Detail Groups with links to Owner Views.
"""

__title__ = 'Detail Group\nschedule'
__doc__ = 'Lists all Detail Groups with links to Owner Views.'

from pyrevit import revit, DB
from pyrevit import script
from pyrevit import output, forms
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
from Autodesk.Revit.UI import UIApplication
from pyrevit.coreutils import Timer
from custom_output import hmsTimer

doc = __revit__.ActiveUIDocument.Document
uiapp = UIApplication(doc.Application)

# detailGroupCount = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_IOSDetailGroups).WhereElementIsNotElementType().GetElementCount()
sheets_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets) \
.WhereElementIsNotElementType().GetElementCount()
# dialogue box only when 1 minute or longer
if sheets_collector > 30:
    res = forms.alert("Táto operácia môže bežať dlhšie.\n\n"
                  "Prajete si pokračovať?",
                  ok=False, yes=True, no=True)
else:
    res = True
if res:
    timer = Timer()

    output = script.get_output()
    output.print_md("# DETAIL GROUP SCHEDULE")

    collector = FilteredElementCollector(doc)
    groups = collector.OfCategory(BuiltInCategory.OST_IOSDetailGroups).WhereElementIsNotElementType().ToElements()

    def newScheduleLine(count,groupName,groupId,viewName,viewType):
                return " \n| "+str(count)+" | "+groupName+" | "+output.linkify([groupId])+" | "+viewName+" | "+viewType+" |"   


    count = 0
    md_schedule = "| Number | Detail Group Name | Detail Group id | Owner View | View Type|\n| ----------- | ----------- | ----------- | ----------- | ----------- |"
    cacheView = ""
    for group in groups:
        try:
            if hasattr(group, "OwnerViewId"):
                groupName = group.Name
                groupId = group.Id
                view = doc.GetElement(group.OwnerViewId)
                # view = group.Document.GetElement(group.OwnerViewId)
                viewName = view.Name
                viewType = str(view.ViewType)
                count += 1
                if cacheView == viewName:
                    md_schedule += newScheduleLine(count,groupName,groupId,viewName,viewType)
                else:
                    blankLine = " \n| **" +viewName.upper()+"**"
                    md_schedule += blankLine + newScheduleLine(count,groupName,groupId,viewName,viewType)
                cacheView = viewName
            else:
                print None 
        except:
            pass

    # print md_schedule
    output.print_md(md_schedule)
    # print dwgInst

    # for timing------
    endtime = timer.get_time()
    print(hmsTimer(endtime))