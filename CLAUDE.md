# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`optimus-map-tools` is the toolkit behind "Optimus Houston" — an AT&T fiber
door-to-door sales operation. It is **not a packaged application**: it is a flat
collection of standalone Python scripts that screenshot the AT&T fiber
availability map, detect colored dots on it, turn those dots into real street
addresses and business phone numbers, validate fiber serviceability, and write
everything into shared Google Sheets that feed a GoHighLevel (GHL) CRM.

There is no test suite, no build step, no package manifest, and no central entry
point. Each `*.py` file at the repo root is a self-contained tool that is copied
onto an operator's device (Windows laptop or an Android phone running **Pydroid
3**) and run directly with `python <tool>.py`. The repo root is effectively the
distribution surface — `install.bat`/`update.bat` and the in-script
auto-updaters pull individual files straight from
`raw.githubusercontent.com/.../main/<file>`.

## The pipeline (the big picture)

The dot colors are the heart of the domain. On the AT&T map:
- **GREEN** = fiber-eligible, not yet an AT&T customer → prime cold-pitch target
- **ORANGE/RED** = fiber-eligible copper customer → forced-upgrade target
- **GREY** = existing fiber customer → upgrade/referral target
- **BLUE** = less common, fiber upgrade available

Data flows in four stages, each a different script, glued together only by the
shared Google Sheet (not by imports):

1. **Capture + detect** — `fiber_hunter.py` (primary, v5.7), `fiber_scan.py`,
   `slow_hunter.py`, and the standalone `FIBERHUNTER` drive a real browser via
   `pyautogui` (pan the map, click "Search this area", screenshot), then use
   `numpy`/`scipy.ndimage` connected-component detection to find and classify
   dots by **saturation-based color matching** (never exact RGB).
2. **Pixel → address** — `hunter_dot_extractor.py` converts screenshot dots to
   lat/lon (per-tile affine bounds) and reverse-geocodes via **Nominatim**
   (hard 1 req/sec limit; `time.sleep(1.1)` between calls) with **Photon** as
   fallback, caching to `geocode_cache.json`.
3. **Address → phone/business** — `mapman_api.py`, `mapman_api_batch.py`,
   `themapman.py` (v11.2.5), and `mapman_pydroid_runner.py` enrich addresses to
   business names and phones via the **Google Places API**. `addressman.py` and
   `validatorman.py` add nearby-business discovery and AT&T fiber-status
   validation. `build_dedup_tab.py` de-duplicates leads into per-metro tabs.
4. **Maintenance / orchestration** — `cleaner.py` and `hunter_reclassifier_safe.py`
   keep the sheet under the 10M-cell limit and fix dot classifications;
   `drive_commander.py` and `optimus_server.py` are polling daemons that launch
   the scanners on command; `mirror_to_drive.py` mirrors files to a Drive folder
   Claude can read.

**The Google Sheet is the integration bus.** Scripts coordinate entirely through
named tabs (e.g. `Hunter Leads`, `Hunter Green Commercial`, `HOT ZONES`,
`COMMAND`) — there is no shared in-process state. `optimus_config.py` defines the
canonical `TABS` schema (column order matters) that the newer tools agree on.

## Running and developing

There is no automated way to "build" or "test." To work on a tool:

```bash
# Dependencies are installed per-script, ad hoc. The common superset:
pip install requests gspread google-auth pillow numpy scipy pgeocode pyautogui

# Run any tool directly. They are argparse-driven where flags exist:
python validatorman.py --tab "Commercial" --force --limit 5   # always test with --limit first
python themapman.py --tab "Hunter OKC Dedup" --no-pick --no-update
python mapman_api_batch.py --addr "732 Esters Blvd, City ST 00000"   # single-address smoke test
python build_dedup_tab.py okc

# The cloud portals (the only web services) run locally as Flask apps:
python cloud/main.py            # Claude-chat portal (needs ANTHROPIC_API_KEY)
python portal/app.py            # team Drive-doc chat portal (needs GOOGLE_CREDS_JSON)
```

Validate a change the way the operators do: run the tool against a small slice
(`--limit`, `--once`, `--addr`, `--test`) and confirm rows land in the sheet —
never do a full run to "verify."

### Credentials and config (intentional conventions)

- **Service-account creds** are expected as `google_creds.json` discovered from a
  list of candidate paths (Android `/storage/emulated/0/Download/...`, repo
  root, `~/Downloads`, `~/optimus`), or via the `GOOGLE_CREDS_JSON` env var for
  cloud deploys. `google_creds.json` is **gitignored** — never commit it.
- **API keys and Sheet IDs are deliberately embedded in source** (e.g.
  `API_KEY`, `SHEET_ID` constants at the top of the mapman tools). This is how
  the operators run them off raw GitHub; do not "fix" this by externalizing them
  unless asked. Two Sheet IDs are in active rotation — `1FhO...` (current
  master, used by the `Hunter`-prefixed tools) and `12PII...` (the older "ATT
  FIBER LEADS" sheet, used by `cleaner.py`/`drive_commander.py`). Match whatever
  the file you are editing already uses.

### Auto-update mechanism

`fiber_hunter.py`, `fiber_scan.py`, `hunter_dot_extractor.py`, `mapman_api.py`,
and `slow_hunter.py` self-update on launch: they fetch their own newest source
from `raw.githubusercontent.com/.../main/<file>`, compare the `VERSION` string,
overwrite themselves, and `os.execv` to relaunch. **Consequence:** the `VERSION`
constant and the filename on `main` are load-bearing. Bump `VERSION` when you
change behavior, and keep the version in the file header docstring in sync.

## Conventions that matter

- **Versioning lives in two places per tool:** a `VERSION` constant and a big
  header docstring that doubles as a changelog ("CHANGES vs v5.6", "PATCH
  NOTES"). Update both together; the docstring is the primary changelog since
  git history is not reliable for this (see below).
- **Patch, never rewrite.** `WORKING_PATTERNS.md` documents that the single
  biggest failure mode here has been panic-rewriting working code and losing
  hard-won calibration. Before adding a feature, check whether a flag already
  exists (`--enrich-only`, `--force`, `--headless`, `--no-pick`). Before
  changing dot-detection thresholds or scanner motion constants, read the
  "CRITICAL LESSONS (DO NOT REDO)" sections — tightening color ranges and adding
  "NEEDS REVIEW" fallbacks have both broken production before.
- **Failed geocodes are skipped, not written.** Writing coordinates or
  placeholder rows poisons the sheet; this is an explicit, repeated rule.
- **Pure ASCII in the cloud portals.** `cloud/main.py` notes that emoji/smart
  characters caused UTF-8 mojibake that broke v1.x — keep portal strings ASCII.
- **Platform split:** `pyautogui`/`scipy`/Tesseract scripts are laptop-only;
  the `gspread`/Places-API data scripts (`themapman.py`, `mapman_pydroid_runner.py`,
  `mapman_api.py`) are written to run on Android/Pydroid and self-install their
  pip deps at startup.

## The BRAIN documentation system

The Markdown files at the root are an operator-facing knowledge base, not code
docs, but they carry the domain truth and operating rules:

- `BRAIN.md` / `brain.md` — short shared context: active Sheet/GHL/GCP IDs,
  phase targets, the **"REPO → LOG → BRAIN → THINK → ACT → RECORD"** operating
  rule (read context before changing code; record important changes back).
- `WORKING_PATTERNS.md` — the deep engineering memory: proven scanner motion,
  the calibrated dot-detection color targets and thresholds, the geocoding
  pipeline, sheet-write conventions and tab column layouts, the setup checklist,
  and an error decision tree. **Read this before touching any scanner or
  geocoding logic.**
- `SESSION_SUMMARY_*.md`, `OPTIMUS_SESSION_LOG.md`, `BRAIN/notes/*.md` — session
  history and infra notes (e.g. how files get to Claude despite the repo being
  private; the Make.com scenarios used to push to GitHub/Sheets).

When you make a meaningful change, the project convention is to record it in
BRAIN.md / WORKING_PATTERNS.md, not just in code.

## Git workflow notes

- The repo is pushed to via **Make.com automation** (GitHub write = scenario
  `5084486`), so `git log` is full of identical, repeated commit messages and is
  **not a useful changelog** — rely on the in-file docstrings instead.
- `cloud/`, `optimus_portal_cloud/`, and `portal/` are three separate Flask
  "portal" deployments (Cloud Run / Render) with their own `Dockerfile` /
  `render.yaml` / `requirements.txt`. The root `Dockerfile` builds
  `optimus_portal_cloud/main.py`. They are independent of the scanner tools.
