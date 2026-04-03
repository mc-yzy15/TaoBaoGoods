$script = Join-Path $PSScriptRoot "scripts\init.ps1"
& $script @args
exit $LASTEXITCODE
