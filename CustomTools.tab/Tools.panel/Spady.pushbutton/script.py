# -*- coding: utf-8 -*- 
__title__ = 'Spády'
__doc__ = """Opens webapp for slope calculation."""
__helpurl__ = 'https://youtu.be/3hEwNb-e7Ls?t=102'

from pyrevit import script

__context__ = 'zero-doc'

output = script.get_output()

url = 'http://pxlsjpg.atwebpages.com/spady/spady.html'
script.open_url(url)
# output.open_page(url)
# js_script_file_path = "C:\\Users\\davidv\\Desktop\\spady\\spadyv3.js"
# output.inject_script('', {'src': js_script_file_path})
