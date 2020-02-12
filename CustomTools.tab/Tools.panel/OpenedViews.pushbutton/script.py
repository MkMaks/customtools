# -*- coding: UTF-8 -*-
__title__ = 'Opened\nViews'
__author__ = 'David Vadkerti'
__credits__ = 'http://eirannejad.github.io/pyRevit/credits/'
__doc__ = 'Lists all opened views in schedule for easier searching.'\
          'Save HTML file and use Import Report tool for reopening views.'

from Autodesk.Revit.UI import UIDocument
from Autodesk.Revit.DB.Document import GetElement
from pyrevit import revit, script

doc = __revit__.ActiveUIDocument.Document
uidoc = UIDocument(doc)

output = script.get_output()
output.print_md("# LIST OF OPENED VIEWS")

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

# show button to open all elements at once - cant open list using linify
# print output.linkify(allViewIds, title="all elements")

output.print_table(table_data=scheduleData,
                   columns=["Number", "View Name", "View Id"],
                   formats=['', '', ''])

print("\nSave this html file on your drive.")
print("Use Import Report tool for reopening views.")