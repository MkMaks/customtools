"""Opens the GFI wiki dynamo help article."""
from pyrevit import script


__context__ = 'zero-doc'


url = 'https://gfi.miraheze.org/wiki/Zoznam_Dynamo_skriptov'
script.open_url(url)
