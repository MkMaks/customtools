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
                viewId = textNote.OwnerViewId
                viewName = doc.GetElement(viewId).Name
                paramList = [viewName, output.linkify(textNoteId)]
                scheduleData.append(paramList)
        sortedScheduleData = sorted(scheduleData, key=lambda x: x[0])
        output.print_table(table_data=sortedScheduleData,
                           title = "",
                           columns=["View Name", "Text Note ID"],
                           formats=['', ''])
    # no All Caps
    except:
        if capsCount == 0:
            print("AllCaps is not used in the project.")
        else:
            print("Something went wrong.")

showAllCapsSchedule()