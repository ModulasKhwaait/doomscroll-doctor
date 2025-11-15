@echo off
echo Starting DoomScrollDoctor...
cd /d "%~dp0"
start /B venv\Scripts\pythonw.exe src/tray_app.py
echo DoomScrollDoctor is running in your system tray!
echo Look for the green icon near your clock.
echo Right-click it to see stats or quit.
timeout /t 3