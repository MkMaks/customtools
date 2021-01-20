"""Opens the GFI BIM trouble shooting for posting issues."""
from pyrevit import script

__title__ = 'Post Issue'
__doc__ = '''Opens the GFI BIM troubleshooting form for posting BIM related issues.'''
__author__ = 'David Vadkerti'
__context__ = 'zero-doc'
__helpurl__ = 'https://gfi.miraheze.org/wiki/BIM_troubleshooting'


# revit user name
# doc = __revit__.ActiveUIDocument.Document
# user_name = doc.Application.Username
# user name in os
import getpass
user_name = getpass.getuser()

# prefilled name in airtable form
url = 'https://airtable.com/shrTPnWkptt5zkBts' + '?prefill_Meno=' + user_name
script.open_url(url)