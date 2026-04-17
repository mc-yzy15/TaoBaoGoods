$ErrorActionPreference = "Stop"

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Error "Virtual environment not found. Run .\scripts\init.ps1 first."
    exit 1
}

& $venvPython (Join-Path $projectRoot "main.py") @args
exit $LASTEXITCODE
