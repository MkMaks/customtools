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
md_schedule = "| Number | View Name | View Id |\n| ----------- | ----------- | ----------- |"  

openUIviews = uidoc.GetOpenUIViews()

count = 0
for uiview in openUIviews:
    count += 1
    view_id = uiview.ViewId
    viewName = doc.GetElement(view_id).Name
    newScheduleLine = " \n| "+str(count)+" | "+viewName+" | "+output.linkify(view_id)+" |"
    md_schedule += newScheduleLine

output.print_md(md_schedule)
print("\nSave this html file on your drive.")
print("Use Import Report tool for reopening views.")