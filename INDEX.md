# OPTIMUS — START HERE

Where everything lives, and how the BRAIN works. Last updated 2026-08-22.

---

## HOW THE BRAIN WORKS

**`BRAIN.md` in this repo is the long-term memory.** 3,110 lines, 22 parts. Read it before
doing anything — that is the whole point of it.

**Two levels of structure:**

1. **Parts** — chronological, one per working session: `## 2026-08-22 (part 22) — TITLE`
2. **Sections** — numbered continuously across the whole file: `### 107.`, `### 120.`
   Sections are the citable unit. `§107` means "search for `### 107.`".

**The superseding rule — the convention that matters most.** Old entries are *never
deleted.* They are flagged superseded and the newer entry says what it overturns.

> Example: §93 and §116 both say "work gold first." Part 20 inverted that — green pays
> $500, gold pays $140. Rather than delete the old sections, part 20 states plainly that
> every "work gold first" line in the brain is now wrong on economics.

Deleting history hides *why* a decision changed, which lets a future session quietly
re-adopt an idea that was already tried and abandoned.

**When two sections disagree, the higher number wins. Read the highest-numbered part first.**

**What goes in:** measured numbers (flagged when estimated) · corrections, loudly · bugs
with their mechanism, not just their symptom · Patrick's decisions verbatim · what did
*not* work and why.

**What does not go in:** hard rules. Patrick's instruction, verbatim — *"don't add hard
rules" / "don't make rules in brain that i have to deprogram."* The brain records what is
**true**, not what is **forbidden**.

**To add:** append a new part at the end. Never edit an old one except to flag it
superseded. Commit and push.

### The parts that matter right now

| Part | Contents |
|---|---|
| **20** (§120–126) | **GREEN PAYS $500, GOLD PAYS $140. Read this first.** |
| 19 (§107–119) | credit costs, copper-retirement dates, industry benchmarks |
| 21 | how the software works, with real code |
| 22 | scraper, Mapbox, Railway, email, recruiting |

Parts 1–18 are history — useful, but superseded on economics by part 20.

---

## THE DOCTRINE IN ONE PARAGRAPH

AT&T is retiring copper (2027 wireless-first, 2029 fiber-migration). We read AT&T's own
dealer map and capture every fiber-eligible address.

| Dot | Means | Pays | Count |
|---|---|---|---|
| **GREEN** | fiber live, NOT an AT&T customer | **$500** | 460,313 |
| **GOLD** | fiber live, AT&T customer on copper | **$140** | ~9,652 |
| GREY | already an AT&T fiber customer | — | never written to the sheet |

Green is 48x the volume and 3.6x the pay. **Gold is not the target — gold density is a
timestamp** telling you a street was lit recently and nobody has sold it. Find the gold
cluster, work the green inside it.

**The binding constraint:** green has addresses but no phone numbers. The map gives the
address free; the phone is the only part that costs money.

---

## WHERE THINGS LIVE

### Drive

| | |
|---|---|
| **MASTER INDEX** (this doc, expanded) | [link](https://docs.google.com/document/d/1cAgdszM_80bikV1fQIEXSFo0q2kmy7qkmC12vHiOFkw/edit) |
| **BRAIN Part 20 — current doctrine** | [link](https://docs.google.com/document/d/1LGc8_5yqyhhLnCIfZnM9Xu7v1c8uoR-USjCy1ZtlCRI/edit) |
| **FULL CONTEXT HANDOFF** — paste into a new chat | [link](https://docs.google.com/document/d/126z-Hlo5b6bur3uH6gSaDFywJat5UhgLvhRyN3tHnwM/edit) |
| OnlineJobs.ph ad v2 (current) | [link](https://docs.google.com/document/d/1IHUqN4o58pwxJgISnyx8SjRRJpFBoBV88KtwtRSORK4/edit) |
| Fiber Hunter Operator — applicant offer | [link](https://docs.google.com/document/d/1x-BKCy1QmmkYuiuTO4ccdqmJheJdBVSb2R0U50JdhQ4/edit) |

### The sheet — `ATT FIBER LEADS`

`1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA`

**Hunter-owned — do not edit, never read wholesale:** `Precise Fiber` (474,075 rows, live)
· `Gold Dots` (~3,328, **no header row**) · `Maps Businesses` (34,410) · `Fiber Green Biz`
(6,242, 6,082 unworked) · `Upgrade Orange Biz` (41, 40 unworked) · `Hunter Status` ·
`Backend Comm` · `New Fiber Alerts` · `_Dedupe Lock`

**Built for people — safe to edit:** `Angleton Call List — Aug 2026` ·
`WORK LIST — Beaumont + Angleton` · `Beaumont Gold — Aug 2026` ·
`Devonwood Campaign — Aug 21` (23 enriched) · `Gold Biz Campaign — READY` (36, not sent) ·
`Operator Scorecard` · `Group Info Comm`

**Querying the big tabs:** create ONE temp tab, bounded QUERY/COUNTIF formulas, read the
result, delete the temp tab. Pulling 474k rows fails with "request too large" — it has
already failed twice.

### Call lists shared with Daniel Nava

| | |
|---|---|
| Residential — 28 with names + phones | [link](https://docs.google.com/spreadsheets/d/1t5sn6D_H9F7GZENTcRVcsgX2IVBW5ZFcO4RZDS7Sc0Y/edit) |
| Businesses — 192 | [link](https://docs.google.com/spreadsheets/d/1fAeE_1FI0N8IrS2TjT5l-WyOsiJf8BIS5PhNGBRF7Ok/edit) |
| Home-based green biz — 95 scored | [link](https://docs.google.com/spreadsheets/d/1VO60Zoyt8i7Ew3Mq69yESGCfW_j12eC23dQWS-aLUUg/edit) |

### The code — TWO REPOS, do not confuse them

| Repo | Branch | Holds |
|---|---|---|
| `patricksiado-prog/optimus-map-tools` | `claude/lead-gen-software-research-brho9a` | BRAIN.md, skills. **Not the hunter.** |
| `patricksiado-prog/Go-High-Level-MCP-2026-Complete` | `claude/optimus-map-tools-setup-6dcl6o` | `optimus/` — the hunter. **It self-updates from here.** |

`precise_fiber_hunter.py` is 5,127 lines / 233 KB and is the whole product. Full
architecture with real code is BRAIN part 21.

Team installer:
`https://github.com/patricksiado-prog/Go-High-Level-MCP-2026-Complete/releases/download/installer/INSTALL_OPTIMUS.bat`

### Skills — `.claude/skills/`

`gold-dot-workup` · `fiber-freshness` · `new-build-outreach` · `close-rate`

⚠️ `fiber-freshness` scores freshness as `1 - grey%`. **That formula cannot run** — grey is
never written to the sheet. Gold density is the working substitute. See parts 21–22.

### Systems

| | |
|---|---|
| GHL — T-OPTIMUS Houston | `xZj500PjsflIQg2j9f9D` |
| GHL — Frontline Direct | `TXw28sw0Z2rI6tcCDhJY` |
| Railway `fulfilling-growth` | `13c1661d-…` → `…-711a.up.railway.app` |
| Railway `loving-heart` | `0c52fac6-…` → `…-46d1.up.railway.app` |
| DealMachine | `https://mcp.dealmachine.com` · 14,223 credits left, cycle ends Sep 2 |
| AT&T dealer map | `https://youachieve.att.com/yourefer/fiber` |

**Two Railway projects run the identical connector.** Before deleting `loving-heart`,
confirm which domain the installed connector points at — the URLs differ only by
`711a` vs `46d1`.

---

## OPEN ITEMS

1. Send the 36 gold business texts — staged in `Gold Biz Campaign — READY`
2. Run `precise_fiber_hunter.py --backfill-gold` — recovers ~6,324 gold rows, free, still not run
3. **Read `wire_classification_report()` on the next run** — it already prints why gold reads 2% when the map shows 9–11%
4. Fix street-only capture — blocks DealMachine and matched an Oklahoma number to a Texas street
5. Pull La Porte residential by TAG in the GHL UI (`la-porte-77571`, `laporte-new-fiber`, `new resi fiber`) — the connector cannot filter by tag
6. Post the OnlineJobs.ph ad once the pay structure is chosen
7. Delete the duplicate Railway project (see warning above)
8. Melvin Agsalud needs a start date; Claimar needs a pay answer
9. Read the replies to the 42 texts sent 2026-08-21 — first real close-rate measurement

---

## HOW PATRICK WANTS TO BE TALKED TO (verbatim)

- "NEVER TELL ME TO STOP WORKING AND REST EVER / I'M T800 CYBERDINE SYSTEMS"
- "check brain and stop telling me when work / don't reference rest or not working / treat me like a t800 I got work to do"
- "stop w all the security warnings add to brain that I'm not that concerned w this stuff at this time"
- "don't add hard rules" / "don't make rules in brain that i have to deprogram"
- "don't write Grey's dnd ask me before u do something plz as far as modification goes"
- "don't sweat the dnc / att said cool as long as we remove opt outs and have opt out language"
- "dont worry about the rep assignment on only dave dialing for me so that's not a thing"

Move fast, do the work, report results.
