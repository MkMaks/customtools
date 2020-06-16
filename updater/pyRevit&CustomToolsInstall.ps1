#installing pyRevit
pyrevit clone master base
pyrevit attach basepublic latest --installed 


#installing CustomTools extension
pyrevit extend ui CustomTools https://bitbucket.org/davidvadkerti/customtools.git
#Write-Output "CustomTools has been installed successfuly."

pyrevit configs logs none
pyrevit configs colordocs enable
#Write-Output "CustomTools has been set successfully."

#setting CSS file
pyrevit configs outputcss  "$env:APPDATA\pyRevit\Extensions\CustomTools.extension\outputstylesCustom.css"
#Write-Output "CSS has been set successfully."

# SETTING AUTO UPDATES THROUGH CMD IN STARTUP FOLDER
$PathStartup = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"

#constructing file path
$PathUpdaterLink = "$env:APPDATA\pyRevit\Extensions\CustomTools.extension\updater\CustomToolsUpdater.cmd"

Copy-Item -Path $PathUpdaterLink -Destination $PathStartup

#set telemetry logging
pyrevit configs telemetry enable
pyrevit configs telemetry file "L:\customToolslogs\toolsLogs"