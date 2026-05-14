@echo off
set REPO=patricksiado-prog/optimus-map-tools
set BRANCH=main
set INSTALL_DIR=%USERPROFILE%\Optimus
set RAW=https://raw.githubusercontent.com/%REPO%/%BRANCH%

cd /d "%INSTALL_DIR%" 2>nul
if errorlevel 1 (
    echo ERROR: %INSTALL_DIR% not found. Run install.bat first.
    pause
    exit /b 1
)

echo Updating Optimus scripts...
for %%F in (mapman_api_batch.py hunter_reclassifier_safe.py hunter_screenshot_extractor.py update.bat install.bat) do (
    echo %%F
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri '%RAW%/%%F' -OutFile '%INSTALL_DIR%\%%F.new' -UseBasicParsing"
    if exist "%INSTALL_DIR%\%%F.new" move /Y "%INSTALL_DIR%\%%F.new" "%INSTALL_DIR%\%%F" >nul
)
echo Done.
pause
