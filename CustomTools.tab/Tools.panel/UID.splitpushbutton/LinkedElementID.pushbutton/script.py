"""
Gets ID of element in a Revit link and copies it to the clipboard. You can use 'Select Elements by IDs' function to select element if link is opened directly.
"""

__title__ = 'ID Of Element\nIn Linked File'
__author__ = 'David Vadkerti'
__doc__ = 'Gets ID of element in a Revit link and copies it to the clipboard.' \
          'You can use "Select Elements by IDs" function to select element if link is opened directly.'
__help_url__ = 'https://youtu.be/fG-dg7D8U8M'

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
TaskDialog.Show("Element Id","Element Id" + str(id)+ " was copied to clipboard.")