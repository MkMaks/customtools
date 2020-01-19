# -*- coding: UTF-8 -*-
"""Detail Group Schedule.
Lists all Detail Groups with links to Owner Views.
"""

__title__ = 'Detail Group\nschedule'
__doc__ = 'Lists all Detail Groups with links to Owner Views.'

from pyrevit import revit, DB
from pyrevit import script
from pyrevit import output
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory

from Autodesk.Revit.UI import UIApplication

doc = __revit__.ActiveUIDocument.Document
uiapp = UIApplication(doc.Application)

output = script.get_output()
output.print_md("# DETAIL GROUP SCHEDULE")

collector = FilteredElementCollector(doc)
groups = collector.OfCategory(BuiltInCategory.OST_IOSDetailGroups).WhereElementIsNotElementType().ToElements()

def newScheduleLine(count,groupName,groupId,viewName,viewType):
            return " \n| "+str(count)+" | "+groupName+" | "+output.linkify([groupId,groupId])+" | "+viewName+" | "+viewType+" |"   

viewList = []

count = 0
md_schedule = "| Number | Detail Group Name | Detail Group id | Owner View | View Type|\n| ----------- | ----------- | ----------- | ----------- | ----------- |"
for group in groups:
    try:
        if hasattr(group, "OwnerViewId"):
            groupName = group.Name
            groupId = group.Id
            view = group.Document.GetElement(group.OwnerViewId)
            viewName = view.LookupParameter('View Name').AsString()
            viewType = view.GetType().Name
            count += 1
            md_schedule += newScheduleLine(count,groupName,groupId,viewName,viewType)
        else:
            print None 
    except:
        pass

# print md_schedule
output.print_md(md_schedule)
# print dwgInst