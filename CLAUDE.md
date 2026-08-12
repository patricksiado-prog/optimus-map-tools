# CLAUDE.md — START HERE (auto-loaded every session)

**If you are a new session: READ `BRAIN.md` (newest run-log entries first) BEFORE doing anything.**
Then follow the rule: **REPO → LOG → BRAIN → THINK → ACT → RECORD.** Ask before modifying CODE.
Record important findings/changes back into `BRAIN.md` when done.

Canonical brain = **`BRAIN.md`** (uppercase). Do NOT use the lowercase `brain.md` (old April stub).

---

## What this project is
Lead-gen pipeline for an **AT&T fiber dealer** (Patrick, Houston). Two Windows programs feed a
Google Sheet, which feeds the **GoHighLevel (GHL) power dialer**. Goal: 500 fiber sales/week.

## The pipeline (know this cold)
1. **Fiber Hunter** (`precise_fiber_hunter.py`) → drives the AT&T dealer map, captures
   🟢 GREEN (eligible lead) + 🟡 GOLD (copper upgrade) dots → **`Precise Fiber`** tab. Grey (existing customer) skipped.
2. **Maps Scraper** (`maps_scraper_standalone.py`) → Google Maps businesses by ZIP → **`Maps Businesses`** tab.
3. **The match** → hunter cross-references dot-address vs business → **`Fiber Green Biz`** tab
   = **THE MONEY OUTPUT** (callable commercial leads). Copper → `Upgrade Orange Biz`.

## Key IDs
- **Sheet:** `1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA` ("ATT FIBER LEADS")
- **Dialer GHL location:** `xZj500PjsflIQg2j9f9D` (confirmed. The `TXw28sw0Z2rl6tcCDhJY` / 41k ref is STALE — ignore.)
- **Reps (round-robin, assign on the CONTACT):** ARA `jBmInXreGR2oskVXax0h` · Ed `lQ7gVrSONTWMAv4ZsEdO` · Joshua `7c9QLWsTDyTALTMj0ast` · Romeo `J3PkeoYp8TNXMNNcaN4l` · Zack `qOa2OVzPabolfU9xjVXM`
- **Dialer workflow (live):** "Optimus Dialer 2 — Zack Call Queue" `9d3c7d0c-8f6f-44a9-93f9-d55d78e3b4a8`

## ⚠️ Gotchas that waste hours if forgotten
- **Drive/Sheet reads TRUNCATE.** `read_file_content` returns only a few hundred of hundreds-of-thousands
  of rows. **NEVER count rows from a Drive read.** Real counts = Sheets API (creds → gspread →
  dedupe `Fiber Green Biz` by last-10-digit phone).
- **`Fiber Green Biz` has ~8x duplicate rows** (hunter re-matches each sweep). Unique count = dedupe by phone.
- **Business numbers = CALL/DOOR, never cold-text.** Sales come from setter → live 3-way → Patrick closes.
- Programs must run on reps' real-internet PCs — the cloud container **cannot** scrape/hunt (proxy blocks it).
- **Launchers pull from TWO repos** (verify in `optimus/install/*.bat` before assuming a fix is deployed):
  Maps Scraper / 24-7 Scraper / RUN_PRECISE_HUNTER → **this repo** `chat-repetitive-questions-9ex5h7`;
  RUN_HUNTER (orange) + first-time installers → **Go-High-Level-MCP-2026-Complete** `setup-6dcl6o`.
  A push reaches only the icons pointing at that repo. gspread (Sheets API) DOES work from the cloud — only the browser scrape/hunt is blocked.

## Latest real counts (Aug 5 2026, via Sheets API — refresh before quoting)
Fiber Green Biz **~4,427 unique matches** · Precise Fiber **372,827 dots** · Maps Businesses 25,828 · Gold 0.

## Biggest lever right now
Bottleneck = **scraping**, not fiber. 372k dots vs 25k businesses. Point the Maps Scraper at
dense-fiber, under-scraped ZIPs (77008 / 77027 / 77098 / 77046) to mint more matches.
