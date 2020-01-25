pyrevit extend ui CustomTools https://bitbucket.org/davidvadkerti/customtools.git
pyrevit configs logs none
pyrevit configs colordocs enable

#constructing CSS file path since %APPDATA% is not working
$firstPath = "C:\Users\"
$secondPath = "\AppData\Roaming\pyRevit\Extensions\CustomTools.extension\outputstylesCustom.css"
$fullPath = "$($firstPath)$($env:UserName)$($secondPath)"
#Write-Output "$($fullPath)" > new.txt

#setting CSS file
pyrevit configs outputcss $fullPath