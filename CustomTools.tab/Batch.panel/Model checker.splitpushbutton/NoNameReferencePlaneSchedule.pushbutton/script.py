# -*- coding: UTF-8 -*-
__title__ = 'Noname Reference Plane schedule'
__author__ = 'David Vadkerti'
__doc__ = 'Lists all Reference Planes without asigned name'

from pyrevit import revit, DB
from pyrevit import script
from pyrevit import output

from Autodesk.Revit.DB import FilteredElementCollector, ReferencePlane
from Autodesk.Revit.DB import View

from pyrevit.coreutils import Timer
from customOutput import hmsTimer
from customOutput import file_name_getter, ct_icon

doc = __revit__.ActiveUIDocument.Document

timer = Timer()
output = script.get_output()
# changing icon
ct_icon(output)
output.print_md("# NONAME REFERENCE PLANES")
output.print_md("### " + file_name_getter(doc))

# reference plane without name
refPlaneCollector = FilteredElementCollector(doc).OfClass(ReferencePlane).WhereElementIsNotElementType().ToElements()
scheduleData = []
for refPlane in refPlaneCollector:
    if refPlane.Name == "Reference Plane":
        refPlane_id = refPlane.Id
        refPlane_creator = DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc,refPlane_id).Creator
        paramList = [output.linkify(refPlane_id), str(refPlane_creator)]
        scheduleData.append(paramList)


# sort by view name
sortedScheduleData = sorted(scheduleData, key=lambda x: x[0].lower())

# output.print_md(md_schedule)
output.print_table(table_data=sortedScheduleData,
                   title = "Sorted by ID",
                   columns=["RefPlane ID","Author"],
                   formats=['', ''])

print("Total Number of Noname Reference Planes: " + str(len(refPlaneCollector)))
# for timing------
endtime = timer.get_time()
print(hmsTimer(endtime))