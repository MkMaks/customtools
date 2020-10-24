from pyrevit import revit, DB
from pyrevit import forms, script

__title__ = "Line Color"
__doc__ = 'Quicker override Projection Line Color of Elements.'
__author__ = "David Vadkerti"

selection = revit.get_selection()
my_config = script.get_config()

try:
    if selection:
        # read the config parameter value
        try:
            # my_config.color_code
            new_color_code = getattr(my_config, "color_code")
        except:
            setattr(my_config, "color_code", "100,177,70")
            new_color_code = getattr(my_config, "color_code")
            script.save_config()

        # print(new_color_code)
        src_style = DB.OverrideGraphicSettings()
        # spliting color code to list of 3 strings
        new_color_code_list = new_color_code.split(",")
        # list of integers
        new_color_list = [int(x) for x in new_color_code_list]
        # print(new_color_list)
        new_color = DB.Color(new_color_list[0],new_color_list[1],new_color_list[2])
        # setting graphic override
        with revit.Transaction('Line Color'):
            src_style.SetProjectionLineColor(new_color)
            for element in selection:
                revit.active_view.SetElementOverrides(element.Id, src_style)
    else:
        forms.alert('You must select at least one element.', exitscript=True)
except:
    pass