#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Opens keyboard shortcuts cheatsheet."""
from pyrevit import script


__context__ = 'zero-doc'
__title__ = 'Keyboard\nshortuts'

url = 'https://airtable.com/shriLXgkKNvsD4O0X'
# url = 'https://gfi.miraheze.org/wiki/Klávesové_skratky_-_Revit#Dávid_Vadkerti'
script.open_url(url)