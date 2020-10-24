from pyrevit import revit

__context__ = 'Room Tags'
room_tags = revit.get_selection()

activeview = revit.active_view
with revit.Transaction("Room Tags Centered"):
    for room_tag in room_tags:
        room_tag_pt = room_tag.Location.Point
        room = room_tag.Room
        bbox = room.BoundingBox[activeview]
        room_pt = (bbox.Min + bbox.Max)/2
        translation = room_pt - room_tag_pt
        room_tag.Location.Move(translation)