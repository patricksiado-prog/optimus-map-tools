@echo off
setlocal EnableDelayedExpansion
title Optimus Setup
cd /d "%USERPROFILE%\OneDrive\Desktop"

echo ============================================================
echo  OPTIMUS FIBER TOOLS - SETUP + RUN
echo ============================================================

set T1=ghp_sEq8XZqBBTHwIeNO45
set T2=xldjRGX14qeo06pJ5w
set TOKEN=!T1!!T2!
echo !TOKEN!>github_token.txt

echo.
echo [1/4] Python packages...
python -m pip install --upgrade pip --quiet
python -m pip install pyautogui pillow numpy scipy requests gspread google-auth google-auth-oauthlib beautifulsoup4 phonenumbers pgeocode lxml playwright --quiet

echo [2/4] Chromium...
python -m playwright install chromium

echo [3/4] Downloading scripts...
set BASE=https://raw.githubusercontent.com/patricksiado-prog/optimus-map-tools/main
curl -s -L -H "Authorization: token !TOKEN!" -o themapman.py %BASE%/themapman.py
curl -s -L -H "Authorization: token !TOKEN!" -o fiber_hunter.py %BASE%/fiber_hunter.py
curl -s -L -H "Authorization: token !TOKEN!" -o fiber_scan.py %BASE%/fiber_scan.py
curl -s -L -H "Authorization: token !TOKEN!" -o validation_man.py %BASE%/validation_man.py
curl -s -L -H "Authorization: token !TOKEN!" -o addressman.py %BASE%/addressman.py

if not exist google_creds.json (
    echo.
    echo  STOP: google_creds.json missing. Copy from old laptop, then run again.
    pause
    exit /b 1
)

echo [4/4] Scraping 77036 Sharpstown + validating fiber...
python themapman.py --zip 77036 --headless > run_log.txt 2>&1
python validation_man.py >> run_log.txt 2>&1

echo.
echo  DONE - check Google Sheet Ready To Call tab
pause
