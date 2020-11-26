"""Opens the GFI BIM trouble shooting from for posting issues."""
from pyrevit import script

__context__ = 'zero-doc'

url = 'https://airtable.com/shr8HrKsT7igtx68O/tblEH2vhKin56Q8kM'
script.open_url(url)