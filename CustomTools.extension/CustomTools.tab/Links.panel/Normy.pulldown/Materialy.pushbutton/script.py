# -*- coding: utf-8 -*-
__title__ = 'Materiály'
__doc__ = """Tepelná ochrana budov teplotechnické vlastnosti stavebných konštrukcií a budov\n
Časť 3: Vlastnosti prostredia a stavebných výrobkov"""

from pyrevit import script

__context__ = 'zero-doc'

# url = 'C:\\Untitled.pdf'
url = 'https://www.dropbox.com/s/38ehwfijzaadw7y/STN_73_0540_3_2012_text%20-%20teplotechnicka%20norma%203%20-%20materialy.pdf?dl=0'
script.open_url(url)