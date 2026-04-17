$ErrorActionPreference = "Stop"

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$venvPath = Join-Path $projectRoot ".venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"

Write-Output "Preparing TaoBaoGoods Python environment..."

if (-not (Test-Path $venvPython)) {
    Write-Output "Creating virtual environment..."
    python -m venv $venvPath
}

& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -e $projectRoot

Write-Output "Environment ready."
