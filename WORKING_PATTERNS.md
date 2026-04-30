# WORKING PATTERNS - what to never forget, what actually runs

Last updated: 2026-04-30
Read this BEFORE building anything new.

---

## THE PROBLEM (the forgetting trap)

Every time something breaks, the instinct is "rewrite everything."
This kills working code.

What happens:
  1. Build something. It works.
  2. Hit an edge case (Nominatim down, map covered, sheet headers wrong).
  3. Panic-rewrite from scratch instead of patching.
  4. New rewrite has fresh bugs.
  5. Old working build gets lost in version churn.
  6. End up rebuilding the SAME LOGIC 5-8 times across sessions.

Real examples from this operation:
  - fiber_scan rebuilt 7+ times. Same hot zone diffing, same color
    detection, same sheet writes - re-coded each time.
  - mapman --enrich-only flag existed for weeks. Multiple sessions
    spent "rewriting mapman to add addresses" when the flag was
    already there.
  - LeadConnector mobile app from GHL already does dialing+texting.
    Multiple discussions about "build an app for dialing" when it
    existed and was free.
  - validatorman --force flag existed. Multiple sessions tried to
    rebuild "force re-validation" when it was a one-line flag.

Rule going forward:
  - SEARCH past chats and BRAIN.md FIRST before building.
  - CHECK if a flag already exists.
  - PATCH, don't rewrite.
  - Verify GHL/existing tools before claiming "we need to build X."

---

## CRITICAL TRUTH: rows in sheet != revenue

Don't conflate three different things:
  1. Code ran without crashing
  2. Rows appeared in the sheet
  3. Rows produced sales

Past sessions celebrated "2,748 rows!" without proving any converted
to commission. That's celebrating output, not outcome.

Master DB with run_id tagging is the fix - know which build produced
which row, then trace which row produced which sale. Until that's
built, every "this build worked" claim is unproven.

---

## SCANNER MOTION - THE PROVEN PATTERN

These mechanics worked across multiple builds. Don't change without reason.

### Mouse drag pan
  - Move to MAP_CENTER (calibrated per laptop)
  - pyautogui.drag(-PAN_PIXELS, 0, duration=0.25, button="left")
  - PAN_PIXELS = 300 (full pan - default)
  - PAN_PIXELS = 150 (half pan - more overlap, 4x slower)
  - WAIT_AFTER_PAN = 1.5 to 2.5 seconds

### Click "Search this area"
  - Required after every pan (no keyboard shortcut)
  - Position calibrated ONCE per laptop
  - Saved to search_button_pos.json
  - First-run hover-to-calibrate flow

### Mouse parking (post-click)
  - After click, move cursor to bottom-right corner
  - Prevents accidental zoom on hover
  - Prevents popup triggers from dot tooltips

### Reactive wait_for_dots()
  - Don't use fixed sleep
  - Poll screen every 150ms
  - Trigger on first orange OR first green appearing
  - Max wait 5-6 seconds, then move on
  - Fast cells finish fast, slow cells get the time they need

### Background processor pattern
  - Scanner thread: pan, click, screenshot, queue.put()
  - Background thread: queue.get(), geocode, classify, sheet.write()
  - Scanner NEVER blocks on API calls
  - Battle-tested - this is what produced the 2,748-row run

### Multi-instance picker (1-4 simultaneous)
  - ZONE_ASSIGNMENTS[total][instance] = list_of_zones
  - Each instance picks zones from its assigned list
  - All write to same sheet (gspread handles concurrent appends)
  - Different filename prefixes (i1_, i2_, etc) so screenshots don't clash

---

## DOT DETECTION - CALIBRATED COLORS (proven on 4 real tiles)

Saturation-based, NOT exact RGB match.

### Color targets (production values)

GREEN (fiber eligible / non-customer - PRIME COLD-PITCH)
  Target RGB: (65, 166, 0)
  Detection: (g > 130) AND (g - r > 30) AND (g - b > 30)
  Range fallback: (30,130,30) to (100,210,80)

GREY (existing fiber customer - upgrade target)
  Target RGB: (137, 137, 137)
  Detection: (110 < r < 180) AND |r-g|<12 AND |g-b|<12 AND |r-b|<12

ORANGE/RED (fiber eligible / copper customer - FORCED upgrade FCC)
  Target RGB: (255, 0, 0)
  Detection: (r > 180) AND (r - g > 50) AND (r - b > 50)
  Range fallback: (200,120,0) to (255,200,90)

BLUE (less common, fiber upgrade available)
  Range: (50,80,180) to (120,160,255)

### Filter thresholds (don't tighten - it breaks detection)
  - DOT_MIN_AREA = 25 pixels
  - DOT_MAX_AREA = 600 pixels
  - aspect_ratio <= 2.0 (round dots only)

### Critical lessons (DO NOT REDO)
  - Tightening orange to "fix freeway false positives" stopped
    detecting all gold dots. Don't tighten. Filter freeways differently.
  - Skipping (no #) rows lost 80% of writes. Keep them - they're
    door-knock leads.
  - Adding "NEEDS REVIEW" fallback when geocoding fails poisons
    the All Leads tab. Skip the row instead.

---

## DOTS -> ADDRESSES (the geocoding pipeline)

Pixel detection alone gives you (color, x, y, area). Useless for sales.
Need to convert to real-world addresses.

### Required step 1: pixel -> lat/lon
Each tile covers a known geographic area. Need bounds:
  north (lat at top edge)
  south (lat at bottom edge)
  east (lon at right edge)
  west (lon at left edge)

Then any pixel (x, y) in W x H tile:
  lon = west + (x / W) * (east - west)
  lat = north - (y / H) * (north - south)

Houston map calibration anchor (proven values):
  LAT_PER_PIXEL = -0.000015
  LNG_PER_PIXEL = +0.000020

### Required step 2: lat/lon -> address (reverse geocoding)

Nominatim (free, OpenStreetMap):
  URL: nominatim.openstreetmap.org/reverse
  RATE LIMIT: 1 request per second (HARD - violations get IP banned)
  Use time.sleep(1.1) between calls
  Returns: house_number, road, postcode, city, state

Photon (free, no rate limit) - FALLBACK ONLY:
  URL: photon.komoot.io/reverse
  Use when Nominatim returns null or rate-limits
  Quality slightly worse than Nominatim

### Critical lessons (DO NOT REDO)

Nominatim failure mode:
  When rate-limited, returns null/empty
  Old code did .get() on null - crashed (bg err: NoneType)
  Fix: use 'or {}' pattern: result.get('address') or {}
  Fix: handle None response BEFORE accessing fields

Cache aggressively:
  Same lat/lng (rounded to 5 decimals) = same address
  Cache file: geocode_cache.json
  After cache fills, re-runs are 10-100x faster
  Saves Nominatim rate limit budget

When BOTH fail:
  Skip the row entirely. Don't write "NEEDS REVIEW" or coordinates
  as fallback - both poison the sheet.

When tile bounds are missing:
  Can't compute lat/lon for dots
  Workaround: OCR street names from tile, geocode the streets,
    use 2-3 anchors to compute tile bounds via affine math
  Tesseract on laptop = free unlimited OCR
  Vision API on phone = $1.50/1000 after 1000/mo free tier

### The 2-stage pipeline (when scanner doesn't save bounds)
  Stage 1: detect dots (pixels only) - fast, free, phone OK
  Stage 2: OCR street names + geocode (laptop, free Tesseract)
  Stage 3: pixel -> lat/lon -> address
  Stage 4: write CSV / sheet

50K pics estimate at Nominatim 1 req/sec = ~14 hours first run.
Subsequent runs hit cache, way faster.

---

## SHEET WRITES - THE CONVENTIONS

### Sheet IDs
Active: 12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag
Original: 15ymTkIGPWs6quB035l414ns5hkG9cQ5xr_W4ukd0OAA

### The split logic (battle-tested)
  if property_type == "COMMERCIAL":
      sheet.write("Commercial", row)
      if is_green:
          sheet.write("Green Commercial", row)
  else:
      sheet.write("Residential", row)
      if is_green:
          sheet.write("Green Residential", row)
  sheet.write("All Leads", row)  # always

### Batch writes (proven)
  BATCH_SIZE = 12 rows per tab before flushing
  HOT ZONES + Changes flush instantly (alerts can't wait)
  All Leads / Commercial buffers (volume can wait)
  flush_all() on Ctrl+C in finally block

### Tab column conventions

Commercial / Green Commercial:
  A=Business Name, B=Address, C=Phone, D=Category,
  E=City, F=State, G=Zip, H=Zone, I=Instance, J=Scan#,
  K=Rep, L=Date, M=Lat, N=Lng

Ready To Call:
  A=Name, B=Phone, C=Address, D=City, E=State, F=Zip

All Biz Phones:
  A=Name, B=Address, C=Phone, D=Category,
  E=City, F=State, G=Zip

### Sheet limits
  10 million cells per workbook (HARD)
  Tabs with 100K rows but 88 actual data rows = wasting cells
  sheet_cleaner.py trims wasted cells
  Currently 9M used of 10M, 6-7M trimmable

### Service account gotcha
  Has ZERO Drive storage write quota
  Can READ and UPDATE existing files
  CANNOT CREATE new files (storageQuotaExceeded)
  Workaround: use GitHub for new files, Drive only for backup

### Hot zone tracking (the diff that matters)
File: zone_history.json
Schema: {zone_row_col: {orange, green, blue, empty, timestamp}}

Triggers (these are the goldmine):
  empty -> has_dots = "NEW FIBER ZONE" (scan immediately)
  big_gold (orange >= 100) appears = "BIG GOLD CLUSTER" (knock when flips)
  orange drops to 0 + green stays = "FIBER JUST WENT LIVE"
  green disappears = AT&T patched the map (investigate)

This is the change-detection logic that separates dot detection
from real intelligence. Don't lose this.

---

## SETUP CHECKLIST - what trips up every new laptop

Before running scanner:
  [ ] google_creds.json next to script
  [ ] Service account email shared as Editor on sheet
  [ ] Terminal shows "Connected to Google Sheets!" at startup
  [ ] Terminal shows "Loaded N existing entries"
  [ ] Chrome with AT&T map MAXIMIZED on top
  [ ] Map zoomed to street level (zoom 16-18)
  [ ] Command Prompt SHRUNK to bottom-right corner (NOT covering map)
  [ ] First run: hover-calibrate Search button
  [ ] First run: click "Created: All Leads, Commercial..." messages

Common failures:
  - Empty sheet, no errors = command prompt covering map
  - "header row contains duplicates" = old schema, rename old tabs
  - "bg err: NoneType" = Nominatim down, retry or wait
  - "GOLD: Res=0 Comm=0" = no dots in this area, or wrong zoom
  - Random pop-ups = mouse hovering over map, add mouse parking
  - Search button gone = panned too far, nudge back

---

## WHAT NEVER TO REBUILD (use what exists)

themapman.py
  --houston flag = walks all 159 metro ZIPs
  --headless flag = no visible browser
  --enrich-only flag = backfill addresses on existing rows
  --all flag = both gold + green
  --reset flag = clear dedupe, redo
  Built-in: 60+ chain blocklist, bad phone detector, dedupe across run

validatorman.py
  --force flag = re-validate even "already done" rows
  --tab "X" flag = target specific tab
  --headless flag = no browser
  --limit N flag = test mode

fiber_scan.py
  Multi-instance picker on startup (1-4)
  Hover-calibrate Search button (first run)
  Resume from scan_progress_N.json after Ctrl+C
  Hot zone alerts to HOT ZONES tab
  GHL CSV export to GHL_exports folder

GHL LeadConnector mobile app (Play Store / App Store)
  Free
  Dials from GHL contact list
  Sends/receives SMS through GHL number
  Logs calls back to contact
  Push notifications for replies

---

## DECISION TREE - when error appears

1. Was something working before this error?
   YES -> patch, do not rewrite
   NO -> investigate from scratch

2. Is the error in geocoding (None, timeout, rate limit)?
   -> Add Photon fallback, NOT rewrite
   -> Verify time.sleep(1.1) between calls
   -> Check geocode_cache.json exists

3. Is the error in sheet writes (header mismatch, permission)?
   -> Rename old tab to "X OLD", let script create fresh
   -> Verify service account is Editor on sheet
   -> Check column count matches script expectation

4. Is the error in screenshot (all empty, all dark)?
   -> Command prompt covering map (most common)
   -> Wrong screen for multi-monitor setup
   -> Browser minimized or not focused

5. Is the error in motion (no pan, no click)?
   -> Browser not active window
   -> Wrong PAN_PIXELS for current zoom level
   -> Search button position needs recalibration

6. Is the rebuild instinct kicking in?
   -> SEARCH past chats first
   -> CHECK if a flag exists
   -> PATCH the broken function only
   -> Test with --limit 5 before full run

---

## RESUME NEXT SESSION

Tell Claude: "pull BRAIN" or "read BRAIN from github"
Then: "read WORKING_PATTERNS"
Claude pulls both, fully synced.

Updates to this doc go through push_lessons_now.py
(self-contained script with content embedded - no copy-paste).

End of WORKING_PATTERNS.
