# -*- coding: UTF-8 -*-\n"
from pyrevit import EXEC_PARAMS
from pyrevit import forms, script

doc = __revit__.ActiveUIDocument.Document

res = forms.alert("POZOR!\n\n"
                  "In Place Families by mali byť použité len vo výnimočných prípadoch, "
                  "keďže majú oproti Loadable Families veľa nevýhod: \n"
                  " - problematické vykazovanie\n"
                  " - nemajú identifikáciu o levele, na ktorom sú umiestnené\n"
                  " - pri skopírovaní prvku vzniká nový nezávislý originál\n"
                  " - nemožnosť modelovať parametricky\n\n"
                  "Chceš naozaj vytvoriť In Place Family?",
                  options=["Vytvoriť",
                           "Zrušiť",
                           "Viac info o In Place Families"],
                  title="In Place Family",
                  footer="CustomTools Hooks")
if res  == "Vytvoriť":
   EXEC_PARAMS.event_args.Cancel = False
   # logging to server
   from hooksScripts import hooksLogger
   hooksLogger("Inplace Component", doc)

elif res  == "Zrušiť":
   EXEC_PARAMS.event_args.Cancel = True
elif res  == "Viac info o In Place Families":
   EXEC_PARAMS.event_args.Cancel = True
   url = 'https://gfi.miraheze.org/wiki/In-place_Families'
   script.open_url(url)
else:
   EXEC_PARAMS.event_args.Cancel = True