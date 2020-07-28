# -*- coding: utf-8 -*-

__title__ = 'Create Short\nRoom Numbers'
__doc__ = """Writes everything agter last delimiter in parameter Room Number to custom Shared Parameter Room Number short."""


# for timing------
from pyrevit.coreutils import Timer
from pyrevit import coreutils, forms
from custom_output import hmsTimer
timer = Timer()
# ----------------

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, \
                Transaction, Document
from pyrevit import revit, DB
from pyrevit import script

doc = __revit__.ActiveUIDocument.Document

# /////// COLLECTORS /////////
# collecting rooms
room_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms) \
    .WhereElementIsNotElementType() \
    .ToElements()

# output = script.get_output()

# /////// UI WINDOW /////////
class getDelimiterWindow(forms.WPFWindow):
    def __init__(self, xaml_file_name):
        forms.WPFWindow.__init__(self, xaml_file_name)
    
    def process_text(self, sender, args):
        self.Close()
        delimiter =  str(self.sheets_tb.Text)

        t = Transaction(doc, "Create Short Room Numbers")
        t.Start()

        for room in room_collector:
            # getting the parameter
            roomNumber = room.LookupParameter('Number').AsString()
            
            # shortening the room number
            # delimiter = "-"
            roomNumberShortValue = roomNumber.split(delimiter)[-1]

            # setting the parameter
            roomNumberShortParameter = room.LookupParameter("Room Number short")
            if roomNumberShortParameter:
                    roomNumberShortParameter.Set(roomNumberShortValue)
            else:
                print("Room " + roomNumber + " has been skipped!")

        t.Commit()

        # for timing------
        endtime = timer.get_time()
        print(hmsTimer(endtime))
        # --------------

getDelimiterWindow('getDelimiterWindow.xaml').ShowDialog()