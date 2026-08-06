@echo off
REM ============================================================
REM  OPTIMUS INSTALLER launcher -- double-click this.
REM  Runs optimus_install_pc.py from this same folder.
REM ============================================================
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel%==0 (
    python "%~dp0optimus_install_pc.py"
    goto end
)

where py >nul 2>nul
if %errorlevel%==0 (
    py "%~dp0optimus_install_pc.py"
    goto end
)

echo.
echo Python was not found on this PC.
echo Install Python from https://www.python.org/downloads/ ,
echo CHECK "Add python.exe to PATH" during install, then double-click this again.
echo.

:end
pause
