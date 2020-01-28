# -*- coding: UTF-8 -*-
from pyrevit import EXEC_PARAMS
from pyrevit import forms, script

# showing of dialog box with warning
def dialogBox():
	res = forms.alert("POZOR!\n\n"
		            "Pri vytváraní nového Shared Parametru si najskôr pozrite, či už podobný parameter nie je vytvorený. Nepoužívajte diakritiku.",
					title="Project Parameters",
					footer="CustomTools Hooks",
	                options=["Zobraziť zoznam Shared Parametrov na Wiki",
	                         "Pridať Parameter",
	                         "Zrušiť"])
	if res  == "Pridať Parameter":
		EXEC_PARAMS.event_args.Cancel = False
		# logging to server
		from hooksScripts import hooksLogger
		hooksLogger("Project or Shared Parameters")
	elif res  == "Zrušiť":
		EXEC_PARAMS.event_args.Cancel = True
	elif res  == "Zobraziť zoznam Shared Parametrov na Wiki":
		EXEC_PARAMS.event_args.Cancel = True
		url = 'https://gfi.miraheze.org/wiki/Shared_parametre_pre_Revit'
		script.open_url(url)
	else:
		EXEC_PARAMS.event_args.Cancel = True

# try to find config file for people who dont want to see the hook
try:
	configFile = open("C:\\PyrevitExtensions\\CustomTools\\hooksConfig.txt","r")
	configSettingsList = (currentVersionFile.readlines())
	configSettings = str(currentVersionList)[2:-2]
	# if content not equal to zero show the dialog box
	if configSettings == "0":
		pass
	else:
		dialogBox()
# if file not found show the dialog box
except:
	dialogBox()
