# The runner — letting Claude start work on a PC

**Status: BUILT AND TESTED. NOT DEPLOYED. Needs Patrick's go (RULE 0).**

## The problem

A Google Drive folder is passive. Files do not execute. When the hunter and the
scraper are both stopped, nothing on that laptop is listening, so nothing Claude
writes anywhere can start them.

## The fix

`optimus_runner.py` (292 lines). Windows Task Scheduler runs it every 5 minutes.
It reads `ORDERS.json` from `OPTIMUS COMMAND CENTER`, carries out any order
addressed to this machine, and writes `RESULT-<hostname>.json` back.

## Why it is not a new program

Patrick's rule: *"i don't wanna run any more programs ... unless I don't have to
mess w them and nobody does."* Nobody launches this. Task Scheduler fires it
invisibly, forever. There is no icon, no link, and nothing to remember.

And it needs **no new installer**: `optimus_runner.py` goes in the hunter's
`_CORE_FILES` (so it self-deploys to every PC at launch) and the registration
snippet goes in `install/RUN_HUNTER.bat` and `install/RUN_SCRAPER.bat` — which
the *existing* `INSTALL_OPTIMUS.bat` already downloads on every run. Every copy
of the installer already in circulation picks it up.

## The vocabulary — the whole safety story

It will only run these. It will never execute a string from a file.

| action | args | what it does |
|---|---|---|
| `run_scraper` | — | launches the Maps Scraper |
| `run_hunter` | — | launches the Fiber Hunter |
| `claim` | `area` | claims territory for this machine |
| `release` | `area` | gives it back |
| `territory` | — | prints the board |
| `gold_audit` | — | unique gold ADDRESSES |
| `decode_gold` | — | which gold dots are real upgrades |
| `sheet_feed` | `tab` | publishes a whole tab for Claude to read |

Anything else is rejected as `unknown action`. Tested.

## ORDERS.json

```json
{"orders": [
  {"id": "2026-09-05-a", "machine": "LAPTOP-67UOPK24", "action": "run_hunter"},
  {"id": "2026-09-05-b", "machine": "any", "action": "claim",
   "args": {"area": "Angleton, TX"}}
]}
```

`id` must be unique — it is how "run once, ever" works.

## What it cannot do

1. **Get past the AT&T login.** It launches the hunter into the chooser; a human
   finishes it. (Auto re-login is a separate, authorised change.)
2. **Press Ctrl+Up on an already-running paused hunter.** A watcher cannot inject
   keystrokes into a live process. That needs the hunter to poll a resume file —
   a second small change, deliberately not folded in here.

## Test

`py test_runner.py` → **ALL PASS** (10 checks), including three attempted
command injections, all rejected.
