"""downloads *.xml file with Keyboarrd shortcuts and run Keyboard Shortcuts command.\n
You need to click Import then find the downloaded file and click overwrite."""
from pyrevit import script


__context__ = 'zero-doc'


# url = 'https://www.dropbox.com/s/ltryffudk24q48a/KeyboardShortcuts_davidv.zip?dl=0'
url = 'http://dynamohelp.atwebpages.com/support_files/KeyboardShortcuts_davidv.7z'

script.open_url(url)

#run command keyboard Shortcuts
from Autodesk.Revit.UI import UIApplication, RevitCommandId, PostableCommand
doc = __revit__.ActiveUIDocument.Document

Command_ID=RevitCommandId.LookupPostableCommandId(PostableCommand.KeyboardShortcuts)
uiapp = UIApplication(doc.Application)
uiapp.PostCommand(Command_ID)