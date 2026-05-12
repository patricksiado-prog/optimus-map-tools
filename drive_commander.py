#!/usr/bin/env python3
"""
drive_commander.py  v2.0
========================
Drop on Desktop alongside themapman.py and fiber_hunter.py.
Reads commands from MAPMAN_COMMAND Google Doc.
Notifies Make webhook when runs finish.

COMMAND DOC ID: 1lSL22B5i195Qw63cJXrMs4ogYwxTyxJHviGJ0abL7bs

Valid commands (write one of these in the doc, save):
  IDLE                        - do nothing (default)
  RUN_MAPMAN                  - mapman enriches all cities
  RUN_MAPMAN:Houston,Bellaire - mapman with city filter
  STOP                        - stop after current row

MAKE WEBHOOK:
  https://hook.us2.make.com/l7c1hoy97i41rh6u8rvgoi0gtwqpxumk
"""

import time, json, urllib.request
from pathlib import Path

COMMAND_DOC_ID   = "1lSL22B5i195Qw63cJXrMs4ogYwxTyxJHviGJ0abL7bs"
MAKE_WEBHOOK_URL = "https://hook.us2.make.com/l7c1hoy97i41rh6u8rvgoi0gtwqpxumk"
POLL_INTERVAL    = 30

CREDS_CANDIDATES = [
    Path("google_creds.json"),
    Path("C:/Users/patri/OneDrive/Desktop/google_creds.json"),
    Path.home() / "OneDrive" / "Desktop" / "google_creds.json",
    Path("/storage/emulated/0/Download/google_creds.json"),
]

_last_cmd = {"val": "IDLE"}
_token    = {"val": None, "exp": 0}


def _find_creds():
    for p in CREDS_CANDIDATES:
        if p.exists():
            return str(p)
    return None


def _get_token():
    now = time.time()
    if _token["val"] and now < _token["exp"] - 60:
        return _token["val"]
    try:
        from google.oauth2.service_account import Credentials
        import google.auth.transport.requests
        creds_path = _find_creds()
        if not creds_path:
            print("  [commander] ERR: google_creds.json not found")
            return None
        creds = Credentials.from_service_account_file(
            creds_path,
            scopes=["https://www.googleapis.com/auth/drive.readonly"]
        )
        creds.refresh(google.auth.transport.requests.Request())
        _token["val"] = creds.token
        _token["exp"] = now + 3500
        return creds.token
    except Exception as e:
        print(f"  [commander] token error: {e}")
        return None


def check_command():
    try:
        token = _get_token()
        if not token:
            return ("IDLE", "")
        url = (f"https://www.googleapis.com/drive/v3/files/"
               f"{COMMAND_DOC_ID}/export?mimeType=text/plain")
        req = urllib.request.Request(
            url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req, timeout=10) as r:
            text = r.read().decode("utf-8").strip()
        text = next((ln.strip() for ln in text.splitlines() if ln.strip()), "IDLE")
        if ":" in text:
            cmd, param = text.split(":", 1)
        else:
            cmd, param = text, ""
        cmd   = cmd.strip().upper()
        param = param.strip()
        if cmd != _last_cmd["val"]:
            print(f"  [commander] -> {cmd}  param={param!r}")
            _last_cmd["val"] = cmd
        return (cmd, param)
    except Exception as e:
        print(f"  [commander] read error: {e}")
        return ("IDLE", "")


def notify_make(stats: dict):
    try:
        body = json.dumps(stats).encode("utf-8")
        req  = urllib.request.Request(
            MAKE_WEBHOOK_URL, data=body, method="POST",
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            print(f"  [commander] Make notified OK ({r.status})")
    except Exception as e:
        print(f"  [commander] Make notify error: {e}")


if __name__ == "__main__":
    print("drive_commander.py v2.0 -- connection test")
    creds = _find_creds()
    print(f"Creds : {creds or 'NOT FOUND -- put google_creds.json on Desktop'}")
    if creds:
        cmd, param = check_command()
        print(f"Doc   : {cmd!r}  param={param!r}")
        print("Make  : sending test ping...")
        notify_make({"test": True, "message": "drive_commander v2.0 connected"})
        print("OK -- commander is ready.")
    else:
        print("Fix creds path first, then run again.")
