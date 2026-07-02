# Optimus Session Log

## 2026-05-23 22:03 CT — Claude
**SESSION GOAL:** Fix GitHub-write via Make so it reliably creates AND updates files, document it in the BRAIN, and start timestamp + session-goal stamping.

- Fixed Make scenario 5084486 (GitHub write): SHA read is now non-fatal (handleErrors), and the PUT includes `sha` only when the file already exists — so it creates new files and updates existing ones.
- This file being created here is the proof the create-path works.
- Capability map: GitHub write = Make scenario **5084486**. BRAIN append = Make scenario **5073448**. Both run via update-trigger → activate → run → deactivate.

## 2026-07-02 — Claude (Precise Hunter fixes, brain read first)
**SESSION GOAL:** Fix the Precise Hunter bugs recorded in the BRAIN's
2026-06-29 Discovery Log (precise_fiber_hunter.py audit).

- Followed REPO → LOG → BRAIN → THINK → ACT → RECORD. Sources: BRAIN Discovery
  Log (PR #3 branch `claude/att-fiber-leads-dedupe-lqr67f`), prior session log
  entry 2026-07-01 (backend_classifier pattern), Drive installer
  "INSTALL Optimus ALL" (confirms hunter still ships from repo
  Go-High-Level-MCP-2026-Complete — not reachable this session).
- **New module `hunter_fixes.py`** (in optimus-map-tools, tested by
  `test_hunter_fixes.py` — 29 checks, all passing), a one-import drop-in for
  precise_fiber_hunter.py fixing the four audited bugs:
  1. **flush() data loss** → `SafePending`: rows leave the buffer ONLY after
     the sheet write succeeds; a 429/network error keeps them queued (plus an
     optional JSONL write-ahead log).
  2. **Exact-string dedup drift** → `Deduper` keyed on the BRAIN's canonical
     core address ("24 Greenway Plz Ste 1800, Houston…" == "24 GREENWAY PLZ
     UNIT COIN"), seedable from the sheet at startup.
  3. **Junk AT&T feed addresses** → `is_junk_address()` / `clean_address()`
     block "UNIT DUMMY"-style placeholders and strip junk unit values
     (DUMMY/CTR/COIN/…) before write.
  4. **Apartment explosion** → `rollup_buildings()` collapses per-unit rows to
     one row per building with a unit count, for the callable list.
  Also `normalize_phone()` = the canonical 10-digit rule (fixes the scraper's
  leading-paren phone bug on ingest too).
- **OPEN ITEM:** wire the module into precise_fiber_hunter.py in
  Go-High-Level-MCP-2026-Complete (one import + swap the pending list/dedup
  set), and remove/gate its `self_update()` `git reset --hard` (RCE hazard,
  still open, can only be fixed in that repo).

## 2026-07-02 — Claude (BUILD #17 sheet-side verification + NEW sheet-read capability)
**SESSION GOAL:** Verify hunter BUILD #17 (map.panBy() motion, commit f186854
in the tools repo) from the sheet side; GitHub scope was optimus-map-tools
only, so no tools-repo pushes from this session.

### NEW CAPABILITY — read ANY range of the big sheet (beats the 500-row cap)
Drive text-read truncates each tab at ~500 rows (known gotcha). Built a
reusable Make pipeline that reads arbitrary ranges via the Sheets API:
- Make scenario **5552199** "Optimus — Claude Sheet Tail Read":
  google-sheets:makeAPICall (connection 8834319 "Optimus Google Sheets")
  → json:TransformToJSON → datastore:AddRecord.
- Read the result with MCP `data-store-records_list` on data store **113728**
  ("claude-scratch2", structure 416549, field `payload`).
- Use: update the scenario's URL (any `values:batchGet?ranges=...`),
  activate → run → deactivate (left deactivated), then list the record.

### Sheet-side verification (all times CT, host LAPTOP-TB1L669N)
- Tab sizes now: Precise Fiber **222,000** rows (+~42k since the 6/29 audit's
  180,190), Hunter Status 21,702, Fiber Green Biz 24,533, Maps Businesses
  18,178, Backend Capture 36 data rows, Fiber Scout ~few hundred.
- 07-01 22:47–22:49: Hunter Status "watching … timed: 8 cells, 336 leads" —
  the timed sweep panned 8 cells and pulled 336 leads off the wire.
- 07-02 00:20:38 and 00:40:09: two manual "single pass" starts; fresh GREEN
  batches written 00:22:45 and 00:40:15 with DIFFERENT streets each time
  (NW 41st/42nd St + N MacArthur Blvd, then Quail Dr/N Evans Dr/Schroeder Ln)
  → **map motion + wire capture WORK on the sheet side**. ⚠️ These captures
  are OKLAHOMA CITY — keep them out of the Houston dialer lane.
- BUILD tag is NOT visible in the sheet (Hunter Status rows carry no build
  stamp — add the build tag to the "started" status row when stamping).
  Console banner check (BUILD #17 + "[motion] recovered the map object")
  still needs Patrick's eyes.
- Fiber Scout survey 06-30: GREEN=0 in every cell, GOLD=**exactly 1 in every
  cell** (even 106-grey cells) → the constant gold=1 smells like the pixel
  counter hitting the map legend, and confirms the pixel path must go
  (backend read replaces it).
- Backend Capture (07-01 22:49:13 snapshot): 164 endpoints logged but
  **"LEADS PARSED: 0 total"** and NO serviceability-JSON endpoint in the
  list (only images/JS/mapbox tiles/fonts). The exact lead-JSON endpoint URL
  is still NOT captured — next capture must run while "Search this area"
  actually fires so the XHR lands in the snapshot.
