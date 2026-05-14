@echo off
setlocal

echo ============================================
echo OPTIMUS MAP TOOLS - OFFLINE INSTALLER
echo ============================================

set INSTALL_DIR=%USERPROFILE%\Optimus
set SOURCE_DIR=%~dp0

echo Install dir: %INSTALL_DIR%
echo Source dir: %SOURCE_DIR%
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed or not in PATH.
    pause
    exit /b 1
)

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%INSTALL_DIR%\hunter_screenshots" mkdir "%INSTALL_DIR%\hunter_screenshots"
if not exist "%INSTALL_DIR%\output" mkdir "%INSTALL_DIR%\output"

echo Copying files...
copy /Y "%SOURCE_DIR%mapman_api_batch.py" "%INSTALL_DIR%\"
copy /Y "%SOURCE_DIR%hunter_reclassifier_safe.py" "%INSTALL_DIR%\"
copy /Y "%SOURCE_DIR%hunter_screenshot_extractor.py" "%INSTALL_DIR%\"
copy /Y "%SOURCE_DIR%update.bat" "%INSTALL_DIR%\" 2>nul

echo Installing packages...
python -m pip install --upgrade pip
python -m pip install requests pillow numpy scipy gspread google-auth pgeocode

echo Creating shortcuts...
set DESKTOP=%USERPROFILE%\Desktop

powershell -NoProfile -ExecutionPolicy Bypass -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%DESKTOP%\Mapman.lnk');$s.TargetPath='python.exe';$s.Arguments='\"%INSTALL_DIR%\mapman_api_batch.py\"';$s.WorkingDirectory='%INSTALL_DIR%';$s.Save()"

powershell -NoProfile -ExecutionPolicy Bypass -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%DESKTOP%\Reclassifier.lnk');$s.TargetPath='python.exe';$s.Arguments='\"%INSTALL_DIR%\hunter_reclassifier_safe.py\"';$s.WorkingDirectory='%INSTALL_DIR%';$s.Save()"

powershell -NoProfile -ExecutionPolicy Bypass -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%DESKTOP%\Extractor.lnk');$s.TargetPath='python.exe';$s.Arguments='\"%INSTALL_DIR%\hunter_screenshot_extractor.py\"';$s.WorkingDirectory='%INSTALL_DIR%';$s.Save()"

echo.
echo INSTALL COMPLETE
echo Put enrich_queue.csv in %INSTALL_DIR%
pause
