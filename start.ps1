$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$webUrl = 'http://127.0.0.1:8765'
function Test-LearningWeb {
    try {
        $webState = Invoke-RestMethod -Uri "$webUrl/api/state" -TimeoutSec 2
        return ($null -ne $webState.lessons)
    } catch { return $false }
}
if (-not (Test-LearningWeb)) {
    $pythonPath = (Get-Command python -ErrorAction Stop).Source
    New-Item -ItemType Directory -Path (Join-Path $PSScriptRoot 'data') -Force | Out-Null
    Start-Process -FilePath $pythonPath -ArgumentList 'server.py' -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $PSScriptRoot 'data/server.log') -RedirectStandardError (Join-Path $PSScriptRoot 'data/server-error.log')
    $webReady = $false
    for ($attempt = 0; $attempt -lt 12; $attempt++) {
        Start-Sleep -Milliseconds 500
        if (Test-LearningWeb) { $webReady = $true; break }
    }
    if (-not $webReady) { throw 'Cannot start English Garden. See data/server-error.log.' }
}
Start-Process $webUrl
Write-Host "English Garden is running at $webUrl"
