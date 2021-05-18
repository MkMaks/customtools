# -*- coding: UTF-8 -*-
__title__ = 'Revision Cloud Schedule\nschedule'
__author__ = 'David Vadkerti'
__doc__ = 'Lists all Revision Clouds with Comments filtered by selected Revisions'
__highlight__= 'updated'


from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms
from pyrevit import output

from Autodesk.Revit.DB import FilteredElementCollector #, BuiltInCategory
from Autodesk.Revit.DB import RevisionCloud, Revision

from pyrevit.coreutils import Timer
from customOutput import hmsTimer, ct_icon

doc = __revit__.ActiveUIDocument.Document
output = script.get_output()

# changing icon
ct_icon(output)

def revision_schedule(selected_revisions):
    timer = Timer()
    # heading
    output.print_md("# REVISION CLOUD SCHEDULE")
    revision_clouds = FilteredElementCollector(doc).OfClass(RevisionCloud).WhereElementIsNotElementType().ToElements()
    selected_revision_names = []
    for selected_revision in selected_revisions:
      count = 0
      scheduleData = []
      # removing accents
      selected_revision_name = selected_revision.Name
      # get revision ID
      selected_revision_Id = selected_revision.Id

      for revision_cloud in revision_clouds:
        revision_Id = revision_cloud.RevisionId
        if revision_Id == selected_revision_Id:
              count += 1
              element_Id = revision_cloud.Id
              comments = revision_cloud.get_Parameter(DB.BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS).AsString()
              creator = DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc,element_Id).Creator 
              mark = revision_cloud.get_Parameter(DB.BuiltInParameter.ALL_MODEL_MARK).AsString()
              if not mark:
              	# changing None to text string to avoid errors when sorting the list
              	mark = "_None"
              paramList = [str(count), mark, comments, output.linkify(element_Id), selected_revision_name, creator]

              scheduleData.append(paramList)
      # printing the schedule if there are data
      if scheduleData:
      	# sort by mark
      	sortedScheduleData = sorted(scheduleData, key=lambda x: x[2].lower())
        output.print_table(table_data=sortedScheduleData,
                           title = "Revision Cloud Schedule for Revision '" + selected_revision_name + "'",
                           columns=["Count", "Mark", "Comments", "Element Id", "Revision Name","Author"],
                           formats=['', '', '', '', '', ''])
      # if there are no data print status claim
      else:
        print("There is no Revision Cloud in Revision '"+ selected_revision_name + "'")
      # for timing------
    endtime = timer.get_time()
    print(hmsTimer(endtime))

# GUI to select revisions for revision clouds
selected_revisions = forms.select_revisions()
if selected_revisions:
    revision_schedule(selected_revisions)