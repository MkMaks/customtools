# -*- coding: UTF-8 -*-

from pyrevit import EXEC_PARAMS
from pyrevit import forms, script

res = forms.alert("POZOR!\n\n"
	            "Pri vytváraní nového Shared Parametru si najskôr pozrite, či už podobný parameter nie je vytvorený.",
				title="Shared Parameters",
				footer="CustomTools Hooks",
                options=["Zobraziť zoznam Shared Parametrov na Wiki",
                         "Pridať Shared Parameter",
                         "Zrušiť"])
if res  == "Pridať Shared Parameter":
	EXEC_PARAMS.event_args.Cancel = False
	# logging to server
	from hooksScripts import hooksLogger
	hooksLogger("Change Shared Parameters")
elif res  == "Zrušiť":
	EXEC_PARAMS.event_args.Cancel = True
elif res  == "Zobraziť zoznam Shared Parametrov na Wiki":
	EXEC_PARAMS.event_args.Cancel = True
	url = 'https://gfi.miraheze.org/wiki/Shared_parametre_pre_Revit'
	script.open_url(url)
else:
	EXEC_PARAMS.event_args.Cancel = True