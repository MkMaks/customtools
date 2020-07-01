# -*- coding: UTF-8 -*-
"""DWG schedule.

Lists all linked and imported DWG instances with worksets and creator.

Copyright (c) 2017 Frederic Beaupere redesigned by David Vadkerti
github.com/frederic-beaupere

--------------------------------------------------------
PyRevit Notice:
Copyright (c) 2014-2017 Ehsan Iran-Nejad
pyRevit: repository at https://github.com/eirannejad/pyRevit

"""

__title__ = 'DWG schedule'
__author__ = 'original author Frederic Beaupere, redesigned by David Vadkerti'
__credits__ = 'http://eirannejad.github.io/pyRevit/credits/'
__doc__ = 'Lists all linked and imported DWG instances in schedule'\
          'with Owner Views and Authors.'

import clr
from collections import defaultdict

from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms
from pyrevit import output


output = script.get_output()

def listdwgs(current_view_only=False,):
    dwgs = DB.FilteredElementCollector(revit.doc)\
             .OfClass(DB.ImportInstance)\
             .WhereElementIsNotElementType()\
             .ToElements()

    dwgInst = defaultdict(list)
    workset_table = revit.doc.GetWorksetTable()
    

    output.print_md("# LINKED AND IMPORTED DWG FILES SCHEDULE")

    for dwg in dwgs:
        if dwg.IsLinked:
            dwgInst["LINKED DWGs"].append(dwg)
        else:
            dwgInst["IMPORTED DWGs"].append(dwg)

    for link_mode in dwgInst:
        md_schedule = "| Number | DWG name |  DWG id | Owner View Name | Current View Only | Author |\n| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |"
        output.print_md("##{}".format(link_mode))
        count = 0
        for dwg in dwgInst[link_mode]:
            dwg_id = dwg.Id
            dwg_name = \
                dwg.Parameter[DB.BuiltInParameter.IMPORT_SYMBOL_NAME].AsString()
            dwg_workset = workset_table.GetWorkset(dwg.WorksetId).Name[6:-1]
            dwg_instance_creator = \
                DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc,
                                                              dwg.Id).Creator  
            # is DWG linked in Current View Only? returns boolean 
            try:
                dwg2D = dwg.ViewSpecific
                if dwg2D:
                    dwg2Dstring = "Yes"
                else:
                    dwg2Dstring = "NO!"
            except:
                dwg2D="No data"
            count += 1
            if current_view_only \
                    and revit.active_view.Id != dwg.OwnerViewId:
                continue
            newScheduleLine = " \n| "+str(count)+" | "+dwg_name+" | "+output.linkify(dwg_id)+" | "+dwg_workset+" | "+dwg2Dstring+" | "+dwg_instance_creator+" |"
            md_schedule += newScheduleLine
        # print md_schedule
        output.print_md(md_schedule)
        # print dwgInst

selected_option = \
    forms.CommandSwitchWindow.show(
        ['Current View',
         'Entire Project'],
        message='Show DWGs for:'
        )

if selected_option:
    listdwgs(current_view_only=selected_option == 'Current View')