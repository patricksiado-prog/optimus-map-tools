# The gold purge has never run because it is gated behind a sheet open that fails

MEASURED 2026-09-03. Not pushed — RULE 0.

## What is actually true

`purge_prefix_gold()` is real and correct. It lives in
**`optimus/standalone/maps_scraper_standalone.py`**, lines 1174-1266, called once
at line 1836. Commit `754ecbf` (2026-08-27T10:02:17Z) modified **exactly one
file**: `optimus/standalone/maps_scraper_standalone.py`, +98 / -0.

**`precise_fiber_hunter.py` contains ZERO occurrences of the string "purge".**
`clean_sheet.py` contains ZERO. So:

- "the purge runs at HUNTER launch" — WRONG, it was never in the hunter
- "fixing the AT&T login runs the purge for free" — WRONG, the AT&T login is
  irrelevant to it
- "CLEAN_SHEET.bat cleans the gold contamination" — WRONG, that dedupes by
  address, it does not date-cut

**The purge runs when the MAPS SCRAPER launches. Nothing else runs it.**

## The five gates it has to pass, and the one that is almost certainly closed

```python
sheet_ws, sheet_seen = (open_sheet() if to_sheet else (None, set()))
...
if sheet_ws is not None and os.environ.get("SCRAPER_NO_DEDUPE", ...) not in (...):
    try:
        purge_prefix_gold(sheet_ws.spreadsheet)
        ...
    except Exception as e:
        print("  (dedupe off: %s)" % str(e)[:60])
```

- **Gate A** — `to_sheet` false (CSV-only run) → skipped.
- **Gate B — the deadlock.** `open_sheet()` opens the **`Maps Businesses`** tab
  and, if that tab is missing, calls
  `sh.add_worksheet(title=SHEET_TAB, rows="20000", cols="7")` = **140,000 cells**.
  On a workbook sitting at the 10,000,000-cell ceiling that throws a 400, the
  bare `except` at line 475 catches it, and `open_sheet()` returns
  `(None, set())`. `sheet_ws is None` → **the whole block, purge included, is
  skipped.**
  So: the sheet is too full to open, therefore the cleanup that would free
  ~118,000 cells (9,052 rows x 13 cols) never runs. The purge is the fix for the
  condition that stops the purge.
- **Gate C** — `SCRAPER_NO_DEDUPE=1`.
- **Gate D — it fails quietly.** Any exception inside prints only
  `"(dedupe off: ...)"`. A failed purge reads as an unrelated minor notice.
  This violates NO SILENT RUNNING (2026-08-28).
- **Gate E — the marker locks on abnormal reads.** Lines 1204 and 1227 write
  `gold_purge_done.flag` for "empty tab" and "clean already". If the tab ever
  read short or empty once — a quota blip, a partial `get_all_values()` — the
  marker is written and **the purge never runs again on that PC, ever.**

## The fix (written, tested by reading, NOT pushed)

Three changes, all in `maps_scraper_standalone.py`:

1. **Do not make the purge depend on `open_sheet()`.** It only needs
   `Gold Confirmed`; it has no business waiting on `Maps Businesses`. Open the
   spreadsheet for it directly and call it before the `sheet_ws` check:

```python
    # The purge only needs 'Gold Confirmed'. Opening 'Maps Businesses' can fail
    # on a full workbook (add_worksheet = 140k cells over the ceiling), and that
    # used to take the purge down with it -- the sheet was too full to open, so
    # the cleanup that frees ~118k cells never ran. Open it on its own.
    if to_sheet and os.environ.get("SCRAPER_NO_DEDUPE", "").strip() not in ("1", "true", "yes"):
        try:
            _c = _find_creds()
            if _c:
                import gspread
                from google.oauth2.service_account import Credentials
                _sc = ["https://www.googleapis.com/auth/spreadsheets",
                       "https://www.googleapis.com/auth/drive"]
                _sh = gspread.authorize(
                    Credentials.from_service_account_file(_c, _sc)).open_by_key(SHEET_ID)
                purge_prefix_gold(_sh)
        except Exception as e:
            print("\n  *** GOLD PURGE DID NOT RUN: %s" % str(e)[:70])
            print("  *** 'Gold Confirmed' still holds the pre-%s contamination."
                  % GOLD_CUTOFF)
```

2. **Never write the marker on an abnormal read.** Line 1204 (`"empty tab"`)
   must not mark done — an empty `Gold Confirmed` is not a clean tab, it is a
   failed read. Delete that write and `return` bare. Keep line 1227
   (`"clean already"`), which is a real measured result.

3. **Say it loudly when it is skipped**, per NO SILENT RUNNING. Replace the
   `"(dedupe off: %s)"` swallow with a block that names the purge specifically.

## What Patrick has to do RIGHT NOW to get the junk out

**Double-click the Maps Scraper Desktop icon and let it start.** The purge runs
in the first ~30 seconds of launch, before any scraping. It backs the whole tab
up to a local CSV and saves the removed rows to their own JSON first.

If the console prints `(dedupe off: ...)` or nothing about a gold purge, gate B
is closed and the patch above is required first.
