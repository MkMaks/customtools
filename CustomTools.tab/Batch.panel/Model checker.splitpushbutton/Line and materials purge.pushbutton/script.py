'''
Erases trash imported from AutoCAD links (Render Materials & Line Patterns)
'''
# for timing------
from pyrevit.coreutils import Timer
from pyrevit import coreutils, script
from pyrevit.output import charts
from customOutput import hmsTimer, ct_icon
timer = Timer()
# ----------------

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction
from Autodesk.Revit.DB import LinePatternElement

__title__ = 'Material &\nLine purge'
doc = __revit__.ActiveUIDocument.Document

# FUNCTIONS
# highlights text using html string with css
def text_highligter(a):
		content = str(a)
		html_code = "<p class='elementlink'>"+content+"</p>"
		return coreutils.prepare_html_str(html_code)

idsToDelete = []
#  MATERIALS
allMaterialsCount = 0
deletedMaterials = []
material_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Materials)
for i in material_collector:
	materialName=i.LookupParameter('Name')
	materialNameString = materialName.AsString()
	materialId = i.Id
	allMaterialsCount += 1
	# filtering out english and czech render materials from dwg links
	materialStart = materialNameString[0:6]
	if materialStart == "Render" or materialStart == "Rendro":
		deletedMaterials.append(materialNameString)
		idsToDelete.append(materialId)

# LINE PATTERNS
allLinePatternsCount = 0
deletedLinePatterns = []
linePattern_collector = FilteredElementCollector(doc).OfClass(LinePatternElement)
for i in linePattern_collector:
	linePatternName=i.Name
	linePatternId = i.Id
	allLinePatternsCount += 1
	if linePatternName[0:6] == "IMPORT":
		deletedLinePatterns.append(linePatternName)
		idsToDelete.append(linePatternId)

t= Transaction(doc, "Materials and Line Patterns purge")
t.Start()

for i in idsToDelete:
	doc.Delete(i)

t.Commit()

# OUTPUT
# for timing------
endtime = timer.get_time()
print(hmsTimer(endtime))
# endtimeRound = round(endtime*1000)/1000
# print("\nTime "+str(endtimeRound)+" seconds.")
# --------------

materialsOutput = str(len(deletedMaterials))+" Materials deleted."
print(text_highligter(materialsOutput))
# for i in deletedMaterials:
# 	print(i)
# print("\n\n")

linePatternsOutput = str(len(deletedLinePatterns))+" LinePatterns deleted."
print(text_highligter(linePatternsOutput))
# for i in deletedLinePatterns:
# 	print(i)

# CHART
output = script.get_output()
# changing icon
ct_icon(output)

chart = output.make_chart(version='2.8.0')
chart.type = charts.BAR_CHART

chart.options.title = {'display': True,
                       'text':'Material & Line Patterns purge',
                       'fontSize': 18,
                       'fontColor': '#000',
                       'fontStyle': 'bold'}

# labels
chart.data.labels = ['PRESERVED - Native Revit Elements','DELETED  - Elements imported from DWG']

# datasets
set_a = chart.data.new_dataset('Materials')
set_b = chart.data.new_dataset('Line Patterns')
# data
set_a.data = [allMaterialsCount-len(deletedMaterials), len(deletedMaterials)]
set_b.data = [allLinePatternsCount-len(deletedLinePatterns), len(deletedLinePatterns)]
# fixed colors
set_a.set_color(0xFF, 0x80, 0x00, 0.7)
set_b.set_color(0x33, 0x66, 0x00, 0.7)

chart.draw()