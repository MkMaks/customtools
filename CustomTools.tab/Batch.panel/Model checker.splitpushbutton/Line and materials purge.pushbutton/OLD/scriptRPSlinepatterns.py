# material_collector = FilteredElementCollector(doc).OfCategoryId(ElementId)
material_collector = FilteredElementCollector(doc).OfCategory(BuitInCategory(OST_lines))
for i in material_collector:
	materialName=i.LookupParameter('Name')
	materialNameString = materialName.AsString()
	print(materialNameString)
	materialId = i.Id