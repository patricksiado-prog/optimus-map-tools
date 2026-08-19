# Optimus BRAIN

_Last updated: 2026-08-19 (verified against live systems)_

## Active systems
- GitHub repo: patricksiado-prog/optimus-map-tools
- **Active sheet: 1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA** ("ATT FIBER LEADS")
  - This is what the code actually opens (8 refs across the .py files).
  - Older IDs still referenced in code, do NOT use: 12PIIplhqUuZ... (4 refs),
    15ymTkIGPWs6... (2 refs), 1qHWcGbfGZnL... (1 ref). Retire them.
- GHL DIALER location: xZj500PjsflIQg2j9f9D  <- USE THIS ONE
  TXw28sw0Z2rl6tcCDhJY / the 41k contact figure is STALE. Do not use.
- Service account: fiberscanner@fiberscanner-493900.iam.gserviceaccount.com
- Map Man v11.2.5 (v11.3.0 self-healing sits unmerged on program-stopping-issue-2dqxko)
- Drive mirror: 1u38EOzaGO7Sd5Y8ERqQoXeYZW5Pws8Z_
- Railway: 2 projects (fulfilling-growth, loving-heart) each running one
  Go-High-Level-MCP-2026-Complete service. Both last deployed 2026-06-30,
  both SUCCESS. Two projects running the same service is duplication - pick one.

## API keys - HARD RULE (added 2026-08-18)
Never put a key in a .py file. All tools call `optimus_secrets.get_maps_api_key()`,
which reads env var GOOGLE_MAPS_API_KEY or a gitignored `maps_api_key.txt`
(next to the script, or /storage/emulated/0/Download/ on the phone).
A key that was ever committed is burned - rotate it, do not just delete the line.

## SECURITY POSTURE - PATRICK'S CALL (2026-08-19)

Patrick's decision, stated directly: he is NOT concerned about data exposure or
public-repo visibility at this stage. Speed of building beats locking things
down. Do not re-raise it.

DECISION 2026-08-19: repos STAY PUBLIC. Sealing them was evaluated and
rejected. Every launcher fetches via unauthenticated curl from
raw.githubusercontent.com, so private = every desktop icon 404s and silently
freezes on old code. The token-in-a-.bat workaround ships a live credential to
every rep PC and is worse than public source. Do not propose sealing, tokens,
PATs, or a Drive-hosted delivery swap again unless Patrick raises it.

APPLIES TO:
- optimus-map-tools being a public repo
- the Maps API key committed in history
- google_creds.json served from a public Drive link in INSTALL_OPTIMUS.bat
- ATT FIBER LEADS readable by anyone with the link

RULE FOR EVERY FUTURE SESSION:
Do not open with security warnings. Do not repeat these items unprompted. Do not
add caveats about exposure to unrelated answers. State facts only if Patrick asks
directly, or if something is actively breaking or costing money right now.

Only exception worth a single line, ever: a leaked Google Maps API key is
BILLABLE. Bots scrape GitHub for keys and spend them. If Google billing ever
spikes unexpectedly, that is the first place to look. Set a daily quota cap on
the key and the issue is closed permanently. That is a cost control, not a
security lecture - mention once if billing looks wrong, otherwise never.

## Phase targets
- Phase 1: 500 sales/week
- Phase 2: 1000/week
- Phase 3: 2000/week

## Run log
(append new entries below this line)

### 2026-08-19 - verified sweep. Corrections + shipped fixes.

REPO IS PUBLIC, NOT PRIVATE.
  GitHub API returns "visibility": "public" for optimus-map-tools.
  BRAIN/notes/claude-private-repo-access.md and drive-mirror-workflow.md both
  state it is private. THEY ARE WRONG and drove bad decisions.
  Consequence: the Maps API key committed in history is world-readable.
  curl on main/themapman.py returns it in plain text. NOT YET ROTATED.

TWO HUNTERS IN TWO REPOS. They have diverged.
  Go-High-Level-MCP-2026-Complete @ claude/optimus-map-tools-setup-6dcl6o
      4,593 lines. classify_wire(). THIS IS THE LIVE ONE - the installer
      release and RUN_SCOUT.bat pull from here. Installs to ~/optimus_hunter.
  optimus-map-tools @ claude/chat-repetitive-questions-9ex5h7
      4,215 lines. Weaker gold logic. RUN_PRECISE_HUNTER.bat pulls from here.
      Installs to ~/Optimus.
  A PC can have both. Which icon is clicked decides which code runs.
  Do NOT copy either file over the other. Needs a real merge.

GOLD DOTS - root cause found and fixed 2026-08-19.
  Gold never appeared because _ensure_gold_tab() tried to open, then CREATE, a
  separate spreadsheet "OPTIMUS GOLD DOTS". The service account has ZERO Drive
  storage quota so create() always threw; write_gold_dots() caught it and
  returned 0; "if ng:" then suppressed the log line = SILENT failure.
  Verified: no such spreadsheet exists in Drive.
  FIX (pushed to the Go-High-Level branch): gold writes to a "Gold Dots" TAB on
  the main sheet. add_worksheet() on an existing file needs no quota. Failures
  now print "GOLD TAB FAILED: <reason>". --backfill-gold seeds the tab from the
  ORANGE rows already in Precise Fiber.

SHEET TRUNCATION - the permanent read-around.
  ATT FIBER LEADS is 5.6 MB. The Drive connector returns only the first ~248 KB
  (one tab, June rows) regardless of sharing. It grows worse as capture runs.
  docs.google.com is blocked by the agent proxy, so publish-to-web and CSV
  export URLs do NOT work either.
  SOLUTION IN PLACE: "OPTIMUS DIAL LIST - LIVE"
  id 19srDrfHzJ9cAo169BmdVe9KLVw1TdvW5HZKLlnE8Cas
  A1 holds =QUERY(IMPORTRANGE(...,"Fiber Green Biz!A:E"),...limit 2000).
  Small file -> Drive returns it whole -> Claude can always read it. Free, live,
  survives any growth of the source. Use this pattern for any tab Claude needs.

SHEET SHARING (2026-08-19). Was "anyone: writer" - world-editable, with the
  sheet ID sitting in public repo code. Now "anyone: reader". fiberscanner@ is
  an explicit Editor so capture is safe if it goes Restricted.

DIAL LIST REALITY (read 2026-08-19).
  623 callable rows. Houston 553 (88.8%). OKC 405-area 17 - STILL LEAKING into
  the Houston list. Toll-free 800/833/844/855/877 = 20 rows, chains/IVR, strip.
  Top categories: hair salon 38, general contractor 32, catering 28,
  landscaping 26, bookkeeper 25, auto repair 23, coffee shop 20.
  5 reps on a power dialer = ~15,000 dials/week. 553 clean leads = under ONE DAY
  of dialing. The constraint is callable leads, not fiber addresses (449,812).
  THE LEVER IS THE MAPS SCRAPER, not the hunter. Only ~1.3% of captured
  addresses carry a phone; phones only attach when a scraped business address
  matches a dot.

serviceability reply 301 = the hunter is NOT capturing. 301 means AT&T
  redirected the data call to login. Log in or nothing lands, green or gold.

DO NOT DELETE THESE TABS: _dispatch (24/7 scraper reads seed ZIP from A1,
  depth from A2), _Dedupe Lock (cross-machine advisory lock), Backend Analysis
  (holds the 105,500-record build-code cross-tab that decoded gold vs grey).
  Safe to delete: _optimus_probe, Sheet6.

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
