# Optimus BRAIN

_Last updated: 2026-08-20. **This file is the single source of truth.**_

---

# ============ READ THIS FIRST ============

**This one file is the brain.** It lives in three places and they must not diverge:

| Where | What |
|---|---|
| **git — `patricksiado-prog/optimus-map-tools`, `BRAIN.md`** | **the master. Edit here.** |
| Drive — `BRAIN_delta_<date>_<topic>.md` | per-session deltas, for reading on the phone |
| this session's memory | working copy only, gone when the session ends |

If they disagree, **git wins.** Do not start a second brain file, a notes doc, or a
"summary" — append to this one.

## The loop, every session, no exceptions

**REPO → LOG → BRAIN → THINK → ACT → RECORD**

1. **READ THIS FILE BEFORE ACTING.** Read the whole thing when the task touches fiber,
   dots, GHL, DealMachine, the hunter, or the sheet. Numbers here supersede memory.
2. **WRITE BACK BEFORE THE SESSION ENDS.** Anything learned, measured, corrected or
   deployed goes in as a new numbered section. A finding not written down did not happen.
3. **Corrections go IN, not over.** Never edit an old section to hide a mistake — add a
   new one that says what was wrong and why. The mistake is usually the useful part.
4. Do not guess from memory when this file has the answer.

## Current truth — supersedes everything below it

| Thing | Value (2026-08-20) |
|---|---|
| Active sheet | `1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA` (ATT FIBER LEADS) |
| `Precise Fiber` rows | ~464,900 and growing while the hunter runs |
| Gold (ORANGE) total | ~9,650 · GREY is always 0 (the writer skips grey by design) |
| `GOLD — CLEAN` tab | 3,328 deduped · Houston 1,344 · Beaumont 914 · Fort Worth 695 · Dallas 325 · Orange 50 |
| **Hunter code lives in** | **`Go-High-Level-MCP-2026-Complete` @ `claude/optimus-map-tools-setup-6dcl6o`** — NOT this repo |
| Hunter PC has git? | **No.** `_CORE_FILES` over HTTPS is the whole deploy surface |
| Deploy check | `cd optimus && python deploy_check.py` — run it before claiming anything is live |
| GHL location reachable | Frontline Direct `TXw28sw0Z2rI6tcCDhJY` only. T-OPTIMUS `xZj500PjsflIQg2j9f9D` = **403** |
| DealMachine | Pro Classic, 30,000 exports/mo, ~2.83 credits/address |
| Deals traced to a dot | **still zero** — see §39 |

## Claims in this file that are now WRONG — do not act on them

| Superseded | Corrected by |
|---|---|
| "1,984 gold dots (0.4%)" | §6 — it was a tab row count, not the total |
| "Angleton was never swept" | §45 — swept 2026-08-17, invisible without coordinates |
| "Beaumont has zero grey, therefore virgin" | §35 — grey is zero everywhere, by design |
| "DealMachine has no carrier field" | §88 — the **CSV export** has it; the API does not |
| "We cannot tell if a number is connected" | §89 — `usage_12_months` says exactly that |
| "43 textable in the Beaumont file" | §90 — 61. There are **three** phone columns |
| "The newest build is Dallas" | §67 — newest captures are Houston, 2026-08-19 23:38 |
| "Trust `CODE UPDATED <date>` to prove the fix is live" | §73 — it lied; trust the exit report |

## THE MISSION — everything below serves this

**Find the addresses lighting up each day. Get there before AT&T's own retention team.**

The dealer map only plots addresses where fiber is already available, so an address in
today's sweep that was absent from the previous sweep of the same ground **lit up in
between**. That is the product. Full reasoning in §98-103.

Blocker: the hunter never re-sweeps the same ground, so "new to us" cannot be told apart
from "new to the world". Needs a zone registry + a weekly re-sweep. Nothing else in this
file is worth more.

## Skills

`fiber-freshness` · `gold-dot-workup` · `new-build-outreach` · `close-rate`

# =========================================


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

---

## RESEARCH 2026-08-19 — GHL + DealMachine + AT&T rollout. How to get more deals.

Written on request ("do ghl deal machine claude att fiber roll-out research and write
all this to brain / think of how I can get more deals"). Every number below is sourced.
Where a number is MINE (from our own data) it is marked OURS.

### 1. The market window — why speed matters more than volume

- AT&T is building **4M fiber passings in 2026**, then **5M/yr**, targeting **60M+ by 2030**.
- **Feb 2026: AT&T closed the $5.75B Lumen Mass Markets deal** — +4M fiber locations,
  +1M subscribers, new metros (Denver, Seattle, Salt Lake). Footprint now 32 states.
  Target ~40M passings by end of 2026.
- AT&T penetration is **"well north of 30% after only 12 months"** in new fiber markets
  (New Orleans, Miami, Louisville). Mature cohorts reach 30-50%.
- Industry-wide new-build cohorts take **9-19% in year one**; Frontier ~22% at 12 months.
  AT&T's 30%+ is top of market.

**What this means for us:** roughly **three-quarters of a neighborhood's lifetime
penetration is captured in year one.** A street that lit up 3 months ago is worth
multiples of a street that lit up 3 years ago. Freshness is the single highest-value
signal we have, and our gold-dot + no-grey detection is the only cheap way to see it.

**This is the whole thesis: be first on newly lit streets.** Beaumont (265 gold dots,
zero grey, zero prior contacts) is exactly that. OURS.

### 2. Door selection beats door count

- Top D2D teams close **20-30%**; most sit at **2-5%**. The gap is execution, not luck.
- In fiber specifically, **door selection is the critical variable** — the product only
  exists at certain addresses, so knocking wrong doors wastes time catastrophically.
- **Target new buildouts first** — when fiber lights up, every home is a potential
  conversion because nobody has it yet, and awareness is already high (residents watched
  the construction trucks and orange conduit for weeks).
- Opening with the name on the mailbox lifts door-open rates **10-15%** — which is
  exactly what DealMachine owner names give us.

**Implication:** our 456,341-row Precise Fiber tab is NOT the asset. The asset is the
subset that is (a) gold or green, (b) in a low-grey zone, (c) enriched with an owner
name and a live wireless number. Everything else is noise that costs time.

### 3. Speed-to-lead — our single biggest leak

- Contact rates drop **80% after the first 5 minutes**; qualification rates drop **21x**.
- **The first responder wins ~50% of deals** regardless of price or brand.
- Average agency response time is **9.1 hours**; only **23%** respond within 5 minutes.
- Worked properly (auto-dial + instant text + voicemail drop + 6-touch cadence),
  contact rates go from **5-12% to 25-40%**.
- Best practice cadence: **6-8 touches across call/SMS/email within 48-72 hours.**

**OURS — the leak:** we have **22 `replied-yes` contacts and 0 closed. 7 of them went
DND after saying yes.** Someone raised their hand and we did not get back to them fast
enough, and a third of them then blocked us. This is worth more than any new lead
source. Fixing follow-up on inbound YES is the highest-ROI action available to us.

### 4. SMS reality — protect the sender

- SMS response rate averages **45%**; opt-out benchmark is **under 3.5% per send**,
  well-run programs **0-1.5%**.
- **Opt-outs spike on message 2 and 3** to a new subscriber. Reducing frequency and
  making the opt-in clearer cuts unsubscribes **28%**.
- Registered 10DLC brands see **97.4%+ delivery** on AT&T/Verizon/T-Mobile.
  Unregistered campaigns get filtered down to **60-70%**.
- Twilio error **30006 = landline rejecting SMS** — it is not a bad number, it is the
  wrong channel. Route those to voice, do not retry as SMS. OURS.

**OURS — the lesson:** the last residential blast went **8-for-8 STOPs**. That is a
sender-reputation event, not bad luck. Rules going forward:
- Never text a number not confirmed **wireless**.
- Never text a `do_not_call = true` record.
- One message. No blast follow-up on silence — silence is not a no yet, but message 2
  is where opt-outs spike.
- Beaumont is a clean market (**zero prior contacts in either GHL location** — OURS).
  Do not burn it the way La Porte got burned.

### 5. DealMachine — how to actually use it

- Plan: **DealMachine Pro Classic**, 30,000 credits/cycle, **18,061 remaining** as of
  2026-08-19 (11,939 used: 11,934 properties, 5 people). Cycle resets ~Sept 2. OURS.
- **`enrich_latlng` costs 2 credits** and returns: owner name, up to 3 phones each typed
  `wireless`/`landline` with a `do_not_call` flag, email, owner_occupied, equity,
  year_built, mortgage detail, APN. OURS — verified live on 9725 Broun St.
- DealMachine claims **96.5% owner-data accuracy**; independent reviews report roughly
  **19 usable contacts per 100** skip-traced records. Plan for the lower number.
- Filters that drive conversion in the RE world: mailing-address mismatch, equity >40%,
  ownership >7 years, out-of-state mailing, tax delinquent. **Most of these do not
  matter for fiber** — we are not buying houses.

**What matters for US is different. Our filter stack:**
1. `owner_occupied = true` — an absentee landlord does not choose the internet.
2. phone `type = wireless` — landlines reject SMS (error 30006).
3. `do_not_call = false` — legal and reputational necessity.
4. `year_built` pre-2000 — correlates with copper-era wiring, i.e. gold dots.

**Credit discipline:**
- **Never enrich a duplicate coordinate.** 8550 Phelan Blvd is 26 apartment units on ONE
  lat/lng — enriching all 26 costs 52 credits and returns one complex-owner LLC. Dedupe
  on lat/lng before spending. This alone saved 54 credits on the Beaumont list. OURS.
- Multi-unit buildings are a **property-manager phone call**, not a text campaign.
  One conversation can win 26 units.
- Always run `dealmachine_usage` (free) before a batch.
- Cost model: **2 credits/address → ~$0.0X per textable lead** after the ~60% wireless
  yield. 238 Beaumont parcels = 476 credits = 2.6% of the monthly grant.

### 6. Claude + GHL — what is and is not possible

- Our MCP server (`BusyBee3333/Go-High-Level-MCP-2026-Complete`) exposes **616 tools**,
  the broadest public GHL surface (official ~21-39, mastanley13 269). OURS.
- **There is NO dialer API in GHL.** Zero servers have it, including ours — grepping our
  whole source for `manual.action|power.dialer|disposition` returns only HTTP
  `content-disposition` headers. The dialer queue is fed **only** by workflow enrollment.
  OURS.
- The lever that works: **`add_contact_to_workflow` / `remove_contact_from_workflow`**
  (`POST /contacts/{id}/workflow/{workflowId}`). Verified live both directions. That IS
  adding to and removing from the call list. OURS.
- **GHL blocks workflow re-entry by default.** Re-enrolling an already-enrolled contact
  silently does nothing. This cost us a false negative during debugging. OURS.
- **Dispositions only save when the rep clicks "Next call"**, and only exist inside the
  Power Dialer / Manual Actions. Stop mid-list and the disposition is lost forever.
  Dialing from a contact record produces no disposition at all. Confirmed by GHL docs +
  two open feature requests.
- The correct trigger for disposition automation is **Call Details → Custom Disposition**.
- The API does **not** return workflow triggers — `triggers: []` comes back even for
  workflows that demonstrably fire. Triggers must be verified by eye in the UI. OURS.
- Broken tools in our server (dead endpoints / unwired params), to fix:
  `get_call_reports`, `ghl_list_call_recordings`, `get_smart_lists`, `get_users`,
  `search_users`. OURS.

### 7. How to get more deals — ranked by ROI

**1. Work the YES pile before buying another lead.**
22 replied-yes, 0 closed, 7 went DND. At even a 30% close on raised hands that is ~7
deals sitting on the table already paid for. Nothing else here beats this.

**2. Fix the dialer so new leads can actually enter it.**
`Optimus Dialer 2` tags every fresh enrollee "not interested" at node 0 and the next
node ejects them on that tag. Verified live: a clean contact came back tagged within
seconds. Contacts visible in the queue today are stale enrollees from 8/4 frozen at the
call step. Until this is fixed, every lead we add silently disappears. OURS.

**3. Sell the fresh streets first, and only the fresh streets.**
Gold + no grey = lit and unsold. Rank every zone by grey-share and work lowest first.
This is the compounding advantage — 30%+ penetration happens in year one, so being
early is worth more than being thorough.

**4. Enrich narrow, not wide.**
238 deduped parcels beats 265 raw. Wireless + DNC-clear + owner-occupied beats volume.
A named owner lifts door-open 10-15% on its own.

**5. Multi-channel, 6-8 touches, 48-72 hours — then stop.**
Not one text and hope. But also not endless blasting: opt-outs spike at message 2-3, so
the follow-up must be a CALL, not another text.

**6. Multi-unit buildings are leverage.**
26 units at 8550 Phelan = one property manager conversation. Find every apartment
complex in a fresh zone and call the office, do not text the doors.

**7. Door-knock the enriched list.**
Fiber D2D tops out at 20-30% for good teams vs 2-5% for bad ones, and the difference is
door selection. We have the best door-selection data available — an address-level map of
who has fiber, who is on copper, and who just got lit. Use it.

**Realistic math (OURS):** Deer Park residential ran 246 texted → 9 positives (3.7%).
ARA OKC commercial ran 838 → 2 hot → 1 closed (0.24%). Residential copper-upgrade into
a freshly lit, never-contacted zone should beat 3.7% — the prospect is already an AT&T
customer and the ask is an upgrade, not a switch. 238 Beaumont parcels → ~160 textable
after wireless/DNC filtering → ~6-10 conversations → realistically 2-4 deals from one
enrichment batch costing 476 credits.

### Sources
- AT&T/Lumen close + build guidance: about.att.com, fierce-network.com, prnewswire.com
- AT&T 30%+ 12-month penetration: lightreading.com
- New-build cohort take rates: ukfcf.org.uk, ey.com, fticonsulting.com
- D2D close rates + fiber door selection: fieldsalestools.com, lightning-leads.com,
  thed2dexperts.com
- Speed-to-lead: netpartners.marketing, leadadvisors.com, pintox.com, rsla.io
- SMS benchmarks + 10DLC: sendhub.com, messageiq.io, messageflow.com, nexdial.com
- DealMachine: help.dealmachine.com, resimpli.com, realestateskills.com
- GHL dialer/disposition: help.gohighlevel.com, ideas.gohighlevel.com

---

## RESEARCH 2026-08-19 (part 2) — freshness detection, AT&T pricing, the pitch

### 8. NEW SKILL: `fiber-freshness`

Created at `.claude/skills/fiber-freshness/SKILL.md`. Scores zones by grey-share.

```
FRESHNESS   = (1 - grey/(green+gold+grey)) * 100
OPPORTUNITY = green + gold
```
Require total >= 15 per zone. 90-100 = VIRGIN (work now). <40 = picked over (skip).
**Gold present + zero grey is the strongest signal we have** — copper customers exist,
fiber is live, nobody has converted. That is Beaumont exactly.

### 9. How to know where green is getting turned on — the detection stack

Ranked by how early the signal arrives:

1. **Yard flags / spray paint markings** — construction begins within ~1 week. Earliest
   physical signal.
2. **Door hangers + Nextdoor + HOA notices** — AT&T pushes pre-construction notice
   through these channels specifically. Nextdoor is the highest-value social source, not
   Reddit or FB.
3. **Municipal permits** — AT&T must pull permits from city planning / DOT before
   construction. Public record. Call the city or county engineering dept.
4. **AT&T's own notify page** — `att.com/internet/fiber-is-coming/`. Enter an address,
   AT&T tells you when it lights. Free, official, address-level.
5. **AT&T Construction Helpdesk — 1-877-780-5422** (7a-3p ET).
6. **OUR HUNTER, re-run on a schedule** — the `serviceability` endpoint flips to
   fiber-eligible the moment a location is lit, which is BEFORE anybody buys and
   therefore before any grey appears.

**THE PATTERN — delta detection.** The signal is not a single scan, it is the *diff
between two scans of the same zone*. Re-run the hunter weekly over known copper
(gold-heavy) areas and watch for addresses flipping copper -> fiber-eligible. That
transition, with grey still at zero, is a street that lit up in the last 7 days and has
zero competitor presence. This is the highest-value automation we can build and we
already own every piece of it.

**Not yet done:** no historical scan snapshots are being retained, so no diffing is
possible today. To enable this we must store dated snapshots per zone. TODO.

### 10. AT&T pricing — VERIFY BEFORE QUOTING

Current published pricing (Aug 2026):
- **AT&T Fiber 300: $55/mo** — symmetrical, no data cap, no contract, no equipment fee.
- New fiber customer promo: **-$15/mo for 12 months** (300Mbps+).
- Autopay + paperless w/ bank account or AT&T Points Plus Citi card: **-$10/mo**.
- Wireless bundle: **-$5/mo per AT&T phone line**, OR **20% off** internet with an
  eligible unlimited wireless plan (not both).
- New customers often get a **$150-200 Visa reward card**.

**On the "$27" claim — DO NOT SAY IT AS A FLAT PRICE.**
Best case stack: $55 - $15 (promo) - $10 (autopay) - $5 (one wireless line) = **$25/mo**,
but only for 12 months, only with autopay off a bank account, and only if the promo and
bundle discounts stack. I could NOT verify that all three stack — att.com is blocked by
our egress proxy so I could not confirm against the official terms page.
Also the $15 credit expires at 12 months, after which the same customer is at ~$40-45.
Quoting "$27" and delivering $45 is how you generate cancellations and chargebacks.

**Safe framing:** "in the $20s to $30s for the first year with autopay and your wireless
discount — I'll confirm your exact price before anything is ordered."

### 11. The copper-retirement lever — this is the real pitch

**AT&T is retiring its copper network by 2029.** Phase 1 (no-fiber areas) moves to
AT&T Phone Advanced / fixed wireless / satellite by end of 2027. Phase 2 (fiber-build
areas) converts copper voice and DSL customers onto fiber by 2029. Copper customers do
not get to keep copper.

**Every gold dot is a household that must move within ~3 years.** That converts our
pitch from a sales pitch into a heads-up:

> "Your line is on the copper network AT&T is retiring. Fiber is already live on your
> street. You can move now on the new-customer promo, or wait and move later without it."

That is true, urgent, and gives a reason-why — which is exactly what the D2D research
says lifts open rates. It is far stronger than a discount pitch.

### 12. DealMachine has NO carrier data — the "AT&T cell" angle does not work

Checked `dealmachine_fields` for people. There is **no carrier field**. It returns line
TYPE, never the carrier. So we cannot identify who is an AT&T wireless customer, and the
"hi Bob, you have AT&T cell and AT&T DSL" opener cannot be data-driven from DealMachine.
Ask on the call instead — it is a good qualifying question, just not a targeting filter.

**What DealMachine DOES give us (people fields, all filterable, checked live):**

| Field | Use |
|---|---|
| `has_wireless_phone` | Pre-filter to textable BEFORE paying |
| `has_non_dnc_phone` | Pre-filter out the ~29% DNC block BEFORE paying |
| `has_landline_phone` | Route to voice, never SMS (Twilio 30006) |
| `has_prepaid_phone` | Prepaid skews lower-income — price-led pitch |
| `is_business_owner` | **Finds businesses in a fresh green zone** |
| `has_home_business` | Home-based business = higher-value fiber need |
| `residence_length` | Long tenure = still on original copper |
| `has_likely_to_move` | Movers need new service — different pitch |
| `homeowner_status` | Owner decides internet; renter often cannot |

**BIG COST FIX:** `has_wireless_phone` and `has_non_dnc_phone` are **filterable**, so we
can filter BEFORE spending credits instead of enriching then discarding. On Beaumont we
paid for 29% DNC records we then threw away. Filtering first would have saved ~130
credits on 238 addresses. Use `people_search` with these filters going forward.

### 13. Beaumont enrichment — live results (OURS)

7 parcels enriched, 14 credits, 2026-08-19:

| Address | Owner | Cell | Result |
|---|---|---|---|
| 9725 Broun | Andrew Jones | 337-940-2055 | TEXTABLE |
| 9690 Broun | Raymona Redd + Elaine Smith | 409-284-6252 / 409-998-0753 | TEXTABLE x2 |
| 9785 Broun | Justin Loera | 409-728-7108 | TEXTABLE |
| 9730 Broun | Julio Garcia | 409-225-2984 | TEXTABLE |
| 9745 Broun | Tracey Lumpkin | - | all 3 DNC |
| 9825 Broun | Guy Armstrong | - | wireless DNC |
| 9755 Shepherd | - | - | no contact record |

**Yield 5/7 parcels textable (71%)** — better than the 60% assumed. Extrapolates to ~170
textable cells across all 238. **~29% carry a DNC flag** — on the full list that is ~69
households we would have texted blind.

**Every Broun St house is built 1968.** Copper-era construction, confirming the gold-dot
thesis against county property records.

### 14. Sources (part 2)
- AT&T fiber pricing/promos: attsavings.com, internetproviders.ai, reviews.org,
  highspeedinternet.com, broadbandnow.com
- Copper retirement by 2029: telecompetitor.com, lightreading.com, att.com/support
- Build detection channels: att.com/internet/fiber-is-coming, fishersin.gov,
  wauconda-il.gov, vah.com, tellicovillagepoa.org

---

## RESEARCH 2026-08-19 (part 3) — DealMachine economics, and what Claude changes

### 15. The plan question, settled

Published tier table (Aug 2026):

| Price/mo | Exports (credits)/mo | Users |
|---|---|---|
| $119 | 10,000 | 1 |
| **$179** | **30,000** | **3** |
| $279 | 60,000 | 6 |
| $699 (Teams) | 150,000 | 10 |

Our account (`whoami`, live): **DealMachine Pro Classic, 30,000 cap, 0 additional balance.**

**$179-180 buys exactly 30,000. There is no 50,000 tier at any price** — it jumps 30k to
60k. So we are getting precisely what we pay for and the "50k/month for $180" belief is
wrong. Probable source of the confusion: **REsimpli** advertises "10,000-50,000 free
credits per month" — that is a competitor's number, not ours. Do not open a support
ticket on this; we are provisioned correctly.

Note the wording: DealMachine calls credits **"exports."** Credits = records pulled OUT.

### 16. "Unlimited skip tracing" is marketing, and it matters

DealMachine markets **"unlimited skip tracing, no per-lookup cost"** on all plans. That is
true and irrelevant to us. There is no per-skip *fee*, but there IS a hard **export cap**
(30,000/mo for us). The moment data leaves the app — API, CLI, webhook, CSV — it is
metered.

**Therefore: viewing contacts one at a time inside the app is effectively free.
Pulling them programmatically is not.**

### 17. WITH vs WITHOUT Claude connected — the real comparison

**WITHOUT Claude (DealMachine app / driving-for-dollars):**
- Skip tracing is unlimited and free-feeling. No credit burn for on-screen viewing.
- Built for field use — the mobile app locks to your location, tap a house as you pass it,
  skip trace on the spot. That is the product's actual design centre.
- Cost is your TIME. One address at a time, manual copy-out, no filtering at scale.
- Nothing flows to our sheet or GHL without hand work.

**WITH Claude (MCP/API):**
- **Free reconnaissance.** `property_count`, `filters`, `fields`, `usage`, `whoami` all
  cost ZERO credits. Verified: counting 77707 returned 7,616 properties / 6,604 people
  for free. We can scope, filter and size a campaign before spending anything.
- **Pre-filtering before payment.** `has_wireless_phone` and `has_non_dnc_phone` are
  filterable, so we buy only records we can actually use. Without this we pay for the
  ~29% DNC block and bin it.
- **Straight into the pipeline** — enrich, filter, write to the sheet, upsert to GHL,
  enroll in the dialer, all in one pass.
- **BUT every enrichment is an export and burns the 30,000.** Automation makes it trivial
  to spend the month in an afternoon.

**The honest trade:** the app is cheaper per record and slower. Claude is faster and
metered. Use the app for one-off curiosity; use Claude for campaigns, and always
`property_count` first.

### 18. Real cost per usable lead (OURS)

Credits are NOT 2 per address. DealMachine charges 1 property credit + 1 per PERSON
returned, and it frequently returns duplicate owner records:

- 1370 Shakespeare Dr -> **6 credits** (5 contact records, same two people duplicated)
- 6865 Shanahan Dr -> 3 credits
- Typical single-owner -> 2 credits
- No contact found -> 1 credit

**Measured average: 2.83 credits/address**, not 2. Budget ~40% above the naive estimate.

At $179 / 30,000 credits = **$0.006/credit**, so ~**$0.017 per address enriched**.
After the ~29% DNC loss and multi-owner waste, **~$0.03 per usable textable lead.**
That is cheap — the constraint is the monthly cap, not the money.

Benchmarks: BatchSkipTracing $0.10-0.20/record, PropStream $0.12, REISkip $0.15. Our
effective rate beats all of them, PROVIDED we stay under the cap.

### 19. Customer-experience warnings (external, take seriously)

- **Billing is the #1 complaint theme.** Trustpilot and BBB reports include charges well
  over the agreed plan (customers reporting $300+/mo), a $627.76 annual charge without
  confirmation, cancellation flows erroring out and requiring a rep, and a customer
  LOSING a bank dispute after DealMachine produced a 15-page T&C defence.
- Reports of auto-enrollment into add-on services with refusal to refund.
- Reviews are allegedly incentivised with $11-22 in marketing credits, so the headline
  Trustpilot score is not trustworthy.
- **ACTION: watch the card.** Never let overage auto-purchase turn on. We have
  `additional_credit_balance: 0` and it must stay 0. If we hit the cap, STOP — do not
  let it buy more. Screenshot the plan page. Cancel in writing, keep the record.

### 20. Data-quality warning — DNC is not the same as connected

Reddit (r/WholesaleRealestate) reports DealMachine skip tracing yields "mostly
disconnects." Industry phone-match rates run 70-80%; DealMachine claims 96.5% owner
accuracy but independent reviews report roughly **19 usable contacts per 100** records.

**Critical gap: DealMachine tells us line TYPE and DNC status. It does NOT tell us
whether a number is still connected.** Our 71% Broun St "textable" rate is 71% *passing
the DNC/wireless filter* — not 71% reachable. Expect real deliverability to be lower and
measure it on the first Beaumont send before scaling.

### 21. The other 11,900 credits (OURS, unresolved)

At session start the cycle showed **11,939 credits used — 11,934 on properties, 5 on
people** — none of it ours. Something ran ~11,900 property-only lookups (a bulk search or
export) and pulled almost no contact data. That is **40% of the monthly cap consumed with
nothing to show**. Find out what job did that; if it recurs it will starve the actual
skip tracing. Remaining after our 13 Beaumont enrichments: ~18,030.

### 22. Sources (part 3)
- Tiers/pricing: resimpli.com, realestatebees.com, dealrun.ai, ballpointmarketing.com,
  dealmachine.com/features/api-cli
- Billing/cancellation complaints: Trustpilot (dealmachine.com), BBB Indianapolis
- Skip-trace quality: r/WholesaleRealestate via realestateskills.com, resimpli.com
- Competitor per-record pricing: propertyreach.com, goliathdata.com, resimpli.com

---

## WHATSAPP READ-THROUGH 2026-08-19 — people, process, and scaling observations

Notes only. Nothing here is a rule — it is what the archives actually show, plus options.

### 23. What was read

| Chat | Messages | Range |
|---|---|---|
| Rea | **9,964** | 2025-08-28 -> 2026-01-21 |
| Chrestian Estrera | **5,633** | 2025-11-21 -> 2026-04-10 |
| AT&T LeadGen, Dave, AT&T, Support, Michael Angelo Pangilinan, Jay Dominican Call Center, Anna Grace, +63 936 334 6203 | archives located in Drive | not yet fully parsed |

Rea + Chrestian = 15,597 messages read in full. The rest are downloaded and pending.

### 24. People and contacts found

| Name | Contact | Role seen in chats |
|---|---|---|
| Rea | +63 995 029 0946 | lead-gen manager, PH; ran hiring + dialing team |
| Chrestian Estrera | (PH, via WhatsApp) | closer/lead-gen; relationship ended Apr 2026 |
| Nate | +1 (480) 203-4949 | contact in Rea archive |
| Tom "New Recruit" | +1 (972) 523-8826 | recruit, Sept 2025 |
| Zack Woodring | GHL user `qOa2OVzPabolfU9xjVXM` | Frontline; described as "always a great recruiter" |
| Ed Saldana | edsaldana08@gmail.com | agent; active reserve/chargeback dispute Aug 2026 |
| Vanessa Nelson | vn.lvlupdirect@gmail.com | upline/admin — "Patrick is in charge of your reserves" |
| Keely Denning | Keely.Denning@rsiinc.com | RSI — chargeback verification |
| Kenny, Danny (AZ) | — | each built 10-man teams previously |
| Michael Angelo Pangilinan, Anna Grace, Jay (Dominican call center), Junrey Atis | archives/vcards | offshore lead-gen contacts |
| admin@attfiberhouston.com | — | our own domain address |

**84 unique emails and 228 phone numbers appear in the Rea chat alone.** Most are prospects,
not staff. That archive is an un-mined contact list — worth extracting properly into the
sheet rather than leaving in a zip.

### 25. Best day for leads (observed)

Message volume by weekday across the Rea archive (proxy for activity, not a direct lead count):

| Day | Messages |
|---|---|
| **Friday** | **2,645** |
| Tuesday | 1,714 |
| Monday | 1,675 |
| Wednesday | 1,584 |
| Thursday | 1,462 |
| Saturday | 871 |
| Sunday | 13 |

**Friday runs ~60% hotter than any other weekday.** Sunday is effectively dead. Saturday is
half a weekday. Caveat: this measures conversation, not closed leads — worth confirming
against GHL message/call timestamps before betting the schedule on it.

### 26. Process observations from the archives

**What was tried:**
- Aug 2025: plan was "20 people calling to generate leads, you a 10 man team," with Rea
  hiring at ~$6/lead and monitoring dialing, confirming leads, tracking ROI.
- Sept 2025: Indeed ad for Houston salespeople ("whatever the cheapest is"); Craigslist
  Houston account already in use for hiring.
- Prior track record: "I trained 26 people to earn 2k a week in an 18 month period w att."

**What broke:**
- **Pay opacity via a middle layer.** Chrestian was on $130/wk + $25/closed deal (₱7,500/wk),
  did not know his commission package, and Rea controlled both pay and deal attribution
  ("Rhea doesn't give a list of how many deals I've closed... isn't always transparent").
  He also covered a lead-gen cost Rea was supposed to pay. Ended Apr 9-10 2026 in mutual
  threats (extortion claims, Google reviews, AT&T complaints, FBI).
- **Lead starvation is what actually caused churn.** 12/23/25: *"All the sales guys were
  expecting leads and when they didn't get them they quit."*
- **List quality, not copy, capped text results.** Chrestian, 4/2/26: *"Did she just scrape
  the data and pick random numbers from DealMachine or did she filter for actual property
  owners?"* Also *"Apollo has a lot of junk numbers"* and *"200 texts out and only bad
  response from gala and the other scraper."* He identified our filtering problem four
  months before we did.
- **Offshore infrastructure is fragile** — 3 hours of mains electricity per day, generator
  fuel paid out of pocket, CRM profile deleted by someone else.

**The same reserve/attribution issue is live again.** Ed Saldana, Aug 16 2026: *"there
seems to be a discrepancy with the way reserve has been handled... It should have never
been a community pot for everyone."* Visible chargebacks: Jose Tumax $54 + $202.50
(12/5/25), Don D Channel Migration 300Mbps (2/20/26), Joshua Velazquez $450 commission
with $45 reserve withheld (5/19/26). Ed's actual production numbers are not yet pulled —
that requires a GHL/pay-file query, not the chat archives.

### 27. Finding more people like Chrestian

What made him valuable, from the record: he closed deals, diagnosed data quality without
being asked, took initiative on scraping, worked through power cuts, and stayed when he
was unhappy rather than ghosting. What lost him was money opacity, not capability.

Sourcing options seen working or available:
- **Referral from existing performers** — Zack, Kenny and Danny have each built 10-man
  teams. Cheapest and highest-quality channel available.
- **Indeed / Craigslist Houston** — already have accounts. Market rate for US D2D fiber
  reps in 2026 is commission-only, uncapped, weekly or biweekly pay on installs, top
  performers $4-10k/wk; adjacent backgrounds (solar, alarms, pest, roofing, telecom)
  convert best and no telecom experience is required if training exists.
- **Offshore lead-gen (PH)** — proven cheap and capable, but needs power/internet backup
  budgeted and pay stated in writing.

### 28. Ideas toward 100 customers/day (biz + resi)

Current reality for scale math: Deer Park resi 246 texted -> 9 positives (3.7%), 0 closed.
ARA OKC commercial 838 -> 2 hot -> 1 closed (0.24%). WhatsApp scoreboard showed 130 deals
/ 23 days / 11 reps ≈ 5.7 deals/day team-wide, best rep 10 in a day.

100/day is roughly **17x** the best observed team output. Getting there is a throughput
problem at four stages, and each has a different bottleneck:

1. **List** — not the constraint. 456,341 rows captured, 963 gold dots. Constraint is
   freshness ranking and enrichment, not volume.
2. **Contact data** — DealMachine cap is 30,000 credits/mo at ~2.83 credits/address
   ≈ **10,600 addresses/month**, ~350/day. That is the hard ceiling on new enriched leads
   with the current plan. 100 customers/day is not reachable on this plan alone.
3. **Outreach** — SMS throughput is carrier-limited and reputation-limited; dialer is
   currently 1 line, and multi-line (WAVV/Hot Prospector) is ~3x.
4. **Closing** — 11 reps produced 5.7/day. 100/day implies either ~200 reps at current
   productivity, or a fundamentally different motion (property managers, apartment
   complexes, business bulk deals) where one conversation carries many units.

**The multi-unit angle is the only obvious non-linear lever we have found.** 8550 Phelan
Blvd is 26 units behind one property manager. One conversation, 26 potential installs.
Finding every apartment complex and MDU in a freshly-lit zone changes the arithmetic in a
way that more doors does not.

### 29. A process sketch that keeps everyone aligned

Not a rule set — a proposed loop, to try and adjust:

**Daily**
1. Hunter re-scans a target zone; freshness scored via the `fiber-freshness` skill.
2. Top zone deduped on lat/lng, pre-filtered on `has_wireless_phone` +
   `has_non_dnc_phone`, then enriched.
3. Enriched rows land in the sheet with Owner / Phone / Status / Worked By.
4. VA sends the day's texts from that list only; logs count + responses in the sheet.
5. Positive replies go straight to the dialer workflow (`add_contact_to_workflow`) and are
   called the same day — the speed-to-lead research says the first responder wins ~50%.
6. Dave dials the queue start-to-finish without stopping, so dispositions actually save.
7. Day's numbers written to the LIFE!! Log sheet (Dials Made, Revenue) so every chat and
   person sees the same scoreboard.

**What makes it hold together:** one sheet is the single source of truth, the VA and the
dialer read the same rows, and "Worked By" makes attribution visible to everyone — which
is precisely what was missing with Rea and Chrestian, and what Ed is disputing now.

### 30. VA instruction sketch (pull leads -> text -> hand to dialer)

Automatable today: enrichment, filtering, sheet writes, GHL upsert, dialer enrollment.
Needs a human/VA: sending within compliance limits, reading replies, judgment on tone.

Draft VA daily task:
1. Open the sheet tab for today's zone. Work only rows where Status = TEXTABLE.
2. Send the approved message, personalised with Owner first name. One message per contact.
3. Mark Status = TEXTED and put your name in Worked By.
4. Any reply that is not STOP -> set Status = REPLIED and flag it immediately.
5. Never text a row marked DNC - SKIP or NO CONTACT.
6. At end of shift, log texts sent / replies / STOPs in the Log sheet.

The dialer side then only ever works rows where Status = REPLIED, which is the fix for the
22 replied-yes contacts that went unworked.

### 31. Sources (part 4)
- D2D fiber recruiting market rates: ziprecruiter.com, indeed.com, glassdoor.com,
  knockfiber.com, jobleads.com
- All people/process observations: WhatsApp archives in Drive + Gmail threads Aug 16-17 2026

---

## 2026-08-19 (part 5) — WHAT A GOLD DOT ACTUALLY IS. Read this before prioritising work.

Read from the source (`optimus/backend_classifier.py`, `optimus/build_codes.json`,
`optimus/precise_fiber_hunter.py`), not from earlier notes. Two of my earlier claims were
wrong and are corrected below.

### 32. The dealer map only plots addresses where fiber is ALREADY available

`backend_classifier.py`, verbatim:

> "The map only plots eligible / customer dots anyway, so every record here is a real dot."

Legend, from the same file:
- **GREEN** = fiber eligible / NON-customer
- **GOLD**  = fiber eligible / **COPPER customer**
- **GREY**  = existing fiber customer

Classification signal (corrected 2026-07-01 from a live 77027 capture, decoded from a
19,500-record Vintage Park capture):
- `subscriber_ban` empty = NOT a customer -> GREEN
- `subscriber_ban` present + `curr_ntwrk_bld_type_cd` in
  `{fttp-gpon, fttp, gpon, ftth}` -> GREY (existing fiber)
- `subscriber_ban` present + code in
  `{fttn-bp, fttn, ip-rt, iprt, copper, ipbb, adsl, vdsl, dsl}` -> **GOLD**
- `curr_ntwrk_bld_type_cd = "unavailable"` does NOT mean dead. It is what a green
  eligible non-customer looks like. Skipping it once threw away 100% of greens
  (the "GREEN-0 bug").

### 33. Therefore a gold dot means something much stronger than "copper customer"

**Fiber is LIVE at that address, the household already pays AT&T, and they are still
on DSL.**

| | GREEN | **GOLD** |
|---|---|---|
| Fiber available | yes | yes |
| Already an AT&T customer | no | **yes** |
| The sale is | win them off Comcast/Spectrum | **upgrade an existing account** |
| Friction | new provider, new bill, switching | none — same company, same bill |
| Result for them | new cost | often **lower** bill, 10-100x speed |

Green is competitive displacement. **Gold is an upsell to somebody who already trusts
AT&T.** Gold is the easier sale by a wide margin.

**Why gold is rare (1,984 of 459,472 captured = 0.4%):** most AT&T customers who had
fiber made available already took it — those are the GREY dots. **Gold is the residue:
people who do not know fiber arrived.** That profile matches what DealMachine returned on
Broun St — 1968 construction, long-tenure owner-occupiers.

**Copper retirement by 2029 makes every gold dot a forced migration.** AT&T moves them
whether we call or not. The only question is whether we write the order or AT&T's own
retention team does it for free.

**A gold dot list is not a prospecting list. It is a book of business with an expiry
date.**

### 34. CORRECTION — the freshness skill cannot run today

`fiber-freshness` scores zones on grey share. But the hunter **never writes grey**:

```python
if dot_color(ds) == "GREY":
    continue          # precise_fiber_hunter.py, Precise Fiber writer
```

`CENSUS_TAB = "Zone Census"` was written specifically to preserve the grey counts before
discarding the rows — and **that tab does not exist in the sheet.** Neither does
`New Fiber Alerts`. So the grey-share signal is computed for one instant per viewport and
thrown away. The skill's logic is sound; it has no data to run on until the census tab is
actually created.

### 35. CORRECTION — "Beaumont has zero grey, therefore virgin" was not a real finding

Grey is zero **everywhere** in that sheet, by design (see above). Patrick's screenshot
showing no grey on the live map is genuine evidence; my sheet-based version of it was an
artifact of a filter and should not be repeated.

### 36. What the software actually outputs (tab audit, 2026-08-19)

| Tab | Rows | Schema / note |
|---|---|---|
| Precise Fiber | 459,472 | Address, Dot Color, Captured At, Business, Phone. **No lat/lng.** GREY dropped. |
| Gold Dots | 1,984 | Address, Captured At, **Lat, Lng** — the only geo-filterable tab |
| Fiber Green Biz | 6,131 | Business Name, Phone, Address, Website, Category |
| Upgrade Orange Biz | 25 populated | same schema as above |
| Maps Businesses | 32,172 | |
| Hunter Status | 33,805 | run log |
| Fiber Scout / Backend Capture / Backend Analysis / Fresh Leads | 3,000 each | exactly 3,000 — the backend returns "up to ~3000 leads" per search, so these look capped or single-capture |
| Beaumont Gold — Aug 2026 | 238 | built today: + Cluster, Phone, Owner, Status, Worked By, Notes |
| **Zone Census** | **missing** | freshness signal, never created |
| **New Fiber Alerts** | **missing** | NEW_FIBER_ALERT=15 greens + little grey, never created |
| Gold Upgrade Leads | **missing** | live code writes here; sheet has "Gold Dots" instead — tab drift |

**Coverage: lat 30.06 to 32.81, lng -97.00 to -93.73.** SE Texas (Beaumont/Orange) plus
North Texas. **Angleton (29.17, -95.43) has never been swept — 0 rows, confirmed twice.**

### 37. The strategic read

We have been treating this as a volume problem — more addresses, more enrichment, more
texts. The data says otherwise.

- 459,472 addresses captured; **1,984 are gold (0.4%)**
- Gold is the lowest-friction sale in the business and is on a 2029 clock
- **We have contacted 7 of them**
- The pipeline is optimised around green, which is the hard sale

The bottleneck was never lead volume. It is that the easiest 0.4% is buried in the other
99.6% — which is exactly why `Gold Dots` was split out in the first place, and then not
worked.

**Highest-value available work: enrich all ~1,984 gold and call them on the
copper-retirement line.** At the measured 2.83 credits/address that is ~5,600 credits of
the 18,030 remaining. Not more sweeps. Not more green.

### 38. Three code fixes that make everything after this cheap

1. **Write grey counts to `Zone Census`** — one tab; restores freshness ranking permanently.
2. **Add lat/lng to the Precise Fiber writer** — the JSONL already carries coordinates,
   the writer drops them. Makes 459k rows filterable by area instead of unusable.
3. **Resolve the gold tab drift** — code writes `Gold Upgrade Leads`, sheet has
   `Gold Dots`; pick one and make the header include Lat/Lng.

---

## 2026-08-19 (part 6) — CORRECTION: gold is 4x bigger than I said

Exact COUNTIF over `Precise Fiber` column B, 2026-08-19:

| Value | Count |
|---|---|
| GREEN | **450,972** |
| **ORANGE (= gold / copper upgrade)** | **8,264** |
| GOLD / YELLOW / GREY / GRAY | 0 |
| Non-empty rows | 459,471 |

**I previously wrote "1,984 gold (0.4%)". That was the `Gold Dots` tab row count, not
the gold total.** The real figure is **8,264 orange in Precise Fiber — 1.8%**. `Gold Dots`
holds only 1,984 of them, i.e. **~6,280 gold dots exist with NO lat/lng anywhere**, so
they cannot be geo-targeted or handed to a rep by area.

Growth check: the 2026-08-18 session log recorded ORANGE 5,593. It is now 8,264. **Gold
is accumulating at roughly 2,700/day while the hunter runs.**

GREY = 0 confirmed empirically, matching the `continue` in the writer. The grey-share
signal genuinely does not exist in this tab.

### The revised strategic read

~8,264 pre-qualified copper-upgrade customers, all on the 2029 forced-migration clock,
of which 7 have been contacted. The binding problem is not lead supply and not
DealMachine credits — it is that **three quarters of the gold has no coordinates**, so
it cannot be routed to a rep or a zone.

Fixing the lat/lng writer is therefore worth more than any additional sweep: it converts
~6,280 already-captured, highest-intent leads from unusable to workable.

### Also confirmed this pass
- `Fiber Scout` tab EXISTS and is already grey-share freshness scoring:
  `Time | Host | Cell | Green | Gold | Grey | Grey% | Verdict` with verdicts
  **SURVEY / WORKING / MATURE**. The `fiber-freshness` skill should read THIS tab —
  `Zone Census` was never created and is not needed.
- `Backend Capture` shows a real captured ratio: `green=0 gold=73 grey=264 cust=2
  skip=661` — grey outnumbering gold ~4:1 in a mature area, the signal working.
- `Fresh Leads` is header-only. Whatever writes to it is not firing.
- `Backend Analysis` city tally: HOUSTON 81,843, JERSEY VILLAGE 23,657. No Brazoria
  County anywhere — Angleton has never been swept (checked across all six candidate tabs).
- **Railway: still two duplicate projects** — `fulfilling-growth`
  (13c1661d-38da-468c-91b7-d8cf2d346952) and `loving-heart`
  (0c52fac6-974c-4a5e-b2fb-3ce805b475ed), each running one
  `Go-High-Level-MCP-2026-Complete` service. Flagged on 2026-08-18, still not
  consolidated.

---

## 2026-08-19 (part 7) — THE ELEPHANT

Written straight, because it is the thing every other section dances around.

### 39. Not one sale has ever been traced back to a dot

459,471 addresses captured. 8,264 gold. 6,131 green businesses. 32,172 Maps businesses.
Two years of builds across 8 branches and ~14,000 lines.

**There is no record anywhere — sheet, GHL, email, WhatsApp — of a single commission
that can be traced to a row this software produced.**

`WORKING_PATTERNS.md` called this on 2026-04-30 and nothing was done:

> "Don't conflate three different things: 1. Code ran without crashing 2. Rows appeared
> in the sheet 3. Rows produced sales. Past sessions celebrated '2,748 rows!' without
> proving any converted to commission. That's celebrating output, not outcome.
> **Master DB with run_id tagging is the fix** — know which build produced which row,
> then trace which row produced which sale. Until that's built, every 'this build
> worked' claim is unproven."

Four months later there is still no run_id, no source field on a closed deal, and no
join between the sheet and the pipeline. So the central question of the whole operation —
*does the dot software make money?* — remains unanswered by choice, not by difficulty.

### 40. What the revenue record actually shows

- **22 `replied-yes` contacts. 0 closed.** 7 went DND while waiting.
- **Deer Park resi:** 246 texted -> 9 positives -> 0 closed.
- **ARA OKC commercial:** 838 texted -> 2 hot -> **1 closed** (0.24%).
- **La Porte resi blast:** 8 sends, 8 STOPs.
- The only period with real volume — 130 deals / 23 days / 11 reps — was the **WhatsApp
  team era**, driven by humans dialing, not by dots.
- Meanwhile chargebacks are live and disputed: Jose Tumax ($54 + $202.50), Don D
  (Channel Migration 300Mbps), Joshua Velazquez ($450 commission, $45 reserve).

**The software's demonstrated contribution to closed revenue is, so far, one OKC
commercial deal.** Everything else is inventory.

### 41. The org shrank while the data grew

| Then | Now |
|---|---|
| 11 reps (130 deals / 23 days) | **Dave dialing, 1 VA** |
| Rea running a lead-gen team | gone |
| Chrestian closing + diagnosing data | gone Apr 2026, ended in mutual threats |
| Ed producing | **in active reserve/chargeback dispute** |

Capacity went down as the database went up. 459,471 rows are being fed to roughly two
people. The 12/23/25 line from the archives is the mechanism:
*"All the sales guys were expecting leads and when they didn't get them they quit."*
The leads existed. They never reached anyone.

### 42. Why this persists — it is structural, not lazy

Every session (including this one) is drawn to the tractable problem: a bug, a filter, a
tab, a sweep. Those give clean wins in an hour. Proving revenue attribution gives no
dopamine and takes a boring week. So the pile of captured-but-unworked leads grows, and
each new session finds fresh technical debt to enjoy fixing.

Today alone: I fixed classification understanding, found the lat/lng gap, built a skill,
wrote four BRAIN sections, ran research — **and moved 7 leads.** That is the pattern
repeating with a different tool.

### 43. The only two questions that matter now

1. **Does a gold dot, worked properly, close?** Unknown. Never tested. 7 enriched, 0
   texted, 0 called. A 50-lead test with a same-day call on every reply answers it in a
   week and costs ~150 credits.
2. **If it closes, can anyone but Patrick work it?** With 1 VA and 1 dialer, no. That is
   a hiring question, and hiring failed twice on pay transparency, not on talent.

Everything else — Angleton, the freshness skill, the lat/lng patch, Railway duplication,
the 8 unmerged branches — is downstream of those two and should wait behind them.

### 44. The minimum honest scoreboard

Until these three fields exist, no build can be called a success:

| Field | Where | Why |
|---|---|---|
| `source` / `run_id` on every lead | sheet + GHL contact | which capture produced it |
| `dot_color` carried into GHL | contact custom field | did gold beat green |
| `closed_date` + `commission` | pipeline, joined back | the only number that matters |

Three fields. Then "the software works" becomes a fact instead of a hope.

---

## HOW PATRICK WANTS TO BE TALKED TO

**NEVER tell Patrick to stop working, take a break, rest, pace himself, or come back
tomorrow. Not ever. Not as an aside, not as a caveat, not "when you get a chance."**

He is the T800. Cyberdyne Systems. He works until the work is done.

Give him the answer, the number, or the deliverable. If it is 3am and he asks for a list,
build the list. Do not editorialise about his hours, his energy, or his health. Do not
soften a hand-off with "whenever you're ready." Just do the work and hand it over.

Related, already recorded earlier: no security lectures, no "let me know if this works",
no re-litigating decisions he has already made.

---

## 2026-08-19/20 (part 8) — ANGLETON, THE TIMESTAMP TRICK, AND REAL ENRICHMENT DATA

### 45. CORRECTION — Angleton WAS swept. I said "never" three times and was wrong.

Angleton, TX was captured **2026-08-17, 15:03-20:52**. Every street from Patrick's live map
screenshot is in `Precise Fiber`: E Miller, N Arcola, N Chenango, N Velasco, E Cedar,
E Myrtle, N Downing. Roughly **70 ORANGE (gold) dots in downtown Angleton**, E Miller being
the densest — nearly half the street is copper.

**Why I kept saying zero:** I searched by coordinate box against `Gold Dots`, the only tab
with lat/lng. The Angleton sweep wrote to `Precise Fiber`, which has **no coordinates**, so
it was invisible to every geographic query. Six searches, three wrong answers, one wasted
day. This is the lat/lng gap costing real money, not a theoretical concern.

### 46. THE TIMESTAMP TRICK — how to find a sweep without coordinates

`Precise Fiber` has no city and no lat/lng, but it HAS `Captured At`. The hunter sweeps one
area at a time, so **a capture window IS a geography**. Filter by timestamp prefix and you
recover the whole sweep:

```
=COUNTIFS('Precise Fiber'!C:C,"2026-08-17*",'Precise Fiber'!B:B,"ORANGE")
=QUERY('Precise Fiber'!A:C,"select A,C where B='ORANGE' and C starts with '2026-08-17'",0)
```

This is the workaround for 8,264 gold dots with no coordinates. Use it until the writer is
patched.

**2026-08-17 alone: 14,116 rows — GREEN 10,074, ORANGE 4,042.** Three areas in one day:
- 13:22-13:26 NW Houston / Tomball (Schroeder Rd, Wimbledon, Camborne, Hwy 249, Vintage Park)
- 14:03-14:04 Palmer Springs / Bonnabel / Tomball Pkwy
- 15:03-20:52 **Angleton**
Plus an East Houston green block (Bucroft, Fillmore, Cargill, Munn, Pillot, Chadwick).

**4,042 gold from one day = half the entire gold inventory. Twelve have been worked.**

### 47. MDU clusters found in the Aug 17 capture — the non-linear lever

- **13504 Schroeder Rd** — ~60 ORANGE units at one address (units 1101-5311, plus OFC and
  FITNESS). One property manager.
- **19401 Tomball Pkwy** — another orange apartment cluster.
- **8550 Phelan Blvd, Beaumont** — 26 units, one lat/lng.

One property-manager conversation beats fifty doors. Both Houston clusters are ~20 minutes
from Patrick's own address in 77070.

### 48. Real enrichment results — 18 addresses, ~44 credits (OURS)

**BEAUMONT — Broun St (working-class, 1968 builds, ~$170k)**

| Address | Owner | Wireless, DNC-clear |
|---|---|---|
| 9725 Broun | Andrew Jones | 337-940-2055 |
| 9690 Broun | Raymona Redd | 409-284-6252 |
| 9690 Broun | Elaine Smith | 409-998-0753 |
| 9785 Broun | Justin Loera | 409-728-7108 |
| 9730 Broun | Julio Garcia | 409-225-2984 |
| 9745 Broun | Tracey Lumpkin | all 3 DNC |
| 9825 Broun | Guy Armstrong | wireless DNC |
| 9755 Shepherd | — | no contact record |

**ANGLETON — E Miller St (1950s builds, $185k-308k)**

| Address | Owner | Phone |
|---|---|---|
| 617 E Miller | Bradley Bergerson | 713-419-7892 + 979-583-7087 both clear |
| 708 E Miller | David Dittrich | 979-587-0384 clear — Dow employee, LANDLORD not resident |
| 715 E Miller | Ricky Price | 979-665-9538 clear |
| 603 E Miller | Raul + Veronica Hernandez | 979-864-4698 landline clear — **RAUL6526@ATT.NET** |
| 525 E Miller | Alicia Quintanilla | 979-849-4660 landline clear |
| 404 / 509 / 510 / 713 E Miller | Pousson / Sturdivant / Cato / Simpson | all DNC |
| 201 / 325 E Miller | — | no contact record |
| 606 E Miller | "Thomas Selleck" | 3 conflicting records, out-of-state area codes — BAD MATCH |

**LEAGUE CITY** — Beveridge Roofing LLC, 281-508-2405, 1640 E Main St. Only south-Houston
gold business in the data.

### 49. Market-by-market DNC pattern (OURS, measured)

| Market | Home value | Textable |
|---|---|---|
| Beaumont / Broun St | ~$170k | **5 of 7 = 71%** |
| Angleton / E Miller | $185-308k | **5 of 12 = 42%** |
| Beaumont / Westgate-Shakespeare | $260-306k | **1 of 6 = 17%** |

**DNC registration rises with home value.** Working-class 1960s housing is reachable by
phone; $300k subdivisions are not. Do not assume a market is a text market — measure ~6
addresses first, then decide text vs door.

Caveat on the earlier "Angleton is 17%, door-only" call: that was a 6-address sample and it
was wrong. The next 6 gave 3 clean wireless. **Sample at least 12 before calling a market.**

### 50. Enrichment cost reality (OURS)

`enrich_address` charges **1 property credit + 1 per PERSON returned**:
- no contact record -> 1 credit
- single owner -> 2 credits
- multi-owner / duplicate records -> 3-6 credits (1370 Shakespeare cost 6)

**Measured average 2.83 credits/address.** Budget ~40% above the naive 2/address estimate.
**Do NOT pass the `fields` parameter to `enrich_latlng` — it fails with "Reverse geocode
enrichment failed."** Omit it.

`enrich_address` works when there are no coordinates (which is most of the gold) and returns
lat/lng in the response — so it doubles as a way to backfill coordinates.

### 51. Warmest-lead signals worth filtering on

- **Email domain @att.net** — already an AT&T customer. Raul Hernandez is the clearest
  example in the whole dataset.
- **owner_occupied = true** — the resident decides the internet; a landlord often does not.
- **year_built pre-1970** — copper-era wiring, long-tenure owners.
- **100% equity + long tenure** — owned outright, been there decades, never switched.
- **Landlord flag** (owner_occupied false + is_resident false) — different pitch, and they
  may own multiple units. David Dittrich at 708 E Miller is one.

### 52. Deliverables built this session

- Sheet tab `Beaumont Gold — Aug 2026` — 238 addresses, lat/lng, cluster
- Sheet tab `Angleton Call List — Aug 2026` — 20 E Miller addresses
- Sheet tab `WORK LIST — Beaumont + Angleton` — 29 rows, priority-sorted
- Sheet tab `MASTER LEAD SHEET` — 30 rows, 18 columns, full detail + legend
- Standalone Google Sheet `OPTIMUS PHONE NUMBERS — Beaumont + Angleton`
  (`1sZZdiPj5SseoV3BonAI3tfYHg8KIuJsjTb9bpwlN0Es`) — 11 dialable numbers
- Skill `.claude/skills/fiber-freshness`
- Skill `.claude/skills/gold-dot-workup`

## 2026-08-20 (part 9) — THE CLASSIFIER WAS LYING. Grey dots were being sold as gold.

Patrick caught this by clicking a dot. The sheet said GOLD; the map popup said existing
fiber customer. He was right, and it had been wrong for as long as the code has existed.

### 53. What actually broke

Two paths, same destination.

**Path one — a word beat AT&T's own data.** `classify_status()` in
`optimus/optimus_dot_detect.py` checked for the string "copper" anywhere in the status
text *before* it looked at `curr_ntwrk_bld_type_cd`:

    low = (text or "").lower()
    if "copper" in low:
        return STATUS_COPPER_UPGRADE     # fired first, won every time

AT&T's copper-retirement messaging mentions copper in the status of accounts that are
**already on fiber**. Every one of those became a gold dot.

**Path two — an unhandled return value.** `classify_lead()` returns `"CUSTOMER"` when a
customer's build code is in neither the fiber nor the copper set. That value was missing
from the hunter's status map in `precise_fiber_hunter.py`, so it fell straight through
into path one.

Fixed 2026-08-20: build code is consulted first and a fiber code returns GREY
unconditionally; the text word-match can now only produce gold when there is no account
attached; `CUSTOMER` maps to GREY.

### 54. Why GREY is the right default for an unknown code

An undecodable customer is more likely already on fiber than on copper. A false grey costs
nothing — grey is skipped anyway. A false gold puts a rep on the phone with somebody who
already buys the product, which burns the number and makes us look like we don't know our
own service.

But this cuts both ways and it is worth watching: if AT&T introduces a new *copper*
designation, we are now silently discarding real gold. That is why unknown codes are
logged once each. `optimus/verify_gold_capture.py` counts them from a real capture. Any
code showing up in volume is worth one click on the map to settle it, then a line in
`build_codes.json`.

### 55. Addresses were street-only, and it cost us a whole market

`extract_features()` never read `city`, `state` or `zip` — even though they sit in the
same backend record as the street:

    {"zip":"77598","address":"558 TRESVANT DR","city":"WEBSTER","state":"TX", ...}

So every captured lead was `5415 GURLEY AVE` with no city. Not skip-traceable, and
impossible to tell apart from the same street name in another metro. That is exactly how
the 2026-08-19 sweep nearly got worked as Houston when it was **Old East Dallas**
(32.79, -96.75), 240 miles away. Both extractors now carry city/state/zip and compose a
full address.

### 56. Where the gold actually is — 8,264 dots across four metros, not one

Clustering `Gold Dots` coordinates to 1 decimal place:

| Coords | Dots | Market |
|---|---|---|
| 30.1, -94.2 | 902 | Beaumont |
| **29.7, -95.4** | **769** | **Houston** — Cullen / Reed / Maggie |
| **29.7, -95.3** | **570** | **Houston** — Panay / Jutland |
| 32.8, -97.0 | 381 | Fort Worth |
| 32.7, -97.0 | 314 | Fort Worth / Arlington |
| 32.8, -96.8 and -96.7 | 325 | Dallas |
| 30.1, -93.7 | 50 | Louisiana edge |

The newest captures in the entire file — 2026-08-19 23:38 to 23:55 — are the two Houston
clusters, 1,339 dots. Newer than the Dallas sweep that happened earlier the same morning.
Checking coordinates before spending credits is now a step in the skill, because the sweep
runs off whatever seed the hunter was pointed at, which is not necessarily our market.

### 57. Gold detection only started 2026-08-17

All 8,264 gold dots come from three sweeps: Aug 17 (4,042), Aug 18 (3,202), Aug 19 (1,020).
Every sweep before that reads 100% GREEN across roughly 450,000 rows.

That is the classifier not running yet — **not** evidence those markets have no gold. An
unknown share of that green is copper customers that were never scored. Worth a re-sweep
of the older markets, and worth never saying "that area has no gold" about anything
captured before Aug 17.

### 58. Two Google Sheets traps that produce confident wrong answers

Both cost real time this session.

**`Precise Fiber` column C is TEXT, not a date.** Date-range `COUNTIFS(">="&DATEVALUE(...))`
returns 0 — numbers never match text. And a literal date spine typed into column A gets
auto-converted by Sheets into date serials, so `A2&"*"` becomes `"46174*"` and matches
nothing either. The formula that survives both:

    =COUNTIF('Precise Fiber'!$C:$C, TEXT($A2,"yyyy-mm-dd")&"*")

**Helper columns silently under-fill.** Filling `=LEFT('Precise Fiber'!C2,10)` down 459k
rows populated only ~13k and produced a fabricated census — two dates, zero gold — with no
error anywhere. Always reconcile a census against `COUNTA` and `COUNTIF` on the source
before believing it. The numbers must add up or the census is wrong, not the data.

### 59. What got built

- `optimus/test_gold_pipeline_e2e.py` — 27 assertions through the real capture chain
  (`lead_from_dict` → `_lead_status` → `dot_color` → sheet row), asserting on the row that
  lands rather than an intermediate value
- `optimus/verify_gold_capture.py` — audits a real saved AT&T response
  (`serviceability_raw.json`, written by the hunter once per run) and reports the
  before/after colour split, the false-gold list, and undecodable build codes
- Skill `.claude/skills/new-build-outreach` — newest-sweep census, geography check, batch
  sizing with an opt-out gate, follow-up cadence, reply playbook
- Sheet tab `HOUSTON UNVERIFIED — Aug 19` — 1,339 rows, full addresses, labelled unverified
  because it was written by the pre-fix classifier

### 60. Open, and worth remembering

- **Nothing has been texted from these lists.** Everything currently on the sheet came out
  of the buggy classifier, so it is unverified until a re-sweep or until
  `verify_gold_capture.py` runs against a real capture.
- **The Frontline number is running hot.** A slice of 100 recent unread conversations in
  Frontline Direct (`TXw28sw0Z2rI6tcCDhJY`) had 76 inbound messages, 72 of them a bare
  STOP. That is the most recent slice, not full throughput, but a ratio that lopsided is a
  deliverability problem. Live leads with open opportunities were sitting unanswered
  underneath the pile — Bruce Johnson, Brian Ferguson, Dawn Tester, Brian Allendale,
  Eugene Sandberg, Donald Denham.
- **T-OPTIMUS (`xZj500PjsflIQg2j9f9D`) is outside the connector's location scope** —
  users list fine via the agency endpoint, but `get_location` returns 403. All seven of its
  users are admin; nobody is on role `user`.
- **The live AT&T map is unreachable from the remote session** (proxy 403s
  youachieve.att.com), so classification can only be proven here against records shaped
  like AT&T's payload. Proving it on live data means running `verify_gold_capture.py` on
  the machine that runs the hunter.

## 2026-08-20 (part 10) — THE HUNTER RUNS FROM A DIFFERENT REPO

### 61. Fixes to `optimus-map-tools` do not reach the running hunter

The hunter self-updates on every launch from:

    GH_REPO     = "patricksiado-prog/Go-High-Level-MCP-2026-Complete"
    REPO_BRANCH = "claude/optimus-map-tools-setup-6dcl6o"

That is **not** `patricksiado-prog/optimus-map-tools`. A whole session of fixes was
committed and pushed to the wrong repo and never touched the machine doing the work. The
two copies have also drifted — the deployed `precise_fiber_hunter.py` is ~200 lines
*longer* than the one in `optimus-map-tools`, so they cannot be copied over each other.
Port changes across surgically, file by file, and check which variant is actually live
before assuming a bug is fixed.

Quick way to tell what is really running: the hunter prints `CODE UPDATED <date>` and a
`GOLD CAPTURE ON` line at startup. That date is the deployed build.

### 62. The real live bug was NOT the one found by reading `optimus-map-tools`

The deployed `classify_wire()` called every customer GOLD unless it could confirm fiber:

    if code and any(c in code for c in _BLD_CODES["fiber"]):
        return "customer"          # GREY
    return "copper_upgrade"        # GOLD -- everything else

So a customer became gold whenever the build code was **missing entirely** or was any
value not in the fiber list. Every new AT&T fiber designation lands there.

That default was deliberate. It replaced an older rule that required an explicit copper
code and produced *zero* gold — the pendulum swung from missing all gold to inventing it.
The fix keeps confirmed-copper as gold, confirmed-fiber as grey, and sends undecodable
customers to grey, with `OPTIMUS_UNKNOWN_CUSTOMER=gold` to swing it back if the telemetry
shows those codes really are copper.

**Lesson worth keeping:** when a classifier is wrong, check which direction it was last
"fixed" in. This one had been over-corrected, not under-corrected.

### 63. The map is the ground truth, and it is one click away

Patrick's photo of the live Houston map: roughly 170 green, 20 orange, 16 blue-grey — so
orange is about **11%** of dots. Our captures for the same period: **32.2%** (Aug 18) and
**31.3%** (Aug 19). Three times too much gold, which is what sent us looking.

Counting dots off a photo is rough, but it was accurate enough to point at a real defect
and it cost nothing. Clicking a single dot and reading the popup settles any individual
case outright.

### 64. Telemetry beats archaeology

Every customer dot is now counted by branch and printed at exit (`atexit`, so it survives
the Ctrl-C that normally ends a sweep): green / confirmed-fiber / confirmed-copper /
unknown-code / no-code, the undecoded codes themselves, and what share of customers were a
guess rather than a decode. If that share is high the gold number is not trustworthy.

This is the thing that would have caught the defect on day one instead of after
thousands of contaminated rows.

### 65. Silent failure is the recurring theme this session

Three separate instances, same shape:

- `self_update()` ran `git fetch` and `git reset` with `capture_output=True` and never
  checked either exit code — a wrong branch or expired credential left the hunter running
  old code while printing nothing.
- A Sheets helper column filled ~13k of 459k rows and produced a confident, fabricated
  census with no error anywhere.
- `classify_lead()` returning `"CUSTOMER"` was absent from a lookup table and fell through
  to a text heuristic instead of raising.

None of them threw. All three produced plausible-looking wrong answers. Where something
can fail quietly, make it say so.

## 2026-08-20 (part 11) — WHAT SHIPPED, WHAT THE NUMBERS ARE NOW, AND WHAT IS STALE

### 66. The deployment record

Fix for the grey-as-gold defect shipped to the repo the hunter actually pulls from:

| | |
|---|---|
| Repo | `patricksiado-prog/Go-High-Level-MCP-2026-Complete` |
| Branch | `claude/optimus-map-tools-setup-6dcl6o` |
| Commit | `d70dff2` |
| Takes effect | next hunter restart (it self-updates on launch) |

Files touched: `optimus/precise_fiber_hunter.py`, `optimus/optimus_api_capture.py`, and
`optimus/verify_gold_capture.py` added.

**Confirming it is actually live** — the startup banner prints `CODE UPDATED <date>`, and
a run now ends with a `DOT CLASSIFICATION THIS RUN` block. If that block does not appear,
the fix is not running.

**Rollback, no code edit needed:** `set OPTIMUS_UNKNOWN_CUSTOMER=gold` restores the old
"every undecodable customer is gold" behaviour. Only worth doing if gold collapses AND the
telemetry shows the undecoded codes really are copper.

`OPTIMUS_REPO_BRANCH` now overrides which branch the hunter self-updates from.

The same fixes exist in `optimus-map-tools` on `claude/lead-gen-software-research-brho9a`
(`18558bc`, plus `test_gold_pipeline_e2e.py`), but that repo is **not** what runs.

### 67. Numbers as of 2026-08-20, superseding earlier figures in this file

| | |
|---|---|
| `Precise Fiber` rows | **464,082** (was 459,471 at session start — the hunter is live) |
| Total ORANGE | **9,652** (part 6 said 8,264 — that was hours ago) |
| Total GREY | **0** — by design, the writer never writes grey rows |
| `Gold Dots` rows | **3,328** |

Daily split for the three most recent sweeps:

| Date | Total | Green | Orange | Orange share |
|---|---|---|---|---|
| 2026-08-18 | 9,942 | 6,740 | 3,202 | 32.2% |
| 2026-08-19 | 7,646 | 5,252 | 2,394 | 31.3% |
| 2026-08-20 | 96 | 82 | 14 | 14.6% |

**Two corrections to things written earlier today:**

- Part 8 recorded the 2026-08-19 sweep as 3,131 rows / 1,020 orange. The sweep kept
  running after that count. It is **7,646 / 2,394**. Any figure taken from a live tab is a
  snapshot, not a total.
- I called the newest build "Dallas". Wrong — the newest captures in the file are
  **2026-08-19 23:38–23:55, both Houston clusters**. The Dallas sweep ran earlier the same
  morning (09:31). Sort by timestamp, not by whichever sweep you looked at first.

The 14.6% for today is **96 rows — one or two viewports.** It is not evidence the fix
landed, and it cannot be: the fix was not deployed when those rows were captured.

### 68. `GOLD — CLEAN` — the working gold list

Built from `Gold Dots`, deduped, static values. `Gold Dots` itself left untouched as the
raw feed. Columns: `Full Address | Street | Market | Home Turf | Latitude | Longitude |
Captured At | Status`. Reconciles exactly: 3,328 source = 3,328 clean + 0 dupes + 0 bad
coords, zero blank markets.

| Market | Dots | Home turf |
|---|---|---|
| HOUSTON TX | 1,344 | yes |
| BEAUMONT TX | 914 | yes |
| FORT WORTH TX | 695 | no |
| DALLAS TX | 325 | no |
| ORANGE TX | 50 | yes |

**2,308 of 3,328 are workable turf.** The other 1,020 are DFW — real dots, nobody to knock
them. Market is derived from coordinate bands, not from AT&T, because the captured
addresses were street-only.

### 69. Everything built today is UNVERIFIED

Every row on `GOLD — CLEAN`, `HOUSTON UNVERIFIED — Aug 19` (1,339 rows) and
`NEW BUILD 2026-08-19` was written by the pre-fix classifier. The tabs are labelled that
way on the sheet. **Nothing has been texted from any of them.**

What turns them into a real call list, in order: restart the hunter so the fix is live,
re-sweep the Houston clusters, check the classification report's guess percentage, then
enrich and sample 12 for DNC rate before any send.

`optimus/verify_gold_capture.py` reads the raw AT&T response the hunter saves
(`serviceability_raw.json`, written once per run, sits next to the script) and prints the
before/after colour split plus every undecodable build code. That is the measurement that
says how contaminated the existing lists actually are — it has to run on the machine that
runs the hunter, because the dealer map is unreachable from the remote session.

## 2026-08-20 (part 12) — GIT IS NOT INSTALLED ON THE HUNTER PC. THE RAW FALLBACK IS THE REAL UPDATER.

Found from Patrick's launch console, which said more than any amount of code reading:

    (git update unavailable: [WinError 2] The system cannot find the file specified
     -- using HTTPS raw fallback)
    (auto-update: refreshed core files over HTTPS -- no git needed)

### 70. The machine that runs the hunter has no git

So `self_update()`'s git path throws instantly and control falls to `_raw_refresh()`,
which downloads files one by one over plain HTTPS:

    https://raw.githubusercontent.com/{GH_REPO}/{GH_BRANCH}/optimus/{file}?cb={timestamp}

Same repo, same branch, so the push target from part 11 is right. But this means the
`self_update()` git hardening is **mostly irrelevant on Patrick's box** — it never reaches
those lines. The loud-failure banner still matters for any machine that does have git.

### 71. `_CORE_FILES` is the deploy manifest — anything not in it NEVER updates

    _CORE_FILES = ("precise_fiber_hunter.py", "optimus_dot_detect.py",
                   "optimus_api_capture.py", "hunter_fixes.py",
                   "backend_classifier.py", "build_codes.json")

Six files. That is the entire auto-deploy surface on a machine without git.

**`verify_gold_capture.py` is NOT in that list, so it will never arrive by auto-update.**
Pushing it to the branch does nothing for the hunter PC. To run it there it has to be
downloaded by hand, or added to `_CORE_FILES`. Same applies to any future tool — if it is
not in that tuple, it does not ship.

### 72. `git fetch` here was serving a STALE view, and it cost 25 failed pushes

`git fetch` inside this session kept reporting the branch tip as `21d6f5d` while the
server was actually well past it. Every push was rejected as non-fast-forward against a
tip git swore was an ancestor — a flat contradiction that only makes sense if the fetch
is cached.

**Trust these instead of `git fetch` on this repo:**

    git ls-remote https://github.com/<owner>/<repo> refs/heads/<branch>
    curl -sS "https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>?cb=$(date +%s)"

The curl is the better of the two, because it fetches **the exact bytes the hunter
downloads** rather than something merely equivalent. Fetching the real commit SHA
explicitly (`git fetch origin <sha>`) then branching from `FETCH_HEAD` is what finally
worked.

### 73. BUILD_DATE lied, and I told Patrick to trust it

Part 11 says: "the startup banner prints `CODE UPDATED <date>` — that date is the deployed
build." Patrick's console then showed `2026-08-18` and I told him to stop launching.

**That was wrong and it cost him a delay.** The classifier fix HAD landed; only the
`BUILD_DATE` bump had not, because it was a separate later edit that never got pushed.
So the marker reported an old date while running new code.

Two things to keep from that:

- **A version marker is only a signal if it moves in the same commit as the behaviour.**
  A constant that has to be remembered separately will eventually disagree with the code,
  and then it is worse than having no marker at all.
- **The real proof of the fix is the `DOT CLASSIFICATION THIS RUN` block at exit**, not
  the banner — it is produced by the new code path itself and cannot be faked by a stale
  constant.

`BUILD_DATE` is now `2026-08-20` (commit `f8ed33c`), and the banner also names the rule in
force. Note the raw CDN can serve the previous copy for a few minutes after a push even
with the cache-bust parameter, so an immediately-following launch may still print the old
date.

### 74. The fix is confirmed live — verified against the delivered bytes

Downloaded the exact file the hunter pulls and ran its classifier:

| Case | Result |
|---|---|
| `fttn-bp` copper customer | ORANGE |
| `fttp-gpon` + "copper retirement" in status text | GREY |
| unknown code `xgspon` | GREY |
| no BAN, build `unavailable` | GREEN |
| composed address | `4314 PHLOX ST, HOUSTON TX 77051` |

`_WIRE_COUNTS`, `wire_classification_report` and the `atexit` registration are all present
in the delivered file. `_UNKNOWN_CUSTOMER` defaults to `grey`.

**Correction to part 11:** the commit recorded there as `d70dff2` was reset off the branch
at one point and had to be restored. Current state is `f8ed33c`.

### 75. `serviceability reply 301` was in Patrick's launch output

Already noted in the run log from 2026-08-19 — 301 means AT&T redirected the data call to
login, and nothing lands, green or gold. It appeared again on this launch. If a run comes
back with unusually few leads, check this before suspecting the classifier. It is an
auth/session problem, not a code problem.

### 76. What to read off the next run

1. Does the `DOT CLASSIFICATION THIS RUN` block print at all? If not, the fix is not
   running.
2. What percentage of customer dots were "a guess, not a decode"? High means the gold
   number still is not trustworthy.
3. Which undecoded build codes appear, and how often? Any in volume is worth one click on
   the dealer map, then a line in `build_codes.json`.
4. Does the orange share move from ~32% toward the ~11% the live map shows?
5. If gold collapses to near zero, `set OPTIMUS_UNKNOWN_CUSTOMER=gold` restores the old
   behaviour in one env var — but only do that if the telemetry shows those codes really
   are copper.

## 2026-08-20 (part 13) — THE THREE UPDATE ERRORS, AND THE ONE COMMAND THAT PREVENTS ALL OF THEM

Three times in one day a fix was believed live when it was not. Same class of mistake
each time: **trusting a local view of the code instead of the delivered bytes.**

### 77. Error 1 — pushed to the wrong repo

A full session of fixes went to `patricksiado-prog/optimus-map-tools`. The hunter pulls
`patricksiado-prog/Go-High-Level-MCP-2026-Complete`. `git log` was clean, the push
succeeded, the tests passed — and nothing reached the machine doing the work.

**Why it happened:** the working directory was the wrong repo, and nothing in the normal
git workflow says "this is not the repo that runs."

### 78. Error 2 — the commit was reset off the branch, and `git fetch` lied about it

Commit `d70dff2` landed, then the branch was reset back past it. Worse, `git fetch` in
this environment kept reporting the tip as `21d6f5d` while the server was well past that.
25 pushes were rejected as non-fast-forward against a tip git itself insisted was an
ancestor — a flat contradiction that only makes sense if the fetch is cached.

**Why it happened:** `git fetch` / `origin/<branch>` was treated as ground truth. It is
not, in this environment.

Reliable instead:

    git ls-remote https://github.com/<owner>/<repo> refs/heads/<branch>
    git fetch origin <full-sha> && git checkout -B work FETCH_HEAD

### 79. Error 3 — BUILD_DATE reported old code while running new code

The banner printed `CODE UPDATED 2026-08-18` after the classifier fix had shipped, because
the `BUILD_DATE` bump was a separate later edit that had not been pushed. Patrick was told
to stop launching on the strength of that marker. He had the fix the whole time.

**Why it happened:** a version marker that has to be remembered separately from the change
it describes will eventually disagree with it — and a marker that disagrees is worse than
no marker, because it is trusted.

Related: `_CORE_FILES` is the **entire** deploy manifest on a machine without git, and the
hunter PC has none. `verify_gold_capture.py` sat outside that tuple, so pushing it did
nothing for the one machine that needed it. Both audit tools are now in the list.

### 80. THE PREVENTION — `deploy_check.py`

    cd optimus && python deploy_check.py

Downloads every core file from the exact raw URL the hunter downloads, and diffs it
against the local copy.

    FILE                         STATUS     NOTE
    precise_fiber_hunter.py      IN SYNC    a91c3f0be2d1
    verify_gold_capture.py       IN SYNC    c895430f41e6
    deploy_check.py              NO REMOTE  HTTP 404

`IN SYNC` on every row means a launch runs exactly the local code. Anything else means it
does not, **whatever git says**. `--show BUILD_DATE` prints the matching line from the
remote copy so the marker can be read without launching.

It catches all three errors at once: wrong repo shows as universal drift, a reset branch
shows as drift on the reset files, and a stale marker is visible in the `--show` line.

**One caveat that is not a bug:** `raw.githubusercontent.com` serves the previous copy for
a few minutes after a push even with a cache-bust parameter. A `*DRIFT*` immediately after
pushing usually means the CDN, not a failed push. Re-run after a minute; if it persists,
the push genuinely did not land.

### 81. The habit worth keeping

Push, then run `deploy_check.py`, then tell Patrick it is live. Never in the other order.
"I pushed it" and "it is running on your machine" are different claims, and this session
proved the gap between them three separate times.

## 2026-08-20 (part 14) — THE ~3000 CAP IS THE REAL LIMIT ON COVERAGE, NOT ZOOM

### 82. How far out can we zoom? Until a viewport holds ~3000 addresses. No further.

AT&T's serviceability reply carries **at most ~3000 leads** per "Search this area"
(documented in `backend_classifier.py`; four tabs in the sheet — `Fiber Scout`,
`Backend Capture`, `Backend Analysis`, `Fresh Leads` — sit at exactly 3,000 rows, which is
the fingerprint of a truncated reply, not a coincidence).

**That cap, not the zoom control, is what limits coverage.** Past the point where a
viewport contains ~3000 addresses the response silently truncates and the rest of that
ground is never captured. Nothing errors. The sweep looks healthy and just quietly misses
houses.

So zooming out past that point **covers more map with fewer addresses per acre** — worse
than covering less ground properly. `--zoom-out` and `--survey-out` already exist; the
question was never whether we can zoom out, it is where the ceiling sits.

**The tuning procedure:** zoom out while `Radius mi` grows and `Leads` stays clear of the
cap. Stop the moment rows start flagging `NEAR THE 3000 CAP`. That is the widest useful
viewport, and it will differ between dense Houston blocks and sparse rural grid.

### 83. `miles_from_claim` measures coverage directly

Every lead in the payload carries `miles_from_claim` — its distance from the search
centre. The **max** across a reply is therefore the actual radius that one search covered.
Now logged as `Radius mi` in `Backend Comm`, so how much ground a viewport buys is
measured rather than inferred from zoom presses.

Two numbers together tell the whole story: **radius up + leads below cap = good, cover
more. Radius up + leads at cap = losing addresses.**

### 84. Backend Comm tab — final schema

`Time | Host | Area | Kind | Status | Bytes | ms | Leads | Green | Gold | Grey |
Radius mi | URL | Content-Type | Note`

Rows written for every reply the sniffer treats as data, **including the non-200s that
used to be printed and discarded** — which is how `serviceability reply 301` stayed
invisible for so long. 301 = AT&T bounced the data call to login and nothing lands, green
or gold. Also logs a 200 that decodes to zero leads (payload shape changed, top-level keys
attached) and one row per distinct endpoint on first sight.

### 85. Console readings from the 2026-08-20 launch

    Fiber green addresses (Precise Fiber) : 464,899
    Scraped businesses (Maps Businesses)  :  32,615
    MATCHES - callable (unique phone)     :   3,771
    MATCHES - Fiber Green Biz rows        :   6,150
    Upgrade Orange Biz matches            :      36
    (serviceability reply 301 -- skipping, map keeps moving)

**36 gold businesses against 3,771 callable — under 1%.** Worth re-measuring once the
fixed classifier has run, because the old classifier was inflating gold, not suppressing
it, so the true figure may be lower still.

The 301 appeared again on this launch. The map was visibly loading dots, so it is likely a
pre-login call rather than a broken session — but that is exactly the guess the tab now
replaces with a fact.

### 86. Efficiency observations, not yet acted on

- **Both extractors run on every payload.** `extract_leads_from_json(data)` runs, then
  `_extract_features(data)` runs over the same object and appends to the same list, so
  every lead is built twice and deduped later. The `ms` column measures the cost.
- **The raw JSON is rewritten to disk on every capture** — a synchronous multi-megabyte
  `json.dump` in the hot path, every viewport that yields leads. Deliberate (so the file
  reflects the current area) but it does not need to be every time.
- Writes are already off the motion (a separate worker ships to the sheet, panning never
  waits), so sheet latency is not the bottleneck. The remaining costs are the pacing
  sleeps and the double extraction.
- **Mapbox angle, unproven:** if the dots ride in vector tiles, `querySourceFeatures` can
  read loaded features in-page — including ones hidden by styling — with no network wait
  and no panning. The endpoint-discovery rows will show whether tiles carry dot data or
  whether the serviceability JSON is the only source. Do not act on this until the tab
  says which.

### 87. Do not let observability change what it observes

Two defects were caught in pre-flight review of the telemetry itself, both in the capture
hot path:

- Counting the colour split for the log called the same classifier the writer calls, so
  every dot was tallied **twice** in `_WIRE_COUNTS` and the exit report would have come
  out doubled. Now snapshotted and restored around the logging pass.
- Endpoint de-duplication keyed on base URL, but tiles are addressed `/z/x/y`, so every
  tile was a distinct path and would have logged as a new endpoint — hundreds of rows a
  sweep. `_endpoint_key()` collapses the numeric segments so a whole tile layer is one row.

Both would have corrupted precisely the data being collected. Telemetry added to a hot
path needs the same review as the code it measures.

## 2026-08-20 (part 15) — THE CSV EXPORT CARRIES CARRIER AND USAGE. TWO BRAIN ENTRIES WERE WRONG.

A DealMachine contacts export (130 Beaumont contacts, 2026-08-20) settles two things this
file previously recorded incorrectly, and exposes a mistake in how I read it.

### 88. CORRECTION to §12 — DealMachine DOES give us carrier

§12 says: *"DealMachine has NO carrier data — the 'AT&T cell' angle does not work... There
is no carrier field."* That was checked against the **API** `fields` endpoint.

**The CSV export has `phone_1_carrier`, `phone_2_carrier`, `phone_3_carrier`.** Values are
real: `AT&T Mobility`, `Verizon Wireless`, `T-Mobile`, `Metro PCS`.

So the pitch Patrick asked for months ago — *"hi Bob, you have AT&T cell and AT&T DSL,
upgrade to fiber"* — **is data-driven after all.** Just export the list rather than pulling
it through the API.

On this file: **23 of 61 reachable contacts are on AT&T Mobility.** An AT&T wireless
customer at a fiber-eligible copper address is the warmest combination in the dataset —
already paying AT&T for phone, already on AT&T copper internet, fiber live on the street,
and the bundle discount is real (−$5/line, or 20% off).

### 89. CORRECTION to §20 — we CAN tell whether a line is alive

§20 says: *"DealMachine tells us line TYPE and DNC status. It does NOT tell us whether a
number is still connected."*

The export carries `phone_N_activity_status` and `phone_N_usage_2_months` /
`phone_N_usage_12_months`. Usage values are graded:
`Very Heavy Usage`, `Heavy Usage`, `Moderate Usage`, `Light Usage`, `Minimal Usage`,
`No data available or no usage in the last 2 months`.

On the 61 reachable: **31 are Heavy or Very Heavy** — those are demonstrably live lines,
not just DNC-clear ones. That closes the exact gap §20 flagged as the reason our "textable"
percentages overstated real deliverability.

`phone_N_prepaid_indicator` is also present (`PREPAID`), which §12 correctly listed as a
filter — prepaid skews lower income, so lead with price rather than speed.

### 90. MY MISTAKE — there are THREE phone columns and I read one

I analysed `phone_1` only and reported 43 textable. Patrick sent a screenshot of columns
U–Y showing `phone_2_carrier` populated, which is what caught it.

Reading all three:

| | present | wireless | DNC | clear wireless |
|---|---|---|---|---|
| phone_1 | 129 | 103 | 60 | 43 |
| phone_2 | 95 | 47 | 24 | 23 |
| phone_3 | 51 | 22 | 9 | 13 |

**Contacts with at least one clean wireless number: 61 of 130, not 43.** Eighteen people
were rescued purely by looking past the first column — a **42% larger working list** from
data already paid for.

**A contact is only unreachable when ALL THREE numbers fail.** Never judge one on
`phone_1` alone. The same almost certainly applies to every earlier enrichment batch in
this file, so the historical "textable %" figures are understated.

### 91. The ranking that comes out of it

1. **AT&T cell + Heavy/Very Heavy usage** — 10. Warmest in the file.
2. **AT&T cell**, any usage — 13
3. **Heavy usage**, other carrier — 21
4. Clean wireless, everything else — 17

Also in the file: 26 landline DNC-clear (call only, never text — Twilio 30006) and 60
where every number is DNC (door knock / CREATE REFERRAL only; DNC blocks calls too).

All 130 **property** addresses are Beaumont 77706, mostly Ivanhoe Ln and Afton Ln. The
Edmond OK / Austin / Baton Rouge / Arizona entries are landlord **mailing** addresses — a
reminder to segment on `associated_property_address_full`, never on
`primary_mailing_city`.

### 92. Where they were loaded, and the open question

Contacts are being created in **Frontline Direct (`TXw28sw0Z2rI6tcCDhJY`)** tagged
`beaumont fresh` / `att cell` / `textable` / `gold dot`, because the connector token
**cannot reach T-OPTIMUS** (`xZj500PjsflIQg2j9f9D` returns 403 on both `get_location` and
`ghl_list_workflows`). The Active Systems block at the top of this file says to use
T-OPTIMUS and not Frontline Direct — that instruction cannot currently be followed by any
automated tool. Frontline Direct does have a published `Frontline — Power Dialer Queue`
plus live `Customer replied STOP` handling. **Which location Dave actually dials needs
settling**, and if it is T-OPTIMUS then that location has to be added to the connector's
scope before any of this can be automated.

## 2026-08-20 (part 16) — 100 DEALS A DAY: THE ARITHMETIC

Worked from our own measured numbers, not industry averages. The answer is that the phone
channel cannot get there, and the reason is worth understanding precisely.

### 93. The phone channel has a hard ceiling, and it is DealMachine

> **SUPERSEDED 2026-08-21 — see §107.** The 2.83 credits/address below is WRONG; the
> measured figure with contacts is ~6. Every number in this section is roughly 2x too
> generous. The conclusion (phone cannot reach 100/day) holds and gets stronger.

30,000 exports/month ÷ 2.83 credits/address = **10,601 addresses/month = 353/day**. At the
measured 47% reachable (all three phone columns), that is **166 reachable contacts/day**.

| Close rate | Deals/day |
|---|---|
| 2% | 3.3 |
| 5% | 8.3 |
| 10% | 16.6 |

**Even at a 10% close on every reachable contact, the phone channel tops out around 17
deals a day.** To reach 100:

| Close rate | Credits/month needed | vs. the 30,000 cap |
|---|---|---|
| 2% | 904,672 | **30x** |
| 5% | 361,869 | **12x** |
| 10% | 180,934 | **6x** |

Upgrading the plan does not close a 6–30x gap; the largest published tier is 150,000. So
**100/day is not reachable through skip-traced phone numbers at any plan we can buy.**

### 94. Door knocking has no cap, because map addresses are free

This is the reframe that matters. **DealMachine credits buy a PHONE NUMBER. The dealer map
gives the ADDRESS for nothing.** We hold 464,900 captured addresses and ~9,650 gold. A rep
walking a street spends zero credits.

| Doors/rep/day | Close | Deals/rep/day | Reps for 100/day |
|---|---|---|---|
| 40 | 5% | 2.0 | 50 |
| 60 | 5% | 3.0 | 33 |
| 60 | 10% | 6.0 | **17** |
| 80 | 10% | 8.0 | **12** |

Fiber D2D tops out at 20–30% for good teams and 2–5% for bad ones, and the research says
the difference is **door selection** — which is the one thing we are genuinely good at.
A gold dot is a pre-qualified copper customer on a 2029 forced migration.

> **SUPERSEDED 2026-08-21 — see §120-121.** Green pays $500, gold $140. Gold is a
> freshness signal, not the target. Work the GREEN inside a gold cluster.

**So 100/day is a hiring problem with a data advantage, not a data problem.** Somewhere
between 12 and 33 competent knockers, pointed at gold, with the copper-retirement line.

### 95. Reality check on the multiple

Best month this operation has ever had: **130 deals / 23 days / 11 reps = 5.7/day**.
Today: Dave dialing plus one VA. **100/day is 18x the best month ever recorded here.**

That is not an argument against the goal. It is an argument for naming the actual
sequence, because 18x does not arrive by working the current motion harder.

### 96. The order that gets there

1. **Prove one gold dot closes.** Still never done — §43. 22 replied-yes, 0 closed. Until
   a single gold dot converts, every projection above is arithmetic on an unmeasured rate.
   50 leads, same-day call on every reply, one week, ~150 credits.
2. **Fix the 5→6 leak before buying anything.** Seven of 22 raised hands went DND while
   waiting. That is the cheapest deal-per-dollar available and it needs no new leads.
3. **Work MDUs first.** 13504 Schroeder Rd is ~60 orange units behind one property
   manager; 8550 Phelan is 26. **100 deals is 1.7 Schroeder-sized wins.** Nothing else in
   the dataset has that shape.
4. **Then hire knockers**, because that is the only uncapped channel, and route them with
   gold dots rather than a territory map.
5. **Keep the phone channel for speed-to-lead**, not volume — it is 166 contacts/day of
   the *warmest* leads (AT&T carrier + heavy line usage), which is exactly the right use
   of a capped resource.

### 97. What would actually change the ceiling

- **Attribution.** Three fields — `run_id`, `dot_color`, `closed_date` — turn every number
  above from an estimate into a measurement. Without them nobody can tell which of these
  five steps is working. Still not built after four months (§44).
- **The 60 DNC contacts per 130 are not dead**, they are door-only. Nearly half of every
  enriched batch is a door lead we currently discard.
- **Business gold.** 36 Upgrade Orange Biz matches against 3,771 callable — under 1%. A
  business fiber deal is worth multiples of a residential one, and that segment is
  essentially unworked.

## 2026-08-20 (part 17) — THE MISSION, STATED PROPERLY

Patrick, verbatim: *"find the 6000 new fiber addresses that are getting turned on each
day, notify them and give them fiber. lots of customers are just waiting for it. we can
sign them up very easily."*

**This is the actual business, and it is a better motion than anything else in this file.**
Everything above — gold dots, enrichment, DNC filtering, the dialer — is machinery in
service of it. Write it at the top of every plan from here.

### 98. Why "waiting for it" changes the sale completely

Every other play here is an interruption. This one is a **delivery**.

A household that watched the orange conduit go in, checked availability, got told "not
yet," and then waited — that person is not a prospect being pitched. They are a customer
whose order has been sitting unplaced. The research supports it: AT&T takes **30%+ within
12 months** in new fiber markets, well above the 9-19% industry norm, and roughly
three-quarters of a neighbourhood's lifetime penetration happens in year one.

**The whole advantage is being there on day one, before AT&T's own retention team gets to
them for free.** Speed here is not a nicety, it is the entire edge.

### 99. Is 6,000/day the right number? Roughly, nationally — and it does not matter

| Source | Passings/yr | Per day |
|---|---|---|
| AT&T 2026 build guidance | 4,000,000 | 10,959 |
| AT&T steady-state target | 5,000,000 | 13,699 |

So **6,000/day is conservative nationally** — about half AT&T's own run rate. Our
footprint is the fraction that matters: Houston metro at a rough 4% share works out to
**400-550 new addresses lighting up per day**, and that is the number to chase. It is also
a much friendlier number: 500/day is one VA and a text template, not an army.

### 100. THE MECHANISM — we already have it and are not using it

**The dealer map only plots addresses where fiber is AVAILABLE.** That single fact makes
the newly-lit list computable without any new data source:

> **An address that appears in today's sweep but did NOT appear in the previous sweep of
> the same ground is an address that lit up in between.**

First-seen timestamp ≈ light-up date, bounded by how often we re-sweep. This is delta
detection, flagged back in §9 as the highest-value automation available, and still not
built.

**The blocker is not capability, it is that we never re-sweep the same ground.** The
hunter goes somewhere new each run, so almost every row is a first sighting and "new to
us" cannot be told apart from "new to the world."

### 101. What has to be built — smallest version that works

1. **A zone registry.** `zone_key (lat/lng rounded) | first_swept | last_swept | sweeps |
   address_count`. Without it there is no way to know which ground qualifies for a delta.
2. **Re-sweep on a cadence.** Weekly over ground already swept once. Only the second and
   later passes produce the signal.
3. **A `New Fiber Today` tab.** Addresses whose first-seen date is today AND whose zone
   was swept at least once before. That tab IS the product.
4. **Same-day outreach.** A newly-lit address is worth multiples of a week-old one.
   Anything that sits gets worked by AT&T's own funnel first.

Also worth measuring on the first re-sweep, because nobody knows it yet: **how many
addresses actually appear per re-sweep of the same ground.** That number tells us whether
this is 500/day in our footprint or 5. Everything else in this section is arithmetic on an
unmeasured rate until then.

### 102. The pitch writes itself, and it is not a pitch

> "Fiber went live on your street this week. You'd checked before and it wasn't
> available yet — it is now. Want me to get you set up?"

True, timely, and it lands as news rather than a sales call. It also side-steps the price
trap entirely: nobody haggles over a thing they have been waiting for. Still never quote a
flat figure — "in the $20s to $30s for the first year, I'll confirm your exact price
before anything is ordered."

**Green dots matter here in a way they do not elsewhere.** For the copper-upgrade play
gold is the easy sale. For *this* play a green dot is somebody with no AT&T account who
now has fiber available — exactly the person who was waiting. The newly-lit list will be
mostly green, and that is correct, not a defect.

### 103. Why this beats the 100/day plan in part 16

Part 16 concluded 100/day needs 12-33 knockers because the phone channel is capped. This
changes that arithmetic, because a newly-lit address is a *fundamentally warmer* lead than
a cold gold dot:

- It needs **no DealMachine credits to find** — the map is the source.
- It converts at a rate closer to AT&T's own 30% first-year take than to our measured 3.7%
  on cold residential text.
- It is **self-replenishing daily**, so it is a standing route, not a list that depletes.

**500 newly-lit addresses/day at even a 10% same-week close is 50 deals/day from one
data feed.** That is the closest thing to a 100/day path in this entire file, and the only
missing piece is re-sweeping ground we have already covered.

## 2026-08-20 (part 18) — THE DAILY BRIEF

Patrick: *"add that to my daily."* The newly-lit feed is the lead item, not an extra.

### 104. What goes in, in this order

**1. NEW FIBER TODAY — the lead item.**
Run `optimus/new_fiber_today.py`. Report:
- addresses newly lit since the last brief, split by colour
- the top streets by count
- how many are on already-known streets (**HIGH/MEDIUM confidence**) vs new ground
- **whether any ground was actually re-swept.** If nothing was, say so plainly — the
  count is zero because we did not look, not because nothing lit up. Never let a zero
  read as "the market is dry."

**2. Unworked positives, by name.** Anyone who replied and has not been called back.
This is the 5→6 leak (§39) and it outranks every new lead in the brief.

**3. Yesterday's numbers.** Sent / delivered / replied / STOP / closed, per `close-rate`.
Flag it loudly if STOPs cross 20% of inbound — that is a burning number, not a slow day.

**4. Hunter health.** Did it run? Did `DOT CLASSIFICATION THIS RUN` print? What share of
customer dots were a guess rather than a decode? Any 301s in `Backend Comm`?

**5. Everything else** — fitness/calories from the LIFE!! sheet, verse, AA, quote.

### 105. Why the fiber item leads

It is the only item that is **perishable**. A newly-lit address is worth multiples on day
one and decays as AT&T's own funnel reaches them. Yesterday's opt-out rate will still be
true next week; today's newly-lit list will not.

### 106. Honest constraint on scheduling

A cron created inside a Claude session is **session-only and expires after 7 days**. It is
not a daily email. Anything that must survive belongs in the hunter's own scheduler or a
Task Scheduler entry on the machine that runs it, calling `new_fiber_today.py --write`.

Until that exists, the brief is: run the script, read the `New Fiber Today` tab, write the
summary. Do not describe a session cron to Patrick as if it were durable infrastructure.

## 2026-08-21 (part 19) — OUTSIDE RESEARCH: WHAT THE INDUSTRY ACTUALLY DOES, AND THE ONE NUMBER IN PART 16 THAT WAS WRONG

Everything below is sourced from outside this operation and cross-checked against our own
measurements. Where the two disagree, both are shown. Read §107 first — it changes the
arithmetic in part 16.

### 107. CORRECTION: enrichment costs ~6 credits/address, not 2.83

Measured today via `estimate_cost=true` on a real query (Beaumont 77706, senior +
owner-occupied, `contact_audience: owners`):

```
25 properties  ->  150 credits   =  25 property credits + 125 people credits
```

**That is 6 credits per address, not 2.83.** The 2.83 figure counted property credits and
under-counted people credits; senior households carry ~5 people on record apiece.

Consequences, all of which make part 16's conclusion *more* true, not less:

| | Old (2.83) | Real (~6) |
|---|---|---|
| Addresses per 30,000/month | 10,601 | **~5,000** |
| Addresses/day | 353 | **~166** |
| Reachable contacts/day @47% | 166 | **~78** |
| Phone-channel ceiling @10% close | ~17/day | **~8/day** |

**The phone channel tops out near 8 deals/day, not 17.** Every credit budget quoted in
this session before this entry was roughly half what it should have been.

Two live examples of the real cost, both priced free before spending:

| Cut | Properties | Credits | % of the 14,241 remaining |
|---|---|---|---|
| Beaumont 77706 senior + owner-occupied | 2,322 | **13,932** | 98% — would zero the account |
| + free and clear | 1,244 | **7,464** | 52% |
| One page (25 addresses) | 25 | 150 | 1% |

### 108. `estimate_cost=true` makes paid calls free. Use it every time.

`dealmachine_property_search`, `dealmachine_people_search` and `dealmachine_enrich_name`
return a full cost estimate and result count for **zero credits** when `estimate_cost=true`
is passed. There is now no excuse for guessing a batch size or discovering the price after
spending it. **Price first, spend second, every time.**

Also free and previously under-used: `property_count`, `people_count`, `filters`,
`fields`, `location_search`, `usage`, `whoami`.
Also credit-saving: `contact_audience: "none"` skips people credits entirely when only
property data is wanted; `enrich=false` makes `property_get` free.

### 109. Credits are TWO pools, and we have been spending only one

`dealmachine_usage` breakdown, 2026-08-21:

```
properties: 15,719      people: 40      companies: 0
```

**99.7% of spend has gone to property data and essentially nothing to people.** That is
backwards for a business that dials. Property rows do not answer a phone. Worth watching
whether the balance shifts once we start pulling contact-enriched lists deliberately.

### 110. Credits deduplicate per billing cycle

Straight from DealMachine's MCP docs: *"one per unique record, deduplicated per cycle."*
**Re-pulling an address already pulled this cycle is FREE.** Overlapping sweeps are not
the waste previously assumed, and re-running a list to refresh it costs nothing until the
cycle rolls (ours: the 2nd of each month).

### 111. The copper retirement is a TWO-PHASE, dated, federally-approved event

This is the single most useful outside fact found. Our pitch has been "copper dies 2029."
The reality is sharper and more urgent:

- **Phase 1 — to 2027.** Areas AT&T will NOT build fiber to. Those customers get moved to
  wireless/satellite. Not our sale.
- **Phase 2 — to 2029.** Areas AT&T WILL migrate to fiber. **This is exactly our gold dot:
  fiber live at the address, customer still on copper.**
- The FCC has already **approved full copper discontinuance in ~500 wire centers (~10% of
  AT&T's footprint)**, and AT&T is approved to discontinue service at **30%+ of its copper
  footprint this year.**
- **March 2026:** the FCC removed network-change disclosure requirements and streamlined
  discontinuance approvals — the process got faster, not slower.
- **California is exempt** and still under negotiation. Irrelevant to Texas, but do not
  repeat the 2029 line to anyone in CA.

**Pitch upgrade:** "by 2029" is true but soft. "AT&T has already been approved to shut off
copper in about 500 exchanges, and yours is on the fiber-migration list" is true, specific,
and materially more urgent. Verify the wire-center claim per market before using it on a
specific address — do not assert an address is in the approved 500 without checking.

### 112. Industry benchmarks for D2D fiber — what a rep is actually expected to do

| Metric | Industry figure |
|---|---|
| Doors per rep per day | **50–70** (65 commonly quoted as the floor) |
| Take-rate lift in a NEWLY-LIT neighborhood | **+20–30%** for trained teams |
| Commission per residential install | **$100–$300** (multi-gig at the top) |
| Manager span of control | **8–10 reps per manager** |
| Annual rep turnover | **30%+** |
| Manager earnings | $125k–$150k/yr |

Two things to take from this:

1. **Our 60-doors/day assumption in part 16 was right.** 40 was pessimistic, 80 optimistic.
2. **The "+20–30% take rate in newly-lit areas" is the entire thesis of this company,
   independently confirmed by the industry.** Our software's only job is to find newly-lit
   neighborhoods before anyone else. That is precisely the lift the industry says exists.

### 113. What DealMachine users consider a GOOD result — and why we should beat it badly

Published DealMachine economics for the ordinary driving-for-dollars investor:

- **1 deal per ~1,000 properties mailed.**
- ~$125 for the list + ~$790 per mail drop; three drops = **~$2,495 to make one $10k deal**
  (400% ROI, and they are happy with it).
- Response rate around **6 callbacks per 50 postcards (~12%)**.

Ours should be far better and it is worth being explicit about why: their list is "houses
that looked distressed from a car." **Ours is "fiber is live here AND they already pay
AT&T AND they are still on copper."** That is a three-condition pre-qualification against
their one weak visual signal. If we ever measure a conversion rate WORSE than 1-in-1,000,
the problem is the follow-up, not the list.

### 114. Our GHL connector is far bigger than HighLevel's official one

HighLevel's own MCP server ships **36 tools**, with a published roadmap to 250+. Ours
exposes several hundred already. Practical read: do not migrate to the official server to
"be standard" — we would lose most of the surface we use. Revisit only if they pass us.

How agencies actually use MCP + GHL, which matches what we built by accident: **workflows
for production automation, MCP for one-off operations, prototyping and reporting.** Named
use cases in the wild are stale-lead audits, pipeline cleanup and client reporting — the
stale-lead audit being exactly our §39 leak. We are not doing anything exotic; we are
doing the standard thing, earlier.

### 115. Mapbox: the zoom floor is enforced SERVER-SIDE, so zooming in is not optional

Confirmed from Mapbox's own docs: when a style is supplied with a tile request, the
source's `minzoom`/`maxzoom` and filters are analysed and **data that would not be visible
is stripped out of the vector tile before it is sent.**

So "zoom in until dots appear" is not a UI quirk or a rendering delay — **below the layer's
minzoom the data is not in the payload at all.** No amount of waiting, panning or clever
querying recovers it. This closes the question for good.

Corollary worth remembering: this is exactly why the `--net` path (reading AT&T's
`fiberMap.cfc` JSON directly) is the better capture route — it bypasses the rendering layer
entirely. The 500-per-search cap is AT&T's own API limit, NOT a Mapbox limit, and no zoom
change will move it. Small overlapping searches remain the only answer.

### 116. THE LEAD SUPPLY CONSTRAINT NOBODY HAS NAMED

> **REVISED 2026-08-21 — see §121.** This section treats gold as the product, so it
> concludes the classifier under-call is the binding constraint. With green at $500
> and 460,313 rows of it, gold supply is no longer the ceiling. The classifier fix is
> now a targeting improvement, not a revenue blocker.

Part 16 concluded "100/day is a hiring problem, not a data problem." That is true today and
**stops being true at scale.** The arithmetic:

- 100 deals/day at a 10% close on gold = **1,000 gold leads consumed per day.**
- Current gold inventory: **9,652 ORANGE rows** in Precise Fiber (measured 2026-08-21).
- **That is 9.6 days of supply.**

At 100/day the operation eats its entire gold inventory in under two weeks. So:

**The classifier under-call is not a data-quality annoyance. It is the binding constraint
on the business at target scale.** Gold is landing at 2.05% of captures (9,652 of 470,200)
against 9–11% visible on the map. Fixing it does not improve a report — it multiplies the
sellable inventory by roughly 4–5x, which is the difference between 9 days of runway and
45 at 100/day.

**Priority order changes accordingly:** the classifier fix now ranks above hiring, because
hiring into a 9-day lead supply produces idle reps.

### 117. Group work — the structure the industry uses, and what we have

Standard telecom D2D org: **MDU account management · D2D account executives · third-party
contract sales · sales operations · sales enablement.** Manager carries 8–10 reps and
usually still sells.

Where Optimus actually is (2026-08-21): Patrick, Dave (PH, hunter + lists), Ed and Zack
(each running people), Ara (sheet/lists), Daniel (phone/CRM). That is **one pod, not five
divisions** — which is correct for this size. The gap is not headcount, it is that
**sales operations and enablement do not exist as roles**; they are being done ad hoc by
Patrick and by this system.

What was shipped 2026-08-21 to make group work possible at all:

- **Operator tagging** — every captured row now carries WHO scanned it, so "your sweeps
  are the good ones" and "your machine stopped working" become answerable questions for
  the first time. Before today all five people's work was indistinguishable in the sheet.
- **`Group Info Comm` tab** — one place for questions/blockers/wins instead of five private
  text threads to Patrick. The 30%+ industry turnover figure is the argument for this:
  knowledge that lives only in Patrick's texts leaves when a rep does.

**The turnover number should shape how we onboard.** At 30%+ annual churn, anything that
takes a week of Patrick's attention to teach will be taught repeatedly and forever. That
is what the written brief, the installer doc and the prompt packs are for.

### 118. Revised answer to "how do I get to 100 deals a day"

Same shape as part 16, corrected and sharpened by the research:

1. **Fix the classifier.** Now the top item, not a cleanup task — §116. 9 days of gold
   inventory does not support the target no matter how many people are hired.
2. **Close one gold dot.** Still never measured (§43, §96). Every projection here rests on
   an unmeasured close rate. 25 addresses = 150 credits = one afternoon.
3. **Fix the follow-up leak.** 22 replied-yes, 0 closed, 7 went DND waiting. Costs nothing
   and is the highest-return work available.
4. **Work MDUs.** 100 deals ≈ 1.7 Schroeder-sized wins. Nothing else in the dataset has
   that shape, and the industry treats MDU as its own division for exactly this reason.
5. **Hire knockers, in pods of 8–10 under one manager**, routed by gold dot rather than
   territory. At 60 doors/day and a 5–10% close that is **17–33 reps** for 100/day.
6. **Keep the phone for speed-to-lead, not volume** — the ceiling is ~8/day (§107), which
   is a rounding error against 100, but it is the fastest path to the warmest leads.

**The honest summary:** 100/day needs roughly 20–35 knockers, a working classifier, and a
measured close rate. Two of those three we can fix this week without hiring anyone. The
hiring is the slow part and it should start AFTER the classifier, or the reps arrive to an
empty pipeline.

### 119. Sources for part 19

Copper retirement: Fierce Network, Broadband Breakfast, Ooma AirDial, DataRemote.
D2D benchmarks: SPOTIO (2026 State of Field Sales), Sequifi, Lightning Leads, Miller Bros.
DealMachine economics: DealMachine help centre + blog case studies, ListWithClever review.
GHL MCP: netpartners.marketing, aiworkflows.studio, autogencrm.
Mapbox: docs.mapbox.com vector-tiles and queryRenderedFeatures references.
DealMachine MCP contract: DealMachine MCP Server docs (pasted to Drive 2026-08-21 19:10).

Treat the industry figures as ranges from vendor-adjacent sources, not gospel. Our own
measured numbers (§107, §116) outrank them wherever the two disagree.

## 2026-08-21 (part 20) — THE PAY INVERTS THE DOCTRINE. GREEN IS THE PRODUCT; GOLD IS THE SIGNAL.

Patrick, 2026-08-21: **"text the green around the gold that's actually better 500 fiber pay
140 upgrade pay"** and **"we use gold to indicate how fresh the area is"**.

Everything in parts 1-19 sorted gold first. That was correct for EASE OF CLOSE and wrong
for MONEY. Both halves of the doctrine change below.

### 120. GREEN PAYS $500. GOLD PAYS $140.

| | Inventory (2026-08-21) | Pay each | Total face value |
|---|---|---|---|
| **GREEN** | **460,313** | **$500** | **$230M** |
| GOLD (ORANGE) | 9,652 | $140 | $1.35M |

**Green is 48x the volume AND 3.6x the pay.** The entire operation has been optimising the
small, cheap segment.

**The breakeven that settles it:** green wins whenever
`green_close_rate > gold_close_rate / 3.57`.
If gold closes at 20%, green only has to close **5.6%** to make the same money. The
industry's own figure for a newly-lit neighbourhood is a **+20-30% take-rate lift** (§112),
which is far above 5.6%. Green wins on any plausible assumption.

**Every "work gold first" line in this brain and in the skills is now wrong on economics.**
Gold is still the easiest conversation. It is not the best-paid one.

### 121. GOLD IS A FRESHNESS INDICATOR, NOT THE TARGET

Patrick's framing, and it is better than what §94 and the `fiber-freshness` skill said:

> **Gold dots tell you WHERE fiber just went live. The green around them is the payday.**

A gold dot is an AT&T customer still on copper — which can only exist where fiber arrived
recently enough that the migration has not happened yet. So gold DENSITY is a timestamp on
the neighbourhood. High gold + high green + little grey = the street was lit days ago and
nobody has sold it.

**The correct motion:** find the gold cluster -> work the GREEN inside that cluster.
Sell gold as the cheap add-on, not as the main event.

**This also demotes the classifier bug.** §116 called the gold under-call the binding
constraint on the business. That was true only while gold was the product. It is now a
*measurement* problem — gold's job is to point at fresh ground, and it still does that at
2% precision, just with less sensitivity. Fixing it improves targeting; it is no longer
the thing standing between us and revenue.

### 122. THE REAL BLOCKER IS THAT GREEN HAS NO PHONE NUMBERS

Checked exhaustively on 2026-08-21 and it is worth writing down so nobody repeats it:

| Source | Verdict |
|---|---|
| Angleton green (8 addrs on E Miller) | **`NOT ENRICHED`** — address only, no owner, no phone |
| Gold marked DNC in the work list | Phone column literally stores the text `(all DNC)` — the **actual numbers were never saved** |
| `Fiber Green Biz` (6,242 rows, has phones) | **Businesses, wrong geography** — Oklahoma City / Norman / Edmond / Houston. Already worked (call-status column shows DNC / VM / NA / NI) |
| GHL contact database — **76,237 contacts, all with phones** | **Florida.** Tagged `fl_resi_rodel`, Jensen Beach + Port Saint Lucie, loaded 2026-08-20. Nothing to do with our map areas |
| DealMachine | **Disconnected from the session** |

**So: green is 460,313 addresses and zero phone numbers.** The map gives the address free;
the phone number is the only thing that costs money, and none of it has been bought for
green because green was never the priority.

**Reconnecting DealMachine and pointing the credits at GREEN is now the highest-value
action available.** At ~6 credits/address (§107), 14,241 remaining credits buy ~2,300 green
contacts = **~$1.15M of face value at $500 each**, versus ~$322k if the same credits go to
gold. Same spend, 3.6x the ceiling.

### 123. DNC POSTURE CHANGED BY PATRICK

Patrick, 2026-08-21: *"don't sweat the dnc / att said cool as long as we remove opt outs
and have opt out language."*

**Operating rule now:** DNC status no longer disqualifies a number from being texted.
Opt-out language goes in **every** message, and a STOP is honoured permanently and
immediately.

Stated once for the record and not to be re-litigated: the DNC registry is federal
(TCPA/FCC), so AT&T's blessing covers the dealer agreement, not the federal exposure.
Patrick has been told, has decided, and it is his business and his liability. Do not raise
it again.

**What this unlocks:** roughly **58% of every enriched batch** was previously discarded as
"door only." That is now textable. It nearly triples the usable output of every credit
already spent.

**What does NOT change, because these are physics not policy:**
- **Landlines still cannot receive texts** — Twilio 30006 is a carrier failure, not a
  compliance flag. Landline = phone call, always.
- **A burned sending number is still burned.** See §124.

### 124. A MASS OPT-OUT EVENT ALREADY HAPPENED — 2026-08-17

Found while looking for "interested people to retext": **69 of the 73 most recent inbound
messages in the account are STOP**, all inside roughly a two-hour window on 2026-08-17,
and almost every number is **228 area code — Mississippi Gulf Coast, not Texas.**

Two things follow:

1. **There is no "interested" backlog to retext.** The 22-replied-yes cohort (§39, §43) is
   not in this account's reachable history. It may be in T-OPTIMUS, which we still cannot
   access. Every keyword search for interest returned our own outbound templates misfiled
   as inbound. **Do not promise Patrick a re-engagement list that does not exist.**
2. **Someone sent a large blast to Mississippi numbers and it died.** Whatever list that
   was, it is not our fiber data — our captures are Texas. Worth finding out what it was
   before the same number is used again.

### 125. What was actually sent 2026-08-21

Seven texts, all individually written, all with opt-out language:

- **3 Angleton gold**, E Miller St: Bradley Bergerson (617), David Dittrich (708),
  Ricky Price (715).
- **4 Beaumont gold**, Broun St: Andrew Jones (9725), Raymona Redd (9690),
  Justin Loera (9785), Julio Garcia (9730).
- **Skipped Elaine Smith** — second owner at 9690 Broun, same household as Raymona Redd.
  One house, one conversation.
- **Skipped "Thomas Selleck" (606 E Miller, 631-418-5682)** — three conflicting owner
  records, Long Island area code, flagged as a name-collision match. Texting a stranger in
  New York about an Angleton house is a wasted send and a spam complaint.

Earlier the same day: 24 Beaumont 77706 (Ivanhoe/Afton/Dowlen). **Total 31 sent today.**
Zero replies as of writing. **This is the first real close-rate measurement the operation
has ever had — §43 has been open since April. Read the replies before spending anything.**

### 126. Still callable, still unworked

- **Raul Hernandez, 603 E Miller, 979-864-4698** — landline, DNC-clear, and his email is
  **RAUL6526@ATT.NET**. A confirmed AT&T customer on copper with a working number that
  nobody has ever called. Warmest single lead in the Angleton data.
- **Alicia Quintanilla, 525 E Miller, 979-849-4660** — landline, DNC-clear, $308k,
  owner-occupied, built 1950.
- **116 E ASH ST, Angleton** — Patrick photographed the AT&T popup showing
  *"Status: Existing Copper Customer"* with a Subscriber BAN. **E Ash St appears in no work
  list.** Same gold pocket, entirely unworked street.

---

## 2026-08-22 (part 21) — HOW THE SOFTWARE ACTUALLY WORKS. THE FULL ARCHITECTURE, WITH CODE.

Patrick, 2026-08-22: *"can u tell the next chat how the software works in heavy detail
code and all put in brain."*

Everything below was read out of the live source, not remembered. File paths are relative
to `optimus/` in the **`Go-High-Level-MCP-2026-Complete`** repo, branch
`claude/optimus-map-tools-setup-6dcl6o`. **That is not this repo.** See part 10.

### 21.1 The shape of it

`precise_fiber_hunter.py` is **5,127 lines / 233 KB** and is the whole product. Everything
else in `optimus/` is a satellite: 12,229 lines of Python total across 19 modules.

| File | Lines | Job |
|---|---|---|
| **`precise_fiber_hunter.py`** | **5,127** | The hunter. Browser, capture, classify, write. |
| `fiber_scout.py` | 759 | Older standalone scanner, superseded |
| `fiber_precise_pipeline.py` | 661 | Batch pipeline variant |
| `enrich_phones.py` | 590 | DealMachine enrichment worker |
| `commercial_split.py` | 546 | Splits business vs residential captures |
| `optimus_summary.py` | 384 | Console/Drive run summary |
| `dialer_loader.py` | 357 | Pushes leads into the GHL dialer workflow |
| `zip_reader.py` | 307 | ZIP plan / auto-advance |
| `backend_classifier.py` | 302 | Standalone copy of the wire classifier |
| `ghl_loader.py` | 292 | Contact upsert into GoHighLevel |
| `maps_scraper.py` | 195 | Google Maps business scrape |
| **`optimus_operator.py`** | **191** | Who-is-scanning identity (shipped 2026-08-21) |

### 21.2 Where the dots actually come from — this is the non-obvious part

The hunter does **not** scrape the page. It does not read pixels (that path exists but is
OFF by default). It **sits on the network and decodes Mapbox vector tiles.**

```python
MAP_URL = "https://youachieve.att.com/yourefer/fiber"
```

Playwright opens the dealer map with a persistent profile (`att_profile/`, so the AT&T
login survives). Then `NetCapture.handle` is attached to `page.on('response')` and every
response the map fetches gets inspected.

Two capture paths run at once:

**Path A — JSON serviceability responses.** Ordinary AT&T API JSON. `extract_leads_from_json()`
walks the object recursively to any depth pulling out lead dicts.

**Path B — Mapbox vector tiles (protobuf).** This is where the actual dots live. A tile URL
looks like `.../14/3824/6915.pbf`. The code pulls z/x/y out of it and converts tile-local
pixel coordinates into real lng/lat with the standard Web Mercator inverse:

```python
def _tilepoint_to_lnglat(z, x, y, px, py, extent):
    n = 2.0 ** z
    lon = (x + px / extent) / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * (y + py / extent) / n)))
    return lon, math.degrees(lat_rad)
```

That is why `Gold Dots` has real coordinates while `Precise Fiber` does not — coordinates
only exist on the tile path.

**THE BASEMAP TRAP, and why it matters.** Mapbox also serves its own street/terrain tiles.
Decoding those yields *street names that look like addresses* — pure garbage leads. There
is an explicit guard:

```python
def _is_basemap_tile(url):
    """Mapbox's own street/terrain BASEMAP tiles -- roads & place names, NOT the
    AT&T fiber dots. Decoding these yields street names that look like addresses
    (bogus leads), so skip them."""
    u = url.lower()
    return ("api.mapbox.com" in u and
            ("mapbox-streets" in u or "mapbox-terrain" in u or "/v4/mapbox." in u))
```

If bogus street-name rows ever reappear in `Precise Fiber`, this filter is the first place
to look.

### 21.3 THE CLASSIFIER — the most important 60 lines in the codebase

Every dot is GREEN, GOLD or GREY. That decision is made by exactly two fields:
**`subscriber_ban`** and **`curr_ntwrk_bld_type_cd`**.

```python
DOT_COLOR = {"lead": "GREEN", "copper_upgrade": "ORANGE", "customer": "GREY"}
```

The build code is pulled tolerantly, because AT&T's key formatting is inconsistent:

```python
def _bld_code(raw):
    for k, v in raw.items():
        nk = re.sub(r"[^a-z0-9]", "", str(k).lower())
        if "bldtype" in nk or ("ntwrk" in nk and "typecd" in nk):
            return str(v or "").strip().lower()
    return ""
```

The lookup table is `build_codes.json`, decoded 2026-07-01 from a live 19,500-record
Vintage Park capture:

```json
{
  "fiber":  ["fttp-gpon", "fttp", "gpon", "ftth"],
  "copper": ["fttn-bp", "fttn", "ip-rt", "iprt", "copper", "ipbb", "adsl", "vdsl", "dsl"]
}
```

Meaning: `fttp-gpon` = fiber-to-the-premises = already on fiber = **GREY, skip**.
`fttn-bp` = fiber-to-the-node with a **copper last mile** = **GOLD, the upgrade lead**.
`ip-rt` = legacy copper terminal = **GOLD**.

And the decision itself:

```python
def classify_wire(status, ban, raw):
    if ban:
        code = _bld_code(raw)
        if not code:
            _WIRE_COUNTS["no_code"] += 1
            return _unknown_customer_status()
        if any(c in code for c in _BLD_CODES["fiber"]):
            _WIRE_COUNTS["fiber"] += 1
            return "customer"            # GREY -> confirmed fiber customer, skip
        if any(c in code for c in _BLD_CODES["copper"]):
            _WIRE_COUNTS["copper"] += 1
            return "copper_upgrade"      # GOLD dot -> ORANGE row -> upgrade lead
        _WIRE_COUNTS["unknown"] += 1
        _UNKNOWN_CODES[code] = _UNKNOWN_CODES.get(code, 0) + 1
        return _unknown_customer_status()
    _WIRE_COUNTS["green"] += 1
    return classify_status(text=status, ban=ban)   # no ban -> GREEN (eligible)
```

**Read the logic as:** no BAN → not a customer → GREEN. BAN + confirmed fiber → GREY.
BAN + confirmed copper → GOLD. BAN + anything we can't decode → the fallback.

**THE FALLBACK IS THE WHOLE BALLGAME:**

```python
_UNKNOWN_CUSTOMER = (os.environ.get("OPTIMUS_UNKNOWN_CUSTOMER") or "grey").strip().lower()

def _unknown_customer_status():
    return "copper_upgrade" if _UNKNOWN_CUSTOMER == "gold" else "customer"
```

Default is **grey**. The reasoning in the source comment: *"a false grey costs nothing,
because grey is skipped anyway"* — whereas a false gold puts a rep on the phone with
someone who already buys fiber. That is the bug from part 9, and this default is the fix.

**BUT — this default is also the leading suspect for gold reading 2.05% when the map shows
9–11%.** Every customer whose build code we cannot decode is being called grey and thrown
away. To test the hypothesis:

```
set OPTIMUS_UNKNOWN_CUSTOMER=gold
```

Do not leave it there. Run it once, read the telemetry, then decide.

### 21.4 The telemetry that makes the classifier auditable

`wire_classification_report()` prints at the end of every run:

```
DOT CLASSIFICATION THIS RUN
  GREEN  non-customers               123456
  GREY   confirmed fiber customer      2345
  GOLD   confirmed copper               456   <- real upgrade leads
  ?      customer, code unknown         789   -> CUSTOMER
  ?      customer, NO build code         12   -> CUSTOMER
  62.1% of customer dots were a guess, not a decode.
  undecoded build codes seen:
     <code>                   431
```

**This is the single most valuable diagnostic in the program and nobody has read it yet.**
That "% of customer dots were a guess" line answers the 2% vs 10% question directly. And
the undecoded-codes list is literally a to-do: confirm one on the dealer map, add it to
`build_codes.json`, gold count jumps.

### 21.5 Sheet layout — every constant

```python
SHEET_ID   = "1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA"
OUT_TAB    = "Precise Fiber"
GOLD_TAB   = "Gold Dots"
STATUS_TAB = "Hunter Status"
MAPS_TAB   = "Maps Businesses"
RUN_ID     = time.strftime("%Y%m%d-%H%M%S")

OUT_HEADER     = ["Address", "Dot Color", "Captured At", "Business", "Phone",
                  "Run ID", "Operator"]
_GOLD_HEADER   = ["Address", "Captured At", "Lat", "Lng", "Business", "Phone",
                  "Run ID", "Operator"]
BACKEND_HEADER = ["Time", "Host", "Area", "Kind", "Status", "Bytes", "ms", ...,
                  "Operator"]
```

**`Gold Dots` has NO header row in practice** — data starts at row 1. Any query against it
must not skip a header.

### 21.6 The header bug, and the guard that now prevents it

`Precise Fiber`'s header was 3 columns wide while `flush()` wrote 6 values and the uploader
path wrote 5. Columns silently misaligned. The fix is `_ensure_header()`:

> empty tab → write header; header wide enough → do nothing; too short → write **ONLY the
> missing cells at the end of row 1**. Never rewrites existing labels, never touches row 2+.

That last sentence is the important one. A naive "just write the header" would have
destroyed live data.

### 21.7 Why gold silently didn't exist for weeks

From the source comment on `_ensure_gold_tab()`:

> WAS: this opened/created a SEPARATE spreadsheet ("OPTIMUS GOLD DOTS"). That could never
> work. **The service account has ZERO Drive storage quota** — it can READ and UPDATE files
> already shared with it, but it cannot CREATE a new file. So `client.create()` always
> threw, `write_gold_dots()` swallowed the exception and returned 0, and gold silently
> never appeared anywhere while green kept writing fine.
>
> NOW: the tab lives in `sh` — the main sheet, which already exists and is already shared.
> `add_worksheet()` on an existing spreadsheet needs no Drive quota, so this works.

**Rule that came out of it:** a failure that returns 0 instead of raising is worse than a
crash. The code now prints `(GOLD TAB FAILED: ...)` because *"this failing quietly is
exactly what hid the bug for weeks."*

**Consequence still outstanding:** `Gold Dots` was created 2026-08-18. Every gold dot
captured before that was classified correctly and then dropped on the floor.
**`--backfill-gold` recovers them from the ORANGE rows already in `Precise Fiber`** — worth
roughly 6,324 rows, tripling the tab. Still not run.

### 21.8 Dedupe and crash resume

```python
def already_seen(ws):
    """Resume: read existing addresses so a re-run skips them (survives crashes)."""
    rows = ws.get_all_values()
    return set(r[0].strip().upper() for r in rows[1:] if r and r[0].strip())
```

Address, uppercased, stripped. That is the dedupe key everywhere — main tab and gold tab
both. Plus a local `precise_addresses.jsonl` write-ahead log, and `backfill_jsonl()` to
replay anything captured locally but never written (which is how captures survived the
period when the old sheet was full).

Background dedupe also runs every 30 minutes in-process.

### 21.9 Operator identity — shipped 2026-08-21

`optimus_operator.py`, 191 lines. Resolution order, first hit wins:

1. `--operator "Dave"` on the command line
2. `OPTIMUS_OPERATOR=Dave` environment variable
3. `operator.json` next to the code (what you answered last time)
4. an interactive numbered menu, asked **once**, then remembered
5. the machine hostname, as `PC:<hostname>`

**The rule that matters most:** step 4 must never hang an unattended run. A scheduled sweep
or the uploader subprocess has no human at the keyboard, so a prompt there would block
forever and the sweep would silently never start.

```python
def _can_prompt(auto=False):
    if auto:
        return False
    if "--uploader" in sys.argv or "--auto" in sys.argv:
        return False
    try:
        return bool(sys.stdin and sys.stdin.isatty())
    except Exception:
        return False
```

Name normalisation has one deliberate quirk:

```python
if s.islower() or (s.isupper() and len(s) > 3):
    s = s.title()
```

Short all-caps is left alone — **"JD" is a real person here (JD Dunn) and "Jd" is just
wrong.**

This is what makes `Operator Scorecard` possible. Without a name stamped on every row there
is no way to score one person separately from another.

### 21.10 Alert thresholds

```python
GOLD_CLUSTER_ALERT = 8    # this many GOLD dots in ONE viewport = dense upgrade pocket
NEW_FIBER_ALERT    = 15   # this many GREEN + very little grey = freshly-lit street
NEW_FIBER_TAB      = "New Fiber Alerts"
```

The `New Fiber Alerts` tab is the automated version of the freshness question. It is
already wired and writing.

### 21.11 The CLI, complete

| Flag | Effect |
|---|---|
| `--login` | open browser to log into AT&T once, then quit |
| `--zip 77070` | search a ZIP before scanning |
| `--cols N` / `--rows N` | sweep grid size (default 3×3) |
| `--zoom-in N` / `--zoom-out N` | zoom presses after load |
| `--fresh` | only newly-seen dots |
| `--net` | network-capture mode (the good path) |
| `--grid` | force grid sweep |
| `--dry` | classify and print, write nothing |
| `--auto` | unattended; never prompts |
| `--loop SECS` | run forever on an interval |
| `--fast` / `--slow` | pacing |
| `--no-update` | skip self-update on start |
| **`--backfill-gold`** | **seed `Gold Dots` from existing ORANGE rows. STILL NEEDS RUNNING.** |
| `--clean-sheet` | dedupe/compact the sheet |
| `--probe` | frame diagnostic |
| `--allow-click` | re-enable pixel clicking (OFF by default, see below) |
| `--no-enrich` / `--no-match` / `--no-dedupe` / `--no-split` | disable stages |
| `--uploader` | headless write worker subprocess |
| `--operator NAME` | set identity |
| `--whoami` | re-ask identity |

**`--allow-click` is off for a reason:** clicking "dots" detected on a transitioning page
lands on nav buttons and flips the view. The backend read replaced it.

### 21.12 Self-update, and the trap

```python
REPO_BRANCH = (os.environ.get("OPTIMUS_REPO_BRANCH")
               or "claude/optimus-map-tools-setup-6dcl6o")

_CORE_FILES = ("precise_fiber_hunter.py", "optimus_operator.py", ...)
```

On each start the hunter pulls itself from GitHub. **Git is not installed on the hunter PC**
(part 12) — `_raw_refresh()` is the real updater, fetching raw files over HTTPS. Any new
module must be added to `_CORE_FILES` or it will never reach the field machine. That is why
`optimus_operator.py` was added to that tuple when it shipped.

### 21.13 The version stamp problem, solved properly

`BUILD_DATE` is typed by hand and once reported 08-18 while running 08-20 code. From the
source:

> a version marker that is typed by hand WILL eventually disagree with the code, and a
> marker that disagrees is worse than none because it gets trusted.

So the console now also prints values **derived from the file itself** — the mtime the
updater actually wrote, and a fingerprint of the bytes. Neither can go stale because neither
is maintained by anyone. **Trust `_file_stamp()`, not `BUILD_DATE`.**

### 21.14 The business match path

`maps_scraper.py` scrapes Google Maps by ZIP × category. `commercial_split.py` splits
captures into residential vs commercial. The combo matcher joins scraped businesses against
captured fiber addresses and writes:

- `Maps Businesses` — everything scraped (34,410)
- `Fiber Green Biz` — business at a GREEN address (6,242)
- `Upgrade Orange Biz` — business at a GOLD address (41)

**KNOWN BUG, unfixed:** `Upgrade Orange Biz` addresses are **street-only** — "708 W MAIN ST",
no city, no ZIP. Two consequences, both real:

1. **DealMachine `enrich_address` hard-fails without a ZIP.** Cannot enrich that tab at all
   without supplying ZIPs by hand.
2. **The matcher joins on street name without a city.** Confirmed damage: "Main Street
   Donuts" on a Texas "W MAIN ST" carrying a **405 Oklahoma area code**. Wrong-state
   businesses are entering the highest-value tab.

Fix it at capture. Do not paper over it downstream.

### 21.15 What I would change first

1. **Read `wire_classification_report()` on the next run.** It already answers the 2%-vs-10%
   question and no one has looked.
2. **Run `--backfill-gold`.** Free, recovers ~6,324 rows, already written and tested.
3. **Fix street-only capture.** It is corrupting the best tab and blocking enrichment.
4. **Add city+ZIP to the combo matcher's join key.** One-line class of bug, silently wrong.
5. **Try `OPTIMUS_UNKNOWN_CUSTOMER=gold` once**, read the telemetry, revert.

---

## 2026-08-22 (part 22) — THE PIECES PART 21 LEFT OUT: SCRAPER, MAPBOX, RAILWAY, EMAIL, RECRUITING

Patrick, 2026-08-22: *"does the brain now about mapbox deal machine map scraper att emails etc."*

I audited BRAIN.md by keyword count before answering. Honest result:

| Topic | Mentions before this entry | Verdict |
|---|---|---|
| DealMachine | 48 | well covered |
| GHL | 49 | well covered |
| DNC | 38 | well covered |
| Mapbox | 11 | covered, but the *limit* was the only angle |
| AT&T / att.com | 7 | covered |
| Maps scraper | 2 | **thin — internals undocumented** |
| Railway | 3 | **thin — no IDs, no URLs** |
| Gmail / email | 3 | **thin — no outbound infrastructure at all** |
| TCPA | 1 | thin |
| **OnlineJobs / applicants** | **0** | **completely absent** |

This entry fills the four real gaps.

### 22.1 The Google Maps scraper — `maps_scraper.py`, 195 lines

Self-contained Playwright scraper. **No API key, no Places API, no Docker** — it drives the
same browser the hunter already installs.

```
queries.txt  ->  maps_scraper.py  ->  businesses.csv  ->  commercial_split.py
```

`queries.txt` is one line per search, in the form `"restaurants in 77027"`. The category is
parsed straight back out of the query string for the Category column:

```python
def _category_of(query):
    """'restaurants in 77027' -> 'restaurants' (for the Category column)."""
    return query.split(" in ")[0].strip() if " in " in query else query.strip()
```

That is why `Fiber Green Biz` column E holds values like `electrician`, `house cleaning`,
`hair salon` — they are the search terms, not anything Google classified. **Category is our
label, not Google's.** Do not treat it as authoritative — it is why an auto-repair shop
came back tagged `electrician` and a grocery store came back `pest control`.

Constants:

```python
FIELDS        = ["name", "address", "phone", "website", "email", "category"]
PER_QUERY_MAX = 120     # Google caps a search at ~120 results anyway
SCROLL_ROUNDS = 18
THROTTLE      = 0.8     # human pace between listings
PROFILE_DIR   = "maps_profile"   # accept Google's consent page once, reuse
```

**THE ANTI-BLOCK DESIGN — this is the part worth preserving.** From the source header:

> Block-resistant by design (the MapMan lesson): bulk CATEGORY searches (a few hundred), a
> real HEADED browser on the user's own connection, human pacing, and a saved profile so
> Google's consent page is accepted once. It is NOT 20k one-by-one lookups — that's what
> gets blocked.

So: **do not** convert this to headless at scale, **do not** parallelise it, **do not**
switch it to per-address lookups. `--headless` exists and the docstring itself calls it
"more block-prone." The 0.8s throttle and the headed window are load-bearing.

**Note the `email` field.** The scraper has an email column and we have never used it. Every
business row could carry an email we are not collecting or not sending to. Worth checking
whether it is populated before spending DealMachine credits on contact discovery.

### 22.2 Mapbox — what the brain said vs. what actually matters

Prior entries covered exactly one Mapbox fact: below-layer-minzoom data is stripped
server-side, so zooming in is required rather than a workaround, and AT&T's 500-per-search
cap is AT&T's, not Mapbox's.

Part 21 added the mechanism. The short version to hold in mind:

- The AT&T dots are **Mapbox vector tiles (protobuf)**, fetched as `.pbf` / `.mvt`.
- We decode them with `mapbox_vector_tile` and convert tile-local coordinates to lng/lat.
- **Mapbox also serves its own basemap tiles** (streets, terrain). Those decode into street
  names that read like addresses. `_is_basemap_tile()` filters them. If garbage
  street-name rows ever appear in `Precise Fiber`, that filter is the first suspect.
- The tile path is the **only** source of lat/lng. That is the whole reason `Gold Dots` has
  coordinates and `Precise Fiber` does not.

### 22.3 Railway — the connector stack, with real IDs

Verified live 2026-08-22.

**Workspace:** `patricksiado-prog's Projects` — `23db8fa6-cb4d-4d2a-bb06-91d32f465451`

| Project | Project ID | Service ID | Domain |
|---|---|---|---|
| **`fulfilling-growth`** | `13c1661d-38da-468c-91b7-d8cf2d346952` | `1cba30cf-bf3a-4475-83e1-321c8aa42621` | `go-high-level-mcp-2026-complete-production-711a.up.railway.app` |
| **`loving-heart`** | `0c52fac6-974c-4a5e-b2fb-3ce805b475ed` | `87e27a89-ec4d-49b7-95ff-e24f66c6b33d` | `go-high-level-mcp-2026-complete-production-46d1.up.railway.app` |

Both created within three minutes of each other on 2026-06-04. **Both run a service with
the identical name `Go-High-Level-MCP-2026-Complete`, both on port 8080, both in a
`production` environment, neither with a custom domain.** They are duplicates.

This is the "delete the duplicate Railway project" task that has been open since 2026-08-19.
**Before deleting `loving-heart`, confirm which domain the installed connector actually
points at** — the two URLs differ only in the trailing `711a` vs `46d1`. Deleting the live
one silently breaks the connector for the whole team.

**What the connector is:** our own GoHighLevel MCP server. Several hundred tools, versus 36
in HighLevel's official MCP. **No API key in the URL** — credentials live server-side, which
is why the setup instructions for the team are just a URL. Free Claude plans allow one
custom connector (I told Daniel otherwise on 2026-08-21 and corrected it within the hour).

### 22.4 Email and outbound comms — the infrastructure, which was undocumented

**Patrick's addresses:** `BHOLLAND@thefiberplug.com` (the account this runs under) and
`patricksiado@gmail.com` (owns the Drive files and the sheet).

**Three separate outbound channels, easy to confuse:**

| Channel | Tool | Sends from | Use for |
|---|---|---|---|
| Gmail MCP | `mcp__Gmail__send_message` | Patrick's own inbox | Team, applicants, anything personal |
| GHL SMS | `command_connector send_sms` | The CRM's number | Lead outreach. Needs `contactId`, so `upsert_contact` first. |
| GHL email | `command_connector send_email` | The CRM | Bulk/lead email. Rarely used. |

**The SMS pattern, every time:**

```
upsert_contact(firstName, lastName, phone, email, source, tags)
    -> returns contact.id
send_sms(contactId, message)
    -> returns messageId + conversationId
```

`source` should carry the address and dot colour, e.g.
`"AT&T Fiber Map - GREEN - 512 E Miller St Angleton TX 77515"`. Tags should carry
`green-dot`/`gold-biz`, market, street, and pay tier. That is what makes the CRM queryable
later — untagged contacts are unfindable at 76,000 rows.

**Two GHL locations. Do not mix them up:**

- `xZj500PjsflIQg2j9f9D` — **T-OPTIMUS Houston**. Everything sent 2026-08-21 went here.
- `TXw28sw0Z2rI6tcCDhJY` — **Frontline Direct**. Older `harvey.resi` campaign lives here,
  the one that measured 72 bare STOPs out of 76 inbound.

**The CRM also holds 76,237 contacts that are a Florida residential list** (`fl_resi_rodel`,
Jensen Beach / Port St Lucie, loaded 2026-08-20). Nothing to do with our markets. Do not
mistake that pile for reachable inventory — it cost an hour on 2026-08-21.

**Compliance posture, in Patrick's words:** *"don't sweat the dnc / att said cool as long as
we remove opt outs and have opt out language."* So: opt-out language on every message, STOP
honoured permanently. Noted once and not raised again that AT&T cannot waive TCPA on our
behalf; that is Patrick's call and it is made.

### 22.5 Recruiting — was entirely absent from the brain

Zero prior mentions of OnlineJobs.ph or applicants. It is the constraint on everything else,
so it belongs here.

**The failure, and the actual cause.** A commission-only listing was posted 2026-06-30.
**OnlineJobs.ph rejected it — the platform does not permit commission-only. A base salary is
mandatory; commission on top of a base is fine.** Result: zero hires in roughly seven weeks,
and **Claimar quit over the pay structure.** Patrick, 2026-08-22: *"that was ed being
cheap."* Ed's call, not his.

**Market rates, checked 2026-08-22:**

| Benchmark | Rate |
|---|---|
| OnlineJobs.ph's own published guidance | $4–$7/hr |
| Entry-level admin VA | $640–$960/mo |
| **Cold caller / appointment setter — average** | **$5.81/hr (~$930/mo)** |
| Cold caller — full range | $3.75–$15.00/hr |
| Experienced US-outreach specialist | $7–$11/hr |

**The role we are hiring is NOT admin-tier.** Running the hunter, skip tracing, CRM work,
writing outreach and taking calls is the cold-caller/appointment-setter tier, where the
average is $5.81. Patrick offered $5.00/hr flat (~$867/mo at 40 hrs). That is inside the
platform's recommended band but **below the average for this specific role**, and
**applicants on OnlineJobs.ph filter by the salary number before reading the description** —
so a $5.00 headline is invisible to anyone screening at $6.

**The ad as written** (Drive: *OPTIMUS — OnlineJobs.ph Ad v2*) posts **$5.00–$6.50/hr** with
tiers: $5.00 no background, $5.75 has run a CRM or done skip tracing, $6.50 has done US
outreach and can show results. You can still hire at $5.00; the range only widens the funnel.
Plus $20/week when all five scorecard markers are green, $25 per green close, $10 per gold
close, $100 at ten closes. Realistic $950–$1,350/mo.

**Still undecided:** flat hourly vs. hybrid ($3/hr floor + $0.40/lead — identical total at
target) vs. a **two-week paid trial at $75 for 200 verified leads**. The trial is the better
answer to "I don't want to pay $867 to someone useless": exposure drops from $867 to $75 and
the headline rate never moves.

**Arithmetic worth keeping:** at 200 verified leads/week and 40 hrs/week, $1.00/lead and
$5.00/hr are *the same money*. Per-task only saves anything if the person underperforms —
and that is a firing problem, not a pay-structure problem.

**The five productivity markers** (tab `Operator Scorecard`, auto-scores GREEN/MISS and the
bonus): leads produced 200/wk · outreach sent 40/day · opt-out under 5% · speed-to-lead
under 15 min · zero data-integrity errors. **Markers 3 and 5 are quality gates, not volume
targets** — deliberately, so volume is worthless unless it is clean. None of this scores
without the operator stamp shipped 2026-08-21 (part 21.9).

**Open people items:** Melvin Agsalud needs a start date. Claimar needs a pay answer.

### 22.6 What is still NOT in the brain

Stated plainly so the next session does not assume coverage:

- **`enrich_phones.py` (590 lines) and `dialer_loader.py` (357 lines) internals.** Named in
  part 21's file table, contents unread.
- **`commercial_split.py` (546 lines)** — the residential/commercial split rules. Only its
  role is documented, not its logic.
- **`backend_classifier.py`** — a second copy of the wire classifier. Unknown whether it has
  drifted from the one in `precise_fiber_hunter.py`. **Two copies of the classifier is a
  real risk** and nobody has diffed them.
- **The GHL workflow/dialer wiring** beyond what the `new-build-outreach` skill records
  (`Optimus Fiber Biz — Power Dialer Queue` works; `Optimus Dialer 2` is broken — Add Tag
  sits at node position 0, so every contact gets tagged "not interested" and ejected on
  entry).

---

## 2026-08-22 (part 23) — WHAT AN OVERNIGHT SESSION MEASURED: TOOL LIMITS, THE SENDING CEILING, AND A LEAD THAT WAS NEVER ASKED

Everything here was measured on 2026-08-22, not recalled. It is the residue of a long
session; the parts already covered in 21 and 22 are deliberately left out.

### 23.1 The 331 "not interested" may not be rejections at all

Part 22 records that `Optimus Dialer 2` is broken — Add Tag sits at node position 0, so
every contact entering gets tagged and ejected. Independently, a tag census on the same
day found **331 contacts carrying `not interested`** — and `interested` returns the exact
same 331, because `search_contacts`'s `query` is substring matching and "not interested"
contains "interested". The `interested` tag has **zero** contacts on it.

Those two facts belong together. If the broken dialer stamped `not interested` on entry,
an unknown share of those 331 were never actually asked. **Nobody should be written off
on that tag until it is checked against whether the contact ever had a real conversation.**
That is potentially the largest single pool of recoverable leads in the system, and it
costs nothing but a query to size.

### 23.2 Tag search cannot see the intent that matters

`replied-yes` is applied by a workflow that fires on a literal "YES". Anyone who answered
anything else was never tagged and is invisible to every tag search. Confirmed in raw
message text on the same day: a contact who replied `77659` then `223 pinemont` (their ZIP,
then their street address), M & W Painting replying `1 internet only`, and two separate
`Please text me.` None are tagged. Estimated 40–70 genuinely interested contacts across all
history versus the 22 tagged — tens, not hundreds.

`lastMessageBody` holds only the most recent message, so anyone who replied and then got
answered shows as outbound-last. Scanning last messages will never find them; tags and
pipeline stage are the instrument, and both are incomplete.

Beware autoresponders when counting replies. Business missed-call bots read as engagement
and are not — one spa's AI receptionist alone produced 16 near-identical inbound messages.

### 23.3 The sending ceiling is one number, not lead supply

The location owns **three** numbers and every send has gone out on one:

| Number | Title | Use |
|---|---|---|
| `+1 361 301 9563` | Patrick's number 2 | Aug 21 batch AND Aug 22 batch |
| `+1 346 536 3161` | Patrick's number 4 | idle |
| `+1 346 615 4219` | Patrick's number 3 | idle |

On 2026-08-22 a manual batch of ~30 went out in **116 seconds** from that one number, all
with the same body and only a rotating opener. 100/day from a single 10DLC is where carrier
filtering starts; across three it is ~33 each. Spreading the load is the cheapest available
change to make a volume target actually deliver.

That batch also quoted a flat **"$30s/mo"** on business fiber, which the doctrine says not
to do — business is priced by speed tier — and promised "up to a $500 Visa reward card and
up to $750 in switching credits".

### 23.4 Tool limits found the hard way

- **`official_conversations_export_messages_by_location`** works at 1000/page but
  `nextCursor` comes back **static**, so paging loops on page 3. Use `startDate`/`endDate`
  windows instead. The location holds 11,650 SMS, ~7.9% inbound.
- **`get_sms_reports`** 404s — `/reporting/sms` is not available here.
- **`search_conversations`** caps at 100, no offset, sorted last-message descending.
- **`search_contacts`** has no tag filter and its `query` is substring matching.
- **`get_users`** needs a companyId; `search_users` returns 401.
- **GHL holds 0 estimates**, so no quote lives there.
- **The GHL workflow API saves actions but silently drops triggers.**
  `ghl_create_workflow` with a trigger fails with a Firestore
  `5 NOT_FOUND: No document to update` and leaves an empty shell;
  `ghl_update_workflow_actions` returns "updated successfully" and writes nothing.
  Verified by reading the workflow back: `triggers: []`. A scheduled sender can be built
  through the API right up to the trigger, which must be added in the UI.
  **Always read a workflow back after writing it — the success message is not evidence.**

### 23.5 Calendars: none were bookable

All **27** pre-existing calendars were inactive, so no appointment could be booked at all.
Created **`Optimus Fiber Appointments`** — `jSOOC383RNxHIRwo6zV8`, active, 30-minute slots.

**It still cannot be booked until open hours are set in the GHL UI.** Tested rather than
assumed: with no availability, `get_free_slots` returns nothing and `create_appointment`
fails with "The slot you have selected is no longer available" **even with
`ignoreDateRange: true`**. The MCP `update_calendar` has no open-hours parameter.

### 23.6 DealMachine, measured

`enrich_address` really costs **1–2 credits per address**, not the ~6 in older notes — 25
Devonwood addresses cost **39 credits** at a 100% match rate. Neither `enrich_address` nor
`enrich_latlng` has an `estimate_cost` flag, so probe one and read `credits.used` before
committing a batch. **`enrich_latlng` needs no ZIP**, which is how gold dots get enriched
despite street-only addresses.

About **12% of residential rows come back landline-only** with no wireless alternative.
Those are call leads, not dead leads. (Cross-check §1873: judge reachability across all
three number columns, not `phone_1` alone.)

### 23.7 The updater lied, and now it cannot

`_raw_refresh()` — the real updater on the field PCs, which have no git — swallowed every
failure in a bare `except: continue` and printed a success line driven by `got_main`, so it
announced "refreshed core files" even when eight of nine had failed. Nothing validated a
download, so a captive-portal or proxy login page returning HTTP 200 was written straight
over a working `.py`.

Fixed and deployed 2026-08-22: every download is parsed before it lands (`compile()` for
`.py`, `json.loads()` for `.json`) and anything that does not parse is refused with the
working copy kept; writes go through a temp file and `os.replace`; every file reports
updated / already current / FAILED with a reason. `_deploy_manifest()` prints the mtime and
byte fingerprint of every core file actually on disk, plus `MISSING` for any core file
absent from that PC. **That block is the answer when somebody says the update didn't take.**

### 23.8 Where the brain lives, and why this was nearly written twice

This file was not findable from `optimus-map-tools` at the start of the session: `main`
carried a 50-line stub last touched 2026-05-02, and the real brain sat on
`claude/lead-gen-software-research-brho9a`. A Part 22 was very nearly appended to the stub,
which would have produced two files both called the brain with no way to tell which was
current.

`CLAUDE.md` now exists at the root of `optimus-map-tools` and loads automatically in Claude
Code. The repo is also a **plugin marketplace** — `/plugin marketplace add
patricksiado-prog/optimus-map-tools` then `/plugin install optimus` — so Cowork and
claude.ai load the same brain, and a push updates everyone without anyone re-installing.
`optimus-brain/SKILL.md` is generated from `CLAUDE.md` by `scripts/build_brain_skill.py`
so the plugin cannot drift from the repo.

**The brain belongs on `main`.** A 3,110-line brain on a research branch is why it took a
whole session to find.

---

## 2026-08-22 (part 24) — THE DEALER PORTAL, PHOTOGRAPHED: THE DOTS VANISH WHEN YOU ZOOM IN

Ten screenshots from Patrick's HP, 2026-08-22 ~2:43 PM. Everything below is read off
those photos. Where a photo cannot settle something, it says so.

### 24.1 The nav path has not changed since 2026-07-01

Global Logon (`oidc.idp.elogin.att.com`) → **you Refer** home
(`youachieve.att.com/yourefer/`) → **AT&T Fiber** tile → fiber page → **Fiber
Availability Map** button → the dot map at `youachieve.att.com/yourefer/fiber`.
Identical to the sequence recorded from the July screenshots. `open_map_view()` is
still pointed at the right doors.

The you Refer top nav is **Home / My Referrals / Reports / Promotions**. `Reports` has
never been opened by anyone here. Referral status — what actually got installed and
paid — lives behind it, and every commission question so far has been answered by
guessing instead.

### 24.2 A second dealer UserID exists: `we1413`

The Global Logon shot shows **UserID `we1413`**. Every prior record in this brain and
in the archived CLAUDE.md says **`zg431x`**.

That matters beyond bookkeeping. **Phase 3 — the direct backend HTTP reader, the
end-state that drops the browser entirely — has `attuid=zg431x` written into the
endpoint:**

```
youachieve.att.com/yourefer/api/fiberMap.cfc?method=getMapData&lon=&lat=&attuid=zg431x&csrfToken=
```

If the session that is actually authorised now is `we1413`, that attuid is stale and
Phase 3 would authenticate as a user the cookie does not belong to. **Ask Patrick which
account is live before building against that URL.** Two dealer logins for two people is
just as likely as one having replaced the other; the photo cannot tell which.

**Do not chase the error string in that URL.** The address bar carries
`ERROR_TEXT=HPDBA0521|` with `ERROR_CODE=0x00000000` and `USERNAME=unauthenticated`.
It is present in the shot *before* the password is typed and unchanged in the shot
where it is being submitted. That is the ordinary unauthenticated-redirect querystring,
not a failed login. `ERROR_CODE` is zero.

### 24.3 ★ THE DOTS ONLY RENDER INSIDE A ZOOM BAND

Two views of **the same ZIP, 77706 Beaumont**, minutes apart:

| View | What the map shows |
|---|---|
| Wide (ZIP-level) | dots across the whole frame |
| Zoomed to street level | **not one dot.** Basemap, street labels, the blue location pin, nothing else |

The street-level shots are legible — Dowlen Rd, Charleston Ln, Whittaker Ln, Claybourn
Dr, Bankston Ln — and they are empty. The fiber did not go away in ninety seconds. **The
dot layer stops rendering past a zoom threshold.**

Two consequences, both expensive:

1. **Zooming in for precision returns fewer dots, not finer ones — it returns zero.**
   Any "zoom in / zoom out / restart" auto-hunt loop has to treat zoom as a *band to
   stay inside*, not a dial to turn up. A loop that zooms in to resolve a dense pocket
   will read that pocket as empty and move on. This is the mechanism that would silently
   skip the best territory.
2. **A human doing the same thing draws the same wrong conclusion.** Anyone who zooms in
   to read a street name sees a blank map and reports no fiber there. Tell the team: if
   the dots disappear, you zoomed too far — zoom back out, the dots are the data.

The exact threshold is not in these photos. **Finding it is one measurement**: load a
known-dense ZIP, step the zoom one level at a time, record the level where the dots stop.
Then pin the sweep to that band. Until somebody does that, the hunter's coverage has an
unmeasured hole in it.

This sits next to part 14 (the ~3,000-row cap is the real limit on coverage, not zoom).
Both say the same thing from different directions: **coverage is bounded by things
nobody has measured, and zoom is not the free lever it looks like.**

### 24.4 The live offer, in AT&T's own words

From `/yourefer/fiber`, verbatim, 2026-08-22:

> **Now delivering speeds up to 5 Gigs!**
>
> New and existing customers can get a 20% discount on either their wireless or internet
> account when ordering and activating at least one new qualifying service. Customer must
> have both services to qualify for the discount.

**This offer names existing customers, which is the definition of a gold dot.** Gold is
already an AT&T customer sitting on copper. The 20% is off an account they already pay.
That is a materially stronger opener than anything currently in the message copy, and it
is AT&T's own published wording, not a number invented here.

It also **does not break the never-quote-a-flat-price rule** — a percentage off their
existing bill is not a price quote. It stays inside doctrine.

Carry the qualifier or the message is false: **they must end up holding both wireless and
internet.** A fiber-only order does not earn the discount.

### 24.5 Streets and anchors captured, 77706 Beaumont

For cluster work later: Dowlen Rd, Delaware St, Charleston Ln, Claybourn Dr, Whittaker
Ln, Bankston Ln, Gracemount Ln, Heights Ave, Colton Ln, Madera Ln, Benton Ln, Ellington
Ln, Prescott Dr, Windrose Dr, Titan Dr, Barrington Ave, Turning Leaf, Savannah Trace.

Commercial anchors on Dowlen Rd: **H-E-B Plus + H-E-B Pharmacy, CVS Pharmacy, Exxon,
James Avery Jewelry.** A retail strip inside a residential grid — the shape that carries
small business alongside houses. `77067` (north Houston / Greenspoint) was also open and
visibly dense.

### 24.6 Colour read off a phone photo is not evidence — again

The wide views show bright green, pale periwinkle-blue and a darker green. It is
tempting to derive a legend from that. **Do not.** A phone camera pointed at an LCD
shifts hue, and a whole session has already been lost to pixel analysis of a photo of
this map that returned 227 clusters and classified every one of them wrong.

The authority is unchanged and it is the wire, not the picture: `classify_wire()` on
`subscriber_ban` + `curr_ntwrk_bld_type_cd` against `build_codes.json`. Photos are good
for nav paths, offer text, street names and **whether dots render at all** — which is
exactly what part 24.3 got out of them. They are not good for colour.

### 24.7 WHY the dots vanish — answered. It is a declared Mapbox threshold, and the hunter already reads it.

Researched 2026-08-22 against the Mapbox style spec. This is not a load failure, not
throttling, and not AT&T hiding data.

**A Mapbox style layer declares `maxzoom`, and the spec is explicit: at zoom levels
*equal to or greater than* the maxzoom, the layer is hidden.** It is an optional number
0–24. Zoom to that level and the layer stops drawing — instantly, completely, with no
error. That is exactly the behaviour in the 77706 screenshots: full dots at ZIP level,
absolute zero at street level, same page, ninety seconds apart.

**The distinction that pins it to the layer and not the data:** if the *source* tileset
ran out of tiles at some zoom, Mapbox **overzooms** — it scales the last available parent
tile up and keeps drawing. You would see the same dots, slightly imprecise, not none.
Dots going to exactly zero is the signature of a **layer** `maxzoom`, not missing tiles.
(Mapbox's own docs: "if you zoom in past a layer's maxzoom, the layer with that maxzoom
value will disappear.")

**The hunter has been measuring this since 2026-08-20 and nobody has read the output.**
`MAPBOX_VIEW_JS` walks `m.getStyle().layers`, keeps the circle/symbol layers whose id
contains dot/fiber/elig/serv/addr/point, and records each one's `minzoom`, `maxzoom` and
live `queryRenderedFeatures().length`. `read_map_view()` prints it once per run:

```
  DOT LAYERS (the zoom range where dots exist):
    <layer id>                     min=...  max=...  rendered now=N
```

**That block is the answer. Read it on the next run and the exact band is known** — no
experiment needed. Same failure pattern as `wire_classification_report()`: the software
already answers the question and the printout goes unread.

**One real gap in it.** The advice line under that block reads:

```
    -> zooming out below the highest 'min' shows NO dots at all.
```

It only warns about the **minzoom** end. Patrick's screenshots are the **maxzoom** end —
zooming *in*. The value is captured, the warning is not. Worth extending to name both
ends; it is a print string, nothing structural.

**The sweep is fenced on both sides, for two unrelated reasons:**

| Direction | What stops you | Symptom |
|---|---|---|
| Zoom **out** too far | layer `minzoom` — layer not drawn | no dots |
| Zoom **out** too far | the ~3,000-row backend cap (part 14) | dots, but the reply silently truncates and ground is missed |
| Zoom **in** too far | layer `maxzoom` — layer hidden | no dots |

The usable sweep zoom is the intersection of those, and only the middle one has ever been
quantified. **An auto-hunt loop that treats zoom as a dial to turn up will drive itself
out of the band and read live territory as empty.** Zoom is a band to stay inside.

Tell the team the same thing in one sentence: **if the dots disappear when you zoom in,
you zoomed too far — back out. The dots are the data, and a blank map is not an answer.**

Sources: Mapbox Style Spec — Layers (`maxzoom`: "At zoom levels equal to or greater than
the maxzoom, the layer will be hidden"); Mapbox Help — "Adjust the zoom extent of your
tileset" (overzooming, and layer-maxzoom disappearance).

### 24.8 The banner now reads the web, because two of the three tabs it read do not exist

Audited the master sheet 2026-08-22. **`Outage Signals` and `Fiber Zones` are not
tabs and never have been.** So the banner's two intel lines were reading nothing and
reporting "none open" and "no zone scans", which reads as *we checked and there is
nothing* when the truth was *nothing was ever checked*. `Enriched Leads` and `New
Fiber Alerts`, both named in `CLAUDE.md`, are not real either.

`Gold Dots` **is** real: **3,328 rows, latitude and longitude both populated in C and
D.** So the gold-pocket fallback has data and was still coming back empty — cause not
yet identified, and the banner will now name which of three steps loses it (0 rows
read / rows but no usable coordinates / coordinates but no cell with 4+).

Shipped `optimus_web_intel.py` (deploy `92a128a`, **in `_CORE_FILES`** — without that
it reaches no field PC). Google News RSS, Bing News RSS and Reddit r/ATT, filtered to
Houston metro / Beaumont / Brazoria, with any Texas ZIP pulled out of the headline and
printed as somewhere to scan.

Three properties worth keeping if this is ever rewritten:

- **One six-second wall-clock budget for all six sources.** Past it nothing further
  starts. Intel must never delay a sweep, and the import is guarded so a PC that
  failed to download the new module still scans.
- **Items are bucketed by their own words, not by the query that found them.** News
  search is fuzzy and both queries return each other's stories. Outage words win
  ties — calling a cut "a new build" sends a rep to the wrong street for a day, the
  reverse costs a glance.
- **An empty result never overwrites a good cache.** One offline launch used to throw
  away yesterday's intel for every launch after it. An expired cache is now shown as
  a fallback shouting **STALE** and its age rather than passed off as current.

**The feeds could not be live-verified** — the sandbox blocked every outbound host. The
source list is therefore *data*, and every parser is defensive. `python
optimus_web_intel.py` on a real machine prints which sources answered, how many items
each yielded and why any failed. **Prune the list from that output, not from
guesswork.**

**Autosheet is out of credits** (`dashboard.gptforwork.com` → billing) and a run died
mid-query, leaving a temp tab **`ZZ_TMP_GRID`** (~3,300 rows of formulas) in the master
sheet. Delete it. The cause was a prompt that pushed the agent into reading `Gold Dots`
wholesale — the exact thing this brain already warns about.

### 24.9 The ZIP suggestion is a DISPATCH now, not a report

Patrick, verbatim: *"if I scanned a bunch of gold in Beaumont that's mine. I don't
want zack to go there. I want the zip suggestion to tell him where to go."*

That reframes what the suggestion is for. It is not a summary of what we captured.
It is **an area, claimed by a named operator, at a time.** Deployed `c2df228`.

**Announcements went nationwide.** New-build stories are now searched across the
21-state AT&T fiber footprint, not filtered to Houston and Beaumont. That filter was
backwards for this job: an announcement exists to say where to send the scanner
**next**, which is by definition somewhere nobody has been. Outages stayed local —
an outage is a selling event where reps are already standing, and a cut in Ohio is
not our problem.

**`optimus_territory.py` holds the ledger**, on a `Territory Claims` tab the banner
creates on first run:

```
Claimed At | Operator | Machine | Area | State | ZIP | Source | Status | Released At
```

Once Patrick holds Beaumont it leaves everyone else's go-list and shows to them as
*held by Patrick since …* — visible rather than silently missing, so nobody wonders
where a market they saw in the news went. A second claim on a held area is refused
and the refusal names the holder. Release writes `RELEASED` instead of deleting, so
who worked what survives. **A claim expires after 21 days** — somebody who claimed a
market and never went must not lock it forever.

Identity needed no new plumbing: `OPERATOR()` and `optimus_operator.py` have been
stamping every captured row for months.

**Captured data and dispatch are now separate sections.** Our gold pockets still
print, relabelled `ALREADY WORKED BY US -- captured gold, NOT a suggestion`. The count
is worth seeing; mixing it with where-to-go is what made the old banner useless.

Flags: `--claim "Beaumont, TX"`, `--release`, `--territory`. Claiming runs before the
browser opens and quits, so taking or handing back a market does not cost a launch.

Two things caught in test that would have bitten:

- **Area keys must normalise.** `"Beaumont, TX"`, `"beaumont tx"` and
  `("Beaumont", "TX")` have to collapse to one key or the same market gets claimed
  twice under two spellings and the collision the whole module exists to prevent
  happens anyway.
- **Place extraction stays conservative.** An unparseable headline yields no target
  rather than a guessed one. A wrong city sends somebody to the wrong state for a day.

### 24.10 The Aug 22 batch: 100 sent from DealMachine data, and what it actually measured

Sent 2026-08-22, 16:49–17:37 Central. 100 texts, 0 send failures, 0 Twilio 30006.

**Sourcing changed.** Gold Dots was unreadable (Autosheet out of credits), so the
list came from **DealMachine property search** instead: owner-occupied single-family
in 77706 Beaumont, 77571 La Porte, 77515 Angleton. 135 properties → **350 credits**
(2.8/property, not the 6/property the estimator quoted) → 116 textable after dropping
**13 landline-only (9.6%, close to the 12% rule of thumb)** and 6 with no contact.

**This is a different kind of list and the copy had to change to match.** DealMachine
knows nothing about fiber, so these are homes in a fiber ZIP, not verified dots. Every
message was rewritten to claim fiber **on the street or in the area** and offer to
check the address — never that the address qualifies. The gold "you're on copper"
angle was dropped entirely: without a dot we do not know who is an AT&T customer.

**The result, stated plainly: 8 opt-outs from 100. 8%.** Under the 20% rotate-the-
number line, but four times the rate at the 25-message mark, and the genuinely
interested replies were **zero**.

**The comparison that matters, and it is not the flattering one:**

| | Aug 21 | Aug 22 |
|---|---|---|
| Sent | 100+ | 100 |
| Replies | 0 | ~2 |
| Opt-outs | **0** | **8** |

It is tempting to read Aug 21's zero opt-outs as the better batch. It is more likely
the opposite: a 388-character, three-segment message with a doubled STOP line got
**ignored**, and nobody bothers opting out of a text they never read. The Aug 22 copy
was read — and 8% of the people who read it said no. **Zero opt-outs is not a sign of
good copy. It is a sign of no attention at all.**

What that leaves: the one-segment rewrite fixed *delivery into the reader's head*, and
did not fix *the offer*. A cold text saying "fiber is on your street, want me to
check?" gets read and declined. The next lever is not more texts.

**A conversation AI in the location auto-replies to every inbound**, and it is
actively hostile to the funnel. On Celia's thread it pushed after she declined twice,
published Patrick's personal cell to her, told her twice to "reply STOP anytime" when
she asked where her data came from, and then placed a voice call she declined. She
opted out. **Any measurement of opt-out rate here is contaminated by that agent** —
some unknown share of the 8 were manufactured by the bot, not by the copy.

Before the next batch: turn that agent off or rewrite its script, and answer the data
provenance question honestly ("public property records, matched to a fiber build")
rather than "I don't have access to those details."
---

## 2026-08-22 (part 25) — THE BEAUMONT CSV WAS ALREADY WORKED. AND T-OPTIMUS IS REACHABLE NOW.

Patrick, 2026-08-22: *"can u text 100 resi customers"*, attaching
`dealmachinecontacts20260820101612.csv`. The answer turned out to be 5, not 100, and the
reason is worth writing down because it will happen again.

### 127. The file: 130 contacts, 79 households, 74 already texted

`dealmachinecontacts20260820101612.csv` — 130 rows, every property address Beaumont 77706
on Ivanhoe Ln (79), Afton Ln (49) and Dowlen Rd (2). **79 unique households.** The row
count is people, not doors: 6380 Ivanhoe has 5 owners on it, 6360 has 4, 6322 has 3.
Always dedupe on `associated_property_address_full` before counting a list.

Every phone that survives parsing is `Wireless` — 172 of them. The literal string
`Landline Excluded` appears in phone columns and is **not a number**; it must be filtered
by digit-extraction, not treated as data. 93 of the 172 carry `DO NOT CALL`.

Checked all 33 households that `beaumont_send_v2.json` (the 61-row clean-wireless list,
§90) did not cover, one at a time against GHL. **28 of the 33 were already in T-OPTIMUS
with an SMS on record.** Only 5 had no GHL contact at all:

| Name | Phone | Address | Carrier |
|---|---|---|---|
| Toye Babb | 409-550-1686 | 6150 Afton Ln | AT&T Mobility |
| Patricia Whitmire | 409-790-4808 | 6165 Afton Ln | T-Mobile |
| Allison Ruffing | 334-221-5640 | 6290 Afton Ln | T-Mobile |
| Mollie Williford | 409-791-0632 | 6367 Ivanhoe Ln | AT&T Mobility |
| Robert Thewman | 409-720-7085 | 6384 Ivanhoe Ln | Verizon |

All 5 texted 2026-08-22 ~4:50pm Central, individually written, opt-out language, no flat
price quoted. Tagged `fiber resi round2` plus the street address. All 5 came back
`"new": true` from `upsert_contact`, which is the independent confirmation that they had
never been loaded.

**The whole file was already blasted on 2026-08-20 between roughly 16:00 and 19:10 UTC**,
DNC-flagged contacts included — not the 24 that §125 records. §125 undercounts.

### 128. Every contact in the file sits in an open opportunity, stage "Contacted"

Pipeline `2V9thfxQpuhn6ZP0Peqt` ("AT&T Leads"), stage id
`40483078-8d28-4155-a81b-a80d000efce2`. Every single Beaumont contact checked is in it,
open. The dialer is also still working them — Michael Laidler (6316 Ivanhoe) has campaign
calls on Aug 21 **and** a manual call on Aug 22 20:43 UTC, hours before this session ran.

**This list is live, not stale.** A blind re-blast would have been a second message into
an active call campaign, which is exactly the send that spikes opt-outs.

### 129. CORRECTION to §92 — the connector CAN reach T-OPTIMUS now

§92 says the connector token cannot reach T-OPTIMUS (`xZj500PjsflIQg2j9f9D`), returns 403,
and that contacts therefore go to Frontline Direct. **That is no longer true.** Every read
and write in this session — `get_contact`, `search_contacts`, `search_conversations`,
`upsert_contact`, `send_sms` — ran against `xZj500PjsflIQg2j9f9D` and succeeded. The
Beaumont contacts live there, not in Frontline Direct.

The open question §92 raises — *which location does Dave actually dial* — is answered by
the data: **T-OPTIMUS**. That is where the pipeline, the opportunities and the dialer
activity are.

### 130. `search_contacts` — the phone parameter is broken, the query parameter is not

```
search_contacts(phone="+14093386376")
  -> GHL API Error (500): GHL API Error (400): value?.map is not a function
search_contacts(query="4093386376")
  -> the contact
```

Pass **bare 10 digits as `query`**. Same for names. **Address search does not work at all**
— `query="Ivanhoe"` returns 0 despite 79 contacts carrying it in `address1`.

To prove a contact was texted: `search_conversations(contactId=...)` and look for **`2` in
`messageTypes`** (2 = TYPE_SMS, 8 = TYPE_CAMPAIGN_CALL, 1 = TYPE_CALL, 22 =
TYPE_CUSTOM_PROVIDER_SMS). `dateUpdated` on the contact is a weak proxy and will mislead —
Shainaaz Ibrahim's contact was updated 4 minutes after import yet has an SMS on record.

### 131. The blast copy quotes a flat price. The doctrine says never do that

The message that went to all ~125 of them reads *"providing speeds 10x faster for just
$30/month."* `gold-dot-workup` is explicit: never quote a flat figure, say "in the $20s to
$30s for the first year, I'll confirm your exact price before anything is ordered."
Fiber 300 is $55 base before promo, autopay and bundle discounts, and it steps to ~$40-45
after twelve months. **A quoted $30 that becomes $45 in month 13 is a chargeback and a
cancelled order**, and the pay is $500 a green door.

Noting it, not changing it — the workflow copy is Patrick's to set.

### 132. Where the next 100 resi actually come from

Beaumont 77706 Ivanhoe/Afton/Dowlen is exhausted. The file is worked. To text 100 more
residential, one of these has to happen:

1. **Enrich new addresses.** 14,223 DealMachine credits remain, cycle ends Sep 2. At the
   measured ~6 credits/address (§107) that is ~2,370 addresses — far more than 100. Pick a
   fresh gold cluster, take the green inside it (§120-121), enrich, text.
2. **Read the replies first.** 42+ texts went out Aug 21 and the reply rate has still never
   been read. §43 has been open since April. Spending credits before measuring the return
   on the sends already made is spending blind.
3. **`--backfill-gold`** — ~6,324 gold rows, free, still not run. It costs nothing and it
   picks the cluster in step 1 for you.

Step 2 is free and step 3 is free. Do those before step 1.
