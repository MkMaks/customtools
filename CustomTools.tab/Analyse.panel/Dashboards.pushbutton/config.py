# -*- coding: utf-8 -*- 
__doc__ = 'Opens folder with templates of Power BI dashboards.'

import subprocess
# getting %HOMEPATH%
from os.path import expanduser
homepath = expanduser("~")

# path for common user
try:
    supportPath = homepath + "\AppData\Roaming\pyRevit\Extensions\CustomTools.extension\support\pbi\doNotErase-pointer"
    test = open(supportPath,"r")
# path for developer using git clone
except:
    supportPath = homepath + "\Documents\gitRepos\pyRevit extensions\CustomTools.extension\support\pbi\doNotErase-pointer"
subprocess.Popen(r'explorer /select, '+supportPath)