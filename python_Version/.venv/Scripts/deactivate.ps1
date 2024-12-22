# deactivate.ps1

if (Test-Path Env:_OLD_VIRTUAL_PROMPT) {
    $env:PROMPT = $env:_OLD_VIRTUAL_PROMPT
    Remove-Item Env:_OLD_VIRTUAL_PROMPT
}

if (Test-Path Env:_OLD_VIRTUAL_PYTHONHOME) {
    $env:PYTHONHOME = $env:_OLD_VIRTUAL_PYTHONHOME
    Remove-Item Env:_OLD_VIRTUAL_PYTHONHOME
}

if (Test-Path Env:_OLD_VIRTUAL_PATH) {
    $env:PATH = $env:_OLD_VIRTUAL_PATH
    Remove-Item Env:_OLD_VIRTUAL_PATH
}

Remove-Item Env:VIRTUAL_ENV -ErrorAction SilentlyContinue
Remove-Item Env:VIRTUAL_ENV_PROMPT -ErrorAction SilentlyContinue