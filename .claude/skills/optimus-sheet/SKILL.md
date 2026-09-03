---
name: optimus-sheet
description: How to read, count, clean and analyse the ATT FIBER LEADS workbook without getting it wrong. Load this BEFORE answering any question about the sheet, before quoting any row or dot count, before enriching or uploading anything sourced from it, and before saying any part of it is unreachable. It carries the tab map, the five read paths in order, the four double-click tools that already exist on Patrick's PC, and the specific ways every previous session has misread this workbook.
---

# THE ATT FIBER LEADS SHEET — read it right or do not quote it

Workbook `1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA`, owner
`patricksiado@gmail.com`. ~772,768 rows across 29 tabs, 8.5 MB, at its
10,000,000-cell ceiling.

**Patrick, repeatedly:** *"every fuking time I ask for data from the sheet u read
it wrong upload or enrich wrong data."* Every one of those misreads is listed at
the bottom of this file. Read them before you answer.

---

## 1. THE TAB MAP — what is actually in there

**Hunter-owned. Never edit by hand, never read wholesale.**

| Tab | Rows | What it is | Dot |
|---|---|---|---|
| `Precise Fiber` | ~645k | every captured dot. **GREEN ONLY since 2026-08-26** | GREEN $500 |
| `Gold Confirmed` | 11,490 | **THE call list.** Has a header row. 79% is pre-08-24 contamination | GOLD $140 |
| `Grey Fiber Customers` | — | existing AT&T fiber customers. Penetration data, **never dial** | GREY |
| `Unknown Customers` | — | build code would not decode. **Not a lead** | — |
| `Gold Dots` | 3,328 | **RETIRED.** Contaminated. No header row. A=Address B=Captured At C=Lat D=Lng | — |
| `GOLD — CLEAN` | 3,328 | cleaned copy of the retired tab | — |
| `Beaumont Gold — Aug 2026` | 238 | market slice | GOLD |
| `Upgrade Orange Biz` | 62 | **gold BUSINESSES — the highest-value slice we own, and it is nearly empty** | GOLD |
| `Maps Businesses` | 38,481 | scraped businesses, unmatched to any dot | — |
| `Fiber Green Biz` | 7,298 | green businesses | GREEN |
| the UNDECODED tab | 225 | **all ZIP 77630 Orange, every Build Code EMPTY. NOT GOLD** | — |
| `TEST-Green-2026-08-24` | 13,027 | frozen snapshot, deletable | — |
| `_dispatch`, `_Dedupe Lock` | 0-1 | machine coordination | — |

**Three tabs that do not exist and never did:** `Enriched Leads`,
`New Fiber Alerts`, `Fiber Zones`, `Outage Signals`. Do not write code against a
tab without checking the live list.

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
3. **Quoting 11,490 as the gold count.** 9,052 of those are pre-2026-08-24
   gold-by-default decode failures. **The purge that removes them has never run.**
4. **Believing a tool failure means no access.** See section 2.
5. **Trusting the first tab.** `Precise Fiber` is tab #1 again, so the cheap read
   returns green apartment addresses instead of numbers. DASHBOARD and README
   were deliberately moved to the FRONT — **if they are not there, the order got
   tidied back and the read path is broken.**
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


## 7. THE LIVE TAB LIST — 29 tabs, MEASURED 2026-09-03 off `_feed/sheet/tabs.json`

`Precise Fiber` 645,422 · `Maps Businesses` 38,481 · `Grey Fiber Customers` 26,689 ·
`Backend Comm` 17,085 · `TEST-Green-2026-08-24` 13,027 · `Gold Confirmed` 11,490 ·
`Fiber Green Biz` 7,298 · `Hunter Status` 3,599 · `Gold Dots` 3,328 ·
`GOLD — CLEAN` 3,328 · `HOUSTON UNVERIFIED — Aug 19` 1,339 · `ZZ_TMP_GRID` 999 ·
`Beaumont Gold — Aug 2026` 238 · `TMP Sweep Census` 92 · `Backend Analysis` 65 ·
`Upgrade Orange Biz` 62 · `Backend Capture` 48 · `Gold Biz Campaign — READY` 45 ·
`Warm Backlog — Replied YES` 40 · `WORK LIST — Beaumont + Angleton` 29 ·
`Devonwood Campaign — Aug 21` 26 · `Angleton Call List — Aug 2026` 20 ·
`Operator Scorecard` 12 · `TEST-Gold-2026-08-24` 5 · `_dispatch` 1 ·
`_Dedupe Lock` 0 · ` _temp_ash_lookup` 0 · `_optimus_probe` 0 · `Territory Claims` 0

**THE GENUINE JUNK — 7 tabs, 17,451 rows:** `Gold Dots` (RETIRED, superseded by
`GOLD — CLEAN`), `TEST-Green-2026-08-24`, `TEST-Gold-2026-08-24` (migrate first),
`TMP Sweep Census`, `ZZ_TMP_GRID`, ` _temp_ash_lookup`, `_optimus_probe`.
Everything else is live or hand-built. **Plus 9,052 pre-08-24 rows inside
`Gold Confirmed`.**

**THREE TABS THIS SKILL AND CLAUDE.md BOTH NAME DO NOT EXIST:** `DASHBOARD`,
`README` and `Unknown Customers` are absent from the live list. The "read
DASHBOARD first" path cannot work until they are rebuilt.


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
| **Is the sheet GROWING (is capture landing)** | `get_file_metadata` on BOTH workbooks: `modifiedTime` AND `fileSize`. Flat size = nothing landing. Production `1FhO2…`, split `1DXu-…` | The console, `latest.json`, the heartbeat, `SUCCEEDED` |
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
