#pylint: disable=E0401,C0111,W0613,C0103
from pyrevit import revit, DB
from pyrevit import forms, script

__title__ = "Line Color"
__doc__ = 'Quicker override Projection Line Color of Elements.'
__author__ = "David Vadkerti"
__highlight__ = "new"

selection = revit.get_selection()

# my_config = script.get_config()

try:
    if len(selection)>0:
        colorPickerData = forms.select_swatch(
            title='Pick color',
            button_name='Override Graphics in View'
            )

        # RGB values from hexadecimal numbers
        colorPairs = []
        colorDataStriped = str(colorPickerData)[1:]
        couples = [colorDataStriped[i:i+2] for i in range(0, len(colorDataStriped), 2)]
        rgbValueList = []
        for i in couples:
            rgbValueList.append(int(i,16))

        with revit.Transaction('Match Graphics Overrides'):
            src_style = DB.OverrideGraphicSettings()
            # constructing RGB value from list
            color = DB.Color(rgbValueList[0],rgbValueList[1],rgbValueList[2])
            src_style.SetProjectionLineColor(color)
            for element in selection:
                revit.active_view.SetElementOverrides(element.Id, src_style)
    else:
        forms.alert('You must select at least one element.', exitscript=True)
except:
    pass