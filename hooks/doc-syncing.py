# -*- coding: UTF-8 -*-
from datetime import datetime

doc = __eventargs__.Document
filePath = doc.PathName

# getting local file name for tmp file name
try:
    lastBackslash = filePath.rindex("\\")
# for syncing detached central file
except:
    lastBackslash = filePath.rindex("/")
# just the file name without the extension
file_name = filePath[lastBackslash:][:-4]

fileExtension = filePath[-3:]

if fileExtension == "rvt":
    # getting timestamp string now in seconds
    start_time_string_seconds = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try: 
        f = open("L:\\customToolslogs\\syncTimeLogs\\"+ file_name + "_Sync.tmp", "w")
        f.write(start_time_string_seconds + "\n")
        f.close()
    except:
         pass