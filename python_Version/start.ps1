# start.ps1

Write-Output "Starting script..."
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path $scriptPath
Set-Location ..
# 激活虚拟环境
Set-Location -Path ".\.venv\Scripts"
.\Activate.ps1

# 返回到脚本所在目录并运行 Python 脚本
Set-Location -Path $scriptPath
python ".\TaoBaoGoods\python_Version\main.py"

Write-Output "Done!"
Write-Output "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
exit