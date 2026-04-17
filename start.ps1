$script = Join-Path $PSScriptRoot "scripts\start.ps1"
& $script @args
exit $LASTEXITCODE
