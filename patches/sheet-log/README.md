# The follow-up board — sheet log patch (2026-09-03, UNTESTED)

Patrick's spec, verbatim, in order:
1. "when we enrich leads add that to the sheet / update the software so that doesn't cause a prob but that way u can tell what's enriched"
2. "so now the sheet will contain the data enriched by deal machine so u don't enrich 2x, dnd, u can check if we called and if dead"
3. "use the sheet to log sales etc"
4. "color for sales status red no / green cb maybe / blue paid"
5. "I want ghl data and whether or not we already enriched something to be obvious so the sheet seems like a good place for that / and if it's sold or needs to be called back cuz we're doing an atrocious job of following up"
6. "I want the sheet to contain the same columns grey green gold biz fiber green biz / and if it's enriched it has name cell number / color coded for sales cb or ni"

## What the patch does

One new block in `optimus/standalone/maps_scraper_standalone.py` (file `sheet_log_block.py` here, to be inserted verbatim immediately BEFORE `def publish_tab_counts(sh):`) plus one call site (bottom of `sheet_log_block.py`, to be inserted immediately AFTER the `replay_parked(...)` try/except in `main()`).

- `Enriched Leads` tab in the SPLIT workbook (`1DXu-nuQvVKrqQVk8LDNwLztG31ddi6sAyo8vXDFKcmQ`): the hunter's 13 columns first (Address, Dot Color, Captured At, Business, Phone, Run ID, Operator, Lat, Lng, City, State, ZIP, Status — copied from Gold Confirmed / Grey Fiber Customers / Precise Fiber (via the biz-match set) / Fiber Green Biz / Upgrade Orange Biz / Maps Businesses), then Tab, Name, Cell, Phone Type, Enriched At, Source, Pool, GHL Contact ID, Likely Gold, DNC, Dialed, Last Call, Disposition, DND, Dead, Status At. 30 columns.
- `Sales Log` tab: Sold At, Address, City, State, ZIP, Name, Cell, Product, Rep #, Pool, Source, GHL Contact ID, Opportunity ID, Stage, Status, Logged At. Hand-typed rows never touched. No dollar figures ever (Ara has the sheet).
- Whole row coloured by Disposition / Status: green `CB|CALL BACK|MAYBE`, red `NO|NI|NOT INTERESTED|DEAD|DNC`, blue `PAID|SOLD|INSTALLED`. Rules added once at tab creation.
- Feed = Google Sheets Claude creates in Drive folder `OPTIMUS FEED (Claude → sheet)` = `1XOqADybKvneC5gwsxjpsGkVC6RLQ-1an` (shared writer with `fiberscanner@fiberscanner-493900.iam.gserviceaccount.com`). Title `OPTIMUS FEED enriched|status|sales <anything>`, first tab = header of field names + rows. Landed files are renamed `LANDED …`. Receipt: `optimus/_feed/_landed.json` on GitHub (no PII). Names and cells never touch GitHub — both repos are public.
- Feed field names: enriched = address, city, state, zip, lat, lng, business, name, cell, phone_type, enriched_at, source, pool, ghl_contact_id, likely_gold, dnc, colour (+ optional dialed, last_call, disposition, dnd, dead, status_at). status = ghl_contact_id, dialed, last_call, disposition, dnd, dead, status_at. sales = sold_at, address, city, state, zip, name, cell, product, rep, pool, source, ghl_contact_id, opportunity_id, stage, status.
- Keys: GHL contact id (else ADDRESS|ENRICHED AT); sales key = opportunity id (else GHL id|sold at). Repeats land nothing twice. FULL workbook is printed once and never retried. Foreign header on an existing tab = left alone.
- Runs AFTER `open_sheet()` (so `init_match()` has loaded the green set) — that is why the call site is after `replay_parked`, NOT in `_run_startup_clean`.

## Status

WRITTEN, NOT COMPILED, NOT RUN. The session that wrote it lost its shell to an auto-mode safety block before `py_compile` and `test_board.py` could run. The local hunter clone that held the edit died with that container.

## To finish (a fresh session, ~15 minutes)

1. Clone the hunter repo branch `claude/optimus-map-tools-setup-6dcl6o`.
2. Insert `sheet_log_block.py` (minus its two apply-comments) before `def publish_tab_counts(sh):`; insert the call-site snippet after the `replay_parked` try/except in `main()`.
3. `python3 -m py_compile optimus/standalone/maps_scraper_standalone.py`.
4. Run `test_board.py` (fake gspread; needs `_UNIT` regex from the scraper if the grab fails — see the top of the test). All asserts must pass.
5. Ask Patrick for go (RULE 0). The scraper self-updates on any byte change; no BUILD_DATE bump needed for the scraper.
6. Add to `brain-verify` CODE_CLAIMS: `(SCRAPER, r"def sync_sheet_log\(", True, ...)` and `(SCRAPER, r'^FEED_FOLDER_ID = "1XOqADybKvneC5gwsxjpsGkVC6RLQ-1an"', True, ...)`.
7. First feed: create `OPTIMUS FEED enriched pcola-fresh` in the folder from the PCOLA FRESH pool (141 rows, name + cell from GHL, tag `pcola-fresh`).
