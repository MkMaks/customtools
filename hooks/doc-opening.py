# -*- coding: UTF-8 -*-
from datetime import datetime

filePath = __eventargs__.PathName

# runing only if file is workshared because of backslash in path
try:
    lastBackslash = filePath.rindex("\\")
    # just the file name without the extension
    file_name = filePath[lastBackslash:][:-4]

    fileExtension = filePath[-3:]

    if fileExtension == "rvt":
        # getting timestamp string now in seconds
        start_time_string_seconds = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            try:
                f = open("L:\\customToolslogs\\openingTimeLogs\\"+ file_name + "_Open.tmp", "w")
            except:
                f = open("\\\\Srv\\Z\\customToolslogs\\openingTimeLogs\\"+ file_name + "_Open.tmp", "w")
                
            f.write(start_time_string_seconds + "\n")
            f.close()
        except:
             pass
except:
    pass