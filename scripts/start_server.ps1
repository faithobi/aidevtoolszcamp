param(
    [string]$HostName = '127.0.0.1',
    [int]$Port = 8000,
    [switch]$NoOpen
)

# Determine project root (one level up from scripts folder)
$projectRoot = Resolve-Path "$PSScriptRoot\.."
$projectRoot = $projectRoot.Path

$venvPython = Join-Path $projectRoot 'venv\Scripts\python.exe'
if (-not (Test-Path $venvPython)) {
    Write-Error "Python executable not found at $venvPython. Create and activate the virtualenv first."
    exit 1
}

$pidFile = Join-Path $projectRoot 'server.pid'
if (Test-Path $pidFile) {
    $old = Get-Content $pidFile -ErrorAction SilentlyContinue
    if ($old -and (Get-Process -Id $old -ErrorAction SilentlyContinue)) {
        Write-Output "Server already running with PID $old"
        exit 0
    } else {
        Remove-Item $pidFile -ErrorAction SilentlyContinue
    }
}

$args = @('manage.py', 'runserver', "${HostName}:${Port}")
$logFile = Join-Path $projectRoot 'server.log'
$errFile = Join-Path $projectRoot 'server.err.log'
$startInfo = @{
    FilePath    = $venvPython
    ArgumentList= $args
    WorkingDirectory = $projectRoot
    PassThru    = $true
    RedirectStandardOutput = $logFile
    RedirectStandardError  = $errFile
}

$proc = Start-Process @startInfo
Start-Sleep -Seconds 1
if ($proc -and (Get-Process -Id $proc.Id -ErrorAction SilentlyContinue)) {
    $proc.Id | Out-File -FilePath $pidFile -Encoding ascii
    Write-Output "Started server (PID $($proc.Id)) at http://$HostName`:$Port"
    Write-Output "Logs are written to: $logFile"
    # Open default browser to the server URL (unless NoOpen switch is set)
    if (-not $NoOpen) {
        try {
            Start-Process "http://$HostName`:$Port" -ErrorAction SilentlyContinue
        } catch {
            # no-op: some environments won't support launching a browser
        }
    }
} else {
    Write-Error "Failed to start server. Check logs in the terminal."
}
