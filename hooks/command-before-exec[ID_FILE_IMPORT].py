# -*- coding: UTF-8 -*-

from pyrevit import EXEC_PARAMS
from pyrevit import forms, script

doc = __revit__.ActiveUIDocument.Document
docName = doc.PathName
fileExtension = docName[-3:]

# for not showing the hook in families - not saved families have no extension
if fileExtension == "rvt" or fileExtension == "rte":
   res = forms.alert("POZOR!\n\n"
                    "Importovať CAD súbory by si mal len výnimočne.\n"
                     "Nikdy neimportuj CAD priamo do modelu, ale do čistého RVT súboru.\n\n"
                     "Si si istý, že vieš, čo robíš?",
                     title="Import CAD file",
                     footer="CustomTools Hooks",
                     options=["Importovať",
                              "Zrušiť",
                              "Viac info o Importovaní CAD súborov"])

   if res  == "Importovať":
      EXEC_PARAMS.event_args.Cancel = False
      # logging to server
      from hooksScripts import hooksLogger
      hooksLogger("CAD file import", doc)

   elif res  == "Zrušiť":
      EXEC_PARAMS.event_args.Cancel = True
   elif res  == "Viac info o Importovaní CAD súborov":
      EXEC_PARAMS.event_args.Cancel = True
      url = 'https://gfi.miraheze.org/wiki/Postupy,_ktor%C3%BDm_je_potrebn%C3%A9_sa_vyhn%C3%BA%C5%A5_-_Revit#Importovanie_DWG'
      script.open_url(url)
   else:
      EXEC_PARAMS.event_args.Cancel = True