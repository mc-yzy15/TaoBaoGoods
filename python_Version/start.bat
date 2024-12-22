@echo off
echo Starting script...

:: 获取当前脚本所在的目录
set scriptPath=%~dp0

:: 返回到项目根目录
cd /d %scriptPath%\..

:: 激活虚拟环境
if exist ".\.venv\Scripts\activate.bat" (
    call .\.venv\Scripts\activate.bat
) else (
    echo 虚拟环境未找到，请先创建虚拟环境或检查路径是否正确。
    exit /b 1
)

:: 运行 Python 脚本
python .\TaoBaoGoods\python_Version\main.py

if %errorlevel% neq 0 (
    echo Python 脚本执行失败，退出码: %errorlevel%
    exit /b %errorlevel%
)

echo Done!
echo Press any key to exit...
pause >nul
exit /b 0