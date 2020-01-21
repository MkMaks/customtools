"""Opens help for the CustomTools Extension on GFI wiki website."""
from pyrevit import script


__context__ = 'zero-doc'


url = 'https://gfi.miraheze.org/wiki/CustomTools_(Extension_pre_pyRevit)'
script.open_url(url)
