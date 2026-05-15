@echo off
REM ============================================================
REM  OPTIMUS MAP TOOLS - PC INSTALLER
REM ============================================================
setlocal enabledelayedexpansion

set REPO=patricksiado-prog/optimus-map-tools
set BRANCH=main
set INSTALL_DIR=%USERPROFILE%\Optimus
set RAW=https://raw.githubusercontent.com/%REPO%/%BRANCH%

echo OPTIMUS MAP TOOLS - INSTALLER
echo Install location: %INSTALL_DIR%
echo.

REM -- 1. CHECK PYTHON --
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not in PATH. Install from python.org and re-run.
    pause & exit /b 1
)
for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo Found: %%v
echo.

REM -- 2. CREATE INSTALL DIR + SUBFOLDERS (FIX #2) --
if not exist "%INSTALL_DIR%"                       mkdir "%INSTALL_DIR%"
if not exist "%INSTALL_DIR%\hunter_screenshots"    mkdir "%INSTALL_DIR%\hunter_screenshots"
if not exist "%INSTALL_DIR%\output"                mkdir "%INSTALL_DIR%\output"
cd /d "%INSTALL_DIR%"

REM -- 3. INSTALL PYTHON DEPS --
echo Installing Python packages...
python -m pip install --upgrade pip --quiet
python -m pip install requests gspread google-auth pillow numpy scipy pgeocode --quiet
if errorlevel 1 echo WARN: pip had errors. Continuing.
echo.

REM -- 4. INSTALL SCRIPTS (local copies if present, else GitHub) --
REM        FIX #1: -NoProfile -ExecutionPolicy Bypass on every PowerShell call
echo Installing scripts...
set SOURCE_DIR=%~dp0
for %%F in (mapman_api_batch.py hunter_reclassifier_safe.py hunter_screenshot_extractor.py update.bat) do (
    if exist "%SOURCE_DIR%%%F" (
        echo   %%F  [local]
        copy /Y "%SOURCE_DIR%%%F" "%INSTALL_DIR%\%%F" >nul
    ) else (
        echo   %%F  [GitHub]
        powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri '%RAW%/%%F' -OutFile '%INSTALL_DIR%\%%F' -UseBasicParsing"
        if errorlevel 1 echo     FAILED - check GitHub repo has %%F
    )
)
echo.

REM -- 5. DESKTOP SHORTCUTS (FIX #4: quoted args for spaces in username) --
echo Creating desktop shortcuts...
set DESK=%USERPROFILE%\Desktop
for %%S in (mapman_api_batch hunter_reclassifier_safe hunter_screenshot_extractor) do (
    powershell -NoProfile -ExecutionPolicy Bypass -Command "$w=New-Object -ComObject WScript.Shell; $s=$w.CreateShortcut('%DESK%\%%S.lnk'); $s.TargetPath='python.exe'; $s.Arguments='\"%INSTALL_DIR%\%%S.py\"'; $s.WorkingDirectory='\"%INSTALL_DIR%\"'; $s.IconLocation='python.exe'; $s.Save()"
)
echo.

REM -- 6. CREDS + KEY REMINDERS --
echo ============================================================
echo   POST-INSTALL CHECKLIST
echo ============================================================
if not exist "%INSTALL_DIR%\google_creds.json" (
    echo   [ ] Copy google_creds.json to %INSTALL_DIR%
    echo       Reclassifier won't run without it.
) else (
    echo   [X] google_creds.json present
)
echo   [ ] API key is embedded in mapman_api_batch.py.
echo       If Google revokes it, replace the value of API_KEY at the top.
echo   [ ] Put enrich_queue.csv into %INSTALL_DIR%\ before running mapman.
echo   [ ] Put Hunter PNGs into %INSTALL_DIR%\hunter_screenshots\ for extractor.
echo.

echo INSTALL COMPLETE.
echo Auto-update on launch: each script checks GitHub for newer version.
echo Manual update: run update.bat
pause
