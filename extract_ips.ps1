param (

    [string]$LogPath = "..\input\firewall.log",
    [string]$OutputPath = "..\output\ips.txt"


)

if (-not (Test-Path $LogPath)) {
    Write-Error "Log file not found: $LogPath"
    exit 1


}



#Regex for IPv4 addresses
$ipRegex = '\b\d{1,3}(\.\d{1,3}){3}\b'




Get-Content $LogPath   |
    Select-String -Pattern $ipRegex -AllMatches  |
    ForEach-Object { $_.Matches.Value }  |
    Sort-Object -Unique   |
    Set-Content $OutputPath



Write-Host "The unique IP addresses are written to $OutputPath"