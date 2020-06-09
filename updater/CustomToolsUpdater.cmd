PowerShell -Command "Set-ExecutionPolicy Unrestricted" >> "%TEMP%\StartupLog.txt" 2>&1
PowerShell pyrevit extensions update CustomTools
PowerShell pyrevit configs rocketmode enable
rem when pyrevit update needed
rem PowerShell pyrevit clones update master