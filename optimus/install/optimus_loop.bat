@echo off
title OPTIMUS 24-7 Scraper (leave this window open)
cd /d "%USERPROFILE%\Optimus"
:loop
set "ZIP=" & set "DEPTH="
for /f "usebackq tokens=1,2 delims=|" %%a in (`py read_dispatch.py 2^>nul`) do (set "ZIP=%%a" & set "DEPTH=%%b")
if not defined ZIP set "ZIP=77008"
if not defined DEPTH set "DEPTH=3"
echo [%date% %time%] Optimus: scraping from seed %ZIP% (depth %DEPTH%) - auto-advances across the metro...
(echo %ZIP%& echo 2& echo %DEPTH%) | py maps_scraper_standalone.py
echo [%date% %time%] pass finished/stopped - restarting in 90s.  CLOSE THIS WINDOW to STOP.
timeout /t 90 /nobreak >nul
goto loop
