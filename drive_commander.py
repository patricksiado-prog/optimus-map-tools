#!/usr/bin/env python3
"""
drive_commander.py  v3.2
========================
Polling daemon. Reads ATT FIBER LEADS COMMAND tab every 30s.
Launches themapman.py with params from B1 when A1 = RUN_MAPMAN.

COMMAND tab:
  A1 = IDLE / RUN_MAPMAN / STOP
  B1 = params  e.g. --commercial-only --city "Austin" --no-pick
  C1 = status  (written back automatically)

Run from Desktop:
  python drive_commander.py
  python drive_commander.py --test
"""

VERSION          = "3.2"
SHEET_ID         = "12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag"
COMMAND_TAB      = "COMMAND"
MAKE_WEBHOOK_URL = "https://hook.us2.make.com/l7c1hoy97i41rh6u8rvgoi0gtwqpxumk"
MAPMAN_SCRIPT    = "themapman.py"
POLL_INTERVAL    = 30

import os, sys, re, time, json, shlex, subprocess, urllib.request, argparse
from pathlib import Path

# v3.2: search all common creds locations
CREDS_CANDIDATES = [
    Path("google_creds.json"),
    Path("C:/Users/patri/OneDrive/Desktop/google_creds.json"),
    Path("C:/Users/patri/Desktop/google_creds.json"),
    Path.home() / "OneDrive" / "Desktop" / "google_creds.json",
    Path.home() / "Desktop" / "google_creds.json",
    Path("/storage/emulated/0/Download/google_creds.json"),
]
SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

_last_cmd    = {"val": "IDLE"}
_gc          = None
_mapman_proc = {"proc": None}


def _find_creds():
    for p in CREDS_CANDIDATES:
        if p.exists():
            # v3.2: auto-cd to wherever creds live so relative paths work
            creds_dir = str(p.parent.resolve())
            cwd       = str(Path.cwd().resolve())
            if creds_dir != cwd:
                try:
                    os.chdir(creds_dir)
                    print(f"  [commander] cd -> {creds_dir}")
                except Exception:
                    pass
            return str(p)
    return None


def _get_client():
    global _gc
    if _gc is not None:
        return _gc
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        cp = _find_creds()
        if not cp:
            print("  [commander] ERR: google_creds.json not found")
            return None
        creds = Credentials.from_service_account_file(cp, scopes=SCOPES)
        _gc   = gspread.authorize(creds)
        return _gc
    except Exception as e:
        print(f"  [commander] auth error: {e}")
        return None


def _get_or_create_tab(sh):
    try:
        return sh.worksheet(COMMAND_TAB)
    except Exception:
        ws = sh.add_worksheet(title=COMMAND_TAB, rows=5, cols=5)
        ws.update("A1", [["IDLE"]])
        ws.update("A2", [["# IDLE / RUN_MAPMAN / STOP"]])
        ws.update("B2", [["# params: --commercial-only --city Austin --no-pick"]])
        print("  [commander] Created COMMAND tab")
        return ws


def check_command():
    try:
        gc  = _get_client()
        if not gc: return ("IDLE", "")
        sh  = gc.open_by_key(SHEET_ID)
        tab = _get_or_create_tab(sh)
        row = tab.row_values(1)
        raw = (row[0].strip() if row else "") or "IDLE"
        params = row[1].strip() if len(row) > 1 else ""
        params = " ".join(p for p in params.split() if not p.startswith("#"))
        if ":" in raw:
            cmd, extra = raw.split(":", 1)
            params = extra.strip() + (" " + params if params else "")
        else:
            cmd = raw
        cmd = cmd.strip().upper()
        if cmd != _last_cmd["val"]:
            print(f"  [commander] -> {cmd}  params={params!r}")
            _last_cmd["val"] = cmd
        return (cmd, params.strip())
    except Exception as e:
        print(f"  [commander] read error: {e}")
        return ("IDLE", "")


def ack(status):
    try:
        gc  = _get_client()
        if not gc: return
        sh  = gc.open_by_key(SHEET_ID)
        tab = sh.worksheet(COMMAND_TAB)
        tab.update("C1", [[status]])
    except Exception as e:
        print(f"  [commander] ack error: {e}")


def reset_idle():
    try:
        gc  = _get_client()
        if not gc: return
        sh  = gc.open_by_key(SHEET_ID)
        tab = sh.worksheet(COMMAND_TAB)
        tab.update("A1", [["IDLE"]])
        _last_cmd["val"] = "IDLE"
    except Exception as e:
        print(f"  [commander] reset error: {e}")


def notify_make(stats: dict):
    try:
        body = json.dumps(stats).encode()
        req  = urllib.request.Request(
            MAKE_WEBHOOK_URL, data=body, method="POST",
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            print(f"  [commander] Make OK ({r.status})")
    except Exception as e:
        print(f"  [commander] Make error: {e}")


def launch_mapman(params_str):
    script = Path(MAPMAN_SCRIPT)
    if not script.exists():
        script = Path(__file__).parent / MAPMAN_SCRIPT
    if not script.exists():
        print(f"  [commander] ERR: {MAPMAN_SCRIPT} not found")
        ack(f"ERROR: {MAPMAN_SCRIPT} not found")
        return None
    try:
        extra = shlex.split(params_str) if params_str else []
    except ValueError:
        extra = params_str.split() if params_str else []
    if "--no-spawn" not in extra: extra.append("--no-spawn")
    if "--no-pick"  not in extra: extra.append("--no-pick")
    cmd = [sys.executable, str(script)] + extra
    print(f"  [commander] Launching: {' '.join(cmd)}")
    kwargs = {}
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NEW_CONSOLE
    try:
        proc = subprocess.Popen(cmd, **kwargs)
        print(f"  [commander] PID {proc.pid}")
        ack(f"RUNNING pid={proc.pid}")
        return proc
    except Exception as e:
        print(f"  [commander] launch error: {e}")
        ack(f"ERROR: {e}")
        return None


def run_loop(once=False):
    print(f"\ndrive_commander v{VERSION} — {'one-shot' if once else 'daemon'}")
    print(f"Sheet: {SHEET_ID}  Tab: {COMMAND_TAB}")
    print(f"Poll: {POLL_INTERVAL}s  |  Set A1=RUN_MAPMAN B1=params to launch")
    print("Waiting for commands...\n")
    while True:
        cmd, params = check_command()
        if cmd in ("RUN_MAPMAN", "RUN_HUNTER"):
            proc = _mapman_proc["proc"]
            if proc and proc.poll() is None:
                print(f"  [commander] Already running PID {proc.pid}")
            else:
                _mapman_proc["proc"] = launch_mapman(params)
        elif cmd == "STOP":
            proc = _mapman_proc["proc"]
            if proc and proc.poll() is None:
                ack("STOP_SENT")
            else:
                ack("IDLE")
            reset_idle()
        proc = _mapman_proc["proc"]
        if proc and proc.poll() is not None:
            rc = proc.returncode
            print(f"  [commander] PID {proc.pid} done (rc={rc})")
            notify_make({"script":"mapman","rc":rc,"params":params})
            ack(f"DONE rc={rc}")
            reset_idle()
            _mapman_proc["proc"] = None
        if once: break
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=f"drive_commander v{VERSION}")
    p.add_argument("--once", action="store_true")
    p.add_argument("--test", action="store_true")
    args = p.parse_args()
    if args.test:
        print(f"drive_commander v{VERSION} — test")
        cp = _find_creds()
        print(f"Creds: {cp or 'NOT FOUND'}")
        if cp:
            cmd, params = check_command()
            print(f"COMMAND A1={cmd!r}  B1={params!r}")
            notify_make({"test": True})
            print("OK — commander is ready.")
    else:
        run_loop(once=args.once)
