"""
WIP script
"""

__title__ = 'Selection Box\nIn Linked File'
__author__ = 'David Vadkerti'
__doc__ = 'WIP - Makes Selection Box around element in linked file' \
          'You can use "Select Elements by IDs" function to select element if link is opened directly.'
__highlight__ = 'new'

from pyrevit import script

from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.UI.Selection import ObjectType

from pyrevit.framework import Math
from pyrevit import revit, DB, UI
from pyrevit import forms

curview = revit.active_view

app = __revit__.Application
uidoc = __revit__.ActiveUIDocument


def makeSectionBox(view):
    selectedElement = uidoc.Selection
    hasPickOne = selectedElement.PickObject(ObjectType.LinkedElement)
    if hasPickOne is not None:
        elementId = hasPickOne.LinkedElementId
        # find how to get linked revit document
        linkedDoc = 
        element = linkedDoc.GetElement(elementId)
        elBoundBoxXYZ =element.BoundingBox
    try:
        with revit.Transaction('Selection Box of Linked Element'):
            view.SetSectionBox(elBoundBoxXYZ)
            revit.uidoc.RefreshActiveView()
    except Exception:
        pass

if isinstance(curview, DB.View3D) and curview.IsSectionBoxActive:
    makeSectionBox(curview)
elif isinstance(curview, DB.View3D) and not curview.IsSectionBoxActive:
    forms.alert("The section box for View3D isn't active.")
else:
    forms.alert('You must be on a 3D view for this tool to work.')