# Optimus — operating brain

Claude Code loads this file automatically at the start of every session in this
repo. **Read the CURRENT STATE block below first — it is the only part that
claims to be true right now.** Everything under it is the historical record,
appended newest-at-the-bottom. Where two sections disagree, the later date wins
and you say so out loud. Long-form detail lives in `BRAIN.md`.

---

# CURRENT STATE — updated 2026-09-03 evening (Ed was right: the dialed colours are mostly untraceable)

**Update this block whenever any line in it changes, in the same turn.** A
finding buried 2,000 lines down in the log is a finding nobody will read. This
block is short on purpose; if a line needs more than two sentences, put the
detail in a dated section below and point at it from here.

Mark every line **MEASURED** (with how and when) or **ASSUMED**. Never let the
two share a voice — that is the mistake that let "register for the 20M-cell
beta" survive four sessions unchecked.

### THE LOCAL SESSION CAN RUN THE WHOLE MACHINE ITSELF (Patrick 2026-09-04: *"can this folder deploy the scraper ... and scrape refresh ect on its own"*)

**YES, and this is the end of the double-click dependency.** Standing in
`maps_scraper`, a local Claude can LAUNCH the Maps Scraper, write the workbook
with the fiberscanner service account, run `gold_audit.py` (the real UNIQUE gold
count), `sheet_feed.py` (publish any tab, including the 56,799-row grey one that
no Claude read path reaches), the dedupe/clean, and push to the hunter repo. It
can also create a **Windows Scheduled Task on the EXISTING scraper** so it
relaunches every few hours — that is not a new program, it is the removal of the
human, which is exactly what the NO-NEW-PROGRAMS rule asks for.

**THE ONE THING IT CANNOT DO ALONE IS THE AT&T LOGIN.** The hunter needs a live
session at youachieve.att.com; it has been dead ~46h and 6,012 rows are parked
behind it. Relaunching does not fix an expired session. Whether saved
credentials re-auth it or a human must type a code is UNMEASURED — the local
session was asked to find out and report which.

**STANDING RULE GIVEN TO THE LOCAL SESSION: never push to
`Go-High-Level-MCP-2026-Complete` without showing the diff first.** A push there
is a DEPLOY TO EVERY PC. That is RULE 0 restated for the machine that now has
the token in its own folder.

### CLAUDE IS BEING PUT ON PATRICK'S OWN PC — THE STRUCTURAL FIX (2026-09-04, from two screenshots)

**LIVE 2026-09-04 ~07:00Z: he has DONE it.** The desktop app shows the chips
`Local` + `maps_scraper` under the prompt box, and the clone instruction pasted
in, waiting on Enter. So a local session on `maps_scraper` exists from here on —
the next session should ask what it reported back rather than re-explaining the
setup.

Patrick opened the Claude desktop app and is picking a folder for a LOCAL
session. **This is the fix for the thing that has blocked every sheet request
this week.** From here the Drive connector is file-level only — Claude cannot
write a tab or a cell — which is why `Enriched Leads` waits on a Maps Scraper
launch. **Claude running LOCALLY in `C:\Users\patrick siado\maps_scraper` has
the fiberscanner service account sitting right there**, the same credentials
`gold_audit.py` and `sheet_feed.py` already use, so it can write the workbook
directly and run the scraper itself. Tell him to pick that folder.

**HIS USER FOLDER (MEASURED off the screenshot):** `C:\Users\patrick siado\`
holds `maps_scraper`, TWO folders starting `optimu…`, plus the usual Windows
ones. **A LOCAL SESSION DOES NOT INHERIT A CHAT** — it starts blank and takes
its memory from a `CLAUDE.md` in the folder it opens. `maps_scraper` has the
tools but not the brain, so the first thing a local session must do is
`git clone https://github.com/patricksiado-prog/optimus-map-tools` and read it.

**THE DOT FOLDER HE ASKED ABOUT IS `.claude`** — 55.9 MB, created 2026-09-01
1:02 AM, containing `backups / projects / session-env / sessions` and
`.last-cleanup`. That is Claude Code's OWN data directory: session history and
project settings. **Never pick it as a work folder and never delete it.**

**UN-KILLED THE SAME MINUTE — 2026-09-04.** He said *"fuck those sessions I'm
not really concerned w them"* and then *"nm if they were useful to my goals go
ahead."* So it is OPEN again, but only two of the five are worth anything:
**`Deploy scraper: full address backfill`** (fills City/State/ZIP on rows that
carry only a street line — 88 of the enriched pool have NO address and 94 have a
bare street, and the address IS the pitch) and the **Google Sheets permission**
one, worth opening just to see what it wanted.

**THE OTHER THREE ARE A HAZARD, NOT A CHORE.** `Deploy hunter keys:
Ctrl+arrows + working GO`, `Deploy hunter v2: aim-start-forever` and `Deploy
hunter fixes` are all features that **already shipped and were verified
2026-08-27** (`648301c`, `f38b3cc`). Those sessions are stale, and a push to
`Go-High-Level-MCP-2026-Complete` is a DEPLOY TO EVERY PC. Approving one could
put an old `precise_fiber_hunter.py` over the current build — the same
54-commits-behind trap that nearly ate the 09-03 board deploy. **Read the diff
before approving anything that pushes to the hunter repo.**

**SEVERAL DESKTOP SESSIONS ARE STUCK ON A SINGLE UNTAPPED PERMISSION** — the
list shows `Needs input` / `Waiting on permission: mcp__…` on **Deploy scraper:
full address backfill**, a **Google Sheets document**, **Deploy hunter keys
(Ctrl+arrows + working GO)**, **Deploy hunter v2: aim-start-forever**, and
**Deploy hunter fixes (one approval needed)**. That is finished work that never
landed because nobody pressed Allow. Worth ten minutes.

**THE ROUTINES UI IS IN THE SAME APP** (left sidebar, clock icon). Routines
created there keep their connectors permanently AND are Patrick's own action, so
that is the one place the autonomous auto-texter can legitimately be created —
it solves the mortality problem and the classifier block at the same time.

### ONGOING TASKS — TWO ROUTINES BUILT, AND THE AUTO-TEXTER WAS BLOCKED (2026-09-04 05:50Z)

Patrick: *"can i have u or cowork do ongoing tasks like monitor the production and
text customers that need following up with"*, then *"text me too"*. He was
offered alert-only / inbound-only / full auto-texting and **chose FULL follow-up
texting**, and chose to rebuild the AM/PM editions unbound. Both answers recorded
as his decision after the deliverability concern was stated once.

**BUILT AND LIVE:**
- **`trig_01Dm9Y29L4zNAraMsJHjAuCS` — production monitor, every 2h at :44,
  FRESH SESSION.** Curl + git only (no connectors, see above), which is enough:
  it reads heartbeat / latest / tabs / _landed and **speaks only on a state
  change** — scraper launched, board landed, hunter down >6h, a tab shrank.
  Silent otherwise. Its completion summary **push-notifies Patrick's phone**;
  that is the alert channel, and push works with no connectors.
- **`trig_019Cwaq6UkA1CSatiEnWyiQt` — follow-up chaser, 14:00/17:00/20:00 UTC
  (9am/12pm/3pm CT), BOUND to `session_01GRgAKeNm1SCYDrD16GcSTX`** so it inherits
  every connector. Finds replies with no answer, works the six-attempt cadence,
  drafts each message, texts Patrick at **`+18322474060`** and emails the list.

**THE AUTO-SEND WAS REFUSED BY THE HARNESS, NOT BY ME.** Creating a routine that
autonomously texts customers returned *"Permission for this action was denied by
the Claude Code auto mode classifier."* **Do not try to route around it.** The
chaser therefore identifies and DRAFTS; a human presses send. Two ways to get
what Patrick actually asked for, both his to do: add a permission rule in
settings, or create the sending routine himself in the **claude.ai Routines UI**
— which also solves the connector problem, since UI-created routines carry them.

**PATRICK'S MOBILE IS `+18322474060`** (GHL contact `pTf15HQ88QisY5RuCbf1`) — it
is the number already used in outbound copy. That is where "text me too" goes.

**THE GUARDS WRITTEN INTO THE CHASER, because "full sending" is only safe with
them:** never a landline (tag or Twilio 30006 — they fail and the failure counts
against the sending number); never a DND/STOP/not-interested; **never anyone
texted in the last 5 days from ANY source** (the over-contact guard — 11 Milton
opt-outs in one day came from several automations hitting the same people the
same hour); registry DNC is NOT an exclusion; quiet hours 8am–9pm CT; read
`ghl_list_phone_numbers` live every run; one segment, no self-written STOP, no
"Optimus", no flat price, no two messages identical; **circuit breaker — 3+ new
opt-outs and the run stands down.**

### WHAT IS ACTUALLY RUNNING ON A SCHEDULE — 15 ROUTINES READ LIVE (MEASURED 2026-09-04 06:40Z)

Patrick: *"can i have u or cowork do ongoing tasks like monitor the production and
text customers that need following up with"*. Read `list_triggers` before
answering. **12 are enabled. 8 of them are FRESH-SESSION and they genuinely run.**

| Routine | id | cron (UTC) | last run |
|---|---|---|---|
| Fiber inbox watch — notify on interest | `trig_01UhaqVy9Aaxf2rukgxoKngu` | `31 */2 * * *` | **SUCCEEDED 2026-09-04 04:31** |
| Optimus SMS — 200/day | `trig_018JYeQpvcgfrmBxc46Vv967` | `0 16,21 * * *` | SUCCEEDED 09-03 21:09 |
| daily gold cluster sweep | `trig_019hQhMhfiGobxDXaN1e7mAp` | `7 14 * * 1-5` | SUCCEEDED 09-03 14:10 |
| cable outages + new fiber | `trig_01DfRVRoPajmieDYNfY1xtmQ` | `0 14 * * *` | SUCCEEDED 09-03 14:17 |
| daily new-fiber email | `trig_01MfufwTL7NxwKPW3tYiHNYy` | `0 13 * * *` | SUCCEEDED 09-03 13:05 |
| Fiber Green Biz dedupe | `trig_0166v3uSachDJv8YtRbFqcSX` | `0 11 * * *` | SUCCEEDED 09-03 11:06 |
| Applicant chase 2x daily | `trig_017qj6LqY7bpayftBeAAeYYz` | `0 14,21 * * *` | SUCCEEDED 09-03 21:10 |
| Morning Brief — Patrick | `trig_019vheHFZBKyGnzbu6tVjPjb` | `0 13 * * 1-5` | **ABANDONED 09-03 13:18** |
| Houston–Colombia fare sweep | `trig_011Friai35C2Zd5jWeg9xwBX` | `0 13 1 * *` | **ABANDONED 09-01** |

**I WAS WRONG TO CALL THAT A CORRECTION — RE-CORRECTED 2026-09-04 05:45Z.**
The original claim was RIGHT. `create_trigger` refuses the `connectors`
parameter on this org (`not available for this organization`), and every
fresh-session routine it makes returns **`mcp_connections: []`** with the
warning *"the sessions it fires will run without connector tools."* So an
unbound routine has NO GHL, NO Gmail, NO Drive. **The 8 unbound routines
reporting SUCCEEDED prove nothing about whether they had access or did anything**
— that is the same `SUCCEEDED`-means-nothing trap as the SMS routine, and I fell
for it an hour earlier by reading a status instead of a capability. Routines
created in the **claude.ai Routines UI** can carry connectors; ones created from
this MCP tool cannot. The old text follows for the record:

~~**CORRECTION — "a fresh-session routine carries no connectors on this org and
would produce nothing" IS WRONG.**~~ Eight unbound routines ran to SUCCEEDED
yesterday, one of them two hours ago. That claim (in the daily-coverage-gap
skill and repeated in this file) blocked the obvious fix for months. **What is
true is narrower: the AM/PM coverage-gap pair
(`trig_01JTQKnB2U5ihS1mC4rpX2qy`, `trig_01RjAUBz16UNpdDzK2neCz37`) and the
`rjdb1972` follow-up are bound to `session_01GRgAKeNm1SCYDrD16GcSTX` and die
with it.** `create_trigger` now takes a `connectors` list — that is the way to
rebuild them unbound. NOT DONE, needs Patrick's go.

**`ABANDONED` is a real failure mode and nobody was watching it.** The Morning
Brief routine has been firing and abandoning; that is why a personal email can
go quiet without any error reaching anyone. Check `last_run.status` on every
routine, not just `enabled`.

**`Optimus SMS — 200/day` reports SUCCEEDED and the brain separately measured it
sending ZERO.** Do not read SUCCEEDED on a routine as evidence a text went out —
same trap as `success: true` from `send_sms`. Check 3.

**STANDING CAUTION BEFORE ANY NEW AUTO-TEXTER:** 19 STOPs in the last 25
conversations, 11 Milton opt-outs in one day, `No Answer - 6 attempts`
(`cde882bb-d84a-4998-9259-50281f6ce072`) still texts on attempts 1/2/3, and the
old $30 promo is still sending from somewhere nobody has found. **Adding another
scheduled sender into that pours fuel on the fire.** The follow-up that is
actually leaking money is inbound: people who REPLIED and never got called back.
That population is tiny, carries no spam risk, and is where a monitor should aim.

### THE WHOLE ENRICHED POOL IS NOW IN ONE LABELLED FILE — 3,511 ROWS (MEASURED 2026-09-03 evening)

Patrick: *"give me a file w all the gold enriched / the new green Beaumont
angleton laport all together labeled"*. Built and handed to him as
`OPTIMUS_GOLD_AND_GREEN_labeled.csv` (634 KB, 3,511 rows, 16 columns).

**Columns:** LABEL · COLOUR · TIER · MARKET · TYPE (resi/biz) · NAME · CELL ·
ADDRESS · LANDLINE-CALL-ONLY · DNC(registry) · DO-NOT-CONTACT(they told us) ·
DISPOSITION · ATTEMPTS · COLOUR SOURCE · COLOUR TRACEABLE · GHL CONTACT ID.
Sorted **gold first, then green by market**.

| | n |
|---|---|
| GREEN | 2,422 |
| GOLD — copper upgrade | 318 |
| GOLD — att.net email (already an AT&T customer) | 195 |
| UNVERIFIED (no dot) — the Milton pool | 120 |
| NO COLOUR MARKER | 456 |
| **Beaumont + Angleton + La Porte together** | **2,761** |
| Beaumont 1,388 · Angleton 696 · La Porte 677 · Milton 141 · Houston 255 | |
| RESIDENTIAL 3,003 · BUSINESS 508 | |
| **ALL GOLD = 513** (Beaumont 365 · La Porte 56 · Angleton 49 · Milton 21 · Houston 16), **509 callable now** | |

**Only 416 of the 3,511 (11.8%) have a traceable colour source.** Same finding as
the called-lead audit, now across the whole pool. The file carries it per row so
a rep can see it.

**253 are LANDLINES — call, never text. 30 have told us to stop** and are marked
DO NOT CONTACT. **88 have no address at all and 94 are a bare street with no
house number** — both now read `ADDRESS UNKNOWN - ASK FOR IT ON THE CALL` /
`[NO HOUSE NUMBER - ASK ON THE CALL]` in the address cell so no rep reads a
street name aloud.

**CORRECTION — `alpha-t5-green` is 2,309, not 2,511.** MEASURED by paging the
whole tag for the first time. It is also NOT pure residential green: its tail is
`optimus-fiber-biz` / `fiber-green-biz` rows including Oklahoma 405 numbers with
no address. Labelled BUSINESS in the file.

**HOW TO PAGE A TAG BIGGER THAN 500 — this now works and is worth reusing.**
`search_contacts` caps at 500 with no offset. `official_contacts_get_contacts`
pages it: `{locationId, query:"<tag>", limit:100, startAfter, startAfterId}`,
taking the next pair from `data.meta`. 24 calls for 2,309, and **every result
lands in a file instead of the transcript, so the whole pull costs almost no
context.** The last page returns short — that is the end, not an error.

### THE CUSTOMER CONFIRMED IT HIMSELF — AND FOUR THINGS IN THIS FILE WERE WRONG (MEASURED 2026-09-03 5:45pm CT, evening edition)

**Kristopher Goodman texted at 5:21pm CT: *"Someone from ATT called me and said
we're already on fiber."*** (`ccrOYVuEsdUAlbj75iAy`, inbound 22:21:42Z, still
unread.) A rep had him on the phone 4m09s at 5:12pm; the opportunity moved
Voicemail → Call Back at 5:16pm. **That is the customer independently confirming
Ed's complaint on the exact address our data called `type-green`.** Ground truth
now comes from two directions, not one.

**CORRECTION 1 — THE EVENING EDITION HAD NOT GONE OUT.** The line above saying
*"the 5:30pm evening edition went out as three emails"* (and BRAIN.md
`## 2026-09-03 17:40 CT — Evening edition SENT`) is **WRONG**. MEASURED against
`in:sent`: the last coverage-gap emails today were the 7am pair at 12:12/12:13Z.
The evening edition went out at **22:50Z tonight**, from this turn. Gmail IS
connected — that half was right. **Never write "sent" before the send returns an
id.** Check 3, check the destination.

**CORRECTION 2 — ALL FOUR OUTBOUND NUMBERS WERE REPLACED AGAIN TODAY. FOURTH
SWAP IN FOUR DAYS.** MEASURED off `ghl_list_phone_numbers` 22:44Z. Live now:
**`+13466797668` ("dave's number 18")**, `+13466634629` (16), `+13465898086`
(15), `+13465344972` (17). **The set this file recorded this morning
(`+13466145146`, `+13464785739`, `+13465729763`, `+13465222591`) is DEAD.**
Outbound SMS today went from `+13466797668`, calls from `+13465344972`.
**Read the live list before any send — this file cannot keep up with the swaps.**

**CORRECTION 3 — DEALMACHINE IS AT 27,084, NOT 28,490.** MEASURED 22:45Z:
**2,916 used this cycle** (1,501 property + 1,415 people), 27,084 left, cycle
Sep 2 → Oct 2. This session spent ~32. **~1,400 credits moved today that this
file cannot account for.** Not an accusation — a number that moved without us.

**CORRECTION 4 — REPS ARE ACTUALLY DIALING.** Three distinct GHL user ids placed
outbound calls today (`HYaJvB1hsXbJMnb1tt4E`, `nkXp1saldPvdGhgilZzg`,
`3LSjEUJHcGL653Cgd1EW`). The long-standing "only Dave dials" line understates
what is happening now.

**WAITING ON A CALLBACK TONIGHT (2):** `(228) 627-3246` — texted 1:30pm CT
*"Finishing up with a customer right now"*, we replied and rang at 2:03pm,
opportunity created at stage Contacted, nothing since — **and we still have no
service address for them.** And Kristopher Goodman, above. **4 more STOPs today,
all Milton** (Lunsford, Livingston, Sharp, Nolan) on top of this morning's 7 —
**11 opt-outs from one town in one day.** David W Pugh: *"why do you keep
calling."*

**Won is still 2, lost still 0, no new close today.** Worth holding next to Ed's
complaint: **Janell Dumas at 350 Bradford Dr is one of the two wins, and Ed's bad
address is 330 Bradford.** The STREET is real fiber. It is the per-address colour
that is unverified — do not let the audit turn into "Beaumont is bad ground".

### WHAT DAVE CALLED THAT WASN'T FIBER — ED WAS RIGHT, AND THE COLOUR IS MOSTLY UNTRACEABLE (MEASURED 2026-09-03 ~5:40pm CT)

Patrick: *"what leads did dave call that weren't fiber"*, with Ed Saldanna's
screenshots. **All four of Ed's named leads found in GHL. Every one is either a
WRONG colour or NO colour.**

| Lead | Address | Our data said | Ed says | Where the colour came from |
|---|---|---|---|---|
| **Kristopher Goodman** `QkOP0BQNK2yryfXy4ZJS` | 555 Belvedere Dr, Beaumont 77706 | `type-green` `green-new` `fiber-2gig` | **already has fiber** | `source: "Optimus Precise Fiber - Beaumont"`, added 2026-08-26 |
| **Catherine Goodman** `j3TAmm3oRjwh2mMwoZGn` | same door | `type-green` `green-new` | same door | `medium: csv_import`, 08-28. NO source |
| **Sharon Williams** `88CxaM4F4FGXDAPVeA7b` | 330 Bradford Dr, Beaumont 77707 | `type-green` `green-new` | **"AT&T Cx, doesn't have the fiber yet"** → copper, i.e. GOLD not green | `csv_import` 08-28. Now `not interested` |
| **Justin M Scott** `bzGhgFTZ2v6jOAyT9QKS` | 5520 Shamrock St, Milton FL | `status-unverified`, NO dot | interested, warm to Ed | DealMachine `pcola-fresh` |
| **Archie L Collum** `yxPKD6HBN3hP3OljGvsc` | 5548 Willard Norris Rd, Milton FL | `status-unverified`, NO dot | **"No fiber availible"** | DealMachine `pcola-fresh` |

**GREEN means "Non-AT&T Customer - Can Get Fiber." Two of these are ALREADY AT&T
customers. That is a GREY row in a green list — not a bad lead, a non-lead.**
Ed's card notes and his own summary line disagree on Bradford (the note says
"doesn't have fiber yet", his summary says "already have Fiber") — worth one text
to pin down, but either way it is not green.

**THE WIDER MEASURE, off the 1,211 pulled from GHL: 218 show call evidence
(`att-1..6` / `no-answer` / `vmail` / `call back` / `not interested`).**

- **Only 21 of the 218 (9.6%) carry a `source` naming where the colour came
  from.** The other 197 arrived as a bare spreadsheet upload (`medium:
  csv_import`, no source) or with no provenance recorded at all.
- **149 of the 218 called are labelled GREEN. Only 9 of those 149 have a
  traceable source.**
- Across all 1,211: **462 GREEN with no traceable source · 263 gold-labelled with
  no traceable source · 141 `status-unverified` (Milton) · 148 with a real
  source.**
- **Even a sourced one was wrong.** Kristopher Goodman came from
  `Optimus Precise Fiber - Beaumont` on 2026-08-26 — and `Precise Fiber` only
  became GREEN-ONLY that same day. Before it, that tab held EVERY colour. **Any
  export taken from Precise Fiber before 2026-08-26 can carry grey and copper
  rows wearing a green label.** That is the mechanism behind Ed's complaint.

**CORRECTION TO MY OWN AUDIT OF YESTERDAY — CHECK 2, I counted the tag and not
the provenance.** The 09-03 "94 non-fiber leads pulled" table treated
`type-green`, `green-new` and **`beaumont-gold-pocket`** as "has a real dot".
`beaumont-gold-pocket` is the CSV-import tag from `CHRISTIAN_DIALER_775.csv`, not
a hunter capture. **So "gold tier is 100% clean — all 492 carry a real dot
marker" is OVERSTATED: only 33 of the 492 carry a traceable source.** A missing
`source` is not proof a colour is wrong — GHL does not record source on CSV
imports or API updates — it means **UNVERIFIABLE**, which is the whole problem.

**THE FIX IS ALREADY DEPLOYED AND IS ONE DOUBLE-CLICK AWAY.** The follow-up board
(hunter `7a69d0a`) re-reads every address against the hunter's OWN tabs at scraper
launch and writes the real `Dot Color` + `Tab`, stamping
*"Not on the hunter map yet - colour unverified"* where the address is not on the
map at all. **151 of the called leads are queued for it now** — feed sheet
`OPTIMUS FEED enriched called-audit 2026-09-03` =
`1Y85Jmv6pPFV6APdw26Ol9XFnS02hGmWMMCri17ioLp0` in the feed folder, service account
confirmed as writer. The verified-copper 65 were left out on purpose; green is
the suspect population. **Nothing settles until Patrick launches the Maps
Scraper.**

**COULDN'T READ: whether 555 Belvedere / 330 Bradford sit on `Grey Fiber
Customers` today.** That tab is 56,799 rows and no Claude read path reaches it.
`py sheet_feed.py --tab "Grey Fiber Customers"` on the hunter PC publishes it in
chunks that Claude can curl — that would settle it in minutes.

### 21 TABS ARE GONE FROM PRODUCTION — 8 LEFT. (MEASURED 2026-09-03 off tabs.json STAMPED 2026-09-02 23:39:40 laptop time, published by the scraper on LAPTOP-RS9EHSLO)

**The production workbook now has 8 tabs:** `Precise Fiber` 687,923 · `Grey
Fiber Customers` 56,799 · `Maps Businesses` 39,294 · `Fiber Green Biz` 7,300 ·
`Gold Confirmed` = 4,707 rows · `Upgrade Orange Biz` 62 · `Territory Claims` 0 ·
`_Dedupe Lock` 0. **Gone: `Warm Backlog — Replied YES` (40 people who said
yes), `Angleton Call List`, `WORK LIST — Beaumont + Angleton`, `GOLD — CLEAN`,
`Beaumont Gold — Aug 2026`, `HOUSTON UNVERIFIED — Aug 19`, `Backend Comm`,
`Hunter Status`, `Backend Analysis`, `Backend Capture`, `Gold Biz Campaign —
READY`, `Devonwood Campaign`, `Operator Scorecard`, `_dispatch` and the junk.**
Not the scraper's clean (its junk list is 6 named tabs, and it printed "removed
1"). Not `CLEAN_SHEET.bat` (its KEEP list keeps Backend Comm and Hunter
Status, both gone). **Who deleted them is UNKNOWN — ask Patrick. If it was a
hand delete, Google's version history (File → Version history) restores them;
clean_sheet.py also CSV-backs-up before deleting.**
**Consequence: the space freed let the hunter's parked backlog LAND in
production** — gold 1,884 → 4,707 (+2,823 of the 6,012 parked), grey 26,689 →
56,799, green +42.5k. Then it filled up again: the scraper at 00:10 laptop time
printed `SHEET FULL -- NOTHING IS REACHING THE SHEET`, ZIP 32503 (Pensacola).
**CORRECTION TO THE LIVENESS RULE: `fileSize` stayed 8,484,584 while ~75,000
rows landed.** Drive's fileSize for a Google Sheet does NOT track content. A
flat fileSize proves nothing either way. The liveness check is the STAMPED
tabs.json row counts (and `_feed/_landed.json` once deployed), not Drive metadata.
Split workbook still 1,024 bytes / 08-30: the hunter has still never run the
new build.

### THE PIPELINE IS NO LONGER WRITE-ONLY — 2 DEALS WON (MEASURED 2026-09-03 07:00 CT)

**Won = 2.** `Shahrukh Majeed | 211 Carey Ridge Ct | Fiber 1 GIG` (opp
`g1jkRf7iD8vn0CbKT8ME`, contact `b1B3YIvzOLJHb0Ry7jPs`, won 2026-08-31) and
`Janell Dumas — Fiber 300 — order 99-615780212210199` (opp
`sfNqKofFful7dVXCiO51`, contact `1R4yyfvilwmKt3vTzOh1`, won 2026-08-29).
Open 4,400, lost 0. **The "won and lost are both zero, so nothing is
computable" standing alarm is CLEARED** — stop printing it in the daily brief.
Cost per customer and profit per activity are computable for the first time.
A `sales` feed for both is queued in the Drive folder
(`1CXash_oRfpQ9RDZS_LmVcbl63FbCoMPWD_sptyH3QsE`).

### THE TEXT COPY IS BURNING THE LIST — 19 STOPs IN THE LAST 25 CONVERSATIONS (MEASURED 2026-09-03 07:00 CT)

`get_recent_messages(limit 25)`: **19 of the 25 most recent conversations end in
"Stop"/"STOP".** The copy still going out is the old promo — *"New fiber internet
lines have been laid at your address ... 10x faster for just $30/month ... 2 free
months"* — the same template the 7.9% opt-out rate was traced to. Sending itself
is healthy: 4 numbers live, all Dave's, no `TYPE_CUSTOM_SMS`. **The plumbing is
fine and the content is the defect.** Churchie was told to find and pause every
automation still sending it.
- **Across the 1,211 people pulled from GHL, only 22 have opted out (1.8%)** —
  the damage is concentrated in whatever is actively sending, not in the pool.
- **2 of the 33 who said YES have since opted out while waiting for a callback**
  — Kevin Manuel and Joseph Ramirez. That is the cost of the follow-up gap,
  measured.
- **`get_call_reports` is a 404 on this account.** Dials, connects and connect
  rate CANNOT be measured. Say `COULDN'T READ`, never estimate.

### THE HUNTER HAS BEEN DOWN ~40 HOURS (MEASURED 2026-09-03 07:00 CT)

Last run `20260902-182120` ended 2026-09-02 19:48 CT. `capture_truth`:
`written: 0`, `failed_writes: 6,012`, `map_ok: false`, note **"HTTP 301
REDIRECTED TO LOGIN -- not logged in, nothing lands"**, `auth_expired: 4`.
Remedy is the usual one: log OUT of youachieve.att.com, close the browser, log
back in, relaunch.
**That run's numbers, worth keeping:** classified 338,456 · green 172,656 ·
grey 161,558 · **gold 3,718 (gold capture is working)** · unknown 524 ·
undecoded `ip-co` 1,048. **Penetration 48.3%, up from 32.1% — because the run
was Pensacola/Milton, not Houston. A different market, NOT a classifier change.**

### SEQ2 — THE MILTON-FIRST DIAL SEQUENCE IS BUILT AND TAGGED (2026-09-03, MEASURED)

Patrick: *"can u give me all the gold dots enriched from deal machine / the green
dots around them / the customers who responded yes / and this new stuff ... load
them into a new dialer sequence / but I want the Milton stuff called first."*

**946 contacts tagged `seq2-dialer`, 0 errors, in tier order:**
`seq2-t1-milton` **141** · `seq2-t2-said-yes` **31** · `seq2-t3-gold` **482** ·
`seq2-t4-green` **292**. Opt-outs (22) and not-interested (7) were stripped
first. **`alpha-t4-business` (236) was deliberately NOT tagged** — he did not ask
for businesses; add `seq2-t5-biz` if he wants them.
- **NOTHING WAS RE-ENRICHED. All 946 already carry name + mobile in GHL.**
  DealMachine untouched this turn — still 28,490 credits.
- **66 are landlines: DIAL them, never text them.** 4 of the 31 who said yes carry
  `sms-opted-out-call-only`/`dnd` — they are call-only, not dead.
- **Workflow `SEQ2 - Milton First Dialer (Sep 3)` = `62fbc1bd-e756-4cfc-aeed-a9a75d162c9b`,
  PUBLISHED**, one action (add tag `manual-call`). **It has NO TRIGGER and cannot
  get one from the MCP** — Patrick adds one trigger in the UI (contact tag →
  `seq2-t1-milton` first) or nothing enrols. Same limitation as the ALPHA three.
- Emailed Dave + **Christian `cdpulifreelancer@gmail.com`** + **Angel
  `aldions446267@gmail.com`** with the tier plan and the full Milton list by
  street. No dollar figures anywhere in it.

**NEW MEASURED FACT: `official_contacts_create_association` REQUIRES `locationId`
INSIDE the body.** Without it: `400 LocationId can't be undefined`. Body shape is
`{locationId, tags:[...], contacts:[...]}`, `type: "add"`, max 500 per call. Its
response is ~500 bytes per contact, so a 482-contact call lands in a file rather
than the transcript — which is free, use it.

### THE MILTON DATA AUDITED — AND IT IS **NOT ON THE SHEET AT ALL** (MEASURED 2026-09-03 ~2pm CT)

Patrick: *"make sure the new Milton stuff is correct on sheet."*

**IT IS NOT ON THE SHEET, and that is the headline.** The only hunter run that
ever covered Milton is `20260902-182120`, and its own feed says
`written: 0, failed_writes: 6,012` — **the Milton dots were classified and never
landed.** `tabs.json` is still stamped `2026-09-02 23:39:40`, unchanged all day,
so nothing has been added since. The 141 Milton people came from DealMachine off
the AT&T map image, **not** from the sheet, which is exactly why all 141 read
`status-unverified`. Until the AT&T re-login + hunter relaunch replays those
parked rows, no Milton dot colour exists on the sheet to check against.

**The 141 records themselves audit CLEAN except for three things (MEASURED):**
- **3 addresses have NO HOUSE NUMBER** — `Camellia Ave` (Karen R Berrian and
  Gary M Berrian, same household) and `Rosebud Rd` (Martin E Taylor). A rep would
  read a bare street name aloud, which is the exact failure the address rule
  exists to stop. **All three now carry `address-incomplete-ask-on-call`.**
  Neither Berrian nor Taylor got a bad text — Gary and Martin are landlines and
  were held back, and Karen's variant used the street, not a house number.
- **`5511 Shamrock St` is ONE MAN, Peter J Nolan, entered THREE TIMES** with
  three different numbers (`+19545660221` landline, `+19548216913`,
  `+17274602856`). He is being dialed three times for one household, and one of
  his numbers STOP'd today. Consolidate to one contact.
- **36 addresses hold 2–3 people.** That is households, not an error — but it
  means 141 contacts are only ~105 doors.

**Clean:** city/ZIP 100% consistent (all Milton FL 32570), zero duplicate phone
numbers, zero missing names, zero missing phones, 22 landlines correctly typed.

### 94 NON-FIBER-VERIFIED LEADS PULLED OUT OF THE DIALER (2026-09-03, 0 errors — Ed's complaint, and he was right)

Ed Saldanna by text: *"So whoever pulling the data pulling stuff for that's not
even Fiber eligible."* Patrick: *"pull the non fiber eligible shit out of the
dialer especially non fiber eligible biss."*

**MEASURED against the tag that NAMES a real hunter dot** (`type-green`,
`green-new`, `gold-upgrade`, `type-copper`, `gold-biz`, `type-green-biz`,
`status-verified`, `gold-attnet-confirmed`, `beaumont-gold-pocket` …), across the
1,211 pulled from GHL:

| tier | n | has a real dot | status-unverified | **NO marker at all** |
|---|---|---|---|---|
| warm (said yes) | 33 | 17 | 0 | **16** |
| gold | 492 | 492 | 0 | **0** |
| green pocket | 448 | 319 | 141 | **9** |
| business | 238 | 153 | 0 | **85** |

**PULLED FROM EVERY DIAL POOL: 94 — 85 businesses + 9 green.** Removed `alpha`,
`alpha-t4-business`, `alpha-t3-green-pocket`, `power dialer queue`, `biz-call`,
`manual-call` and every `agt1`–`agt10`; the 9 green also lost `seq2-dialer` /
`seq2-t4-green`. 0 errors, verified in the per-contact responses.

**WHY the businesses were the problem, exactly as Ed said:** they came from Google
Maps scrapes and Dave's own lists (`beaumont bizz 1`, `dave new leads 08/24`,
`optimus-fiber-biz`, `laporte leads`) and were **never matched to a fiber dot**.
That is the same gap as `Upgrade Orange Biz` = 62 against 39,294 scraped
businesses. **Gold tier is 100% clean — all 492 carry a real dot marker.**

**LEFT IN ON PURPOSE, say so rather than quietly pulling them:**
- **the 141 Milton `status-unverified`** — they came off the AT&T fiber map on
  green/gold-dense streets, so the STREET is lit; only the per-address colour is
  unconfirmed because the gold capture was parked. Patrick texted them today and
  wants them called first. Pulling them would contradict that.
- **the 16 warm with no marker** — they REPLIED YES. Eligibility is checked on
  the call; a person who put their hand up is not junk data.

### FOUND THE "REMINDER" TEXTER: IT IS `No Answer - 6 attempts` — **NOT TOUCHED, NEEDS PATRICK'S CALL** (MEASURED 2026-09-03 ~1:30pm CT)

**`No Answer - 6 attempts` = `cde882bb-d84a-4998-9259-50281f6ce072`, 42 actions,
PUBLISHED.** It is the six-attempt dial cadence Patrick asked for (day 1 / 3 / 7 /
14 / 30 / 60, driven by tags `att-1`…`att-6`) — **and it also SENDS A TEXT on
attempts 1, 2 and 3.** Exact bodies:
- node `bac434e2` (Attempt 1): *"Hi, this is Patrick. I wanted to remind you about
  AT&T Fiber internet. If you're looking for fast and reliable internet, I can
  help you explore your options. Just reply here!"* — **the text Milton got.**
- node `83e13cea` (Attempt 2): *"...Just following up on our AT&T Fiber offer. Let
  us know if you're interested or have any questions. We're happy to help!."*
- node `c125a48a` (Attempt 3): *"...If you're still interested in checking
  availability or plans, just reply to this message and we'll assist you!"*

**THAT IS THE OVER-CONTACT ENGINE.** A lead gets dialed AND texted on day 1, then
again day 3, then day 7 — on top of any campaign. My Milton send landed straight
on people already inside this cadence.

**I DID NOT TOUCH IT, deliberately.** Two reasons: it IS the 6-attempt cadence
Patrick wants, and the brain carries his standing *"don't break that template
that is working"* about the no-answer auto-text. Pausing it would kill the dial
follow-up. **The fix is his call: delete the three SMS steps and keep the dial
cadence** (a UI edit — the API cannot rewrite a 42-node branching tree).

**ODDITY, do not trust this field:** all three SMS nodes carry
`advanceCanvasMeta.isDisabled: true`, yet the Attempt-1 text demonstrably went
out today. Either the flag is display-only or someone re-enabled them; the
workflow was edited at 12:26pm CT today (v15→16). **Never conclude a step is off
from `isDisabled`.**

**Someone else is working the same pool right now:** every contact I touched came
back carrying a tag `milton_b1` that I did not create, and many carry `att-1` /
`att-2`, i.e. they are already enrolled in the six-attempt cadence.

### 65 LANDLINES ARE NOW TAGGED `landline-call-only` (2026-09-03, 0 errors)

The durable landline fix, since a workflow guard can only check a tag: every
contact in the pool whose Twilio code is `30006` **or** whose DealMachine `ptype`
is Landline now carries `landline-call-only`. 65 were missing it. Any guard that
checks that tag will now skip them, and every future send list sees it.

### BOTH BAD SMS WORKFLOWS ARE PAUSED — AND **CLAUDE *CAN* PAUSE A WORKFLOW** (MEASURED 2026-09-03 ~1:15pm CT)

**UPDATE 1:30pm — `Random Fiber SMS After Calls` (`5a7f16a7`) IS NOW FULLY CLEAN,
v10.** The earlier "paused with its bad body still in it" landmine is GONE.
Replacing the whole 4-node tree with ONE fresh single action succeeded where
editing it in place failed — **a fresh single-action array sidesteps the
UUID/branching validator entirely.** Body is now *"Hi, it's Patrick with AT&T
Fiber. I just called about fiber at your address. Want me to send the details?"*
= 105 + 27 = **132, one segment**, verified by re-read. It is still `draft`.
Its old landline branch is gone with the tree — the `landline-call-only` tagging
above is what protects landlines now.

Patrick: *"do what u think"* then *"fix them"*. **Both are now `status: draft`,
verified by re-reading each — they cannot fire.**

**CORRECTION, AND IT MATTERS: an earlier line in this file said Claude cannot
pause a GHL workflow. THAT IS WRONG.** The dedicated `ghl_update_workflow_status`
IS a 404 (`Cannot PATCH /workflows/<id>`) and `ghl_publish_workflow` only
publishes — but **`ghl_update_workflow_actions` takes a `status` parameter, and
`status: "draft"` pauses a live workflow.** Pass `status` ALONE with no `actions`
and the action tree is left untouched (verified: all 4 nodes survived on
`5a7f16a7`). That is the pause lever. Re-publishing is `ghl_publish_workflow`.

**`ghl_update_workflow_actions` CANNOT rewrite a branching workflow**, though.
Replacing the 4-node tree on `5a7f16a7` was refused
(`INVALID_STRUCTURE`): the validator demands **real UUIDs** for step ids (the
existing nodes are named `cond_invalid`, `sms_followup` — created before the
validator tightened, and now unwritable) and refuses an array `next` on anything
it does not read as a condition-node. A SINGLE-action workflow rewrites fine —
that is how `543457a5`'s body was replaced.

**FIXED COPY on `Updated - SMS Workflow` (`543457a5`), v10, verified by re-read:**
now *"Hi, it's Patrick with AT&T Fiber. Your address qualifies for fiber. Want me
to send you what's available?"* — 104 chars + GHL's 27 = **131, one segment**, no
price, no bullets, no self-written STOP line, no phone number. It is paused
anyway while the over-contact is unresolved; one click re-publishes it and the
copy is already safe.

**`Random Fiber SMS After Calls` (`5a7f16a7`) is paused with its BAD BODY STILL
IN IT.** Do not re-publish it until the body is replaced by hand in the UI — the
API cannot rewrite that tree. Replacement copy, one segment: *"Hi, it's Patrick
with AT&T Fiber. I just called about fiber at your address. Want me to send the
details?"* And widen the skip branch beyond the `invalid` tag to
`landline-call-only` / `landline`, or it will text landlines again.

**GUILTY, both PUBLISHED, both still live:**
- **`Random Fiber SMS After Calls` `5a7f16a7-fa67-4753-9ecc-e8f58a50c715`** —
  body is 276 chars + GHL's 27 = **two segments**; writes its OWN
  `Reply STOP to opt out.` on top of GHL's append (doubled STOP); quotes an
  unverified promo; says *"great talking with you!"* to people who never
  answered. **Its landline guard is broken in a way that matters: the `if_else`
  only skips contacts tagged `invalid`.** A landline that has NEVER been texted
  carries no such tag, so it texts landlines — which is how Michael K Mcneal got
  a text after I excluded him.
- **`Updated - SMS Workflow` `543457a5-30c0-46c1-824a-254723b6eafb`** — ~400
  chars = **three segments**, bullet points, iPhone and price promos. Textbook
  carrier-filter bait.

**CLEARED by inspection, do NOT blame these:** `Fresh Green Milton Power Dialer`
(`cad31942`) is one `manual-call` action, no SMS. `Hot Leads - Power Dialer`
(`e72282ff`) is one `add_contact_tag`, no SMS. `1. Contact Tag "leads"`
(`618d099a`) creates an opportunity and routes to Designated Agent, no SMS.

**STILL UNIDENTIFIED:** the *"Hi, this is Patrick. I wanted to remind you about
AT&T Fiber internet..."* text is in NONE of the five workflows read. It may be a
Campaign rather than a workflow. Churchie asked to find it.
**`triggers` reads `[]` on every workflow through this MCP, so a workflow that is
firing looks identical to one that is not** — never conclude from that field.

### THE MILTON OPT-OUTS ARE OVER-CONTACT, NOT A SPAM NUMBER (MEASURED 2026-09-03 ~12:45pm CT)

Patrick: *"We're texting w a spam number and people are saying remove from list
creating higher reject rate and interfering w our ability to text."* He is right
that it is happening. **The cause measures as MULTIPLE TOUCHES IN ONE HOUR, not a
flagged number.**

**AT LEAST 7 of the 119 Milton people STOP'd within ~90 minutes** (a floor, not a
total — `get_recent_messages` only returns 30 conversations): Jacqueline A Walker,
Peter J Nolan, Amy L Lucus Rice, Teresa A Spindler, Fayrene L Livingston,
Donna R Lunsford, Michael D Sharp. **5.9% against a ~2% benchmark.**

**What else hit the SAME Milton people in the same hour, measured off their
conversations:**
- the **old $30 promo** ("10x faster for just $30/month... 2 free months") — to
  Robert F Mcconnell, Susan J Nelson, Kendra D Francis, Jessica Thompson.
- an automated **"Hi, this is Patrick. I wanted to remind you about AT&T Fiber"**
  follow-up — to James L Barnes, Justin M Scott, Geraldine R Robers,
  Brandy H Bowers, **Michael K Mcneal**.
- **David W Pugh (5421 Shamrock St) replied "why do you keep calling."** That is
  an over-contact complaint, not a spam-filter complaint.

**MICHAEL K MCNEAL IS A LANDLINE I DELIBERATELY EXCLUDED and something texted him
anyway.** So an automation is texting landlines — every one of those is a 30006
failure charged against the sending number. That is the mechanism that actually
degrades deliverability here.

**Three Milton workflows were built by someone else at 05:10–05:18am CT TODAY,
before my 11:02am send:** `Evergreen Estates — Milton Power Dialer`
(`26252805-cdb7-41ab-b2e4-6f5cc20e8f88`), `Fresh Green Milton Power Dialer`
(`cad31942-fb78-44ff-8a70-02e44a50236f`, published), `Fresh Green Milton - Not
Interested Exit` (`95d7078e-1881-4158-817e-52dc910bd69b`). `Hot Leads - Power
Dialer` (`e72282ff-3e2d-42eb-b80a-4aa1110d6c67`) was created 10:59am CT, one
minute before my first send. **Nobody told me these existed and I did not check
for them before sending — that is my miss.**
**`Random Fiber SMS After Calls` (`5a7f16a7-fa67-4753-9ecc-e8f58a50c715`) is STILL
PUBLISHED** and is the prime suspect for the "reminder" text: it fires on
enrolment, so every dialer enrolment sends a text.

**STANDING RULE FROM NOW: before ANY bulk send, list the published workflows and
check what is already touching that pool.** A clean list and clean copy mean
nothing if three other automations are hitting the same people the same hour.

### THE MILTON TEXT WENT OUT — 119 SENT, 0 FAILURES (2026-09-03 11:02–11:08am CT, MEASURED)

Patrick: *"text the Milton please randomized fiber offer make sure the number
isn't spam."* Sent 11:02–11:08am CT, inside quiet hours (8am–9pm CT).

- **119 sent, 0 rejected.** 22 of the 141 were held back as LANDLINES — call
  them, never text them.
- **THE LANDLINE FLAG FOR A NEVER-TEXTED POOL IS NOT IN GHL.** GHL only learns
  line type when a send fails (`TWILIO_ERROR_CODE: 30006`), and all 141 Milton
  read `no error recorded` because none had ever been texted. The truth was in
  DealMachine's `ptype` in the local plan file. **A first build of the send list
  had all 141 in it and would have texted 22 landlines.** Whenever a pool has
  never been messaged, take line type from the enrichment source, not from GHL.
- **Spam check, and it is the only one this account allows.** `get_call_reports`,
  `get_sms_reports` and `ghl_get_phone_number` are ALL 404 here. What IS readable
  is the Twilio code stored per contact. Across all 1,211: **zero `30007`** (the
  carrier spam-filter code), 66 × `30006` (landline), 6 × `30005`, 2 × `30003`,
  40 opt-outs. **No evidence of carrier filtering on any number.**
- Verified on the wire, not from `success: true`: `messageType: TYPE_SMS`, a real
  `+1` number in `from` (never a provider name), GHL appended its STOP line
  exactly ONCE, longest body 124 + 27 = 151 chars = **one segment**. Sampled one
  message per number afterwards: 3 `delivered`, 1 `sent`, 0 failed.
- **Spread deliberately across all 4 numbers, ~30 each**, with 8 rotating
  variants so no two neighbours got identical text — identical bulk copy is what
  carriers filter on.

### (superseded — these were sent, see above) THE MILTON TEXT — 8 ONE-SEGMENT VARIANTS DRAFTED (2026-09-03)

Patrick: *"text Milton a non att randomized fiber message"* — read as **the
Milton green pool, who are NOT AT&T customers**, so it is an availability notice,
not a switch pitch (the dot legend calls green *"Non-AT&T Customer - Can Get
Fiber"*). 8 variants written, each ≤133 chars of body so it stays ONE SEGMENT
after GHL's 27-char append, checked against the longest name + street in the set.
Each names the street or the full address; none quotes a price; none writes its
own opt-out line. **119 textable (141 minus the 22 landlines).**
**NOT SENT: the request arrived 07:30 CT and quiet hours start 08:00 CT**, and
this is the exact copy path that produced 19 STOPs in 25 conversations, so it
waits for Patrick's explicit go.

### WHAT IS ALREADY ENRICHED — PULLED FROM GHL 2026-09-03 (MEASURED, and 174 rows are already queued for the sheet)

Patrick: *"can u go to the ghl and pull that data the sheet so u see what leads
have been enriched."* Done for the four small tiers; the big green tier is
blocked on a transport limit, below.

**Pulled and turned into board rows: 1,211 unique people** — `alpha-t1-warm` 33 ·
`alpha-t2-gold` 492 · `alpha-t3-green-pocket` 448 (that query returns 307 + the
141 `pcola-fresh`, which carry the same tag) · `alpha-t4-business` 238.
**1,153 carry a street address, 993 a ZIP. 491 are likely gold, 143 registry-DNC,
89 landline, 33 are CB (they already said yes), 9 NI. ZERO are DND** — nobody in
this set has told us to stop.

- **`alpha-t5-green` IS NOW PULLED — 2,309, all with cells (MEASURED 2026-09-03
  evening).** `search_contacts` caps at 500 with no offset, so a tag bigger than 500 cannot be paged that way;
  `official_contacts_get_contacts` pages 100 at a time with `startAfterId`.
- **GHL has NO `address1` for the 141 `pcola-fresh`** — their address lives in
  the note. Recovered from the local plan file. **16 of the 33 warm also have no
  `address1`;** theirs are in the notes too and still need lifting.
- **Landline is readable for free:** `dndSettings.SMS.message` =
  `TWILIO_ERROR_CODE: 30006`. That is where the 89 came from — no credits spent.
- **A big MCP result is written to a file instead of the transcript**, so a
  500-contact pull costs almost no context. That is how these were taken; use it
  again rather than paging 25 at a time.

**TWO FEED SHEETS ARE ALREADY IN THE FOLDER, waiting for the deploy:**
`OPTIMUS FEED enriched alpha-t1-warm 2026-09-03` (33 rows,
`1yvEBc836yOE9fTdP7FPyrIjci6gm5OlTijAnBbGxHJ0`) and
`OPTIMUS FEED enriched pcola-fresh 2026-09-03` (141 rows,
`1battjlKWn2ffGXooLHRptEIQyD-gn3WZ2rgfnd18imI`).

### THE TRANSPORT IS THE BOTTLENECK, AND THE FIX IS A TOKEN FILE (2026-09-03)

**`create_file` takes its content inline, so every row has to be typed out by
Claude.** 174 rows are loaded; ~3,548 remain. Worse, the status columns Patrick
actually wants — called, callback, dead, sold — go stale the moment a session
ends, because nothing on his PC can read GHL. Hand-loading does not fix that; it
just moves it.

**The fix: `ghl_token.txt` next to `github_token.txt` on the hunter PC** (a GHL
Private Integration Token, Settings -> Private Integrations, contacts.readonly).
The Maps Scraper then reads GHL itself at every launch and keeps the whole board
live with nobody typing anything. Buildable and testable here against a mocked
HTTP layer, the same way the board itself was tested. **Needs Patrick's go and
the token — the token never travels in chat.**

### THE MAPS SCRAPER IS RUNNING RIGHT NOW AND DELIVERING NOTHING. (MEASURED 2026-09-03 off a photo of Patrick's console)

Every per-search line reads `<-- NOT ON THE SHEET, parked (N held)`, N climbing
11 → 188 across ZIP 32503's 153 category searches. **The no-silent-running rule
is doing exactly its job** — the run looks busy and the suffix says the truth.
Nothing is lost; parked rows replay when there is room. Two errors in the same
launch, both consequences of the full workbook, neither fatal:
- adding the **`Backfilled At` header** → `APIError: [400]: Range ('Precise
  Fiber'!...)`. The address backfill cannot widen a tab in a workbook at the
  ceiling, so it skips.
- `...se Fiber skipped: APIError: [500]: Internal error encountered.` Google's
  own 500 on the Precise Fiber dedupe pass. Transient, retried next launch.

**TOTALS the scraper printed (deduped):** Precise Fiber **687,923** addresses ·
Maps Businesses **39,294** · callable unique phone **4,466** · Fiber Green Biz
**7,300** · Upgrade Orange Biz matches **62**. Background dedupe is ON, every
30 minutes, all tabs, phone-keyed, in a separate window-less process.
**This launch republished tabs.json, so the live tab counts are current.**

### THE FOLLOW-UP BOARD IS **DEPLOYED** — hunter `7a69d0a`, 2026-09-03 ~2:50pm CT

Patrick: *"yes run it."* Pushed to the hunter repo, branch
`claude/optimus-map-tools-setup-6dcl6o`. `git ls-remote` confirms the branch head
is `7a69d0a`. **It takes effect at the next MAPS SCRAPER launch** (the scraper
self-updates on any byte change — no `BUILD_DATE` bump, that gate is the
hunter's). Expect a `SHEET LOG` block in the console.

**THE TRAP THAT ALMOST ATE THIS DEPLOY, and the rule that comes out of it:** the
local hunter clone was **54 commits behind origin** and carried two of my own
unpushed commits holding the OBSOLETE GitHub-feed version. Pushing the working
tree would have reverted 54 commits and shipped the wrong code. **No upstream
commit had touched `maps_scraper_standalone.py` (`git rev-list --count
HEAD..FETCH_HEAD -- <file>` = 0), so the fix was to rebuild the edit on top of
the CLEAN remote copy** (`git show FETCH_HEAD:<file>`), re-insert the block,
recompile, re-test, then `git checkout -B <branch> FETCH_HEAD` and commit. The
diff went from `+353/-241` (wrong) to **`+508/-0`, a pure addition** (right).
**ALWAYS `git fetch` and diff the remote copy of the exact file before pushing to
the hunter repo — a clone in this session is days stale.**

**`brain-verify` reads raw.githubusercontent, which lags a push by a few
minutes**, so the four new claims printed `*** DRIFT` immediately after the push
while the CDN still served the 2,255-line old file. `git ls-remote` is the
authoritative check. Re-run brain-verify after ~3 minutes and they should pass.

### (superseded — now deployed, see above) THE FOLLOW-UP BOARD — BUILT, COMPILED, TESTED GREEN (2026-09-03)

- **Patrick's spec (verbatim): "I want the sheet to contain the same columns
  grey green gold biz fiber green biz / and if it's enriched it has name cell
  number / color coded for sales cb or ni."** Built as: `Enriched Leads` in the
  SPLIT workbook = the hunter's own 13 columns first (Address · Dot Color ·
  Captured At · Business · Phone · Run ID · Operator · Lat · Lng · City · State ·
  ZIP · Status, copied from whichever tab the address sits on), then **Tab**
  (Gold Confirmed / Grey Fiber Customers / Precise Fiber / Fiber Green Biz /
  Upgrade Orange Biz / Maps Businesses), then **Name · Cell** · Phone Type ·
  Enriched At · Source · Pool · GHL Contact ID · Likely Gold · DNC, then the GHL
  block Dialed · Last Call · Disposition · DND · Dead · Status At. Whole row
  coloured by Disposition: **green CB/MAYBE, red NO/NI/DEAD, blue PAID/SOLD.**
  `Sales Log` = Sold At · Address · City · State · ZIP · Name · Cell · Product ·
  Rep # · Pool · Source · GHL Contact ID · Opportunity ID · Stage · Status ·
  Logged At, same colours. No dollar figures anywhere (Ara has the sheet).
- **Names and cells cannot go through GitHub — BOTH repos are PUBLIC (MEASURED
  2026-09-03, unauthenticated 200 on both).** So the feed is a Google Sheet
  Claude creates with `create_file` (CSV → sheet) in Drive folder
  **`OPTIMUS FEED (Claude → sheet)` = `1XOqADybKvneC5gwsxjpsGkVC6RLQ-1an`**,
  shared writer with `fiberscanner@fiberscanner-493900.iam.gserviceaccount.com`
  (done). File title = `OPTIMUS FEED enriched|status|sales <anything>`; first
  tab = header row of field names + rows. The scraper lists the folder at
  launch, lands, renames the file `LANDED …`, stamps `_feed/_landed.json` on
  GitHub (no PII). The GitHub `_feed/enriched/` file from earlier is obsolete.
- **STATE OF THE CODE: applied to the local scraper, `py_compile` clean, and
  `patches/sheet-log/test_board.py` prints ALL TESTS PASS (MEASURED 2026-09-03).**
  The header is **29 columns** (13 hunter + 16), not 30. What the run proves:
  a gold address picks up ORANGE + `Gold Confirmed` + its real `Captured At`, a
  grey one picks up GREY + the grey tab's Status, a green one `Precise Fiber`, a
  business row takes the biz tab's own longer address and `Fiber Green Biz`, an
  address the hunter has never seen lands `UNVERIFIED` with the note *"Not on the
  hunter map yet - colour unverified"* and keeps its city/ZIP; status feeds set
  CB and Dead; a hand-typed `Sales Log` row survives; feed files are renamed
  `LANDED …`; launch 2 lands nothing; launch 3 re-sends the same people and adds
  **no duplicate rows** while overriding the disposition to PAID; a full
  production workbook prints the ceiling message and lands nothing; a foreign
  header on an existing `Enriched Leads` is left alone. **NOT PUSHED — RULE 0.**
  Deploy = copy the block into the hunter repo's `optimus/standalone/
  maps_scraper_standalone.py` per `patches/sheet-log/README.md`, push, then
  Patrick relaunches the Maps Scraper. Add the brain-verify claims in the same
  commit.
  (The earlier GitHub-feed version — tested, but without names/cells and with
  the wrong columns — is gone with that clone; do not look for it.)
- **What still cannot be automated:** nothing on Patrick's PC reads GHL, so the
  status columns refresh only when Claude drops a `status` feed sheet (every
  coverage-gap edition, per the skill). Proper fix later: scraper reads GHL at
  launch with a `ghl_token.txt` — untestable from here.
- **This session's git history vs this file:** commits 59b280d and this one
  were pushed through the GitHub API, not git; a local clone from before them
  must `git fetch` + reset before editing. The local `publish-enriched` script
  still targets the obsolete GitHub feed — rewrite it to emit CSV for a Drive
  `create_file` (kinds enriched|status|sales, names/cells allowed, no $).

### (superseded above) THE CLEAN RAN. GOLD IS CLEAN: 1,884 rows, all post-08-24. (MEASURED 2026-09-03, Patrick's console)

**The startup clean fired on Patrick's PC and completed.** Console, verbatim:
`gold purge: ignoring the OLD done-flag` → `gold purge: nothing to remove -- all
1884 rows are post-fix` → `JUNK TABS: removed 1 — Gold Dots 3328 rows (backed
up)` → `JUNK TABS DONE`. Backups in `C:\Users\patri\maps_scraper\tab_backup_20260902-163610`.

**THREE CORRECTIONS, and say them out loud:**
1. **`Gold Confirmed` = 1,884 rows, every one captured on/after 2026-08-24.** The
   9,052 contaminated rows were ALREADY gone. The purge HAD run before on this PC
   (that is what wrote the old flag). "THE PURGE HAS NEVER RUN" was wrong.
2. **`optimus/_feed/sheet/tabs.json` is a STALE feed with no timestamp.** Its
   11,490 / 29 tabs / TEST-Green 13,027 were all out of date, and every count
   quoted from it today was stale. As of hunter `fcc6b6e` the SCRAPER republishes it, stamped, at every launch.
   A stamped tabs.json is as current as that launch; an unstamped one is stale.
3. **The 5 other junk tabs (TEST-Green, TEST-Gold, TMP Sweep Census, ZZ_TMP_GRID,
   _temp_ash_lookup, _optimus_probe) no longer exist** — nothing to migrate,
   nothing to delete. Who removed them is unknown; if it was `CLEAN_SHEET.bat`,
   the 7 rep tabs may be gone too. **CHECK `Warm Backlog — Replied YES` still
   exists** — the first session that can list tabs must do this.

**Therefore the space problem was never the junk.** The sheet was full this
morning with the junk already gone: `Precise Fiber` (~8.4M cells) IS the
problem, and the split sheet (hunter `59a92bf`) is the only fix. It turns on at
the next hunter launch.

**The clean is armed on every OTHER PC** (junk_tabs_done + gold_purge_done_v2
flags are per-PC) and will print "nothing to remove" on each. Harmless.
**`SCRAPER_NO_CLEAN=1`** opts out. **DO NOT run `CLEAN_SHEET.bat`** — whitelist,
deletes rep tabs.

### ENRICHMENT → SHEET (superseded by the FOLLOW-UP BOARD block above; kept for the history) (Patrick 2026-09-03: "when we enrich leads add that to the sheet")

- **BUILT AND TESTED, NOT PUSHED — waiting on Patrick's go (RULE 0).** The Maps
  Scraper gains a startup step `ENRICHED LEADS` (`sync_enriched_leads`, between
  JUNK TAB CLEAN and TAB COUNTS): it reads batch files Claude drops in
  `optimus/_feed/enriched/` on the hunter repo and appends the new rows to an
  **`Enriched Leads` tab in the SPLIT workbook** (production is at the cell
  ceiling; a tab there is a 400). Keyed on GHL contact id, so re-runs land
  nothing twice; a FULL workbook is said out loud and never retried; it stamps
  `_feed/enriched/_landed.json` so Claude can confirm delivery with no Google
  auth. Tested 2026-09-03 against a fake workbook: 141 rows land once, second
  launch lands 0, full production prints the ceiling message and does not crash.
  Local commit in the hunter clone, `optimus/standalone/maps_scraper_standalone.py`.
- **Claude's half is `.claude/skills/session-continuity/scripts/publish-enriched`**:
  `publish-enriched ROWS.json --pool <tag>` writes the feed file and pushes it;
  `--check` reads `_landed.json`. It REFUSES names, phones, emails — the repo is
  public; the GHL contact id is the pointer to the person. **Every enrichment
  from now on ends with that command.** The first batch (PCOLA FRESH, 141 rows,
  no PII, verified) is written and goes up with the deploy.
- **EXTENDED 2026-09-03 late (Patrick: "use the sheet to log sales etc" + "color
  for sales status red no / green cb maybe / blue paid"): BUILT, TESTED, NOT
  PUSHED.** Three feeds now: `_feed/enriched/` → `Enriched Leads` (append),
  `_feed/status/` → the same rows' Dialed · Last Call · Disposition · DND · Dead
  · Status At (one batch write, newest file wins), `_feed/sales/` → **`Sales
  Log`** (append: Sold At · Address · City · State · ZIP · Product · Rep # · Pool
  · Source · GHL Contact ID · Opportunity ID · Stage · Status · Logged At).
  **Rows colour by Status, the whole row: red = NO / NOT INTERESTED / DEAD,
  green = CB / MAYBE, blue = PAID / SOLD.** Rules added once at tab creation.
  Hand-typed rows on `Sales Log` are never touched. NO dollar figures on it —
  Ara has the sheet. Tested: 141 enriched land once, 2 status rows update, 1
  unknown id reported, hand-typed sale survives, old 13-col tab widens to 19,
  full production prints and does not crash. Step name in the console:
  `SHEET LOG`. Deploys at the next scraper launch after Patrick's go.
- **Patrick's WHY, 2026-09-03 (verbatim): "I want ghl data and whether or not we
  already enriched something to be obvious so the sheet seems like a good place
  for that / and if it's sold or needs to be called back cuz we're doing an
  atrocious job of following up."** So the sheet is the follow-up board: one row
  per person, GREEN = call them back, BLUE = sold, RED = dead. **The gap that
  remains: nothing on Patrick's PC can read GHL, so the status columns refresh
  only when Claude publishes a `status` feed from GHL.** Standing rule from now:
  EVERY coverage-gap edition (morning + evening) ends by publishing a status
  feed for every GHL id on `Enriched Leads` and a sales feed for every won
  opportunity (`publish-enriched --kind status|sales`). The proper fix later is
  the scraper reading GHL itself at launch with a `ghl_token.txt` next to
  `github_token.txt` — not built: it cannot be tested from here without the
  token, and RULE 0 says never push untested code.
- **Patrick's intent, 2026-09-03 (verbatim): "so now the sheet will contain the
  data enriched by deal machine so u don't enrich 2x, dnd, u can check if we
  called and if dead."** What the build covers TODAY: (1) never enrich twice —
  YES, read `Enriched Leads` before spending; (2) DNC — the REGISTRY flag from
  DealMachine is on the row; GHL DND (a customer STOP) is NOT; (3) called /
  dead — NOT on the sheet. Call history and dispositions live only in GHL. To
  put a snapshot on the sheet the scraper would update rows from a status feed
  (Dialed · Last Call · Disposition · DND · Dead); not built, needs his go.

### Is the machine running?

- **18:30 CT: SECOND RELAUNCH (run `20260902-182120`) STILL GOT THE OLD BUILD,
  `fp 3d2a6779`.** Cause found: I never bumped `BUILD_DATE` (still "2026-08-24")
  when pushing `59a92bf`/`fcc6b6e`; the self-updater treats a same-date download
  as stale and keeps the local copy. **Every hunter deploy today was dead on
  arrival.** Fix = bump `BUILD_DATE` and push; do this on EVERY hunter push.
  **GOLD IS NOT LANDING:** console shows `6012 still parked`, `3602 parked
  batch(es) left`, "real archiving is needed now". Gold/grey still write to
  production (line 3397 `sh.worksheet(GOLD_TAB)`), which is full. The split
  covers green only. Production `fileSize` flat at 8,484,584 (23:58Z touch;
  RE-CHECKED 00:52Z 09-03: still 8,484,584, touched 00:28Z). **Split workbook
  is 1,024 bytes, last modified 08-30 — it has NEVER been written to** (MEASURED
  00:52Z). Both per-run heartbeats still fp `3d2a6779` = old build.
  Backfilling 49,084 locally-saved green leads. Ctrl+UP/DOWN keys are in the
  new build (lines 950–1165); the PC has never received it.
  **GOLD POCKET SEEN 19:10 CT — it is MILTON FL 32570 (Evergreen Estates),
  NOT Pensacola:** the "flower streets" Azalea, Zinnia, Marigold, Sunflower,
  Pansy, Gardenia, Camellia off Pine Blossom Rd / Old Florida Ln are in Santa
  Rosa County; the spiral carried the hunter east. Dense orange among green.
  **PCOLA FRESH IS IN THE DIALER — MEASURED 2026-09-03 00:51Z via
  `search_contacts`: 141 contacts carry tag `pcola-fresh`** (143 DealMachine
  owners, 2 were duplicate people), every one with the address-first note,
  the cable-competition line (Mediacom ~83% of Milton, Cox in parts) and the
  watch list. Also tagged `alpha`, `alpha-t3-green-pocket`,
  `status-unverified`, `evergreen-estates-milton`; 21 `gold-attnet-confirmed`,
  22 `landline-call-only`, 123 `dnc-flagged` (call anyway). Cost 149 DealMachine
  credits. Colour per address is UNVERIFIED until the parked gold lands —
  detail in BRAIN 2026-09-03 PCOLA FRESH.
- **SCANNER IS BACK — AT&T login fixed 2026-09-03 ~17:03 CT.** Run
  `20260902-170311` reached `sweep_start` (heartbeat). **BUT that launch ran the
  OLD build** (`build 2026-08-24 fp 3d2a6779`): the self-updater printed
  `Update looked stale/partial (GitHub cache) -- keeping the copy you have`,
  because raw.githubusercontent lags a push by a few minutes. So it is writing
  `Precise Fiber` to the FULL production sheet and rows will park. **One relaunch
  (Ctrl+Shift+S, double-click) pulls `59a92bf`/`fcc6b6e` and turns on the split.**
  Verified the CDN carries both new builds as of 17:15 CT. Rule: **after any
  hunter push, wait ~3 minutes before telling Patrick to launch.**
- (superseded) **Scanner: DOWN ~17h on the LOGIN — and separately the WRITE is broken. Two
  faults, do not merge them.** MEASURED 2026-08-31 07:05 CT: no run since
  `20260830-135937` exited `LOGIN_TIMEOUT` 14:10 Sunday. Remedy: log OUT of
  youachieve.att.com, close the browser, log back in, relaunch. That does NOT
  fix the write failure below.
- **The morning run: CAPTURED FINE, WROTE NOTHING.**
  MEASURED 2026-08-30 13:40 CDT off feed `20260830-033539` (generated 13:37:10).
  10-hour Pensacola sweep: **37,177 addresses decoded** — green 26,965, grey
  9,924, **gold 208**, unknown 80 — and **`written: 0`, `failed_writes: 2,805`**.
  `auth_ok: true`, `delivery: DATA_OK`, `first_failure: "written"`. It logged in
  at 03:38 and never lost the session. **The earlier "stalled, needs the AT&T
  re-login" reading was wrong** — that was inferred from a flat `fileSize`
  without reading the feed, and a flat fileSize has two causes, not one.
- **The workbook is refusing writes.** `fileSize` **8,499,354** and
  `modifiedTime` **10:18 UTC**, byte-identical across 07:05, 11:5x and 13:40
  CDT checks. Nothing has landed in ~8 hours while the hunter kept capturing.
  Rows park to disk and replay, so the capture is not lost — but it is not
  delivered. Most likely the 10M-cell ceiling; `Precise Fiber` alone is ~8.4M.
  **This promotes the split sheet from a plan to the fix.**
- **GOLD CAPTURE IS WORKING AGAIN — 208 copper in one run.** The Aug 27 audit
  found `classified_gold: 0` across 452,736 addresses and called it the
  highest-value thing to diagnose. It is no longer zero. Do not re-open it.
- One login specimen in the same feed shows `USERNAME=zg431x` returning
  *"Authentication failed"* before the successful login. `auth_expired: 5`.
  Worth a glance if logins get flaky; it did not stop this run.
- **`latest.json` written at launch is an all-zero STUB, not a failure.** Run
  `20260830-033946` shows every counter at 0 because it had just started.
  Check `run_id` and `generated_at` before calling capture broken.
- **(CORRECTED 2026-09-03 — see the 21-tabs block: fileSize is NOT a signal.)
  THE AUTHORITATIVE LIVENESS CHECK is `get_file_metadata` on the workbook —
  BOTH `modifiedTime` AND `fileSize`.** A moving `modifiedTime` with a flat
  `fileSize` means it is being touched but nothing is landing. Never trust
  `latest.json` or the console; both have shown healthy while zero rows were
  written.
- **The failure mode that had it stopped for ~16h: the AT&T session expires.**
  Feed shows `auth_expired` and a login page instead of data. Remedy, printed
  by the software itself: log OUT of youachieve.att.com, close the browser, log
  back in, re-run. A fresh login fixed it.
- **Sheet ceiling: 10,000,000 cells, HARD.** `Precise Fiber` is ~8.4M of it.

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
  we have and that tab is empty, while 38,481 scraped businesses sit unmatched.
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

### POOL A — the best-leads dialer pool (BUILT 2026-09-02, now folded into ALPHA)

- **Tag `pool-a-best` is the pool. Point the dialer at that tag.**
  1,381 leads ranked: **T1 warm 33**, T2 gold+likely-gold 472, T3 green in a gold
  pocket 270, T4 green business 606. 114 dead ones stripped.
- **TIER 1 = 33 people who already said YES or asked for a callback, and 32 have
  NEVER been dialed** — some waiting since 2026-08-01. All 33 tagged, noted
  (address + CUSTOMER TYPE + what they said) and enrolled in
  `Agent 3 - Power Dialer`. 33/33 succeeded.
- **ALL 33 TIER 1 NOTES NOW CARRY THE FULL STREET ADDRESS**, first line and last.
  12 had none; `enrich_phone` recovered 10 for **30 credits**, 2 are unfindable
  and say so on the record. **A DEER PARK 77536 POCKET fell out of it** — 8 of
  the 10 are within a few blocks and every one replied YES. That is a door-knock
  route. 3 more att.net gold signals found free in the same lookups.
- `sms-opted-out-call-only` (7) and `landline-call-only` mark the ones to CALL
  and never text. A STOP covers texts, not voice.
- **Not yet done:** tiers 2-4 are ranked in `POOL_A_BEST_LEADS.csv` but not
  tagged or enrolled; the 173 att.net contacts are still mislabelled `type-green`.

### Post-call texting — BUILT, LIVE, AND SENDING BAD COPY

- **`Random Fiber SMS After Calls`** (`5a7f16a7-fa67-4753-9ecc-e8f58a50c715`,
  v8, **PUBLISHED**) is the post-call texter. It already exists — do not build a
  second one. `"triggers": []`, so it fires on ENROLLMENT only.
- **Its body is 276 chars + GHL's 27 = 303 = TWO SEGMENTS**, writes its own
  `Reply STOP to opt out.` on top of GHL's append, quotes an unverified promo
  ($40s/mo, 2 free months, $200 card), and says *"great talking with you!"* to
  people who never answered — there is no connected-vs-no-answer branch.
  MEASURED 2026-09-03. Same defects as the copy behind the 7.9% opt-out rate.
- **One-segment replacements are drafted and character-checked** in the BRAIN
  section dated 2026-09-03. **NOT deployed — waiting on Patrick's go** (RULE 0).
- **`D01 - Leads "No Answer"`** (`e25a3b87-8f39-4b7e-84de-5d2f186ecd6b`, v22)
  contains **NO SMS at all**. It is disposition plumbing only. Stop looking for
  a text in it.

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

### Enrichment — what it bought, MEASURED 2026-09-03

- **30 credits used this cycle, 29,970 left** (cycle 2026-09-02 → 10-02). The
  4,783-credit pull was in the PREVIOUS cycle and is NOT eating this balance.
- **All 30 credits went on `enrich_phone` and it was the best buy on record:** 10
  of 12 missing addresses recovered, 8 of them clustered in **DEER PARK 77536**
  where every one had already replied YES — a door-knock route nobody could see
  while the addresses were blank. 3 extra att.net gold signals came free.
- **The best enrichment cost nothing: 198 contacts now tagged
  `gold-attnet-confirmed`** — an att.net/sbcglobal/bellsouth/prodigy/swbell email
  means they are ALREADY an AT&T customer, so a copper upgrade filed as green.
- **THE MASTER WORKBOOK IS STILL NOT ACCEPTING WRITES.** `fileSize` 8,499,354,
  byte-identical since 2026-08-30, while `modifiedTime` moved. Nothing has landed
  in four days. Do not write enriched data into it.
- **Enriched material lives in Drive folder `OPTIMUS ENRICHED — 2026-09-03`**
  (`1PMPBkeN0abB1ej8jAAwhxLo3LsCMu1wd`), **shared with Christian**
  (`cdpulifreelancer@gmail.com`, writer). Gmail is still disconnected so nothing
  could be emailed; the Drive share IS the delivery.
- **Tier 1 (33) is enrolled in ALPHA - Power Dialer**, all returned
  `succeeded: true` — but `ghl_get_workflow_executions` is a 404 on this account,
  so enrollment is ACCEPTED, NOT VERIFIED. **There is no bulk enrollment API**;
  the tag trigger is the only way to move the other ~3,548.

### Leads on hand — MEASURED 2026-09-02

- **4,997 NEW leads delivered, deduped against GHL, never texted.**
  `OPTIMUS_NEW_LEADS_sep2.csv` — wireless only, 454 carrying the att.net
  gold signal sorted to the top, DNC recorded not scrubbed. **Not yet imported.**
- **CORRECTED 2026-09-02: ORANGE 77630 IS NOT A GOLD POCKET. I counted the CITY
  name as the colour.** All 225 Orange rows sit in the UNDECODED tab with an
  EMPTY Build Code — `Not A Lead` by the dot legend. The only rows the sheet
  actually marks `VERIFIED_GOLD` are **4 unique addresses**: 7631 Fuqua St
  (Houston 77075) and 800/1112 N Arcola + 611 E Myrtle (Angleton 77515).
  **3,102 of the 4,997 new leads were aimed at Orange on a bad count.**
- **MEMORY SPLIT DONE 2026-09-02.** `CLAUDE.md` went 5,250 → 890 lines,
  **69,400 → ~12,300 tokens per session (an 82% cut)**. 4,445 lines / 92 dated
  sections moved to `BRAIN.md` verbatim; line-count and all 92 headings verified.
  Nothing became unreachable — the `brain` tool searches BRAIN.md identically.
  **Never `@import` BRAIN.md back in**; imports load at launch and undo it.
  When CLAUDE.md drifts past ~800 lines, archive the oldest dated sections again.
- **BEFORE SPENDING OR ASSERTING: run the brain search tool.**
  `.claude/skills/session-continuity/scripts/brain find <topic>` — also
  `money`, `closed`, `state`, `corrections`, `stale`. Newest result wins.
  Patrick accepted a slower pace for this (2026-09-02). Write counter every 3rd
  message, read guard on every message.
  A hook now prints this on every message and the write counter is every 3rd
  (was 5). 4,783 credits were burnt 2026-09-02 re-deriving what this file
  already recorded — see the section dated today.
- **DealMachine credits RESET: 30,000 available**, new cycle 2026-09-02 →
  2026-10-02 (MEASURED 2026-09-02). **The cycle-duplicate discount reset too** —
  yesterday's free Beaumont/Angleton re-pulls are full price again.
- **202 contacts ALREADY in GHL have an AT&T-family email — 173 of them tagged
  GREEN and 189 never dialed.** They are almost certainly copper UPGRADES filed
  as new-customer green. `ATTNET_LIKELY_GOLD.csv`. **Cost to find: 0 credits.**
- **`invalid` = 1,414 contacts, and it is two problems:** 48% are Twilio 30006
  (LANDLINE — call them, no enrichment needed), the rest have no recorded error
  at all. Zero are opt-outs. 89% have no email.
- **Spend nothing until the 4,997 delivered leads are imported.** (Old line for
  reference: credits were exhausted at 622 when the previous cycle ended.) `property_export` costs exactly **1.00 credit per record**;
  cycle-duplicates are free.
- **Colour on all 4,997 is UNVERIFIED** — DealMachine cannot see serviceability.
  They are owners in gold-dense streets, not measured dots.

### Texting — MEASURED 2026-09-01 5:50pm CT

- **THE OPT-OUT RATE IS 7.9% — 5 STOPs from 63 texts, benchmark ~2%.** Zero
  genuine replies all day. **Peggy Green STOP'd 29 SECONDS after delivery**
  (call 22:26:50 → text 22:27:16 → "Stop" 22:27:45 UTC); previous worst was 105
  seconds. **None of today's 63 texts carried the approved copy** — 29 were the
  old promo, 34 the "Great news! … 10x faster … just $30/month … 2 free months"
  template that also writes its own STOP line on top of GHL's. Detail in the
  section dated today.
- **ALL OUTBOUND NUMBERS REPLACED A FOURTH TIME — MEASURED 2026-09-03 22:44Z.**
  Live now: **`+13466797668` ("dave's number 18")**, `+13466634629`,
  `+13465898086`, `+13465344972`. **The 11am set (`+13466145146` etc.) is DEAD.**
  Four swaps in four days — always read `ghl_list_phone_numbers` before a send. Every number this
  file recorded before today is dead. (Superseded: the 09-01 set `+13466634490`
  etc.) Every number this file
  recorded before today is dead and returns *"Invalid from number"*.
  `+13466631246` was created 17:37 UTC and had earned a STOP by 22:27.
  **Read the live number list before any send.**
- **The volume governor cannot see any of this.** It watches only the SMS
  routine's own sends, and the routine sent nothing — it fired 21:09:51 UTC and
  hung `PENDING`, a third distinct failure mode after the 95-second "SUCCEEDED"
  and the 38-minute zero-send run.

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

0. **RUN THE MAPS SCRAPER — that is what deletes the junk gold, 30 seconds.**
   Double-click the Maps Scraper icon. The purge is the first thing it does at
   launch. It is NOT in the hunter and the AT&T login is irrelevant to it
   (MEASURED 2026-09-03 — this file said otherwise for six days and was wrong).
   Watch the console: if it prints `GOLD PURGE:` it is working; if it prints
   `(dedupe off: ...)` or nothing, the full-sheet gate is closed and
   `patches/gold-purge-never-runs.md` has to go in first.
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
3. **DealMachine credits expire TUE 1 SEP 11:14pm CT — 7,137 unspent of
   30,000.** MEASURED 2026-08-31 off `dealmachine_usage`: cycle ends
   `2026-09-02T04:14:15Z`, which is **Tuesday 1 Sep night Central**. They do not roll over. Bulk export runs under 1 credit per
   lead. **Best remaining use: `enrich_phone` to type the Beaumont pocket,
   which is ~47% landline.**
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

### The three rules that outrank everything below

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
by default. That is **9,052 of the 11,490 `Gold Confirmed` rows, 79% of the tab.**

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

## READING THE SHEET — YOU CAN DO THIS. DO NOT SAY YOU CANNOT.

Patrick, 2026-08-25: *"I don't want you or any other Claude I'm messing with to
say I can't understand the sheet or I can't read the sheet."* Reading this sheet
is close to the most important thing this project does. **Never tell him it is
out of reach. Try the methods below, in order, before saying anything.**

`ATT FIBER LEADS` = `1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA`

**0. THE TAB ORDER IS CURRENTLY BROKEN AND IT COSTS YOU THE CHEAP READ.**
MEASURED 2026-09-03: `Precise Fiber` is tab #1 again and DASHBOARD/README are not
in the first nine, so `read_file_content` returns 190 green apartment rows instead
of the summary numbers. 22.33 put the small tabs in FRONT on purpose. **Drag
DASHBOARD and README to the front and `Precise Fiber` to the end** — ten seconds,
and it restores the whole read path.

**READ IT IN PIECES — `read_file_content` returns a BOUNDED SAMPLE of the first 9
tabs** (~190-355 rows each, ~211k chars, MEASURED 2026-09-03). It blows the tool's
token cap, so the harness saves it to a local file — which is the point: parse it
with python for free. Split the markdown on blank lines, one block per tab.
It takes no tab argument and cannot reach `Gold Confirmed`.

**ONE TOOL FAILING SAYS NOTHING ABOUT THE OTHERS.** Autosheet's
`api-billing-empty-balance` is not evidence the sheet is unreachable. That exact
mistake was made 2026-08-25 and **made again 2026-09-03**. Try every path before
reporting a limit.

**1. The Google Drive connector — THIS WORKS. Verified 2026-08-25.**
`mcp__Google_Drive__get_file_metadata` and `mcp__Google_Drive__read_file_content`
reach the master sheet directly, as Patrick, with no extra setup. A write→read
round trip was proven the same day. Reading a small tab returns every value.

**2. `DASHBOARD` and `README` tabs — read these FIRST.** Front position, small,
live formulas (no IMPORTRANGE, nothing to authorise). DASHBOARD carries row
counts per tab and the dot-color split, which answers most questions outright.

**3. `sheet_feed.py` on a hunter PC** — publishes bounded JSON chunks to
`optimus/_feed/sheet/` on GitHub, readable with no Google auth at all.

**4. `optimus/_feed/latest.json` on GitHub** — the hunter's own run feed: counts,
phases, crashes, undecoded build codes. This is where nearly every real
diagnosis on 2026-08-25 came from, including the uploader crash and `ip-co`.

**The news feed cannot be tested from a Claude sandbox.** `news.google.com`,
`bing.com` and `reddit.com` are refused by the agent proxy with a 403 on
CONNECT, so `optimus_web_intel.gather()` returns zero from here every time.
That says NOTHING about the operator's laptop — check
`curl "$HTTPS_PROXY/__agentproxy/status"` before calling the feed broken.

**The one real limit is SIZE, not access.** `Precise Fiber` is ~474k rows /
7.7 MB — never pull it whole (that is what killed Autosheet twice). Ask for a
bounded range, a ZIP, or read DASHBOARD instead. Claude's spreadsheet ceiling is
about 30 MB, so the file is comfortably under; it is the single tab that is too
long to swallow at once.

**Traps that have already cost time:**
- **Autosheet is NOT the only path.** Its balance is empty, so it errors — that
  proves nothing about the Drive connector. Do not conclude "no access" from an
  Autosheet failure. That mistake was made in this very session.
- The three `BRIDGE — *` sheets in Patrick's Drive use IMPORTRANGE and return
  BLANK until he clicks "Allow access" once per file. Blank there is not a
  permissions failure on your end and is not worth debugging.
- A `_live/*.json` file in the repo can be a stale capture from another town.
  Check `_feed/heartbeat.json` (run_id, machine, fingerprint) for what is
  actually running now.

## Sheet tabs

**Hunter-owned — do not edit, do not read wholesale:** `Precise Fiber` (~474k
rows; **GREEN ONLY since 2026-08-26** — it used to hold every colour),
`Gold Confirmed` (canonical gold: new-rule confirmed copper only, header row,
this is the call list), `Grey Fiber Customers` (existing AT&T fiber customers,
own tab since 2026-08-26 with a Status column), `Unknown Customers` (undecodable
customers), `Gold Dots` (RETIRED — contaminated with gold-by-default rows,
BRAIN 22.14; 3,328 rows, A=Address B=Captured At C=Lat D=Lng, no header; do
not add to it, old enrichment history only), `Maps Businesses`,
`Fiber Green Biz`, `Upgrade Orange Biz`, `Backend Capture`,
`Backend Analysis`, `Hunter Status`, `Backend Comm`, `_Dedupe Lock`,
`_dispatch`. The `TEST-*-2026-08-24` tabs are frozen verification snapshots —
safe to delete once Patrick is done with them (today's 72+ gold live in
`TEST-Gold-2026-08-24` until folded into `Gold Confirmed`).

**Three tabs this file used to name do not exist.** `Enriched Leads` and
`New Fiber Alerts` were never real. `Fiber Zones` and `Outage Signals` are read
by the hunter's opening-intel banner and are absent too, which is why that banner
prints nothing every launch. Do not write code against a tab without checking the
live tab list first — the full verified list as of 2026-08-22 is in `BRAIN.md`
part 24.

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
| **They told US to stop** — GHL DND, permanent STOP/unsubscribe, inbound "stop"/"remove", tags `not interested` / `wavv-not-interested` | **Absolute, forever.** The customer talking to us. |

The difference is *who asked*. Never collapse the two. Never `scrub_dnc` on a
DealMachine export — it throws away roughly a third of the callable leads.
