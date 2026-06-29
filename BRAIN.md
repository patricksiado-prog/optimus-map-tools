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
