'''
Erases all Materials & Line Patterns
'''
# for timing------
from pyrevit.coreutils import Timer
from pyrevit import coreutils
from custom_output import hmsTimer
timer = Timer()
# ----------------

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction
from Autodesk.Revit.DB import LinePatternElement

__title__ = 'All Materials & Lines Eraser'
doc = __revit__.ActiveUIDocument.Document

# FUNCTIONS
# highlights text using html string with css
def text_highligter(a):
		content = str(a)
		html_code = "<p class='elementlink'>"+content+"</p>"
		return coreutils.prepare_html_str(html_code)

idsToDelete = []
#  MATERIALS
deletedMaterials = []
material_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Materials)
for i in material_collector:
	materialName=i.LookupParameter('Name')
	materialNameString = materialName.AsString()
	materialId = i.Id
	deletedMaterials.append(materialNameString)
	idsToDelete.append(materialId)

# LINE PATTERNS
deletedLinePatterns = []
linePattern_collector = FilteredElementCollector(doc).OfClass(LinePatternElement)
for i in linePattern_collector:
	linePatternName=i.Name
	linePatternId = i.Id
	deletedLinePatterns.append(linePatternName)
	idsToDelete.append(linePatternId)

t= Transaction(doc, "All Materials and Line Patterns purge")
t.Start()

for i in idsToDelete:
	doc.Delete(i)

t.Commit()

# OUTPUT
# for timing------
endtime = timer.get_time()
print(hmsTimer(endtime))
# --------------

materialsOutput = str(len(deletedMaterials))+" Materials deleted."
print(text_highligter(materialsOutput))
for i in deletedMaterials:
	print(i)
print("\n\n")

linePatternsOutput = str(len(deletedLinePatterns))+" LinePatterns deleted."
print(text_highligter(linePatternsOutput))
for i in deletedLinePatterns:
	print(i)