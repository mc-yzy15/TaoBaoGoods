@echo off
echo Installing requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Done!
echo Press any key to exit...
pause >nul