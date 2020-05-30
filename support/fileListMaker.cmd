PowerShell -Command "Set-ExecutionPolicy Unrestricted" >> "%TEMP%\StartupLog.txt" 2>&1

PowerShell dir -n > zoznamVykresov.csv
PowerShell #Write-Output "Zoznam bol vytvoreny."