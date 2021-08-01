# -*- coding: utf-8 -*-
from pyrevit.userconfig import user_config
from customOutput import def_hookLogs, def_revitBuildLogs, def_revitBuilds
from customOutput import def_massMessagePath, def_syncLogPath, def_openingLogPath, def_dashboardsPath

# version of CustomTools
releasedVersion = "0.9"
snapshot = "210801"

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
      # if parameter exists in config file
      try:
        hookLogs = user_config.CustomToolsSettings.hookLogs
      # if parameter doesnt exist in config file
      except:
        hookLogs = def_hookLogs
      f = open(hookLogs + "\\" + file_name + ".log", "a")
      # f = open("L:\\customToolslogs\\hooksLogs\\"+ file_name + ".log", "a")
    except:
      f = open("\\\\Srv2\\Z\\customToolslogs\\hooksLogs\\"+ file_name + ".log", "a")

    f.write(datestamp + separator + log_string + separator + user_name + "\n")
    f.close()
  except:
         pass

# logging currentVersion and snapshot with username to server
def versionLogger(releasedVersion,snapshot):
  from datetime import datetime
  import getpass
  from pyrevit import revit, _HostApplication
  from pyrevit import forms, script
  from stringFormating import listFromString
  user_name = getpass.getuser()
  datestamp = str(datetime.now())

  # from pyrevit import EXEC_PARAMS
  # from hooksScripts import hookTurnOff

  # showing of dialog box with warning if wrong revit build
  def dialogBox(build):
     res = forms.alert("POZOR!\n\n"
                       "Používaš zlý Revit Build! To môže poškodiť model.\n"
                       "\n"
                       "Správne Revit Buildy sú " + " alebo ".join(company_build),
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
  # if parameter exists in config file
  try:
    company_build = listFromString(user_config.CustomToolsSettings.revitBuilds)
  # if parameter doesnt exist in config file
  except:
    company_build = listFromString(def_revitBuilds)

  # checking if revit build is inline with company standard
  if build not in company_build:
    dialogBox(build)

  # tabulator between data to easy import to excel schedule
  separator = "\t" 
  try:
    try:
      # if parameter exists in config file
      try:
        revitBuildLogs = user_config.CustomToolsSettings.revitBuildLogs
        # f = open("L:\\customToolslogs\\versions.log", "a")
       # if parameter doesnt exist in config file
      except:
        revitBuildLogs = def_revitBuildLogs
      f = open(revitBuildLogs, "a")
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


# HOOKS GUI VALUES
# ct_footer="CustomTools Hooks"

# # CAD file import
# cfi_hook_name = "CAD file import"
# cfi_main_message = "POZOR!\n\nImportovať CAD súbory by si mal len výnimočne.\nNikdy neimportuj CAD priamo do modelu, ale do čistého RVT súboru.\n\n si si istý, že vieš, čo robíš?"
# cfi_title="Import CAD file"
# cfi_options=["Importovať",
#          "Zrušiť",
#          "Viac info o Importovaní CAD súborov"]
# cfi_url = 'https://gfi.miraheze.org/wiki/Postupy,_ktor%C3%BDm_je_potrebn%C3%A9_sa_vyhn%C3%BA%C5%A5_-_Revit#Importovanie_DWG'