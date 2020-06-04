PowerShell -Command "Set-ExecutionPolicy Unrestricted" >> "%TEMP%\StartupLog.txt" 2>&1

PowerShell tree /a /f> tree.txt
PowerShell #Write-Output "Strom bol vytvoreny."