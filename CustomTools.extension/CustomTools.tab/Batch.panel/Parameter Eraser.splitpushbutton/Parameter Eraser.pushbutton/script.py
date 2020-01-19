# -*- coding: utf-8 -*-
__title__ = 'Parameter\nValue Eraser'
__doc__ = """Erases selected Instance and Type parameters values."""

# for timing------
from pyrevit.coreutils import Timer
from pyrevit import forms
from custom_output import hmsTimer
# timer = Timer()
# ----------------

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction

# uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

class paramEraserWindow(forms.WPFWindow):
    def __init__(self, xaml_file_name):
        forms.WPFWindow.__init__(self, xaml_file_name)



    def process_text(self, sender, args):
        self.Close()
        typeParamString =  str(self.typeParamtb.Text)
        instanceParamString =  str(self.instanceParamtb.Text)
        roomParamString =  str(self.roomParamtb.Text)

        typeParamList=['Type Comments','Model','Manufacturer','URL','Description','Type Mark','Fire Rating']
        roomParamList=['Name','Number','Base Finish','Wall Finish','Floor Finish','Ceiling Finish','Department','Occupancy']
        instParamList=['Comments','Mark']

        # list from textbox strings
        typeParamList = self.listFromString(typeParamString)
        instanceParamList = self.listFromString(instanceParamString)
        roomParamList = self.listFromString(roomParamString)
        # print(instanceParamList)

        #Creating collector categories
        element_collector = FilteredElementCollector(doc).WhereElementIsNotElementType()
        type_collector = FilteredElementCollector(doc).WhereElementIsElementType()
        room_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType()

        t= Transaction(doc, "Full Parameter Value Eraser")
        t.Start()
        
        # for timing
        timer = Timer()

        for element in element_collector:
            try:
                self.ParamEraser(element,instanceParamList)
            except:
                pass

        for type in type_collector:
            try:
                self.ParamEraser(type,typeParamList)
            except:
                pass

        for room in room_collector:
            try:
                self.ParamEraser(room,roomParamList)
            except:
                pass

        t.Commit()
        # for timing------
        endtime = timer.get_time()
        print(hmsTimer(endtime))
		# ----------------

    def listFromString(self,string):
        letter=1
        spaceLessString=""
        for i in string:
            try:
                # treating double space
                if i==" " and string[letter]==" ":
                    i=""
                # treating space + comma
                if i==" " and string[letter]==",":
                    i=""
                # treating comma + spaces
                try:
                    if i==" " and spaceLessString[-1]==",":
                        i=""
                except:
                    pass
                letter+=1
                spaceLessString+=i
            except:
                pass

        splitValues = spaceLessString.split(",")
        print(spaceLessString)
        return splitValues

    def ParamEraser(self,el,paramList):
        paramValueString =  str(self.paramValuetb.Text)
        for paramname in paramList:
            filterp = el.LookupParameter(paramname)
            if filterp:
                # filterp.Set("no value")
                filterp.Set(paramValueString)          

paramEraserWindow('paramEraserWindow.xaml').ShowDialog()