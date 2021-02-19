# -*- coding: utf-8 -*- 

# import subprocess
# subprocess.Popen(r'explorer /select,"L:\customToolslogs\doNotErase-pointer"')
from pyrevit import script

output = script.get_output()
url = '\\\\Srv2\\Z\\_customToolsReports\\'
output.open_page(url)