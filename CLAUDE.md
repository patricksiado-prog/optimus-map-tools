# Optimus — operating brain

Claude Code loads this file automatically at the start of every session in this
repo. **Read the CURRENT STATE block below first — it is the only part that
claims to be true right now.** Everything under it is the historical record,
appended newest-at-the-bottom. Where two sections disagree, the later date wins
and you say so out loud. Long-form detail lives in `BRAIN.md`.

---

# CURRENT STATE — updated 2026-09-03 00:20 CDT

**Update this block whenever any line in it changes, in the same turn.** A
finding buried 2,000 lines down in the log is a finding nobody will read. This
block is short on purpose; if a line needs more than two sentences, put the
detail in a dated section below and point at it from here.

Mark every line **MEASURED** (with how and when) or **ASSUMED**. Never let the
two share a voice — that is the mistake that let "register for the 20M-cell
beta" survive four sessions unchecked.

### Is the machine running?

- **Scanner: DOWN ~17h on the LOGIN — and separately the WRITE is broken. Two
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
- **THE AUTHORITATIVE LIVENESS CHECK is `get_file_metadata` on the workbook —
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

- **`Gold Confirmed` = 11,490 rows, but only ~2,438 believed real (21%)** —
  MEASURED 2026-08-27 via `optimus/_feed/sheet/tabs.json`, **now 6 days stale**
  because the scanner is down. The other 9,052 are pre-08-24 gold-by-default
  decode failures; the purge may not have run.
- **Rows are not dots.** 170 `VERIFIED_GOLD` rows in a sample were **4 unique
  addresses**. Treat any row count as an upper bound on unique gold.
- **296 gold contacts in GHL** (MEASURED 2026-09-01, unique) — the only gold
  number that is both current and de-duplicated.
- **`Upgrade Orange Biz` = 62 rows.** Gold businesses are the highest-value slice
  we have and that tab is empty, while 38,481 scraped businesses sit unmatched.
- Full census in the BRAIN.md section dated 2026-09-02.

### POOL A — the best-leads dialer pool (BUILT 2026-09-02)

- **Tag `pool-a-best` is the pool. Point the dialer at that tag.**
  1,381 leads ranked: **T1 warm 33**, T2 gold+likely-gold 472, T3 green in a gold
  pocket 270, T4 green business 606. 114 dead ones stripped.
- **TIER 1 = 33 people who already said YES or asked for a callback, and 32 have
  NEVER been dialed** — some waiting since 2026-08-01. All 33 tagged, noted
  (address + CUSTOMER TYPE + what they said) and enrolled in
  `Agent 3 - Power Dialer`. 33/33 succeeded.
- `sms-opted-out-call-only` (7) and `landline-call-only` mark the ones to CALL
  and never text. A STOP covers texts, not voice.
- **Not yet done:** tiers 2-4 are ranked in `POOL_A_BEST_LEADS.csv` but not
  tagged or enrolled; the 173 att.net contacts are still mislabelled `type-green`.

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
- **ALL FIVE OUTBOUND NUMBERS WERE REPLACED AGAIN 2026-09-01** — second full
  swap in 26 hours. Live now: **`+13466634490` (DEFAULT)**, `+13466603376`,
  `+13466632307`, `+13466631246`, `+13466631510`. Every number this file
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

### Blocked on Patrick — nothing moves until he does these

1. **SPLIT SHEET — share DONE, ONE STEP LEFT, and only Patrick can do it.**
   The sheet is shared with the service account. The hunter cannot be told about
   it from a session: **`git push` to the hunter repo is now classifier-blocked,
   scratch branch included** (the PR route that shipped #7–#11 is dead). Either
   (a) create `~/optimus/optimus_sheet_id.txt` on the hunter PC holding
   `1DXu-nuQvVKrqQVk8LDNwLztG31ddi6sAyo8vXDFKcmQ` — 30 seconds, but leaves the
   8-vs-13 column bug live, so add a 13-column `Precise Fiber` tab to the split
   workbook first — or (b) make the two-line `PF_SPLIT_SHEET_ID` edit in
   GitHub's web editor, which fixes both on every PC. Patch tested locally,
   commit `ad9ae65`. Wire it while the sweep is idle.
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
- **Business cross-match is a 1-line `ValueError`**, fix written, NOT deployed.
  `patches/scraper-crossmatch-fix.md`.
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
```

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

## READING THE SHEET — YOU CAN DO THIS. DO NOT SAY YOU CANNOT.

Patrick, 2026-08-25: *"I don't want you or any other Claude I'm messing with to
say I can't understand the sheet or I can't read the sheet."* Reading this sheet
is close to the most important thing this project does. **Never tell him it is
out of reach. Try the methods below, in order, before saying anything.**

`ATT FIBER LEADS` = `1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA`

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
