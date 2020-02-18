"""Manual instant update of CustomTools without system restart.
"""

__title__ = 'Update Now!'
__context__ = 'zero-doc'
__doc__ = 'Manual instant update of CustomTools without system restart.' \
          'Click Reload button after installation.' \
          'CustomTools checks for updates on system startup.'

import os
import subprocess
try:
	# running CustomToolsUpdater.cmd script at:
	# %AppData%\\Roaming\\pyRevit\\Extensions\\CustomTools.extension\\updater\\CustomToolsUpdater.cmd
	appdataPath = os.getenv('APPDATA')
	updaterPath = appdataPath + '\\pyRevit\\Extensions\\CustomTools.extension\\updater\\CustomToolsUpdater.cmd'
	p = subprocess.Popen([updaterPath])
except:
	print("Something went wrong. Install manualy at %AppData%\\Roaming\\pyRevit\\Extensions\\CustomTools.extension\\updater\\CustomToolsUpdater.cmd")