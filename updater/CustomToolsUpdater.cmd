PowerShell -Command "Set-ExecutionPolicy Unrestricted" >> "%TEMP%\StartupLog.txt" 2>&1
PowerShell pyrevit extensions update CustomTools
PowerShell pyrevit configs rocketmode enable
# when pyrevit update needed
# pyrevit clones update master