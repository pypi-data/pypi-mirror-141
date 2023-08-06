$limit = (Get-Date).AddDays(-15)
$path = "C:\ProgramData\Streambox\Iris\log"

# Delete iris log files older than the $limit.
Get-ChildItem -Path $path -Recurse -Force |
Where-Object { !$_.PSIsContainer -and $_.LastWriteTime -lt $limit -and $_.Name -like "iris*.log" } |
Remove-Item -Force
