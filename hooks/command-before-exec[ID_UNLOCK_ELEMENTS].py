# -*- coding: UTF-8 -*-

from pyrevit import EXEC_PARAMS
from pyrevit import forms, script

res = forms.alert("POZOR!\n\n"
	              "Chceš naozaj odpinovať tento element?\n"
                  "Elementy sú väčšinou zapinované kvôli tomu, aby nimi náhodou niekto nepohol.\n\n"
                  "Chceš to naozaj urobiť?",
                  title="Unpin element",
                  footer="CustomTools Hooks",
                  options=["Unpin",
                           "Zrušiť",
                           "Viac info o Pin/Unpin"])
if res  == "Unpin":
	EXEC_PARAMS.event_args.Cancel = False
elif res  == "Zrušiť":
	EXEC_PARAMS.event_args.Cancel = True
elif res  == "Viac info o Pin/Unpin":
	EXEC_PARAMS.event_args.Cancel = True
	url = 'https://gfi.miraheze.org/w/index.php?search=unpin&title=Špeciálne%3AHľadanie&go=Ísť+na'
	script.open_url(url)
else:
	EXEC_PARAMS.event_args.Cancel = True