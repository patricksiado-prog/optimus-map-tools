# Optimus BRAIN

_Last updated: 2026-05-02 05:32:19 CDT_

## Active systems
- GitHub repo: patricksiado-prog/optimus-map-tools
- Active sheet: 12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag
- GHL Houston Location: TXw28sw0Z2rl6tcCDhJY (~41,325 contacts)
- Service account: fiberscanner@fiberscanner-493900.iam.gserviceaccount.com
- Map Man v10
- Drive mirror: 1u38EOzaGO7Sd5Y8ERqQoXeYZW5Pws8Z_

## Phase targets
- Phase 1: 500 sales/week
- Phase 2: 1000/week
- Phase 3: 2000/week

## Run log
(append new entries below this line)

### 2026-07-26 (b) — Code audit + external-API research (DISCOVERIES)
PIPELINE IS "PARTS, NOT A MACHINE": programs work individually but the hunt->enrich->score->load chain is not fully wired. Top conflicts (files under optimus/):
- hunter_fixes.py is DEAD CODE — imported by nothing. SafePending (data-loss), Deduper (address drift), junk-address blocker, apartment roll-up all un-wired. Hunter still dedups on raw string (precise_fiber_hunter.py:2237). The "critical fixes" are inert.
- enrich->load handoff BROKEN: enrich_phones writes enriched_leads.jsonl (JSONL) but ghl_loader does json.load() (needs a JSON array) -> crash. business_score wraps records under ["business"] but ghl_loader reads name/phone/address at top level -> contacts load with score but no name/phone. business_score imported by nothing.
- Hunter can't tell GOLD(copper) from GREY(fiber): it uses optimus_dot_detect.classify_status and NEVER loads build_codes.json; only fiber_scout uses backend_classifier + codes. backend_classifier ships empty code sets.
- enrich sets phone_type="business" but business_score only rewards "landline"/"wireless" -> every enriched phone scores 0 reachability.
- Vocab conflicts across tabs: copper = "ORANGE" (hunter/enrich) vs "GOLD" (scout/classifier); grey spelled "GRAY" vs "GREY".
- Phone stored 3 ways (bare 10-digit / E.164 / raw); ~/Optimus vs ~/optimus path casing breaks state on Linux; two Maps scrapers write different businesses.csv columns; hunter hardcodes zone_label="WORKING" so FRESH weighting never fires.
- BUG: enrich cache stores empty misses with no tier -> running FREE then --paid SKIPS every earlier free miss (undermines the ~4,800 enrichment plan).
EXTERNAL (research, sources in Drive delta):
- AT&T map = biggest fragility: undocumented internal API; main community tool broke on an endpoint change and was ARCHIVED June 2026. backend_classifier has NO schema tolerance (hardcoded subscriber_ban / curr_ntwrk_bld_type_cd). Isolate behind an adapter + add a canary.
- Google Places: legacy API FROZEN Mar 2025; phone (nationalPhoneNumber) is an Enterprise-tier field ~=$20/1k requests, ~1k free/mo. Must be on Places API (New) with X-Goog-FieldMask. De-dupe by place_id; fetch all needed fields in one call. ~4,800 enrich run ~= ~$76 after free tier IF cache bug fixed.
- mapbox_vector_tile maintained (v2.2.0) but coords are tile-local ints [0,4096) -> must transform to lat/lng, watch y-flip + v2 GeoJSON default.
- Playwright: stealth alone insufficient; TLS/JA3-JA4 mismatch is the layer stealth can't fix. Ongoing maintenance cost.
OUTPUT MAP: hunter -> precise_addresses.jsonl (+ "Precise Fiber" tab); enrich -> enriched_leads.jsonl (+ "Enriched Leads" tab); scout -> "Fiber Scout"/"Backend Capture" tabs + fresh_leads.csv; maps_scraper -> businesses.csv; ghl_loader -> GHL contacts/opps + power-dialer + dial_queue.json.
GOOD: no hardcoded secrets (all env-based); SHEET_ID 1FhO consistent everywhere; backend green-dot logic sound where used.
TOP FIXES: (1) wire hunter_fixes, (2) fix enrich->load format/shape, (3) load build_codes.json in hunter, (4) fix enrich cache tiering.

### 2026-07-26 — Optimus programs copied into repo + brain/sheet pointer corrections
- COPIED the three production programs into this repo under `optimus/` (branch
  `claude/chat-repetitive-questions-9ex5h7`), pulled verbatim from
  `Go-High-Level-MCP-2026-Complete` (branch `claude/optimus-map-tools-setup-6dcl6o`,
  folder `optimus/`) — the source the desktop installer actually runs:
  - `precise_fiber_hunter.py` (v0.4, 3439 lines) — Playwright click-every-dot exact-address grabber
  - `fiber_scout.py` (759 lines) — NEW-fiber finder (green+gold vs grey freshness)
  - `maps_scraper.py` + `standalone/maps_scraper_standalone.py` — Google Maps biz scraper
  - shared: `optimus_dot_detect.py`, `optimus_api_capture.py`, `hunter_fixes.py`,
    `backend_classifier.py`, `build_codes.json`; tests; `install/*.bat` launchers.
  - All 10 .py compile clean; build_codes.json valid.
- BACKEND GREEN-DOT READER confirmed present + wired: `optimus_api_capture.py`
  (ResponseSniffer/extract_features) + `backend_classifier.py` read the AT&T
  `content[]` JSON feed; GREEN = empty subscriber_ban (GREEN-0 "unavailable" bug
  stays fixed). Used by scout (`bc.summarize`) and hunter (`NetCapture`/`drain_viewport_backend`).
- POINTER CORRECTIONS (stale in old brain):
  - Production sheet = `1FhO...` (NOT `12PII...` — that ID no longer resolves; never write leads there).
  - MASTER BRAIN `1v2Jxgt...` no longer resolves from Drive; treat repo BRAIN.md +
    BRAIN_delta_* notes as the live brain until a new master is set.
- GHL: active dialer location this session = `xZj500PjsflIQg2j9f9D` (brain names
  `TXw28sw0Z2rl6tcCDhJY`/~41k contacts — verify which is the real book of business).
- DIALER: removed 1 invalid lead (Peppercinis) from `power dialer queue`; 17 valid
  Houston fiber leads queued. Houston green-biz sheet math: 245 unique addresses,
  20 no-phone, 18 already uploaded -> 207 net-new callable remaining.

<!-- REPO_LOG_BRAIN_THINK_ACT_RECORD_START -->
## OPERATING RULE - REPO LOG BRAIN THINK ACT RECORD

Date added: 2026-05-02

Rule:
Before answering or doing anything new on Optimus / AT&T / fiber / GHL / Sheets / GitHub / app-builder work:

REPO -> LOG -> BRAIN -> THINK -> ACT -> RECORD

Meaning:
1. Read repo/context first when available.
2. Check logs/history before changing code.
3. Read BRAIN before acting.
4. Think through the task before speaking or editing.
5. Act only after understanding the current source/context.
6. Record important changes, rules, scripts, repo updates, file links, and fixes back into BRAIN.

Source of truth:
- Repo: patricksiado-prog/optimus-map-tools
- Short brain: BRAIN.md
- Full context: BRAIN_FULL_CONTEXT.md
- Drive brain: Optimus Scripts Notes 2026-05-02
- Drive mirror file: BRAIN.md

Important:
- Do not guess from memory if repo/BRAIN/context is available.
- Do not create workaround files when the correct move is to fix the real repo/BAT/program.
- If GitHub connector is unavailable, use Drive BRAIN, Drive mirror files, and uploaded repo bundle until live GitHub access is fixed.
<!-- REPO_LOG_BRAIN_THINK_ACT_RECORD_END -->
