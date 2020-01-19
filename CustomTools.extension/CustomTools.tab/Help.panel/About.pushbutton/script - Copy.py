"""Version and support information."""
from pyrevit import script, coreutils


__context__ = 'zerodoc'

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

print("Extension for pyRevit Add-In")
print(text_highligter("version 0.2:181114\n"))
#print("\nvadkerti@gfi.sk")
print(mailto("vadkerti@gfi.sk"))


