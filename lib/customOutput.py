# -*- coding: utf-8 -*- 

# colors for chart.js graphs
colors = 10*["#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb",
            "#4d4d4d","#000000","#fff0f2","#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb","#e97800","#a6c844",
            "#4d4d4d","#fff0d9","#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb","#4d4d4d","#e97800","#a6c844",
            "#fff0e6","#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb","#4d4d4d","#fff0e6","#e97800","#a6c844",
            "#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb","#4d4d4d","#9988bb","#4d4d4d","#e97800","#a6c844",
            "#4d4d4d","#fff0d9","#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb","#4d4d4d","#e97800","#a6c844",
            "#4d4d4d","#fff0d9","#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb","#4d4d4d","#e97800","#a6c844",
            "#4d4d4d","#fff0d9","#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb","#4d4d4d","#e97800","#a6c844",
            "#4d4d4d","#fff0d9","#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb","#4d4d4d","#e97800","#a6c844",
            "#4d4d4d","#fff0d9","#ffc299","#ff751a","#cc5200","#ff6666","#ffd480","#b33c00","#ff884d","#d9d9d9","#9988bb","#4d4d4d","#e97800","#a6c844",]

# list of Warnings rated as critical
criticalWarnings = ['Elements have duplicate "Type Mark" values',
    'There are identical instances in the same place',
    'Room Tag is outside of its Room',
    'Multiple Rooms are in the same enclosed region',
    'Multiple Areas are in the same enclosed region',
    'One element is completely inside another',
    'Room is not in a properly enclosed region',
    'Room separation line is slightly off axis and may cause inaccuracies',
    'Area is not in a properly enclosed region',
    "Rectangular opening doesn't cut its host",
    'Elements have duplicate "Number" values',]

# default paths for settings
def_hookLogs = "L:\\customToolslogs\\hooksLogs"
def_revitBuildLogs = "L:\\customToolslogs\\versions.log"
def_revitBuilds = "20200826_1250(x64)"
def_massMessagePath = "L:\\_i\\CTmassMessage\\mass_message.html"
def_syncLogPath = "L:\\customToolslogs\\syncTimeLogs"
def_openingLogPath = "L:\\customToolslogs\\openingTimeLogs"
def_dashboardsPath = "L:\\powerBI"

# formating time in seconts to HHMMSS format
def hmsTimer(timerSeconds):
    # for treating formating of pyrevit timer function
    from math import floor
    seconds = round(timerSeconds,2)
    if seconds<60:
        hms = str(seconds)+" seconds"
    elif seconds<3600:
        minutes = int(floor(seconds//60))
        seconds = seconds%60
        hms = str(minutes)+" min "+str(seconds)+" seconds"
    else:
        hours = seconds//3600
        minutes = int((seconds%3600)//60)
        seconds = seconds%60
        if minutes ==0:
            hms = str(hours)+" h "+str(seconds)+" seconds"
        else:
            hms = str(hours)+" h "+str(minutes)+" min "+str(seconds)+" seconds"
    claim = "Transaction took "+hms
    return claim

# gets name of the current document
def file_name_getter(doc):
    file_path = doc.PathName
    # trying all cases, for worshared, not worshared and detached files
    try:
        file_name = file_path[file_path.rindex("/"):]
    except:
        try:
            file_name = file_path[file_path.rindex("\\")+1:]
        except:
            file_name = file_path
    return(file_name)

# setting icon for output window
def ct_icon(output):
    import os
    appdataPath = os.getenv('APPDATA')
    iconPath = appdataPath + '\\pyRevit\\Extensions\\CustomTools.extension\\CustomToolsLogo.PNG'
    output.set_icon(iconPath)