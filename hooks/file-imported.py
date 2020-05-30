# -*- coding: UTF-8 -*-

from pyrevit import EXEC_PARAMS
from pyrevit import forms, script, revit
from Autodesk.Revit.DB.Document import GetElement

# pylint: skip-file
import os.path as op
from pyrevit import script

cadLinkId = __eventargs__.ImportedInstanceId
doc = __eventargs__.Document
cadLinkElement = doc.GetElement(cadLinkId)
twoD = cadLinkElement.ViewSpecific
docName = doc.PathName
fileExtension = docName[-3:]

# if ViewSpecific or not revit project
# because imports in revit families doesn't have Viewspecific Yes Value
if twoD or fileExtension!="rvt":
  pass
else:
  res = forms.alert("POZOR!\n\n"
                    "Nezašrktol si možnosť 'Current View Only'.\n"
                    "Tým pádom linkuješ CAD súbor do 3D!",
                    title="Link CAD file in 3D",
                    footer="CustomTools Hooks",
                    options=["Zrušiť",
                             "OK, potrebujem DWG v 3D",
                             "Viac info o Linkovaní CAD súborov"])
  if res  == "OK, potrebujem DWG v 3D":
      pass
      # logging to server - cannot access active document
      from hooksScripts import hooksLogger
      hooksLogger("Link DWG in 3D", doc)
  elif res  == "Zrušiť":
      #run command UNDO
      from Autodesk.Revit.UI import UIApplication, RevitCommandId, PostableCommand

      Command_ID=RevitCommandId.LookupPostableCommandId(PostableCommand.Undo)
      uiapp = UIApplication(doc.Application)
      uiapp.PostCommand(Command_ID)
  elif res  == "Viac info o Linkovaní CAD súborov":
      url = 'https://gfi.miraheze.org/wiki/Linknutie_DWG_s%C3%BAboru_do_Revitu#HLAVN.C3.89_Z.C3.81SADY'
      script.open_url(url)
  else:
      pass