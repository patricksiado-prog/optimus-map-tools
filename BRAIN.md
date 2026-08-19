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
