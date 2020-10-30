# -*- coding: UTF-8 -*-
from datetime import datetime
from pyrevit import revit
from os import path, remove

doc = __eventargs__.Document
filePath = doc.PathName

# getting central file name for log name
central_path = revit.query.get_central_path(doc)
fileExtension = filePath[-3:]

if fileExtension == "rvt":
    # GETTING FILE NAME
    # getting local file name for tmp file name
    try:
        lastBackslash_L = filePath.rindex("\\")
    except:
        # for opened as dettached file
        lastBackslash_L = filePath.rindex("/")

    # just the file name without the extension
    local_file_name = filePath[lastBackslash_L:][:-4]

    # skipped if file is not workshared (when slash is not in filepath)
    # if central_path != None or central_path !="":
    try:
        try:
            # for rvt server
            lastBackslash_C = central_path.rindex("/")
        except:
            # for other locations
            lastBackslash_C = central_path.rindex("\\")
        # just the file name without the extension
        central_file_name = central_path[lastBackslash_C:][:-4]
    except:
        central_file_name = local_file_name

    # LOGGING
    # tabulator between data to separte columns of the schedule
    separator = "\t" 
    try:
        # reading timestamp from tmp file
        tmp_file_path = "L:\\customToolslogs\\openingTimeLogs\\"+ local_file_name + "_Open.tmp"
        tmp_file = open(tmp_file_path, "r")
        start_time_string = tmp_file.read()
        # converting string to datetime
        start_time = datetime.strptime(start_time_string,"%Y-%m-%d %H:%M:%S")
        tmp_file.close()

        if path.exists(tmp_file_path):
            remove(tmp_file_path)

        # end time in seconds
        # round datetime to seconds (converting to string and then back to datetime object with correct)
        end_time_string_seconds = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time_string_seconds,"%Y-%m-%d %H:%M:%S")


        timeDelta = end_time - start_time
        # print timeDelta

        user_name = doc.Application.Username

        # writing time to log file
        log_file = open("L:\\customToolslogs\\openingTimeLogs\\"+ central_file_name + "_Open.log", "a")
        log_file.write(end_time_string_seconds + separator + str(timeDelta)+ separator + user_name + "\n")
        log_file.close()
    except:
         pass