# -*- coding: utf-8 -*-
__title__ = 'UID getter'
__doc__ = """Get Unique IDs of selected objects and copies it to clipboard.
You need to make selection to make command active."""


__context__ = 'Selection'

from pyrevit import revit
from System.Windows.Forms import Clipboard

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *


element_collector = revit.get_selection()
UniqueIds = [i.UniqueId for i in element_collector]
stripedUIDstring =""

# list to long string with commas
for i in UniqueIds:
	stripedUIDstring = stripedUIDstring + i + ", "

# removing comma after last Unique ID
stripedUIDstring = stripedUIDstring[:-2]

#copy to clipboard
a = "{}".format(stripedUIDstring)
Clipboard.SetText(a)

print("List of Unique IDs for selected elements:\n{}".format(stripedUIDstring))
print("\nVýstup bol nakopírovaný do schránky.")