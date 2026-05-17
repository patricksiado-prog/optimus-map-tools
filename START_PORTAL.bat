@echo off
title OPTIMUS SERVER
cd /d "%USERPROFILE%\Desktop"
echo Fixing server file...
python -c "import urllib.request; urllib.request.urlretrieve('https://raw.githubusercontent.com/patricksiado-prog/optimus-map-tools/main/optimus_server.py', '%USERPROFILE%\Desktop\optimus_server.py'); print('[OK] server ready')"
echo Starting...
python "%USERPROFILE%\Desktop\optimus_server.py"
pause
