# -*- coding: utf-8 -*-

# version of CustomTools
releasedVersion = "0.8"
snapshot = "210121"

# logging to server
def hooksLogger(log_string, doc):
  from datetime import datetime
  from pyrevit import revit
  
  # doc = __revit__.ActiveUIDocument.Document
  
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
     central_path = revit.query.get_central_path(doc)
     # central_path = revit.query.get_central_path(doc=revit.doc)
     file_name = path2fileName(central_path,"/")
  # non workshared file
  except:
     file_path = doc.PathName
     file_name = path2fileName(file_path,"\\")

  datestamp = str(datetime.now())
  # tabulator between data to easy import to excel schedule
  separator = "\t" 
  try:
    try:
      f = open("L:\\customToolslogs\\hooksLogs\\"+ file_name + ".log", "a")
    except:
      f = open("\\\\Srv2\\Z\\customToolslogs\\hooksLogs\\"+ file_name + ".log", "a")

    f.write(datestamp + separator + log_string + separator + user_name + "\n")
    f.close()
  except:
         pass

# logging currentVersion and snapshot with username to server
def versionLogger(releasedVersion,snapshot):
  from datetime import datetime
  from pyrevit import revit, _HostApplication
  import getpass
  user_name = getpass.getuser()
  datestamp = str(datetime.now())

  # from pyrevit import EXEC_PARAMS
  from pyrevit import forms, script
  # from hooksScripts import hookTurnOff

  # showing of dialog box with warning if wrong revit build
  def dialogBox(build):
     res = forms.alert("POZOR!\n\n"
                       "Používaš zlý Revit Build! To môže poškodiť model.\n"
                       "\n"
                       "Správny Revit Build je " + company_build,
                       title="Revit Build",
                       footer="CustomTools Hooks",
                       options=["Chcem len otvoriť súbor bez synchronizácie",
                                "Ako môžem tento problém opraviť?"])
     if res  == "Chcem len otvoriť súbor bez synchronizácie":
        pass
     if res  == "Ako môžem tento problém opraviť?":
        url = 'https://gfi.miraheze.org/wiki/Aktualizácia_Revitu'
        script.open_url(url)
     else:
      pass

  hostapp = _HostApplication()
  build = hostapp.build
  # company standard build
  company_build = "20200826_1250(x64)"
  # checking if revit build is inline with company standard
  if build != company_build:
    dialogBox(build)

  # tabulator between data to easy import to excel schedule
  separator = "\t" 
  try:
    try:
      f = open("L:\\customToolslogs\\versions.log", "a")
    except:
      f = open("\\\\Srv\\Z\\customToolslogs\\versions.log", "a")  
    f.write(datestamp + separator + releasedVersion + "_" + snapshot + separator + user_name + separator + build + "\n")
    f.close()
  except:
         pass

# read number from config file, if not zero run function that show f.e. dialog box
def hookTurnOff(func, number, *args, **kwargs):
  try:
    configFile = open("C:\\pyRevitExtensions\\CustomTools\\hooksConfig.txt","r")
    # first or other item of file content
    index = number - 1
    configSetting = (configFile.readline())[index]
    # if first item of file content not equal to zero show the dialog box
    if configSetting == "0":
      pass
    else:
      func(*args, **kwargs)
  except:
    func(*args, **kwargs)