"""Manual instant update of CustomTools without system restart.
"""

__title__ = 'Update Now!'
__context__ = 'zero-doc'
__doc__ = 'Manual instant update of CustomTools without system restart.' \
          'CustomTools checks for updates on system startup.'

import os
import subprocess
from pyrevit import script
from pyrevit.loader import sessionmgr
from pyrevit.loader import sessioninfo
try:
    # running CustomToolsUpdater.cmd script at:
    # %AppData%\\Roaming\\pyRevit\\Extensions\\CustomTools.extension\\updater\\CustomToolsUpdater.cmd
    appdataPath = os.getenv('APPDATA')
    updaterPath = appdataPath + '\\pyRevit\\Extensions\\CustomTools.extension\\updater\\CustomToolsUpdater.cmd'
    p = subprocess.Popen([updaterPath])

    # reload pyRevit
    logger = script.get_logger()
    results = script.get_results()
    # re-load pyrevit session.
    logger.info('Reloading....')
    sessionmgr.reload_pyrevit()

    results.newsession = sessioninfo.get_session_uuid()
except:
    print("Something went wrong. Install manualy at %AppData%\\Roaming\\pyRevit\\Extensions\\CustomTools.extension\\updater\\CustomToolsUpdater.cmd")