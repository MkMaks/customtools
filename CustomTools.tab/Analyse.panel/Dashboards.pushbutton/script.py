# -*- coding: UTF-8 -*-

__title__ = 'Dashboards'
__doc__ = '''Power BI Dashboards for analysing RVT model quality, CustomTools Hooks logs, opening and sync times, revit builds and more.

You need to install Power BI Desktop application first.'''
__author__ = 'David Vadkerti'
__helpurl__ = 'https://gfi.miraheze.org/wiki/Power_BI'
__context__ = 'zero-doc'

# import subprocess
# subprocess.Popen(r'explorer /select,"L:\powerBI\doNotErase-pointer"')
from pyrevit import script
from customOutput import ct_icon

output = script.get_output()
# seting CustomTools icon
ct_icon(output)

url = 'L:\\powerBI\\'
# url = '\\\\Srv2\\Z\\powerBI\\'


output.open_page(url)
