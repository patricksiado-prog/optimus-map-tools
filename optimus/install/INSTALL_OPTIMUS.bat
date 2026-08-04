@echo off
REM ===========================================================================
REM  INSTALL_OPTIMUS.bat  --  ONE-CLICK installer for the Optimus toolkit.
REM
REM    * Installs Python the reliable way (python.org, on PATH).
REM    * Downloads the LATEST Map Scraper + Precise Hunter from GitHub.
REM    * Installs all Python packages + the Chromium browser engine.
REM    * Drops your Google key so it writes to the sheet.
REM    * Creates TWO DESKTOP ICONS:  "Optimus Map Scraper"  and
REM      "Optimus Precise Hunter".  Each icon re-downloads the newest code
REM      from GitHub every launch, so they are always up to date.
REM    * Both work in OKC and everywhere.
REM
REM  Re-run anytime to refresh everything.
REM ===========================================================================
setlocal EnableDelayedExpansion
title OPTIMUS - Installer
set "APP=%USERPROFILE%\Optimus"
set "REPO=patricksiado-prog/optimus-map-tools"
set "BRANCH=claude/chat-repetitive-questions-9ex5h7"
set "RAW=https://raw.githubusercontent.com/%REPO%/%BRANCH%/optimus"
set "CREDS=https://drive.usercontent.google.com/download?id=1upYH4h2VsmOwO82v9CVjMpE6IzV-5dIs&export=download&confirm=t"
set "DESK=%USERPROFILE%\Desktop"
if exist "%OneDrive%\Desktop" set "DESK=%OneDrive%\Desktop"

echo.
echo  ================================================================
echo     OPTIMUS TOOLKIT  --  installing Map Scraper + Precise Hunter
echo  ================================================================
echo.

echo [1/7] Python...
where py >nul 2>&1
if errorlevel 1 (
    echo     Installing Python ^(one time, ~2 min^)...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "iwr https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe -OutFile $env:TEMP\pysetup.exe; Start-Process $env:TEMP\pysetup.exe -ArgumentList '/quiet','InstallAllUsers=0','PrependPath=1','Include_launcher=1' -Wait"
)
where py >nul 2>&1 || ( echo     Python did not finish installing - reboot and run this again. & pause & exit /b 1 )

echo [2/7] Folders...
if not exist "%APP%" mkdir "%APP%"

echo [3/7] Downloading the latest programs from GitHub...
set "CB=%RANDOM%%RANDOM%"
for %%F in (precise_fiber_hunter.py optimus_dot_detect.py optimus_api_capture.py hunter_fixes.py backend_classifier.py build_codes.json) do (
  powershell -NoProfile -Command "iwr '%RAW%/%%F?cb=%CB%' -OutFile '%APP%\%%F'" || ( echo     Could not reach GitHub. Check internet. & pause & exit /b 1 )
)
powershell -NoProfile -Command "iwr '%RAW%/standalone/maps_scraper_standalone.py?cb=%CB%' -OutFile '%APP%\maps_scraper_standalone.py'"
powershell -NoProfile -Command "iwr '%RAW%/install/RUN_PRECISE_HUNTER.bat?cb=%CB%' -OutFile '%APP%\RUN_PRECISE_HUNTER.bat'"
powershell -NoProfile -Command "iwr '%RAW%/install/RUN_MAP_SCRAPER.bat?cb=%CB%'  -OutFile '%APP%\RUN_MAP_SCRAPER.bat'"
powershell -NoProfile -Command "iwr '%RAW%/install/STOP_OPTIMUS.bat?cb=%CB%'      -OutFile '%APP%\STOP_OPTIMUS.bat'"

echo [4/7] Python packages...
py -m pip install --upgrade pip >nul 2>&1
py -m pip install --upgrade requests gspread google-auth playwright pgeocode numpy pillow

echo [5/7] Browser engine ^(first time can take a minute or two^)...
py -m playwright install chromium

echo [6/7] Google key ^(so it writes to your sheet^)...
powershell -NoProfile -Command "try{iwr '%CREDS%' -OutFile '%APP%\google_creds.json'}catch{}"

echo [7/7] Creating desktop icons...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$w=New-Object -ComObject WScript.Shell;$s=$w.CreateShortcut('%DESK%\Optimus Map Scraper.lnk');$s.TargetPath='%APP%\RUN_MAP_SCRAPER.bat';$s.WorkingDirectory='%APP%';$s.IconLocation='%SystemRoot%\System32\SHELL32.dll,18';$s.Description='Optimus Google Maps Scraper (OKC + everywhere)';$s.Save()"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$w=New-Object -ComObject WScript.Shell;$s=$w.CreateShortcut('%DESK%\Optimus Precise Hunter.lnk');$s.TargetPath='%APP%\RUN_PRECISE_HUNTER.bat';$s.WorkingDirectory='%APP%';$s.IconLocation='%SystemRoot%\System32\SHELL32.dll,13';$s.Description='Optimus Precise Fiber Hunter (OKC + everywhere)';$s.Save()"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$w=New-Object -ComObject WScript.Shell;$s=$w.CreateShortcut('%DESK%\Stop Optimus.lnk');$s.TargetPath='%APP%\STOP_OPTIMUS.bat';$s.WorkingDirectory='%APP%';$s.IconLocation='%SystemRoot%\System32\SHELL32.dll,27';$s.Description='Turn OFF the Optimus Hunter + Scraper (and background workers)';$s.Save()"

echo.
echo  ================================================================
echo     DONE.  Two icons are on your desktop:
echo        - Optimus Map Scraper
echo        - Optimus Precise Hunter
echo     Double-click either one. They auto-update from GitHub on launch.
echo  ================================================================
echo.
pause
