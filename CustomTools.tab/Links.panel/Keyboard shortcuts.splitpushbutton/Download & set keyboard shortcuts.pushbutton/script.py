"""Opens *.xml file location with Keyboarrd shortcuts and run Keyboard Shortcuts command.\n
Copy file to your hardrive and click Import. Then find the downloaded file and click overwrite."""

__context__ = 'zero-doc'

import subprocess
subprocess.Popen(r'explorer /select,"U:\REVIT\Keyboard_Shortcuts\KeyboardShortcuts_davidv.xml"')

#run command keyboard Shortcuts
from Autodesk.Revit.UI import UIApplication, RevitCommandId, PostableCommand
doc = __revit__.ActiveUIDocument.Document

Command_ID=RevitCommandId.LookupPostableCommandId(PostableCommand.KeyboardShortcuts)
uiapp = UIApplication(doc.Application)
uiapp.PostCommand(Command_ID)