"""Version and support information."""
from pyrevit import script, coreutils
from hooksScripts import releasedVersion, snapshot

__context__ = 'zero-doc'

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

print("CustomTools is extension for pyRevit Add-In")
print(text_highligter("version " + releasedVersion) + text_highligter("snapshot " + snapshot))

# git updater - DEPRECATED
# print("\nCustomTools checks for updates on system startup.")
# print("For manual update run manual update file and click Reload button.")
# print("%APPDATA%\\pyRevit\\Extensions\\CustomTools.extension\\ManualUpdate.lnk")
# print(linkMaker("%APPDATA%\\pyRevit\\Extensions\\CustomTools.extension\\ManualUpdate.lnk","Update Now!"))

#prints clickable email address
print("\nFor support contact "+ mailto("vadkerti@gfi.sk"))
print("\n- " + linkMaker("https://gfi.miraheze.org/wiki/CustomTools_(Extension_pre_pyRevit)","Help page")+" - GFI wiki")
print("- " + linkMaker("https://gfi.miraheze.org/wiki/CustomTools_Hooks","CustomTools Hooks article")+" - GFI wiki")
print("- " + linkMaker("https://www.youtube.com/watch?v=WhEJ_YVtSM8&list=PL7jLBbBNDaKk8iQjLTBasAntRjiu4W2G2&index=1","CustomTools Youtube channel")+" - video user manual")
print("- " + linkMaker("https://bitbucket.org/davidvadkerti/customtools/src/master/","Git repository")+" - Bitbucket repo")
print("- " + linkMaker("https://bitbucket.org/davidvadkerti/customtools/issues","Issue tracker"))
print("- " + linkMaker("https://bitbucket.org/davidvadkerti/customtools/downloads/?tab=tags","Download installer"))





