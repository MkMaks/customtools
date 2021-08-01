# -*- coding: UTF-8 -*-
from pyrevit.userconfig import user_config
from hooksScripts import versionLogger, releasedVersion, snapshot
from customOutput import ct_icon, mass_message_url

# CustomTools update at revit startup
import os
import subprocess
try:
    appdataPath = os.getenv('APPDATA')
    # replacing CustomToolsUpdater.cmd file for new one
    # running InitUpdate.cmd script at:
    # %AppData%\\Roaming\\pyRevit\\Extensions\\CustomTools.extension\\hooks\\InitUpdate.cmd
    newCTupdatePath = appdataPath + '\\pyRevit\\Extensions\\CustomTools.extension\\hooks\\InitUpdate.cmd'
    u = subprocess.Popen([newCTupdatePath])

    # running CustomToolsUpdater.cmd script at:
    # %AppData%\\Roaming\\pyRevit\\Extensions\\CustomTools.extension\\updater\\CustomToolsUpdater.cmd
    updaterPath = appdataPath + '\\pyRevit\\Extensions\\CustomTools.extension\\updater\\CustomToolsUpdater.cmd'
    p = subprocess.Popen([updaterPath])
except:
    pass

versionLogger(releasedVersion,snapshot)

"""TEASER."""
#prints heading and links offline version of mass message
from pyrevit import script, coreutils
from os import path
output = script.get_output()
output.set_height(700)
output.set_title("Mass Message")
# changing icon
ct_icon(output)


# # server version of massmessage
# # if parameter exists in config file
# try:
#     url = user_config.CustomToolsSettings.massMessagePath
# # if parameter doesnt exist in config file
# except:
#     url = def_massMessagePath

# # url = "L:\\_i\\CTmassMessage\\mass_message.html"
# url_unc = "\\\\Srv\\Z\\_i\\CTmassMessage\\mass_message.html"
# if path.exists(url):
#     # output.open_url(url)
#     output.open_page(url)
# elif path.exists(url_unc):
#     output.open_page(url_unc)

# server version of massmessage
output.open_page(mass_message_url(output))