# -*- coding: UTF-8 -*-
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms
from pyrevit import output

from Autodesk.Revit.DB import FilteredElementCollector #, BuiltInCategory
from Autodesk.Revit.DB import RevisionCloud, Revision, TextNoteType, TextNote

from pyrevit.coreutils import Timer
from customOutput import hmsTimer, ct_icon, file_name_getter

doc = __revit__.ActiveUIDocument.Document
output = script.get_output()

# changing icon
ct_icon(output)

timer = Timer()
# heading
output.print_md("# Text Note Type schedule")

textNoteType_collector = FilteredElementCollector(doc).OfClass(TextNoteType).ToElements()
textNote_collector = FilteredElementCollector(doc).OfClass(TextNote).WhereElementIsNotElementType().ToElements()

# count of instances per type
text_note_types = {}
for tn in textNote_collector:
    tn_type_id = tn.GetTypeId().ToString()
    try:
        text_note_types[tn_type_id] +=1
    except:
        text_note_types[tn_type_id] = 1

# text notes type parameters
scheduleData = []
for text_note in textNoteType_collector:
    text_note_name = text_note.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
    font = text_note.get_Parameter(DB.BuiltInParameter.TEXT_FONT).AsString()
    size = text_note.get_Parameter(DB.BuiltInParameter.TEXT_SIZE).AsDouble() * 304.8
    bold = text_note.get_Parameter(DB.BuiltInParameter.TEXT_STYLE_BOLD).AsInteger()
    background = text_note.get_Parameter(DB.BuiltInParameter.TEXT_BACKGROUND).AsInteger()
    tb_visibility = text_note.get_Parameter(DB.BuiltInParameter.TEXT_BOX_VISIBILITY).AsInteger()
    width_factor = text_note.get_Parameter(DB.BuiltInParameter.TEXT_WIDTH_SCALE).AsDouble()
    text_note_id = text_note.Id
    try:
        count = text_note_types[text_note_id.ToString()]
    except:
        count = 0

    paramList = [text_note_name, font, size, bold, background, tb_visibility, width_factor, output.linkify(text_note_id), count]

    scheduleData.append(paramList)

# sort by parameters
sortedScheduleData = sorted(scheduleData, key=lambda x: int(x[8]))

# printing the schedule if there are data
if sortedScheduleData:
    output.print_table(table_data=sortedScheduleData,
                       title = file_name_getter(doc),
                       columns=["Text Note Type", "Font", "Size", "Bold", "Background", "Text Box Visibility" ,"Width Factor", "Text Note Type ID", "Count"],
                       formats=['', '', '', '', '', '', '', '', ''])
# if there are no data print status claim
else:
    print("There are no Text Note Types in the Project")
  # for timing------
endtime = timer.get_time()
print(hmsTimer(endtime))