# -*- coding: UTF-8 -*-
"""Detail Group Schedule.
Lists all Detail Groups with links to Owner Views.
"""

__title__ = 'Import Report'
__doc__ = 'Drag and drop interactive HTML file saved from pyRevit script output. Makes element links active.'
__helpurl__ = 'https://youtu.be/0lXwqbIrDiY'
__context__ = 'zero-doc'

# print("log files are here:")
# print("L:\\customToolslogs")

import subprocess
subprocess.Popen(r'explorer /select,"L:\_customToolsReports\doNotErase-pointer"')

print("Drag and drop interactive HTML file saved from pyRevit script output into this window.")
print("Makes element links active.")