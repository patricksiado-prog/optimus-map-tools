@echo off
setlocal EnableDelayedExpansion
title OPTIMUS - Install 24-7 Auto-Scraper
set "APP=%USERPROFILE%\Optimus"
set "REPO=patricksiado-prog/optimus-map-tools"
set "BRANCH=claude/chat-repetitive-questions-9ex5h7"
set "RAW=https://raw.githubusercontent.com/%REPO%/%BRANCH%/optimus"
set "CB=%RANDOM%%RANDOM%"
echo.
echo  ==============================================================
echo     OPTIMUS 24-7 AUTO-SCRAPER  --  runs the map scraper nonstop
echo     and takes its target from your Google Sheet (Claude steers it).
echo  ==============================================================
echo.
if not exist "%APP%" mkdir "%APP%"
where py >nul 2>&1 || ( echo   Run INSTALL_OPTIMUS.bat first ^(installs Python + your Google key^), then re-run this. & pause & exit /b 1 )
if not exist "%APP%\google_creds.json" ( echo   Missing Google key - run INSTALL_OPTIMUS.bat first. & pause & exit /b 1 )
echo   [1/3] Downloading latest scraper + runner...
powershell -NoProfile -Command "iwr '%RAW%/standalone/maps_scraper_standalone.py?cb=%CB%' -OutFile '%APP%\maps_scraper_standalone.py'"
powershell -NoProfile -Command "iwr '%RAW%/install/optimus_loop.bat?cb=%CB%' -OutFile '%APP%\optimus_loop.bat'"
powershell -NoProfile -Command "iwr '%RAW%/install/read_dispatch.py?cb=%CB%' -OutFile '%APP%\read_dispatch.py'"
powershell -NoProfile -Command "py -m pip install --quiet --upgrade gspread google-auth playwright pgeocode requests >$null 2>&1"
echo   [2/3] Setting it to auto-start every reboot...
set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$w=New-Object -ComObject WScript.Shell;$s=$w.CreateShortcut('%STARTUP%\Optimus 24-7 Scraper.lnk');$s.TargetPath='%APP%\optimus_loop.bat';$s.WorkingDirectory='%APP%';$s.Save()"
set "DESK=%USERPROFILE%\Desktop"
if exist "%OneDrive%\Desktop" set "DESK=%OneDrive%\Desktop"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$w=New-Object -ComObject WScript.Shell;$s=$w.CreateShortcut('%DESK%\Optimus 24-7 Scraper.lnk');$s.TargetPath='%APP%\optimus_loop.bat';$s.WorkingDirectory='%APP%';$s.IconLocation='%SystemRoot%\System32\SHELL32.dll,18';$s.Save()"
echo   [3/3] Starting it now...
start "" "%APP%\optimus_loop.bat"
echo.
echo  DONE. It is running now and will restart itself on every reboot.
echo  STOP anytime: close the "OPTIMUS 24-7 Scraper" window (or delete the
echo  'Optimus 24-7 Scraper' shortcut from your Startup folder).
echo.
pause
