# -*- coding: UTF-8 -*-

from pyrevit import EXEC_PARAMS
from pyrevit import forms, script
from hooksScripts import hookTurnOff

doc = __revit__.ActiveUIDocument.Document

def dialogBox():
  res = forms.alert("POZOR!\n\n"
                    "CAD súbory môžu poškodiť revitový model.\n"
                    "Spravil si všetko podľa návodu nižšie?",
                    title="Link CAD file",
                    footer="CustomTools Hooks",
                    options=["Link CAD",
                             "Zrušiť",
                             "Viac info o Linkovaní CAD súborov"])
  if res  == "Link CAD":
      EXEC_PARAMS.event_args.Cancel = False
      # logging to server
      from hooksScripts import hooksLogger
      hooksLogger("Link CAD file",doc)
  elif res  == "Zrušiť":
      EXEC_PARAMS.event_args.Cancel = True
  elif res  == "Viac info o Linkovaní CAD súborov":
      EXEC_PARAMS.event_args.Cancel = True
      url = 'https://gfi.miraheze.org/wiki/Linknutie_DWG_s%C3%BAboru_do_Revitu'
      script.open_url(url)
  else:
      EXEC_PARAMS.event_args.Cancel = True

# try to find config file for people who dont want to see the hook
hookTurnOff(dialogBox,3)