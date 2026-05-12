#!/usr/bin/env python3
import time, json, urllib.request
from pathlib import Path

VERSION="3.0"
SHEET_ID="12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag"
COMMAND_TAB="COMMAND"
MAKE_WEBHOOK_URL="https://hook.us2.make.com/l7c1hoy97i41rh6u8rvgoi0gtwqpxumk"
POLL_INTERVAL=30
CREDS_CANDIDATES=[
    Path("google_creds.json"),
    Path("C:/Users/patri/OneDrive/Desktop/google_creds.json"),
    Path.home()/"OneDrive"/"Desktop"/"google_creds.json",
    Path("/storage/emulated/0/Download/google_creds.json"),
]
SCOPES=["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
_last_cmd={"val":"IDLE"}
_gc=None

def _find_creds():
    for p in CREDS_CANDIDATES:
        if p.exists(): return str(p)
    return None

def _get_client():
    global _gc
    if _gc: return _gc
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        cp=_find_creds()
        if not cp: print("  [cmd] ERR: creds not found"); return None
        _gc=gspread.authorize(Credentials.from_service_account_file(cp,scopes=SCOPES))
        return _gc
    except Exception as e:
        print(f"  [cmd] auth err: {e}"); return None

def _tab(sh):
    try: return sh.worksheet(COMMAND_TAB)
    except:
        ws=sh.add_worksheet(title=COMMAND_TAB,rows=5,cols=5)
        ws.update("A1",[["IDLE"]]); ws.update("A2",[["# IDLE/RUN_MAPMAN/RUN_HUNTER/STOP"]])
        print("  [cmd] Created COMMAND tab"); return ws

def check_command():
    try:
        gc=_get_client()
        if not gc: return ("IDLE","")
        row=_tab(gc.open_by_key(SHEET_ID)).row_values(1)
        raw=(row[0].strip() if row else "")or"IDLE"
        cmd,param=(raw.split(":",1) if ":" in raw else (raw,""))
        cmd=cmd.strip().upper(); param=param.strip()
        if cmd!=_last_cmd["val"]: print(f"  [cmd] -> {cmd} {param}"); _last_cmd["val"]=cmd
        return (cmd,param)
    except Exception as e:
        print(f"  [cmd] err: {e}"); return ("IDLE","")

def ack_command(status="DONE"):
    try:
        gc=_get_client()
        if gc: gc.open_by_key(SHEET_ID).worksheet(COMMAND_TAB).update("C1",[[status]])
    except Exception as e: print(f"  [cmd] ack err: {e}")

def notify_make(stats):
    try:
        req=urllib.request.Request(MAKE_WEBHOOK_URL,
            data=json.dumps(stats).encode(),method="POST",
            headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(req,timeout=10) as r:
            print(f"  [cmd] Make OK ({r.status})")
    except Exception as e: print(f"  [cmd] Make err: {e}")

if __name__=="__main__":
    print(f"drive_commander v{VERSION} -- test")
    cp=_find_creds(); print(f"Creds: {cp or 'NOT FOUND'}")
    if cp:
        cmd,param=check_command(); print(f"Sheet COMMAND A1={cmd!r}")
        notify_make({"test":True,"version":VERSION})
        print("Ready. Control: ATT FIBER LEADS -> COMMAND tab -> A1")
