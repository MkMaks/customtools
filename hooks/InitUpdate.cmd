PowerShell -Command "Set-ExecutionPolicy Unrestricted" >> "%TEMP%\StartupLog.txt" 2>&1
PowerShell pyrevit configs telemetry enable
PowerShell pyrevit configs telemetry file "L:\customToolslogs\toolsLogs"

