PowerShell -Command "Set-ExecutionPolicy Unrestricted" >> "%TEMP%\StartupLog.txt" 2>&1
PowerShell pyrevit extensions update CustomTools
PowerShell pyrevit configs rocketmode enable
PowerShell pyrevit configs telemetry enable
PowerShell pyrevit configs telemetry file "L:\customToolslogs\toolsLogs"
PowerShell pyrevit attach ct default --installed
# PowerShell pyrevit configs telemetry file "\\Srv2\Z\customToolslogs\toolsLogs"
# when pyrevit update needed
# pyrevit clones update master