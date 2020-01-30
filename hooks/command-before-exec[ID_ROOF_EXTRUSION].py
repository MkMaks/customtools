# -*- coding: UTF-8 -*-

from pyrevit import EXEC_PARAMS
from pyrevit import forms, script

res = forms.alert("POZOR!\n\n"
                  "Roof By Extrusion by sa mali používať len výnimočne.\n"
                  "Ak potrebuješ spraviť strechu v spáde, použi Floor a nastav spád.\n"
                  "Strechám vymodelovaným ako Roof by Extrusion sa nedá upraviť pôdorysný obrys inak ako Voidom.",
                  title="Roof by Extrusion",
                  footer="CustomTools Hooks",
                  options=["Vytvoriť Roof by Extrusion",
                           "Zrušiť",
                           "Viac info o Roof by Extrusion"])
if res  == "Vytvoriť Roof by Extrusion":
   EXEC_PARAMS.event_args.Cancel = False
   # logging to server
   from hooksScripts import hooksLogger
   hooksLogger("Roof by Extrusion")
elif res  == "Zrušiť":
   EXEC_PARAMS.event_args.Cancel = True
elif res  == "Viac info o Roof by Extrusion":
   EXEC_PARAMS.event_args.Cancel = True
   url = 'https://gfi.miraheze.org/wiki/Postupy,_ktor%C3%BDm_je_potrebn%C3%A9_sa_vyhn%C3%BA%C5%A5_-_Revit#Roofs'
   script.open_url(url)
else:
   EXEC_PARAMS.event_args.Cancel = True