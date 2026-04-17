@echo off
setlocal

set "script_dir=%~dp0"
powershell -ExecutionPolicy Bypass -NoProfile -File "%script_dir%scripts\start.ps1" %*
exit /b %errorlevel%
