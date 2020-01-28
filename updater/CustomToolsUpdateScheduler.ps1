#constructing file path since %APPDATA% is not working
$PathStartup = "C:\Users\$env:UserName\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

#constructing file path since %APPDATA% is not working
#$PathUpdater = "C:\Users\$($env:UserName)\AppData\Roaming\pyRevit\Extensions\CustomTools.extension\updater\CustomToolsUpdater.ps1"
$PathUpdaterLink = "C:\Users\$($env:UserName)\AppData\Roaming\pyRevit\Extensions\CustomTools.extension\updater\CustomToolsUpdater.cmd"

#Copy-Item -Path $PathUpdater -Destination $PathStartup
Copy-Item -Path $PathUpdaterLink -Destination $PathStartup

#Write-Output "$PathUpdater $PathUpdaterLink $PathStartup" > new.txt