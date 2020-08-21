# -*- coding: UTF-8 -*-
__title__ = 'Detail Group\nschedule'
__author__ = 'David Vadkerti'
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

view_count = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views) \
.WhereElementIsNotElementType().GetElementCount()


group_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_IOSDetailGroups).WhereElementIsNotElementType()
groups = group_collector.ToElements()
groups_count = group_collector.GetElementCount()

# dialogue box only when 1 minute or longer
if view_count*groups_count > 500000:
    res = forms.alert("Táto operácia môže bežať dlhšie.\n\n"
                  "Prajete si pokračovať?",
                  ok=False, yes=True, no=True)
else:
    res = True
if res:
    def showGroupSchedule(sortBy):
        timer = Timer()

        output = script.get_output()
        output.print_md("# DETAIL GROUP SCHEDULE")

        if groups_count>0:
            scheduleData = []
            for group in groups:
                try:
                    # if hasattr(group, "OwnerViewId"):
                    groupName = group.Name
                    groupId = group.Id
                    view = doc.GetElement(group.OwnerViewId)
                    viewName = view.Name
                    viewType = str(view.ViewType)
                    # else:
                    #     print None 
                except:
                    pass

                paramList = [groupName, output.linkify([groupId]), viewName, viewType]
                scheduleData.append(paramList)

            # sort by parameter name
            if sortBy == "Detail Group Name":
                sortedScheduleData = sorted(scheduleData, key=lambda x: x[0].lower())
            # sort by parameter group
            elif sortBy == "View Name":
                sortedScheduleData = sorted(scheduleData, key=lambda x: x[2].lower())
            else:
                sortedScheduleData = scheduleData
            # output.print_md(md_schedule)
            output.print_table(table_data=sortedScheduleData,
                               title = "Sorted by " + sortBy,
                               columns=["Detail Group Name", " Detail Group id", "Owner View", "View Type"],
                               formats=['', '', '', ''])

            # for timing------
            endtime = timer.get_time()
            print(hmsTimer(endtime))
        else:
            print("There are no Detail Groups in the Project.")

    selected_option = \
        forms.CommandSwitchWindow.show(
            ['Detail Group Name',
             'View Name',
             "Time"],
            message='Sort by:'
            )

    if selected_option:
        showGroupSchedule(selected_option)