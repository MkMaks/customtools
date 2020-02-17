'''
Finds all Text Notes shere AllCaps is used.
'''

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, TextNote
from pyrevit import revit, DB, script

doc = __revit__.ActiveUIDocument.Document

output = script.get_output()

# Text notes with allCaps applied in Revit
def showAllCapsSchedule():
    output.print_md("# ALL CAPS SCHEDULE")
    scheduleData = []

    textNote_collector = FilteredElementCollector(doc).OfClass(TextNote).ToElements()
    capsCount = 0
    try:
        for textNote in textNote_collector:
            capsStatus = textNote.GetFormattedText().GetAllCapsStatus()
            if str(capsStatus) != "None":
                capsCount +=1
                textNoteId =  textNote.Id
                paramList = [capsCount, output.linkify(textNoteId)]
                scheduleData.append(paramList)
        output.print_table(table_data=scheduleData,
                           title = "",
                           columns=["Number", "Text Note ID"],
                           formats=['', ''])
    # no All Caps
    except:
        if capsCount == 0:
            print("AllCaps is not used in the project.")
        else:
            print("Something went wrong.")

showAllCapsSchedule()