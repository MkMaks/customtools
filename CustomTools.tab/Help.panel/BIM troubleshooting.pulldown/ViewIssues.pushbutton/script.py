"""Opens the GFI BIM trouble shooting for View issue tracker history."""
from pyrevit import script

__title__ = 'View Issues'
__doc__ = '''Opens the GFI BIM troubleshooting history.'''
__author__ = 'David Vadkerti'
__context__ = 'zero-doc'

url = 'https://airtable.com/shr8HrKsT7igtx68O/tblEH2vhKin56Q8kM'
script.open_url(url)