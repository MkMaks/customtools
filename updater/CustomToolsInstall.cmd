PowerShell -Command "Set-ExecutionPolicy Unrestricted" >> "%TEMP%\StartupLog.txt" 2>&1

PowerShell pyrevit extend ui CustomTools https://bitbucket.org/davidvadkerti/customtools.git
PowerShell #Write-Output "CustomTools has been installed successfuly."

PowerShell pyrevit configs logs none
PowerShell pyrevit configs colordocs enable
PowerShell #Write-Output "CustomTools has been set successfully."

PowerShell #setting CSS file
PowerShell pyrevit configs outputcss  "$env:APPDATA\pyRevit\Extensions\CustomTools.extension\outputstylesCustom.css"
PowerShell #Write-Output "CSS has been set successfully."

PowerShell # SETTING AUTO UPDATES THROUGH CMD IN STARTUP FOLDER
PowerShell $PathStartup = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"

PowerShell #constructing file path
PowerShell $PathUpdaterLink = "$env:APPDATA\pyRevit\Extensions\CustomTools.extension\updater\CustomToolsUpdater.cmd"

PowerShell Copy-Item -Path $PathUpdaterLink -Destination $PathStartup