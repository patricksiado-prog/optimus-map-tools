# Optimus — operating brain

Claude Code loads this file automatically at the start of every session in this
repo. **Read the CURRENT STATE block below first — it is the only part that
claims to be true right now.** Everything under it is the historical record,
appended newest-at-the-bottom. Where two sections disagree, the later date wins
and you say so out loud. Long-form detail lives in `BRAIN.md`.

---

# CURRENT STATE — updated 2026-09-04 evening (WE CALL DND — new rule; Milton 134 callable; gold+grey dedup unpushed)

**Update this block whenever any line in it changes, in the same turn.** A
finding buried 2,000 lines down in the log is a finding nobody will read. This
block is short on purpose; if a line needs more than two sentences, put the
detail in a dated section below and point at it from here.

Mark every line **MEASURED** (with how and when) or **ASSUMED**. Never let the
two share a voice — that is the mistake that let "register for the 20M-cell
beta" survive four sessions unchecked.

### MILTON DELIVERED — 126 CALLABLE OF 141, AND EVERY COLOUR ON IT IS UNVERIFIED (2026-09-04)

Patrick: *"can u give me the new fiber area in milton look phone numbers and
info."* Built `MILTON_NEW_FIBER_callable.csv` off a LIVE GHL pull of the
`evergreen-estates-milton` tag (141 records, 141 with a phone, **0 with
`address1` — the street lives only in the file I built 09-04**, joined back by
GHL contact id).

**15 STRIPPED under RULE 0b: 7 said NOT INTERESTED, 8 are DND.** Never re-add
them. 126 remain.

| Tier | n | What it is |
|---|---|---|
| 1 REPLIED YES | **3** | already answered a text — call today |
| 2 AT&T CUSTOMER (`att.net`/`att-1`) | **41** | the ONLY hard evidence on this list — an upgrade, no competitor to beat |
| 3 NEVER CONNECTED | 56 | fresh in the pocket |
| 4 TRIED, NO ANSWER | 26 | texted/dialed, never connected |

**22 are landline CALL-ONLY** (never text — Twilio 30006). **110 carry registry
DNC — call anyway**, standing rule. **3 have no house number**; the row says ask
on the call.

**STREET DENSITY = the pocket, and it matches Patrick's own AT&T map screenshot:
PANSY DR 20 · MARIGOLD AVE 17 · SHAMROCK ST 12 · ZINNIA AVE 11 · CAMELLIA AVE 10
· ASTER ST 9 · AZALEA AVE 9 · WILLARD NORRIS RD 8 · GARDENIA AVE 7.**
(`5520 Shamrock St` was the address in his screenshot.)

**THE HONEST CAVEAT, AND IT GOES ON THE COVER EVERY TIME: MILTON IS NOT ON THE
HUNTER SHEET AT ALL.** Measured across all 5 read paths 2026-09-04 — zero
Milton/FL/32570 rows on any of the 8 tabs. The only run covering it
(`20260902-182120`) classified 338,456 addresses and wrote **0** — everything
parked behind the AT&T login. So 85 of the 126 rows carry
`UNVERIFIED - ASK WHO THEY HAVE TODAY`; only the 41 att.net rows carry real
evidence.

**DO NOT TEXT THIS LIST AGAIN.** 119 of these people were texted 2026-09-03 and
**at least 7 STOP'd within 90 minutes** — over-contact, not a bad number. The
file flags every texted row `ALREADY TEXTED - do not text again, CALL`.

### THE FIVE COLOURS, DEDUP, AND GHL-BACK-TO-THE-SHEET — CHECKED AGAINST THE LIVE SOURCE (2026-09-04)

Patrick: *"green grey gold bis fiber green biz / sofware reflects this / also
dedup / ghl enriched leads are reflected."* Answered by reading the LIVE
`maps_scraper_standalone.py` (2,763 lines) and `precise_fiber_hunter.py` (8,710)
off raw.githubusercontent, not by trusting this file.

**1. THE FIVE COLOURS — the software DOES reflect them, all five, both ways.**
Hunter writes `Precise Fiber` (green) · `Gold Confirmed` (gold) ·
`Grey Fiber Customers` (grey) · `Unknown Customers`, each row carrying its
`STATUS_*` wording (hunter lines 123-140). Scraper writes `Fiber Green Biz` and
`Upgrade Orange Biz` (lines 486-487). **And the follow-up board READS all of
them back** — line 1549 `for tab in (GOLD_TAB, GREY_TAB)`, line 1557
`for tab in (GREEN_BIZ_TAB, ORANGE_BIZ_TAB, MAPS_BIZ_TAB)`, plus Precise Fiber —
so an enriched row picks up its true `Dot Color` AND a `Tab` column naming which
of the five it sits on. That is his spec, and it is already in the deployed code.

**2. DEDUP — THE REAL GAP, AND IT EXPLAINS THE GOLD PROBLEM.**
`dedupe_all_tabs()` (scraper line 920) runs every 30 min in a background
process, holds the cross-machine `_Dedupe Lock`, CSV-backs-up before touching
anything, caps at 6,000 removals per pass. Its job list is **Maps Businesses ·
Fiber Green Biz · Upgrade Orange Biz · Precise Fiber (every 6th pass)**.

**`Gold Confirmed` and `Grey Fiber Customers` ARE NOT IN IT AND NEVER HAVE
BEEN.** The two colour tabs a rep actually calls off are the two nothing has
ever cleaned. **That is the mechanism behind "4,707 gold rows = 10 unique
addresses"** — 7631 Fuqua written 96 times, 800 N Arcola 50, 611 E Myrtle 22.
Grey is 56,799 rows on the same footing, and grey is the SCRUB list.

**FIX WRITTEN AND TESTED, NOT PUSHED (RULE 0):**
`patches/dedupe-gold-grey/`. Two lines added to `jobs`, reusing the
`pf_key`/`pf_score` already proven on Precise Fiber (keep the FULLEST copy of an
address, not the earliest). Test runs the REAL `_dd_dedupe_tab` against a fake
workbook seeded with the measured duplication: **172 gold rows → 5 unique, 41
grey → 2, the fullest 7631 row beats its skinny twin, second pass removes 0,
missing tab safe. ALL TESTS PASS, py_compile clean.** It is the SCRAPER, so no
`BUILD_DATE` bump; it self-updates on any byte change.

**3. GHL ENRICHED LEADS REFLECTED — HALF DONE, and the missing half is a token.**
`Enriched Leads` is LIVE in the split workbook with all 29 columns
(`ENRICHED_HEADER`, scraper line 1463): the hunter's own 13 + `Tab` + Name ·
Cell · Phone Type · Enriched At · Source · Pool · GHL Contact ID · Likely Gold ·
DNC + **Dialed · Last Call · Disposition · DND · Dead · Status At**, whole row
coloured green CB / red NI-DEAD / blue SOLD. `Sales Log` alongside it.

**But `sync_sheet_log` reads a Drive feed folder that CLAUDE has to drop
(`FEED_FOLDER_ID = 1XOqADybKvneC5gwsxjpsGkVC6RLQ-1an`). Nothing on Patrick's PC
reads GoHighLevel.** So the six GHL columns are only as fresh as the last time a
session published a `status` feed — they go stale the moment a chat ends. **The
real fix is `ghl_token.txt` next to `github_token.txt`** (GHL → Settings →
Private Integrations, contacts.readonly); the scraper then reads GHL itself at
every launch and the board stays live with nobody typing anything. Not built —
it cannot be tested from here without the token, and RULE 0 says never push
untested code. **Needs Patrick's go and the token, and the token never travels
in chat.**

### THE SHEET IS CLEAN. THE SOFTWARE DOES IT ITSELF. THE BRAIN FILE WAS THE PART STILL BROKEN — FIXED THIS TURN (2026-09-04)

Patrick: *"I asked for the sheet to be cleaned and junk tabs removed and the
software to reflect that and I wanted better memory and brain files."* Three
asks. Status of each, MEASURED, not claimed.

**1. SHEET CLEANED — DONE.** tabs.json stamped 2026-09-04 03:08:57 lists **8
tabs and ZERO junk.** Every TEST-*, TMP, ZZ_, _probe, _temp, Backend* and
`Gold Dots` tab is gone. The gold date-purge also ran and completed — the
console printed *"nothing to remove -- all 1884 rows are post-fix"*, and
`Gold Confirmed` is 4,707 rows, all post-08-24.

**2. THE SOFTWARE REFLECTS IT — DONE, and brain-verify proves it every session.**
Passing claims: *the whole sheet clean runs at scraper startup* · *junk tabs are
an explicit NAMED list, not a whitelist* · *the clean is NO LONGER gated behind
open_sheet()'s 140k-cell add_worksheet* · *stale done-flags are ignored (v2
marker)* · *`TEST-Gold-*` can only leave via migration, never deletion* · *tab
counts publish themselves at launch, stamped*. Nobody runs anything: it happens
in the first 30 seconds of a Maps Scraper launch.

**THE ONE PIECE STILL OUTSTANDING: `CLEAN_SHEET.bat` is STILL the old
whitelist** and would delete rep-built tabs. brain-verify flags it every session.
The inverted-to-a-named-junk-list fix is written and TESTED in
`patches/clean-sheet-one-doubleclick.md` and **NOT PUSHED — RULE 0.** Nothing
needs it (the scraper does the job), so it is a landmine, not a gap: **do not
run that .bat.**

**3. BETTER BRAIN FILES — THIS WAS THE REAL FAILURE AND IT WAS MINE.**
CLAUDE.md was cut to 890 lines on 09-02 and **I grew it back to 2,589 in two
days** — 52 dated sections, loaded in full on every single turn. The file's own
rule says archive past ~800 and I ignored it while writing more.

**Fixed this turn: 2,589 -> ~1,300 lines.** Thirteen dated blocks moved VERBATIM
to BRAIN.md (nothing deleted — `brain find` reaches all of it), each leaving a
one-line pointer. Also killed in the same pass: the `optimus-sheet` skill's
29-tab map (a week stale, it is what kept resurrecting "11,490 gold" and "645k
Precise Fiber"), the dead "read DASHBOARD and README FIRST" path in both files,
and two finished items still sitting on the Blocked-on-Patrick list.

**THE MAINTENANCE RULE, restated because I broke it:** when this file passes
~800 lines, archiving the oldest dated sections is NOT a decision to be raised
with Patrick — it is routine, do it in the turn you notice. A dated block older
than ~24h belongs in BRAIN.md unless it is a rule, an ID, or currently true.

**STILL UNANSWERED AND IT IS HIS TO ANSWER: four hand-built tabs went with the
21** — `Warm Backlog — Replied YES` (40 people who said yes), `Angleton Call
List — Aug 2026`, `WORK LIST — Beaumont + Angleton`, `GOLD — CLEAN`. Not the
scraper's named junk list (it printed *"removed 1"*), not `CLEAN_SHEET.bat`
(its KEEP list protects two of them). Google File -> Version history restores
them.

### RESI IS THE PRODUCT. THE BIZ TAB IS A COMPASS, NOT A CALL LIST. (Patrick 2026-09-04: *"not bizz were focused on resi"*)

**KILLED THE SAME TURN I OFFERED IT: the 3,767-row Fiber Green Biz call file is
NOT wanted. Do not build it, do not re-offer it.** He confirmed the green-biz
tab's job in the previous message (*"how u detect new fiber Green and gold
concentrations"*) and then drew the line: **it points at the ground, we sell the
HOUSES on that ground.** Same shape as the gold rule — gold is the compass,
green is the money — one level up.

**SO THE READING ORDER IS: green-biz cluster tells you WHERE, then you work
`Precise Fiber` (resi green) and `Gold Confirmed` (resi copper) inside it.**
Never hand a rep a business list off the back of a detector reading.

**WHAT THE BRAIN ALREADY HOLDS ON THE RESI SIDE — searched, not re-derived:**

| Population | Where | n | State |
|---|---|---|---|
| resi GREEN | `Precise Fiber` (green-only since 08-26; new green → split workbook) | **687,923 rows** | unreadable from a Claude session — needs `sheet_feed.py` |
| resi GOLD | `Gold Confirmed` | **4,707 rows** | a SIGHTING count — 176 readable rows were 10 unique addresses |
| resi GREY | `Grey Fiber Customers` | **56,799 rows** | never dial, and it is the scrub list |

**THE RESI CONCENTRATION MAP IS ALREADY BUILT AND IT IS GOLD DENSITY PER STREET**
(measured 2026-09-04, in the call-list section below): Beaumont carries **365 of
the 513 gold**. Densest streets **Chatwood 22 · Stacewood 19 · Monterrey 16 ·
Norwood 16 · Shakespeare 14 · Brandywine 13 · Galway 12 · Potter 12**, then
Armstrong / Eldridge / Todd / Norvell 9 each. **That is the residential version
of exactly what he is describing, and it is the door-knock map as well as the
dial map.** Gold density = fiber lit recently, nobody converted it.

**THE ONE THING THAT MAKES RESI HONEST IS STILL NOT RUN.** Under RULE 0b the
resi green is the WEAKEST population we own — of 84 board-checked addresses,
**21 came back GREY and ZERO residential rows came back GREEN.** The fix is
`py sheet_feed.py --tab "Grey Fiber Customers"` then `--tab "Precise Fiber"`
then `--tab "Gold Confirmed"` on the hunter PC. **`_feed/sheet/` still holds only
`tabs.json`; every chunk URL is a 404.** Until those chunks exist, every resi
list ships with unverified rows and has to say so.

### THE GREEN-BIZ TAB IS THE NEW-FIBER DETECTOR — AND ITS GOLD HALF IS DEAD (Patrick 2026-09-04: *"fiber green tab is how u detect new fiber Green and gold concentrations"*)

**This is the tab's PURPOSE and I had been treating it as just another lead
list.** Record it as the method, not as a fact about one tab.

**HOW THE DETECTOR WORKS.** The Maps Scraper pulls businesses off Google Maps
into `Maps Businesses` (39,294), then cross-matches every business address
against the hunter's own dot tabs. A green match writes `Fiber Green Biz`; a
gold match writes `Upgrade Orange Biz`. **So a CLUSTER of green businesses is a
block where fiber is lit and nobody is on AT&T — and it is a better beacon than
a residential dot, because businesses are sparse, named, and sit on the main
road of whatever neighbourhood just got built.** Find the green-biz cluster,
then work the residential green and gold around it.

**THE GOLD HALF OF THE DETECTOR HAS BEEN PRODUCING NOTHING: `Upgrade Orange Biz`
= 62 against 39,294 businesses.** Cause is already recorded — `init_match` read
dot colours from `Precise Fiber`, which has been GREEN ONLY since 08-26, so the
orange side scanned a tab with zero orange in it. **Fixed 2026-09-03 (gold now
loads from `Gold Confirmed`), NEVER RUN.** It needs one Maps Scraper launch.
Until then Patrick's method only works on the green half.

**WHAT THE TAB ACTUALLY CARRIES — MEASURED 2026-09-04 off `read_file_content`,
and it is thinner than the hunter tabs:** `Business Name | Phone | Address |
Website | Category | <hand-typed call status>`. **NO `Captured At`, NO Lat/Lng,
NO Dot Color, NO City/State/ZIP.** So you cannot date a green business off this
tab and you cannot map one precisely — the colour was decided at match time and
not written down. **That is the gap to close if the detector is to be trusted**
(the hunter's own tabs carry all four).

**THE READABLE SAMPLE, 356 of 7,300 — a BOUNDED SAMPLE IN SCRAPE ORDER, NOT the
tab.** 330 of 356 have a phone. Two distinct populations: an **Oklahoma City**
block at the top (405 numbers, bare streets like `1524 SE 44TH ST`, no city at
all — 120 of the 356 have no parseable city) and then **Houston, concentrated
hard: 77027 = 121 · 77046 = 45 · 77006 = 40 · 77002 = 30.** 77027 is
Galleria/Uptown. **DO NOT extrapolate those ZIP counts to the tab** (Check 2) —
the sample is the first ~355 rows, so it reflects scrape order.

**THE TWO COMMANDS THAT TURN THE DETECTOR BACK ON, both on the hunter PC:**
`py sheet_feed.py --tab "Fiber Green Biz"` (publishes all 7,300 in chunks Claude
reads with plain curl — that is the real concentration map) and **one Maps
Scraper launch** to repopulate `Upgrade Orange Biz` with the fixed match. Add
`--tab "Upgrade Orange Biz"` after it runs.

*(Archived: the full Fiber Green Biz measurement. Headline kept in CURRENT STATE — 7,300 on the tab, 3,767 enriched in GHL, 3 ever in a call list, and the only 8 board-confirmed greens were all businesses on it.)*

### "4,500 GOLD" DOES NOT EXIST AS 4,500 DOORS — MEASURED OFF THE TAB ITSELF (2026-09-04)

Patrick asked three times for "the 4500 golds". **All five read paths tried.
Path 1 WORKED:** `read_file_content` on production now returns all 8 tabs, and
`Gold Confirmed` comes back as block 4 — **176 rows containing 10 UNIQUE
ADDRESSES.**

| rows | address |
|---|---|
| **96** | 7631 FUQUA ST, HOUSTON TX 77075 |
| **50** | 800 N ARCOLA ST, ANGLETON TX 77515 |
| **22** | 611 E MYRTLE ST, ANGLETON TX 77515 |
| 2 | 1112 N ARCOLA ST, ANGLETON |
| 1 each | Sommermeyer · Nyoka x2 · Edmond OK · Jersey Village |

**170 of the 176 carry `Tier: VERIFIED_GOLD`** — the real marker, just written
over and over. **`Build Code` and `Status` are EMPTY on all 176.** Only 2 have a
phone; 170 have City and Lat/Lng.

**THIS IS THE SECOND INDEPENDENT SAMPLE TO LAND ON THE SAME FOUR ADDRESSES.** The
brain already recorded "170 VERIFIED_GOLD rows in a sample were 4 unique
addresses: 7631 Fuqua, 800/1112 N Arcola, 611 E Myrtle". **Confirmed today from a
different read.** So `Gold Confirmed` = 4,707 is a SIGHTING count, not a door
count, and the duplication is enormous — one address written 96 times.

**DO NOT extrapolate a unique total from this** (Check 2). The sample is bounded.
What is proven is only that the tab is heavily duplicated and 4,707 ≠ 4,707 doors.

**THE TWO THINGS THAT SETTLE IT, both one line on the PC:**
`py gold_audit.py` (rows vs UNIQUE addresses vs duplicates, ~10s, read-only) and
`py sheet_feed.py --tab "Gold Confirmed"` (publishes the whole tab in chunks
Claude reads with plain curl). **Neither has ever been run** — `_feed/sheet/`
holds only `tabs.json`, every chunk URL is a 404.

**AUTOSHEET RE-TESTED LIVE 2026-09-04 and it is STILL `api-billing-empty-balance`.**
That is path 5 closed until a card goes on it.

**WHAT IS ACTUALLY CALLABLE: the 505 gold in GHL with a name and a cell** —
delivered as `2_GOLD.csv`, 432 never dialed. The raw tab has no names and almost
no phones, so a row there is not a lead until it is enriched.

### THE AT&T LOGIN NEEDS A HUMAN — MEASURED AT LAST (run `20260904-090820`, 2026-09-04 09:20Z)

The hunter DID launch this morning at 09:08 and **died 12 minutes later**.
Phases: `LOGGED_OUT` → `LOGIN_TIMEOUT` → `exit`. `auth_ok: false`,
`delivery: PARSE_ERROR`, classified 0, written 0.

**THE NEW DETAIL THAT SETTLES IT — `capture_truth.notes` says:
*"access chooser, not the map"*** and *"NOT JSON — AT&T sent something this
parser cannot read. First 120 chars: `<!DOCTYPE html>`"*. **AT&T is serving an
ACCESS CHOOSER page — an account/role picker a person has to click through.**

**So the question the brain listed as UNMEASURED is now MEASURED: saved
credentials alone do NOT get in. A human has to log in and pick.** Relaunching,
watchdogs and scheduled tasks cannot solve this one — they will each burn 12
minutes and exit. Patrick or the local session with a human at the keyboard has
to clear the chooser once; after that the hunter runs itself.

*(Archived: how the 1,937-name call list was built. `OPTIMUS_CALL_LIST_Sep4.csv`. Gold density per street is in CURRENT STATE.)*

*(Archived: the chaser's first run and the unreadCount correction. The rule that survives: `unreadCount` means nobody opened it in the GHL inbox, NOT that nobody replied — pull the conversation and check whether the last INBOUND has an outbound after it.)*

### IT LANDED. THE SHEET IS ENRICHED — AND THE BOARD PROVED ED RIGHT (MEASURED 2026-09-04 12:20Z)

**The split workbook went 1,024 bytes → 20,328, modified 2026-09-04 07:59:07Z**
(2:59am CT). It had been untouched since 08-30. **`Enriched Leads` is LIVE with
all 29 columns**, `Sales Log` created. Three feed files renamed **LANDED** at
07:59 (called-audit, pcola-fresh, alpha-t1-warm). The **local session** did it,
not the scraper. The Maps Scraper separately launched at **03:08:57** (tabs.json
stamp moved off 09-02 23:39:40 for the first time).
**The SALES feed did NOT land** — `_landed.json` reads `sales: files 0, landed 0`.

**THE FINDING, and it is the whole week's argument settled. Of the 84 rows the
Drive read returns (a BOUNDED SAMPLE, not the tab):**

| Board wrote | n | Means |
|---|---|---|
| **GREY — "Existing AT&T Customer"** | **21** | **NOT A LEAD.** Already on AT&T fiber |
| UNVERIFIED — "Not on the hunter map yet" | 55 | The colour was never real |
| GREEN | 8 | **every one a BUSINESS** |

**ZERO residential rows came back GREEN.** **`555 BELVEDERE DR` reads GREY**,
captured 2026-08-26, run `20260826-023936`, real lat/lng — Ed's address, and the
customer's own text said the same thing. **Three independent sources now agree
and the dial list was the odd one out.**

**The 21 greys, all of which were in the dial pool:** 555 & 1495 Belvedere ·
1135, 1060, 1020, 1185, 1085, 1080 Norwood · 7550 Chelsea · 1055 Wisteria ·
850 & 1095 Iris · 5765 & 5795 Longwood · 565, 415, 575 Potter · 355 Littlejohn ·
350 Georgetown · 380 Langham · 1090 Lockwood. **Sent to Dave and Churchie to
scrub.**

**DO NOT extrapolate 25% grey to the whole tab** — that is Check 2. The real
proportion needs `py sheet_feed.py --tab "Enriched Leads"` on the PC.

**Everything else this morning:** hunter still down (heartbeat frozen at
2026-09-02 19:48, `written 0` / `failed_writes 6012`, HTTP 301 to login) ·
won 2 / lost 0, no new close · **zero new opt-outs overnight** after 11 in one
day · 4 replies waiting on a call ((228) 627-3246, Glovera, Razzle Dazzle,
Wilton Cooper) · DealMachine 27,084 unchanged overnight · **the $30 promo is
STILL sending, day 2** · no live cable outage in any of our markets ·
production `fileSize` 8,484,584 flat with `modifiedTime` moving, which is NOT an
alarm (fileSize does not track content on a Google Sheet).

**Morning edition sent 12:2xZ as three emails.** The DAILY LOG is still empty —
last dated entry 08-27, GOALS block still blank.

*(Archived: the hunter-all-day instruction to the local session.)*

### `main` HAS NO BRAIN ON IT — THE BRANCH IS LOAD-BEARING (MEASURED 2026-09-04 07:20Z)

The local session opened on this repo showing **`optimus-map-tools main`** and a
**+12,402 / -50** diff with a *Create PR* button. Measured against origin:

- **`origin/main` is 249 commits behind `claude/new-session-8z4pyb`.**
- **`origin/main` contains NO `CLAUDE.md` at all** (0 lines). Its head is
  `696f998 themapman v11.2.5 clean`, unrelated to Optimus.
- The whole brain — 2,154 lines — exists only on **`claude/new-session-8z4pyb`**.

**So a clone that lands on the default branch gets NO BRAIN, and a commit there
forks the memory in two.** That is the failure this entire setup exists to
prevent, and it nearly happened in the first ten minutes of the local session.

**RULE: every session, local or remote, works on `claude/new-session-8z4pyb`.**
First thing a fresh clone must run:
`git fetch origin claude/new-session-8z4pyb && git checkout claude/new-session-8z4pyb`
then confirm by printing the last 5 commit messages before touching anything.

**GOOD NEWS FROM THE SAME RUN, worth keeping:** the local session independently
confirmed **the local scraper copy is stale but self-updates from the hunter repo
on launch** — so double-clicking the Maps Scraper pulls the deployed follow-up
board down with it. That is the mechanism this file has been asserting; it is now
confirmed from the PC itself rather than from the repo.

*(Archived: what a local Claude in `maps_scraper` can do. The one rule that stays: NEVER push to `Go-High-Level-MCP-2026-Complete` without showing the diff first — a push there is a DEPLOY TO EVERY PC.)*

### The gold question — answer it with the caveat, never the raw number

- **`Gold Confirmed` = 4,707 rows (MEASURED off tabs.json STAMPED 2026-09-02 23:39 laptop time). It was 1,884 at the 16:36 purge; +2,823 of the 6,012 parked gold rows landed once 21 tabs vanished and freed cells. All post-08-24. Unique addresses still unmeasured — `py gold_audit.py`.** (older text follows) The old "11,490 / 2,438 believed real" was a stale tabs.json number —
  MEASURED 2026-08-27 via `optimus/_feed/sheet/tabs.json` and **RE-CONFIRMED
  UNCHANGED 2026-09-03**: the last run ended `LOGIN_TIMEOUT` with all counters at
  zero, and `fileSize` has been byte-identical since 08-30, so nothing has been
  added. The other 9,052 are pre-08-24 gold-by-default decode failures; the purge
  may not have run. **~208 confirmed gold from the 08-30 run were captured and
  never written.** Other gold tabs: `Gold Dots` 3,328 (RETIRED), `GOLD — CLEAN`
  3,328, `Beaumont Gold — Aug 2026` 238, `Upgrade Orange Biz` 62.
- **The feed is fetchable with plain `curl`, no Google auth** —
  `raw.githubusercontent.com/patricksiado-prog/Go-High-Level-MCP-2026-Complete/claude/optimus-map-tools-setup-6dcl6o/optimus/_feed/{latest,sheet/tabs}.json`.
  `main` and `master` both 404 — the branch name is load-bearing.
- **UNIQUE gold addresses IS MEASURABLE — run `py gold_audit.py` on the hunter PC.**
  It prints total rows, UNIQUE ADDRESSES, duplicates, lat/lng coverage and the
  capture date range off `Gold Confirmed`, read-only, using the fiberscanner
  service account. One-line paste, nothing to save:
  `py -c "import urllib.request as u;exec(u.urlopen('https://raw.githubusercontent.com/patricksiado-prog/Go-High-Level-MCP-2026-Complete/claude/optimus-map-tools-setup-6dcl6o/optimus/gold_audit.py').read())"`
  **Never again say the unique count cannot be taken.** It cannot be taken from a
  Claude session; the software takes it in seconds.
- **`py sheet_feed.py --tab "Gold Confirmed"`** publishes the whole tab to GitHub
  in 500-row chunks (`optimus/_feed/sheet/chunk_NNN.json`) which Claude reads with
  plain curl, no Google auth. That is how any tab too big for the Drive connector
  gets analysed.
- **`py clean_sheet.py`** (dry run) then **`--yes`** IS the sheet clean: migrates
  `TEST-Gold-*` into `Gold Confirmed`, dedupes `Gold Confirmed` and `Precise Fiber`
  by address, deletes every non-KEEP tab with a CSV backup first. It has existed
  since 2026-08-24.
- **`build_codes.json` is the ground truth on gold:** copper/GOLD = `fttn-bp`,
  `fttn`, `ip-rt`, `iprt`, `copper`, `ipbb`, `adsl`, `vdsl`, `dsl`; fiber/GREY =
  `fttp-gpon`, `fttp`, `gpon`, `ftth`; no subscriber BAN = GREEN regardless.
- **The 492 gold in GHL are only what was IMPORTED.** The sheet holds more.
- **(superseded) UNIQUE gold from a Claude session** — still not possible here:
  `Gold Confirmed` is too big to read wholesale and the workbook is at its cell
  ceiling, so no temp COUNTIF tab can be added. Never present a row count as a
  dot count.
- **Rows are not dots.** 170 `VERIFIED_GOLD` rows in a sample were **4 unique
  addresses**. Treat any row count as an upper bound on unique gold.
- **296 gold contacts in GHL** (MEASURED 2026-09-01, unique) — the only gold
  number that is both current and de-duplicated.
- **`Upgrade Orange Biz` = 62 rows.** Gold businesses are the highest-value slice
  we have and that tab is empty, while 39,294 scraped businesses sit unmatched.
- Full census in the BRAIN.md section dated 2026-09-02.
- **THE ANALYSIS SHEET EXISTS:** `OPTIMUS ANALYSIS — sheet + CRM (live state)`,
  `1lnMzr4cceYjMfvLGeUtNvRRwjURwIGYZ9Kx9y4ONbX0` (rebuilt twice 2026-09-03; the last rebuild records the clean COMPLETED and gold = 1,884; earlier copies trashed), in the enriched Drive folder
  shared with Christian. Every row carries the number, how it was measured and
  when. Update it rather than re-deriving the same figures in chat.

### ALPHA — the one big dial pool (BUILT 2026-09-03)

- **Tag `alpha` is the pool: 3,379 UNIQUE PEOPLE** (was 3,581 before 202
  duplicate second-copies were stripped 2026-09-03). Point the dialer at that tag.
  Tiers, best first: `alpha-t1-warm` 33 · `alpha-t2-gold` 492 ·
  `alpha-t3-green-pocket` 307 · `alpha-t4-business` 238 · `alpha-t5-green` **2,309**
  (MEASURED 2026-09-03 by paging the whole tag; the old 2,511 was wrong).
  Angleton + La Porte + Beaumont + Devonwood + the whole dialer queue + Pool A +
  the att.net gold, merged and deduped. 90 dropped (73 NI, 16 unsellable, 1 no
  phone); 220 more came back `contact is deleted` — stale ids, not a bug.
- **Three workflows, all PUBLISHED:** `ALPHA - Power Dialer`
  (`ea28081b-399e-4a28-b0ef-8fa06fbd9f13`, the `manual-call` queue),
  `ALPHA - Not Interested REMOVES from dialer` (`80525fcc-fd11-4a23-a4e5-9dd231e38456`),
  `ALPHA - Call Back re-enters the dial pool` (`f9875f7d-3b01-45af-a04f-43fe2de2c72c`,
  routes around the `2. Designated Agent` first-branch bug).
- **NI now really exits.** All 73 contacts tagged `not interested` had `leads` and
  their `agt*` tags stripped 2026-09-03, 73/73. `D03` still does not remove
  anything — the new workflow does it instead. Do not "fix" D03 without asking.
- **THE GHL MCP CANNOT SET WORKFLOW TRIGGERS** (accepted, silently discarded — every
  workflow reads `triggers: []`) **and cannot build multi-action workflows**
  (auto-chain writes `next` as an array; GHL's validator refuses it). Single-action
  workflows publish fine. **So the three ALPHA workflows need Patrick to add one
  trigger each in the UI before anything enrols.** Detail in BRAIN 2026-09-03.
- **THE 492 REAL GOLD ARE SPLIT 246/246 ACROSS AGENT 3 AND AGENT 5** (2026-09-03),
  the only two who actually dial. Every agent tag was stripped from all 492 first,
  so nothing carries two and the first-branch-wins router cannot misfire.
  Enrichment needed almost nothing: only 6 lacked an address, 5 of those are
  businesses DealMachine will not trace, and the one residential lookup cost
  **2 credits** (29,968 left). Zero of the 492 are DND; 23 are CALL-ONLY landlines.
- **THE agt4+agt6 DOUBLE TAG IS FIXED.** All 296 gold carried both, and the
  first-branch-wins router sent every one to Agent 4 who has no rep. `agt4`
  stripped from all 296 on 2026-09-03, verified per record. Do not re-add it.
- **AUTOSHEET IS ONE TOP-UP FROM CLEANING THE SHEET** — tested 2026-09-03, it
  returns `api-billing-empty-balance`. With credits it can drop the `TEST-*` tabs
  and purge the pre-08-24 gold. Exporting the workbook to xlsx instead is
  impossible: `File too large for export`.
- **Bulk tagging works only through `official_contacts_create_association`** —
  really `POST /contacts/bulk/tags/update/{type}`, body key `contacts`, max 500.
  `bulk_update_contact_tags` is a 404.

*(Archived 2026-09-04: POOL A, superseded by ALPHA above.)*

*(Archived: `Random Fiber SMS After Calls` `5a7f16a7-fa67-4753-9ecc-e8f58a50c715` — v10, one clean single-segment action, still `draft`.)*

### The dial queue

- **GOLD IS NOW IN FRONT OF THE AGENTS WHO ACTUALLY DIAL.** MEASURED + FIXED
  2026-09-01 4:15pm CT: all **296** copper-upgrade leads were parked in
  **Agent 4's** queue — 100% gold, 100% of that queue, and only **3% ever
  dialed** — because every one carries BOTH `agt4` and `agt6` and the
  `2. Designated Agent` if_else takes the first matching branch. Agents 3 and 5
  are the ones working (23% dialed each) and held pure green. All 296 enrolled
  into Agent 3 (148) and Agent 5 (148), 296/296 succeeded. Full detail in the
  section dated today.
- **Not yet fixed:** the double `agt4`+`agt6` tag is still on all 296, so
  anything re-routed through `2. Designated Agent` gets re-parked with Agent 4.
  Agent 4 still has no live rep. And the queue applies NO exclusion — contacts
  dispositioned `not interested` and rows tagged `excluded-unsellable` are
  still being dialed.

*(Archived: the 09-03 enrichment ledger. Live: DealMachine 27,084, cycle Sep 2 - Oct 2.)*

### What is live and sending right now

| Thing | ID | State |
|---|---|---|
| SMS routine — **Beaumont gold pocket first**, 200/day, 11am + 4pm CT | `trig_018JYeQpvcgfrmBxc46Vv967` | **ENABLED BUT SENDING NOTHING.** MEASURED 2026-08-31: fired 11:10am CT, `SUCCEEDED` in **95 seconds** — too short to send 100 texts, and no new-copy send exists anywhere in GHL today. Second time (29 Aug: 38 min, zero sends). **`SUCCEEDED` on this routine does NOT mean texts went out** |
| **UNKNOWN GHL workflow texting the OLD template from `+13465178890`** | GHL workflow | **LIVE and collecting instant STOPs.** MEASURED 2026-08-31 — see the section dated today. NOT the no-answer workflow. Needs Patrick's call |
| AM coverage-gap email | `trig_01JTQKnB2U5ihS1mC4rpX2qy` | live, 12:00 UTC |
| PM coverage-gap email | `trig_01RjAUBz16UNpdDzK2neCz37` | live, 22:30 UTC |
| GHL no-answer auto-text, from `+13468106925` | GHL workflow | **LIVE — DO NOT TOUCH.** Patrick: *"don't break that template that is working"* |

Both email routines are **session-bound and therefore mortal** — they die with
the session that made them. That is the answer to "why did my email stop".

**GMAIL IS CONNECTED AGAIN — MEASURED 2026-09-03 22:50Z: the evening edition
sent as three emails and returned message ids.** (CORRECTED: an earlier claim
that it went out at 17:40 CT was written before the send and was false — see the
evening-edition block at the top.) (Superseded:
as of the morning of 2026-09-03 it was disconnected and the AM routine delivered
nothing.) The AM routine fired on schedule and could not deliver a single
one of the three emails, because the Gmail MCP server is unauthenticated and a
scheduled session cannot run OAuth. **Patrick must re-authorise Gmail in his
claude.ai connector settings.** Until then a routine "firing" is no evidence
anybody received anything — same trap as the SMS routine reporting `SUCCEEDED`
while sending zero texts.

### Blocked on Patrick — nothing moves until he does these

0. **(DONE — DELETE THIS ASK.) The gold purge RAN and COMPLETED** on Patrick's
   PC: console printed *"nothing to remove -- all 1884 rows are post-fix"*.
   `Gold Confirmed` is 4,707 rows, all post-08-24. **The scraper launch that is
   still wanted is for a different reason** — it repopulates `Upgrade Orange Biz`
   with the 09-03 gold-match fix (62 rows against 39,294 businesses today).
1. **SPLIT SHEET — DEPLOYED, hunter `59a92bf` (2026-09-03).** Patrick: *"u know
   what I want make it happen."* `Precise Fiber` now defaults to its own workbook
   `1DXu-nuQvVKrqQVk8LDNwLztG31ddi6sAyo8vXDFKcmQ` on every PC (no id file needed;
   a file still wins if present). The scraper carries the identical id so the
   biz match follows. The 8-vs-13 column bug is fixed. **Takes effect at the next
   HUNTER launch — which needs the AT&T re-login first.** On that launch expect
   `PRECISE FIBER -> separate workbook 'ATT FIBER LEADS — Precise Fiber'` in the
   console; if instead it prints `CANNOT OPEN THE PRECISE FIBER WORKBOOK`, the
   share was lost. Old `Precise Fiber` (645k rows) stays in production as
   history; new green lands in the split. brain-verify now tests all four claims.
1b. **`CHRISTIAN_DIALER_775.csv` IMPORT IS DONE** — MEASURED 2026-08-30 13:39
   CDT: **684 contacts tagged `beaumont-gold-pocket`** in T-OPTIMUS Houston,
   `medium: csv_import`, newest 13:29 CDT, being split across agents (`agt4`,
   `agt5`). The dialer queue was 199 yesterday. Still open: import
   `ENRICHED_TAB.csv` as a workbook tab, and `OPTIMUS_DIALER_2000_labeled.csv`
   (2,000 rows) remains the bigger pool behind the 775.
3. **(EXPIRED — DELETE THIS ASK.) That cycle ended 2026-09-02.** The credits
   reset. Live number MEASURED 2026-09-03 22:45Z: **27,084 left**, cycle
   Sep 2 → Oct 2, 2,916 used. Nothing is about to expire.
4. **A phone number for the flyer** — both sheets say `[YOUR PHONE]`.
5. **Call Antonio, 713-474-3899** — said *"come replace"* his copper, still not
   called back.
6. **Janell Dumas** — AutoPay/Paperless was declined at the order, and the
   Spectrum port-out PIN is still needed.
7. **Frontline Direct GHL token** (`TXw28sw0Z2rI6tcCDhJY`) returns **403**.
   Zack's Houston book is invisible from here; an empty lookup against
   T-OPTIMUS is NOT evidence a customer does not exist.

### Known broken, measured, not yet fixed

- **1,376 contacts tagged `invalid` are not invalid.** 100/100 sampled are
  dialable; 45 are Twilio 30006 (landline — call it, don't text it), 55 have no
  recorded error at all. Biggest recoverable pool in the CRM.
- **974 of 2,000 leads carried a dot colour their source could not know**
  (DealMachine has no serviceability data). Now marked `status-unverified` in
  `OPTIMUS_DIALER_2000_labeled.csv`. ~360 of them are probably GREY.
- **85% of the live dial queue has no dot colour at all** (sample of 100/199).
- **The pipeline is nearly write-only** — 3,835 open, 1 won, 0 lost.
- **Business cross-match — the `ValueError` fix IS deployed** (grepped the live
  file 2026-09-03, line 672 has the slice; the "NOT deployed" line above was
  stale). **The REAL reason `Upgrade Orange Biz` froze at 62:** `init_match`
  read dot colours from `Precise Fiber` only, which has been GREEN ONLY since
  08-26, so the ORANGE side scanned a tab with zero orange rows. **Fixed
  2026-09-03: gold is now loaded from `Gold Confirmed` and overrides green.**
  Fifth casualty of the green-only change. Look for `(N gold from 'Gold
  Confirmed')` in the COMBO MATCH line to confirm it loaded.
- **Wireless attach rate is 4%** on 449 internet customers. ~$385 of stackable
  attach sits on every already-closed sale.

### CLOSED — do not re-propose, do not re-ask

| Thing | Why it is closed |
|---|---|
| **Lumen states (AZ CO IA ID MN MT NE NM OR UT WA)** | Not our territory. Patrick: *"ignore Lumen deal that doesn't matter."* |
| **Google's 20M-cell beta** | Allowlisted per DOMAIN by a Workspace admin. Workbook is on a personal Gmail account — nothing to allowlist |
| **Using `thefiberplug.com` as the Workspace domain** | Patrick, 2026-08-30: *"no cuz I owe them $$."* Do not ask again |
| **Sub-sheets joined by IMPORTRANGE** | Crawls past ~50 formulas, needs a manual Allow-access click per file, would need 37 of them |
| **Airtable** | Per-editor pricing compounds once VAs are in seats |
| **Recycle leads forever** | Patrick settled it: *"6 attempts ok that's enough"* |
| **Claude posting to FACEBOOK MARKETPLACE** | MEASURED 2026-09-03: Meta publishes **no API for Marketplace listings** — it is a manual, in-app surface only, and automating it breaks their terms and risks the account. Claude writes the listing, Patrick pastes it. Do not re-offer to post it |
| **Posting to a Facebook PAGE through GHL instead** | `get_social_accounts` returns **0 accounts, 0 groups** (MEASURED 2026-09-03). GHL social posting exists but nothing is connected, so there is no page to post to until Patrick links one in GHL → Settings → Social Planner |
| **A DealMachine→GHL connector** | No first-party integration exists; we already call both APIs directly, which is better |
| **A2P as the cause of the 405** | It was a fake SMS provider. Fixed by switching to LeadConnector |
| **`scrub_dnc` on a DealMachine export** | Registry DNC is recorded and dialed anyway; scrubbing deletes >half the list |
| **Naming the dealership in a customer text** | *"don't say optimus / we're att"* |

### THE GOLD LABEL FAILED THE SAME WAY THE GREEN ONE DID (MEASURED 2026-09-04)

Patrick: *"are u sure it's right?? u know the sheet was fucked up. check and
rename it."* He was right to push, twice over.

**CORRECTION TO MY OWN COLUMN, SHIPPED AN HOUR EARLIER.** The `COLOUR PROOF`
column I put on every file read *"VERIFIED <colour> - traced to a hunter
capture"* on 241 rows. **That was WRONG.** All it actually meant was that
GoHighLevel had a `source` string on the contact — provenance of the IMPORT, not
verification of the DOT. I conflated the two and shipped it. Corrected the same
turn; the files now carry `HOW SOLID IS THIS` with a truthful sentence per row.

**WHERE THE "GOLD" ON 513 ROWS ACTUALLY COMES FROM:**

| n | source |
|---|---|
| **263** | a spreadsheet somebody uploaded — NO source recorded |
| **195** | an **att.net / sbcglobal email** on the contact = they ARE an AT&T customer |
| 32 | export named "Beaumont gold pocket - verified copper upgrade" |
| 22 | export named "Optimus gold biz" |
| 1 | "Optimus Precise Fiber - Beaumont" |

**AND THE BOARD AGREES WITH ED AGAIN.** Of the gold-labelled rows the follow-up
board could check against the hunter's own tabs: **2 came back GREY (7550 Chelsea
Pl, 1055 Wisteria Dr — both were tagged `t2-gold`), 14 came back "not on the map",
and ZERO came back confirmed gold.** Gold is no safer than green was.

**THE FILES ARE NOW NAMED FOR WHAT THEY ARE.** 507 rows, 16 chunks of ~50, the
2 confirmed-grey golds stripped:

- **`A-ATT-CUSTOMER_*` — 192.** att.net/sbcglobal email on file. This is the ONLY
  independently verifiable gold signal we own: the email proves they are an AT&T
  customer. It does NOT prove copper vs fiber. **Hand these out first.**
- **`B-COPPER-EXPORT_*` — 52.** Came from an export whose NAME claims verified
  copper. Never re-checked against the map.
- **`C-UNVERIFIED_*` — 263.** The word "gold" was typed into a spreadsheet.

**THE NAMING IS THE CONTROL.** A rep reading `C-UNVERIFIED` cannot mistake it for
proof. Never ship a file called `GOLD_*` again unless the map says gold.

## WE CALL DND. (Patrick, 2026-09-04: *"we call dnd / put that in the brain"*)

**This overrides the older line in this file that said GHL DND is "absolute,
forever." That was too broad and it was costing us leads.** A DND in
GoHighLevel is almost always an **SMS opt-out**, and an SMS opt-out is not a
call opt-out.

**MEASURED THE SAME TURN, and it is why he is right.** All 8 DND rows in the
Milton pool read `dndSettings: {"SMS": {"message": "STOP_KEYWORD", "status":
"permanent"}, "RCS": ...}` and **`dnd: false` on the master flag.** They replied
STOP to a text. Nothing about that record blocks a phone call, and GHL itself
does not treat them as globally suppressed.

**THE RULE, three lines, and they do not collapse into each other:**

| Signal | Text? | Call? |
|---|---|---|
| **Registry DNC** (`dnc-flagged`, DealMachine DNC=yes) | YES | **YES** — a third party's list, standing rule since 08-29 |
| **GHL DND / STOP_KEYWORD on SMS** | **NEVER** | **YES — WE CALL DND** |
| **They told a human "stop calling me"** — disposition `Do Not Call`, or `not interested` | NEVER | **NO. Absolute, forever** |

**NEVER TEXTING A STOP IS NOT A POLICY CHOICE — the carrier and GHL enforce it
at the channel.** A send to a STOP'd number fails or, worse, ships and gets the
sending number flagged. So a DND row goes in a CALL list and never in a send
list, and every list must say which it is.

**WHAT CHANGED IN PRACTICE:** stop stripping `dnd` from call files. Keep
stripping `not interested` and `Do Not Call` — those are a person saying no to
us, which is a different thing and still ends the lead. The `Do Not Call`
disposition must still set DND automatically; that has legal weight and stays.

**Milton was rebuilt the same turn: 126 → 134 callable, the 8 STOP'd rows back
in, each carrying `DND - SMS STOP, CALL ONLY - NEVER TEXT`.**

## RULE 0b — NEVER SHIP AN UNVERIFIED COLOUR. NEVER PUT GREY IN A CALL LIST.

**Patrick, 2026-09-04: *"Never send me garbage again... I can't call gray."***
This sits next to RULE 0 because it is the same class of failure: something goes
out the door that should not have.

**A colour is a CLAIM until the hunter's own tabs say otherwise.** A `type-green`
tag in GoHighLevel is a value somebody typed into a spreadsheet column. It is not
a dot. On 2026-09-04 the follow-up board checked 84 of them against the map:
**21 came back GREY — existing AT&T customers who can never buy fiber — 55 came
back "not on the map at all", and the only 8 confirmed greens were businesses.
Zero residential greens were confirmed.** Ed said this first, then a customer
texted it, then the software wrote it down.

**THE RULE, and it applies to every list, file, email, tag and dialer load:**

1. **GREY NEVER SHIPS.** An address the hunter has marked `Grey Fiber Customers`
   / "Existing AT&T Customer" is not a lead and never goes in a call list, a text
   list, a dialer tag or a door-knock route. Strip it, and say how many you
   stripped.
2. **EVERY ROW CARRIES ITS PROOF.** Every list gets a column that says, per row,
   either `VERIFIED <colour> - <run id> <date>` or
   `UNVERIFIED - ASK WHO THEY HAVE TODAY`. No blank, no implication, no colour
   word standing on its own.
3. **THE COVER MESSAGE STATES THE SPLIT** — how many verified, how many not, out
   of how many. If it is "241 of 4,278", say 241 of 4,278.
4. **NEVER PRESENT A ROW COUNT AS A DOT COUNT** (`Gold Confirmed` = 4,707 rows
   was 10 unique addresses in the readable sample) and never infer a colour from
   a ZIP, a city name, a tab position or a neighbour's dot.
5. **WHEN IN DOUBT THE ROW IS UNVERIFIED.** Downgrading a lead costs a question
   on the call. Upgrading one costs Dave four minutes and the customer's trust.

**THE VERIFICATION IS ONE COMMAND AND IT IS NOT OPTIONAL BEFORE A BIG LIST:**
`py sheet_feed.py --tab "Grey Fiber Customers"` (then `Precise Fiber`, then
`Gold Confirmed`) on the hunter PC publishes each tab in chunks Claude reads with
plain curl. **Until those chunks exist, say plainly that the colour is unproven
rather than shipping it as fact.**

**THE OPENER THAT SURVIVES A WRONG COLOUR:** *"Who do you have for internet
today?"* Thirty seconds, and it turns a bad green into a known gold, grey or
prospect before anyone pitches. Put it at the top of every list that ships with
unverified rows.

## The three rules that outrank everything below

1. **RULE 0 — ASK BEFORE YOU PUSH.** Reading, diagnosing, writing and testing a
   fix are free. Pushing is the line. Patrick: *"don't ever break software!!"*
2. **NO NEW PROGRAMS.** Two exist — the Fiber Hunter and the Maps Scraper. New
   capability goes INSIDE one of them, running by itself. A `.bat` a human must
   remember to run is a failure, not a deliverable.
3. **NO COMMISSION NUMBERS anywhere Ara or a VA can see.** Check the recipient
   list before sending to more than one person.

---


## THE ADDRESS GOES IN THE NOTE. ALWAYS. (Patrick, 2026-09-03)

*"address / I want the address in the notes always"*.

**Every lead note opens with the full street address and closes with it again.**
Not the city. Not the ZIP. The street address, on the first line, before
anything else — because these leads ARE the address. The whole pitch is "fiber
is live at your address", and a rep who has to hunt for it will not say it.

**The shape, in this order:**

```
<FULL STREET ADDRESS>  |  POOL/PRIORITY  |  CUSTOMER TYPE  |  why this lead
|  what to watch (STOP / landline / DNC)  |  SAY THE ADDRESS OUT LOUD
|  <FULL STREET ADDRESS>
```

**A contact with no address in GHL is not an exception — it is a job.**
1. `dealmachine_enrich_phone` with `include_properties`. The **owner-occupied**
   property, or the one where `is_resident` is true, is the service address.
   ~1-3 credits. On 2026-09-03 this recovered **10 of 12** for **30 credits**.
2. If DealMachine returns `no_match`, or the record is **LLC-owned** (it will not
   skip-trace an LLC), write **`ADDRESS UNKNOWN - ASK FOR IT ON THE CALL AND
   WRITE IT HERE`** as the first line, and say what you checked and when.

**Never leave the address line silently blank, and never fill it with a city
name.** "laporte" sat in the address field of 13 dialer leads and reps were
being told to read a town out loud. If two addresses are plausible, name both
and tell the rep to CONFIRM ON THE CALL before pitching.

## THE FOUR CHECKS — every mistake that has cost money failed one of these

Patrick, 2026-09-02: *"develop the skill and the rule to not fuck up all the dam
time / costing me time and money and tockens."* These are the four. They are
short on purpose. Run them, do not admire them.

**1. SEARCH FIRST.** Before spending credits, sending texts, building a list,
quoting any number, or saying something is broken:
`.claude/skills/session-continuity/scripts/brain find <topic>`.
*Cost of skipping it: 4,783 DealMachine credits on 2026-09-02, on ground this
file had already mapped.*

**2. COUNT THE MARKER, NOT THE SHAPE.** Grep the thing that NAMES the value
(`VERIFIED_GOLD`, a Status string, a tag) and count **UNIQUE ADDRESSES, never
rows**. Never infer from a ZIP, a city name, a tab position or a row shape.
*Cost of skipping it: four separate wrong counts — gold-by-default (8/23),
colour-by-default (8/29), agent-by-first-match (9/01), city-name-as-colour
(9/02). Nothing errored any of those times. The count just looked fine.*

**3. CHECK THE DESTINATION, NOT THE RETURN VALUE.** `success: true` from
`send_sms` means GHL accepted the request, not that a text arrived — read
`status` on the message. `SUCCEEDED` on a routine does not mean it sent.
`classified: 126,628` means nothing if `written: 0`. A moving `modifiedTime`
with a flat `fileSize` means nothing is landing.
*Cost of skipping it: 88 texts reported sent that all failed, 2026-08-31.*

**4. LABEL IT MEASURED OR ASSUMED, WITH A DATE.** A measured claim carries the
number, the date and how it was taken so it can be re-taken. An assumed one says
so in the same sentence. Never let the two share a voice.
*Cost of skipping it: "register for the 20M-cell beta" was repeated confidently
across four sessions and was never available at all.*

**If one of these was skipped and it went wrong, say so plainly and name which
one.** That is cheaper than a defence, and it is the only way the list improves.

## HOW THIS MEMORY WORKS — read this before you go looking for anything

**This file is deliberately short now.** On 2026-09-02 it was 5,250 lines and
~69,400 tokens, loaded IN FULL at the start of every session. Anthropic's own
guidance is to keep a `CLAUDE.md` under 200 lines, because a long one costs
tokens on every turn and measurably reduces how well its instructions are
followed. 4,445 lines of dated session history were moved to **`BRAIN.md`**,
verbatim, nothing deleted. Cost per session went 69,400 → ~11,700 tokens.

**Nothing was lost, because retrieval is a tool now, not a scroll:**

```bash
B=.claude/skills/session-continuity/scripts/brain
$B find <topic>     # searches CLAUDE.md + BRAIN.md + the log, NEWEST FIRST
$B money            # read before spending a credit
$B closed           # decisions Patrick killed — never re-propose
$B state            # the CURRENT STATE block
$B corrections      # where the brain corrects itself; the correction wins
$B rules            # standing rules
$B stale [days]     # MEASURED claims going out of date
$B index            # every section, dated, newest first
$B/brain-verify      # TESTS the brain's code claims against the LIVE files -- runs at every session start
```

**`brain-verify` is the fix for code-claim rot (2026-09-03).** Every checkable
claim this file makes about where code lives or what it does has a line in that
script's manifest and is re-tested at session start against the live GitHub
files. A `*** DRIFT` line at launch means this file is wrong RIGHT NOW -- fix it
in the first turn. **A code claim with no manifest line is ASSUMED.** When you
deploy a change, add its claim in the same commit.

**Four actions REQUIRE a search first — this is the rule that exists because
breaking it cost 4,783 DealMachine credits on 2026-09-02:**

1. spending credits / enriching / exporting
2. sending texts or building a send list
3. quoting any count, colour or rate
4. saying something is broken or fixed

**An empty search result is a real answer** — it means the thing is genuinely
new, so measure it and write it down. If the tool says `TOOL FAILURE, NOT AN
ANSWER`, it could not read the files; that is not "nothing recorded".

**Where things go now.** Durable rules, IDs, legends and the CURRENT STATE block
live here. Dated findings and session history go to the BOTTOM of `BRAIN.md`.
When this file drifts back over ~800 lines, archive the oldest dated sections
into `BRAIN.md` again — that is routine maintenance, not a decision.

**Never `@import` BRAIN.md into this file.** Imported files load at launch too,
so it would restore the whole token cost and undo the point.

## Who and what

Patrick Siado runs **Optimus**, an authorized AT&T dealer. We sell fiber.

**TERRITORY IS THE ENTIRE AT&T FOOTPRINT** (Patrick, 2026-08-25, correcting the
old note): all **21 legacy ILEC states**, not just Texas.

**The Lumen states are NOT our territory.** AT&T closed the Lumen Mass Markets
fiber acquisition in Feb 2026, which put AT&T Fiber into 11 more states (AZ CO
IA ID MN MT NE NM OR UT WA — Denver, Seattle, Portland, Salt Lake City,
Minneapolis-St. Paul, Phoenix). Patrick, 2026-08-26: *"ignore Lumen deal that
doesn't matter."* `optimus_web_intel.py` keeps them in
`LUMEN_STATES_NOT_OUR_TERRITORY`, defined but never merged into `STATES`.
Recorded so no future session rediscovers the deal and "fixes" the footprint
by adding them back. Houston metro, Beaumont and
Brazoria County (Angleton, Clute) are where the FEET are — the boots-on-ground
core — but lead discovery is national. Do not scope a scan, a news query or a
freshness check to Texas on the assumption that out-of-state is noise.

AT&T is retiring copper — **Phase 1 by 2027** (wireless-first areas), **Phase 2
by 2029** (fiber-migration areas). That deadline is the opener on every pitch:
it is true, it is urgent, and it reads as a heads-up rather than a sales call.

**Team:** Dave (dials), Ed, Zack, Ara, Daniel, **Valmore** (new, 2026-08-28).
Patrick closes
and builds.

## The dot legend — everything downstream depends on this

One colour, one tab, one meaning (Patrick, 2026-08-26). Every row on these
tabs carries the wording below in a **Status** column, so a single exported row
still explains itself and nobody has to remember a colour code.

| Dot | Tab it lands on | Status wording on the row | Worth |
|---|---|---|---|
| **GREEN** | `Precise Fiber` | `Non-AT&T Customer - Can Get Fiber` | **$500** — the prize |
| **GOLD / ORANGE** | `Gold Confirmed` | `Upgrade Customer - On Copper, Fiber Available` | **$140** — easiest sale, an upgrade not a switch |
| **GREY** | `Grey Fiber Customers` | `Existing AT&T Customer` | Not a fiber lead — but it IS written: penetration data, and the best wireless/bundle list we have |
| **UNKNOWN** | `Unknown Customers` | `Build Code Not Decoded - Not A Lead` | Parked for review, never called |

**THE PURGE LIVES IN THE MAPS SCRAPER, NOT THE HUNTER — MEASURED 2026-09-03,
and this corrects what this file said for six days.** Commit `754ecbf`
(2026-08-27) modified **exactly one file**:
`optimus/standalone/maps_scraper_standalone.py`, +98/-0. `purge_prefix_gold()`
is at lines 1174-1266, called at line 1836 on scraper launch.
**`precise_fiber_hunter.py` contains ZERO occurrences of "purge". So does
`clean_sheet.py`.** Therefore:
- "it runs at HUNTER launch" — **WRONG, delete that idea.**
- "fixing the AT&T login runs the purge for free" — **WRONG.** The AT&T login
  has nothing to do with it. That line sent Patrick after the wrong fix.
- "CLEAN_SHEET.bat cleans the gold contamination" — **WRONG.** It dedupes by
  address; it does not date-cut. The clean and the purge are different jobs.

**THE ONE ACTION THAT RUNS IT: double-click the Maps Scraper Desktop icon.**
The purge runs in the first ~30 seconds of launch, before any scraping, backing
the whole tab up to a local CSV and the removed rows to their own JSON first.

**AND IT IS PROBABLY STILL GATED SHUT.** The purge sits behind
`if sheet_ws is not None`, and `sheet_ws` comes from `open_sheet()`, which opens
**`Maps Businesses`** and, if that tab is missing, calls `add_worksheet(20000x7)`
= **140,000 cells** — which throws a 400 on a workbook at the 10M ceiling, gets
swallowed by a bare `except`, and returns `None`. **The sheet is too full to
open, so the cleanup that would free ~118,000 cells never runs.** Two more
gates: any failure prints only `"(dedupe off: ...)"`, and the marker file
`gold_purge_done.flag` is written even on an "empty tab" read, which locks the
purge off that PC forever. Fix written, tested by reading, **NOT pushed**:
`patches/gold-purge-never-runs.md`. Ask Patrick before pushing — RULE 0.

It still cannot be done from a Claude session: the Drive connector is file-level
only (no row or tab edits), Autosheet's balance is empty, and the cell ceiling
blocks even a temp COUNTIF tab. Do not promise to clean the sheet from here —
point at the Maps Scraper instead.

**THE MISCLASSIFICATION WINDOW IS EVERYTHING BEFORE 2026-08-24** — the old
`OPTIMUS_UNKNOWN_CUSTOMER=gold` setting labelled any undecodable build code GOLD
by default. That is **9,052 rows when the tab read 11,490. THE PURGE HAS SINCE RUN — the tab is 4,707 rows, all post-08-24 (MEASURED 2026-09-04).**

**GOLD WAS CONTAMINATED AND IS BEING PURGED (2026-08-27).** `Gold Confirmed`
read 9,658 rows and Patrick called it immediately: most predate working gold
capture. Gold-by-default — gold = "could not decode the build code" — died
2026-08-23 (BRAIN 22.17); confirmed-copper capture was verified 2026-08-24.
Scraper commit `754ecbf` now purges `Gold Confirmed` rows captured before
**2026-08-24**, once per PC at launch: whole tab backed up to a local CSV plus
a JSON of the removed rows first, abort-untouched if the `Captured At` header
is missing. **Never quote a gold count without checking the purge has run** —
pre-purge counts are mostly decode failures wearing a gold label.

**FULL ADDRESS EVERYWHERE (2026-08-27).** Rows captured before the 13-column
format carry a street line and nothing else, so they cannot be mailed or
skip-traced. The scraper now repairs a bounded 400-row batch each launch from
each row's coordinates using the US Census Bureau's free keyless geocoder,
writing City/State/ZIP plus a **`Backfilled At`** stamp in its own column.
`Captured At` is NEVER overwritten — that is when the dot was seen. A row with
no coordinates is left exactly as it is; a city is never guessed from a street
name. A coordinate is retired as `NO MATCH` only once a sibling row in the same
run proves the geocoder was answering, so an outage cannot write off real
addresses. The tab heals itself over a few days with nobody running anything.

**`Precise Fiber` is GREEN ONLY as of 2026-08-26.** It used to take every
colour, which buried the call list under grey customers nobody can sell. Do not
write a non-green dot to it and do not assume a colour filter on it means
anything — every row is green now.

The wording lives in ONE place: `STATUS_GREEN` / `STATUS_GOLD` / `STATUS_GREY` /
`STATUS_UNKNOWN` at the top of `precise_fiber_hunter.py`. `clean_sheet.py`
imports them for the README, the DASHBOARD and the dot legend, so the sheet and
this file cannot drift apart. Change the words there, not in three places.

Green is ~48x the volume and 3.6x the pay, so green is the money. Gold is the
**compass**: a dense pocket of copper customers means fiber was lit recently and
nobody has converted it, so nobody has worked it. Inside a pocket, work gold
first — it closes faster and warms the street.

## System IDs

| Thing | ID |
|---|---|
| Master sheet `ATT FIBER LEADS` | `1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA` |
| GHL location — T-OPTIMUS Houston | `xZj500PjsflIQg2j9f9D` |
| GHL location — Frontline Direct | `TXw28sw0Z2rI6tcCDhJY` |
| Pipeline — AT&T Leads (residential) | `2V9thfxQpuhn6ZP0Peqt` |
| Pipeline — AT&T Commercial | `trc5dwodtc1LBYHikmiK` |
| Calendar — Optimus Fiber Appointments | `jSOOC383RNxHIRwo6zV8` |
| Hunter repo (self-updates from here) | `patricksiado-prog/Go-High-Level-MCP-2026-Complete`, branch `claude/optimus-map-tools-setup-6dcl6o` |
| AT&T dealer map endpoint | `/yourefer/api/fiberMap.cfc` (returns text/html despite being JSON) |

**Two-repo trap:** the hunter self-updates from `Go-High-Level-MCP-2026-Complete`,
not from this repo. Hunter code pushed here reaches nobody. Worse, any file in
`_CORE_FILES` in `precise_fiber_hunter.py` **auto-deploys to every hunter PC** on
next launch, so a push there is a deploy, not a commit.

## READING THE SHEET — LOAD THE `optimus-sheet` SKILL FIRST, EVERY TIME

**Patrick, 2026-09-03: *"every fuking time I ask for data from the sheet u read it
wrong upload or enrich wrong data."* He is right.** So the tab map, the five read
paths in order, the four tools that already exist on his PC, the build-code
ground truth and the full list of every way this workbook has been misread now
live in **`.claude/skills/optimus-sheet/SKILL.md`**. Load it before answering ANY
sheet question, quoting ANY count, enriching or uploading anything sourced from
it, or saying any part of it is out of reach.

**The two double-click tools, because "I can't" is almost never true:**
- **`CLEAN_SHEET.bat`** — THE CLEAN, **BUT DO NOT RUN IT UNTIL THE PATCH IS IN.**
  MEASURED 2026-09-03 against the 29 live tabs: it deletes 14 tabs / 22,457 rows,
  and **7 are hand-built working tabs, not junk** — including
  **`Warm Backlog — Replied YES` (40 people who already said yes)**, the Angleton
  call list, the Beaumont work list, `Beaumont Gold — Aug 2026`, `GOLD — CLEAN`
  (3,328) and `HOUSTON UNVERIFIED — Aug 19`. Each is CSV-backed-up first, so
  nothing is destroyed forever, but the tab leaves the workbook. Cause: it is a
  **whitelist**, so it deletes every tab nobody thought to list — backwards for a
  sheet reps work in. Fix written, NOT pushed:
  `patches/clean-sheet-one-doubleclick.md` inverts it to a named JUNK list AND
  moves the gold date-purge into it, so one double-click does tabs and rows.
- **`COUNT_TABS.bat` — RETIRED 2026-09-03.** The Maps Scraper now publishes every
  tab's row count to `_feed/sheet/tabs.json` at every launch, WITH a
  `generated_at` stamp (hunter `fcc6b6e`). Patrick: *"I don't like extra
  program, connect it to the launch of something."* An UNSTAMPED tabs.json means
  the scraper has not launched since the deploy; never quote it as live.

## READING THE SHEET — the five paths live in the `optimus-sheet` skill

**NEVER say the sheet is out of reach.** Patrick, 2026-08-25: *"I don't want you
or any other Claude to say I can't read the sheet."* Load the skill, then say
WHICH of the five paths you tried:

1. `read_file_content` on the workbook — a BOUNDED SAMPLE of the first tabs,
   saved to a local file the harness names. Parse it with python, free.
2. `get_file_metadata` — but **`fileSize` is NOT a liveness signal** on a Google
   Sheet; it sat at 8,484,584 while ~75,000 rows landed.
3. **`_feed/sheet/tabs.json`** on the hunter repo — exact row counts per tab,
   plain curl, no Google auth. Only trust it with a `generated_at` stamp.
4. **`py sheet_feed.py --tab "<name>"`** on the hunter PC — publishes any tab in
   500-row chunks Claude reads with curl. **This is the answer for every tab too
   big for the Drive connector, and it has still never been run.**
5. Autosheet — the only path that can WRITE. `api-billing-empty-balance`.

**ONE TOOL FAILING SAYS NOTHING ABOUT THE OTHERS.** Autosheet's billing error is
not evidence the sheet is unreachable — that mistake was made 2026-08-25 and
again 2026-09-03.

**The `BRIDGE — *` sheets return BLANK until Patrick clicks "Allow access" once
per file.** Not a permissions failure on your end, not worth debugging.


## Sheet tabs — EIGHT OF THEM (MEASURED 2026-09-04 off tabs.json stamped 03:08:57)

| Tab | Rows |
|---|---|
| `Precise Fiber` — **GREEN ONLY since 08-26**; new green goes to the split workbook | 687,923 |
| `Grey Fiber Customers` — never dial, this is the SCRUB list | 56,799 |
| `Maps Businesses` — scraped, unmatched to any dot | 39,294 |
| `Fiber Green Biz` — the NEW-FIBER DETECTOR | 7,300 |
| `Gold Confirmed` — a SIGHTING count, not doors | 4,707 |
| `Upgrade Orange Biz` — the gold half of the detector, dead | 62 |
| `Territory Claims` · `_Dedupe Lock` | 0 |

**TWENTY-ONE TABS WERE DELETED 2026-09-02/03 BY SOMEBODY UNKNOWN.** Anything
this file or the sheet skill ever named that is not in the table above is GONE:
`Unknown Customers` · `Gold Dots` · `GOLD — CLEAN` · `Beaumont Gold — Aug 2026` ·
`TEST-Green-2026-08-24` · `TEST-Gold-2026-08-24` · `Backend Comm` ·
`Backend Analysis` · `Backend Capture` · `Hunter Status` ·
`HOUSTON UNVERIFIED — Aug 19` · `ZZ_TMP_GRID` · `TMP Sweep Census` ·
`Gold Biz Campaign — READY` · `Devonwood Campaign` · `Operator Scorecard` ·
`_dispatch` · ` _temp_ash_lookup` · `_optimus_probe`. **Four of those were
hand-built working tabs that should not have gone — `Warm Backlog — Replied YES`
(40 people who said yes), `Angleton Call List — Aug 2026`, `WORK LIST — Beaumont
+ Angleton`, `GOLD — CLEAN`. Google File → Version history restores them; ASK
PATRICK whether he deleted them.**

**`DASHBOARD`, `README`, `Enriched Leads`, `New Fiber Alerts`, `Fiber Zones` and
`Outage Signals` are NOT tabs on production.** DASHBOARD and README never
existed and were this file's recommended first read path for a week.
`Enriched Leads` and `Sales Log` are REAL but live in the **SPLIT workbook**
`1DXu-nuQvVKrqQVk8LDNwLztG31ddi6sAyo8vXDFKcmQ`, not here. `Fiber Zones` and
`Outage Signals` are read by the hunter's opening-intel banner, which is why it
prints nothing every launch.

For anything big: make ONE temp tab, put bounded QUERY/COUNTIF formulas in it,
read the small result, delete the temp tab. Autosheet has died twice pulling
whole tabs.

**The workbook has a hard ceiling of 10,000,000 cells and it has been hit
(2026-08-26).** Writes then fail with `[400] This action would increase the
number of cells ... above the limit`, which no retry can ever satisfy. A tab is
billed for its whole GRID, not the rows in it — a tab added as 5000x26 bills
130,000 cells holding ten rows, and the hunter creates tabs that way, so there
is usually free room. `FREE_SPACE.bat` shrinks over-allocated grids (deletes
nothing) and can then drop the frozen `TEST-*` tabs. Precise Fiber alone is
roughly 5.7M cells, so if resizing is not enough that tab needs archiving to
its own spreadsheet. Google also allows only ~60 writes per minute per user;
the hunter now throttles itself rather than collecting 429s.

## Things that cost real time to learn

**Texting**
- **Identify as "Patrick with AT&T Fiber." Never name the dealer brand in a
  customer text.** Patrick, 2026-08-22: *"don't say optimus / we're att."* The
  customer is buying AT&T Fiber and has never heard of the dealership.
- **Never write opt-out language — GoHighLevel appends its own.** Verified: the
  Aug 21 batch shipped `Reply STOP to opt out.` followed by GHL's
  `Reply STOP to unsubscribe.` on every send. A doubled STOP line is the
  clearest tell that no human wrote the message.
- **One SMS segment: 160 characters INCLUDING GHL's 27-character append**, so
  ~130 of body. The Aug 21 message ran 388 characters and three segments.
  Keeping price out of the first text buys most of that back.
- Read the contact tags before writing. `absentee-owner` means they do not live
  there — ask about the property, never "your address".
- Never text a landline — Twilio 30006, and it counts against the sending number.
  About **12% of residential skip-trace rows are landline-only**.
- Quiet hours **8am–9pm Central**. Check `America/Chicago` before sending.
- Never quote a flat price. Residential: "in the $20s to $30s for the first year,
  I'll confirm your exact price before anything is ordered." **Business fiber is
  priced by speed tier — never use residential figures on a business.**
- Every message individually written. No two identical.
- **Text people 2-3 times.** Patrick, 2026-08-27, striking the old
  one-text-then-call rule: *"I didn't say that its retarded text people 2x 3x
  time they sometimes respond wtf."* Later touches get replies — that is how
  every outbound sequence works. Space them a few days apart, write each one
  fresh, and stop the sequence the moment someone replies or opts out.
- The old rule claimed opt-outs spike on message two. **That was never
  measured.** The only batch we have numbers on (Aug 21, 100+ texts) produced
  zero replies AND zero opt-outs, because nobody ever sent a message two. Watch
  the opt-out rate as touches go up and let the real number decide — it is a
  dial, not a law.
- Any reply gets a call the **same hour**. People have opted out while waiting.

**DealMachine**
- `enrich_address` really costs **1–2 credits**, not the ~6 in older notes.
- `enrich_address` / `enrich_latlng` have **no `estimate_cost` flag** — probe one
  and read `credits.used` before a batch.
- **`enrich_latlng` needs no ZIP**, which is how gold dots get enriched despite
  street-only addresses. `enrich_address` fails hard without a ZIP.
- LLC-owned commercial property returns `contacts: []`. Use the free Texas
  Comptroller franchise search for officers, then enrich their home address.
- Name-only search is a money pit — narrow by ZIP.

**Data integrity**
- Never write placeholder text into a phone or status field. A column once held
  the literal text `(all DNC)` where digits belonged; the numbers were fetched
  and thrown away and gold couldn't be texted for a day.
- Column F of `Fiber Green Biz` is a hand-typed call-status field, **not a DNC
  check**. DNC status on those rows is unknown.

**DNC:** Patrick's standing call is not to sweat it — AT&T is fine provided
opt-outs are honored and opt-out language is present. Record the status, send
anyway.

## NO COMMISSION NUMBERS IN ANYTHING THAT REACHES ARA (2026-08-27)

Ed, by text: *"Please do not put commission numbers in any email that goes to
[Ara] ... I just don't want her to know upgrades pay 140!! Because I have told
her they pay very little."*

**Rule: no dollar figures in any email, sheet or message that Ara can see.** Not
$140, not $500, not a total, not a per-unit rate, not a "worth about" — nothing
a commission can be reconstructed from. This is Ed's call about his own rep and
Patrick agreed to it; record it, do not relitigate it.

Ara is `aranezzaespinosa99@gmail.com`. The trap is that she sits on the
all-hands distribution (Dave, Ed, Ara, Jay, Churchie), so a team-wide update is
an email to Ara. **Before sending anything to more than one person, check the
recipient list for her address, then strip the money.** The same applies to the
daily brief's VA section, which emails VAs directly, and to any sheet shared
with her.

Say "the upgrade" and "the higher-value sale" instead of the numbers. Dave and
Churchie can still be given figures directly — the restriction is Ara.

**This has already been breached once, by Claude.** Gmail `1a0443ed44f775a2`,
sent 2026-08-27 17:22 to all five, states "The $500 sale" and "The $140
upgrade" in plain text. That is the email behind Ed's message. It cannot be
unsent.

## How Patrick wants to be worked with

Move fast, do the work, report results. He corrects hard and directly — take it
and move, don't over-apologize.

- Don't tell him to stop working or rest. Ever.
- Don't add hard rules to the brain that he then has to deprogram. Record facts.
- Ask before modifying his data or config.
- Don't pile on security warnings; that isn't his concern at this stage.
- Dave is the only one who dials — don't invent rep assignments.

Where a line is worth holding: anything irreversible and outward-facing. Texting
at 11pm, deploying to every hunter PC, spending a large credit batch on an
unverified assumption. State the concern once, then do what he decides.

## The hunter's contract (2026-08-27): aim, start, forever

Patrick, after one night of watching news-flights: *"no jumping!! we never
stop until the pc dies."* Default behavior (commit `f38b3cc`): the operator
aims the map, the sweep spirals OUTWARD from there and never ends on its own.
News-chasing (auto-flying to AT&T build-out towns) survives ONLY behind
`--follow-news` — full flight lessons in BRAIN 22.36/22.36b. **DEPLOYED and
verified 2026-08-27** (hash `648301c`), together with the Ctrl+arrow keys and
the fix for GO, which had never worked mid-run on any machine. Closing the
browser takes typing `q`; a bare Enter does nothing, because a stray Enter
once killed Chromium mid-run.

## Hunter keyboard controls (global — work while Chrome has focus)

| Keys | What it does |
|---|---|
| **Ctrl+DOWN-arrow** *(aliases: Ctrl+P, Ctrl+Pause)* | **PAUSE / RESUME — same key both ways, MOTION ONLY.** Hunter lets go of the map at the next cell; capture and the uploader stay ON. Pan/zoom/search by hand; everything viewed is still captured |
| **Ctrl+UP-arrow** *(aliases: Ctrl+G, Ctrl+Shift+Y)* | **GO** — sweep outward from the CURRENT view (fresh spiral, no relaunch). Also skips the opening countdown. **Before 2026-08-27 GO never worked mid-run** — the key raised a flag only the countdown read; the sweep never consumed it. Fixed in `03dca35` |
| Ctrl+Shift+S | Gentle stop — finish the cell, close clean |
| Ctrl+Shift+K | Force-quit, even if frozen |

**Ctrl+arrows as of 2026-08-27, third round** (Patrick: three-finger chords
"never work", then "give me different keys"). Ctrl+arrow opens no dialog in any
program. The hunter injects a key-shield script into every page that cancels
Chrome's handling of Ctrl+P/G/Up/Down (Print, find-next, and Mapbox bearing
rotation) so only the hunter acts on them; if the shield fails it says so at
launch. Bare F9 stays dead (a stray press once un-paused a sweep mid-edit).
"B to print to sheet" from the same conversation was a typo — no such key.

The corner-stop gesture needs the pointer **still** for ~1.2s, not merely in a
corner: the hunter drives the cursor on every pan, so the old 0.45s rule let it
stop itself and blame the mouse.

The sweep also **holds 10 seconds before its first pan** so the map can be aimed
by hand — Ctrl+Shift+Y skips the wait. Unattended runs skip it automatically.
Operators type **initials** now (PS), not a name picked off a menu.

Ctrl+Shift+P is a real alias, not a typo: Pause/Break is an Fn-layer key on most
HP laptops. Pausing drops a `PAUSED.flag` file — that is how the **separate
uploader process** knows a long pause isn't idleness and keeps writing. Never
"clean up" that file mid-run.

## Installing on a new PC

ONE installer covers both tools (Fiber Hunter + Maps Scraper): `INSTALL_OPTIMUS.bat`.
Double-click it, wait ~5-10 min the first time, and two Desktop icons appear. It
pulls the tools from public GitHub on every launch, so it never goes stale and
needs no Drive access of its own.

| Source | Link |
|---|---|
| Google Drive (Patrick's My Drive) | https://drive.google.com/file/d/1IRnfbeQt2TTxNGVgQL664q3C4lu1biLd/view |
| Drive direct download (skips the preview page) | https://drive.google.com/uc?export=download&id=1IRnfbeQt2TTxNGVgQL664q3C4lu1biLd |
| GitHub Release (no Google login) | https://github.com/patricksiado-prog/Go-High-Level-MCP-2026-Complete/releases/download/installer/INSTALL_OPTIMUS.bat |
| Release page | https://github.com/patricksiado-prog/Go-High-Level-MCP-2026-Complete/releases/tag/installer |

All three are the SAME file, verified 2026-08-23: **7,204 bytes**, sha256
`0f9295b82aba2ef2b6cf47a55a8e7c700cae91afa614657bb1f1c95ac8b95252`. If a copy
does not match that, it is not the current installer.

**Three stale installers are still sitting in Drive** and will strand a new PC on
old code — `install_optimus.bat` (4,838 bytes, May 26), `install_optimus.py`
(8,137 bytes, May 10), `install_optimus.bat` (3,906 bytes, Jun 12, different
folder). Only the ALL-CAPS `INSTALL_OPTIMUS.bat` is current.

The Drive copy is not shared with anyone — it works on a PC signed in as Patrick.
Anyone else uses the GitHub Release link.

## Where things live

- **`BRAIN.md`** — long-form memory. Read it when you need depth on the hunter,
  the classifier, or past sessions.
- **`OPTIMUS_SESSION_LOG.md`** — dated session records and findings.
- **`.claude/skills/gold-cluster-sweep/`** — the full lead loop: backlog dig →
  cluster → enrich → text/email/dialer → book → follow up. Invoke it whenever
  the work is finding or working leads.
- **`docs/archive/`** — older material, superseded. Do not act on it.

## NO NEW PROGRAMS — EVER (Patrick, 2026-08-27)

*"i don't wanna run any more programs or even have programs ... unless I don't
have to mess w them and nobody does ... if the scraper or hunter launches
something or something cool but probably better to attach to them."*

Two programs exist: the **Fiber Hunter** and the **Maps Scraper**. That is the
whole roster. Any new capability gets built INSIDE one of them — running
automatically, at startup or when the problem appears, asking nobody. A .bat
that a human must remember to run is a failure of this rule, not a deliverable.
`FIND_NEW_FIBER.bat` died to this rule on 2026-08-26; `FREE_SPACE.bat` was
retired by it on 2026-08-27 (see below). Before proposing anything that needs
an operator: research what people actually do, then make the software do it.

## DO NOT BREAK THE SOFTWARE — AND ASK BEFORE YOU TOUCH IT

Patrick, 2026-08-27: *"new brain rule don't ever break software!! and if u
modify sheet modify software check w me and don't break stuff."*

**RULE 0 — ASK FIRST. Every time.** Before changing anything in the hunter, the
Maps Scraper, or the sheet: say what is broken, say what the fix is, and WAIT
for him to say go. This outranks every rule below it. A fix that is written,
tested and sitting unpushed has cost nothing. A fix that is pushed without
asking has already deployed to every PC.

This is not a rule about being careful. It is a rule about *who decides*. He
runs the machines, he watches the console, he loses the day when capture stops.
The call is his, not yours — including when the fix is obviously right, including
when the software is visibly broken right now, and including when you are certain.

Applies to: any file in `_CORE_FILES`, anything under `optimus/standalone/`,
the sheet's tabs, headers or contents, and any config on a hunter PC.
Reading, diagnosing, writing the fix and testing it locally need no permission —
those are free and reversible. **Pushing is the line.**

## EVERY HUNTER PUSH BUMPS `BUILD_DATE` (learned 2026-09-03, the hard way)

`BUILD_DATE` at the top of `precise_fiber_hunter.py` is how the self-updater
decides a download is real. Two relaunches on 2026-09-03 printed *"Update looked
stale/partial -- keeping the copy you have"* and ran the 08-24 build, because
`59a92bf` and `fcc6b6e` shipped with the date untouched. **Every deploy to the
hunter today was dead on arrival until `35f1607` bumped it.** brain-verify now
checks the date matches the last push. Bump it in the same commit as the change,
then wait ~3 minutes for the raw CDN before telling Patrick to launch.

## DO NOT BREAK THE HUNTER

**A push to `Go-High-Level-MCP-2026-Complete` is a DEPLOY, not a commit.** Every
file in `_CORE_FILES` lands on every hunter PC at next launch. There is no
staging, no rollback button, and nobody is watching the console when it breaks.
A silent regression costs a day of capture on every machine at once. These rules
were all bought with real damage on 2026-08-26.

**1. Find what silently depends on what you are changing.** Grep for every
reader of it before you touch it. Making `Precise Fiber` green-only quietly
broke four things that all looked unrelated: `seen`-marking (fed from that
queue, so grey would re-queue every 2s forever), idle detection (a grey-only
stretch left the queue empty and the uploader quit mid-run), the gold cluster
alert (read that queue for gold, and was gated on it), and `optimus_summary`'s
ORANGE scan (now matches nothing while reading two 474k-row columns to prove
it). None of them error. They just go quiet.

**2. Measure behaviour changes. Do not reason about them.** Gold clusters, so
tightening the sweep onto a gold pocket is obviously right — and simulation
against the real control flow showed it was **80% WORSE**: 11 unique cells
instead of 100, because the outward spiral already visits every neighbour once
and any dwell re-scans captured ground. It was written, measured, and deleted
the same hour. Build the simulation before shipping the idea.

**3. Check the checker.** The first column-alignment test written that day was
off by one and called correct code broken. If a test says something is wrong,
confirm the test is right before "fixing" the code.

**4. Anything touching the sheet writer must respect BOTH quotas.** Google
allows ~60 writes AND ~300 reads per minute, counted separately, plus the 10M
cell ceiling. `replay_pending` looked up the worksheet once per parked FILE --
a read each -- and blew the read quota before writing a row, then left every
file in place so the next launch had more. Anything per-item in a loop that
touches Google is a bug waiting for volume: cache per tab, merge into 500-row
batches, and bound the work per launch.

**5. Never retry an error that cannot succeed.** The 400 cell-limit error was
retried three times per batch like a network blip. Classify first: 429 = wait
(and the wait must outlive a per-MINUTE window, so 1s and 2s were useless),
400-cell-limit = permanent, say so once and stop.

**6. Rows are never allowed to vanish.** `_park_batch` named files by row COUNT,
so two failed batches of the same size in one run overwrote each other. The
function whose entire job is "do not lose rows" was losing them. Park files are
deleted only for rows Google actually acknowledged.

**7. Verify against the feed, not against hope.** `optimus/_feed/latest.json`
carries `written`, `failed_writes` and `capture_truth.delivery`. "It classified
126,628" means nothing if `written: 0`. Check that field before saying anything
is fixed.

## Keeping this file useful

When something is learned that would change what a future session does, add it
here (short) or to `BRAIN.md` (long), then commit and push. Anything not
committed does not survive — a finding that lives only in a chat is lost when
that chat ends.

## NEW RULE — NO SILENT RUNNING (Patrick, 2026-08-28)

*"going forward dont let the software work if it's not writing to the sheet"*

Ara ran the Maps Scraper for hours on 2026-08-28 and asked why her ZIP wasn't on
the sheet. It wasn't because the workbook was FULL — the scraper had quietly
switched to parking rows on her disk and kept scraping. Nothing was lost, but
nothing was **delivered**, and the operator had no way to know. Hours of an
operator's time bought zero usable rows.

**Patrick corrected this the same day: NOT stop-on-full.** *"not stop on full
but make it obvious it's doing nothing."* He is right and the first draft of this
rule was wrong — the capture is still worth having, the parked rows replay
automatically, and stopping throws away good work. The only real defect was that
a full sheet *looked like* a working run.

**The rule: never stop, but never let it look like it is working.** DEPLOYED
2026-08-28 (PR #8, `e06d976`):

- **Every per-search line** ends `<-- NOT ON THE SHEET, parked (N held)`. A
  banner printed once scrolls away in minutes; a suffix on every line cannot.
- **The ZIP-complete line** says plainly that nothing went to the sheet.
- **The closing summary** ends on a loud block, never on a row count that reads
  like success.
- **`LIVE_COUNTS_scraper.txt`** carries the same status, so it is visible
  remotely and not only on the operator's screen.
- **`_PARKED_ROWS`** tracks the real count so every message quotes a number.
- **Rate limiting (429) is untouched** — transient and self-clearing. Park and
  replay untouched. Nothing is ever discarded.

The general principle, worth applying anywhere else it fits: **when software
degrades to a mode that produces nothing usable, the degradation has to be
visible in the thing the operator is already looking at** — not in a banner
they scrolled past twenty minutes ago.

## REPS ARE NUMBERS IN GHL, NOT NAMES (Patrick, 2026-08-29)

*"I don't want names Just rep #."* Confirmed as meaning **inside GoHighLevel**:
rename the users to `Rep 1`, `Rep 2`, `Rep 3`, so lead assignments, dispositions
and every report show a rep number instead of a person. Set it up that way from
the start — renaming users after assignments exist is messy. This is separate
from what a rep says on a call, which stays "Patrick with AT&T Fiber."

## DIALER PRIORITY ORDER — BEST LEADS FIRST (2026-08-29)

Patrick: *"I want the best leads dialed first ... clean att dial."* The order,
which is by VALUE not by capture date:

1. **GOLD / copper** — existing AT&T customers still on copper. No competitor to
   beat, it is an upgrade not a switch.
2. **GREEN, never touched**, with a mobile number, in a worked market.
3. **GREEN, touched once, no answer, 3+ days ago.**
4. Everything else.

**Never dial:** GREY (already on AT&T fiber — not a lead), any row with no mobile
number, and anyone already dispositioned Not Interested / Bad Number / Do Not
Call.

Two rules that outrank the order itself: **cut every list down before it ships**
(60 right numbers beats 300 wrong ones), and **persistence beats fresh names** —
one dial connects ~1 in 10, the same prospect across several attempts ~1 in 4.

**The `Do Not Call` disposition must set DND automatically.** It is the one
automation in the dialer with legal weight and must never depend on a rep
remembering a second step. DNC-status-on-the-lead is a different thing: a data
field that arrives with the list, recorded and then called anyway per Patrick's
standing call.

### Connecting a second Claude to the same GHL

Patrick was right that it is the **same connector**, not a second one — the
GoHighLevel MCP endpoint is identical for everybody and the **token** is what
scopes it. So a contractor uses the same connector with their own Private
Integration Token issued from our sub-account (GHL → Settings → Private
Integrations). Free with any plan, ~5 minutes. **The token comes from Patrick and
never travels in an email or chat.**

## SIX DIAL ATTEMPTS, THEN OUT OF THE QUEUE (Patrick, 2026-08-29)

Patrick first said *"I want leads to recycle until they say no"*, then read it
back and settled it: *"6 attempts ok that's enough."* **Six is the rule.** The
recycle-forever version is dead — do not resurrect it.

A No Answer re-queues rather than removing, on a widening gap:

| Attempt | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Dial on | day 1 | day 3 | day 7 | day 14 | day 30 | day 60 |

About two months of coverage per lead. **The widening gap is load-bearing, not
decoration** — repeat-dialing the same person inside a short window is one of the
behaviours that earns a number a `Spam Likely` label, so the spacing protects the
caller ID while the lead still gets six real chances.

**After the sixth attempt, do NOT mark them `Not Interested`.** Nobody said no —
we never reached them. Leave the lead un-dispositioned and out of the dial queue
so it stays available for a future campaign and the reporting does not count it
as a rejection. A no-answer and a no are different numbers; keep them apart.

**Only three dispositions are real exits:** `Not Interested`, `Do Not Call`,
`Bad Number`.

The underlying evidence still holds and is why six rather than one: a single dial
connects ~1 in 10, the same person across several attempts ~1 in 4.

## WHAT THE REP SEES BEFORE THEY SPEAK (Patrick, 2026-08-29)

*"Addresses in n notes section / And indicator of what it is."* Two things on
every GHL contact, visible without opening another tab:

1. **The property address at the TOP of Notes**, on its own line — not only in
   `address1`. These leads ARE the address; the whole pitch is "fiber is live at
   your address," and a rep who has to hunt for it will not say it.
2. **An indicator of the dot colour**, in two places: a **tag** so the dialer can
   sort and prioritise by it, and a **line in Notes under the address** so the
   rep reads it before speaking.

| Colour | Tag | Means | How the rep opens |
|---|---|---|---|
| GOLD / copper | `GOLD-UPGRADE` | Existing AT&T customer still on copper, fiber at the curb | An upgrade they are already entitled to. No competitor to beat |
| GREEN | `GREEN-NEW` | Fiber live, NOT an AT&T customer | Availability notice, not a switch pitch |
| GREY | — | Already on AT&T fiber | **Not a lead. Never dial** |

That distinction is the whole call. A rep who cannot tell gold from green at a
glance pitches both the same way and loses the easy one. The opener for both
stays the same true thing: AT&T is retiring copper, Phase 1 by 2027, Phase 2 by
2029.

## DNC IS NOT A BLOCKER — SAY IT PLAINLY (Patrick, 2026-08-29)

*"I don't mind dnc texting and calling."* The SMS routine had been excluding
`dnc-flagged`, which contradicted this. **Fixed 2026-08-29.** The distinction the
software must make, and the wording now sitting in the routine prompt:

| | |
|---|---|
| **Registry DNC** — tag `dnc-flagged` / `dnc`, or DealMachine DNC=yes | **Record it and send/dial anyway.** A third party's list. |
| **They told US to stop** — inbound "stop"/"remove", tags `not interested` / `wavv-not-interested`, disposition `Do Not Call` | **Absolute, forever.** The customer talking to us. **CORRECTED 2026-09-04: GHL DND / SMS STOP_KEYWORD is NOT in this row — see "WE CALL DND" above. A STOP blocks TEXTS only; we call them.** |

The difference is *who asked*. Never collapse the two. Never `scrub_dnc` on a
DealMachine export — it throws away roughly a third of the callable leads.
