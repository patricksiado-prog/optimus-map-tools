# -*- coding: utf-8 -*-
"""Proves the runner does what it claims BEFORE it goes near a laptop."""
import os, sys, json, shutil, tempfile, socket

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

TMP = tempfile.mkdtemp()
CC = os.path.join(TMP, "OPTIMUS COMMAND CENTER")
os.makedirs(CC)
os.environ["OPTIMUS_COMMAND_CENTER"] = CC

import optimus_runner as R

MACHINE = socket.gethostname()
LAUNCHED = []

# Stub the two things that touch the real OS.
R.already_running = lambda needle: False
class FakePopen:
    def __init__(self, argv, cwd=None, shell=False):
        assert shell is False, "shell=True would allow injection"
        LAUNCHED.append(("popen", list(argv), cwd))
R.subprocess.Popen = FakePopen
def fake_check_output(argv, cwd=None, shell=False, **kw):
    assert shell is False, "shell=True would allow injection"
    LAUNCHED.append(("run", list(argv), cwd))
    return "FAKE OUTPUT for %s" % " ".join(argv)
R.subprocess.check_output = fake_check_output
# Pretend the tool folders exist.
for d in (R._hunter_dir(), R._scraper_dir(), R._launchers()):
    os.makedirs(d, exist_ok=True)
for b in ("RUN_SCRAPER.bat", "RUN_HUNTER.bat"):
    open(os.path.join(R._launchers(), b), "w").write("rem")

fails = []
def check(name, cond, extra=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + ("" if cond else "  <- " + str(extra)))
    if not cond: fails.append(name)

def write_orders(orders):
    json.dump({"orders": orders}, open(os.path.join(CC, "ORDERS.json"), "w"))

def result():
    p = os.path.join(CC, "RESULT-%s.json" % MACHINE)
    return json.load(open(p)) if os.path.exists(p) else None

print("\nTEST 1 -- an order for THIS machine is carried out")
write_orders([{"id": "o1", "machine": MACHINE, "action": "run_scraper"}])
R.main()
check("scraper launched", any(x[0] == "popen" for x in LAUNCHED), LAUNCHED)
check("result file written", result() is not None)
check("reported as ok", result()["carried_out"][0]["ok"] is True, result())

print("\nTEST 2 -- the SAME order does not run a second time")
n = len(LAUNCHED)
R.main(); R.main(); R.main()
check("still only launched once", len(LAUNCHED) == n, "%d -> %d" % (n, len(LAUNCHED)))

print("\nTEST 3 -- an order for a DIFFERENT machine is ignored")
write_orders([{"id": "o2", "machine": "SOMEBODY-ELSES-PC", "action": "run_hunter"}])
n = len(LAUNCHED); R.main()
check("not carried out", len(LAUNCHED) == n)

print("\nTEST 4 -- machine 'any' is carried out here")
write_orders([{"id": "o3", "machine": "any", "action": "territory"}])
R.main()
check("territory ran", any("--territory" in x[1] for x in LAUNCHED if x[0] == "run"), LAUNCHED)

print("\nTEST 5 -- ARBITRARY COMMANDS ARE IMPOSSIBLE (the whole safety story)")
write_orders([
    {"id": "bad1", "machine": MACHINE, "action": "del C:\\Windows\\System32"},
    {"id": "bad2", "machine": MACHINE, "action": "cmd", "args": {"c": "format c:"}},
    {"id": "bad3", "machine": MACHINE, "action": "run_scraper; rm -rf /"},
])
n = len(LAUNCHED); R.main()
check("none of the 3 executed", len(LAUNCHED) == n, LAUNCHED[n:])
outs = {c["id"]: c for c in result()["carried_out"]}
check("each rejected as unknown action",
      all(not outs[i]["ok"] and "unknown action" in outs[i]["detail"] for i in ("bad1","bad2","bad3")),
      outs)

print("\nTEST 6 -- an order with a missing argument fails cleanly, does not crash")
write_orders([{"id": "o4", "machine": MACHINE, "action": "claim"}])
R.main()
c = [x for x in result()["carried_out"] if x["id"] == "o4"][0]
check("claim without an area is rejected", (not c["ok"]) and "area" in c["detail"], c)

print("\nTEST 7 -- a real claim passes the area through as ONE argv element")
write_orders([{"id": "o5", "machine": MACHINE, "action": "claim",
               "args": {"area": "Angleton, TX"}}])
R.main()
got = [x for x in LAUNCHED if x[0] == "run" and "--claim" in x[1]][-1]
check("argv is exact", got[1] == ["py", "precise_fiber_hunter.py", "--claim", "Angleton, TX"], got)

print("\nTEST 8 -- 'already running' means do not open a second window")
R.already_running = lambda needle: True
write_orders([{"id": "o6", "machine": MACHINE, "action": "run_scraper"}])
n = len(LAUNCHED); R.main()
c = [x for x in result()["carried_out"] if x["id"] == "o6"][0]
check("nothing launched", len(LAUNCHED) == n)
check("reported as already running", c["ok"] and "already running" in c["detail"], c)
R.already_running = lambda needle: False

print("\nTEST 9 -- no folder at all: silent, no crash, exit 0")
os.environ["OPTIMUS_COMMAND_CENTER"] = os.path.join(TMP, "does-not-exist")
_real = R.find_folder
R.find_folder = lambda: None
check("returns 0", R.main() == 0)
R.find_folder = _real
os.environ["OPTIMUS_COMMAND_CENTER"] = CC

print("\nTEST 10 -- a corrupt ORDERS.json does not crash the runner")
open(os.path.join(CC, "ORDERS.json"), "w").write("{ this is not json ,,,")
check("returns 0", R.main() == 0)

print("\n" + ("ALL PASS" if not fails else "FAILED: %s" % fails))
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(1 if fails else 0)
