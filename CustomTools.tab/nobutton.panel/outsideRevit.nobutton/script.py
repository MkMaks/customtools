__context__ = 'zero-doc'
__doc__ = 'Opens folder which contains scripts for use outside Revit.'

import subprocess
# getting %HOMEPATH%
from os.path import expanduser
homepath = expanduser("~")

# path for common user
try:
    supportPath = homepath + "\AppData\Roaming\pyRevit\Extensions\CustomTools.extension\support\doNotErase-pointer"
    test = open(supportPath,"r")
# path for developer using git clone
except:
    supportPath = homepath + "\Documents\gitRepos\pyRevit extensions\CustomTools.extension\support\doNotErase-pointer"
subprocess.Popen(r'explorer /select, '+supportPath)