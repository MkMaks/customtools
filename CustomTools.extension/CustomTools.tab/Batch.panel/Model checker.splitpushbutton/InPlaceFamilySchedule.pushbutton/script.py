# -*- coding: UTF-8 -*-
"""In Place Family schedule.

"""

__title__ = 'In Place Family\nschedule'
__author__ = 'David Vadkerti'
__doc__ = 'Lists all In Place Families'

import clr
from collections import defaultdict

from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms
from pyrevit import output

from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import Family

from pyrevit.coreutils import Timer
from custom_output import hmsTimer

doc = __revit__.ActiveUIDocument.Document
timer = Timer()

output = script.get_output()


families = FilteredElementCollector(doc).OfClass(Family).ToElements()


dwgInst = defaultdict(list)
workset_table = revit.doc.GetWorksetTable()


output.print_md("# IN PLACE FAMILY SCHEDULE")

md_schedule = "| Number | In Place Family Name | Category | Family ID | Author |\n| ----------- | ----------- | ----------- | ----------- | ----------- |"
count = 0
for family in families:
    if family.IsInPlace == True:
        count += 1
        familyCategory = family.FamilyCategory.Name
        familyName = family.Name
        family_id = family.Id
        # familySymbol_id = str(family.GetFamilySymbolIds())
        # familySymbol_id = family.GetFamilySymbolIds()
        # f = []
        # for i in familySymbol_id:
        # 	f.append(str(i))
        family_creator = DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc,family_id).Creator 
        newScheduleLine = " \n| "+str(count)+" | "+familyName+" | "+familyCategory+" | "+output.linkify(family_id)+" | " + family_creator + " |"
        # newScheduleLine = " \n| "+str(count)+" | "+familyName+" | "+familyCategory+" | "+output.linkify(f)+" | " + family_creator + " |"
        md_schedule += newScheduleLine

# print md_schedule
output.print_md(md_schedule)

# for timing------
endtime = timer.get_time()
print(hmsTimer(endtime))