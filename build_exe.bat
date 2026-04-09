@echo off
echo [Drag to Search] Windows EXE Build Script
echo ------------------------------------------
echo 1. Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

echo 2. Building EXE file...
pyinstaller --noconsole --onefile --name "DragToSearch" src/main.py

echo ------------------------------------------
echo Build Complete! Check the 'dist' folder.
pause
