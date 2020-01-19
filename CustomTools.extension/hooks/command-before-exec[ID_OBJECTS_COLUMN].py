# -*- coding: UTF-8 -*-

from pyrevit import EXEC_PARAMS
from pyrevit import forms, script

res = forms.alert("POZOR!\n\n"
                  "Všetky nosné stĺpy by mali byť vymodelované ako Structural a nie ako Architectural Column.\n"
                  "- Architectural Columns sa nezobrazia v statickom modeli.\n"
                  "- v budúcnosti bude musieť niekto po tebe upraviť všetky stĺpy na Structural",
                  title="Architectural column",                  
                  footer="CustomTools Hooks",
                  options=["Vytvoriť aj napriek tomu Architectural Column",
                           "Zrušiť",
                           "Viac info o Architectural Columns"])
if res  == "Vytvoriť aj napriek tomu Architectural Column":
   EXEC_PARAMS.event_args.Cancel = False
   # logging to server
   from hooksScripts import hooksLogger
   hooksLogger("Architecural Column")

elif res  == "Zrušiť":
   EXEC_PARAMS.event_args.Cancel = True
elif res  == "Viac info o Architectural Columns":
   EXEC_PARAMS.event_args.Cancel = True
   url = 'https://gfi.miraheze.org/wiki/Postupy,_ktorým_je_potrebné_sa_vyhnúť_-_Revit'
   script.open_url(url)
else:
   EXEC_PARAMS.event_args.Cancel = True