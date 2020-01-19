"""Opens the GFI wiki website."""
from pyrevit import script


__context__ = 'zero-doc'


url = 'https://gfi.miraheze.org/wiki/GFI_wiki'
script.open_url(url)
