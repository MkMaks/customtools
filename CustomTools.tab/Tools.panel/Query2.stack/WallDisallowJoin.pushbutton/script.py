# -*- coding: utf-8 -*-
__title__ = 'Wall Disallow Join'
__doc__ = """Changes Wall ends to Disallow join or Allow join of all selected Walls."""

__context__ = 'Selection'


from Autodesk.Revit.DB import WallUtils
from pyrevit import revit
from Autodesk.Revit.DB import Transaction
from pyrevit import forms

doc = __revit__.ActiveUIDocument.Document


class wallDisallowJoinWindow(forms.WPFWindow):
    def __init__(self, xaml_file_name):
        forms.WPFWindow.__init__(self, xaml_file_name)

    def viewEraser(self, sender, args):
        self.Close()
        disallowCB= self.disallow.IsChecked
        allowCB= self.allow.IsChecked
        wallEnd0CB= self.wallEnd0.IsChecked
        wallEnd1CB= self.wallEnd1.IsChecked

        doc = __revit__.ActiveUIDocument.Document
        curview = revit.active_view

        t = Transaction(doc, "Wall dissallow join")
        t.Start()


        if disallowCB == True:
            element_collector = revit.get_selection()
            for wall in element_collector:
                try:
                    if wallEnd0CB == True:
                        WallUtils.DisallowWallJoinAtEnd(wall,0)
                    if wallEnd1CB == True:
                        WallUtils.DisallowWallJoinAtEnd(wall,1)
                except:
                    pass

        if allowCB == True:
            element_collector = revit.get_selection()
            for wall in element_collector:
                try:
                    if wallEnd0CB == True:
                        WallUtils.AllowWallJoinAtEnd(wall,0)
                    if wallEnd1CB == True:
                        WallUtils.AllowWallJoinAtEnd(wall,1)
                except:
                    pass

        t.Commit()

wallDisallowJoinWindow('wallDisallowJoinWindow.xaml').ShowDialog()