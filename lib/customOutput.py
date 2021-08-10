# -*- coding: utf-8 -*- 
from pyrevit import coreutils
from pyrevit import output

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
def_revitBuilds = "20210420_1515(x64)"
def_massMessagePath = "L:\\_i\\CTmassMessage\\mass_message.html"
def_syncLogPath = "L:\\customToolslogs\\syncTimeLogs"
def_openingLogPath = "L:\\customToolslogs\\openingTimeLogs"
def_dashboardsPath = "L:\\powerBI"
def_language = "Slovak/SK"

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

# creating mass message url
def mass_message_url(output):
    from customOutput import def_massMessagePath
    from pyrevit.userconfig import user_config
    from os import path
    import os
    appdataPath = os.getenv('APPDATA')
    # server version of massmessage
    # if parameter exists in config file
    try:
        url = user_config.CustomToolsSettings.massMessagePath
    # if parameter doesnt exist in config file
    except:
        url = def_massMessagePath

    # url = "L:\\_i\\CTmassMessage\\mass_message.html"
    url_unc = "\\\\Srv\\Z\\_i\\CTmassMessage\\mass_message.html"
    if path.exists(url):
        # output.open_url(url)
        return url
    elif path.exists(url_unc):
        return url_unc
    # offline hardcoded version of massmessage
    else:
        # offline content of mass message
        return appdataPath + '\\pyRevit\\Extensions\\CustomTools.extension\\mass_message\\mass_message.html'

# highlights text using html string with css
def text_highligter(a):
    content = str(a)
    html_code = "<p class='elementlink'>"+content+"</p>"
    return coreutils.prepare_html_str(html_code)

# makes mailto link in output window
def mailto(a):
    content = str(a)
    html_code = '<a href=mailto:"'+ content +'" target="_blank" style="text-decoration: none; color: black; font-weight: bold;">'+ content +'</a>'
    # html_code = '<a href=mailto:"'+ content +'" target="_blank">'+ content +'</a>'
    return coreutils.prepare_html_str(html_code)

# makes html link tag
def linkMaker(a,title):
    content = str(a)
    html_code = '<a href="'+content+'">'+ title +'</a>'
    return coreutils.prepare_html_str(html_code)

# views image in output window
def imageViewer(html_code):
    # sample_code = "<img src='https://i.ytimg.com/vi/SfLV8hD7zX4/maxresdefault.jpg' width=50%>"
    print(coreutils.prepare_html_str(html_code))