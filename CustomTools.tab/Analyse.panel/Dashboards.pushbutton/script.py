# -*- coding: UTF-8 -*-

__title__ = 'Dashboards'
__doc__ = '''Power BI Dashboards for analysing RVT model quality, CustomTools Hooks logs, opening and sync times, revit builds and more.

You need to install Power BI Desktop application first.

SHIFT+Click - open folder with templates of Power BI dashboards'''
__author__ = 'David Vadkerti'
__helpurl__ = 'https://gfi.miraheze.org/wiki/Power_BI'
__context__ = 'zero-doc'

# import subprocess
# subprocess.Popen(r'explorer /select,"L:\powerBI\doNotErase-pointer"')
from pyrevit import script
from pyrevit.userconfig import user_config
from customOutput import ct_icon, def_dashboardsPath

output = script.get_output()
# seting CustomTools icon
ct_icon(output)

# if parameter exists in config file
try:
	url = user_config.CustomToolsSettings.dashboardsPath
# if parameter doesnt exist in config file
except:	
	url = def_dashboardsPath
# url = '\\\\Srv2\\Z\\powerBI\\'


output.open_page(url)