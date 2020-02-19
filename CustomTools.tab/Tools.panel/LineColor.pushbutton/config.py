"""Configuration window for Match tool."""
#pylint: disable=E0401,C0111,W0613
from pyrevit import HOST_APP
from pyrevit import forms
from pyrevit import script


rgbValueList = [200,0,0]
_config.get_option('rgbValueList', rgbValueList)


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

script.save_config()