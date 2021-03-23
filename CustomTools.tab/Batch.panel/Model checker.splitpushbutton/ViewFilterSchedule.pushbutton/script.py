# -*- coding: UTF-8 -*-
__title__ = 'View Filter List'
__author__ = 'David Vadkerti'
__doc__ = 'Lists all View Filters with corresponding View Names'
__highlight__= 'new'

from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms
from pyrevit import output

from Autodesk.Revit.DB import FilteredElementCollector #, BuiltInCategory
from Autodesk.Revit.DB import RevisionCloud, Revision

from pyrevit.coreutils import Timer
from customOutput import hmsTimer, ct_icon, file_name_getter

doc = __revit__.ActiveUIDocument.Document
output = script.get_output()

# changing icon
ct_icon(output)

def revision_schedule(sortBy):
    timer = Timer()
    # heading
    output.print_md("# VIEW FILTER SCHEDULE")

    views = DB.FilteredElementCollector(revit.doc)\
              .OfCategory(DB.BuiltInCategory.OST_Views)\
              .WhereElementIsNotElementType()\
              .ToElements()

    scheduleData = []
    for v in views:
        view_filters = v.GetFilters()
        view_Name = v.Name
        view_id = v.Id
        viewType = str(v.ViewType)
        # view_creator = DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc,view_id).Creator
        for fl in view_filters:
            fl_name = revit.doc.GetElement(fl).Name
            paramList = [fl_name, view_Name, output.linkify(view_id), viewType]

            scheduleData.append(paramList)

    # sort by parameters
    if sortBy == "Filter Name":
        sortedScheduleData = sorted(scheduleData, key=lambda x: x[0].lower())
    elif sortBy == "View Name":
        sortedScheduleData = sorted(scheduleData, key=lambda x: x[1].lower())
    elif sortBy == "View Type":
        sortedScheduleData = sorted(scheduleData, key=lambda x: x[3].lower())
    else:
        sortedScheduleData = scheduleData


    # printing the schedule if there are data
    if sortedScheduleData:
        output.print_table(table_data=sortedScheduleData,
                           title = file_name_getter(doc),
                           columns=["Filter Name", "View Name", "View ID", "View Type"],
                           formats=['', '', '', ''])
    # if there are no data print status claim
    else:
        print("There are no View Filters in the Project")
      # for timing------
    endtime = timer.get_time()
    print(hmsTimer(endtime))

# GUI for sorting by parameter
selected_option = \
    forms.CommandSwitchWindow.show(
        ['Filter Name',
         'View Name',
         'View Type'],
        message='Sort by:'
        )

if selected_option:
    revision_schedule(selected_option)