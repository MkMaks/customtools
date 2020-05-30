import os
from os import listdir
from os.path import isfile, join
#workingDir = 'C:\Users\\pxls\\Desktop\\renameFolder\\'
workingDir = os.path.dirname(os.path.realpath(__file__))
fileList = [f for f in listdir(workingDir) if isfile(join(workingDir, f))]
fileList.remove("revisionIncrement.pyw")

alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','ZA','ZB','ZC']

os.chdir(workingDir)
a=1
for i in fileList:
	rev = i[-5].upper()
	revIndex = alphabet.index(rev)
	newRev = alphabet[revIndex+1]
	os.rename(i,i[:-5]+newRev+i[-4:])
