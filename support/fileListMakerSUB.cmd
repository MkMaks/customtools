PowerShell -Command "Set-ExecutionPolicy Unrestricted" >> "%TEMP%\StartupLog.txt" 2>&1
PowerShell Get-ChildItem -File -Recurse | Select-Object FullName > list.txt