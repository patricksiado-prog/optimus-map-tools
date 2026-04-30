# OPTIMUS HOUSTON - PROJECT BRAIN

Last updated: 2026-04-30

This is the team's shared context. Update via brain.py from any device.
Stored in: github.com/patricksiado-prog/optimus-map-tools

---

## NORTH STAR

500 fiber sales per week from 20K+ AT&T fiber-eligible addresses.
Phase 2 goal: 1000/week. Phase 3 goal: 2000/week.
Mobile-first ops. Tools should work on phone.

---

## TEAM

Partners working together. Roles, not ranks.

- Patrick - sales, strategy, customer-facing, lead intel
- [Tech partner names go here]

---

## INFRASTRUCTURE

GitHub: github.com/patricksiado-prog/optimus-map-tools

Google Cloud:
- Project: fiberscanner-493900
- Service account: fiberscanner@fiberscanner-493900.iam.gserviceaccount.com

GHL:
- Account: Optimus Houston
- Location ID: TXw28sw0Z2rl6tcCDhJY
- A2P 10DLC approved, Twilio active
- Daily SMS limit: 100

Sheets:
- Active Q2: 12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag
- Original: 15ymTkIGPWs6quB035l414ns5hkG9cQ5xr_W4ukd0OAA

Drive folders:
- Fiber Map Snap Shots: 1whewiysliFB4rs1TqZYZk5NA43Es08Ad

CRM contacts: 41,325 in GHL

---

## TAM ANALYSIS

Existing fiber territory (already built, not yet sold):
- 37.5M total locations passed Q1 2026
- 12.5M subscribed -> 25M UNSOLD
- Legacy AT&T penetration: 40% (60% unsold)
- Lumen-acquired (Feb 2026): 25% (75% unsold) - PRIORITY

Coming fiber 2026:
- 8M new locations (4M organic + 4M Lumen + 1M Gigapower)
- ~150K new locations per WEEK nationwide
- Texas estimated: ~30K new per week

Channel mix:
- 20-25% of fiber adds come from D2D/outside sales
- Texas D2D: ~1,000-1,200 per week

---

## COMPETITIVE MAP

Geographic reality:
- AT&T fiber and Verizon Fios DO NOT OVERLAP. Never compete head-to-head.

TEXAS:
- Spectrum (cable) - PRIMARY TARGET, outage-prone
- Xfinity/Comcast (cable) - secondary, harder pitch
- Google Fiber - Austin only
- Frontier Fiber - pockets

LUMEN STATES:
- Ziply Fiber (PNW)
- Comcast Xfinity (some metros)

Difficulty (easy -> hard):
1. CenturyLink/Frontier DSL - phased out
2. Optimum, Cox - bad reputation
3. Spectrum - OUR TARGET
4. Xfinity/Comcast - careful pitch
5. Google Fiber, Frontier Fiber - AVOID head-to-head

Pitch adjustments:
- SPECTRUM: outages + neighbor proof + free trial parallel
- XFINITY: no data cap + bundle + price stability (NOT speed)
- DSL: "your service is being retired" + 10x speed

---

## TOOLS BUILT

- fiber_hunter.py v5.7 - news-driven scanner, RES/COMM tagging
- themapman.py v9.4 - Playwright biz scraper
- validatorman.py - AT&T API fiber validator
- addressman.py - find addresses around a map dot
- drive_helper.py - Drive upload/download
- sheet_cleaner.py - trim wasted cells (Pydroid)
- brain.py v2 - GitHub-backed updater

---

## BUILD QUEUE

1. battle_card.py - Type address, get back: fiber status, nearby AT&T customers, Spectrum outages, speed/pricing. SMS-ready.

2. outage_hunter.py - Scrape DownDetector, istheservicedown.com for live cable outages. Cross-ref with Green Commercial + All Biz Phones. Output STRIKE NOW / 24H / PATTERN tabs.

3. fiber_hunter Playwright conversion - 4-8 parallel headless instances. Houston metro overnight.

4. live_validator.py - Mobile call-center tool. Address -> fiber status in 2 sec.

5. Bulk validator - validate fiber for all 41K GHL contacts.

6. Map Man auto-overflow patch - auto-create overflow tab when 50K rows hit.

---

## STRATEGIES

1. CABLE OUTAGE STRIKING - LIVE (0-4hr) text blast, AFTERMATH (4-48hr) calls, PATTERN (2+ in 30 days) commercial
2. TEXT-ON-REQUEST BATTLE CARD - "want me to text you details?" -> auto SMS with neighbors+outages+pricing
3. GREY DOT SOCIAL PROOF - "your neighbor has had AT&T fiber 2 years"
4. PARALLEL CITY SCRAPING - 4-8 scanners before AT&T patches scanner
5. MOBILE FIELD VALIDATION - door-knockers validate in 2 sec

---

## RESEARCH POINTS

AT&T fiber:
- 40M passings target end 2026 (8M new in 2026)
- Lumen Feb 2026 - OR/WA/ID/UT/CO/NE/IA
- Gigapower JV - Las Vegas, Phoenix, Albuquerque, MN, PA
- FCC copper retirement 30%+ wire centers by 2026

Hot Texas markets:
- 77024 Houston Memorial - mature, premium
- 77019 Houston River Oaks - dense
- 77382 The Woodlands - mature + active builds
- 77479 Sugar Land - commercial heavy
- 78258 Stone Oak SA - high-income
- 78023 Helotes - fresh build, low competition
- 75093 Plano West - DFW core dense biz
- 76065 Midlothian - recently lit
- 79932 West El Paso - BEAD virgin builds

Cable outages 2026-04-30:
- Houston/Spring 77388 - Spectrum drop confirmed
- Cypress - biweekly outage history
- Austin Wells Branch - recent fiber-line attack
- San Antonio/Corpus/RGV - recent mass Spectrum outage

---

## SMS SCRIPTS

Cold open:
"Hi u wanna hear who's got it and loves it? Spectrum was out 13x this year, AT&T 0. What's up wanna give me a maybe on a free trial run parallel?"

Live outage strike:
"[Name] - Patrick @ AT&T. Saw Spectrum just dropped in [ZIP]. AT&T fiber is live at your address. Want a same-day install quote? Reply Y."

Live outage commercial:
"[BizName] - saw your area's Spectrum is down. How much per hour are you losing? AT&T fiber is lit at [address]. Reply Y for emergency install."

Aftermath:
"[Name] - your area got hit again yesterday. AT&T fiber is live at you. 5 min call?"

Pattern (commercial):
"[BizName] - your ZIP has had 4 Spectrum outages this month. AT&T fiber has 99.9% uptime SLA."

Battle card text-on-request:
"[Address] - fiber confirmed lit. Your block: [neighbors]. Spectrum [ZIP]: [N] outages YTD. AT&T: 0. Available: 1Gig $80/mo, free install today, 30-day trial run parallel. Reply YES."

---

## CONSTRAINTS

- Google Sheets hard limit: 10M cells per workbook
- Service accounts have ZERO Drive storage quota
- pyautogui scripts cannot run on Android - laptop only
- gspread/google-auth/data scripts work on Android via Pydroid
- AT&T scanner may get patched - scrape aggressively
- Daily SMS limit 100 (request increase from GHL)

---

## IDEAS

[Add via brain.py menu option 2]

---

## NOTES

[Add via brain.py menu option 3]

---

## DONE

[Items move here when marked complete]
