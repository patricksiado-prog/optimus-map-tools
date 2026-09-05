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

## 1. DESKTOP ONLY — push the deploy (2026-09-05, the one that fixes every PC)

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
