# -*- coding: UTF-8 -*-

__title__ = 'Import Report'
__doc__ = 'Drag and drop interactive HTML file saved from pyRevit script output. Makes element links active.'
__helpurl__ = 'https://youtu.be/0lXwqbIrDiY'
__context__ = 'zero-doc'

# print("log files are here:")
# print("L:\\customToolslogs")

import subprocess
subprocess.Popen(r'explorer /select,"L:\_customToolsReports\doNotErase-pointer"')

# heading
from pyrevit import output, script
output = script.get_output()
output.print_md("## Drag and drop interactive HTML file saved from pyRevit script output into this window.")

print("Element links in  HTML files will be working exclusively in this window.")
print("If you are experiencing any formating glitches use 'ModelChecker >>> Fix Report Visual Style' feature of CustomTools.")