"""Opens the GFI BIM trouble shooting from for posting issues."""
from pyrevit import script

__context__ = 'zero-doc'

url = 'https://airtable.com/shrTPnWkptt5zkBts'
script.open_url(url)