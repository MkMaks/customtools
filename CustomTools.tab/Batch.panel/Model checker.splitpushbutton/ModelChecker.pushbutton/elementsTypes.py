# -*- coding: UTF-8 -*-
from __future__ import division
"""Model Checker.
Revit file quality control.
"""

__title__ = 'Model\nChecker'
__doc__ = 'Revit file quality control'
__author__ = 'David Vadkerti'
__helpurl__ = 'https://youtu.be/c7Q3IYmRFlM'


from pyrevit import revit, DB
from pyrevit import forms
from pyrevit import script, coreutils
from pyrevit import output
import os.path as op
import math

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, ImportInstance
from Autodesk.Revit.UI import UIApplication
from pyrevit.coreutils import Timer
from custom_output import hmsTimer
from Autodesk.Revit.DB import LinePatternElement, Family, TextNoteType, ScheduleSheetInstance, WorksetTable, TextNote, ReferencePlane

from stringFormating import accents2ascii
from customOutput import colors, criticalWarnings

doc = __revit__.ActiveUIDocument.Document
uiapp = UIApplication(doc.Application)

timer = Timer()


# View Dependent element count
all_elements = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()
elementCount = FilteredElementCollector(doc).WhereElementIsNotElementType().GetElementCount()

md_scheduleOther = ""
md_schedule2d = ""
md_schedule3D = ""

output = script.get_output()

# for element in all_elements:
#     owner_view_id_int = element.OwnerViewId.IntegerValue
#     if owner_view_id_int != -1:
#         _View_dependent_elements += 1
#     else:
#         _3D_elements += 1
#         md_schedule += output.linkify(element.Id)

for element in all_elements:
    if element.Location:
        if element.ViewSpecific:
            md_schedule2d += output.linkify(element.Id)
        else:
            md_schedule3D += output.linkify(element.Id)
    else:
        md_scheduleOther += output.linkify(element.Id)


        # print(element.Location)
    # if element.Location != -1:
    #     _View_dependent_elements += 1
    # else:
    #     _3D_elements += 1
    #     md_schedule += output.linkify(element.Id)
output.print_md("##2D elements")
output.print_md(md_schedule2d)
output.print_md("##3D elements")
output.print_md(md_schedule3D)
output.print_md("##other elements")
output.print_md(md_scheduleOther)

print("_View_dependent_elements " + str(_View_dependent_elements))
print("_3D_elements " + str(_3D_elements))

# calculating percentage
if _View_dependent_elements == 0:
    print(0)
else:
    percentage = _3D_elements/elementCount*100
    print(str(percentage) + " %")
    

# for timing------
endtime = timer.get_time()
print(hmsTimer(endtime))