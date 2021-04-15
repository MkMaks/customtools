"""Opens *.xml file location with Keyboarrd shortcuts and run Keyboard Shortcuts command.\n
Copy file to your hardrive and click Import. Then find the downloaded file and click overwrite."""

__context__ = 'zero-doc'

import subprocess
# getting %HOMEPATH%
from os.path import expanduser
homepath = expanduser("~")


# path for common user
try:
    ksPath = homepath + "\AppData\Roaming\pyRevit\Extensions\CustomTools.extension\CustomTools.tab\Links.panel\Keyboard shortcuts.splitpushbutton\Download & set keyboard shortcuts.pushbutton\KeyboardShortcuts_davidv.xml"
    test = open(ksPath,"r")
# path for developer using git clone
except:
    ksPath = homepath + "\Documents\gitRepos\pyRevit extensions\CustomTools.extension\CustomTools.tab\Links.panel\Keyboard shortcuts.splitpushbutton\Download & set keyboard shortcuts.pushbutton\KeyboardShortcuts_davidv.xml"

subprocess.Popen(r'explorer /select, '+ksPath)
# subprocess.Popen(r'explorer /select,"U:\REVIT\Keyboard_Shortcuts\KeyboardShortcuts_davidv.xml"')


#run command keyboard Shortcuts
from Autodesk.Revit.UI import UIApplication, RevitCommandId, PostableCommand
doc = __revit__.ActiveUIDocument.Document

Command_ID=RevitCommandId.LookupPostableCommandId(PostableCommand.KeyboardShortcuts)
uiapp = UIApplication(doc.Application)
uiapp.PostCommand(Command_ID)