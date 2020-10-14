# -*- coding: UTF-8 -*-

__title__ = 'Fix report visual style'
__doc__ = 'Fixes visual style of saved report.'
__context__ = 'zero-doc'

from pyrevit import forms
import os
from shutil import copyfile

# pick source html file to edit
filePath = forms.pick_file(file_ext='html')

# copy file to correct location for all users of the extension
def copyFile(fileName,pathTo,folderPath):
    # path for common user
    try:
        copyFromPath = homepath + "\AppData\Roaming\pyRevit\Extensions\CustomTools.extension" + pathTo
        copyfile(copyFromPath, folderPath+fileName)
    # path for developer using git clone
    except:
        copyFromPath = homepath + "\Documents\pyRevitExtensions\CustomTools.extension" + pathTo
        copyfile(copyFromPath, folderPath+fileName)

if filePath:
    # make folder if it already does not exist
    lastBackslash = filePath.rindex("\\")
    folderPath = filePath[:lastBackslash]+"\\lib\\"
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
       
    # make copy of Chart.js and css file
    # getting %HOMEPATH%
    from os.path import expanduser
    homepath = expanduser("~")

    # copy Chart.js file
    copyFile("Chart.min.js.download","\support\outputWindow\Chart.min.js.download",folderPath)

    # copy css file
    copyFile("outputstylesCustom.css","\outputstylesCustom.css",folderPath)


    f = open(filePath, "r+")
    content = f.read()
    # print(content)

    # read the file and find css path
    try:
        start = content.index('<link href="file:///')
        end = content.index('outputstylesCustom.css"')
        changed_content = content[:start]+'<link href="lib/'+content[end:]

        # write changed relative path to css file
        f = open(filePath, "w")
        f.write(changed_content)
        f.close()
    except:
        pass