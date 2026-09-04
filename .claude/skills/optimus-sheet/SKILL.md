---
name: optimus-sheet
description: How to read, count, clean and analyse the ATT FIBER LEADS workbook without getting it wrong. Load this BEFORE answering any question about the sheet, before quoting any row or dot count, before enriching or uploading anything sourced from it, and before saying any part of it is unreachable. It carries the tab map, the five read paths in order, the four double-click tools that already exist on Patrick's PC, and the specific ways every previous session has misread this workbook.
---

# THE ATT FIBER LEADS SHEET — read it right or do not quote it

Workbook `1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA`, owner
`patricksiado@gmail.com`. **8 TABS, ~796,085 rows, at its 10,000,000-cell
ceiling.**

**Patrick, repeatedly:** *"every fuking time I ask for data from the sheet u read
it wrong upload or enrich wrong data."* Every one of those misreads is listed at
the bottom of this file. Read them before you answer.

---

## 1. THE TAB MAP — MEASURED 2026-09-04 off `tabs.json` STAMPED 2026-09-04 03:08:57

**THERE ARE EIGHT TABS. 21 WERE DELETED ON 2026-09-02/03 BY SOMEBODY UNKNOWN.**
This table used to list 29 and was a week stale; that staleness is what made the
"11,490 gold" and "645k Precise Fiber" numbers keep coming back.

| Tab | Rows | What it is | Dot |
|---|---|---|---|
| `Precise Fiber` | **687,923** | every captured dot. **GREEN ONLY since 2026-08-26.** New green goes to the SPLIT workbook `1DXu-nuQvVKrqQVk8LDNwLztG31ddi6sAyo8vXDFKcmQ` | GREEN $500 |
| `Grey Fiber Customers` | **56,799** | existing AT&T fiber customers. **Never dial — this is the SCRUB list** | GREY |
| `Maps Businesses` | **39,294** | scraped businesses, unmatched to any dot | — |
| `Fiber Green Biz` | **7,300** | green businesses. **This is the NEW-FIBER DETECTOR** — a cluster means fiber was just lit there. Columns are only `Business Name / Phone / Address / Website / Category / <hand-typed call status>` — NO Captured At, NO lat/lng, NO city/state/ZIP | GREEN |
| `Gold Confirmed` | **4,707** | resi copper. **A SIGHTING COUNT, NOT DOORS** — 176 readable rows were 10 unique addresses. Purge ran; all post-08-24 | GOLD $140 |
| `Upgrade Orange Biz` | **62** | gold BUSINESSES — the gold half of the detector, **and it is dead**: 62 against 39,294 businesses. `init_match` fix went in 09-03, never run | GOLD |
| `Territory Claims` | 0 | machine coordination | — |
| `_Dedupe Lock` | 0 | machine coordination | — |

**TABS THAT NO LONGER EXIST — do not read them, do not write code against them,
do not tell Patrick a number is on one of them:** `Unknown Customers` ·
`Gold Dots` · `GOLD — CLEAN` · `Beaumont Gold — Aug 2026` ·
`TEST-Green-2026-08-24` · `TEST-Gold-2026-08-24` · `Backend Comm` ·
`Backend Analysis` · `Backend Capture` · `Hunter Status` ·
`HOUSTON UNVERIFIED — Aug 19` · `ZZ_TMP_GRID` · `TMP Sweep Census` ·
`Gold Biz Campaign — READY` · `Devonwood Campaign` · `Operator Scorecard` ·
`_dispatch` · ` _temp_ash_lookup` · `_optimus_probe` · **and four hand-built
working tabs that should NOT have gone: `Warm Backlog — Replied YES` (40 people
who said yes), `Angleton Call List — Aug 2026`, `WORK LIST — Beaumont +
Angleton`, `GOLD — CLEAN`.** Google's File → Version history restores them.

**`DASHBOARD` and `README` DO NOT EXIST EITHER.** Any instruction anywhere to
"read DASHBOARD first" is dead — it was the recommended read path for a week
against tabs that are not there.

## 2. THE FIVE READ PATHS — try them in this order

1. **`read_file_content`** on the workbook. Returns a BOUNDED SAMPLE of the
   **first 9 tabs** (~190-355 rows each, ~211k chars). Too big for the tool cap,
   so the harness saves it to a local file — parse that with python for free.
   Takes no tab argument. **Cannot reach `Gold Confirmed`.**
2. **`get_file_metadata`** — `contentSnippet`, plus the authoritative liveness
   pair `fileSize` + `modifiedTime`.
3. **`optimus/_feed/sheet/tabs.json`** on the hunter repo — exact row counts per
   tab, plain curl, no Google auth:
   `raw.githubusercontent.com/patricksiado-prog/Go-High-Level-MCP-2026-Complete/claude/optimus-map-tools-setup-6dcl6o/optimus/_feed/sheet/tabs.json`
   **`main` and `master` both 404 — the branch name is load-bearing.**
4. **`sheet_feed.py --tab "<name>"`** run on the hunter PC — publishes that whole
   tab in 500-row chunks to `_feed/sheet/chunk_NNN.json`, which Claude reads with
   curl. **This is how any tab too big for the Drive connector gets analysed.**
5. **Autosheet** — the only path that can address a tab by name or WRITE.
   Currently `api-billing-empty-balance`; needs a card.

**ONE TOOL FAILING SAYS NOTHING ABOUT THE OTHERS.** Autosheet's billing error is
not evidence the sheet is unreachable. That mistake was made 2026-08-25 and made
again 2026-09-03.

## 3. THE FOUR TOOLS THAT ALREADY EXIST — stop saying it cannot be done

All in the hunter folder on Patrick's PC. They use the fiberscanner service
account, which talks to the sheet directly — no Autosheet, no Claude creds.

| Run this | It does |
|---|---|
| ~~`COUNT_TABS.bat`~~ RETIRED | The Maps Scraper publishes stamped tab counts to `_feed/sheet/tabs.json` at every launch (2026-09-03). Nothing to run |
| **`CLEAN_SHEET.bat`** (double-click) | **THE CLEAN — UNSAFE UNTIL PATCHED. It deletes `Warm Backlog — Replied YES` and 6 other rep-built tabs (MEASURED 2026-09-03; see `patches/clean-sheet-one-doubleclick.md`).** Dry run first, asks for YES, then migrates `TEST-Gold-*` into `Gold Confirmed`, backs every tab up to CSV, dedupes `Gold Confirmed` and `Precise Fiber` by address, deletes only DEBUG/TEST tabs. Pipeline tabs are protected by a KEEP whitelist |
| **`py gold_audit.py`** | READ-ONLY: total rows, **UNIQUE ADDRESSES**, duplicates, lat/lng coverage, capture date range on `Gold Confirmed`. **This is the unique-gold number.** One-line paste, nothing to save |
| **`py decode_gold.py`** | reads AT&T's own saved reply and settles what `unavailable` means. If it is copper, one line in `build_codes.json` converts that whole bucket to gold retroactively |

The `gold_audit.py` one-liner:

```
py -c "import urllib.request as u;exec(u.urlopen('https://raw.githubusercontent.com/patricksiado-prog/Go-High-Level-MCP-2026-Complete/claude/optimus-map-tools-setup-6dcl6o/optimus/gold_audit.py').read())"
```

## 4. WHAT GOLD IS — `build_codes.json`, the only ground truth

`curr_ntwrk_bld_type_cd` decides it:

- **COPPER → GOLD:** `fttn-bp` `fttn` `ip-rt` `iprt` `copper` `ipbb` `adsl` `vdsl` `dsl`
- **FIBER → GREY:** `fttp-gpon` `fttp` `gpon` `ftth`
- **No subscriber BAN → GREEN**, whatever the build code says
- anything else → UNKNOWN (since 2026-08-23)

**A real gold dot is a CUSTOMER whose build code is in the copper list. Nothing
else is gold.**

## 5. EVERY WAY THIS SHEET HAS BEEN MISREAD — check yourself against this list

1. **Counting rows as dots.** The sheet writes one row per sighting. 170
   `VERIFIED_GOLD` rows were **4 unique addresses.** Always say "rows" or run
   `gold_audit.py` for uniques.
2. **Counting a CITY NAME as a colour.** 225 rows in *Orange, Texas* were
   reported as orange dots. They are ZIP 77630 with an EMPTY build code — not
   leads at all.
3. **Quoting a stale gold count.** 11,490 was never right after the purge, and
   4,707 is a SIGHTING count, not doors. `py gold_audit.py` gives uniques.
4. **Believing a tool failure means no access.** See section 2.
5. **Trusting the first tab.** `Precise Fiber` is tab #1, so the cheap read
   returns green apartment addresses instead of numbers. **There is no DASHBOARD
   and no README to fall back to — those tabs were deleted.** Path 3
   (`tabs.json`) is the counts answer now.
6. **Reading `latest.json` at launch.** It is an all-zero STUB. Check `run_id`
   and `generated_at` before calling capture broken.
7. **A moving `modifiedTime` with a FLAT `fileSize`** means it is being touched
   and nothing is landing. That is the authoritative liveness check, not the
   console and not the heartbeat.

## 6. BEFORE YOU ANSWER ANY SHEET QUESTION

- Did you name the tab, or are you guessing from a row shape?
- Are you saying ROWS or UNIQUE ADDRESSES? Say which.
- Is the number MEASURED today, with how, or carried forward?
- Did you try all five read paths before saying anything is unreachable?
- Is a `.bat` or a one-liner the real answer instead of "I can't"?


## 7. (removed 2026-09-04) — the 29-tab list lived here and was a week stale

It listed 21 tabs that no longer exist and three (`DASHBOARD`, `README`,
`Unknown Customers`) that never did. **Section 1 above is the live map.** Never
re-add a tab list that is not read from a STAMPED `tabs.json` in the same turn.

## 8. HOW TO ANALYSE THE SHEET — one method per question (added 2026-09-03)

Patrick: *"tell brain how to analyze sheet."* The failures were never access;
they were picking the wrong method for the question. Match the question to the
row below, quote the number WITH its method and date, and never substitute a
neighbouring method because it is easier.

| Question | The ONLY method | Never |
|---|---|---|
| **How many rows per tab / which tabs exist** | `_feed/sheet/tabs.json` **with a `generated_at` stamp** (scraper republishes it at every launch). Unstamped = stale feed, say so | Counting a Drive `read_file_content` sample; quoting an unstamped file as live |
| **How many GOLD / GREEN / GREY** | Tab = colour: `Gold Confirmed`, `Precise Fiber` (green only since 08-26, split workbook since 09-03), `Grey Fiber Customers`. Row count from stamped tabs.json | Filtering `Precise Fiber` by a colour column; reading colour off a city name or ZIP |
| **UNIQUE gold addresses (dots, not rows)** | `py gold_audit.py` on the hunter PC (one-line paste in CLAUDE.md). Prints rows, uniques, dupes, date range | Presenting a row count as a dot count; saying it cannot be taken |
| **Is a specific address gold** | `Status` column on its row, or `build_codes.json` on its build code | The tab position, a neighbour's colour, a DealMachine field |
| **Where is a gold POCKET** | Gold density per street/ZIP off `Gold Confirmed` (group by ZIP + street). Confirm the town from the lat/lng, not the sweep name — the 09-03 "Pensacola" pocket was Milton | Trusting the sweep label; counting a city name as a colour |
| **Is the sheet GROWING (is capture landing)** | Row counts in a STAMPED `tabs.json` (scraper launch) compared with the previous stamp; after the sheet-log deploy also `_feed/_landed.json`. **Drive `fileSize` is NOT a signal — it sat at 8,484,584 while ~75k rows landed (2026-09-03)** | `fileSize`, the console, `latest.json`, the heartbeat, `SUCCEEDED` |
| **What did the last run capture** | `_feed/latest.json` → `classified_*`, `written`, `failed_writes`, `capture_truth.delivery`. Check `run_id`/`generated_at` first (a launch stub is all zeros) | Reading counters without the run id |
| **Anything on a tab too big for Drive** | `py sheet_feed.py --tab "<name>"` → `_feed/sheet/chunk_NNN.json`, then python on the chunks | Pulling the tab whole; Autosheet on a big tab |
| **Which contacts are dialable / dialed / opted out** | GHL `search_contacts` on the tag, then read `tags`, `dnd`, dispositions on each record | The sheet — it has no dial history |
| **Did the clean / purge run** | The scraper console (`GOLD PURGE:` / `JUNK TABS DONE`) or a stamped tabs.json without the junk tabs | Assuming from a flag file, or from CLAUDE.md alone |

**Every answer states three things: the number, the method from this table,
the date it was taken.** If the method was unavailable, say "could not measure"
— never fall through to a weaker method silently. Rows are an upper bound on
addresses; addresses are an upper bound on people.


## 9. WHAT HAS BEEN ENRICHED — the `Enriched Leads` tab (2026-09-03)

Patrick: *"when we enrich leads add that to the sheet."* The answer lives in
the **SPLIT workbook** (`1DXu-nuQvVKrqQVk8LDNwLztG31ddi6sAyo8vXDFKcmQ`), tab
`Enriched Leads`, one row per enriched person: Address · City · State · ZIP ·
Enriched At · Source · Pool · GHL Contact ID · Phone Type · Likely Gold · DNC ·
Colour · Landed At. It is written by the Maps Scraper at launch from the feed
Claude publishes — never by hand, never by Claude directly.

**After ANY enrichment (DealMachine pull, GHL load, tagging a pool):**
```
.claude/skills/session-continuity/scripts/publish-enriched ROWS.json --pool <ghl-tag>
```
ROWS.json = address, city, state, zip, enriched_at, ghl_contact_id, phone_type,
likely_gold, dnc, colour. **No names, phones or emails** — the script refuses
them; the repo is public. Then, after the next Maps Scraper launch,
`publish-enriched --check` reads `_feed/enriched/_landed.json` and says how many
rows are on the tab. A stamp older than your drop = no launch since, not
"nothing to land".

**Before enriching anywhere:** read this tab (or the feed dir) for the ZIP/pool
first. A street already on it has already cost credits.
