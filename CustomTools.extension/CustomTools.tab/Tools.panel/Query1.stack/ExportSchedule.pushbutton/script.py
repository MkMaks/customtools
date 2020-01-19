'''
Exports active schedule
'''
from pyrevit import revit

doc = __revit__.ActiveUIDocument.Document
curview = revit.active_view

#run command
from Autodesk.Revit.UI import UIApplication, RevitCommandId, PostableCommand
doc = __revit__.ActiveUIDocument.Document

Command_ID=RevitCommandId.LookupPostableCommandId(PostableCommand.ExportReportsSchedule)
uiapp = UIApplication(doc.Application)
uiapp.PostCommand(Command_ID)