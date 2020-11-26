"""Opens the GFI BIM trouble shooting for posting issues."""
from pyrevit import script

__title__ = 'Post Issue'
__doc__ = '''Opens the GFI BIM troubleshooting form for posting BIM related issues.'''
__author__ = 'David Vadkerti'
__context__ = 'zero-doc'

url = 'https://airtable.com/shrTPnWkptt5zkBts'
script.open_url(url)