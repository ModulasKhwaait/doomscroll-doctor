@echo off
echo Stopping DoomScrollDoctor...
taskkill /F /IM pythonw.exe /T >nul 2>&1
if %errorlevel% == 0 (
    echo DoomScrollDoctor stopped successfully!
) else (
    echo DoomScrollDoctor was not running.
)
pause