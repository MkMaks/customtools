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

if twoD:
  pass
else:
  res = forms.alert("POZOR!\n\n"
                    "Linkuješ CAD súbor do 3D!",
                    title="Link CAD file in 3D",
                    footer="CustomTools Hooks",
                    options=["Zrušiť",
                             "OK, potrebujem DWG v 3D",
                             "Viac info o Linkovaní CAD súborov"])
  if res  == "OK, potrebujem DWG v 3D":
      # logging to server
      from hooksScripts import hooksLogger
      hooksLogger("Link DWG in 3D")
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