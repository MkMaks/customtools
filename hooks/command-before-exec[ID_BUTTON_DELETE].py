# -*- coding: UTF-8 -*-

from pyrevit import EXEC_PARAMS
from pyrevit import forms, script, revit

doc = __revit__.ActiveUIDocument.Document
selection = revit.get_selection()

def alertWindow(viewNames):
    res = forms.alert("POZOR!\n\n"
    	              "Chceš naozaj vymazať tieto Views?\n"
                      + str(viewNames)[1:-1],
                      title="View, Schedule or Sheet Deletion",
                      footer="CustomTools Hooks",
                      options=["Zrušiť",
                               "Delete"])
    if res  == "Delete":
    	EXEC_PARAMS.event_args.Cancel = False
        from hooksScripts import hooksLogger
        hooksLogger("View, Schedule or Sheet Deletion",doc)
    elif res  == "Zrušiť":
    	EXEC_PARAMS.event_args.Cancel = True
    else:
    	EXEC_PARAMS.event_args.Cancel = True

# treating just Views and Schedules
viewNames = []
for element in selection:
    try:
        catName = element.Category.Name
        # print(catName)
        # print(element.Name)
        if catName == "Views" or catName == "Schedules" or catName == "Sheets":
            name = element.Name
            # noaccents conversion
            import unicodedata
            name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore')
            # name = name.decode('utf-8')
            viewNames.append(name)
    except:
        pass

# If there is at least one View or Schedule in selection show alert window
if len(viewNames) > 0:
    alertWindow(viewNames)