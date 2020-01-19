'''
Erases most common Type parameters values and Room parameters.
'''
# for timing------
from pyrevit.coreutils import Timer
timer = Timer()
# ----------------

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction

__title__ = 'Material &\nLine purge'
doc = __revit__.ActiveUIDocument.Document

deletedMaterials = []
idsToDelete = []
linePattern_collector = FilteredElementCollector(doc).OfClass(LinePatternElement)
for i in linePattern_collector:
	linePatternName=i.Name
	linePatternId = i.Id
	if linePatternName[0:5] == "IMPORT":
		deletedMaterials.append(linePatternName)
		idsToDelete.append(linePatternId)


t= Transaction(doc, "purge")
t.Start()

for i in idsToDelete:
	doc.Delete(i)

t.Commit()


print(len(deletedMaterials))
for i in deletedMaterials:
	print(i)