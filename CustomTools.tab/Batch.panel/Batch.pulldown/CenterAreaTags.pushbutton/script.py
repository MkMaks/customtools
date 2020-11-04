from pyrevit import revit

__context__ = 'Area Tags'
area_tags = revit.get_selection()

activeview = revit.active_view
with revit.Transaction("Room Tags Centered"):
    for area_tag in area_tags:
        area_tag_pt = area_tag.Location.Point
        area = area_tag.Area
        bbox = area.BoundingBox[activeview]
        area_pt = (bbox.Min + bbox.Max)/2
        translation = area_pt - area_tag_pt
        area_tag.Location.Move(translation)