# GOLD AND GREY WERE NEVER BEING DEDUPED — found 2026-09-04

**NOT PUSHED. RULE 0 — Patrick decides.** A push to
`Go-High-Level-MCP-2026-Complete` is a DEPLOY TO EVERY PC.

## What is wrong

`dedupe_all_tabs()` in `optimus/standalone/maps_scraper_standalone.py` has run
every 30 minutes, in the background, on every scraper launch, for weeks. Its job
list (line ~928 of the LIVE file) is:

    Maps Businesses · Fiber Green Biz · Upgrade Orange Biz
    Precise Fiber   (every 6th pass — huge tab)

**`Gold Confirmed` and `Grey Fiber Customers` are not in it.** The two colour
tabs a rep actually calls off are the two tabs nothing has ever cleaned.

## What that cost, measured

`Gold Confirmed` reads **4,707 rows**. The 176 rows a Claude session can read
off it were **10 unique addresses** — `7631 FUQUA ST` written **96 times**,
`800 N ARCOLA ST` 50 times, `611 E MYRTLE ST` 22 times. That is why "I want the
4500 golds" has no honest answer: the row count is a SIGHTING count, and nothing
in the software collapses it.

`Grey Fiber Customers` is **56,799 rows** on the same footing — and grey is the
SCRUB list, so its duplication makes every scrub pass slower for no gain.

## The fix

Two lines added to the `jobs` list. Both tabs are address-first, so they reuse
`pf_key` / `pf_score` — the exact key and score already proven on
`Precise Fiber`: **keep the FULLEST copy of each address, not the earliest.**
Gold (4,707) runs every pass; grey (56,799) runs on the same every-6th-pass
cadence as Precise Fiber so a big tab does not dominate a pass.

Nothing else changes. `_dd_dedupe_tab` already backs the whole tab up to a local
CSV before touching anything, holds the cross-machine `_Dedupe Lock`, is
append-safe, and caps at 6,000 removals per pass so it converges instead of
timing out.

## Test

`python3 test_dedupe_goldgrey.py` — runs the REAL `_dd_dedupe_tab` against a
fake workbook shaped like the live tabs, seeded with the duplication we actually
measured.

    Gold Confirmed           172 rows -> 5 unique (removed 167)
    Grey Fiber Customers      41 rows -> 2 unique (removed 39)
    kept the FULLEST 7631 Fuqua row (City=HOUSTON), not the skinny twin
    second pass removed 0 rows -- idempotent
    missing tab returns 0, no crash
    ALL TESTS PASS

## Deploy

Apply `dedupe-gold-grey.diff` to `optimus/standalone/maps_scraper_standalone.py`
in the hunter repo, on a FRESH `git fetch` of that file (a clone in a Claude
session is days stale — that trap nearly reverted 54 commits on 2026-09-03).
This file is the SCRAPER, not the hunter, so `BUILD_DATE` does not apply; the
scraper self-updates on any byte change. Takes effect at the next Maps Scraper
launch. Expect `[dedupe] Gold Confirmed: removed N duplicate rows` in the
console, and `Gold Confirmed` to drop hard.

Add a brain-verify claim in the same commit:
"gold and grey are in the dedupe job list".
