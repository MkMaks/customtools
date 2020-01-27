# -*- coding: utf-8 -*-
# logging to server
def hooksLogger(log_string):
  from datetime import datetime
  from pyrevit import revit
  from Autodesk.Revit.UI import UIApplication

  doc = __revit__.ActiveUIDocument.Document
  uiapp = UIApplication(doc.Application)

  user_name = doc.Application.Username
  def path2fileName(file_path,divider):
      # file_path_split = file_path.split("\\")
      file_path_split = file_path.split(divider)
      file_name = file_path_split[-1]
      file_name = file_name[:-4]
      # print file_name
      return file_name

  # workshared file
  try:
     central_path = revit.query.get_central_path(doc=revit.doc)
     file_name = path2fileName(central_path,"/")
  # non workshared file
  except:
     file_path = doc.PathName
     file_name = path2fileName(file_path,"\\")

  datestamp = str(datetime.now())
  # tabulator between data to easy import to excel schedule
  separator = "\t" 
  try:
     f = open("L:\\customToolslogs\\"+ file_name + ".log", "a")
     f.write(datestamp + separator + log_string + separator + user_name + "\n")
     f.close()
  except:
         pass

# logging currentVersion and snapshot with username to server
def versionLogger(releasedVersion,snapshot):
  from datetime import datetime
  from pyrevit import revit
  import getpass
  user_name = getpass.getuser()
  datestamp = str(datetime.now())
  # tabulator between data to easy import to excel schedule
  separator = "\t" 
  try:
     f = open("L:\\customToolslogs\\versions.log", "a")
     f.write(datestamp + separator + releasedVersion + "_" + snapshot + separator + user_name + "\n")
     f.close()
  except:
         pass

# version of CustomTools
releasedVersion = "0.5"
snapshot = "200124"