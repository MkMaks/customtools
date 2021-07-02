from pyrevit import script
from hooksScripts import releasedVersion, snapshot
from customOutput import ct_icon, mass_message_url, text_highligter, mailto, linkMaker, imageViewer

__context__ = 'zero-doc'
__doc__ = 'Version, support information, mass message, issue tracker, git repo, manual, video help'

output = script.get_output()
output.set_height(710)
# changing icon
ct_icon(output)

# printing icon
import os
appdataPath = os.getenv('APPDATA')
iconPath = appdataPath + '\\pyRevit\\Extensions\\CustomTools.extension\\CustomToolsLogo.PNG'
iconPath_code = '<img src="' + iconPath + '" height="250">'
imageViewer(iconPath_code)

print("CustomTools is extension for pyRevit Add-In")
print(text_highligter("version " + releasedVersion) + text_highligter("snapshot " + snapshot))

#prints clickable email address
print("\nFor support contact "+ mailto("vadkerti@gfi.sk"))
print("\n- " + linkMaker("https://gfi.miraheze.org/wiki/CustomTools_(Extension_pre_pyRevit)","Help page")+" - GFI wiki")
print("- " + linkMaker("https://gfi.miraheze.org/wiki/CustomTools_Hooks","CustomTools Hooks article")+" - GFI wiki")
print("- " + linkMaker("https://www.youtube.com/watch?v=WhEJ_YVtSM8&list=PL7jLBbBNDaKk8iQjLTBasAntRjiu4W2G2","CustomTools Youtube channel")+" - video user manual")
print("- " + linkMaker("https://bitbucket.org/davidvadkerti/customtools/src/master/","Git repository")+" - Bitbucket repo")
print("- " + linkMaker("https://bitbucket.org/davidvadkerti/customtools/issues","Issue tracker"))
print("- " + linkMaker("https://bitbucket.org/davidvadkerti/customtools/downloads/?tab=tags","Download installer"))
# print("\n- " + linkMaker("L:\\_i\\CTmassMessage\\mass_message.html","Mass message")+" - view mass message")
# print("\n- " + linkMaker("\\\\Srv2\\Z\\_i\\CTmassMessage\\mass_message.html","Mass message")+" - view mass message")
print("\n- " + linkMaker(mass_message_url(),"Mass message")+" - view mass message")