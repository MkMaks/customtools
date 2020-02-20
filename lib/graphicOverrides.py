# -*- coding: utf-8 -*- 

# overrides projection lines in view
def setProjLines(r,g,b):
    from pyrevit import revit, DB, forms
    try:
    	selection = revit.get_selection()
        if len(selection)>0:
            with revit.Transaction('Line Color'):
                src_style = DB.OverrideGraphicSettings()
                # constructing RGB value from list
                # color = DB.Color(255,0,0)
                color = DB.Color(r,g,b)
                src_style.SetProjectionLineColor(color)
                for element in selection:
                    revit.active_view.SetElementOverrides(element.Id, src_style)
        else:
            forms.alert('You must select at least one element.', exitscript=True)
    except:
        pass