@echo off
REM ===========================================================================
REM  RUN_MAP_SCRAPER.bat  --  desktop launcher for the Google Maps Scraper.
REM  Re-downloads the newest code from GitHub every launch, then runs it. Works
REM  in OKC and everywhere: it searches "category in ZIP" straight on Google
REM  Maps, so whatever ZIPs you type are exactly what it scrapes.
REM ===========================================================================
title Optimus Map Scraper
setlocal EnableDelayedExpansion
set "RAW=https://raw.githubusercontent.com/patricksiado-prog/optimus-map-tools/claude/chat-repetitive-questions-9ex5h7/optimus"
set "APP=%USERPROFILE%\Optimus"
if not exist "%APP%" mkdir "%APP%"
cd /d "%APP%"

echo Checking for the latest Map Scraper...
set "CB=%RANDOM%%RANDOM%"
curl -L -s -o maps_scraper_standalone.py "%RAW%/standalone/maps_scraper_standalone.py?cb=!CB!"
findstr /C:"maps" maps_scraper_standalone.py >nul 2>&1 && echo   (on the latest version) || echo   (could not refresh -- running the copy you have)

echo.
echo  Type your ZIP codes when it asks -- OKC, Houston, anywhere.
echo.
set "PYCMD=python"
where py >nul 2>&1 && set "PYCMD=py"
%PYCMD% maps_scraper_standalone.py %*
echo.
echo  Closed. Double-click the desktop icon to run again.
pause
