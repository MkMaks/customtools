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

# releasedVersion = "0.5"
# snapshot = "200124"
print(text_highligter("version " + releasedVersion) + text_highligter("snapshot " + snapshot))

# git uploader
print("\nCustomTools checks for updates on system startup.")
print("For manual update run manual update file and click Reload button.")
print("%APPDATA%\\pyRevit\\Extensions\\CustomTools.extension\\ManualUpdate.lnk")

# deprecated
# new version checker
# try:
# 	currentVersionFile = open("L:\REVIT\Dynamo\PyrevitExtensions\CustomToolsCurrentVersion.txt","r")
# 	currentVersionList = (currentVersionFile.readlines())
# 	currentVersion = str(currentVersionList)[2:-2]
# 	if currentVersion == releasedVersion:
# 		print("Your CustomTools extension IS up to date.")
# 	else:
# 		print("Your CustomTools extension IS NOT up to date.\n"+ 
# 			linkMaker("http://dynamohelp.atwebpages.com/support_files/CustomTools.extension_"+currentVersion+".7z", "DOWNLOAD NEW "+ currentVersion))
# except:
# 	pass

#prints clickable email address
print("\nFor support contact "+ mailto("vadkerti@gfi.sk"))
print("For help visit " + linkMaker("https://gfi.miraheze.org/wiki/CustomTools_(Extension_pre_pyRevit)","help page") + "on GFI wiki")

print("\nFor description of hooks functions and logging visit " + linkMaker("https://gfi.miraheze.org/wiki/CustomTools_Hooks","CustomTools Hooks article") + "on GFI wiki")
print(linkMaker("https://bitbucket.org/davidvadkerti/customtools/src/master/","Bitbucket git repository"))


