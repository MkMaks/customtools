# -*- coding: utf-8 -*- 
__title__ = 'Spády'
__doc__ = """Opens webapp for slope calculation."""
__helpurl__ = 'https://youtu.be/3hEwNb-e7Ls?t=102'

from pyrevit import script

__context__ = 'zero-doc'


url = 'http://pxlsjpg.atwebpages.com/spady/spady.html'
script.open_url(url)
