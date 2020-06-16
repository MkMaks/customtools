# -*- coding: UTF-8 -*-
from hooksScripts import versionLogger, releasedVersion, snapshot

versionLogger(releasedVersion,snapshot)

import os
import subprocess
try:
    # running CustomToolsUpdater.cmd script at:
    # %AppData%\\Roaming\\pyRevit\\Extensions\\CustomTools.extension\\updater\\CustomToolsUpdater.cmd
    appdataPath = os.getenv('APPDATA')
    updaterPath = appdataPath + '\\pyRevit\\Extensions\\CustomTools.extension\\updater\\CustomToolsUpdater.cmd'
    p = subprocess.Popen([updaterPath])
except:
    pass

# import os
# import subprocess

# # running script InitUpdate.cmd:
# appdataPath = os.getenv('APPDATA')
# # updaterPath = appdataPath + '\\pyRevit\\Extensions\\CustomTools.extension\\hooks\\InitUpdate.cmd'
# updaterPath = '.\\InitUpdate.cmd'
# p = subprocess.Popen([updaterPath])