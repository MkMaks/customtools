from pyrevit import script
from pyrevit import forms


my_config = script.get_config()

if __name__ == "__main__":
    filePath = forms.pick_file(file_ext='txt', title='Select Shared Parameter File')

    if filePath:
        # setting parameter 
        setattr(my_config, "shared_param_path", filePath)
        script.save_config()