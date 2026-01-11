@echo off
REM Build a single-file Windows executable using PyInstaller
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --noconfirm --onefile main.py
echo.
echo Build finished. See the dist folder for the executable (dist\main.exe).
pause
