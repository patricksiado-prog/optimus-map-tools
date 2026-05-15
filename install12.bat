@echo off
REM ============================================================
REM  OPTIMUS MAP TOOLS - INSTALLER v12
REM  Repo: patricksiado-prog/optimus-map-tools (PUBLIC)
REM  Skips pip install. Downloads only verified files.
REM ============================================================
setlocal enabledelayedexpansion

set REPO=patricksiado-prog/optimus-map-tools
set BRANCH=main
set INSTALL_DIR=%USERPROFILE%\Optimus
set RAW=https://raw.githubusercontent.com/%REPO%/%BRANCH%

echo ============================================================
echo   OPTIMUS MAP TOOLS - INSTALLER v12
echo ============================================================
echo Install location: %INSTALL_DIR%
echo.

REM -- 1. CHECK PYTHON --
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH.
    echo Install from https://www.python.org/downloads/ and re-run.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo Found: %%v
echo.

REM -- 2. CREATE INSTALL DIR --
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
cd /d "%INSTALL_DIR%"
echo Working dir: %CD%
echo.

REM -- 3. DOWNLOAD VERIFIED FILES ONLY --
echo Installing scripts from repo...
set SOURCE_DIR=%~dp0
set FILES=fiber_scan.py fiber_hunter.py themapman.py addressman.py slow_hunter.py cleaner.py update.bat

for %%F in (%FILES%) do (
    if exist "%SOURCE_DIR%%%F" (
        echo   %%F  [local]
        copy /Y "%SOURCE_DIR%%%F" "%INSTALL_DIR%\%%F" >nul
    ) else (
        echo   %%F  [GitHub]
        powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri '%RAW%/%%F' -OutFile '%INSTALL_DIR%\%%F' -UseBasicParsing" 2>nul
        if errorlevel 1 (
            echo     FAILED - %RAW%/%%F does not exist
            echo     Skipping.
        ) else (
            echo     OK
        )
    )
)
echo.

REM -- 4. DESKTOP SHORTCUTS --
echo Creating desktop shortcuts...
set DESK=%USERPROFILE%\Desktop
for %%S in (fiber_scan fiber_hunter themapman) do (
    if exist "%INSTALL_DIR%\%%S.py" (
        powershell -NoProfile -ExecutionPolicy Bypass -Command "$w=New-Object -ComObject WScript.Shell; $s=$w.CreateShortcut('%DESK%\%%S.lnk'); $s.TargetPath='python.exe'; $s.Arguments='"%INSTALL_DIR%\%%S.py"'; $s.WorkingDirectory='"%INSTALL_DIR%"'; $s.IconLocation='python.exe'; $s.Save()"
    )
)
echo Done.
echo.

REM -- 5. FINAL CHECKS --
echo ============================================================
echo   INSTALL COMPLETE
echo ============================================================
if not exist "%INSTALL_DIR%\google_creds.json" (
    echo   [ ] Copy google_creds.json to %INSTALL_DIR%
    echo       (Required for MapMan / fiber_scan)
) else (
    echo   [X] google_creds.json present
)
echo   [ ] GitHub token file: Desktop\github_token.txt or ./github_token.txt
echo   [ ] Ready. Run: python fiber_scan.py (or use desktop shortcuts)
echo.
pause
