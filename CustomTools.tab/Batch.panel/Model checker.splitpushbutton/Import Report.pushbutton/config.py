# -*- coding: utf-8 -*- 

# import subprocess
# subprocess.Popen(r'explorer /select,"L:\customToolslogs\doNotErase-pointer"')
from pyrevit import script

output = script.get_output()

url = 'L:\\customToolslogs\\'
output.open_page(url)