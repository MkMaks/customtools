'''
Deletes all Views, Sheets and Schedules in Project and runs Purge Unused afterwards
'''
# for timing------
from pyrevit.coreutils import Timer
from pyrevit import forms
from custom_output import hmsTimer
timer = Timer()
# ----------------

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction
from pyrevit import revit, DB

__title__ = 'Views, Sheets &\nSchedule Eraser'


class viewEraserWindow(forms.WPFWindow):
    def __init__(self, xaml_file_name):
        forms.WPFWindow.__init__(self, xaml_file_name)


    def viewEraser(self, sender, args):
        self.Close()
        sheetsCB= self.sheets.IsChecked
        schedulesCB= self.schedules.IsChecked
        viewsCB= self.views.IsChecked

        doc = __revit__.ActiveUIDocument.Document
        curview = revit.active_view


        t = Transaction(doc, "Deleting all views, sheets and schedules")
        t.Start()


        if sheetsCB == True:
            sheets_id_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets) \
            .WhereElementIsNotElementType() \
            .ToElementIds()

            for sheet_id in sheets_id_collector:
                try:
                    doc.Delete(sheet_id)
                except:
                    pass

        if schedulesCB == True:
            schedules_id_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Schedules) \
            .WhereElementIsNotElementType() \
            .ToElementIds()

            for schedule_id in schedules_id_collector:
                try:    
                    doc.Delete(schedule_id)
                except:
                    pass

        if viewsCB == True:
            views_id_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views) \
            .WhereElementIsNotElementType() \
            .ToElementIds()

            for view_id in views_id_collector:
                    if view_id != curview.Id:
                        try:
                            doc.Delete(view_id)
                        except:
                            pass
                
        t.Commit()

        #run command Purge Unused
        from Autodesk.Revit.UI import UIApplication, RevitCommandId, PostableCommand

        Command_ID=RevitCommandId.LookupPostableCommandId(PostableCommand.PurgeUnused)
        #Command_ID=RevitCommandId.LookupCommandId("ID_PURGE_UNUSED")
        uiapp = UIApplication(doc.Application)
        uiapp.PostCommand(Command_ID)

viewEraserWindow('viewEraserWindow.xaml').ShowDialog()

# for timing------
endtime = timer.get_time()
print(hmsTimer(endtime))
# --------------