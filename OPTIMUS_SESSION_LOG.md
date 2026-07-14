# Optimus Session Log

## 2026-05-23 22:03 CT — Claude
**SESSION GOAL:** Fix GitHub-write via Make so it reliably creates AND updates files, document it in the BRAIN, and start timestamp + session-goal stamping.

- Fixed Make scenario 5084486 (GitHub write): SHA read is now non-fatal (handleErrors), and the PUT includes `sha` only when the file already exists — so it creates new files and updates existing ones.
- This file being created here is the proof the create-path works.
- Capability map: GitHub write = Make scenario **5084486**. BRAIN append = Make scenario **5073448**. Both run via update-trigger → activate → run → deactivate.

## 2026-07-01 — Claude (Fiber Scout: backend read)
**SESSION GOAL:** Move the Fiber Scout off pixel-sampling and onto the AT&T
dealer-map BACKEND JSON, so "fresh area" detection is accurate and hands us
addresses directly.

- **Finding:** the dealer map's "Search this area" call returns JSON
  `{success, error, content:[...]}` — up to ~3000 leads, each with ADDRESS +
  lat/lng + `subscriber_ban` + `curr_ntwrk_bld_type_cd`. Proven by the Scout's
  Backend Capture tab (Webster 77598 run). So dot color/status is in the
  payload — no need to count pixels (that's the GREEN_MIN/MAX / GREEN-0 bug).
- **Color key** (from dealer-map legend, Third Ward screenshot): GREEN = fiber
  eligible / non-customer (prize); GOLD = eligible / copper customer (upgrade);
  GREY = fiber customer (sold).
- **New module `backend_classifier.py`** (in optimus-map-tools): `classify_lead`,
  `summarize` (FRESH/MATURE verdict + green addresses), and `inspect`
  (build_type × ban cross-tab to discover the gold/grey codes). Tested:
  Webster→MATURE (all `unavailable`), synthetic green view→FRESH.
- **OPEN ITEM for next run:** run `inspect()` over a GREEN area (Arbor/Blodgett
  77004) to learn the `curr_ntwrk_bld_type_cd` codes for fiber-customer vs
  copper-customer, then fill FIBER_BUILD_CODES / COPPER_BUILD_CODES. Also grab
  the exact lead-JSON endpoint URL from the capture.
- **Scope note:** `fiber_scout.py` / `optimus_dot_detect.py` live in repo
  Go-High-Level-MCP-2026-Complete (not reachable this session); the classifier
  was built standalone here to drop into the Scout via one import + one call.

## 2026-07-01 — Claude (Scout reuses HUNTER dot detection)
**SESSION GOAL:** Fix the Scout's GREEN-0 bug by making it reuse the hunter's
proven pixel detection (green+gold high, very little grey) instead of its own
broken green window.

- Root cause of GREEN-0: the Scout's own `optimus_dot_detect.py` green window
  misses green dots; the HUNTER's window works (pulled thousands of 77027 greens).
- **New module `scout_dot_score.py`** (optimus-map-tools): ports fiber_hunter.py's
  EXACT color windows (GREEN 30,130,30–100,210,80; GOLD/ORANGE 220,160,0–255,200,60;
  GREY 140,140,160–190,190,210), the shape-filtered `count_dot_clusters`, and the
  `is_blank_map` guard. Adds `score_view()` → green/gold/grey + FRESH verdict
  (FRESH = green+gold ≥6 and grey% <20) and `summary_row()` for the Fiber Scout tab.
  Tested with numpy/scipy: green+gold view → FRESH, grey-heavy view → MATURE.
- **Wire-in (other chat / tools repo):** in fiber_scout.py, per scanned view:
  `import scout_dot_score as sds; r = sds.score_view(screenshot)` → write
  r["green"], r["gold"], r["grey"], r["grey_pct"], r["verdict"]; hunt where FRESH.
- Two paths now exist for the Scout: `scout_dot_score.py` (pixel, hunter-matched)
  and `backend_classifier.py` (server JSON, no pixels). Backend is better long-term;
  scout_dot_score is the immediate GREEN-0 fix that needs no endpoint.
