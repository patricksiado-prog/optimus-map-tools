# OPTIMUS HOUSTON - SESSION SUMMARY

Date: 2026-04-30 (overnight session)
For: Patrick + tech partners + future Claude context

---

## NORTH STAR

500 fiber sales/week from 20K+ AT&T fiber-eligible addresses.
Phase 2: 1000/week. Phase 3: 2000/week.
Mobile-first ops.

---

## STRATEGIC FRAMEWORKS

### Sales Channel Reality
- AT&T fiber and Verizon Fios DO NOT OVERLAP geographically
- Real Texas competitors: Spectrum (primary), Xfinity (secondary), Google Fiber (Austin only)
- Real Lumen-state competitors: Ziply, Comcast in some metros

### Pitch By Competitor
- SPECTRUM: outage stats + neighbor proof + free trial parallel
- XFINITY: no data cap + bundle savings + price stability
- DSL (Lumen/CenturyLink/Frontier): "your service is being retired" + 10x speed

### Three Strike Strategies
1. CABLE OUTAGE STRIKE
   - LIVE STRIKE (0-4hr): text blast residential + biz
   - AFTERMATH STRIKE (4-48hr): phone calls
   - PATTERN STRIKE (2+ outages in 30 days): premium commercial

2. TEXT-ON-REQUEST BATTLE CARD
   - Agent on call: "want me to text you the details?"
   - Auto SMS with: nearby AT&T customers, Spectrum outages, pricing

3. GREY DOT SOCIAL PROOF
   - "Your neighbor at 1230 Main has had AT&T fiber for 2 years"

### Field Wisdom
- Old residential fiber lists = LOW conversion
- Google Maps filtered for CELL phones + texting = winning channel
- AT&T cell service $10-20 = strong bundle hook
- Lead with cell deal, fiber follows

### Dot Color Codes (Confirmed from real AT&T map)
- GREEN = Fiber eligible / non-customer (PRIME COLD-PITCH TARGET)
- ORANGE/RED = Fiber eligible / copper customer (FORCED UPGRADE - FCC retirement)
- GREY = Existing fiber customer (upgrade/referral target)

### TAM Reality
- 37.5M fiber locations passed Q1 2026, 12.5M subscribed = 25M UNSOLD
- Legacy AT&T penetration 40% (60% unsold)
- Lumen-acquired (Feb 2026) 25% (75% unsold = PRIORITY)
- 8M new fiber locations going live 2026
- D2D channel = 20-25% of fiber adds = our lane

---

## TOOLS BUILT

| Tool | Where | Purpose |
|---|---|---|
| brain.py v2 | Phone | Read/write BRAIN.md to GitHub |
| backup_drive.py | Phone | Pulls repo files, archives to Drive |
| process_drive_pics.py | Phone | Detect dots + Vision OCR |
| sheet_cleaner.py | Phone | Trim wasted sheet cells |
| dot_extractor.py | Laptop | Tesseract OCR + dot detection |
| rename_pics.py | Laptop | Bulk rename by content |
| geo_extractor.py | Laptop | FREE pipeline: Tesseract + Nominatim -> addresses |
| push_to_repo.py | Phone | Push any file to GitHub |
| push_brain_now.py | Phone | Push this summary directly |

### Infrastructure
- Phone Python toolkit: numpy, gspread, google-auth, google-api-python-client, requests, phonenumbers, beautifulsoup4, pillow, google-cloud-vision (all installed)
- google_creds.json on phone Downloads
- github_token.txt on phone Downloads
- Service account: fiberscanner@fiberscanner-493900.iam.gserviceaccount.com
- Active sheet: 12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag
- 244 hot leads queued in GHL workflow
- 326+ map pics in Drive folder "Fiber Map Snap Shots"

### Dot Detection - PROVEN WORKING
- Tested on 4 real fiber map tiles
- Calibrated colors: GREEN=RGB(65,166,0), GREY=RGB(137,137,137), ORANGE=RGB(255,0,0)
- Saturation-based detection (not exact RGB match)
- Filtered by aspect ratio
- Tile r2_c3_refine_6 = 47 GREEN + 5 ORANGE + 97 GREY = 149 records

---

## BUILD QUEUE

1. Coordinate data source clarified (where lat/lon stored per tile)
2. battle_card.py - SMS-ready address lookup
3. outage_hunter.py - DownDetector scrape + cross-ref + STRIKE tabs
4. Master DB with change detection - track GREY/ORANGE/GREEN transitions
5. Zoom-aware confidence scoring
6. Multi-pass scanner (broad first, drill-down)
7. 10 parallel scanners (cloud or API reverse-engineer)
8. fiber_hunter Playwright conversion
9. live_validator.py - 2-sec mobile call-center lookup
10. Bulk validator for all 41K GHL contacts

---

## KEY DISCOVERIES

### Sheet Cell Waste (~7M cells freeable)
- HOT ZONES: 100K rows, 88 with data
- Gold Clusters: 100K rows, 3 with data
- GOLD ALERTS: 100K rows, 98 with data
- Green Residential: 50K rows, 7,914 with data

### Dot Detection Math
- One high-zoom tile = 50-150 dots
- 326 pics x ~50-150 dots = 15K-50K real addresses in scan history
- Scanner's "count=N" labels are unreliable

### Service Account Limits
- Service accounts have ZERO Drive storage quota
- Can READ/UPDATE existing files but NOT CREATE new ones
- Workaround: GitHub for files (this is why BRAIN.md lives there)

---

## CONSTRAINTS

- Google Sheets: 10M cells/workbook hard limit
- pyautogui: laptop only (no Android)
- Tesseract: laptop only (no Android)
- gspread/data scripts: phone OK
- AT&T scanner may get patched
- GHL: 100 SMS/day limit
- Nominatim: 1 req/sec free

---

## SMS SCRIPTS

### Cold open
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

---

## TEAM WORKING AGREEMENT

Patrick: sales side - calling, texting, customer-facing.
Tech partners: run scripts, update scanner, set up cloud infra, maintain Pydroid setups, push code to repo.
**Claude does ALL the coding. Nobody on team is expected to write code.**
When something breaks or a new feature is needed: describe it, screenshot the error, Claude rewrites/fixes.

---

## TIER S TEXAS TARGETS

- 77024 Houston Memorial - mature, premium
- 77019 Houston River Oaks - dense
- 77382 The Woodlands - mature + active builds
- 77479 Sugar Land - commercial heavy
- 78258 Stone Oak SA - high-income
- 78023 Helotes - fresh build, low competition
- 75093 Plano West - DFW core dense biz
- 76065 Midlothian - recently lit
- 79932 West El Paso - BEAD virgin builds

## Cable Outage Activity 2026-04-30
- Houston/Spring 77388 - Spectrum drop confirmed
- Cypress - biweekly outage history
- Austin Wells Branch - recent fiber-line attack
- San Antonio/Corpus/RGV - recent mass Spectrum outage

---

## RESUME NEXT SESSION

Tell Claude: "pull BRAIN" or "read BRAIN from github.com/patricksiado-prog/optimus-map-tools"
Claude reads, syncs, picks up at BUILD QUEUE.

### Open questions
- Where exactly is coordinate metadata in scanner output?
- 10-scanner architecture decision (cloud vs API)
- Tech partner names + roles for BRAIN

End of summary.
