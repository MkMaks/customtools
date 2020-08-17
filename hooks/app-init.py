# -*- coding: UTF-8 -*-
from hooksScripts import versionLogger, releasedVersion, snapshot

versionLogger(releasedVersion,snapshot)

import os
import subprocess
try:
    # running CustomToolsUpdater.cmd script at:
    # %AppData%\\Roaming\\pyRevit\\Extensions\\CustomTools.extension\\updater\\CustomToolsUpdater.cmd
    appdataPath = os.getenv('APPDATA')
    updaterPath = appdataPath + '\\pyRevit\\Extensions\\CustomTools.extension\\updater\\CustomToolsUpdater.cmd'
    p = subprocess.Popen([updaterPath])
except:
    pass


"""TEASER."""
from pyrevit import script, coreutils

# highlights text using html string with css
def text_highligter(a):
        content = str(a)
        html_code = "<p class='elementlink'>"+content+"</p>"
        return coreutils.prepare_html_str(html_code)

def imageViewer(html_code):
    # sample_code = "<img src='https://i.ytimg.com/vi/SfLV8hD7zX4/maxresdefault.jpg' width=50%>"
    print(coreutils.prepare_html_str(html_code))

def mailto(a):
        content = str(a)
        html_code = '<a href=mailto:"'+ content +'" target="_blank" style="text-decoration: none; color: black; font-weight: bold;">'+ content +'</a>'
        # html_code = '<a href=mailto:"'+ content +'" target="_blank">'+ content +'</a>'
        return coreutils.prepare_html_str(html_code)

# make html link tag
def linkMaker(a,title):
        content = str(a)
        html_code = '<a href="'+content+'">'+ title +'</a>'
        return coreutils.prepare_html_str(html_code)

#prints heading and links
output = script.get_output()
output.set_height(700)

output.print_md("# NOVINKY - REVIT")

print("- " + linkMaker("https://gfi.miraheze.org/wiki/Automatické_vytvorenie_Sheetov_podľa_Excelu","Automatické_vytvorenie_Sheetov_podľa_Excelovskej tabuľky")+" - čiastočná automatizácia tvorby knihy bytov")

output.print_md("## CustomTools")
print("- " + linkMaker("https://www.youtube.com/watch?v=WhEJ_YVtSM8&list=PL7jLBbBNDaKk8iQjLTBasAntRjiu4W2G2","Video návod")+" - playlist s krátkymi návodmi a ukážkami na Youtube")
print("- " + linkMaker("https://gfi.miraheze.org/wiki/CustomTools", "CustomTools")+" - článok na wiki")

output.print_md("## pyRevit")
print("- " + linkMaker("https://www.youtube.com/playlist?list=PLc_1PNcpnV55VgYBfrIPrvjZjsvwki8LR","Video návod")+" - playlist na Youtube")
print("- " + linkMaker("https://gfi.miraheze.org/wiki/PyRevit","pyRevit")+" - článok na wiki")
print("\n\n")

imageViewer("<img src='https://images.squarespace-cdn.com/content/v1/5605a932e4b0055d57211846/1579016738840-S4HNYZPL5U05TTOGFZSR/ke17ZwdGBToddI8pDm48kGUB6bvAQyL_fjdXd3nTTDBZw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZUJFbgE-7XRK3dMEBRBhUpy1qOPYMCUmUox1BUDmVYF_KfvPNJdunqX1yE5UASPGwIGTVuQfUTrbnSl6yicKsPc/image-asset.png?format=750w'>")