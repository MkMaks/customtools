collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Lines).WhereElementIsNotElementType().ToElements()
for line in collector:
	print line.LineStyle.Name
	viewId = line.OwnerViewId
	view = doc.GetElement(viewId)
	viewName = view.Name
	print(viewName)