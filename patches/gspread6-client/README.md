# gspread 6 killed the split-workbook redirect AND the Enriched Leads board — found 2026-09-04 off Patrick's console

**NOT PUSHED. RULE 0 — Patrick decides.** `maps_scraper_standalone.py` self-updates
on any byte change: a push to `Go-High-Level-MCP-2026-Complete` is a DEPLOY TO EVERY PC.

## What the console showed (photos, 14:04-14:06 CT)

    (Precise Fiber redirect 1DXu-...: 'HTTPClient' object has no attribute 'open_by_key'
     -- falling back to the main workbook. Check it is shared with the service account.)
    SHEET LOG: feed folder not readable ('HTTPClient' object has no attribute 'li...')

The "check it is shared" hint is wrong — sharing is fine. It is an API change.

## Mechanism (proven locally on gspread 6.2.1 — what a plain `pip install gspread` gives every PC)

gspread 6 made `Spreadsheet.client` an **`HTTPClient`**. `HTTPClient` has no
`open_by_key()` and no `list_spreadsheet_files()` — those live on `gspread.Client`.
The scraper calls both on `sh.client`:

- line 540  `return sh.client.open_by_key(sid)`  → split-workbook redirect → **falls back to the FULL main workbook**, rows park
- line 1798 `client = sh.client` → line 1505 `client.list_spreadsheet_files(folder_id=FEED_FOLDER_ID)` → **`sync_sheet_log` cannot read the feed folder** → every `publish-enriched` drop (including the 9-row `sheet-gold` drop of 2026-09-04 18:47Z) never lands on `Enriched Leads`

The hunter is clean: it keeps its own `client` from `gspread.authorize()` and calls
`client.open_by_key` directly.

brain-verify passed both features because it checks code PRESENCE, not runtime.
Two NEGATIVE claims were added (`sh.client.open_by_key` and `client = sh.client`
must be absent); they read `*** DRIFT` until this lands — correctly.

## The fix (48-line diff, one helper + two call sites)

`_gc(sh)` returns a real `gspread.Client` on gspread 5 AND 6: if `sh.client`
already has `open_by_key` (gspread 5) it is returned unchanged; otherwise a
`gspread.Client` is built on the SAME `AuthorizedSession` (no re-auth, same
service account). Both call sites use `_gc(sh)` instead of `sh.client`.

Alternative considered: pin `gspread<6` in the installer. Rejected — it touches every
PC's Python environment and needs a reinstall; the helper is the smaller blast radius.

## Test — `python3 test_gspread6_client.py` (no network)

Builds the exact objects the scraper holds after `open_sheet()` on gspread 6.2.1,
reproduces BOTH console errors verbatim with the old path, then proves the fix.
Output:

    gspread 6.2.1
    reproduced (old path): 'HTTPClient' object has no attribute 'open_by_key'
    reproduced (old path): 'HTTPClient' object has no attribute 'list_spreadsheet_files'
    fixed (gspread 6): _gc(sh) -> Client with open_by_key + list_spreadsheet_files, same creds
    gspread 5 shape: returned the existing Client unchanged
    both call sites now go through _gc(sh); no sh.client.open_by_key left
    
    ALL TESTS PASS

## Deploy (on Patrick's go)

Apply `gspread6-client.diff` to `optimus/standalone/maps_scraper_standalone.py` on a
FRESH fetch of the hunter branch (`claude/optimus-map-tools-setup-6dcl6o`). Scraper,
so no `BUILD_DATE` bump. At the next Maps Scraper launch expect the redirect line to
print the split workbook title instead of the HTTPClient error, and `SHEET LOG:` to
report the feed files it found. Then `publish-enriched --check` should show the 9
`sheet-gold` rows landed. Add the two brain-verify claims' inverse (`^def _gc\(sh\):`
present) in the same commit.

**This does NOT fix "THE SHEET IS FULL."** That is the 10M-cell ceiling on the main
workbook and needs archiving (BRAIN.md 22.35). The fix only stops the scraper from
throwing green-biz rows at the full workbook when the split one is right there.
