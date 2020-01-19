'''
Erases trash imported from AutoCAD links (Render Materials & Line Patterns)
'''
# for timing------
from pyrevit.coreutils import Timer
from pyrevit import coreutils, script
from custom_output import hmsTimer
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
	if materialNameString[0:6] == "Render":
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


output = script.get_output()

# step1
# # Line chart
# chart = output.make_line_chart()
# # Bar chart
chart = output.make_bar_chart()
# # # Bubble chart
# chart = output.make_bubble_chart()
# # # Radar chart
# chart = output.make_radar_chart()
# # # Polar chart
# chart = output.make_polar_chart()
# # # Pie chart
# chart = output.make_pie_chart()
# # Doughnut chart
# chart = output.make_doughnut_chart()

# step1a
# chart.set_style('height:300px')

chart.options.title = {'display': True,
                       'text':'Material & Line Patterns purge',
                       'fontSize': 18,
                       'fontColor': '#000',
                       'fontStyle': 'bold'}

# step2
# setting the charts x line data labels
chart.data.labels = ['PRESERVED - Native Revit Elements','DELETED  - Elements imported from DWG']

# Let's add the first dataset to the chart object
# we'll give it a name: set_a
set_a = chart.data.new_dataset('Materials')
set_b = chart.data.new_dataset('Line Patterns')
# And let's add data to it.
# These are the data for the Y axis of the graph
# The data length should match the length of data for the X axis
set_a.data = [allMaterialsCount-len(deletedMaterials), len(deletedMaterials)]
set_b.data = [allLinePatternsCount-len(deletedLinePatterns), len(deletedLinePatterns)]
# Set the color for this graph
set_a.set_color(0xFF, 0x80, 0x00, 0.7)
set_b.set_color(0x33, 0x66, 0x00, 0.7)

# step3
# Finally let's draw the chart
# chart.randomize_colors()
chart.draw()