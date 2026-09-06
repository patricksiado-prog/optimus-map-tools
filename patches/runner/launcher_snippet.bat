REM ===========================================================================
REM  OPTIMUS RUNNER -- one-time, self-registering. Paste into BOTH
REM  install/RUN_HUNTER.bat and install/RUN_SCRAPER.bat, after the download
REM  block and before the tool is launched.
REM
REM  Why here and not in a new installer: the existing INSTALL_OPTIMUS.bat
REM  downloads BOTH launchers from the repo on every run, so putting it here
REM  means every copy of the installer already in circulation picks it up.
REM  No new file, no new link, no new icon.
REM
REM  It is idempotent -- checks whether the task exists and does nothing if it
REM  does -- and it can never stop the launcher, because every line is
REM  swallowed. A PC with no Google Drive folder simply has a task that finds
REM  nothing and exits.
REM ===========================================================================
schtasks /query /tn "OptimusRunner" >nul 2>&1
if errorlevel 1 (
  echo   Registering the Optimus runner ^(checks for orders every 5 minutes^)...
  schtasks /create /tn "OptimusRunner" /sc minute /mo 5 /f ^
     /tr "py \"%USERPROFILE%\optimus_hunter\optimus_runner.py\"" >nul 2>&1
  if errorlevel 1 (
     echo   ^(runner not registered -- orders from the shared folder will not run
     echo    on this PC. Everything else works normally.^)
  ) else (
     echo   Runner registered. Claude can now start the tools on this PC.
  )
)
