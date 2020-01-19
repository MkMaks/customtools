# -*- coding: utf-8 -*-
def hmsTimer(timerSeconds):
    # for treating formating of pyrevit timer function
    from math import floor
    seconds = round(timerSeconds,2)
    if seconds<60:
        hms = str(seconds)+" seconds"
    elif seconds<3600:
        minutes =  int(floor(seconds/60))
        seconds = seconds%60
        hms = str(minutes)+" min "+str(seconds)+" seconds"
    else:
        hours =  int(floor(seconds/3600))
        minutes =  int(floor(seconds%60))
        seconds = seconds%60
        hms = str(hours)+" h "+str(minutes)+" min "+str(seconds)+" seconds"

    claim = "Transaction took "+hms
    return claim