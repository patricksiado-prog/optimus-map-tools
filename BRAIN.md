# Optimus BRAIN

_Last updated: 2026-06-29 (Claude session: ATT FIBER LEADS audit + program code review — see Discovery Log at bottom)_

## Active systems
- GitHub repo: patricksiado-prog/optimus-map-tools
- Active sheet: 12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag
- GHL Houston Location: TXw28sw0Z2rl6tcCDhJY (~41,325 contacts)
- Service account: fiberscanner@fiberscanner-493900.iam.gserviceaccount.com
- Map Man v10
- Drive mirror: 1u38EOzaGO7Sd5Y8ERqQoXeYZW5Pws8Z_

## Phase targets
- Phase 1: 500 sales/week
- Phase 2: 1000/week
- Phase 3: 2000/week

## Run log
(append new entries below this line)

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

## DISCOVERY LOG — 2026-06-29 (Claude session: sheet audit + code review)

Worked on sheet **ATT FIBER LEADS** = `1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA`
(note: differs from the "Active sheet" id listed above — this is the live hunter/scraper output sheet, 2.3 MB).

### ⚠️ CRITICAL GOTCHA — Drive reads are TRUNCATED
- Google Drive `read_file_content` (natural-language) and the spreadsheet content-snippet
  **silently cap each tab at ~500 rows.** Counts taken from it are WRONG (undercounts).
- Early in this session that cap made me report "20 unique businesses / ~20 callable" — the
  REAL numbers are ~80x bigger. Do not trust the text read for counts.
- `download_file_content` as **xlsx and csv FAILED** ("session expired") on this large file.
  **ODS worked**: export `application/vnd.oasis.opendocument.spreadsheet`, base64-decode,
  unzip `content.xml`, parse `table:table` rows (handle `number-columns/rows-repeated`).
  (pandas/odfpy not installable in sandbox — parse XML manually.)

### REAL tab structure + row counts (full ODS export)
| Tab | Rows | Notes |
|---|---|---|
| Precise Fiber | 180,190 GREEN | hunter output. 175,635 unique addresses (~115,122 distinct buildings; rest are apt units) |
| Fiber Green Biz | 14,691 | hunter green-addr → nearest-business join. **1,667 unique phones**, 1,760 businesses |
| Maps Businesses | 14,939 | scraper raw. **13,181 unique phones**, 14,387 businesses |
| Enriched Leads | 1,073 | geocode resolver (osm/cache/gmaps), all GREEN/WORKING |
| Hunter Status | 12,394 | scan run log |
| Upgrade Orange Biz | 1 | empty/unused |
| Sheet6 | 0 | empty |

### CALLABLE LEADS (green fiber dot + a business AT that address)
- **Strict (business address == green-fiber address): 1,203 addresses / 1,200 phones.**
- Fiber Green Biz tab deduped by phone: 1,667 unique callable phones.
- These are the real commercial fiber leads to dial. (NOT 20 — that was the truncation bug.)

### PROGRAMS (shipped by installer, reviewed this session)
Installer `INSTALL_OPTIMUS.bat` (GitHub release, repo **Go-High-Level-MCP-2026-Complete**,
branch `claude/optimus-map-tools-setup-6dcl6o`) deploys two tools:
- **precise_fiber_hunter.py** (2,889 lines) → `%USERPROFILE%\optimus_hunter\` (precise hunter)
- **maps_scraper_standalone.py** (650 lines) → `%USERPROFILE%\maps_scraper\` (maps scraper)
- Only Drive dependency: pulls **google_creds.json** (Drive id `1upYH4h2VsmOwO82v9CVjMpE6IzV-5dIs`)
  into both tool folders. ⚠️ service-account key is distributed via shareable Drive link = key-leak risk.

### BUGS FOUND
**maps_scraper_standalone.py**
- **Phone bug (line 30):** `_PHONE_RE = re.compile(r"\+?\d[\d\-\.\s\(\)]{8,}\d")` can't start on `(`,
  so EVERY phone drops its leading paren → `346) 401-1250`. **Fix:** `r"[\+\(]?\d[\d\-\.\s\(\)]{8,}\d"`.
- `self_update()` runs `git reset --hard origin/<branch>` + re-exec on every launch = RCE / wipes local edits.
- ZIP filter is a substring test (`zip in addr`) + no ZIP validation → wrong rows kept/dropped.
- CSV dedup key (raw `name|address`) vs sheet key (`.upper()`) mismatch → dup rows.

**precise_fiber_hunter.py**
- Dedup is **exact-string, in-memory only** (loaded once at start). Address-string drift between
  passes (pin vs street, ZIP/no-ZIP, UNIT vs STE) re-adds the same place hours later = the dup rows.
- `flush()` pops from `self.pending` BEFORE the sheet write succeeds → a 429/network error
  **permanently loses those captures** (only survive in JSONL). High-priority data-loss fix.
- "UNIT DUMMY / CTR / COIN" junk = AT&T feed values passed through with NO validation. Add an
  address sanity filter before write.
- Apartment explosion (200+ rows for one complex) = REAL AT&T data (1 feature per unit), no roll-up.
  For a call list, add building roll-up or per-building cap.
- Same `self_update()` `git reset --hard` hazard; hardcoded prod `SHEET_ID` (line 111).

### TODO / OFFERED (not yet done)
- Build a clean "Callable Leads" tab (~1,200 strict matches: Address·Business·Phone·Category·Website),
  phones corrected + deduped.
- Patch the scraper phone regex (1-line) and add dedup-on-write to both tools.

---

## HOW TO COUNT FIBER LEADS (canonical method) — ATT FIBER LEADS sheet

Sheet `1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA`. The lead count comes from
**2 source tabs that the 2 programs write SEPARATELY**, plus their overlap:

| Tab | Written by | What a row is |
|---|---|---|
| **Precise Fiber** | precise_fiber_hunter.py | one AT&T green fiber dot (address) |
| **Maps Businesses** | maps_scraper_standalone.py | one scraped business (by ZIP) |
| Fiber Green Biz | derived join | **DO NOT trust its row count** (see below) |

### Step 0 — get FULL data (never trust the truncated read)
Drive text-read caps each tab at ~500 rows. Export the whole workbook as **ODS**
(`download_file_content` mime `application/vnd.oasis.opendocument.spreadsheet`),
base64-decode, unzip `content.xml`, parse `table:table` rows. (xlsx/csv export errors;
pandas/odfpy don't install — parse XML by hand.)

### Step 1 — normalize before counting
- **Phone:** strip to digits; drop leading `1` if 11 digits; valid = exactly 10 digits.
- **Address "core":** UPPERCASE, take text before first comma, then drop everything from
  ` UNIT / APT / STE / SUITE / # / BLDG / FL ` onward. (Collapses apartment units + suites
  to the building so a business at "24 GREENWAY PLZ STE 1800" matches dot "24 GREENWAY PLZ UNIT COIN".)

### Step 2 — the three counts
1. **Green dots (Precise Fiber):** rows where Dot Color == GREEN. Unique by full address =
   the address list; unique by *core* address = distinct buildings (apartments inflate raw rows).
2. **Businesses (Maps Businesses):** unique by normalized phone.
3. **FIBER LEADS = the overlap** = businesses whose OWN core address is in the green-dot set.
   This is the real callable list. (Match business core-address ∈ {green core-addresses}.)

### Step 3 — sanity rules
- **Maps Businesses is NOT a fiber list** — only ~20% of its businesses sit on a green dot.
- **Fiber Green Biz tab ≠ the overlap.** It is bloated (one business stamped across every
  apartment unit → ~8 rows each) AND incomplete (missing ~1,000 real on-dot businesses).
  Recompute the overlap from the 2 source tabs; don't read it off this tab.
- "Callable" = overlap business has a valid 10-digit phone. Filter to Houston via the
  business address city/ZIP if a Houston-only list is needed.

### Canonical numbers as of 2026-06-29 (full ODS export)
- Green dots: **180,190** GREEN rows → ~175,635 unique addresses → ~115,000 buildings.
- Businesses: **13,181** unique phones (14,939 rows).
- **FIBER LEADS (overlap, biz on a green dot): ~2,686** (~2,576 Houston).
- Fiber Green Biz tab: 14,691 rows = only 1,667 unique businesses (1,549 verified on-dot, 118 near-match noise).
- Loaded into GHL autodialer: **122** (tag `green-houston`/`fiber-green`/`optimus-fiber-biz`,
  source "Optimus Fiber Biz") = ~5% of the 2,686. Last load 2026-06-19; not refreshed since.

### GHL location ID correction
Real autodialer location = **`TXw28sw0Z2rI6tcCDhJY`** (capital `I`). The id written elsewhere
in this brain as `TXw28sw0Z2rl6tcCDhJY` (lowercase `l`) is WRONG and 403s.
Note: same location also holds an unrelated ~320 "romeo"-tagged Florida insurance set — keep dialer on the `green-houston` tag.

---

## BUILDING-FED / EXCLUDE ADDRESSES (do NOT load or call)

These are multi-tenant high-rises / office towers where **internet comes from the building**
(shared building service), NOT an individually sellable standalone fiber drop. The green dot is
the building, not the tenant. A tenant in a suite there cannot buy AT&T Fiber for their unit, so
every "business at this address" is a dead lead. **Skip these when counting/loading; delete if loaded.**

Rule of thumb (already in the canonical method): any address with a suite/Ste/#/Floor token at a
high green-dot-density building is building-fed — exclude it. Standalone single-tenant addresses
(no suite, low dot density) are the only sellable fiber-green leads.

| Address | City/ZIP | Notes | Action taken |
|---|---|---|---|
| 4265 San Felipe St (all suites: #780/#800/#970/#1100…) | Houston, TX 77027 | Multi-tenant office tower, internet from building | **11 contacts deleted from Optimus dialer 2026-06-30** |

(Append new building-fed towers here as they're found so they never get re-loaded.)

---

## DIALER EXCLUSION RULE — "can't-sell" leads stay OUT of the dialer (2026-07-03)

**Standing rule:** before enrolling ANY lead into a power dialer (Optimus workflow
`41e00387-a766-4975-bbcd-627c684a3ee1` or Frontline `ac28196d-a9fc-4e26-8247-d148681c0b7b`),
FILTER OUT everything below. These do not sell and/or cannot be reached — keep them out.

**Persistent exclusion phone list:** `dialer_exclusions.json` (repo root, 487 phones as of
2026-07-03). Subtract these from every load. Contacts already scrubbed carry GHL tags
`excluded-unsellable`, `excluded-clinic`, or `excluded-vertical` (unenrolled, not deleted).

### Never load / always pull (the "can't sell" set)
1. **Invalid / unreachable** — any contact tagged `invalid` (SMS failed, Twilio 30003/30005/30006 =
   landline/dead number). ~205 in Optimus. Enumerate via `search_contacts` query="invalid".
2. **Building-fed towers** — suite-numbered addresses at multi-tenant high-rises (internet from the
   building). Known: 24 Greenway Plz/Plaza, 4200 Westheimer, 1201 San Jacinto, 4265 San Felipe,
   any `San Felipe St #`. Same logic as the BUILDING-FED section above.
3. **Medical / clinics** — orthodontist, physical therapy, chiropractor, counseling, therapist,
   optometrist, acupuncture, med spa, podiatrist, nutritionist, dermatologist, dental, veterinary,
   urgent care, hospital, pharmacy. (Category tags are unreliable — also match on the NAME.)
4. **Professional offices w/ gatekeepers** — law firms / attorneys / `PC` / `PLLC` / `LLP`,
   CPA / accountant. (Per Patrick, real-estate agents / bookkeepers / insurance are KEPT.)
5. **National chains** — Pep Boys, AutoZone, O'Reilly, U-Haul, CubeSmart, Public Storage, Kroger,
   H&R Block, Jackson Hewitt, Sherwin-Williams, Johnstone Supply, Transtar, Regus/WeWork, banks
   (PNC/Chase/BofA/etc.), fast food, gas stations, gym franchises, etc.
6. **Government / institutional** — police/fire/sheriff, city of / county / state / federal,
   schools / ISD / university, post office, library, funeral/cremation, etc.
7. **Non-businesses** — public parks, etc.

### How to filter (canonical)
- Skip any phone in `dialer_exclusions.json`.
- Skip any GHL contact tagged `invalid` / `excluded-unsellable` / `excluded-clinic` / `excluded-vertical`.
- Skip by NAME keyword (chains/gov/clinic/law) AND by suite-at-tower ADDRESS — do NOT trust the
  scraper's Category column alone (it mislabels: a park as "pool cleaning", a law firm as "bookkeeper",
  a vet clinic as "dog grooming").
- Prefer standalone (single-tenant, no suite) owner-operated small biz — "the boss picks up".

### Cleanup done 2026-07-02/03 (Optimus dialer)
Pulled from the dialer (unenrolled + tagged, not deleted): 152 clinics, ~311 tower/office/junk,
~200 invalid/unreachable, 18 chains/government. 11 building-fed (4265 San Felipe) hard-deleted.
Watch for FALSE POSITIVES on name keywords (e.g. "Chase Carpentry" = a carpenter, "…Lending Library"
= a salon, "Federal American Grill" = a restaurant) — confirm before cutting.
