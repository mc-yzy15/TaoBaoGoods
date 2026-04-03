@echo off
setlocal
chcp 65001 > nul

echo TaoBaoGoods C Experimental Helper
echo ==================================
echo Building manual-helper prototype...

gcc -c ..\main.c -o main.o -Wall -O2 -I..\src
gcc -c ..\config.c -o config.o -Wall -O2 -I..\src
gcc -c ..\browser.c -o browser.o -Wall -O2 -I..\src
gcc -c ..\ui.c -o ui.o -Wall -O2 -I..\src

if %errorlevel% neq 0 (
    echo Build failed during compilation.
    exit /b 1
)

gcc main.o config.o browser.o ui.o -o TaoBaoGoodsManualHelper.exe -lcomctl32 -lgdi32 -lshell32

if %errorlevel% neq 0 (
    echo Build failed during linking.
    exit /b 1
)

del *.o

echo Build succeeded.
echo Output: TaoBaoGoodsManualHelper.exe
echo This executable is an experimental manual-helper prototype.
exit /b 0
