from pyrevit import revit, DB
from pyrevit import forms, script
from Autodesk.Revit.UI import ColorSelectionDialog

__title__ = "Line Color"
__doc__ = 'Quicker override Projection Line Color of Elements.'
__author__ = "David Vadkerti"

selection = revit.get_selection()

# my_config = script.get_config()

try:
    if len(selection)>0:
        # Color dialog from revit
        colorPickerDialog = ColorSelectionDialog()
        colorPickerDialog. Show()
        color = colorPickerDialog.SelectedColor
        with revit.Transaction('Line Color'):
            src_style = DB.OverrideGraphicSettings()
            # constructing RGB value from list
            src_style.SetProjectionLineColor(color)
            for element in selection:
                revit.active_view.SetElementOverrides(element.Id, src_style)
    else:
        forms.alert('You must select at least one element.', exitscript=True)
except:
    pass