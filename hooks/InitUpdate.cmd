PowerShell -Command "Set-ExecutionPolicy Unrestricted" >> "%TEMP%\StartupLog.txt" 2>&1
PowerShell Copy-Item -Path "$env:APPDATA\pyRevit\Extensions\CustomTools.extension\updater\CustomToolsUpdater.cmd" -Destination "$env:APPDATA\Microsoft\Windows\Start` Menu\Programs\Startup"