# -*- coding: UTF-8 -*-\n"
from pyrevit import EXEC_PARAMS
from pyrevit import forms

res = forms.alert("Chceš uložiť zoznam otvorených Views?",
                  options=["Uložiť",
                           "Neuložiť",
                           "Zistiť viac"],
                  title="In Place Family",
                  footer="CustomTools Hooks")
if res  == "Uložiť":
    # opened views
    from Autodesk.Revit.UI import UIDocument
    from Autodesk.Revit.DB.Document import GetElement
    from pyrevit import script

    doc = EXEC_PARAMS.event_args.Document
    uidoc = UIDocument(doc)
    docName = doc.PathName

    output = script.get_output()
    output.print_md("## List of Views for file: " + docName)

    openUIviews = uidoc.GetOpenUIViews()

    count = 0
    scheduleData = []
    allViewIds = []
    for uiview in openUIviews:
        count += 1
        view_id = uiview.ViewId
        viewName = doc.GetElement(view_id).Name
        paramList = [str(count), viewName, output.linkify(view_id)]
        scheduleData.append(paramList)
        allViewIds.append(view_id)

    output.print_table(table_data=scheduleData,
                       columns=["Number", "View Name", "View Id"],
                       formats=['', '', ''])

    print("\nSave this html file on your drive.")
    print("Use Import Report tool for reopening views.")

elif res  == "Neuložiť":
    pass
elif res  == "Zistiť viac":
    from pyrevit import script
    url = 'https://youtu.be/1lANcq6WONI'
    script.open_url(url)
else:
    pass

