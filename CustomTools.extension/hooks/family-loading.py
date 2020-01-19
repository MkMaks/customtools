# -*- coding: UTF-8 -*-
from pyrevit import EXEC_PARAMS
from pyrevit import forms, script

import os.path as op

fam_path = __eventargs__.FamilyPath
fam_name = __eventargs__.FamilyName
famSize = op.getsize(fam_path + fam_name + ".rfa")

# checking if family is larger than 1 megabyte
if famSize > 1048576:
   res = forms.alert("POZOR!\n\n"
                    "Family by mala mať veľkosť pod 1 MB.\n"
                     "Pred naloadovaním si vždy skontroluj veľkosť súboru.\n\n"
                     "Nie Family príliš detailne vymodelovaná?",
                     title="Load Family",
                     footer="CustomTools Hooks",
                     options=["Zrušiť",
                              "Naloadovať",
                              "Viac info o Families"])
   if res  == "Naloadovať":
      pass
      # logging to server
      # from hooksScripts import hooksLogger
      # hooksLogger("Family loading over 1 MB")
   elif res  == "Zrušiť":
      EXEC_PARAMS.event_args.Cancel()
   elif res  == "Viac info o Families":
      url = 'https://gfi.miraheze.org/wiki/Loadable_Families#Ve.C4.BEkos.C5.A5_Family'
      script.open_url(url)
      EXEC_PARAMS.event_args.Cancel()
   else:
      EXEC_PARAMS.event_args.Cancel()
else:
   pass