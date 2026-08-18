# Optimus Session Log

## 2026-05-23 22:03 CT — Claude
**SESSION GOAL:** Fix GitHub-write via Make so it reliably creates AND updates files, document it in the BRAIN, and start timestamp + session-goal stamping.

- Fixed Make scenario 5084486 (GitHub write): SHA read is now non-fatal (handleErrors), and the PUT includes `sha` only when the file already exists — so it creates new files and updates existing ones.
- This file being created here is the proof the create-path works.
- Capability map: GitHub write = Make scenario **5084486**. BRAIN append = Make scenario **5073448**. Both run via update-trigger → activate → run → deactivate.

## 2026-08-18 — Claude (lead-gen-software-research)
**SESSION GOAL:** Full sweep — brain, other chats, repo, Railway, Gmail, Drive, the live sheet — then fix what the sweep exposed.

Findings:
- **Leaked key.** Google Maps/Places key `AIzaSy...kCG9g` was hardcoded in
  themapman.py, mapman_api.py, mapman_api_batch.py, mapman_pydroid_runner.py and
  is in git history. Removed from the working tree; all four now call
  `optimus_secrets.get_maps_api_key()`. **The key itself still has to be rotated
  in Google Cloud — deleting the line does not un-leak it.**
- **Wrong sheet in BRAIN.** BRAIN.md said active sheet was `12PII...`; the code
  actually opens `1FhO...` ("ATT FIBER LEADS", 5.5 MB, last written 2026-08-18).
  Four different sheet IDs are referenced across the .py files. Corrected.
- **Branch sprawl.** 8 unmerged `claude/*` branches, ~14,000 lines, none on main.
  Documented in BRANCH_MAP.md. Richest: `chat-repetitive-questions-9ex5h7` (+10,438).
- **The unlock.** `optimus_api_capture.py` / `backend_classifier.py` read the AT&T
  dealer-map backend JSON (address + lat/lng + subscriber_ban + build-type code)
  instead of counting pixels. Blocked only on filling FIBER_BUILD_CODES /
  COPPER_BUILD_CODES via one `inspect()` run over a green-heavy area.
- **Railway.** Two projects (fulfilling-growth, loving-heart) each run one
  Go-High-Level-MCP-2026-Complete service. Both SUCCESS, both last deployed
  2026-06-30. Duplicate — consolidate to one.

Changed: optimus_secrets.py (new), BRANCH_MAP.md (new), BRAIN.md, .gitignore,
themapman.py, mapman_api.py, mapman_api_batch.py, mapman_pydroid_runner.py

## 2026-08-18 (later) — Claude — GOLD DOT CAPTURE
**SESSION GOAL:** Make the Precise Hunter reliably read GOLD (copper-upgrade) dots and write them to the sheet, the way it already does GREEN.

Read the live sheet through the Autosheet connector (Drive's connector only
returns a truncated view). Real numbers, ATT FIBER LEADS (1FhO...):

    Precise Fiber      449,812 rows   GREEN 443,983 | ORANGE 5,593 | GOLD 0 | GREY 0 | other 235
    Hunter Status       32,912        Maps Businesses  31,616
    Fiber Green Biz      6,058        Upgrade Orange Biz   23
    Backend Analysis     3,000        Fresh Leads       3,000
    Backend Capture      3,000        Fiber Scout       3,000
    Enriched Leads       2,001        _dispatch 10, _Dedupe Lock 2, Sheet6 0
    Capture range: 2026-06-16 22:49 -> 2026-08-18 11:31 (still running)
    Business/phone fill is 4.2% (2,102 of 50,000), NOT the 100% COUNTA implies -
    the blank cells hold empty strings, which COUNTA counts.

WHY GOLD WAS DISAPPEARING (root cause, three compounding bugs):
1. `classify_status()` in optimus_dot_detect.py could only recognise copper
   from the literal word "copper" in popup text. The backend JSON never says
   "copper" - it carries curr_ntwrk_bld_type_cd = FTTN-BP / IP-RT / FTTN.
   So every copper customer fell through to CUSTOMER, was treated as grey,
   and was dropped by the `continue` in the writer. Gold could never appear.
2. That fallback runs whenever backend_classifier.py fails to import - and the
   import was wrapped in a bare `except: _classify_lead = None` with NO message,
   so gold capture could be silently off and look identical to working.
3. The GOLD CLUSTER alert compared `r[1] == "GOLD"`, but rows are written with
   dot_color(), which emits the legend word "ORANGE". The alert was dead code.

FIXED (all additive - green capture is untouched, verified by test):
- optimus_dot_detect.py: FIBER_BUILD_CODES / COPPER_BUILD_CODES now live in the
  low-level module, and classify_status() takes a `build` argument that decides
  GOLD vs GREY for a customer. Works with or without backend_classifier.py.
- precise_fiber_hunter.py: _lead_status() extracts curr_ntwrk_bld_type_cd off
  the raw record and passes it to the fallback; a failed backend_classifier
  import now prints a loud warning instead of failing silently; gold-cluster
  alert compares against the legend word.
- NEW "Gold Upgrade Leads" tab: gold dots are written there as well as into
  Precise Fiber, so they are workable instead of buried 1-in-80 among green.
  Fully guarded - a gold-tab failure cannot stop the green capture.
- optimus/test_gold_capture.py: 18 tests, all passing. Existing
  test_backend_classifier.py and test_hunter_fixes.py still pass.

NOTE ON THE MARKET DATA (corrects an earlier claim in this log):
The Backend Analysis tab holds a real 105,500-record capture (Vintage Park /
NW Houston, 4 ZIPs, 2026-07-15). Cross-tab:
    unavailable + non-cust   62,942   -> GREEN
    fttp-gpon   + customer   42,456   -> GREY
    fttn-bp/fttn/ip-rt + customer 93  -> GOLD
That is 40.3% penetration, matching BRAIN's stated 40% figure - the pipeline is
sane. But it also means GOLD is genuinely rare in these ZIPs (93 in 105,500,
0.09%). Gold is worth capturing and is a strong freshness signal, but it is not
a large standalone segment here. Do not size a campaign on it before measuring
gold density in the target ZIPs.
