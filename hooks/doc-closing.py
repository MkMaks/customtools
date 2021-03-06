# -*- coding: UTF-8 -*-\n"
from pyrevit import EXEC_PARAMS
from pyrevit import forms

from Autodesk.Revit.UI import UIDocument
from Autodesk.Revit.DB.Document import GetElement
from hooksScripts import hookTurnOff

# showing of dialog box with warning
def dialogBox():
  doc = EXEC_PARAMS.event_args.Document
  uidoc = UIDocument(doc)
  docName = doc.PathName
  fileExtension = docName[-3:]
  openUIviews = uidoc.GetOpenUIViews()

  if fileExtension == "rvt" and len(openUIviews)>1:
      res = forms.alert("Chceš uložiť zoznam otvorených Views?",
                        options=["Uložiť",
                                 "Preskočiť",
                                 "Zistiť viac"],
                        title="Save List Of Opened Views",
                        footer="CustomTools Hooks")
      if res  == "Uložiť":
          # try to cancel - if user is closing application we cannot cancel the event
          try:
           EXEC_PARAMS.event_args.Cancel()
          except:
            pass

          # opened views
          from pyrevit import script
          output = script.get_output()
          output.print_md("## List of Views for file: " + docName)

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

      elif res  == "Preskočiť":
          pass
      elif res  == "Zistiť viac":
          EXEC_PARAMS.event_args.Cancel()
          from pyrevit import script
          url = 'https://youtu.be/1lANcq6WONI'
          script.open_url(url)
      else:
          pass

# try to find config file for people who dont want to see the hook
hookTurnOff(dialogBox,12)