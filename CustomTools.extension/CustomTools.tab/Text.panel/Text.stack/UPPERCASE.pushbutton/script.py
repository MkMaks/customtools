"""Changes all characters in text box to Uppercase"""

__context__ = 'Text Notes'

from pyrevit import revit, coreutils

selection = revit.get_selection()

def uppercase():
    with revit.Transaction('uppercase'):
        for el in selection.elements:
            el.Text = el.Text.upper()

uppercase()