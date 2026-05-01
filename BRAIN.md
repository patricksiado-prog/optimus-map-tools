# OPTIMUS HOUSTON - BRAIN

Last updated: 2026-04-30
Patrick Siado, AT&T fiber sales rep + small team
Full institutional memory — read this first when resuming any session

---

## NORTH STAR
500 fiber sales/week from 20K+ AT&T fiber-eligible addresses.
Phase 2: 1000/week. Phase 3: 2000/week.
Mobile-first ops. Phone-based admin.

---

## TEAM WORKING AGREEMENT
- Patrick: sales side - calling, texting, customer-facing
- Tech partners (India, ~$200/wk): run scripts, push code, set up cloud, NO PYTHON expected
- Claude: ALL coding, all debugging, all architecture
- When stuff breaks: describe error or screenshot, Claude rewrites/fixes
- Patrick is 45, makes own decisions
- DON'T mention sleep, time, battery, call him boss/CEO
- DON'T reference past success ($10M, 104K accounts 2016-2019) externally - drives up contractor costs
- Treat like robot working with a robot

---

## CORE INFRASTRUCTURE

### GitHub
- Repo: github.com/patricksiado-prog/optimus-map-tools
- Token: /storage/emulated/0/Download/github_token.txt
- Auto-update URL for fiber_hunter:
  raw.githubusercontent.com/patricksiado-prog/optimus-map-tools/main/fiber_hunter.py

### Google Cloud
- Project: fiberscanner-493900
- Service account: fiberscanner@fiberscanner-493900.iam.gserviceaccount.com
- Creds: /storage/emulated/0/Download/google_creds.json
- KNOWN LIMIT: service accounts have ZERO Drive storage quota
  - Can READ/UPDATE existing files, NOT CREATE new ones
  - Workaround: GitHub for files, Drive for pic backup only

### Sheets
- Active: 12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag
- Original: 15ymTkIGPWs6quB035l414ns5hkG9cQ5xr_W4ukd0OAA "ATT FIBER LEADS"
- 15 tabs, 41,000+ rows total
- Hard limit: 10M cells per workbook (~9M used currently, ~6-7M trimmable)

### GHL (GoHighLevel)
- Account: Optimus Houston
- Location ID: TXw28sw0Z2rl6tcCDhJY
- 41,325 contacts loaded
- A2P 10DLC fully approved (Brand, Campaign, SHAKEN/STIR, CNAM all green)
- Twilio number active
- Daily SMS limit: 100/day (need increase to 1000)
- 244 hot leads queued for tomorrow's dialing
- 592 unread inbound replies in inbox
- URL: app.gohighlevel.com/v2/location/TXw28sw0Z2rl6tcCDhJY/

### Drive
- Folder: "Fiber Map Snap Shots" id 1whewiysliFB4rs1TqZYZk5NA43Es08Ad
- 326+ map pics backed up
- Service account can list/read but NOT create

### Working Directory (laptop)
- C:\\Users\\patri\\Desktop\\
- C:\\Users\\patri\\OneDrive\\Desktop\\

---

## SHEET TABS (CRITICAL - know what each is)

### Lead tabs
- All Leads - 14,523 rows (master log)
- Commercial - businesses (Map Man writes phones here)
- Residential - 23,100 rows
- Green Commercial - 728 verified fiber-eligible biz
- Green Residential - 5,981 verified fiber-eligible homes
- $ LEADS - 5,301 validated with phones
- Ready To Call - 10,000 (filtered/clean call list)
- All Biz Phones - 2,743 (phone enrichment dump)

### Intelligence tabs
- HOT ZONES - 88 hot zone alerts
- GOLD ALERTS - 98 recent gold dot surges
- Gold Clusters - 100K rows but only 3 with data
- ZONES, Changes - tracking tabs
- Validator Man, Address Man - tool output tabs

### Sheet column conventions

**Commercial tab:**
A=Business Name, B=Address, C=Phone, D=Category, E=City, F=State, G=ZIP

**Ready To Call:**
A=Name, B=Phone, C=Address, D=City, E=State, F=ZIP

**All Biz Phones:**
A=Name, B=Address, C=Phone, D=Category, E=City, F=State, G=ZIP

---

## DOT COLOR CODES (CONFIRMED from real AT&T map legend)

- GREEN = Fiber eligible / NON-customer (PRIME COLD-PITCH TARGET)
  - Pitch: "Fiber is lit at your address, $80/mo, free install"
- ORANGE/RED = Fiber eligible / COPPER customer (FORCED upgrade target)
  - Pitch: "Your copper line is being retired, fiber is the upgrade"
  - FCC approved copper retirement in 30%+ wire centers by 2026
- GREY = Existing fiber customer
  - Pitch: "Want to upgrade to Gigapower symmetric?"
  - Use for SOCIAL PROOF: "Your neighbor at 1230 Main has had AT&T fiber 2 years"
- BLUE = Fiber upgrade available (less common)

### Calibrated colors (proven on 4 real tiles)
- GREEN target: RGB(65, 166, 0)
- GREY target: RGB(137, 137, 137)
- ORANGE target: RGB(255, 0, 0)
- Detection: saturation-based, NOT exact RGB match
- Filter: aspect ratio <= 2.0 (round dots only)
- Size: 25-600 pixels per dot

---

## DOT DETECTION RESULTS (PROVEN)
Tested on 4 real fiber map tiles tonight:
- tile_r2_c3_refine_6_debug.png at high zoom = 47 GREEN + 5 ORANGE + 97 GREY = 149 dots
- Scanner's "count=N" filename labels are UNRELIABLE (one labeled count=10 actually had 149)
- Total est: 326 pics x 50-150 dots each = 15K-50K real addresses

---

## GEOCODING LESSONS LEARNED THE HARD WAY

### Nominatim (free, OpenStreetMap)
- 1 req/sec rate limit (HARD)
- Going faster = empty results / "NEEDS REVIEW" rows
- 60-70% of fast-fired calls return coord-only junk
- Fix: time.sleep(1.1) between calls
- Fallback: Photon (free, no rate limit)

### v1 fiber_scan failure mode
- Old fiber_scan rushed Nominatim, got back coordinates dumped as "addresses"
- Sheet rows like: "29.84659,-95.27686 UPGRADE ELIG RESIDENTIAL Houston TX"
- Useless for door-knocking, calls, validation
- Fix in v2: rate-limit + retry + Photon fallback + skip if both fail

### Vision API (Google Cloud, paid)
- Free tier: 1,000 calls/month
- Patrick rejected for daily 1000-pic scale ($45+/mo)
- Use: Tesseract on laptop instead (free, unlimited)

---

## TOOLS BUILT (with where they run)

### Phone-based (Pydroid 3)
- brain.py v2 - Read/write BRAIN.md to GitHub via menu
- backup_drive.py - Pull repo files, archive to Drive
- process_drive_pics.py - Detect dots + Vision OCR (Vision API needed)
- sheet_cleaner.py - Trim wasted sheet cells
- push_to_repo.py - Push any file from Downloads to GitHub
- push_brain_complete.py - This file (push BRAIN updates)

### Laptop-based
- fiber_hunter.py v5.7 - PRIMARY scanner, news-driven, RES/COMM tag, spiral mode
- fiber_scan.py v10.0 - Backup scanner, Houston-only
- themapman.py v9.4 - Playwright biz scraper
- validatorman.py - AT&T API validator
- addressman.py - Address standardizer
- ready_to_call.py - Merger that joins fiber + phone data into Ready To Call list
- dot_extractor.py - Tesseract OCR + dot detection (Windows)
- rename_pics.py - Bulk rename pics by content
- geo_extractor.py - FREE pipeline: Tesseract + Nominatim -> addresses

### Pydroid Python toolkit (ALL INSTALLED)
numpy, gspread, google-auth, google-api-python-client, requests,
phonenumbers, beautifulsoup4, pillow, google-cloud-vision

---

## SCANNER DEEP KNOWLEDGE

### Motion (proven, don't change)
- PAN_PIXELS = 300 (v1 default, sometimes 150 for tighter overlap)
- Drag from MAP_CX/CY (mouse drag pan)
- Click "Search this area" button after pan (REQUIRED, no keyboard shortcut)
- WAIT_AFTER_PAN = 1.5-2.5s
- WAIT_DARK_RETRY = 3.0s if map dark
- Search button position calibrated once, saved to search_button_pos.json

### Calibration files (laptop)
- search_button_pos.json - "Search this area" pixel position
- scan_progress.json / scan_progress_N.json - resume state
- zone_history.json - past scan history
- spiral_state.json - spiral pattern state
- geocode_cache_v2.json - geocoded results cache
- gold_cluster_log.json - gold dot tracking

### Color detection (calibrated for AT&T map)
- ORANGE: RGB (200,120,0) to (255,200,90) - copper customers
- GREEN:  RGB (30,130,30) to (100,210,80) - fiber eligible
- BLUE:   RGB (50,80,180) to (120,160,255) - existing customers/gray
- MIN_DOT_PIXELS = 3
- CLUSTER_THRESHOLD = 15

### Map calibration (Houston anchor)
- LAT_PER_PIXEL = -0.000015
- LNG_PER_PIXEL = +0.000020

### Known classification bias
COMMERCIAL keywords: pkwy, parkway, blvd, plaza, business, industrial, etc.
RESIDENTIAL keywords: court, ln, lane, way, trail, place, etc.
Numbers/no_number heuristic: 5-signal reclassification

---

## STRATEGIC FRAMEWORKS

### Sales Channel Reality
- AT&T fiber and Verizon Fios DO NOT OVERLAP geographically
- STOP saying "AT&T vs Verizon" - never compete head-to-head
- Real Texas competitors: Spectrum (PRIMARY target), Xfinity (secondary), Google Fiber (Austin only)
- Real Lumen-state competitors: Ziply, Comcast in some metros

### Pitch By Competitor (Locked In)
- SPECTRUM: outage stats + neighbor proof + free trial parallel
- XFINITY: no data cap + bundle savings + price stability (NOT speed)
- DSL (Lumen/CenturyLink/Frontier): "your service is being retired" + 10x speed

### Three Strike Strategies
1. CABLE OUTAGE STRIKE
   - LIVE STRIKE (0-4hr): text blast residential + biz with cells
   - AFTERMATH STRIKE (4-48hr): phone calls
   - PATTERN STRIKE (2+ outages in 30 days): premium commercial

2. TEXT-ON-REQUEST BATTLE CARD
   - Agent on call: "want me to text you the details?"
   - Auto SMS with: nearby AT&T customers, Spectrum outages, pricing

3. GREY DOT SOCIAL PROOF
   - "Your neighbor at 1230 Main has had AT&T fiber 2 years"
   - Existing customer intel = social proof on every cold call

### Field Wisdom (Patrick's experience)
- Old residential fiber lists = LOW conversion
- Google Maps filtered for CELL phones + texting = winning channel
- AT&T cell service $10-20 = strong bundle hook
- Lead with cell deal, fiber follows naturally
- Mortgage brokers, credit repair shops, business consultants = PRIME fiber targets
  (run on phones + internet, easy pitch)

### TAM Reality
- 37.5M fiber locations passed Q1 2026, 12.5M subscribed = 25M UNSOLD
- Legacy AT&T penetration 40% (60% unsold)
- Lumen-acquired (Feb 2026) 25% (75% unsold = PRIORITY)
- 8M new fiber locations going live 2026 (~150K/wk nationwide)
- D2D channel = 20-25% of fiber adds = our lane

---

## TEXAS HOT ZIPS (Tier S)
- 77024 Houston Memorial - mature, premium
- 77019 Houston River Oaks - dense
- 77382 The Woodlands - mature + active builds
- 77479 Sugar Land - commercial heavy
- 78258 Stone Oak SA - high-income
- 78023 Helotes - fresh build, low competition
- 75093 Plano West - DFW core dense biz
- 76065 Midlothian - recently lit
- 79932 West El Paso - BEAD virgin builds

## Cable Outage Activity (2026-04-30)
- Houston/Spring 77388 - Spectrum drop confirmed
- Cypress - biweekly outage history
- Austin Wells Branch - recent fiber-line attack
- San Antonio/Corpus/RGV - recent mass Spectrum outage

---

## SMS DELIVERABILITY RULES (LEARNED HARD WAY)

### Why messages get blocked (error 30007)
- HTML tags in message (br, p, etc) = #1 spam trigger
- Promising "Free iPhone" or "$$" = #2 spam trigger
- Signing as "AT&T" = brand impersonation, can REVOKE A2P approval
- ALL CAPS = spam filter
- Links without branded shortener = filter
- Emojis = some carriers flag

### What works
- Plain text only
- Sign with name only ("- Patri") OR "Patri (AT&T Authorized Rep)"
- NEVER "AT&T" alone
- Soft CTA (question)
- STOP language at end
- Under 160 characters when possible

### Common GHL/Twilio error codes
- 30007: Carrier filter (spam) - rewrite message
- 30003: Unreachable - dead number
- 30005: Unknown - invalid number
- 30006: Landline - can't text
- 21610: Recipient opted out (STOP'd)
- 21611: Number not on A2P campaign
- 30034: Toll-free unverified

### A2P 10DLC compliance
- Approved for Optimus brand (your business name)
- DOES NOT cover: signing as AT&T, claiming to be carrier
- Burn it once = months to get re-approved
- New campaign = test with self first, never bulk first

---

## SMS SCRIPTS (BATTLE-TESTED)

### Cold open (curiosity hook)
"Hi u wanna hear who's got it and loves it? Spectrum was out 13x this year, AT&T 0. What's up wanna give me a maybe on a free trial run parallel?"

### Live outage residential
"[Name] - Patrick @ AT&T. Saw Spectrum just dropped in [ZIP]. AT&T fiber is live at your address. Same-day install? Reply Y."

### Live outage commercial
"[BizName] - saw your area's Spectrum is down. How much per hour are you losing? AT&T fiber is lit at [address]. Reply Y for emergency install."

### Aftermath
"[Name] - your area got hit again yesterday. AT&T fiber is live at you. 5 min call?"

### Pattern (commercial)
"[BizName] - your ZIP has had 4 Spectrum outages this month. AT&T fiber 99.9% SLA."

### Battle card text-on-request
"[Address] - fiber confirmed lit. Your block: [neighbors]. Spectrum [ZIP]: [N] outages YTD. AT&T: 0. 1Gig $80/mo, free install today, 30-day trial run parallel. Reply YES."

### Workflow message (CLEAN, replaces old br tag version)
"Hi - quick heads up, fiber internet just opened up at your business address.

Faster speeds, no contracts, business pricing.

Want me to send you the rates? - Patri

Reply STOP to opt out."

---

## CONSTRAINTS LOCKED IN

### Tech
- Google Sheets: 10M cells/workbook hard limit
- pyautogui: laptop only (no Android)
- Tesseract: laptop only (no Android)
- gspread/data scripts: phone OK
- Service accounts: ZERO Drive storage write quota
- Nominatim: 1 req/sec rate limit
- Vision API: 1000/mo free, $1.50/1000 after

### Business
- GHL: 100 SMS/day (request increase)
- Workflow brand impersonation: NEVER sign as AT&T
- TCPA: residential needs explicit opt-in
- A2P: Optimus brand approved, AT&T claim NOT covered

### Operational
- AT&T scanner may get patched - scrape aggressively while it works
- Houston saturation: older neighborhoods 40% gray
- Out-of-state markets: scan before calling

---

## BUILD QUEUE (priority order)

1. CLARIFY: Where is coordinate metadata stored per tile?
   (Patrick said "in bottom of screenshot, logic writes to all leads file"
   but sample tiles don't show visible coords - need to find the actual source)

2. battle_card.py - Agent types address -> fiber status + neighbors + outages + speeds + pricing, SMS-ready

3. outage_hunter.py - Scrape DownDetector + cross-ref Green Commercial -> STRIKE NOW/24H/PATTERN tabs

4. Master DB with change detection (compressed deltas):
   - 3 tabs: MASTER_DOTS + CHANGE_EVENTS + WEEKLY_AGGREGATES
   - Track GREY->ORANGE (FCC retirement activating)
   - NONE->GREEN (new build, be first)
   - ORANGE->GREY (lost to AT&T direct)
   - GREY->GREEN (win-back opportunity)

5. Zoom-aware confidence scoring
   (low-zoom cluster dots != individual addresses)
   (only count high-confidence toward sales totals)

6. Multi-pass scanner (broad first, drill-down on hotspots)

7. 10 parallel scanners - options:
   A) Reverse-engineer AT&T API (FREE, fastest, may get blocked)
   B) Cloud VM 10x headless Playwright (~$150-200/mo)
   C) Tech partner cloud farm
   Single scanner zoom 18 = ~96 days serial Houston metro
   10 parallel = ~10 days

8. fiber_hunter Playwright conversion (4-8 parallel local)

9. live_validator.py - 2-sec mobile call-center lookup

10. Bulk validator for all 41,325 GHL contacts

---

## OPEN QUESTIONS / NEXT SESSION

- Where exactly is coordinate metadata in scanner output?
  (Bottom strip? Sidecar JSON? In All Leads sheet by filename?)
- 10-scanner architecture decision (cloud vs API)
- Tech partner names + roles for BRAIN
- Vision API billing yes/no for OCR scaling
- SMS limit increase request status

---

## RESUME NEXT SESSION

Tell Claude:
- "pull BRAIN" or
- "read BRAIN from github.com/patricksiado-prog/optimus-map-tools"

Claude pulls latest, fully synced, picks up at next BUILD QUEUE item.

---

End of BRAIN.

---

## CABLE WEAKNESS MAP — HOUSTON (added 2026-04-30)

### Dominant Cable in Houston = Xfinity/Comcast
Spectrum is more San Antonio / Austin / Corpus / RGV.
Houston metro = mostly Xfinity, which means our outage angle here is Xfinity-flavored.

### Active Hate ZIPs (Xfinity dropouts, public complaints)
| ZIP | Area | Signal |
|-----|------|--------|
| 77018 | Oak Forest | Xfinity drops all day long, work-from-home complaints |
| 77044 | NE Houston | Week-long outages, residents threatening to switch |
| 77008 | Heights / Garden Oaks | Customer publicly switched to AT&T after week-long outage |
| 77388 | Spring | Spectrum drop confirmed |
| Cypress | NW | Biweekly Xfinity outage pattern |

### THE EZEE FIBER WEDGE 🔥 (NEW ANGLE - HOUSTON SPECIFIC)
Ezee Fiber is a Houston-based fiber competitor actively destroying neighborhoods.
Their BBB accreditation was revoked June 2025. They are being sued.
This is the SHARPEST wedge we have in Houston right now.

**Confirmed Ezee damage zones:**
- **Briarhills subdivision** (Energy Corridor, near Addicks-Howell) — April 2026 — property damage, residents furious, KPRC news coverage
- **Katy / Fort Bend MUD No. 2** (Williamsburg Colony, Williams Chase) — sued for $70,000, broke water mains, 1,150 homes lost water, boil water notice
- **Oak Cliff Place** (NW Houston / Jersey Village) — water pipe breaks, up to 3 leaks per day at peak
- **General Houston** — BBB complaints stacking, 7+ month unresolved damage tickets, sprinkler/irrigation breaks pattern

**The pitch flip:** Ezee dug up their yard. AT&T fiber is already lit. No digging needed.

### STRIKE LIST (priority order for fiber_hunter runs)
1. 🔥🔥🔥 **Briarhills 77077 / 77079** (Energy Corridor) — Ezee just hit them
2. 🔥🔥🔥 **Katy MUD 77449 / 77450 / 77494** — Ezee water main lawsuit fresh news
3. 🔥🔥 **77018 Oak Forest** — Xfinity hate
4. 🔥🔥 **77044** — week-long Xfinity outage history
5. 🔥🔥 **77008** — neighbors already switching to AT&T
6. 🔥 **Jersey Village / Oak Cliff Place NW** — Ezee damage history
7. 🔥 **77388 Spring** — Spectrum drop

### SMS VARIANTS

**Ezee wedge (Briarhills, Katy MUD areas):**
> Hi neighbor - saw Ezee Fiber tore up your block last week. AT&T fiber's already lit at your address - no digging, no torn-up yard, install tomorrow. Want speeds + price? Reply Y.

**Xfinity outage (77018, 77044, 77008):**
> [Address] - saw Xfinity dropped your block again. AT&T fiber lit at you, 99.9% uptime SLA. 1Gig $80, free install, 30-day parallel run. Reply YES to lock it.

**Ezee water main (Katy):**
> Hi - your MUD is suing Ezee for breaking water mains. AT&T fiber doesn't dig in your neighborhood - it's already there. Want me to check your address? Reply Y.

### NEW BUILD CHATTER (Houston growth zones)
- The Woodlands 77382
- Sugar Land 77479
- Cypress 77433 / 77429
- Katy 77449 / 77494
- Energy Corridor 77077 / 77079
- Stone Oak SA 78258 (TX core, not Houston)

### OPEN ITEMS
- Confirm exact Briarhills street range (target by-block, not by-ZIP)
- Pull Williamsburg Colony / Williams Chase address lists
- Run fiber_hunter on top 3 strike ZIPs and compare hit rate
- Build Ezee-specific landing page or SMS opt-in flow

---

---

## SESSION 2026-04-30

### Numbers
- 15+ calls dialed in evening session
- 5 interested + 1 angry-existing recovery = 6 actionable contacts
- Interested rate jumped from ~0% prior sessions to ~30-40% this session
- Driver: Patrick personally on the phone vs offshore caller

### Confirmed Leads (also live in GHL)
- Gelato Constantino | +1 281-798-8504 | INTERESTED
- Kindred Stories    | +1 713-396-2396 | WANTS-INFO
- Flavors            | +1 281-819-2494 | WANTS-INFO
- Quad               | +1 713-857-1800 | INTERESTED-PASTDUE (bill block)
- The Fade Room      | +1 713-524-2336 | 5221 Almeda Rd, Houston TX 77004
                                       | EXISTING-ATT-UPGRADE (copper, 2 modems, internet sucks)
- 1 angry existing AT&T customer | ANGRY-EXISTING (cool-down recovery play)

### Tag Taxonomy (locked in for team)
- interested            - wants to buy
- wants-info            - needs follow-up call
- angry-existing        - cool down then recovery call
- interested-pastdue    - wants fiber but blocked by past-due bill
- existing-att-upgrade  - on old copper/U-verse, ripe for fiber upgrade
- not-interested        - auto from WAVV

Rule: keep total tags 4-6. Smart Lists filter by tag for daily queues.

### Patterns Discovered Today

1. PAST-DUE BLOCK
   Customers want fiber but past-due AT&T bills block them.
   Unknown: what credit/rollover/payment-plan authority Patrick has.
   Action: ask AT&T contact tomorrow.

2. EXISTING AT&T UPGRADE GOLDMINE
   Customers on old copper/U-verse with multiple modems = ripe upgrade.
   Way easier conversion than cold - already trust AT&T, already in billing system.
   Build pipeline: existing-att-upgrade smart list.

3. WANTS-INFO STALLERS LEAK WITHOUT TASK
   Tag alone is not enough. Must add GHL Task with due date.
   Tasks tab = daily callback queue.

### Strategic Plays Unlocked

PAST-DUE RESCUE PLAY
Rebuttal: "Heard you. Real quick - if AT&T could roll the past-due into
the new service or apply a credit at install, would that change things?"
Even if no authority yet, surfaces who would say yes if it were possible.

EXISTING-ATT-UPGRADE PLAY
"Sounds like y'all are on our older copper service with the 2 modems -
that's why it's been slow. Good news, fiber's lit. Same company, way
better service, usually same price or less. One fiber gateway replaces
both modems, way faster, no contract."

BARBERSHOP / SMALL-BIZ ANGLE
- Square/Toast POS runs on internet (outage = no payments)
- Streaming music for shop = bandwidth
- Booking app + customer wifi as perk
- 6-day/week operation = reliability > price
Lead with operational pain not speed specs.

### Pitch Iteration

OLD OPENER (buried lead, scam-flavored, escape hatch close):
  "Hey this is Pat with AT&T. We're running new fiber lines through
  there next kinda like week or so. Or - I'm sorry I say that. I actually
  say hey my name is Pat we just got through running new fiber internet
  lines there last like kinda couple of weeks. It's finally available.
  If you guys will let us we can connect it for free and give you a
  couple of months to use it for free. ... Is am I talking to the right
  person?"

NEW OPENER (test next 10 calls):
  "Hey - fiber just went live at your address. This is Pat with AT&T.
  Free install, 30-day money-back, no contract. Quick yes or no - are
  you the one who handles the internet bill there?"

Why new beats old:
- Lead in 5 words ("fiber just went live") not buried in 2nd sentence
- "30-day money-back" replaces "couple months free" (sounds legit not scam)
- "Yes or no - are you the one who handles the internet bill" replaces
  "right person?" - same intent, qualifies decision-maker, surfaces
  billing pain in one move

### Operational Wins

- GHL Tasks added for every wants-info / pastdue / angry lead
- Smart Lists planned: interested, wants-info, existing-att-upgrade
- Notes tab in use for context-specific intel
- Google Places used to verify Fade Room address (5221 Almeda) - improves
  pitch quality and feeds validation_man.py
- BRAIN stays strategic; individual leads stay in GHL (don't push every
  lead one-at-a-time - clogs repo)

### TODO TOMORROW

1. Test NEW OPENER on first 10 calls. Track interested rate vs old opener.
2. Ask AT&T contact: what payment-plan / credit authority do I have for
   past-due customers? Even partial rescue authority opens new pipeline.
3. Build GHL Smart List: tag = existing-att-upgrade. This is the
   highest-conversion segment.
4. Run validation_man.py on confirmed addresses to fiber-verify.
5. Add address 5221 Almeda Rd, Houston TX 77004 to The Fade Room contact
   in GHL (Edit Contact -> Address1).
6. Follow up: Quad (30 days for past-due cycle), Flavors + Kindred
   (2-3 days), angry-existing (3 days cool-down).

---

## WEIRD THINKING LOOPS - DO NOT REPEAT

### Loop A: OCR-the-streets to "extract addresses" (2026-04-30)
SYMPTOM: Claude proposed reading street names off screenshots via OCR
to approximate addresses near dots.
WHY WRONG: That problem is already solved by the existing pipeline.
The pipeline does pixel -> lat/lng -> reverse geocode. No OCR needed.
Reading streets off the image was a workaround for a problem that
didn't exist - and a worse workaround than the actual code.

CORRECT PIPELINE (always default to this for "screenshot -> address"):
  1. Filename       -> ZIP or zone name
  2. ZIP            -> centroid lat/lng (pgeocode, offline)
  3. Tile anchor    -> top-left lat/lng using R/T/row/col + pixel math
  4. Each dot pixel -> exact dot lat/lng (already-built shot_pixel_to_gps)
  5. Reverse geocode lat/lng -> real street address (Nominatim)

RULE: When asked anything about "screenshot to address", first verify
the existing pipeline is the answer. Only propose OCR / visual reading
as QA / sanity-check, never as the primary path.

### Loop B: Treating "no dots" as failure (2026-04-30)
SYMPTOM: Claude classified empty maps as garbage / unusable.
WHY WRONG: No-dots is a different lead bucket, not a failure.
  - Empty map today = baseline for change detection (dots next scan = newly lit fiber)
  - Empty map = AT&T Internet Air pitch territory (5G fixed wireless)
  - Empty map = scan history record (proof we covered the area)
RULE: No-dots is data. Three lead buckets, not one:
  green/gold dots = fiber pitch
  no dots         = Internet Air pitch
  newly lit dots  = "fiber just went live" pitch (highest urgency)

### Loop C: Solving a problem we already solved
GENERAL RULE: Before proposing a new approach, check the existing
codebase / past chat for the working solution. If it exists and works,
use it. If it exists and is broken, fix the bug - don't rebuild.

---

## DOTS-TO-SHEET WORKFLOW (locked in 2026-04-30)

Output: Active Sheet 12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag

### Tab: Pic Salvage
One row per screenshot ever taken. Refreshed nightly.
Columns: filename, folder, size_bytes, category, dot_count_est,
zone_id, row, col, R, T, lat_top..lng_right, last_classified
Categories: HAS_DOTS / EMPTY_MAP / API_ERROR / DIALOG_BLOCKED /
DESKTOP / UNKNOWN

### Tab: Fiber Addresses
One row per fiber dot detected. Deduped by address.
Columns: address, biz, color (green/gold), lat, lng, zip,
source_pic, scan_date, last_seen
green = cold pitch (fiber eligible non-customer)
gold  = upgrade pitch (existing AT&T copper customer) - PRIORITY
        these convert easiest

### Pipeline (nightly run on laptop)
  1. fiber_scan / fiber_hunter generate pics (with the v5.1+ patches)
  2. salvage.py runs:
     - Phase 1: classify all pics -> Pic Salvage tab
     - Phase 2: for HAS_DOTS pics, extract dots, geocode, dedupe
                -> Fiber Addresses tab
  3. Map Man scrapes biz from Google Maps -> Ready To Call tab
  4. Daily dial sheet = JOIN Fiber Addresses + Ready To Call by address

### NOT doing
- New CSV files daily (sheet refresh only)
- Local-only logs (everything goes to the sheet)
- OCR-based street reading (see Loop A)

---

## fiber_hunter LOOKUP BUG (2026-04-30)

SYMPTOM: v5.0 rejected "77036" and "houston" with "Not found. Try again."

FIX: drop-in geo_lookup.py module on Desktop, edit fiber_hunter.py to
import lookup() from it. Three-layer resolver:
  1. Hardcoded TX cities + outage ZIPs (instant)
  2. pgeocode (offline, all US ZIPs)
  3. Nominatim (online fallback)

---

## CITY / ZIP / GEOCODING - SINGLE SOURCE OF TRUTH

Lives in: fiber_scan.py
Functions: lookup_zip(zip5), lookup_city(name), PRESET_CITIES dict

### Coverage already in PRESET_CITIES
TX cities (Houston metro + statewide):
  Houston, Dallas, Austin, San Antonio, Fort Worth, Sugar Land,
  Pearland, Katy, Spring, The Woodlands, Cypress, Tomball, Conroe,
  Pasadena, Humble, Sugarland, Helotes, Midlothian
Other AT&T footprint states:
  OK: Oklahoma City, Tulsa, Edmond
  GA: Atlanta
  TN: Nashville, Memphis
  NC: Charlotte
  AL: Birmingham
  LA: New Orleans, Baton Rouge
  FL: Miami, Orlando, Tampa, Jacksonville
  IL: Chicago
  IN: Indianapolis
  MO: Kansas City
  CA: Los Angeles, San Diego

### lookup_zip(zip5) handles ANY US 5-digit ZIP
Uses persistent cache in geo_cache.json. Census/Nominatim under the hood.

### THE RULE - applies to every program

ALL programs use fiber_scan as the source. No exceptions:
  fiber_scan       - owns the dict (master)
  fiber_hunter     - imports from fiber_scan
  map_man          - imports from fiber_scan
  validation_man   - imports from fiber_scan
  addressman       - imports from fiber_scan
  salvage.py       - imports from fiber_scan
  any new program  - imports from fiber_scan

Standard import line for every program:
  from fiber_scan import lookup_zip, lookup_city, PRESET_CITIES

### DO NOT (this list exists because Claude has done all of these)

- Do NOT add pgeocode as a new dependency
- Do NOT create new geo_lookup.py modules
- Do NOT hardcode ZIP coordinates in any program except fiber_scan
- Do NOT propose Nominatim retry logic before checking PRESET_CITIES
- Do NOT suggest downloading ZIP databases - we already have the lookup
- Do NOT write OCR-of-streets workarounds when a ZIP+pixel-math
  geocode will give exact addresses (see Loop A above)

### LOOKUP PRECEDENCE (always this order, every program)

  1. PRESET_CITIES dict (instant, offline)
  2. lookup_zip if input is 5 digits
  3. lookup_city for everything else (cached + Nominatim)
  4. If all return None: print "Not found", do not retry online

### IF a city or ZIP is missing

Add it ONCE to fiber_scan.py PRESET_CITIES, push fiber_scan to GitHub,
all programs auto-use it on next auto-update.

---

## fiber_hunter v5.0 LOOKUP BUG - FIX

SYMPTOM: rejects valid input ("77036", "houston") with "Not found. Try again."
CAUSE: when fiber_hunter was forked from fiber_scan, PRESET_CITIES
was intentionally stripped to allow spiral-anywhere. But the lookup
chain went with it. fiber_hunter has no resolver.

FIX (one-time edit on laptop):

In fiber_hunter.py, near the top imports, ADD:

    from fiber_scan import lookup_zip, lookup_city, PRESET_CITIES

Find the function/loop that prints "Not found. Try again."
Replace its lookup body with:

    key = user_input.strip().lower()
    lat, lng, name = None, None, None
    if key in PRESET_CITIES:
        c = PRESET_CITIES[key]
        lat, lng, name = c["lat"], c["lng"], key
    elif user_input.isdigit() and len(user_input) == 5:
        lat, lng, name = lookup_zip(user_input)
    else:
        lat, lng, name = lookup_city(user_input)
    if lat is None:
        print("  Not found. Try again.")
        continue

Both files live on Desktop in the same folder, so the import resolves
automatically. fiber_scan is the source of truth, fiber_hunter just uses it.
