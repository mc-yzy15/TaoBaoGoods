@echo off

rem 设置中文编码
chcp 936 > nul

echo 淘宝自动购买器 - C语言版本编译脚本
echo ===================================

rem 检查是否安装了MinGW
where gcc > nul 2> nul
if %errorlevel% neq 0 (
    echo 错误：未找到GCC编译器。请确保已安装MinGW并将其添加到系统PATH中。
    pause
    exit /b 1
)

echo 开始编译项目...

rem 编译所有源文件
gcc -c main.c -o main.o -Wall -O2
gcc -c config.c -o config.o -Wall -O2
gcc -c browser.c -o browser.o -Wall -O2
gcc -c ui.c -o ui.o -Wall -O2

rem 检查编译是否成功
if %errorlevel% neq 0 (
    echo 错误：编译失败！
    pause
    exit /b 1
)

echo 链接程序...

rem 链接生成可执行文件
gcc main.o config.o browser.o ui.o -o main.exe -lcomctl32 -lgdi32

rem 检查链接是否成功
if %errorlevel% neq 0 (
    echo 错误：链接失败！
    pause
    exit /b 1
)

echo 清理临时文件...
del *.o

echo 编译完成！生成的可执行文件：main.exe
echo 使用方法：
echo 1. 确保已配置好chromedriver.exe
rem 确保chromedriver版本与Chrome浏览器版本匹配
echo 2. 运行 main.exe 或按照提示操作

echo.
echo ===================================
echo 编译成功！
rem 提示用户按任意键继续
pause > nul