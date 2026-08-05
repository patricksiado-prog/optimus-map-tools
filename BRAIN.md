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

### 2026-07-27 — FULL LOAD COMPLETE: all unique callable fiber leads tagged into dialer
Ground through the entire non-Houston set (812) via API upsert (phone + tag optimus-fiber-biz +
assignedTo Zack), on top of the 1,922 Houston already tagged. optimus-fiber-biz live count:
1,922 -> **2,519**. That's the whole deduped 2,495-unique callable set now in the dialer list.
Mix: ~half were new:false (existing contacts, tag added), ~half new:true (genuinely new, mostly
OKC 405-area + Houston-metro suburbs that weren't in GHL). NOTE: the newly-CREATED contacts were
upserted phone-only, so their dialer card shows just the phone number (no business name/address)
— cosmetic; they're fully callable. To backfill names/addresses on those ~300 new ones, re-run
the sheet rows through update_contact by phone (firstName=business, lastName=address). The
already-existing contacts kept their name+address. Dialer mechanism unchanged from (e): native
Power Dialer on tag optimus-fiber-biz; recycle inherent; dispositions via DND; multi-rep via
"view all contacts". Resumable loader state: scratchpad/non_houston.json (all 812 fired).

### 2026-07-26 (f) — KEY FINDING: all 2,495 leads ALREADY EXIST in GHL (tag-sync, not load)
Upserted 72 "non-Houston" uniques via API. EVERY ONE returned new:false (dateAdded 6/30 &
7/24 via INTEGRATION/OAUTH source 6a25617c1d5fcb2f6e8b826b). So the full 2,495-unique callable
set was already imported to GHL weeks ago; ~573 of them just lacked the `optimus-fiber-biz`
tag. optimus-fiber-biz tagged count moved 1,922 -> 1,945 after the 72 upserts (only ~23 were
genuinely untagged; rest already tagged). => API upsert is a BAD tool to finish: ~23 net tags
per 60 calls means ~1,400 more calls for the last ~550, all redundant re-writes of existing
contacts. The GHL bulk CSV import (Contacts>Import, scratchpad/optimus_fiber_dialer_import.csv)
matches by phone and adds the tag to all 2,495 in ONE op — the correct finish. Note: many
non-Houston-by-address rows are actually Houston-metro suburbs (Heights/Katy/Satsuma); only
405-area OKC (~273) is a genuinely separate market. Some contacts carry Twilio SMS DND
(error 30006) but voice-callable.

### 2026-07-26 (e) — DIALER: what API can/can't do + the working design (FINAL)
Tested every path live. HARD API LIMITS in command_connector for GHL dialer:
- ghl_update_workflow_actions accepts triggers in the payload but SILENTLY DROPS them
  (re-GET shows triggers:[]). Confirmed: workflow triggers are UI-only.
- manual-call actions create "Manual Actions", a SEPARATE object from Tasks. get_contact_tasks
  and search_location_tasks both return [] for an enrolled contact -> Manual Actions are
  invisible/unverifiable via API. This is why the Manual-Actions dialer path burned 3 days.
- create_smart_list -> 404 (Cannot POST /contacts/smart-lists). Smart lists are UI-only.
- No custom-call-disposition API. Dispositions are UI/DND-driven.
WHAT WORKS (native, verifiable): dialer list = Contacts filtered by tag `optimus-fiber-biz`.
- Recycle = inherent: tag stays, list repopulates every Power Dialer session.
- Dispositions = DND: "no" -> rep sets DND (Power Dialer won't dial DND) -> drops from list.
  "sold/yes" -> move opportunity to Won -> filter excludes. else -> stays -> recycles.
- Multi-rep = Settings>Team> each rep enable "view all contacts" (leads are assigned to Zack).
COUNTS (live from Fiber Green Biz tab via Sheets API): 18,241 rows but only **2,495 unique
callable phones** (dedup collapses the 18k -> reconciles the "18k vs 2k" argument; both true).
Houston unique 1,683; non-Houston 812 (incl. OKC 405-area). Already tagged optimus-fiber-biz:
1,922. Upserted 12 non-Houston (OKC) as a test -> ALL came back new:false = they ALREADY EXIST
in GHL (loaded 7/24) but LACKED the tag. So "load the rest" = really "add the tag to existing".
DELIVERABLE: generated scratchpad/optimus_fiber_dialer_import.csv (2,495 rows, cols First Name=
business, Last Name=address, Phone E.164, Address, Category, Tags=optimus-fiber-biz). GHL bulk
CSV import (Contacts>Import) adds the tag to all existing + creates any missing = whole list in
one drop (API has no bulk contact create; import is the only bulk path). 12 already done via API.

### 2026-07-26 (d) — DIALER SOLVED: data was never the blocker
LOCATION: xZj500PjsflIQg2j9f9D. Confirmed live via search_contacts(query="optimus-fiber-biz"):
- **total = 1,922 contacts**, tag `optimus-fiber-biz`, source "Optimus Fiber Biz", ALL assigned
  to Zack (qOa2OVzPabolfU9xjVXM). Each contact is FULLY built:
  firstName = business name, lastName = full street address, phone = E.164, most have an open
  opportunity in pipeline 2V9thfxQpuhn6ZP0Peqt. So name+address show on every dialer card
  (not just notes). THE LEADS ARE DONE — loading was never the missing piece.
- Two dialer workflows exist:
  - `41e00387` "Optimus Fiber Biz — Power Dialer Queue": 1 action = manual-call "Fiber Biz Call",
    no trigger, no loop. Clean/pristine.
  - `9d3c7d0c` "Optimus Dialer 2 — Zack Call Queue": manual-call "Fiber Call" -> wait 2 days ->
    LOOP back to the call. The recycle loop wiring IS intact in stored structure. BUT both
    manual-call actions have `attributes:{}` (NO assigned user) — the likely reason Manual
    Actions showed empty: a manual-call task with no assignee surfaces to nobody.
- WORKING ANSWER (no fragile automation): native Power Dialer on the tag filter. Contacts ->
  filter Tag = optimus-fiber-biz -> select all -> Power Dialer. Works for ANY rep with a dialer
  seat, shows name+address per card, and "recycles" because the filter re-includes every lead
  each session. No workflow / Manual Actions dependency.
- MULTI-REP: leads are assigned to Zack; for Dave/Shika/Dominic/TFA to dial the same list they
  need "view all contacts" permission (Settings > Team) OR run it from a shared smart list.
- AUTO 2-DAY RECYCLE (optional upgrade): Dialer 2 already has the call->wait2d->recall loop.
  To light it up, open Dialer 2 in UI, click the "Fiber Call" Manual Call step, set Assign To =
  rep, Save. That one field is what makes the tasks appear (can't set reliably via API).
- DISPOSITIONS: set Custom Call Dispositions so "Not Interested"/"Do Not Call" removes tag
  optimus-fiber-biz (drops the lead off the list); "Sold/Yes" moves pipeline stage. Everything
  else keeps the tag and naturally recycles on the next Power Dialer pass.
- API LIMITS re-confirmed: get_smart_lists 400s; workflow /executions endpoint 404s;
  get_users needs companyId. Manual Actions screen not readable via API (user must eyeball).

### 2026-07-26 (c) — REAL live sheet counts (corrected) + how to get them
CORRECTION: an earlier "224 Houston callable" was WRONG — it came from a stale mini-extract
("ATT FIBER LEADS - Fiber Green Biz", id 1hI_t3..., ~245 Houston rows). The LIVE production
sheet 1FhO is far bigger. Patrick was right about ~18,000 matches.

HOW TO GET LIVE COUNTS (the MCP Drive read truncates + download caps at 10 MB, so use the
Sheets API directly): download google_creds.json from Drive (service account
fiberscanner@fiberscanner-493900, Drive id 1upYH4h2VsmOwO82v9CVjMpE6IzV-5dIs), then
`gspread.authorize(Credentials.from_service_account_file(... scopes=[spreadsheets.readonly]))`,
`gc.open_by_key('1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA')`. Count filled rows per tab
via `len(ws.col_values(1))`. NOTE: cryptography lib in the sandbox needed a reinstall; creds
are a SECRET — use in scratchpad only, never commit.

LIVE TAB COUNTS (2026-07-26):
- Precise Fiber ......... 308,522 rows (hunter fiber addresses)
- Maps Businesses ....... 23,759   (raw scrape; cols: Name,Address,Phone,Website,Category,Fiber Check; NO header row)
- Fiber Green Biz ....... 18,218   (MATCHED green-biz = the ~18k; cols: Business Name,Phone,Address,Website,Category)
- Enriched Leads ........ 1,311
- Hunter Status ......... 24,004   (run log)
- Fiber Scout .......... 1,750 ; Upgrade Orange Biz ~empty(1)

HOUSTON callable (from Fiber Green Biz):
- Houston rows: 1,932  ->  unique callable phones (deduped): ~1,675  (all-cities unique: ~2,472)
- In dialer now: 17  ->  ~1,658 Houston callable NOT yet loaded.

DATA LINEAGE (where dialer data came from):
- precise_fiber_hunter.py -> tab "Precise Fiber" (SHEET_ID 1FhO, OUT_TAB).
- maps_scraper_standalone.py -> tab "Maps Businesses"; then MATCHES scraped biz vs "Precise Fiber"
  green dots -> writes hits to "Fiber Green Biz" (green) / "Upgrade Orange Biz" (copper).
- The Houston rows of "Fiber Green Biz" were imported to GHL as source "Fiber Green Biz - Houston"
  = the dialer contacts.

NEXT: load the ~1,675 Houston callable into Dialer 2 (dedup by phone, assign Zack, tag
"power dialer queue"). Only 17 loaded so far.

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

---
## RUN-LOG 2026-07-27 — Dialer ROOT CAUSE found + custom skill written

**THE bug (3-day mystery solved):** every `manual-call` action in the dialer
workflows was built via `ghl_update_workflow_actions` with `attributes: {}` —
i.e. **empty assignee**. An empty `assignTo` makes GHL create the Manual-Call
task UNASSIGNED, so it never shows when Conversations → Manual Actions is
filtered to a rep (Zack). That is why the screen kept reading "Good Work! no
pending tasks" despite contacts being tagged + assigned + enrolled.

**Fix applied:** rewrote "Optimus Dialer 2 — Zack Call Queue"
(`9d3c7d0c-8f6f-44a9-93f9-d55d78e3b4a8`) manual-call action to
`attributes: {"assignTo": "qOa2OVzPabolfU9xjVXM"}` (Zack), loop preserved
(manual-call → wait 2d → back to manual-call). Now version 5, re-GET confirmed
assignTo + next/parentKey survived. Re-enrolled the 5 test contacts
(remove+re-add) so they hit the corrected step. Awaiting a DESKTOP
Conversations → Manual Actions check (mobile app screen is unreliable; API
cannot read Manual Actions to self-verify).

**Recycle confirmed by HighLevel docs:** manual-call advances only when the rep
deletes/completes the task → then Wait 2d → loops back. No native disposition
branching (open feature request); dispositions handled by rep (DND+remove / move
to pipeline / leave to recycle).

**Enrollment reality:** tagging ≠ enrolling. `add_contact_to_workflow` is single
-only (no bulk API); fastest full load is desktop UI bulk "Add To Workflow".
`official_contacts_get_contacts?query=optimus-fiber-biz` paginates via
startAfter/startAfterId (100/pg) — used to pull all 2,525 IDs.

**Skill research:** no public skill covers the power dialer. Closest useful ones:
sales-skills/sales `sales-gohighlevel` (API ref), mvanhorn/printing-press-library
`pp-gohighlevel` (bulk tag/dedup CLI). Connector = BusyBee3333
Go-High-Level-MCP-2026-Complete (user fork: patricksiado-prog/go-high-level-mcp-2026-complete).
Wrote custom skill: `.claude/skills/ghl-power-dialer/SKILL.md`.

---
## RUN-LOG 2026-07-27 (cont) — Dialer deep source dive, definitive API limits

Read the connector source (patricksiado-prog/go-high-level-mcp-2026-complete):
- Workflows are built via HIDDEN internal API `backend.leadconnectorhq.com/workflow`
  (Firebase-token auth). NOT the official API. `ghl_update_workflow_actions` sends
  `workflowData.templates = [my action objects]` verbatim and REPLACES all actions.
- `add_contact_to_workflow` = official `POST /contacts/{id}/workflow/{id}` — enrollment
  is REAL and works.
- Official GHL API spec (bundled, 168KB): ZERO endpoints for manual/dialer/manual-action.
  No `/workflows` endpoints. Manual Actions has NO public API (can't create OR read).
- Action TYPE naming: valid recognized types are hyphen/word (`manual-call` ACCEPTED),
  and snake_case for multiword (`create_opportunity`,`add_contact_tag`,`if_else`,`add_notes`,
  `ivr_say`,`conversation_ai`). Tested `manual_call` (underscore) → 400 "corrupted type".
  So `manual-call` (hyphen) IS the correct, engine-recognized type. Node is NOT a dead node.
- Real UI-built action nodes carry hybrid fields: `isHybridAction:true`,`hybridActionType`,
  `cat:"action"`,`transitions:[]`, and wait uses `startAfter:{when,type,value,action_in}`.
  Account has NO UI-built manual-call node anywhere to copy (checked Wavv, Fiber Info Voice
  Call = ivr_say/ivr_gather/ivr_connect_call/conversation_ai, Commercial Lead = call/conversation_ai).
- Optimus Dialer 2 (9d3c7d0c-...) is at v5: manual-call + assignTo=Zack (qOa2OVzPabolfU9xjVXM)
  + wait 2d loop, published. ~113 optimus-fiber-biz contacts enrolled this session.
- CANNOT verify Manual Actions screen via API (no read endpoint). Final inch = open workflow
  in desktop UI, Save+Publish the manual-call step (re-serializes it the way the engine needs),
  then bulk Add-To-Workflow the tag list. This is the only remaining step and requires UI.
- Works-today alternative needing no workflow: Contacts → tag filter → tap-to-call.

---
## RUN-LOG 2026-08-03 — OKC/national fix pushed to the LAUNCHER SOURCE branch
- **Where the desktop apps actually pull from** = `Go-High-Level-MCP-2026-Complete`
  branch `claude/optimus-map-tools-setup-6dcl6o`, folder `optimus/` (RUN_HUNTER.bat /
  RUN_SCRAPER.bat curl raw files from there each launch). The copy in
  optimus-map-tools is a MIRROR — fixes must land on the MCP-repo setup branch or the
  launchers never see them.
- **Bug:** VA (Ara) entered OKC zips but scraped 480/540/510 numbers. Root cause:
  `precise_fiber_hunter.py search_zip()` typed the ZIP + pressed Enter, but the
  Mapbox/MapLibre geocoder leaves a bare 5-digit ZIP unresolved → map never moved →
  scan ran on the DEFAULT view.
- **Fix (commit 9c0f818 on setup-6dcl6o):** search_zip now clicks the first geocoder
  SUGGESTION to force the map to fly to the ZIP; on failure it STOPS with a loud
  banner instead of silently scanning the wrong area. Verified live at the raw URL
  RUN_HUNTER pulls (154,103 bytes, fix present, old "scanning the current view" gone,
  compiles clean).
- **National status:** both tools already work anywhere — scraper via `nearby_zips()`
  (SCF-geographic ZIP expansion, any US ZIP), hunter via the fixed search_zip. Enter
  any city's ZIP → it works that metro + auto-advances outward. (Optional future: a
  built-in top-100-metro list for hands-off national sweep.)
- **Desktop icons:** newer = "Optimus Fiber Hunter" (orange, RUN_HUNTER, auto-updates
  = precise hunter). Older = "Optimus Hunter V200K (June build)" static; slow_hunter =
  old screen-grab. Use the orange one.

---

## Run log — 2026-08-04 — "sheet writes 0" investigation + capture-robustness fix

**User report:** hunter "used to get to 200k" but recent runs write 0 to the sheet.
Insisted a functional version exists / something in the code changed.

**Investigation (proved with git, not guesses):**
- The address-CAPTURE engine is **byte-for-byte identical since the FIRST commit
  (d30d5b7, 2026-07-26)** — verified `scan_net`, `sweep_continuous`, `sweep_grid`,
  `scan`, `search_this_area`, `pan`, and the NetCapture path all unchanged. My only
  earlier edits were `search_zip` + the launch prompt. **No code change explains
  200k→0.**
- The real signal is in the **Hunter Status** tab (per machine):
  - `LAPTOP-RS9EHSLO` → 26,160 cells / **3,806 leads** (this box built the 200k)
  - `DESKTOP-VCRE1E8`, `smallpc` → short runs, **0 leads**
  So the big numbers came from ONE machine; the 0-runs are on different machines and
  very short (15 cells). Points at login/session or map-not-showing-dots, OR AT&T
  changing their serviceability payload (would hit every machine).

**How capture actually works:** the continuous sweep does NOT click dots. It reads
AT&T's `serviceability` JSON responses off the wire (`NetCapture.handle`), parses each
with `lead_from_dict`, and `flush()`es GREEN/GOLD to the sheet (GREY = existing
customer, skipped). `lead_from_dict` REQUIRED an inline street address — if AT&T's
feed drops/renames the address field, every dot returns None → 0 written everywhere.

**Fixes shipped (precise_fiber_hunter.py, both branches):**
1. **Coordinate capture** — `lead_from_dict` now also captures a dot that has a fiber
   STATUS + US lat/lng but NO street address, recording `(lat, lng)` as the address.
   Tightly gated (US coord range + status/ban that classifies GREEN/GOLD) so junk
   coordinate/UI JSON can't get in. Unit-tested: green-coord captures; grey/no-status/
   non-US-coord all rejected. This is the prime fix for "map shows dots, sheet 0."
2. **Zero-capture diagnostics** — `NetCapture` counts serviceability responses
   (`svc_seen`) and leads (`svc_leads`); `.diag()` returns the reason. When a sweep is
   still at 0 leads it writes that reason to the **Hunter Status** sheet, e.g.
   "NO serviceability responses seen -> not logged in / map not loading" vs
   "saw N responses but decoded 0 leads -> AT&T payload changed; top keys: ...".
   A 200 svc reply that yields 0 leads dumps its top-level keys to the Drive log once.
   => next run tells us the ACTUAL root cause remotely (readable from the sheet).

**Gold-cluster alert (user request):** when >= `GOLD_CLUSTER_ALERT` (default 8) GOLD
(copper→fiber UPGRADE) dots land in ONE viewport, it prints a loud banner, logs
`GOLD-CLUSTER ...` to Drive, and writes a "GOLD CLUSTER" row to the Hunter Status
sheet. Gold = hottest leads (existing copper customers eligible to upgrade). Tune the
threshold via `GOLD_CLUSTER_ALERT` near the top of the file.

**Next-run playbook:** relaunch on the 0-lead machine, log in, get green dots visible,
press Enter, let it run. Then read the Hunter Status tab — `.diag()` will state whether
it's a login/map issue (no svc responses) or an AT&T-format issue (responses but 0
leads, keys shown), and we fix the confirmed cause precisely.

---

## Run log — 2026-08-04 — HOW THE COMBO MATCH WORKS (confirmed by reading both programs)

**User's model (CONFIRMED correct):** precise hunter builds the green-dot list; map
scraper writes business address+info; BOTH programs contain logic to match the two and
write the combined result to the **Fiber Green Biz** tab (copper→fiber to **Upgrade
Orange Biz**).

### Two sources
- **Precise Hunter** -> `Precise Fiber` tab: `Address | Dot Color(GREEN/GOLD) | Captured At`.
- **Maps Scraper** -> `Maps Businesses` tab: `Name | Address | Phone | Website | Category`.

### The join key (IDENTICAL `_norm_addr` in BOTH files)
`address -> "HOUSE|STREET CORE"`: uppercase, take text before the first comma (drops
city/state/zip), strip unit tokens (APT/STE/UNIT/#/BLDG/FL/RM/LOT...), standardize the
street suffix (STREET->ST, AVENUE->AVE, ROAD->RD...), normalize directionals
(NORTH->N). So `1524 SE 44th Street, OKC, OK 73129` and `1524 SE 44TH ST` both ->
`1524|SE 44TH ST`. That normalized key is how a dot and a business are declared "the
same address."

### Matching lives in BOTH programs (bidirectional — whichever finds the pair 2nd writes it)
- **Hunter side** — `init_bizmatch()` loads Maps Businesses into an index keyed by
  `_norm_addr`; on every `flush()` of newly captured dots, `match_leads_to_biz()` looks
  up each dot's address in that index and writes hits to Fiber Green Biz / Upgrade
  Orange Biz. Also: `reload_biz_index()` re-reads Maps Businesses every ~20 flushes so
  businesses the scraper adds mid-hunt get caught, and `_backlog_match()` matches prior
  captures from `precise_addresses.jsonl` at startup.
- **Scraper side** — `init_match()` loads Precise Fiber GREEN/ORANGE dots into a
  `leads{normkey:color}` dict; as each business is scraped, `_match_new()` looks up its
  address and writes hits to the SAME two tabs. Prints `COMBO MATCH ON ...` +
  `MATCH +N green ... [total matches: X]` (the counter seen on screen).

### Dedup lives in BOTH — but it is ASYMMETRIC (this is the important caveat)
- **Scraper** dedups matches by **address AND phone** (`green_seen`/`orange_seen` +
  `green_ph`/`orange_ph`, last-10-digit) — the stronger guard. Its Maps Businesses
  write also dedups by `NAME|ADDRESS`.
- **Hunter** dedups matches by **raw uppercase ADDRESS only** (`green_seen`) — NO phone
  dedup. (BRAIN already flagged hunter dedups on raw string -> address drift.)
- Both seed their seen-sets by reading the existing Fiber Green Biz/Orange tab (+ local
  CSV) at startup, so they don't re-append rows already present.

### CONSEQUENCE — why the row count is ~8x the real lead count (measured 2026-08-04)
`Fiber Green Biz`: **21,660 rows / 21,656 unique addresses / only 2,719 unique phones /
2,843 unique business names.** Dedup by ADDRESS passes (raw strings differ), but the
SAME business gets matched to many address VARIANTS (unit/suite numbers and near-dupe
spellings that all share one `_norm_addr`), so one phone repeats ~8x. **True callable
list ≈ 2,719 businesses, not 21,660.** (Consistent with the earlier "18k rows vs ~2,495
unique phones" note.) Two smaller gaps feed this: (1) hunter has no phone-dedup;
(2) the two programs hold SEPARATE in-memory seen-sets, so running hunter + scraper at
the SAME time can double-write a match until the other side reloads.

### FIX DIRECTION (not yet done — needs sign-off)
Dedup the match tabs by **last-10-digit phone** (dialer key), not raw address, on BOTH
sides; collapse unit-level address variants to one business; optionally add phone-dedup
to the hunter's `match_leads_to_biz`. Report/export the **unique-phone** count as the
real number. Until then: treat "matches" = **unique phones (~2.7k)**, not row count.

---

## Run log — 2026-08-04 — NEW-FIBER alerts + email notify (partly DEFERRED)

**Built + shipped (both branches):**
- Hunter flags a **freshly-lit block** = a viewport that's mostly GREEN (fiber
  eligible / NON-customer) with almost no grey (existing customers). Threshold
  `NEW_FIBER_ALERT`=15 green AND green >= 4x grey. On a hit it: prints a banner,
  writes a row to a **"New Fiber Alerts"** sheet tab, pushes to a public GitHub
  file `optimus/_live/NEW_FIBER_ALERTS.txt`, and (if configured) sends a
  real-time email. Legend confirmed from the AT&T map: green=eligible/non-customer,
  gold=eligible/copper-upgrade, grey=existing fiber customer.
- Real-time email path: `_email_alert()` sends via SMTP the moment a block is
  found (10-min cooldown), reading login from a LOCAL `optimus_email.json`
  (gitignored, never committed) in the same spots as github_token.txt. Recipient
  defaults to **DEFAULT_ALERT_TO = patricksiado@gmail.com** (override via "to").
- Daily digest Routine (trig_01MfufwTL7NxwKPW3tYiHNYy): once a day 13:00 UTC
  (8am Central), fresh session reads the public NEW_FIBER_ALERTS.txt and emails
  a digest — but the CCR notification email can only go to the ACCOUNT OWNER
  (Brandon / BHOLLAND@thefiberplug.com), NOT an arbitrary address. Went hourly
  briefly -> "too many junk emails" -> reverted to daily + "nothing new = don't send".

**DEFERRED / TODO (user said "do this later"):**
- Get new-fiber alerts to **patricksiado@gmail.com**. Blocker: the free CCR daily
  email only reaches the account owner; Gmail MCP connector was NOT available to
  the cron session. Two ways to finish:
  1. **Real-time to Patrick (recommended):** drop `optimus_email.json` on the
     hunter PC's Desktop = {"user":"patricksiado@gmail.com","password":"<gmail app
     password>"} (16-char App Password from Google Account > Security > 2FA > App
     passwords). Code already targets patricksiado@gmail.com, so nothing else
     needed. Sends instantly on each block (10-min cooldown).
  2. Or keep the daily email going to Brandon and forward to Patrick.
- Open question for the user: **turn OFF the daily owner-email** (trig_01Mfuf...)
  now that Patrick is the intended recipient, or keep it as a backup? (Not decided.)
- If a reliable cron-usable Gmail connector becomes available, could rebuild the
  Routine to actively send to patricksiado@gmail.com instead of the SMTP file.

---

## Run log — 2026-08-04 — PERIODIC + STARTUP DEDUPE (shipped & verified live)

Built into BOTH `precise_fiber_hunter.py` and `maps_scraper_standalone.py` (identical
embedded block; gitignored nothing new). On program START it deletes duplicates on all
shared tabs and prints totals; then a background thread re-runs every 30 min.
- **Precise Fiber** → exact-duplicate address rows. **Maps Businesses** → same phone
  (else name|address). **Fiber Green Biz / Upgrade Orange Biz** → same phone (else
  name|address); keeps the row that has a call disposition. Collapses the ~8x
  unit/spelling inflation. Verified read-only first: FG 21,662 → 4,105 rows, **0 unique
  phones lost**; Precise Fiber −5,278; Maps −1,505.
- Safety: deletes only specific duplicate row numbers from a snapshot, applied
  BOTTOM-UP via one `batch_update` (live appends never disturbed); local CSV backup per
  tab before delete; cross-machine advisory lock (`_Dedupe Lock` cell) so hunter+scraper
  never dedupe at once; per-pass cap `_DEDUPE_MAXDEL`=6000; Precise Fiber cleaned every
  6th pass. Startup shows: fiber-green addresses / scraped businesses / MATCHES-unique-
  phone / FG rows. Off via `--no-dedupe` (hunter) or `SCRAPER_NO_DEDUPE=1` (scraper).
- **LIVE PROOF (this session):** user ran the scraper; console showed
  "Cleaning duplicates on startup ... [dedupe] Precise Fiber: removed 5278 duplicate
  rows" — the EXACT predicted number. Feature works end to end.
- Pushed to both branches (optimus-map-tools chat-repetitive-questions-9ex5h7 + MCP
  Go-High-Level-...-setup-6dcl6o). Unit-tested selection + bottom-up delete with a mock.

## Run log — 2026-08-04 — DIALER: what's live + THE bug blocking new-lead adds

**Live dialer = "Optimus Dialer 2 — Zack Call Queue"** (`9d3c7d0c-8f6f-44a9-93f9-
d55d78e3b4a8`, published v21). Proof: user's mobile Manual Action screen shows every
lead labeled that workflow, "Assigned To: Zack Woodring." Its `manual-call` ("Fiber
Call") IS correctly assigned to Zack via `attributes.assignedUser` /
`standardAssignedUser` = `qOa2OVzPabolfU9xjVXM` (built in desktop UI — that's why it
works; API-built manual-call comes out with empty attributes).
- **Flow:** manual-call (assigned Zack) → wait 0.5 min → goto back to an if_else that
  checks tag "not interested" (yes→remove, none→call again). Recycle loop.
- **THE BUG (why new adds never stick):** the workflow's ENTRY action (order 0) is
  `add_contact_tag` **"not interested"**, and the very next if_else removes anyone with
  that tag. So every NEW enrollee is tagged not-interested and booted before reaching
  the call. Leads already in the loop re-enter at the if_else (never hit the Add Tag),
  so they keep calling — that's why "it's been working" yet nothing new gets in. Every
  lead in the queue is dated 07/29 = nothing new added since.
- **FIX:** delete the entry "Add Tag: not interested" step in the DESKTOP workflow UI.
  Do NOT do it via API — `ghl_update_workflow_actions` replaces all actions and would
  likely strip the manual-call's assignee (known quirk), un-assigning Zack's live queue.
- Other "dialers" are dead: Dialer 3 (`b21e43bd`) and "Optimus Fiber Biz — Power Dialer
  Queue" (`41e00387`) both have `manual-call` with empty attributes (unassigned →
  invisible); `e88c6596` is literally named "[RETIRED — loop moved into Dialer 2]".
- Tag `optimus-fiber-biz` = **2,281** contacts, assigned to Zack (some have broken
  phones like +12913411 — clean later).
- Call reporting/recordings endpoints 404 via API (`get_call_reports`,
  `ghl_list_call_recordings`) — can't read call activity; use desktop Reporting.

**PENDING — load the DealMachine list into the dialer:** user uploaded
`dealmachinecontacts...csv` = skip-traced homeowners on **Dorrcrest Ln / Houston 77070**
(the new-fiber block): 237 rows, **200 valid unique cell numbers** (37 no phone). Cleaned
to `Dorrcrest_Fiber_77070_ready.csv` (scratchpad; sent to user), tag
`dorrcrest-fiber-77070`. Plan agreed: (1) USER deletes the Add Tag entry step; (2) then
CLAUDE creates the 200 contacts (name/cell/address, assigned Zack) + enrolls each into
Dialer 2 via `add_contact_to_workflow` (no bulk API), OR user imports the CSV + Bulk
Actions → Add to Workflow. Blocked on step 1 (the Add Tag deletion). These are
RESIDENTIAL homeowners going into the "Fiber Biz" dialer — intentional (they're the
new-fiber leads to call).

---

## Reference — 2026-08-04 — MAPBOX GL JS knowledge (the AT&T fiber map runs on it)

AT&T's dealer fiber map (youachieve.att.com/yourefer/fiber) is a **Mapbox GL JS**
map. This is the accumulated, sourced knowledge for anyone working the hunter.

### How it renders (why the hunter works the way it does)
- Mapbox GL JS draws vector tiles + a style on a **WebGL canvas = the GPU**. Data =
  **Sources**; how it's drawn = **Layers**. AT&T's green/gold/grey dots are a point
  Source rendered by a Layer.
- The map object on AT&T's page is **hidden** (not on `window`), so the hunter hooks
  `mapboxgl.Map`/`maplibregl.Map` at page-init (`MAPBOX_HOOK_JS`) and also scans globals.
- **Dots come off AT&T's "serviceability" JSON endpoint** (response URL contains
  "serviceability"); "Search this area" (appears only AFTER you pan) triggers that fetch.
  Motion MUST be a **mouse DRAG** — arrow keys / `panBy` do nothing on the hidden map.

### Reading features programmatically (what MAPBOX_DOTS_JS relies on)
- `queryRenderedFeatures()` → features VISIBLE in the current viewport.
- `querySourceFeatures(id)` → all features in a source's **currently-loaded tiles**
  (incl. just off-screen), but NOT tiles outside the viewport. Behaves like
  queryRenderedFeatures but also finds invisible-but-loaded ones.
- `map.getSource(id)._data` → the raw GeoJSON for a geojson source (hunter reads this).
- **Timing gotcha:** sources/layers are NOT queryable right after they're added — you
  must wait for load/data. The hunter currently uses fixed `SEARCH_SETTLE` sleeps.
  POSSIBLE FUTURE IMPROVEMENT (not done): wait on `map.on('sourcedata', e=>e.isSourceLoaded)`
  or `map.once('idle')` instead of a fixed sleep -> more reliable capture, fewer 0-cells.

### Source types (how the dots are served)
- **Vector tiles** (.mvt/.pbf, pre-tiled, only visible tiles load) vs **GeoJSON** (raw,
  client tiles it) vs a plain **JSON API** (AT&T's serviceability feed). Rule of thumb:
  <5 MB GeoJSON, 20 MB+ vector tiles. Addresses ride in the serviceability JSON, geometry
  in tiles — the hunter reads the JSON off the wire (tiles carry geometry only).

### THE FREEZE — WebGL context loss (blank white, permanent) — root-caused 2026-08-04
- WebGL runs on the GPU. On a low-RAM laptop the browser drops the map's GPU context —
  console: **"Too many active WebGL contexts. Oldest context will be lost."** The canvas
  goes **blank white and never re-renders**; our Python loop keeps sweeping a DEAD map,
  so the motion watchdog never fires = looks permanent.
- **Triggers:** other VRAM-heavy tabs (video/3D), Chrome Memory-Saver/tab-discard when the
  tab is backgrounded, and software rendering (SwiftShader, when HW accel is off — it
  drops contexts real GPUs survive).
- **Detect:** the canvas fires a `webglcontextlost` event (`GL_WATCH_JS` listens; sets
  `window.__optimusGLLost`). `_map_frozen()` reads it.
- **Recovery is NOT automatic here:** a page reload lands back on AT&T's login/portal and
  the map only returns after the manual log-in + "Fiber Availability Map" clicks — which
  the hunter can't do. So on a detected freeze it **alerts + stops cleanly** (marks Hunter
  Status "stopped", no auto-restart) instead of scanning a dead map. (`_handle_frozen_map`.)
  Reopen the hunter, click the map on, press Enter to resume.
- **Prevention (shipped, launch flags):** `--disable-background-timer-throttling`,
  `--disable-renderer-backgrounding`, `--disable-backgrounding-occluded-windows`,
  `--disable-features=CalculateNativeWinOcclusion,IntensiveWakeUpThrottling,HighEfficiencyModeAvailable`,
  `--disable-dev-shm-usage` — keep the map rendering when the window is covered/backgrounded
  and stop tab-discard mid-run.
- **Operator mitigations:** close other tabs (frees VRAM), keep the Optimus window in
  front, run one tool at a time on a weak PC. A general Mapbox recovery is `map.resize()`
  when the container is shown/resized — but that doesn't fix a lost GPU context here.

### The giant blue/white blob (fixed, cosmetic)
- Mapbox **GeolocateControl** draws a "user-location accuracy circle" sized to the device's
  geolocation accuracy (95% confidence). A laptop has no GPS -> IP/Wi-Fi accuracy is poor
  (miles) -> the circle balloons into a blob covering the map and hiding dots. Real fix is
  `showAccuracyCircle:false`, but it's AT&T's config, so the hunter hides
  `.mapboxgl-user-location-accuracy-circle` via injected CSS (`GEO_HIDE_JS`). No dot affected.

### Sources
- Mapbox docs: queryRenderedFeatures example; Sources API; Events API (sourcedata/idle);
  Improve performance / Working with large GeoJSON; Blank-tiles troubleshooting;
  Locate-the-user (GeolocateControl).
- GitHub issues: mapbox-gl-js #7332 (too many WebGL contexts), #3751 (query vs source
  features), #2942 (blank on Chrome/Windows).

---

## Proposals backlog — 2026-08-04 — "detect more green" + "run longer" (researched, NOT built)

Ideas with research backing, for when the operator green-lights them. Nothing here
is implemented yet. Grouped by goal; each tagged effort/risk.

### A) Detect NEW GREEN better
1. **Event-gated capture (replace the fixed SEARCH_SETTLE sleep).** [med effort, low risk]
   Read each viewport only after the dots finish loading, not after a fixed pause.
   Pattern: after a pan, `map.on('moveend')` -> wait for `sourcedata` with
   `e.isSourceLoaded === true` (or `map.once('idle')`), THEN read. CAVEATS from research:
   the `idle` event has been flaky (reported not firing since GL 3.4, and it does NOT
   fire in HEADLESS browsers -- issue #9920). The hunter runs HEADED so idle should work,
   but ALWAYS add a max-wait timeout fallback so it never hangs waiting for idle. Net:
   fewer greens read half-loaded, fewer false "0 leads" cells.
2. **Auto-skip dead (all-grey) zones.** [low effort, low risk] If K cells in a row are
   all grey / 0 green, grow the spiral step or jump farther so time is spent where green
   is. More green captured per hour.
3. **Wire the dormant FRESH-fiber weighting.** [low-med] BRAIN notes zone_label is
   hardcoded "WORKING" so `--fresh` weighting never fires -> a just-lit all-green block is
   treated like a mature one. Wiring it makes it linger/expand on new-fiber pockets.
4. **Zoom guard.** [low] Dots only render within a zoom band; too far out = silent misses.
   Check/nudge zoom into the dot-rendering range before scanning.
5. **querySourceFeatures over just queryRenderedFeatures.** [low] Source features include
   loaded-but-just-off-screen dots; already partly used in MAPBOX_DOTS_JS -- make sure the
   source path is preferred so edge dots aren't missed.

### B) Run LONGER (fewer freezes / less memory)
1. **Cut screenshot/memory churn.** [low-med, low risk] The pixel path grabs a full-page
   PNG per viewport, but addresses come off the wire (serviceability JSON), so most
   screenshots are redundant VRAM/heap pressure that helps trigger the WebGL-context-loss
   freeze on weak laptops. Gate screenshots to only when the backend read returns nothing.
2. **Block junk network resources (NOT the map).** [med, MEDIUM risk] Research: blocking
   resource types with no data cuts load 30-60% + memory. Use Playwright routing to abort
   ads/analytics/trackers/unrelated media. HARD RULE: never block Mapbox tiles
   (api.mapbox.com, *.pbf/.mvt), fonts/sprites the map needs, or AT&T's serviceability/api
   calls -- blocking those breaks capture. Allow-list the map, block the rest.
3. **Cap/trim NetCapture buffers.** [low] Long runs leak: `seen_urls` (debug dict),
   `pending`, `endpoints` grow unbounded (research: response buffers accumulate). Periodically
   trim the debug dict + drop already-flushed pending. The address `seen` set must stay (dedup).
4. **Chromium memory flags.** [low] `--js-flags=--max-old-space-size=<MB>` bumps V8 heap so
   GC has room. DO NOT use `--disable-gpu` (the map NEEDS WebGL/GPU) or `--single-process`
   (unstable). `--disable-dev-shm-usage` already added.
5. **Resume-where-it-stopped.** [med] Persist the grid `done` set / last center to disk so a
   freeze-stop can resume the same area instead of re-covering. (No auto-reload -- still needs
   the manual map-on clicks, but it resumes coverage.)
6. **Auto-slow on weak PCs.** [low] Detect low RAM (psutil) -> gentler pacing = less churn.

### Recommended first two (best value, contained)
- A1 event-gated capture (with idle-timeout fallback) -> catches more green.
- B1 cut screenshot churn -> runs longer.

### Sources
- Mapbox idle/until: mapbox-gl-js #10192, #13236, #12964, #9920 (idle not firing in headless).
- Query features: docs queryRenderedFeatures / querySourceFeatures.
- Playwright memory: microsoft/playwright #15400, #28942; WebScraping.AI memory best-practices.
- Chromium flags: Puppeteer/headless memory guides (js-flags max-old-space-size; avoid
  --disable-gpu for WebGL; --disable-dev-shm-usage).

---

## Skill — 2026-08-04 — TRACKING cable outages + new fiber installs (built + scheduled)

Goal: know (A) where cable internet is DOWN today (pitch "your cable's out, fiber's live,
switch") and (B) where new AT&T fiber just turned on / is being announced (aim the hunters).

### Best sources (researched)
- **Cable outages (real-time):** Downdetector is the gold standard — detects outages from
  user-report SPIKES before the ISP admits it, mapped by city. Alternatives: Outage.Report,
  GeoBlackout, ISPDown. Plus **local news** and **Reddit** (r/Comcast_Xfinity, r/Spectrum,
  local city subs) light up during outages. Downdetector has a paid API; the public pages +
  web/news/Reddit search are enough for a daily scan.
- **New fiber (street-level, most actionable):** OUR OWN HUNTER on the AT&T dealer map is the
  most real-time, granular source. The public maps LAG MONTHS — FCC National Broadband Map's
  current data is Dec 2025 (May 2026 release); BroadbandNow similar. So do NOT rely on FCC/
  BroadbandNow for "just lit"; use the hunter + its New-Fiber Alerts.
- **New fiber (new MARKETS to point the hunter at):** AT&T press releases + tech/business
  news (Finviz/StockTitan/local) + Reddit r/ATTFiber announce expansions city-by-city.

### What was built
1. **Hunter New-Fiber Alerts** (already shipped): flags a freshly-lit block (dense green,
   low grey) -> New Fiber Alerts tab + public GitHub file + optional email. Street-level.
   (NOTE: only fires on the UPDATED hunter; the machine seen 2026-08-04 was on old code, so
   the tab didn't exist yet.)
2. **Daily web tracker Routine** `trig_01DfRVRoPajmieDYNfY1xtmQ` ("Optimus — cable outages +
   new fiber tracker (daily)"): fires a fresh session daily 14:00 UTC (9am Central), WebSearches
   for cable outages (Xfinity/Spectrum/Cox) TODAY in Houston TX, OKC metro, Warren/Detroit MI,
   AND recent AT&T fiber expansion announcements; emails + phone-pushes the owner a short digest, PRIVATE (outages
   first). Silent ("nothing new") when nothing real is found, so no junk email. Target markets
   are hardcoded in the prompt -> update via update_trigger if markets change.

### The play
- Outage digest hits inbox -> reps call that market SAME DAY: "your <cable co> is down, AT&T
  fiber's live at your address, switch." Strongest vs Xfinity (worst-rated cable, 60/100, data
  caps).
- New-fiber announcement -> point hunter + scraper at that new metro to build the match list
  before competitors.
