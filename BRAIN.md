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
