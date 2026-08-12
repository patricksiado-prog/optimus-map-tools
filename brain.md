# OPTIMUS HOUSTON - PROJECT BRAIN

Last updated: 2026-08-12

Team's shared context. Stored in github.com/patricksiado-prog/optimus-map-tools

---

## UPDATE 2026-08-12 (Claude session review)

### Field programs (the two desktop apps) — verified purpose + output
- **Optimus Fiber Hunter** (`fiber_hunter.py`) — scans a seed ZIP on the AT&T map, drops a colored dot per address. GREEN = fiber lit/available. Writes: `Address | Dot Color | Captured At`.
- **Optimus Maps Scraper** (`themapman.py`) — Playwright scrapes Google Maps businesses by category in the area (commercial leads). Writes: `Business Name | Phone | Address | Website | Category`.
- Both write to sheet **ATT FIBER LEADS** = `1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA` (NOT the old master `12PIIpl…`). This is the actively-written sheet.

### Current sheet counts
- Fiber Hunter: **310 GREEN matches** (fiber-available addresses), captured 2026-06-16/17 (Houston scan).
- Maps Scraper: **~283 businesses** (landscaping, electricians, contractors, salons, roofing, etc.).
- Control tab shows scanner re-seeded to **ZIP 37211 Nashville TN on Aug 5** — so sheet still shows the older Houston scan; newer Nashville results may not have written back yet. NEEDS a fresh re-pull to confirm live count.

### GHL / account discrepancy — RESOLVE
- Brain lists GHL Location **TXw28sw0Z2rl6tcCDhJY** ("Optimus Houston", 41,325 contacts).
- All live outreach this session ran in a DIFFERENT sub-account: **xZj500PjsflIQg2j9f9D** (4,860 contacts, "AT&T Leads" pipeline, sending number +13466840331, source "Optimus Fiber Biz"/"T-OPTIMUS").
- OPEN QUESTION: is xZj500 the current op, or a stray/child account? Confirm before scaling.

### Live SMS campaign state
- Running a GENERIC blast: "New fiber at your address, 10x faster, $30/mo, 2 free months, reply YES." Paced 30/shift x2/day (~60/day).
- AT&T Leads pipeline: 100 open opps, ALL stuck in "Contacted" stage (no hot/cold separation).
- AI responder replies as an AT&T rep, asks for address + # of lines, auto-creates opportunities.
- **STRATEGY DRIFT:** none of the brain's outage-strike / battle-card / neighbor-proof scripts are in use. Generic blast likely drives the high opt-out.

### Reply scan (149 inbound, Jul 31–Aug 11, 54 unique repliers)
- **~52% opt-out (STOP)** — carrier spam-flag risk. Lower volume + tighten to residential.
- 8 auto-responders (business missed-call bots — noise), 3 not-interested, ~7 junk.
- Only **6 genuine warm humans** (hot list). Best: (804) 475-6410 replied YES "1 internet only"; Kevin Manuel (281) 414-3408 hot-lead but texted STOP → CALL ONLY.

### Scraper → dialer gap
- Scraper businesses in the sheet are largely NOT loaded into the GHL dialer (only a handful confirmed present in a 500-contact sample). Scraper is running ahead of the dialer — need an import/dedupe path.

### Next actions (proposed, awaiting Patrick)
1. Confirm which GHL account is the real op (41K vs 4,860).
2. Re-pull live sheet for current Nashville green count.
3. Swap generic SMS → battle-card/outage scripts to cut opt-out rate.
4. Add auto-tag + hot-lead pipeline stage so the call list builds itself.
5. Cross-match 310 green addresses × 283 scraped businesses → commercial fiber leads.

---

## NORTH STAR

500 fiber sales per week from 20K+ AT&T fiber-eligible addresses.
Phase 2 goal: 1000/week. Phase 3 goal: 2000/week.
Mobile-first ops.

---

## TEAM

Partners working together. Roles, not ranks.
- Patrick - sales, strategy, customer-facing
- [Tech partner names here]

---

## INFRASTRUCTURE

GitHub: github.com/patricksiado-prog/optimus-map-tools
GCP: project fiberscanner-493900, service account fiberscanner@fiberscanner-493900.iam.gserviceaccount.com
GHL: Optimus Houston, Location ID TXw28sw0Z2rl6tcCDhJY
Sheets: 12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag
CRM: 41,325 contacts in GHL

---

## TAM

- 37.5M fiber locations passed Q1 2026, 12.5M subscribed = 25M unsold
- Legacy AT&T penetration 40%, Lumen-acquired 25% (75% unsold = priority)
- 8M new locations in 2026 (~150K/week nationwide, ~30K/week Texas)
- 20-25% of fiber adds via D2D channel = our lane
- Texas D2D estimated 1,000-1,200 sales/week available

---

## COMPETITIVE MAP

AT&T fiber and Verizon Fios DO NOT OVERLAP - never compete head-to-head.

Texas competitors:
- Spectrum (cable) - PRIMARY TARGET, outage-prone
- Xfinity/Comcast - secondary, harder pitch
- Google Fiber - Austin only

Difficulty easy to hard:
1. CenturyLink/Frontier DSL - phased out
2. Optimum, Cox - bad reputation  
3. Spectrum - OUR TARGET
4. Xfinity/Comcast - careful pitch needed
5. Google Fiber, Frontier Fiber - AVOID

Pitch by competitor:
- SPECTRUM: outages + neighbor proof + free trial parallel
- XFINITY: no data cap + bundle + price stability (NOT speed)
- DSL: "your service is being retired" + 10x speed

---

## TOOLS BUILT

- fiber_hunter.py v5.7 - PRIMARY scanner
- themapman.py v9.4 - Playwright biz scraper
- validatorman.py - AT&T fiber API validator
- addressman.py - addresses around a dot
- drive_helper.py - Drive upload/download
- sheet_cleaner.py - trim wasted cells (Pydroid)

---

## BUILD QUEUE

1. battle_card.py - address -> fiber status + nearby AT&T customers + Spectrum outages + speeds + pricing. SMS-ready.
2. outage_hunter.py - DownDetector scrape + cross-ref green commercial -> STRIKE NOW/24H/PATTERN tabs
3. fiber_hunter Playwright conversion - 4-8 parallel headless
4. live_validator.py - call center mobile tool, 2 sec address check
5. Bulk validator for all 41K GHL contacts
6. Map Man auto-overflow patch (when 50K rows hit)

---

## STRATEGIES

1. CABLE OUTAGE STRIKING - LIVE (0-4hr) text blast, AFTERMATH (4-48hr) calls, PATTERN (2+ in 30 days) commercial
2. TEXT-ON-REQUEST BATTLE CARD - "want me to text details?" -> auto SMS
3. GREY DOT SOCIAL PROOF - "your neighbor has had AT&T 2 years"
4. PARALLEL CITY SCRAPING - 4-8 scanners before patch
5. MOBILE FIELD VALIDATION - 2-sec address check

---

## RESEARCH

AT&T fiber expansion:
- 40M passings target end 2026
- Lumen integration Feb 2026 (OR/WA/ID/UT/CO/NE/IA)
- Gigapower JV (Las Vegas, Phoenix, Albuquerque)
- FCC copper retirement 30%+ wire centers by 2026

Hot Texas markets:
- 77024 Memorial, 77019 River Oaks, 77382 Woodlands
- 77479 Sugar Land, 78258 Stone Oak, 78023 Helotes
- 75093 Plano West, 76065 Midlothian, 79932 West El Paso

Cable outages 2026-04-30:
- Houston/Spring 77388 - Spectrum drop tonight
- Cypress - biweekly outages
- Austin Wells Branch - fiber attack
- San Antonio/Corpus/RGV - mass Spectrum outage

---

## SMS SCRIPTS

Cold open:
"Hi u wanna hear who's got it and loves it? Spectrum was out 13x this year, AT&T 0. What's up wanna give me a maybe on a free trial run parallel?"

Live outage:
"[Name] - saw Spectrum just dropped in [ZIP]. AT&T fiber is live at your address. Same-day install? Reply Y."

Aftermath:
"Your area got hit again yesterday. AT&T fiber is live at you. 5 min call?"

Pattern commercial:
"Your ZIP has had 4 Spectrum outages this month. AT&T fiber 99.9% uptime SLA."

Battle card:
"[Address] - fiber confirmed lit. Your block: [neighbors]. Spectrum [ZIP]: [N] outages YTD. AT&T: 0. 1Gig $80/mo, free install today, 30-day trial run parallel. Reply YES."

---

## CONSTRAINTS

- Sheets 10M cell hard limit per workbook
- Service accounts have ZERO Drive storage quota
- pyautogui scripts laptop-only (not Android)
- AT&T scanner may get patched - scrape aggressively
- SMS daily limit 100 (request increase from GHL)

---

## IDEAS

[Edit on github.com to add]

---

## NOTES

[Edit on github.com to add]

---

## DONE

Drive backup of 326+ map pics (2026-04-30)
244 hot leads queued in GHL workflow (2026-04-30)
Pydroid 3 setup with gspread + google-auth (2026-04-30)
Sheet inventory ran successfully (2026-04-30)
