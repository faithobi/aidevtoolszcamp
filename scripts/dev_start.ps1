param(
    [string]$HostName = '127.0.0.1',
    [int]$Port = 8000,
    [switch]$Open
)

# Use NoOpen on the underlying start script to avoid double-open
Write-Output "Starting server at http://$HostName`:$Port (Open browser: $Open)"
& "$PSScriptRoot\start_server.ps1" -HostName $HostName -Port $Port -NoOpen

if ($Open) {
    Start-Sleep -Seconds 1
    try {
        Start-Process "http://$HostName`:$Port" -ErrorAction SilentlyContinue
    } catch {
        Write-Output "Failed to open browser, but server should still be running."
    }
}
