#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OPTIMUS RUNNER -- the thing that lets Claude start work on this PC.

It is NOT a program anybody launches. Windows Task Scheduler runs it every few
minutes, it looks in the OPTIMUS COMMAND CENTER folder (synced by Google Drive
for Desktop), and if there is an order addressed to THIS machine it carries it
out and writes the result back into the same folder.

DESIGN RULES, and they are the whole point:

  * FIXED VOCABULARY. It will only ever run actions from ACTIONS below. It will
    never execute an arbitrary string out of a file. A mistake in an order can
    therefore never do anything worse than launch a tool that was already on
    this PC.
  * EVERY ORDER RUNS ONCE. Order ids are recorded in _runner_done.json. A file
    that sits in the folder for a week does not relaunch the scraper every five
    minutes.
  * IT NEVER RAISES. Task Scheduler jobs that crash get disabled by Windows and
    then nothing works and nobody knows why. Every failure is caught, written to
    the result file, and reported as a failed order.
  * IT NEVER STARTS A SECOND COPY. If the scraper is already running, the order
    to run the scraper reports "already running" instead of opening a fifth
    window.
"""

import os
import sys
import json
import time
import socket
import subprocess

MACHINE = socket.gethostname()
HOME = os.path.expanduser("~")
HERE = os.path.dirname(os.path.abspath(__file__))

FOLDER_NAME = "OPTIMUS COMMAND CENTER"
ORDERS_FILE = "ORDERS.json"
DONE_FILE = "_runner_done.json"
MAX_DONE = 500          # keep the ledger from growing forever
HEARTBEAT_EVERY = 3600  # write a result file at least hourly even with no orders


# --------------------------------------------------------------------------
# Finding the synced folder. Google Drive for Desktop mounts either as a drive
# letter (G:\My Drive\...) or under the profile, and the letter is not stable
# across machines -- so look, do not assume.
# --------------------------------------------------------------------------
def find_folder():
    cands = []
    for base in (HOME, os.path.join(HOME, "Documents")):
        for mid in ("My Drive", "Google Drive", os.path.join("Google Drive", "My Drive")):
            cands.append(os.path.join(base, mid, FOLDER_NAME))
    for letter in "GHIJKLMNOPQRSTUVWXYZ":
        cands.append("%s:\\My Drive\\%s" % (letter, FOLDER_NAME))
        cands.append("%s:\\%s" % (letter, FOLDER_NAME))
    env = os.environ.get("OPTIMUS_COMMAND_CENTER")
    if env:
        cands.insert(0, env)
    for c in cands:
        try:
            if os.path.isdir(c):
                return c
        except Exception:
            pass
    return None


# --------------------------------------------------------------------------
# The vocabulary. Each entry returns (argv, cwd, detached).
# detached=True means "launch it and leave it running" (the scraper and the
# hunter run for hours). detached=False means "run it and capture the output".
# --------------------------------------------------------------------------
def _hunter_dir():
    return os.path.join(HOME, "optimus_hunter")


def _scraper_dir():
    return os.path.join(HOME, "maps_scraper")


def _launchers():
    return os.path.join(HOME, "optimus", "launchers")


def act_run_scraper(args):
    bat = os.path.join(_launchers(), "RUN_SCRAPER.bat")
    if not os.path.exists(bat):
        return None, None, False, "RUN_SCRAPER.bat not on this PC (%s)" % bat
    return ["cmd", "/c", "start", "", bat], _launchers(), True, None


def act_run_hunter(args):
    bat = os.path.join(_launchers(), "RUN_HUNTER.bat")
    if not os.path.exists(bat):
        return None, None, False, "RUN_HUNTER.bat not on this PC (%s)" % bat
    return ["cmd", "/c", "start", "", bat], _launchers(), True, None


def act_claim(args):
    area = (args or {}).get("area") or ""
    if not area:
        return None, None, False, "claim needs an 'area'"
    return (["py", "precise_fiber_hunter.py", "--claim", area],
            _hunter_dir(), False, None)


def act_release(args):
    area = (args or {}).get("area") or ""
    if not area:
        return None, None, False, "release needs an 'area'"
    return (["py", "precise_fiber_hunter.py", "--release", area],
            _hunter_dir(), False, None)


def act_territory(args):
    return (["py", "precise_fiber_hunter.py", "--territory"],
            _hunter_dir(), False, None)


def act_gold_audit(args):
    return ["py", "gold_audit.py"], _hunter_dir(), False, None


def act_decode_gold(args):
    return ["py", "decode_gold.py"], _hunter_dir(), False, None


def act_sheet_feed(args):
    tab = (args or {}).get("tab") or ""
    if not tab:
        return None, None, False, "sheet_feed needs a 'tab'"
    return ["py", "sheet_feed.py", "--tab", tab], _hunter_dir(), False, None


ACTIONS = {
    "run_scraper": act_run_scraper,
    "run_hunter": act_run_hunter,
    "claim": act_claim,
    "release": act_release,
    "territory": act_territory,
    "gold_audit": act_gold_audit,
    "decode_gold": act_decode_gold,
    "sheet_feed": act_sheet_feed,
}


# --------------------------------------------------------------------------
# "is it already running" -- so a repeated order cannot open five windows.
# --------------------------------------------------------------------------
def already_running(needle):
    try:
        out = subprocess.check_output(
            ["wmic", "process", "get", "CommandLine"],
            stderr=subprocess.STDOUT, universal_newlines=True)
    except Exception:
        return False        # cannot tell -> do not block the order
    hits = [l for l in out.splitlines() if needle.lower() in l.lower()]
    return len(hits) > 0


BUSY_NEEDLE = {
    "run_scraper": "maps_scraper_standalone.py",
    "run_hunter": "precise_fiber_hunter.py",
}


def load_json(path, default):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, obj):
    try:
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(obj, f, indent=1)
        if os.path.exists(path):
            os.remove(path)
        os.rename(tmp, path)
        return True
    except Exception:
        return False


def run_one(order):
    """Carry out a single order. Never raises."""
    action = str(order.get("action") or "").strip()
    args = order.get("args") or {}
    if action not in ACTIONS:
        return {"ok": False, "detail": "unknown action %r -- allowed: %s"
                % (action, ", ".join(sorted(ACTIONS)))}

    needle = BUSY_NEEDLE.get(action)
    if needle and already_running(needle):
        return {"ok": True, "detail": "already running on this PC -- nothing to do"}

    try:
        argv, cwd, detached, err = ACTIONS[action](args)
    except Exception as e:
        return {"ok": False, "detail": "could not build the command: %s" % e}
    if err:
        return {"ok": False, "detail": err}
    if cwd and not os.path.isdir(cwd):
        return {"ok": False, "detail": "folder missing on this PC: %s" % cwd}

    try:
        if detached:
            subprocess.Popen(argv, cwd=cwd, shell=False)
            return {"ok": True, "detail": "launched"}
        out = subprocess.check_output(argv, cwd=cwd, shell=False,
                                      stderr=subprocess.STDOUT,
                                      universal_newlines=True, timeout=900)
        return {"ok": True, "detail": "ran", "output": out[-4000:]}
    except subprocess.CalledProcessError as e:
        return {"ok": False, "detail": "exit %s" % e.returncode,
                "output": (e.output or "")[-4000:]}
    except Exception as e:
        return {"ok": False, "detail": str(e)[:300]}


def main():
    folder = find_folder()
    if not folder:
        # Nothing to do and nothing to report to -- Drive is not installed yet.
        return 0

    orders_path = os.path.join(folder, ORDERS_FILE)
    done_path = os.path.join(folder, DONE_FILE)
    result_path = os.path.join(folder, "RESULT-%s.json" % MACHINE)

    done = load_json(done_path, {})
    if not isinstance(done, dict):
        done = {}
    mine_done = done.get(MACHINE) or []

    doc = load_json(orders_path, None)
    orders = []
    if isinstance(doc, dict):
        orders = doc.get("orders") or []
    elif isinstance(doc, list):
        orders = doc

    carried = []
    for o in orders:
        if not isinstance(o, dict):
            continue
        target = str(o.get("machine") or "any")
        if target != "any" and target.lower() != MACHINE.lower():
            continue
        oid = str(o.get("id") or "")
        if not oid:
            continue                      # an order with no id is not runnable
        if oid in mine_done:
            continue                      # already carried out
        res = run_one(o)
        res["id"] = oid
        res["action"] = o.get("action")
        res["at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        carried.append(res)
        mine_done.append(oid)

    if carried:
        done[MACHINE] = mine_done[-MAX_DONE:]
        save_json(done_path, done)

    prev = load_json(result_path, {})
    last = prev.get("checked_at_epoch") or 0
    if carried or (time.time() - last) > HEARTBEAT_EVERY:
        save_json(result_path, {
            "machine": MACHINE,
            "checked_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "checked_at_epoch": int(time.time()),
            "folder": folder,
            "orders_seen": len(orders),
            "carried_out": carried,
            "scraper_running": already_running("maps_scraper_standalone.py"),
            "hunter_running": already_running("precise_fiber_hunter.py"),
        })
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)          # never let Task Scheduler mark this job failed
