"""Opens the dynamo help website."""
from pyrevit import script


__context__ = 'zero-doc'


url = 'http://dynamohelp.atwebpages.com'
script.open_url(url)
