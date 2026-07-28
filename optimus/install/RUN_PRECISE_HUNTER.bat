@echo off
REM ===========================================================================
REM  RUN_PRECISE_HUNTER.bat  --  desktop launcher for the Precise Fiber Hunter.
REM  Re-downloads the newest code from GitHub every launch (cache-busted) so the
REM  icon can never be stuck on old code, then runs it. Auto-restarts on crash.
REM  Works in OKC and everywhere: it types your ZIP into the AT&T map's search
REM  box and flies the map there before scanning (v0.4 search_zip fix).
REM ===========================================================================
title Optimus Precise Hunter
setlocal EnableDelayedExpansion
set "RAW=https://raw.githubusercontent.com/patricksiado-prog/optimus-map-tools/claude/chat-repetitive-questions-9ex5h7/optimus"
set "APP=%USERPROFILE%\Optimus"
if not exist "%APP%" mkdir "%APP%"
cd /d "%APP%"

echo Checking for the latest Precise Hunter...
set "CB=%RANDOM%%RANDOM%"
for %%F in (precise_fiber_hunter.py optimus_dot_detect.py optimus_api_capture.py hunter_fixes.py backend_classifier.py build_codes.json) do (
  curl -L -s -o "%%F" "%RAW%/%%F?cb=!CB!"
)
findstr /C:"PRECISE FIBER HUNTER" precise_fiber_hunter.py >nul 2>&1 && echo   (on the latest version) || echo   (could not refresh -- running the copy you have)

echo.
echo  Enter your ZIP codes when it asks -- OKC, Houston, anywhere.
echo.
set "PYCMD=python"
where py >nul 2>&1 && set "PYCMD=py"

:runloop
%PYCMD% precise_fiber_hunter.py %*
set "RC=%ERRORLEVEL%"
if "%RC%"=="0" goto :eof
if "%RC%"=="42" (
  echo   It locked up -- restarting automatically...
) else (
  echo   It stopped ^(code %RC%^) -- restarting automatically...
)
set "OPTIMUS_AUTORESUME=1"
timeout /t 5 >nul
goto runloop
