# -*- coding: utf-8 -*-

__title__ = 'Create Short\nRoom Numbers'
__doc__ = """Writes everything after last delimiter to parameter Room Number to custom Shared Parameter 'Room Number short'. You need to add parameter manually.

f.e.:
Room Number: 201.03.001a
Room Number short: 001a
"""
__author__ = 'David Vadkerti'

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, \
                Transaction, Document
from pyrevit import revit, DB
from pyrevit.coreutils import Timer
from pyrevit import coreutils, forms
from custom_output import hmsTimer
# from pyrevit import script
# output = script.get_output()

doc = __revit__.ActiveUIDocument.Document

# /////// COLLECTORS /////////
# collecting rooms
room_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms) \
    .WhereElementIsNotElementType() \
    .ToElements()

# /////// UI WINDOW /////////
class getDelimiterWindow(forms.WPFWindow):
    def __init__(self, xaml_file_name):
        forms.WPFWindow.__init__(self, xaml_file_name)
    
    def process_text(self, sender, args):
        self.Close()
        delimiter =  str(self.sheets_tb.Text)

        # for timing------
        timer = Timer()
        # ----------------

        t = Transaction(doc, "Create Short Room Numbers")
        t.Start()

        for room in room_collector:
            # getting the parameter
            # roomNumber = room.LookupParameter('Number').AsString()
            roomNumber = room.get_Parameter(DB.BuiltInParameter.ROOM_NUMBER).AsString()
            
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