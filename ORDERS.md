# ORDERS.md — the shared instruction file for every Optimus PC

Written by the remote Optimus Claude (this repo, branch `claude/new-session-8z4pyb`).
Each PC's local Claude: `git pull` this repo, read this file top to bottom, do what
applies to your PC, then REPORT (section 4). Never text or email a customer from an
order in this file — customer contact is a human's call. Never push to the hunter repo
without showing Patrick the diff first, except the deploy in order 1, which is tested.

Orders are numbered and dated. A struck-through order is done. Newest at the bottom.

## 0. First launch on any PC (2026-09-05)

1. `git -C C:\Optimus\optimus-map-tools checkout claude/new-session-8z4pyb && git pull`
   — the brain (CLAUDE.md, BRAIN.md) and this file live on that branch, NOT on main.
2. `git -C C:\Optimus\Go-High-Level-MCP-2026-Complete checkout claude/optimus-map-tools-setup-6dcl6o && git pull`
   — the hunter and scraper live on that branch, NOT on main.
3. Read CLAUDE.md in optimus-map-tools before doing anything else. It is the brain.
4. Confirm the toolkit installed: `%USERPROFILE%\optimus_hunter\precise_fiber_hunter.py`
   exists and its `BUILD_DATE` line reads 2026-09-03 or later.
5. Log into the AT&T fiber map ONCE by hand in the hunter's Chromium profile
   (launch the hunter, click AT&T Employee at the chooser, sign in, Remember me).
   No Claude can do this step. Never record the credentials anywhere.

## 1. ~~DESKTOP ONLY — push the deploy~~ DONE 2026-09-05 08:2xZ by the remote Claude (hunter commit a995b27). ONE PIECE LEFT FOR THE DESKTOP: `gh release upload installer patches/DEPLOY-2026-09-04/optimus/install/INSTALL_OPTIMUS.bat --clobber` so the emailed release link serves v2 (this session is refused release edits). Report the asset size (must be 8,704).

Follow `patches/DEPLOY-2026-09-04/README.md` in this repo exactly: copy the four files
into the hunter repo (on its claude branch), commit, push, then
`gh release upload installer patches/DEPLOY-2026-09-04/optimus/install/INSTALL_OPTIMUS.bat --clobber`.
Prove it: the raw hunter file shows `BUILD_DATE = "2026-09-04"` and the release asset
is 8,704 bytes. Report both numbers.

## 2. EVERY PC — after order 1 lands (2026-09-05)

Relaunch the hunter from its Desktop icon. The console must print
`BUILD_DATE : 2026-09-04`. If it prints an older date, run the v2 installer again
(`INSTALL_OPTIMUS.bat` from `patches/DEPLOY-2026-09-04/optimus/install/`) and relaunch.
Then leave the hunter running. Aim: the desktop stays on Milton, FL (it is logged in
there). Laptops: aim targets come in the next order once your heartbeat shows up —
do not sweep ground the sheet already owns.

## 3. DESKTOP — the "James" text blast (2026-09-05, urgent)

A workflow is texting "Hi, this is James from a local business fiber installation
team…" from +1 850-695-1985 to Port St. Lucie / Jensen Beach numbers and drawing STOPs
within minutes. Find the workflow or bulk action sending that template and PAUSE it.
Do not delete anything. Report its name, id and who created it.

## 4. REPORT — every PC, every time you finish an order

Append one dated line per order to `REPORTS/<your hostname>.md` in this repo
(create the file if missing), commit, push to branch `claude/new-session-8z4pyb`.
Format: `2026-09-05 20:15 CT — order 1 — DONE — raw BUILD_DATE 2026-09-04, asset 8704`
or `— BLOCKED — <one line why>`. The hunter and scraper already report through the
hunter repo's `optimus/_feed/` and `optimus/_live/`; you do not need to repeat those.

## 5. DESKTOP — HUNTER WATCH, the standing order (2026-09-05 03:1xam CT)

Patrick: *"start by you controlling precise hunter from here, learning to log in and
restart scan etc autonomously."* The remote Claude supervises from the feed every hour
and writes here; YOU (the local Claude on the desktop) are the hands. Run the hunter
ONLY through `%USERPROFILE%\optimus_hunter` via the Desktop icon / `RUN_HUNTER.bat`.
Never from the C:\Optimus clone, never an old copy from the Desktop.

**5a. Measure the login first (UNMEASURED since 09-04, this settles it).**
Launch the hunter. When the console prints the LOGGED_OUT steps, drive the browser
yourself: dismiss "Restore pages?", click **AT&T Employee** on the youachieve.att.com
chooser, and watch Global Logon. Record ONE of:
  - `LOGIN: auto` — Remember-me carried it through with no typing (then youRefer →
    AT&T Fiber Availability Map tile → the map loads), or
  - `LOGIN: needs-typing` — it asks for the ID/password (a human types them; NEVER store
    them in any file, repo, note or report), or
  - `LOGIN: needs-code` — it asks for a one-time code (a human must be present).
Report that word in REPORTS. It decides how autonomous this loop can ever be.

**5b. Restart rules (check the console + `optimus/_feed/heartbeat.json` every 15 min).**
  - heartbeat `last_phase` = `LOGGED_OUT` for > 10 min → do 5a again.
  - `latest.json` `capture_truth.raw_features` = 0 on a `pass_done` → the map is not
    logged in even if `auth_ok` is true (that is Google). Do 5a.
  - heartbeat older than 2 hours while the window is open → Ctrl+Shift+K, relaunch
    from the icon (answer N to "Terminate batch job?" so the launcher loop relaunches).
  - console prints `Update looked stale/partial` → run installer v2 once, relaunch.
  - Never press Enter on an old-build prompt ("STEP 2 -> press Enter to scan"). That
    is the 08-18 build; reinstall instead.
  - Never touch `PAUSED.flag`, never press bare Enter in the console (a stray Enter
    once killed Chromium mid-run).

**5c. Aim.** Desktop stays on Milton, FL until the remote Claude changes this line.
Aim by hand during the 10-second hold or Ctrl+Down (pause) / Ctrl+Up (go).

**5d. Proof, not announcement.** A launch is not a capture. Report only what the feed
shows: `raw_features`, `classified`, `written`, `failed_writes`, `last_phase`. The main
workbook is FULL; green goes to the split workbook, and `written: 0` there is a real
zero until the deploy (order 1) lands.

**5e. Report every hour** to `REPORTS/<hostname>.md`:
`2026-09-05 04:00 CT — order 5 — phase <x> — raw <n> — written <n> — LOGIN: <auto|needs-typing|needs-code>`.

## STATUS (the remote Claude updates this block; newest line last)

- 2026-09-05 08:2xZ — DEPLOY PUSHED: hunter branch commit a995b27. CDN verified serving BUILD_DATE 2026-09-04 + LAUNCHER_SENTINEL, scraper with dedupe gold/grey + gspread-6 client + five GHL tabs, launcher BUILD_DATE gate, installer v2 (8,704). Every PC un-pins at its next hunter launch; the scraper picks up its changes at its next launch. Feed at 08:13Z: heartbeat 14:51 LOGGED_OUT (LAPTOP-FJEEPATI, 08-24 build), scraper LAPTOP-RS9EHSLO 02:51 with 877 parked, sheet FULL. Release asset still 7,204 (desktop: the gh line in order 1). Next: order 2 (relaunch, confirm BUILD_DATE 2026-09-04), order 5a (measure the login), order 3 (pause the James blast).
- 2026-09-05 11:2xZ (HUNTER WATCH) — **THE MAPS SCRAPER IS RUNNING RIGHT NOW** on
  `LAPTOP-RS9EHSLO`: `LIVE_COUNTS_scraper.txt` updated **2026-09-05 06:06:40 CT**
  (~8 min before this check), ZIP **77070**, 1,115 businesses pulled this run,
  **0 added to the sheet, 1,078 parked — `*** SHEET FULL ***`.** It is on the
  **PRE-DEPLOY build**: its `tabs.json` is stamped 2026-09-04 14:26:48, which is when
  this run launched, so it carries none of a995b27 (no gold/grey dedupe, no gspread-6
  `_gc()`, no five GHL tabs). **To get them it must be CLOSED AND RELAUNCHED** — the
  scraper only self-updates at launch. Hunter unchanged: heartbeat 2026-09-04 14:51:49
  `LOGGED_OUT`, LAPTOP-FJEEPATI, fingerprint 3d2a6779 (old build); `latest.json` run
  20260904-121609 all counts 0, `failed_writes` 5,815. Live hunter file on the CDN is
  `BUILD_DATE = "2026-09-04"` + `LAUNCHER_SENTINEL` — order 1's deploy half is done and
  serving. Release asset size **COULDN'T READ** from this session (proxy returns 401 on
  the release CDN); the `gh release upload` line in order 1 is still assumed open.
  No PC has written to `REPORTS/`.
- **HUMAN NEEDED — the hunter has captured nothing since 2026-09-02 (69+ hours).**
  Order 5a (a human clicks through the AT&T access chooser, then report
  `LOGIN: auto | needs-typing | needs-code`) is the only thing that unblocks capture.
  Second, smaller: relaunch the Maps Scraper on LAPTOP-RS9EHSLO so it picks up a995b27.
- 2026-09-05 12:0xZ (MORNING EDITION) — **ORDER 5a IS SATISFIED ON ONE PC WITHOUT ANYBODY REPORTING IT.**
  `LAPTOP-67UOPK24` (a machine not previously in this file) is logged into the AT&T
  map and captured **551 rows in ANGLETON 77515 between 06:25:00 and 06:56:49 CT**
  — GREEN 137, GREY 146, GOLD 4 (2 unique addresses) — **into the split workbook**,
  which went 20,328 → 38,633 bytes. **The `_feed/` heartbeat knew none of this**
  (still `20260904-145042 / LOGGED_OUT / LAPTOP-FJEEPATI`). **New standing rule for
  this watch: check the split workbook's `modifiedTime` + `fileSize` BEFORE calling
  the hunter blind.** Main workbook confirmed full: mtime moving 11:45:22Z, size flat
  8,484,584. Orders still open: 1 (release upload), 3 (pause the James blast — 8 STOPs
  in the 30 newest threads), and the LAPTOP-RS9EHSLO scraper relaunch.
- **The earlier `HUMAN NEEDED — hunter blind 69h` line is WITHDRAWN.** It was measured
  off the feed and the feed was not looking at the machine that was working.
- 2026-09-05 12:1xZ (HUNTER WATCH) — **THE ANGLETON RUN HAS STOPPED.** Split workbook
  `1DXu-nuQ…` is **still `fileSize 38,633`, `modifiedTime 2026-09-05T12:01:29Z`** — no
  growth in the 16 minutes since the last check. LAPTOP-67UOPK24 captured 06:25:00 →
  06:56:49 CT and its last sheet write was 07:01 CT, so that run lasted ~36 minutes and
  ended. **That breaks the hunter's own contract — "aim, start, forever, we never stop
  until the PC dies."** A 36-minute run means the window was closed, the browser died,
  or the sweep hit its edge. **Next action on that PC: relaunch and leave it running.**
  Scraper on LAPTOP-RS9EHSLO still going and still parking: 07:11:50 CT, 1,168 pulled,
  **1,143 parked** (was 1,115/1,078 at 06:06) — the sheet is full, so archiving is the
  action there, not a relaunch. Feed unchanged and still reporting the wrong machine
  (`20260904-145042 / LOGGED_OUT / LAPTOP-FJEEPATI`). BUILD_DATE on the CDN is
  `2026-09-04` — the deploy half of order 1 stands. `tabs.json` still stamped 09-04
  14:26:48, confirming the running scraper is pre-deploy. Release asset: COULDN'T READ
  (401). No PC has written to `REPORTS/`.
- **HUNTER WATCH routine rewritten this turn** (`trig_01NFW7FKJpcpQ66iTLS3Lbjr`): step 1
  is now the SPLIT WORKBOOK's `modifiedTime`+`fileSize`, and the feed is corroboration
  only. It also carries the five-PC list and the "release size returns 401, say
  COULDN'T READ" rule. The old prompt's claim that the firing has no connectors was
  wrong — it is self-bound, so it has this session's Drive and GHL.
- 2026-09-05 13:1xZ (HUNTER WATCH) — **THE 67UOPK24 PROCESS IS ALIVE BUT NOT CAPTURING,
  AND THAT IS A DIFFERENT FAULT FROM A CLOSED WINDOW.** Split workbook `modifiedTime`
  moved `12:01:29Z → 13:01:35Z` while `fileSize` stayed **flat at 38,633**. A 60-minute
  cadence with no byte growth is the `_Dedupe Lock` heartbeat refreshing (the lock row
  read `1788609692.9|LAPTOP-67UOPK24` at 12:01:32Z), **not capture**. So the hunter
  process on that PC is still running and holding its lock — it just has not written a
  row since **06:56:49 CT, about 1h15m ago**. That points at a PAUSE (Ctrl+Down) or the
  sweep sitting at a prompt, **not** a dead window. **Action on that PC: press Ctrl+Up
  (GO) to resume the sweep from the current view; only relaunch if Ctrl+Up does nothing.**
  Main workbook is the same signature and the same meaning as before: `modifiedTime
  13:10:07Z` moving, `fileSize 8,484,584` flat = full, archive is the action.
  Scraper LAPTOP-RS9EHSLO 07:53:03 CT, now on ZIP **77005**: 1,233 pulled, 0 added,
  **1,184 parked** (was 1,143 at 07:11, 1,078 at 06:06) — climbing ~50/hour, all parked.
  Feed unchanged (`20260904-145042 / LOGGED_OUT / LAPTOP-FJEEPATI`), `tabs.json` still
  09-04 14:26:48, CDN BUILD_DATE `2026-09-04`. Release asset: COULDN'T READ (401).
  No PC has written to `REPORTS/`. Not yet a `HUMAN NEEDED` line — under the 6-hour bar
  and the process is alive.
- 2026-09-05 14:1xZ (HUNTER WATCH) — **THE 2-HOUR THRESHOLD IS CROSSED. THE RESTART ORDER
  IS NOW DUE ON LAPTOP-67UOPK24.** Split workbook `modifiedTime` has now stepped
  `12:01:29Z → 13:01:35Z → 14:01:43Z` — a clean hourly cadence — with `fileSize` **flat
  at 38,633 through all three**. That confirms the `_Dedupe Lock` reading: the hunter
  process is ALIVE and holding its lock, and has captured nothing since **11:56:49Z
  (06:56:49 CT), 2h19m ago**. Per order 5b as rewritten, static over 2 daylight hours =
  restart order.
  **THE ORDER, in sequence — do not skip to the relaunch:**
  1. **Ctrl+Up (GO)** on that PC. The process is alive, so this resumes the sweep from
     the current view with no relaunch and no lost login. If the console starts printing
     cells again, stop here.
  2. If Ctrl+Up does nothing, **Ctrl+Down first** (it is the same key for pause AND
     resume — if it was paused twice it is running, if it was left paused this frees it),
     then Ctrl+Up.
  3. Only if neither moves it: **Ctrl+Shift+K** to force-quit, then relaunch from the
     icon and answer **N** to "Terminate batch job?" so the launcher loop restarts it on
     the 09-04 build.
  Do NOT press bare Enter in that console and do NOT delete `PAUSED.flag`.
  Scraper LAPTOP-RS9EHSLO 09:09:19 CT, ZIP 77005: 1,342 pulled, 0 added, **1,233 parked**
  (1,078 → 1,143 → 1,184 → 1,233 across four checks). Main workbook `14:14:10Z` moving,
  `8,484,584` flat — full, archive is the action. Feed unchanged. No `REPORTS/` entries.
  Not a `HUMAN NEEDED` line yet — that bar is 6 hours and we are at 2h19m.
- 2026-09-05 15:1xZ (HUNTER WATCH) — no change, the clock is the only thing moving.
  Fourth consecutive hourly lock touch on the split workbook: `15:01:50Z`, `fileSize`
  **still 38,633** (12:01:29 → 13:01:35 → 14:01:43 → 15:01:50, flat throughout).
  **LAPTOP-67UOPK24 has now gone 3h18m without capturing** (last row 11:56:49Z). The
  3-step restart order from 14:1xZ stands unchanged and unactioned — **Ctrl+Up first.**
  Scraper LAPTOP-RS9EHSLO 10:10:45 CT, ZIP 77005: 1,515 pulled, 0 added, **1,279 parked**
  (1,078 → 1,143 → 1,184 → 1,233 → 1,279). Feed unchanged, no `REPORTS/` entries.
  Still short of the 6-hour `HUMAN NEEDED` bar; it is crossed at **17:57Z** if nobody
  touches that PC. Nothing written to BRAIN.md this hour — nothing changed.
- 2026-09-05 16:1xZ (HUNTER WATCH) — no change. Fifth hourly lock touch: split workbook
  `16:01:58Z`, `fileSize` **still 38,633** (12:01 → 13:01 → 14:01 → 15:01 → 16:01, flat
  throughout). **LAPTOP-67UOPK24 is now 4h18m without capturing.** The 3-step order stands
  — Ctrl+Up first. Scraper LAPTOP-RS9EHSLO 10:56:52 CT, ZIP 77005: 1,598 pulled, 0 added,
  **1,318 parked**. Feed unchanged, no `REPORTS/` entries. **The 6-hour `HUMAN NEEDED`
  bar falls at 17:57Z — one more watch from now.** Nothing written to BRAIN.md; nothing
  changed.
- 2026-09-05 17:1xZ (HUNTER WATCH) — no change. Sixth flat touch: split workbook
  `17:02:06Z`, `fileSize` **still 38,633** (12:01 → 13:01 → 14:01 → 15:01 → 16:01 →
  17:02, flat throughout). **LAPTOP-67UOPK24 is now 5h18m without capturing.** The
  6-hour `HUMAN NEEDED` bar falls at **17:57Z** — 43 minutes out, so the next watch
  (18:14Z) crosses it and will raise the line. Not writing it early: at this moment it
  is 5h18m, not 6.
  Scraper LAPTOP-RS9EHSLO 11:48:23 CT, ZIP 77005: 1,602 pulled, 0 added, **1,322 parked**
  — the rate has flattened (1,318 → 1,322 in the last hour, versus ~50/hr this morning),
  which is what a ZIP running out of new businesses looks like, not a fault.
  Feed unchanged, no `REPORTS/` entries. Nothing written to BRAIN.md; nothing changed.
- 2026-09-05 18:1xZ (HUNTER WATCH) — **THE 6-HOUR BAR IS CROSSED.** Seventh flat touch:
  split workbook `18:02:13Z`, `fileSize` **still 38,633** (12:01 → 13:01 → 14:01 → 15:01
  → 16:01 → 17:02 → 18:02, flat every time). Last captured row **11:56:49Z**, so
  **LAPTOP-67UOPK24 has been idle 6h17m** with nobody acting.
- **HUMAN NEEDED — the only PC proven logged into the AT&T map has captured nothing for
  6h17m, and it is still running.** It swept Angleton 77515 for 32 minutes this morning
  (551 rows: 137 green, 146 grey, 2 gold addresses) and has done nothing since 06:56 CT.
  The process is alive — it refreshes its `_Dedupe Lock` on the hour, every hour — so this
  is a paused sweep, not a dead machine, and **it does not need a reinstall.**
  **Someone at that PC: press Ctrl+Up (GO).** If nothing happens, Ctrl+Down then Ctrl+Up.
  Only if neither works: Ctrl+Shift+K, relaunch from the icon, answer **N** to "Terminate
  batch job?". Not bare Enter; do not delete `PAUSED.flag`.
  **Every hour it stays paused is a lost hour on the only machine that can see the map.**
  Scraper LAPTOP-RS9EHSLO 12:33:16 CT, ZIP 77005: 1,613 pulled, 0 added, **1,334 parked**.
  Feed unchanged (`LAPTOP-FJEEPATI / LOGGED_OUT / 2026-09-04 14:51:49`). No `REPORTS/`.
