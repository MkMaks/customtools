"""Manual instant update of CustomTools without system restart.
"""

__title__ = 'Update Now!'
__context__ = 'zero-doc'
__doc__ = 'Manual instant update of CustomTools without system restart.' \
          'Click Reload button after installation.' \
          'CustomTools checks for updates on system startup.'
__highlight__ = 'new'

# import getpass
# username = getpass.getuser()
# print(username)

import subprocess
# running CustomToolsUpdater.cmd script at:
# C:\Users\pxls\Documents\customtools\updater\CustomToolsUpdater.cmd
p = subprocess.Popen(['..\\..\\..\\..\\updater\\CustomToolsUpdater.cmd'])