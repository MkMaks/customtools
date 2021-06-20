from pyrevit import revit, UI
from pyrevit import script

logger = script.get_logger()

__context__ = 'selection'

selection = revit.get_selection()
selected_cat_ids = []
for element in selection:
    # list of unique category IDs
    if element.Category.Id not in selected_cat_ids:
        selected_cat_ids.append(element.Category.Id.ToString())

class PickByCategorySelectionFilter(UI.Selection.ISelectionFilter):
    """Selection filter implementation"""
    def __init__(self, cat_options):
        self.cat_options = cat_options

    def AllowElement(self, element):
        """is element in category list (is it listed to be selected)?"""
        if element.Category and element.Category.Id.ToString() in self.cat_options:
            return True
        else:
            return False

    def AllowReference(self, refer, point):
        """Not used for selection"""
        return False


def pick_by_category(cat_options):
    """Handle selection by category"""
    try:
        new_selection = revit.get_selection()
        msfilter = PickByCategorySelectionFilter(cat_options)
        selection_list = revit.pick_rectangle(pick_filter=msfilter)
        filtered_list = []
        for element in selection_list:
            filtered_list.append(element.Id)
        selection.set_to(filtered_list)
    except Exception as err:
        logger.debug(err)

pick_by_category(selected_cat_ids)