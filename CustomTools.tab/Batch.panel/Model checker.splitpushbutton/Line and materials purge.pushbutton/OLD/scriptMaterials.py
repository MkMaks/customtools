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
material_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Materials)
for i in material_collector:
	materialName=i.LookupParameter('Name')
	materialNameString = materialName.AsString()
	materialId = i.Id
	if materialNameString[0:6] == "Render":
		deletedMaterials.append(materialNameString)
		idsToDelete.append(materialId)


t= Transaction(doc, "purge")
t.Start()

for i in idsToDelete:
	doc.Delete(i)

t.Commit()


print(len(deletedMaterials))
for i in deletedMaterials:
	print(i)