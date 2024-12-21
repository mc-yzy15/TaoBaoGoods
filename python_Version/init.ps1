# init.ps1

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Output "Installing requirements..."
Set-Location -Path $scriptPath

# 激活虚拟环境
Set-Location -Path ".\.venv\Scripts"
.\Activate.ps1

# 返回到脚本所在目录并安装依赖
Set-Location -Path $scriptPath
python -m pip install --upgrade pip
pip install -r ".\TaoBaoGoods\python_Version\requirements.txt"

Write-Output "Done!"
Write-Output "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
exit