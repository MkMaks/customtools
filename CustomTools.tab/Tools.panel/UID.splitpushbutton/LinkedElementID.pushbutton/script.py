"""
Gets ID of element in a Revit link and copies it to the clipboard. You can use 'Select Elements by IDs' function to select element if link is opened directly.
"""

__title__ = 'Get ID Of Element In Linked File'

from pyrevit import script

from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.UI.Selection import ObjectType

app = __revit__.Application
uidoc = __revit__.ActiveUIDocument

def selectElemInLink():
    selectedElement = uidoc.Selection
    hasPickOne = selectedElement.PickObject(ObjectType.LinkedElement)
    if hasPickOne is not None:
        return hasPickOne.LinkedElementId.IntegerValue

id = selectElemInLink()
#Copy id to clipboard
script.clipboard_copy(str(id))
TaskDialog.Show("Id",str(id))