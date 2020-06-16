# -*- coding: UTF-8 -*-
from hooksScripts import versionLogger, releasedVersion, snapshot

versionLogger(releasedVersion,snapshot)

# uncomment if settings changes are needed

import os
import subprocess
try:
    # running CustomToolsUpdater.cmd script at:
    # %AppData%\\Roaming\\pyRevit\\Extensions\\CustomTools.extension\\updater\\settingsUpdater.cmd
    appdataPath = os.getenv('APPDATA')
    updaterPath = appdataPath + '\\pyRevit\\Extensions\\CustomTools.extension\\updater\\settingsUpdater.cmd'
    p = subprocess.Popen([updaterPath])
except:
    pass