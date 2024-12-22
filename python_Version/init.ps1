# init.ps1

# 获取脚本所在目录
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# 定义路径
$venvPath = Join-Path -Path $scriptPath -ChildPath ".venv"
$scriptsPath = Join-Path -Path $venvPath -ChildPath "Scripts"
$requirementsPath = Join-Path -Path $scriptPath -ChildPath "requirements.txt"

# 函数：检查文件是否存在
function Test-FileExists {
    param (
        [string]$filePath,
        [string]$errorMessage
    )
    if (-Not (Test-Path -Path $filePath)) {
        Write-Error $errorMessage
        exit 1
    }
}

# 函数：运行脚本
function Invoke-Script {
    param (
        [string]$scriptPath,
        [string]$errorMessage
    )
    if (Test-Path -Path $scriptPath) {
        . $scriptPath
    } else {
        Write-Error $errorMessage
        exit 1
    }
}

# 切换到脚本所在目录
Set-Location -Path $scriptPath

# 激活虚拟环境
Invoke-Script -scriptPath "$scriptsPath\Activate.ps1" -errorMessage "Virtual environment activation script not found at $scriptsPath\Activate.ps1"

# 检查 requirements.txt 文件是否存在
Test-FileExists -filePath $requirementsPath -errorMessage "requirements.txt file not found at $requirementsPath"

# 安装依赖
try {
    python -m pip install --upgrade pip
    python -m pip install -r $requirementsPath
} catch {
    Write-Error "Failed to install requirements: $_"
    exit 1
}

Write-Output "Done!"
Write-Output "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# 取消激活虚拟环境
Write-Output "Deactivating virtual environment..."
Invoke-Script -scriptPath "$scriptsPath\deactivate.ps1" -errorMessage "Virtual environment deactivation script not found at $scriptsPath\deactivate.ps1"
Write-Output "Virtual environment deactivated."