# Stops the server started by start_server.ps1 (reads PID from server.pid)
$projectRoot = Resolve-Path "$PSScriptRoot\.."
$projectRoot = $projectRoot.Path

$pidFile = Join-Path $projectRoot 'server.pid'
if (-not (Test-Path $pidFile)) {
    Write-Output "No server.pid found. Server may not be running."
    exit 0
}

$pidVal = Get-Content $pidFile -ErrorAction SilentlyContinue
if (-not $pidVal) {
    Remove-Item $pidFile -ErrorAction SilentlyContinue
    Write-Output "PID file was empty and has been removed."
    exit 0
}

if (Get-Process -Id $pidVal -ErrorAction SilentlyContinue) {
    Stop-Process -Id $pidVal -Force -ErrorAction SilentlyContinue
    Remove-Item $pidFile -ErrorAction SilentlyContinue
    Write-Output "Stopped process $pidVal"
    # Cleanup log files
    $logFile = Join-Path $projectRoot 'server.log'
    $errFile = Join-Path $projectRoot 'server.err.log'
    Remove-Item $logFile -ErrorAction SilentlyContinue
    Remove-Item $errFile -ErrorAction SilentlyContinue
} else {
    Remove-Item $pidFile -ErrorAction SilentlyContinue
    Write-Output "No process with PID $pidVal found. PID file removed."
}
