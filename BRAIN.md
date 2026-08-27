# Optimus BRAIN

_Last updated: 2026-05-02 05:32:19 CDT_

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

> **Note (2026-08-22):** everything above this line predates 2026-05-02 and is
> largely stale. Current operating facts live in `CLAUDE.md`, which Claude Code
> loads automatically every session. This file is the long-form memory behind it.

---

# PART 22 — 2026-08-22 overnight session

Everything below was measured this session, not recalled.

## 22.1 The first real close-rate numbers

- **Aug 21 batch: 100+ SMS sent 13:06-18:11 CT. Zero replies. Zero opt-outs.**
  The 100 most recently active conversations in the location were all from that
  day and all outbound-last.
- The two threads that looked like replies were **business missed-call
  autoresponders** (Boost The Heights, Cleanzen). Read the message body before
  counting a reply; autoresponders read as engagement and are not.
- Location totals: 4,685 conversations, 11,650 SMS messages, ~7.9% of messages
  inbound.

## 22.2 The warm backlog nobody had read

- **22 contacts carry `replied-yes`. 7 were already unreachable** — 3 hard
  opt-outs (`STOP_KEYWORD`, permanent) and 4 DND'd by the STOP workflow. Two of
  the seven had also been tagged `hot-lead`.
- **15 were still reachable and none had ever been closed**, the oldest sitting
  since June 30.
- Staged to the tab `Warm Backlog — Replied YES` with call-first actions.

## 22.3 What the tag search can and cannot see

- `interested` returns 331 contacts — and `not interested` returns **the same
  331**. The `interested` tag has zero contacts on it. Same for
  `client is interested`, `wavv-interested`, `engaged and interested`.
- `hot-lead` = 3, `warm-chase-sent` = 10, both entirely inside the 22.
- `callback`, `appt booked`, `needs-followup`, `commercial-warm` = 0 contacts.
  A tag existing in the location's 617-tag list does not mean anything carries it.
- `search_contacts` `query` is **substring matching**, which is why "interested"
  catches "not interested". It has no tag filter.
- **The `replied-yes` tag is applied by a workflow that fires on a literal
  "YES".** Anyone who answered with anything else was never tagged and is
  invisible to every tag search. Confirmed examples found in raw message text:
  a contact who replied `77659` then `223 pinemont` (ZIP then street address),
  M & W Painting replying `1 internet only`, and two separate `Please text me.`
  Estimated 40-70 genuinely interested contacts across all history versus the
  22 tagged — tens, not hundreds.
- `lastMessageBody` holds only the most recent message, so anyone who replied
  and got answered shows as outbound-last. Scanning last messages will not find
  them.
- 3,305 open opportunities all sit in "Contacted" because the workflow creates
  one per outreach. Pipeline stage is not an interest signal here.

## 22.4 DealMachine, measured

- **`enrich_address` really costs 1-2 credits per address, not the ~6 in older
  notes.** 25 Devonwood addresses cost **39 credits** total, 100% match rate.
- **`enrich_address` and `enrich_latlng` have no `estimate_cost` flag**, unlike
  `property_search` / `people_search` / `enrich_name`. Probe one address and read
  `credits.used` before committing a batch.
- **`enrich_latlng` needs no ZIP.** Gold Dots carries lat/lng, so gold dots can
  be skip-traced despite their street-only addresses.
- **~12% of residential rows come back landline-only** with no wireless
  alternative. A 25-row list is not a 25-message send.

## 22.5 Connector behaviour worth not rediscovering

- `get_sms_reports` 404s — `/reporting/sms` is not available on this location.
- `search_conversations` caps at 100 with no offset, sorted last-message
  descending.
- `get_users` requires a companyId; `search_users` returns 401.
- `official_conversations_export_messages_by_location` works at 1000/page, but
  **`nextCursor` comes back static and pagination loops**. Use `startDate` /
  `endDate` windows instead.
- GHL holds **0 estimates**, so no quotes live there.
- Pipelines: AT&T Leads `2V9thfxQpuhn6ZP0Peqt`, AT&T Commercial
  `trc5dwodtc1LBYHikmiK`.
- Workflow `Optimus Dave` has `triggers: []` — manual enrollment only, call
  windows Mon-Fri 09:00-17:00. That is what makes it safe to enroll a batch into.

## 22.6 Calendars and booking

- **All 27 pre-existing calendars were inactive**, so no appointment could be
  booked at all.
- Created **`Optimus Fiber Appointments`**, id `jSOOC383RNxHIRwo6zV8`, active,
  30-minute slots.
- **Booking still fails until open hours are set in the GHL UI.** Tested:
  `get_free_slots` returns nothing and `create_appointment` fails with "The slot
  you have selected is no longer available" even with `ignoreDateRange: true`.
  The MCP `update_calendar` has no open-hours parameter, so this is a one-time
  manual step in the interface.

## 22.7 Quotes

- No customer quotes exist in 2026 email; the real ones are 2025.
- Searching `from:` Patrick's own address misses system-generated quotes.
- Seven quotes sent, none showing a close. **Hub 92 Prints (Feb 2025) asked "Can
  you send me the full quote for both please" and "does that quote include the
  insurance?" and the thread ends with no reply** — $325/mo all-in, saving them
  about $300/mo.

## 22.8 Environment limits hit this session

- **`send_later` / scheduling denied by the auto-mode classifier**, second
  session running. A morning send cannot be queued from inside a session.
- **Routines created via `create_trigger` carry no MCP connectors**, so the
  sessions they fire have no GHL, DealMachine or Sheets access. Connectors have
  to be attached from the claude.ai Routines UI.
- Reddit is blocked to the web crawler. Public AT&T announcements report at
  "725,000 locations / 38 neighborhoods" granularity — too coarse to aim a sweep.
  Our own gold density is finer than anything published.

## 22.9 The supply-vs-conversion picture

Lead supply is not the constraint: 2,461 untapped Houston green businesses
(blank status, phone present), 3,328 gold dots, 474k Precise Fiber rows. Against
that, the Aug 21 batch converted zero, 15 people who said yes were never called,
and 7 more opted out while waiting. The sales log shows 889 orders across
Apr 2023 - Jul 2025 (446 / 280 / 163 by year), roughly one a day.

Caveat on the 2,461: an 80-row sample was heavily apartment complexes, national
chains, toll-free numbers and office-tower LLCs. DealMachine returns no contacts
for LLC-owned commercial property, so the workable small-business count is well
below the headline number.

## 22.10 Built this session

- `.claude/skills/gold-cluster-sweep/` — SKILL.md plus
  `scripts/find_clusters.py`. Covers backlog dig, cluster finding, enrichment,
  filtering, text/email/dialer, booking, follow-up cadence and a cluster queue.
- `intel_banner()` in `precise_fiber_hunter.py` — prints open outages and
  suggested new-build ZIPs at every hunter opening. Committed as 85ac42a on
  branch claude/new-session-8z4pyb of the hunter repo but **not pushed**, because
  precise_fiber_hunter.py is in `_CORE_FILES` and pushing auto-deploys to every
  hunter PC.
- Sheet tabs: `Warm Backlog — Replied YES` (15 workable, 7 lost, 7 open quotes)
  and the enriched `Devonwood Campaign — Aug 21` (20 READY, 5 BLOCKED).

## 22.11 Sending numbers — the real ceiling on volume

The location owns **three** numbers, and all outbound has been going out on one:

| Number | Title | Use |
|---|---|---|
| `+1 361 301 9563` | Patrick's number 2 | Every send — Aug 21 batch AND the Aug 22 batch |
| `+1 346 536 3161` | Patrick's number 4 | Idle |
| `+1 346 615 4219` | Patrick's number 3 | Idle |

100/day from a single 10DLC is where carrier filtering starts; split across the
three it is ~33 each and unremarkable. Spreading the load is the cheapest thing
available to make a 100/day target actually deliver.

Observed 2026-08-22: a manual batch of ~30 went out in **116 seconds** from that
one number, all with the same body and only a rotating opener. Identical bulk
text at burst rate is the pattern carriers filter on.

## 22.12 GHL workflow API — actions save, triggers do not

`ghl_create_workflow` with a trigger fails with a Firestore error
(`5 NOT_FOUND: No document to update: .../triggers/<id>`) and leaves an empty
workflow shell behind. `ghl_update_workflow_actions` saves **actions** fine —
including a `wait` with a `window` (days + start + end), which is how a send is
held until a time of day — but passing `triggers` returns "updated successfully"
and writes nothing. Verified by reading the workflow back: `triggers: []`.

So a scheduled auto-sender can be built through the API right up to the trigger,
and the trigger has to be added by hand in the GHL UI. Always read a workflow
back after writing it; the success message is not evidence.

## 22.13 Home-based business categories are the enrichable ones

The Maps scraper's combo match (317,084 captured fiber leads vs 34,410 scraped
businesses) yields 6,242 green biz rows, 41 orange, and **3,850 callable matches
with a unique phone**.

The categories that matter are the home-based trades and services — home
daycare, notary, maid service, window cleaning, lawn mowing, gutter cleaning,
chimney sweep, tutoring, home organizer, carpenter, masonry, septic, insulation.
Those skip-trace to a real owner record with a cell for ~2 credits. Office-tower
and LLC-held businesses return `contacts: []` and are where credits get wasted;
an 80-row sample of the "untapped Houston" pool was mostly apartment complexes,
national chains, toll-free numbers and Greenway Plaza suites.

## 22.14 Gold Dots audit — what the tab is actually made of (2026-08-23)

Patrick: *"I wanna clean up our gold dot list make sure it's accurate so verify
pleaee / im suspicious of it / don't mind if we have to rescan but want good data
accurate data."* He is right to be. Six findings, all reproducible from the repo.

**1. The gold rule changed mid-history, and the tab holds rows from both rules.**
`classify_wire()` in `precise_fiber_hunter.py` used to send a customer with an
*unrecognised* build code to GOLD. It now sends that customer to GREY. Rows
captured before the change are therefore contaminated with existing fiber
customers — the exact thing Patrick hit when he clicked a gold dot and got a
customer already on fiber. The tab has no column that says which rule wrote a
row, so the bad ones cannot be picked out in place.

**2. The docstring above `classify_wire()` still describes the OLD rule.** It
says "every other customer is a copper-upgrade GOLD" directly above code that
returns grey for that case. Anyone reading it will re-introduce the bug. Fix the
comment, not the code — the code is right.

**3. `backend_classifier.py` ships with EMPTY code tables.**
`FIBER_BUILD_CODES = set()` and `COPPER_BUILD_CODES = set()`, and nothing in that
file ever reads `build_codes.json`. Every customer comes back `CUSTOMER`, so that
module **can never emit GOLD**. `fiber_scout.py`, `zip_reader.py` and
`verify_gold_capture.py` all import it. Proof: running
`verify_gold_capture.py _live/serviceability_raw.json` reports `fttp-gpon` as an
"undecodable" build code — a code that is sitting in `build_codes.json`. The
hunter has its own classifier that does load the JSON, so Gold Dots itself is not
zeroed; but any gold figure produced by the scout path is fiction.

**4. `IP-CO` is a live build code in neither list.** 9 of 105,500 records in
`_live/backend_analysis.txt`. Real gap, negligible volume — it cannot explain any
gold shortfall. Confirm one on the map before adding it; guessing into the money
path is how the last bug happened.

**5. The dedupe skips row 1.** `_ensure_gold_tab()` seeds its `seen` set with
`gw.col_values(1)[1:]`, which assumes a header row. The live tab has **no header
row** (verified 2026-08-22). So row 1 is a real address that is never in `seen`
and gets re-appended on every run that captures it.

**6. The writer and the tab disagree on shape.** `write_gold_dots()` writes eight
columns — Address, Captured At, Lat, Lng, Business, Phone, Run ID, Operator — and
expects a header. The live tab has four populated columns and no header. The
existing 3,328 rows therefore carry **no Run ID and no Operator**: there is no
provenance on any of them.

**The volume check says the same thing.** In the 105,500-record capture in
`_live/backend_analysis.txt`: 62,942 non-customers (green) and 42,558 customers,
of which 42,456 are FTTP-GPON (99.76% already on fiber → grey) and 93 are copper
(gold). Gold is 0.088% of dots; green:gold is about 677:1. Against 481,576 green
in Precise Fiber the current rule predicts roughly **711** gold. The tab holds
**3,328** — about 4.7x more. That over-count is consistent with finding 1 and is
the quantified version of Patrick's suspicion.

**Error runs both ways.** `BACKEND_LEAD_CAP = 3000`: AT&T silently truncates a
"Search this area" reply at ~3,000 leads, so dense viewports lose addresses with
no error raised. Gold is over-counted historically and under-captured in dense
ground at the same time.

**Conclusion: the 3,328 rows cannot be audited in place** — no provenance, no
rule stamp, no header. They can only be re-verified against AT&T. Rebuild beats
clean-up.

**Also true, and separate from any bug: the scanned territory is genuinely
fiber-saturated.** 99.76% of AT&T customers in the captured data are already on
FTTP-GPON. Gold really is rare where we have been scanning. 77019 (River Oaks) is
long-converted ground — matching the team's own guidance: lots of grey = old
area, already worked over, move on.

## 22.15 The day capture died silently — what broke, what I got wrong (2026-08-23)

A full day was spent chasing a gold-classification bug that was not a
classification bug. Writing the whole thing down, including the wrong turns,
because the wrong turns cost more hours than the fix did.

### The actual defect: two paths that threw AT&T's answer away without a word

`precise_fiber_hunter.py`, the serviceability response handler:

1. **Non-200 replies** logged one console line and returned. A 301 bounce to
   login printed `(serviceability reply 301 -- skipping, map keeps moving)`,
   which scrolls past in a fast sweep and is persisted nowhere. The file's own
   comment had predicted this exact failure and it happened anyway.

2. **A 200 whose body is not JSON** hit a bare `except Exception: return`.
   Nothing counted, nothing logged, nothing said.

AT&T's login page returns **200 with an HTML body**. So `json.loads` threw, the
response evaporated, `svc_seen` never incremented, and every cell reported
`+0 (total 0)`. The run then reported "no serviceability responses seen".

**The tell was that GREEN and GOLD died together.** A classifier fault produces
one colour or the wrong colour. Losing every colour at once means nothing is
reaching the classifier at all — the failure is upstream, in delivery.

### Why it looked like a classification problem

The map kept drawing green and orange dots the whole time. That is not proof the
feed is alive: dots already rendered stay on screen, and a fresh
`Search this area` can fail without clearing them. **Seeing dots proves nothing
about whether capture works.**

### Wrong turns, so nobody repeats them

* **"The dots come from Mapbox tiles, the API is separate."** Wrong. The July
  endpoint inventory (`_live/net_endpoints.txt`) lists only Mapbox *base map*
  tiles — terrain and streets. The dots are drawn client-side from
  `fiberMap.cfc` JSON. One source, not two.
* **"The response is too small, it must be an error page."** Wrong reasoning.
  The working July run returned **5,713 bytes** and decoded **500 leads** — the
  bodies are gzipped, so byte size says almost nothing. Today's failing response
  was 7,593 bytes, i.e. *larger* than a known-good one.
* **"83d2137e is not one of my builds."** Wrong: compared with sha1 when
  `_file_stamp()` uses **sha256**. Always hash the way the tool hashes.
* **Predicted the row-1 dedupe bug would show as duplicate rows in Gold Dots.**
  It did not — the exported 3,328 rows contain **zero** duplicates. The code
  defect was real; the damage was not there.

### What the session token research says

`_live/backend_exchange.txt` holds the real request:

```
GET /yourefer/api/fiberMap.cfc?method=getMapData&lon=..&lat=..
    &attuid=zg431x&csrfToken=CD619C0F...
RESP: 200  text/html;charset=UTF-8
```

Every call carries a **csrfToken** and an **attuid**, both session-bound. When
they go stale AT&T answers 200 with a login page rather than an error code. The
endpoint is declared `text/html` but really serves JSON, so content-type sniffing
cannot tell data from a login wall — **parse it as JSON first, then decide.**

### Fixed

* Both silent paths now print a loud banner naming the cause and the remedy, and
  publish it to the feed.
* `optimus_feed.py` — every run pushes counts, undecoded build codes with sample
  addresses, dedupe/verification totals, and up to 300 records **with their
  build code** to `optimus/_feed/latest.json`. Screenshots of a console can not
  carry `curr_ntwrk_bld_type_cd`; this can. The subscriber BAN is published as a
  boolean only, never the account number.
* `diagnose()` returns a plain-English verdict for six cases: login page,
  `success:false`/403, valid-but-empty, renamed fields, records that *do* parse,
  and not-JSON-at-all.

### Standing rules this produced

* **A silent zero is a bug, not a result.** Any path that drops a response must
  say so on the console AND in the feed.
* **Never diagnose from a console photograph.** Push the evidence to GitHub and
  read it.
* **Dots on screen are not proof of capture.** Only a non-zero `+N` is.
* **Before blaming classification, check whether anything arrived.** Green and
  gold failing together always means delivery, never classification.

## 22.16 Five candidate solutions, written for outside review (2026-08-23)

Written to be argued with. Each option states what it is, the evidence behind
it, what it costs, how it fails, and how we would know it worked. They are not
mutually exclusive; the recommended order is at the end.

Shared facts every option has to respect:

* The dealer map is **Mapbox GL JS**. The dots are GeoJSON features inside the
  page's map object. The hunter already hooks `mapboxgl.Map` at page-init
  (v0.5) and can call `queryRenderedFeatures()`. Pixel detection exists only as
  a fallback and is OFF (`ALLOW_CLICK = False`).
* The address data comes from `GET /yourefer/api/fiberMap.cfc?method=getMapData
  &lon=..&lat=..&attuid=..&csrfToken=..`, declared `text/html` but serving JSON.
* AT&T caps a reply at **500 records** (measured; the code carried 3000 for
  months and the truncation guard therefore never fired).
* The classifying field is `curr_ntwrk_bld_type_cd`. `fttp-gpon` = fiber/GREY,
  `fttn-bp`/`ip-rt` = copper/GOLD, `unavailable` is extremely common and decodes
  to neither.
* A live popup on a confirmed gold dot reads
  `Status: Existing Copper Customer`. That string does **not** appear anywhere
  in the wire payload — it is rendered client-side.

---

### Solution 1 — Make the session self-healing

**What.** Detect a dead API session and recover without a human. Watch for the
three signatures — non-200 redirect, `success:false`, and a 200 whose body is
HTML — and on any of them re-navigate the login flow, let the page mint a fresh
`csrfToken`, then resume the sweep from the cell that failed.

**Evidence.** `backend_exchange.txt` proves every call is session-bound. Today
every cell returned `+0` while the map still showed dots, which is what a dead
session plus a live tile cache looks like.

**Cost.** Small. The detection already exists as of `cb915e1d`; this adds the
recovery arm.

**How it fails.** If AT&T requires interactive MFA the re-login cannot be
automated, and the honest outcome is a loud stop rather than a silent one. Also
risks a login loop if the failure is not actually auth — needs a hard cap of one
retry per run.

**Verified when.** A run that hits a stale session recovers and continues, and
the feed shows a resume rather than a zero.

---

### Solution 2 — Second capture path via `queryRenderedFeatures()`

**What.** Read the dots from the map object instead of the network. Promote the
existing v0.5 hook to a first-class path: on each viewport call
`queryRenderedFeatures()`, take each feature's geometry (exact lng/lat) and
properties, and emit records without touching `fiberMap.cfc`.

**Evidence.** The hook is already written and has ~20 call sites. The map cannot
draw a dot it does not have, so **anything visible on screen is queryable.** This
is the only option that is immune to a stale API session.

**Cost.** Medium. The hook exists; what is unproven is whether the features carry
usable properties.

**How it fails.** The features may carry only a colour and a geometry with no
address and no `curr_ntwrk_bld_type_cd`. Then it yields position and colour but
not the classifying field — useful for *finding* gold pockets, not for building
a callable list. Also bounded by `maxzoom`: above the layer's max the layer is
hidden and returns nothing.

**Verified when.** One run dumps the property keys of a single dot feature. That
single dump decides whether this is a full replacement or only a locator.
**This is the cheapest unknown to close and should be done first.**

---

### Solution 3 — Call the API directly, drop the browser button

**What.** Harvest `csrfToken` + `attuid` + cookies once from the live session,
then issue `fiberMap.cfc` requests ourselves over a lat/lng grid. No
"Search this area", no panning, no waiting on the map to paint.

**Evidence.** `backend_exchange.txt` documents the exact request. Every failure
today was in the browser-driven path: the button not being found, cells panning
over empty ground, responses cancelled mid-pan.

**Cost.** Medium. The request shape is known; the work is grid planning, cookie
handling and pacing.

**How it fails.** Rate limiting (the code already knows 429), and the 500-record
cap means the grid must subdivide wherever a reply comes back at exactly 500 or
ground is silently lost. It also drops any evidence that only exists in the
rendered popup. Tokens still expire, so it depends on Solution 1 for longevity.

**Verified when.** A scripted grid over Prestonwood Forest returns the same
addresses as a manual sweep, with no reply landing exactly on 500.

---

### Solution 4 — Store observations, classify separately

**What.** The hunter writes an immutable observation per dot — address, lat, lng,
captured_at, ban_present, raw build code, run_id, scanner_version,
classifier_version — and classification becomes a separate pass over that store.

**Evidence.** The 3,328 gold rows cannot be audited because they carry no build
code and no rule stamp. The rule changed on Aug 20 and there is no way to tell
which rows came from which rule. When `IP-CO` or `unavailable` is finally
decoded, this is the difference between reprocessing a file and re-driving half
a million addresses.

**Cost.** Medium-high, and it touches the sheet schema — the highest-risk edit.

**How it fails.** The sheet is the team's UI; a schema change that breaks their
view is worse than the problem. Mitigation: additive columns only, written by
name against the live header (already implemented in `cb915e1d`), never by
position.

**Verified when.** A build code can be reclassified and the existing rows update
without a single new AT&T request.

---

### Solution 5 — Re-verify the existing 3,328 by coordinate

**What.** Do not rescan and do not discard. Every legacy gold row has lat/lng.
Push those coordinates back through AT&T and re-read each one, writing
VERIFIED_GOLD / GREY / UNKNOWN into a fresh output while `GOLD_UNVERIFIED_LEGACY`
is preserved untouched.

**Evidence.** 3,328 rows, **zero duplicates**, **100% carry lat/lng** — verified
against the export. Two of two spot-checked rows came back customers with no
copper status, and the one confirmed gold dot found by hand (8211 Coolshire) is
**not in the list at all**. So the list is both contaminated and incomplete.

**Cost.** Low relative to a rescan — 3,328 lookups against ~500 per reply.

**How it fails.** Depends on a working API path, so it is gated on 1 or 3. And
if `unavailable` is never decoded, a large share lands in UNKNOWN and the
exercise only partly pays.

**Verified when.** Every legacy row carries a verdict and a build code, and the
gold count agrees with what is visibly orange on the map.

---

### Recommended order, and why

1. **Solution 2's property dump** — one run, closes the biggest unknown, decides
   whether an API-independent path exists at all.
2. **Solution 1** — nothing else survives a session that dies mid-sweep.
3. **Solution 3** — only if the browser path stays unreliable after 1.
4. **Solution 4** — before any large rescan, or the same un-auditable data is
   simply regenerated at scale.
5. **Solution 5** — last, because it consumes whichever capture path wins.

### The question none of the five answers

**What build code does a confirmed copper customer return?** 8211 Coolshire
reads `Status: Existing Copper Customer` in its popup. Until its
`curr_ntwrk_bld_type_cd` is known, `unavailable` cannot be judged — and
`unavailable` is the most common value in the data. Called gold it produces the
contaminated 3,328; called grey it may be discarding every real upgrade lead.
**One captured record from that address settles it, and every option above is
worth more after that answer than before it.**

## 22.17 The UNKNOWN bucket — Patrick's proposal, and why it beats all five above (2026-08-23)

Patrick, after reading 22.16: *"that doesn't make sense — u can detect green,
can u detect gold? why can't u print them to sheet"*

He was right and 22.16 was overbuilt. The answer is one paragraph, not five
options.

### Why green never fails and gold does

They come from the same response, the same code, the same instant. They are not
detected the same way:

* **GREEN is detected by ABSENCE.** `subscriber_ban` empty -> green. Nothing has
  to match anything. It essentially cannot fail.
* **GOLD is detected by a MATCH.** Customer AND `curr_ntwrk_bld_type_cd` must
  appear in the copper list (`fttn-bp`, `ip-rt`, ...). Miss, and it falls
  through.

AT&T's most common build code is **`unavailable`**. It is in neither list. So a
customer carrying it matched nothing and was filed GREY — **and grey is dropped
before the write path, so it never reached the sheet at all.**

That is the whole asymmetry. Green survives because it is defined by a missing
field. Everything ambiguous was deleted.

### The proposal: stop deleting what we cannot decode

A customer whose build code we cannot decode is **not** a confirmed fiber
customer. Calling it GREY asserts something we do not know, and the assertion
costs the row its existence. So:

| Dot | Before | Now |
|---|---|---|
| No BAN | GREEN -> sheet | GREEN -> sheet |
| Customer, `fttp-gpon` | GREY -> deleted | GREY -> deleted (correct) |
| Customer, `fttn-bp` | ORANGE -> gold tab | ORANGE -> gold tab |
| **Customer, `unavailable`** | **GREY -> deleted** | **UNKNOWN -> sheet** |
| Customer, `ip-co` | GREY -> deleted | UNKNOWN -> sheet |

`UNKNOWN` rows land in Precise Fiber with `UNKNOWN` in the Dot Color column.
They are **not** on the call list and **not** in the Gold Dots tab. They are
visible, countable, and inspectable.

Implemented as `OPTIMUS_UNKNOWN_CUSTOMER`, now defaulting to `unknown`:
`gold` = the original rule that produced the contaminated 3,328;
`grey` = the rule that silently deleted them; `unknown` = write them out.

### Why this is better than any of 22.16's five

Every option in 22.16 was a way to get *more* data. This is about not throwing
away the data already arriving. Three consequences:

1. **`unavailable` becomes measurable.** Right now nobody knows whether it means
   copper or fiber. Once the rows exist, clicking ten of them settles it — and
   if they are copper, one line in `build_codes.json` converts the whole bucket
   to gold retroactively.
2. **It removes the guess.** Both prior settings asserted something unproven:
   gold-by-default put fiber customers on the call list, grey-by-default may be
   discarding every real upgrade lead. UNKNOWN asserts nothing.
3. **A category that gets deleted can never be debugged.** That is the general
   lesson and it is worth more than the specific fix.

### The standing rule

**Never delete a record to express uncertainty.** Write it with an honest label.
Deletion is a claim of knowledge — it says "this is worthless" — and here that
claim was wrong for the most common value in the dataset.

### Open question for review

Does `unavailable` mean copper, fiber, or "AT&T does not know"? 8211 COOLSHIRE
LN reads `Status: Existing Copper Customer` in its popup and is **not** in the
gold list, which suggests at least some `unavailable` rows are real copper. Not
proven. The UNKNOWN bucket is what makes it provable.

## 22.18 Silence is the disease — three variants in one day (2026-08-23)

Written for review. The gold classifier was never the problem. **Every hour lost
today went to a capture path turning a real condition into silence**, and there
were three separate instances of the same defect in the same file.

### Variant 1 — a non-200 that only printed a line

```python
print("  (serviceability reply %s -- skipping, map keeps moving)" % st)
return
```

AT&T bounces a stale session to login with a 301. That line scrolls past in a
fast sweep and is persisted nowhere. The file's own comment had predicted this
exact failure — *"this print is how 'serviceability reply 301' stayed
invisible"* — and it happened anyway, because a comment is not a mechanism.

### Variant 2 — a 200 whose body is not JSON

```python
try:
    body = response.body()
    data = json.loads(body)
except Exception:
    return          # <-- nothing counted, nothing logged, nothing said
```

**AT&T's login page returns HTTP 200 with an HTML body.** `json.loads` throws,
the response evaporates, `svc_seen` never increments, and the run reports "no
serviceability responses seen" — the opposite of what happened. Every cell reads
`+0`.

### Variant 3 — a prompt that waits forever

```python
input("  Map on the right spot? Press Enter to START scanning... ")
```

A bare `input()` blocks indefinitely. If that window does not hold keyboard
focus — trivially easy, since the operator has just been clicking the map — the
sweep never begins. **Six launches in one afternoon reported in with all-zero
counts. Not one had actually started.** Nothing anywhere said "waiting for a
keypress."

### The shared shape

| | Real condition | What the operator saw |
|---|---|---|
| 1 | Session redirected to login | a line that scrolled away |
| 2 | Session returned a login page | `+0 (total 0)` |
| 3 | Never started | `+0 (total 0)` |

All three are indistinguishable from **"this neighbourhood has no fiber."** That
is why five hours went into the classifier: the evidence said empty ground, and
empty ground is what a dead session, a dead parse and a never-started sweep all
look like.

### Fixed

* Non-200 and non-JSON both print a loud banner naming the cause **and the
  remedy**, and publish it to `optimus/_feed/`.
* `diagnose()` returns a plain-English verdict across six cases: login page,
  `success:false`/403, valid-but-empty, renamed fields, records that do parse,
  and not-JSON-at-all.
* The start prompt auto-starts after 45s (`OPTIMUS_START_WAIT`), starts
  immediately with no interactive console, and — importantly — the fallback path
  no longer calls `input()`, which would have preserved the original bug.

### The rule

**Never convert a transport error, an auth failure, an unready map, an
out-of-range zoom, a broken hook, a parse failure, or a missing keypress into
`+0 dots`.** A zero is a claim about the world. It may only be reported after
the system has proven the observation was actually valid — session alive,
response parsed, sweep started. Anything else is `INVALID_ZERO` and must say so.

This is the same principle as 22.17's UNKNOWN bucket, one layer down: *do not
let uncertainty wear the costume of a result.*

### Still open

Whether green and gold capture again. **No sweep completed on 2026-08-23**, so
none of the above is proven in the field — only in tests. Green is definitely
alive: Precise Fiber went from 481,576 to **496,512** during the day. The next
completed run is the first real evidence.

## 22.19 The backend diagnostic — the tool reports its own health (2026-08-23)

Patrick: *"create backend feedback u need to diagnose the issue not me."*

Correct instruction, and it is the fix that makes 22.18 stop repeating. Three
silent-failure variants were found in one day. Finding a fourth by asking the
operator to photograph a console is not a method.

### What it does

`capture_diagnostic(page)` runs **before a single cell is swept** and publishes
to `optimus/_feed/latest.json` under `capture_diagnostic`, where any future
session reads it directly — no screenshots, no sheet, no Autosheet credits.

It answers, in one call:

| Question | Field |
|---|---|
| Is the `mapboxgl` hook alive? | `hook_installed`, `maps_hooked` |
| Did we capture the real map object? | `map_captured` |
| Is the style loaded, is the map ready? | `style_loaded`, `map_loaded` |
| Where are we? | `zoom`, `center` |
| Which layers can carry dots? | `candidate_layers[].id / type / source / source_layer` |
| **What is each layer's zoom band?** | **`minzoom` / `maxzoom` per layer** |
| Is it actually visible? | `visibility`, `circle_color` |
| How many features does it return NOW? | `rendered` per layer + a sample feature's property keys |

Then it renders a verdict: `HOOK_MISSING`, `MAP_NOT_READY`, `ZOOM_OUT_OF_BAND`,
`NO_DOT_LAYERS`, `ZERO_RENDERED`, `MAPBOX_OK` — and derives a **safe capture
zoom** from the live layers rather than a hardcoded guess:

```
safe_zoom = (max(minzoom of in-band layers) + min(maxzoom of in-band layers)) / 2
```

Console output is one block:

```
[HUNTER DIAG] mapbox=ZOOM_OUT_OF_BAND  zoom=17.1  layers_in_band=0
              every dot layer is outside its zoom band at z=17.1 --
              a zero here is INVALID, not empty ground
              safe capture zoom ~ 13.5
```

### The zoom band, and why it belongs here

A Mapbox layer above its `maxzoom` is **hidden**, so `queryRenderedFeatures()`
returns zero. That zero means *"you cannot see this from here"* — not *"there is
nothing here."* The hunter has read and printed those thresholds since v0.5 and
**never acted on them**. Recording a constraint is not enforcing it.

This is the same disease as 22.18's three variants, one layer up the stack:
a real condition (layer hidden) rendered as a result (`+0 dots`).

It also means auto-hunt zooming in "for precision" is actively harmful.
Feature geometry already carries exact lng/lat — extra zoom buys no accuracy
and can push the layer out of its band. **Geographic precision and layer
visibility are separate concerns.**

### Why this is the load-bearing change

Everything else built on 2026-08-23 was a fix for a specific bug. This is a fix
for *how bugs get found*. The cost of the day was not any single defect — it was
that each one had to be discovered by a human photographing a terminal and a
model guessing from the photo. Wrong guesses made along the way, all avoidable
with this in place: a two-source theory that the endpoint inventory disproved,
reasoning from gzipped byte sizes, and hashing with sha1 when the tool uses
sha256.

### The standing rule

**A tool that cannot report its own health cannot be debugged remotely.** Any
capture path added here ships with a diagnostic that states, without
interpretation: was the precondition met, was the observation valid, and if not,
which precondition failed.

### Still unproven

No sweep completed on 2026-08-23, so the diagnostic has not yet run in the
field. First completed run is the first real evidence — and it should answer,
in one shot, whether the Mapbox hook is alive, whether the map sits in a usable
zoom band, what the dot layers are named, what properties their features carry,
and whether AT&T's API answered at all.

## 22.20 It was the login page. Eight empty reports, one cause (2026-08-23)

**The answer, confirmed from the field.** A photo of the hunter's own browser
showed `youachieve.att.com/yourefer/fiber/` sitting on **"Choose your method of
access — AT&T Employee / AT&T Retiree/Affiliate with login / without login."**

Not the fiber map. The access chooser. The session was logged out.

Everything follows from that. The hunter loaded the URL, got a 200, carried on
as though it were on the map, never issued a `fiberMap.cfc` request, captured
nothing, and reported a clean zero. Eight runs today, eight identical empty
reports, one cause — and none of the eight said the word "login."

### What the reports were actually telling me

Every run today published this:

```
delivery      null      raw_features  null      rendered  null
classified    0         written       0         diag      {}
```

`null` is not `0`. `null` means **never measured**. Every boundary counter I
built lives INSIDE the sweep, so a run that dies before the sweep starts trips
none of them. The reports were not describing a broken sweep — they were the
sound of no sweep at all, and I read them for hours as if they were data.

Worse, `first_failure()` returned **`classified`** on every one of them, because
`classified=0` was the first measured value and nothing upstream contradicted
it. The tool I built to stop me guessing pointed confidently at the wrong file.
A diagnostic that answers when it has no evidence is worse than one that stays
quiet: I trusted it.

### The three fixes

1. **`_logged_in(page)` — refuse to sweep a login page.** Checked positively
   (is the map canvas there?) and then negatively (does the body carry
   `choose your method of access`, `at&t employee`, `global logon`, `user id`?).
   Either test alone is fooled: the portal landing page has no map but is not a
   login, and a slow map render is not a logout. A logged-out run now prints the
   problem in block capitals, waits **10 minutes** for the sign-in (password plus
   MFA on a phone is not a 60-second job), and **stops** rather than sweeping a
   login page and reporting zero. Tested against the exact chooser text from the
   photo, a Global Logon form, a live map, the portal landing, and an unreadable
   page — 5/5.

2. **A phase breadcrumb, pushed live.** `optimus_feed.phase()` stamps every
   startup milestone — `start, browser_up, page_loaded, sheet_open,
   resume_loaded, wait_done, diag_done, sweep_start, pass_done, exit` — and
   pushes each one to `optimus/_feed/heartbeat.json` as it happens. Pushed, not
   buffered: the whole point is to survive a run that never reaches its own exit
   report. A hung or force-quit run now names the last thing it did. The exit
   report also lists what was **NEVER REACHED**.

3. **The diagnostic stops guessing.** `first_failure()` will not blame a
   boundary when nothing upstream was ever measured, and `truth_report()` now
   calls an all-null run **"THE SWEEP NEVER RAN"** instead of **"HEALTHY."**
   Seven scenarios tested, including today's — it no longer accuses the
   classifier.

### The lesson, and it is not the one from 22.18

22.18 said silence is the disease. This is the sequel and it is nastier: I
replaced the silence with a **confident wrong answer**. Three separate times
today I reasoned from an all-zero report toward a bug in the classifier, the
writer, the zoom band — and the run had never opened the map.

So: **a measurement that was never taken must never be reported as a
measurement.** `null` and `0` are different facts and code that conflates them
will send the next person to the wrong file, fast and with conviction. Check
liveness before correctness — before debugging what a tool produced, prove it
ran at all.

And the cheap check I skipped for a full day: **look at the screen.** One photo
of the browser answered what eight telemetry reports could not.

## 22.21 Gold capture — the fix, and why green never had this problem (2026-08-23)

**The asymmetry, stated plainly.** Green is detected by an **absence**: no
`subscriber_ban` means a non-customer, and that test never fails. Gold is
detected by a **match**: `curr_ntwrk_bld_type_cd` has to appear in the copper
list in `build_codes.json`. So green captures ~496k rows and gold captures
almost nothing — not because the sweep misses gold dots, but because it cannot
name what it caught.

**The hinge is one value: `unavailable`.** It is AT&T's most common build code
and it is in **neither** list. Every customer carrying it falls through to a
guess, and both guesses have now failed in production:

| Guess | What it did |
|---|---|
| `gold` | Put existing FIBER customers on the call list. Patrick clicked a gold dot and got somebody already on fiber. Produced the contaminated 3,328 rows. |
| `grey` | Deleted them. Grey never reaches the sheet, so real $140 upgrades vanished with no trace. |

Two wrong answers to a question nobody had actually looked up.

### What was built

1. **`Gold Recheck` tab.** A real CUSTOMER on an undecodable build code is now
   **written**, with its build code, instead of dropped. Its own tab — so
   `Gold Dots` stays confirmed-only and nothing unconfirmed can reach a rep.
   It also touches nothing on the live headerless 3,328-row tab: adding a header
   there would shift every existing row, and writing unconfirmed rows without a
   Tier column would recreate the exact defect that made those rows unauditable.
   Dave works `Gold Dots`. `Gold Recheck` is a review queue, not a call list.

2. **`Tier` + `Build Code` on the Gold Dots header.** A row now records **why**
   it was called gold. Not recording that is precisely why the existing 3,328
   rows cannot be told apart — `VERIFIED_GOLD` vs `NEEDS_RECHECK` is
   reconstructable going forward, never backward.

3. **Customer specimens in the feed.** The full record for CUSTOMER dots
   (BAN redacted to a boolean, capped at 40, spread across build codes rather
   than first-come). **The field that separates a DSL customer from a fiber one
   is already in the payload and has never been looked at** — `speed` is the
   obvious candidate; the sample record shows `"speed":""` on a non-customer.
   One sweep over a customer pocket should decode `unavailable` from data.
   When it does, every `Gold Recheck` row carrying that code promotes to real
   gold in a single move — which is the whole reason the build code is stored
   on the row.

### The identity bug the tests caught

Writing tests for the recheck tab surfaced a live defect in `keys_for()`:
**AT&T geocodes neighbouring townhouses to a single point**, and the coordinate
key merged them. 8231 and 8233 Devonwood arrived on the same lat/lng and
collapsed into one row — a $140 lead gone silently. Same class as the Wenda St
cross-city merge and the apartment-unit merge before it; the third time this
key has lost a lead.

The coordinate key now carries the **street number and unit**, so two doors at
one point stay two rows, while the same door written two ways
(`5309 WENDA ST` vs `5309 WENDA ST, HOUSTON TX 77016` — the legacy-format split
the key exists for) still collapses to one. Six identity cases tested.

**The lesson:** a positional key is not an identity. Coordinates say *where*,
not *who*, and AT&T's geocoder is coarser than its address list. Any dedupe that
can merge two distinct doors will eventually delete a sale, and it will do it
without a message.

### Still open

`unavailable` is **recorded, not decoded**. Nothing here decides it — the point
is to stop destroying the evidence while we find out. It needs one completed
sweep over a pocket with customers in it.

## 22.22 An outside review, the right bug in the wrong file (2026-08-23)

A detailed external review landed. Its **headline finding is a real bug**, and
it is **not in the program that is running** — a distinction worth recording,
because the mix-up is now built into the repo layout and will happen again.

### The two-hunter trap, from the outside

The reviewer inspected `optimus-map-tools/main/fiber_hunter.py`, found v5.27,
pixel-based, with `ImageGrab` / `GREEN_MIN` / `count_dot_clusters()` and no
trace of `queryRenderedFeatures`, `curr_ntwrk_bld_type_cd`, or `BUILD_DATE` —
and correctly concluded that this could not be the architecture we were
discussing. That was the right call from the evidence available.

Then it reported this, from that file:

```python
try:
    tabs[tab].append_rows(buf)
except Exception as e:
    print("  write err %s: %s" % (tab, e))
_buffers[tab] = []          # cleared whether the write worked or not
```

**Verified: that bug is real and still sits in `fiber_hunter.py` line 886.** It
is also in a tool nobody is running. The live hunter has no `_buffers` and no
`_flush` at all.

The lesson is not "the reviewer was wrong" — it read the only code it could
reach. It is that **a public repo holding a stale copy of a differently-named
tool will burn anyone who looks, including a careful reader.** Hence
`print_identity()`: every run now states its file, BUILD_DATE, fingerprint,
repo, branch and self-update URL, and names the other hunter explicitly as
*not* the one running.

### The same defect was live, wearing different clothes

Checking the live writer against the principle found this in `write_gold_dots`:

```python
keys = _gold_keys(addr, ...)
if keys & seen: continue
seen.update(keys)        # <-- marked captured HERE
...
gw.append_rows(batch)    # <-- attempted much later; on failure, rows are gone
```

A failed batch was **discarded and permanently marked captured**, so not even a
re-sweep would retry it. Same silent gold loss the reviewer described, reached
by a different route. Their instinct was right even though their file was not.

**Fixed:** `commit_rows()` retries with bounded backoff; a batch that still
fails is parked to `optimus/_pending/*.json` and replayed at the next run's
startup; rows leave the queue only after Google ACKs. The dedupe key is marked
seen **only for rows that actually committed**. The console now says
`SHEET COMMITTED` / `SHEET COMMIT FAILED` / `PRESERVED FOR RETRY` — nothing
claims a row was written before it is in the sheet.

Tested four ways: transient failure retries and commits; permanent failure
parks and reports **zero** committed; the next run replays the parked batch into
the sheet; uncommitted keys stay retryable.

### The best idea in the review: source vs rendered

`queryRenderedFeatures()` and `querySourceFeatures()` answer **different
questions** — what the style is drawing now, versus what is in the loaded tiles
regardless of style. Running both makes a zero self-explaining:

| source | rendered | meaning |
|---|---|---|
| >0 | >0 | healthy |
| >0 | **0** | a filter, visibility flag or zoom band is hiding it — **this zero is invalid** |
| 0 | >0 | wrong source identified |
| 0 | 0 | no data reached the map — session or load problem |

The diagnostic now runs both and emits `RENDERED_ZERO_SOURCE_FULL` instead of
reporting a valid zero. This is the same principle as 22.20 — never turn
uncertainty into a zero — applied one layer deeper, and it is a genuinely new
idea that came from outside.

### What was deliberately NOT done

- **A `FiberDot` dataclass and a rebuilt pipeline.** Correct design, wrong
  moment: it is a rewrite, and no sweep has completed yet. Rewriting the path
  under an unproven capture is how the last three days were spent.
- **Per-feature-ID loss reporting.** Better than counts, agreed. The boundary
  counters plus `first_failure()` already name the failing stage; IDs are the
  next increment, not this one.
- **Purging every bare `except`.** Done on the write paths. Telemetry keeps
  its catches on purpose — the feed must never be the reason a sweep dies.

**Their recommended order — verify build → fix the writer → prove the commit →
counters → source-vs-rendered → only then the classifier — is right, and it is
the order actually followed.**

## 22.23 The Hunter's two permanent invariants (2026-08-23)

These are not observations. They are rules the code now enforces and the run
report checks by name.

> **A fiber observation is only valid if the capture state was valid, and a
> captured dot is only complete once persistence is acknowledged.
> Never convert an invalid capture into `+0`, and never convert a failed write
> into `seen`.**

### Invariant 1 — `seen ⊆ committed`

A dot is marked seen **only after Google acknowledges the write.** The old order
was:

```
detect -> mark seen -> attempt write -> on failure, rows discarded
```

which lost the rows *and* left them permanently marked captured, so no re-sweep
would ever retry them. The order is now:

```
detect -> stage -> attempt write -> ACK -> mark seen -> clear pending
                              \-> failure -> park on disk, NOT seen, retry next run
```

Checked at the end of every run as `gold_seen == gold_committed`. A breach
prints `IT WILL NEVER RETRY` and names the stage.

### Invariant 2 — a zero must earn the right to be a zero

`VALID_ZERO` requires **all** of: map captured, style loaded, map loaded, dot
layers found, zoom inside the layer band, query without error. Anything else is
`INVALID_ZERO`, printed with the failed preconditions listed, and is never
written as `+0`.

### Stage counters

Printed at the end of every run and published to the feed:

```
RAW FEATURES 480 / GREEN 440 / GOLD 12 / GREY 22 / UNKNOWN 6
GOLD QUEUED 12 -> ATTEMPTED 12 -> COMMITTED 12 -> SEEN 12 -> PENDING 0
```

The shape is the diagnosis. `GOLD CLASSIFIED 12, COMMITTED 0` means stop looking
at Mapbox. `GOLD CLASSIFIED 0, RAW 480` means it is the classifier. `RAW 0` means
nothing was delivered. Tested against all four shapes.

### On SQLite, and being honest about what was built

Two outside reviews called for a SQLite pending queue. **It is not SQLite — it
is append-only JSON files in `optimus/_pending/`,** replayed at startup and
deleted only after an ACK. That satisfies the actual requirement (the queue must
survive a crash, a reboot, or a kill) because the files are on disk before the
write is attempted. SQLite would add `attempt_count` and `last_error` cleanly and
is the better long-term store, but it was not built, and the difference is worth
recording rather than glossing.

**A status table arrived claiming ten items were "✅ Fixed."** Six were absent
from the code: SQLite, stage counters, VALID_ZERO/INVALID_ZERO, the
layer-vs-source maxzoom split, a Devonwood regression test, and `attempt_count`
on pending rows. Four of those six have since been built for real; the Devonwood
regression test and SQLite have not.

The lesson is the same one as 22.20, one level up: **a confident status report is
not evidence.** Verify a claim about the code against the code — including, and
especially, a claim that agrees with you.

### Still not proven

Every item above is verified by unit test, not by a field run. **No sweep has
completed.** Until one does, none of this is known to work on live data.

## 22.24 The session was the bug, all day (2026-08-23, evening)

**A 150-cell sweep captured nothing, and the reason was not in our code.**

The console said it outright once the reporting was good enough to show it:

```
!! AT&T REPLIED 301 -- NOTHING CAN LAND THIS RUN
!! REDIRECTED TO LOGIN -- not logged in, nothing lands
!! AT&T SENT 200 BUT THE BODY IS NOT DATA:
!! NOT JSON -- First 120 chars: <!DOCTYPE html> <html lang="en">
```

Every cell panned, pressed *Search this area*, and received a login page.
150 times. Every cell scored `+0`.

### The trap: a half-dead session looks perfectly healthy

The cookie still authenticated the page shell. **The map kept showing dots** —
green, gold and grey, thick across Devonwood — because those were fetched
*before* the session went stale. So the screen looked right while the data path
was shut. That is why this read as a code bug for hours: the evidence a human
looks at first was lying.

Patrick, reasonably: *"how did u break the green too!!"* — and the check that
settles it is worth recording. **Nothing in the decode path changed all day.**
Every one of the 28 commits was reporting, the login gate, or the writer. Green
scored zero for exactly the same reason gold did: there is no green in a login
page. Verify before you defend, and verify before you accept blame.

### What was built in response

- **`recover_session()`** — three consecutive auth failures stop the sweep,
  clear the cookies so AT&T must present a real login, wait for the sign-in,
  and **resume where it left off**. Telling the operator to log out by hand
  afterwards is not a fix; it is a chore handed back. Any real reply clears the
  streak, so one blip never interrupts a healthy sweep.
- **Crash capture** — an unhandled exception or a non-zero `sys.exit` now
  publishes its type, message and traceback.
- **Per-run heartbeats** — a second launch used to overwrite the shared
  breadcrumb, and did: the trail of the run that was working was erased by the
  one that died in 1.5 seconds.
- **`_as_spreadsheet()`** — three opening-intel lines were failing with
  `'Worksheet' object has no attribute 'add_worksheet'`, one of them reading
  *"could not read 'Gold Dots'"*. That is a banner error that looks exactly like
  gold capture being broken. All 15 sheet entry points now normalise the
  argument instead of trusting the caller.

### Process hygiene is a real failure mode

Three separate runs today were killed by **two hunters sharing one Chromium
profile**, and a **zombie run from 15:17** surfaced at 18:08 having sat open for
three hours, overwriting the shared report with zeros. One window at a time is
not a style preference; it is a correctness requirement.

### The idea that should have come first

Gold and grey are identical on the wire except `curr_ntwrk_bld_type_cd`, and
`unavailable` — the most common value — is in neither list. Every classification
of those dots has been reverse-engineered from captures, and both guesses have
been wrong in production.

**But AT&T's own map paints them correctly from that same payload.** The rule is
in their JavaScript, already sitting in the browser profile. `decode_gold.py`
now reads it out of the cache.

That was available from the first hour. Instead the day went to inferring a rule
that was sitting on disk the whole time. **When a system demonstrably already
knows the answer, read its answer before deriving your own.**

## 22.25 FREEZE: the gold predicate is locked, and nothing else moves (2026-08-24)

An outside review's diagnosis of why this dragged on: **"too many layers were
being modified in response to one symptom."** That is correct, and it matches my
own count — of 36 builds on 2026-08-23, six were fixing bugs I had introduced
that same day, and roughly twenty were instrumentation added one gap at a time
instead of in a single pass.

The freeze, adopted:

```
DO NOT TOUCH the green path
DO NOT TOUCH the writer
DO NOT TOUCH the Mapbox diagnostics
ONLY: capture raw gold + grey records, diff the fields,
      lock the gold predicate, add tests
```

### There are TWO implementations of the gold rule

`precise_fiber_hunter.classify_wire()` runs the live sweep.
`backend_classifier.classify_lead()` serves fiber_scout, zip_reader and
verify_gold_capture. Two copies of one rule is how they drift apart unnoticed —
CLAUDE.md already warns about this exact thing.

`test_gold_predicate.py` now holds them to the same answers on every decided
case and pins the three decisions that have cost money before: an undecodable
customer is not gold (that put fiber customers in front of a rep), not grey
(grey never reaches the sheet, so real $140 leads were deleted), and a
placeholder BAN like `non-cust` is not a customer (reading it as one dropped a
$500 green). Both implementations pass all of it.

### A false alarm I nearly shipped, twice

Writing that test, the harness reported the live classifier returning UNKNOWN
for `fttp-gpon` and `fttn-bp` — which would mean gold could never be emitted at
all. It was wrong both times, and for two different reasons:

1. it exec'd only `_BLD_CODES = {"fiber": (), "copper": ()}`, the empty default,
   not the loader below it;
2. once that was fixed, the loader resolves `build_codes.json` relative to
   `__file__`, which the harness namespace did not define — so `open()` threw,
   `except: pass` swallowed it, and the tables stayed empty.

An empty code table looks *identical* to a broken classifier. Had either been
reported, the next hours would have gone to rewriting a classifier that was
correct all along.

**The rule: a test harness is not evidence until the harness itself is
verified.** The same standard applied to a status report in 22.23 applies to my
own tooling — and `except: pass` around a loader is what made a missing
precondition indistinguishable from a wrong answer.

### What remains, and only this

`unavailable` on a real account is still undecided, and nothing guesses at it.
Deciding it needs raw gold+grey records from one authenticated capture — or
AT&T's own colouring rule, which `decode_gold.py` reads out of the browser
cache. When the answer arrives it is a change to **build_codes.json — data, not
code** — and the test above proves both implementations pick it up.

## 22.26 State of the fiber capture system — written for outside review (2026-08-24)

Everything an outside reviewer needs, with the specifics. No summary of a
summary: file names, field names, real numbers, and an explicit line between
what is proven and what is assumed.

### The architecture (this is not a pixel scraper)

```
Playwright drives Chromium (persistent profile)
      -> youachieve.att.com/yourefer/fiber
      -> the page's own JS calls GET /yourefer/api/fiberMap.cfc
                ?method=getMapData&lon=..&lat=..&attuid=..&csrfToken=..
      -> page.on("response") captures that reply OFF THE WIRE
      -> json.loads(body) -> data["content"] = list of address records
      -> classify each record -> write to Google Sheets
```

The hunter does **not** read the screen. It reads AT&T's own JSON. The Mapbox
hook is a cross-check only and is not in the capture path — a distinction worth
holding, because a day was partly spent on Mapbox diagnostics that could not
have affected the outcome either way.

The endpoint is declared `text/html` and serves JSON. It caps at **500 records
per reply** (measured, not documented).

### The record, verbatim

```json
{"zip":"77598","address":"558 TRESVANT DR","city":"WEBSTER","state":"TX",
 "latitude":"29.562304","longitude":"-95.144801",
 "subscriber_ban":"", "subscriber_ban_masked":"",
 "curr_ntwrk_bld_type_cd":"unavailable", "speed":"",
 "miles_from_claim":"0.10137", "missing_supl":0}
```

### The predicate, in full

```python
if is_customer_ban(ban):                      # a real AT&T account
    if "copper" in (status or "").lower():    # AT&T said it outright
        return "copper_upgrade"               # GOLD  $140
    code = _bld_code(raw)                     # curr_ntwrk_bld_type_cd
    if not code:                 return "unknown_customer"
    if code in FIBER_CODES:      return "customer"        # GREY, never written
    if code in COPPER_CODES:     return "copper_upgrade"  # GOLD  $140
    return "unknown_customer"                 # <-- 'unavailable' lands here
return "lead"                                 # no account = GREEN  $500
```

`build_codes.json`, the single source of truth for both implementations:

```
fiber  (GREY): fttp-gpon, fttp, gpon, ftth
copper (GOLD): fttn-bp, fttn, ip-rt, iprt, copper, ipbb, adsl, vdsl, dsl
```

### The asymmetry — why green works and gold does not

**GREEN is detected by an ABSENCE.** `subscriber_ban` empty means non-customer.
One field, no lookup table, cannot fail. ~496,000 rows captured historically.

**GOLD needs a POSITIVE MATCH** against a reverse-engineered code list. And
AT&T's most common value for `curr_ntwrk_bld_type_cd` is the literal string
**`unavailable`**, which is in neither list.

Both guesses at it have failed **in production**:

| guess | outcome |
|---|---|
| gold | existing FIBER customers reached the call list; Patrick clicked a gold dot and got someone already on fiber. Produced the contaminated 3,328 rows. |
| grey | grey never reaches the sheet, so real $140 upgrades were deleted silently |

Current behaviour: neither. Undecodable customers are written to a separate
`Gold Recheck` tab **with their build code**, off the call list, so nothing is
destroyed while the question is open.

Confirmed separately: for a NON-customer, `unavailable` is normal — a live
capture over ZIP 77027 returned every green address as `ban=""` +
`unavailable`. Treating it as dead once threw away 100% of the greens.

### Two implementations of one rule

- `precise_fiber_hunter.classify_wire()` — the live sweep
- `backend_classifier.classify_lead()` — fiber_scout, zip_reader,
  verify_gold_capture

`test_gold_predicate.py` (15 assertions, all passing) holds them to identical
answers on every decided case and pins three regressions that have cost money:
undecodable is not gold, undecodable is not grey, and a placeholder BAN like
`non-cust` is not a customer.

### What is PROVEN

- The predicate, by unit test, both implementations agreeing
- Durable writes: a failed Sheets write parks to `optimus/_pending/*.json`,
  replays at next startup, and `seen` is marked **only** after Google ACKs.
  13 assertions in `test_durability.py`, including forced-failure and
  crash-recovery
- Green and gold share one write path (they did not, until 2026-08-23)
- Telemetry: phase breadcrumb, stage counters, crash tracebacks, and the raw
  body of any zero-lead reply, all pushed to `optimus/_feed/`

### What is NOT proven

**The capture path has never been handed a single real record.** Every failure
on 2026-08-23 was environmental:

- a stale cookie that authenticated the page shell but **not** the API — AT&T
  returned `301 -> login` or a 200 carrying `<!DOCTYPE html>`, 150 cells in a
  row, every cell `+0`, while the map still showed dots fetched before the
  session went stale
- two hunters sharing one Chromium profile; the loser dies instantly and
  overwrites the shared report with zeros
- a zombie run from 15:17 that surfaced at 18:08 having sat open three hours

So: classifier, writer and dedupe are unit-proven and field-unproven.

### The one open question

**What does `curr_ntwrk_bld_type_cd = "unavailable"` mean when
`subscriber_ban` IS populated?**

Three readings, each implying different action:

1. **copper** — the recheck queue is thousands of $140 leads awaiting promotion
2. **fiber** — they are grey and correctly excluded
3. **not a broadband account at all** (wireless/DirecTV only) — they are **not
   leads**, and working them wastes a rep's time entirely

Nothing in the system guesses. Three ways to settle it, none requiring a code
change:

- `decode_gold.py` cross-tabs build code against customer/non-customer from the
  saved `serviceability_raw.json`. A code appearing on **both** customers and
  non-customers would prove the field is not describing the subscriber at all.
- The same script reads **AT&T's own colouring rule** out of the map JavaScript
  cached in the browser profile. Their map paints gold and grey correctly from
  this exact payload, so the rule is in their code — the original, not an
  inference.
- `speed` is in the payload and has never been examined. A DSL subscriber
  should show 768K/6M/25M; fiber 300M/1G/5G.

When the answer arrives it is an edit to **`build_codes.json` — data, not
code** — and `test_gold_predicate.py` proves both implementations pick it up.

### What a reviewer should NOT ask for

- A pixel/RGB detector. Not the architecture; it is fallback only.
- A rewrite of the green path. It works and was untouched throughout.
- A classifier rewrite before counters show loss AT classification. The stage
  counters print `RAW -> classified green/gold/grey/unknown -> gold queued /
  committed / seen / pending`; the first drop names the stage.

## 22.27 THE GOLD BUG — found 2026-08-23. It was never the classifier

The reason gold never landed, after a month of suspicion and a full day of
rebuilds, is four lines in the writer:

```python
seen = already_seen(ws)        # 507,053 addresses read from PRECISE FIBER
...
key = addr.upper()
if key in seen:
    continue                   # <-- dropped BEFORE classify_lead() runs
dot_status = classify_lead(ld)
```

`seen` is built from **Precise Fiber — the GREEN tab.** Any address captured on
an earlier sweep was discarded before its colour was ever evaluated. It never
reached `write_gold_dots`. **It could not be added to the Gold Dots tab, ever,
no matter how many times the ground was re-swept.**

### This explains the discrepancy that has been open for weeks

**Precise Fiber holds 8,264 ORANGE rows. Gold Dots holds 1,984.** That gap was
not a writer failure or a classifier failure — it was structurally unable to
close. Every gold dot already recorded in Precise Fiber was invisible to the
gold path forever after.

### And it explains the entire day

One run's report and console, side by side:

```
report : OK: 86 serviceability responses -> 42,500 leads
console: [cell 210] +0  (total 1)
stage  : classified_green 1, classified_gold 0, classified_grey 0
```

**42,500 records decoded. One classified.** Capture was never broken. Prestonwood
had already been swept, so every dot on that screen was skipped on sight.

`+0` means **zero NEW**, not zero captured. I read it as a capture failure for
most of a day and chased the session, the parser, the payload shape, and the
Mapbox rendering path because of it. Two outside reviews chased the classifier
for the same reason. All of it was downstream of a filter doing exactly what it
was written to do.

### The fix (build 4303a589)

```python
_already = key in seen
if not _already:
    staged_keys.append(key)        # not marked seen until the write is ACKed
dot_status = classify_lead(ld)     # ALWAYS runs now
...
if _already:
    stage(revisited=1)             # suppress only the Precise Fiber ROW
else:
    new_rows.append([...])
```

Classification always runs; gold, grey and recheck routing always run. Only the
duplicate Precise Fiber row is suppressed. Each destination tab carries its own
dedupe, so nothing duplicates.

**The trap inside the fix.** The obvious form is `continue` after the guard. That
skips `new_records` — and `new_records` is exactly what feeds `write_gold_dots`,
so it silently re-creates the bug being fixed. I wrote it that way first and
caught it only by tracing one record's path through the function. A fix that
re-implements the bug is the most expensive kind, because it looks like a fix.

### The lesson, and it is the day's real one

**A counter that means "new" was read as if it meant "captured".** `+0` is not a
zero from AT&T; it is a zero after our own filter. Nothing in the console said
which, so every layer downstream got investigated before the filter itself.

The rule this earns: **when a count is zero, establish whether the zero came
from the source or from us before touching anything.** The whole diagnostic
apparatus built today — boundary counters, capture truth, first-drop — exists to
answer that question, and it still could not, because `revisited` was not a
counter that existed. It is now.

Related and previously recorded: 22.20 (a login page read as empty ground),
22.22 (a real bug found in a file nobody runs), 22.25 (an empty code table looks
identical to a broken classifier). This is the fourth instance of the same
shape — **a missing precondition wearing the costume of a wrong answer** — and
the most expensive.

### Status

Fixed against the code and unit-tested. **Not yet proven on the map.** The next
sweep over already-captured ground is the test: if gold lands on ground that has
returned `+0` for weeks, this is confirmed.

---

## 22.28 2026-08-24 Dot Capture Debug — Zero Captures, Root Cause Analysis

**Problem Statement:** The system captures zero dots to sheets after runs complete. Dots appear on the Mapbox UI ("the dots are populating"), but nothing writes to TEST-Green / TEST-Gold / TEST-Grey tabs. Previous builds produced +0 consistently across all three types.

**Session Actions:**
1. Redirected code to write to test tabs (TEST-Green-2026-08-24, TEST-Gold-2026-08-24, TEST-Grey-2026-08-24) to isolate test data
2. Inspected production flush path (lines 2560-2784) against documented gold bug fix (build 4303a589)
3. Traced data flow: NetCapture.handle() extraction → classify_lead() → routing (Precise/Gold/Grey writes)
4. Read BRAIN.md 22.27 gold bug pattern; verified current code implements it correctly

**Code Structure Verified Correct:**
- Line 2589: `_already = False  # key in seen  # DISABLED FOR TEST` — correctly disables dedupe for test mode, matching gold bug fix pattern
- Line 2592: `dot_status = classify_lead(ld)` — ALWAYS runs, not gated by _already
- Line 2663-2669: Precise Fiber row suppressed only if `_already`, new_records still populated
- Line 2639-2653: GREY records added to grey_records, then continue (correct — prevents GREY from Precise Fiber)
- Line 2670-2687: new_records ALWAYS populated with full record, whether _already or not
- Line 2731: `if new_rows:` → write Precise Fiber independently
- Line 2754: `if new_records and not (dry or ws is None):` → write Gold independently
- Line 2766: `if grey_records and not (dry or ws is None):` → write Grey independently

**Routing Logic Correct:** All three destinations (Precise/Gold/Grey) write independently without early returns. No `if not new_rows: return 0` before write_grey_dots().

**Classification Pipeline Verified:**
- classify_lead() → classify_wire() → DOT_COLOR mapping
- GREEN: no customer BAN → "lead" → dot_color() = "GREEN"
- GOLD/ORANGE: BAN + copper build code → "copper_upgrade" → "ORANGE"
- GREY: BAN + fiber build code → "customer" → "GREY"
- UNKNOWN: BAN + undecodable code → "unknown_customer" → "UNKNOWN"

**Split Mode vs Production Mode:**
- Redirect to test tabs uses production flush (line 2567: `if _SPLIT[0]:` checks split mode)
- Split mode sends to local JSONL, uploader sends to sheets (lines 2786-2829)
- Production mode writes directly to sheets via commit_rows()

**Potential Root Causes Identified:**
1. **Session Expiry During Data Capture:** Previous test run hit "LOGGED_OUT phase at 62.1s with zero captured records." Browser session may expire mid-sweep, all network captures fail silently.
2. **Network Silence:** AT&T API returning empty serviceability responses (0 leads extracted → 0 to classify → 0 to write). Logs would show "OK: 0 serviceability responses" if this occurs.
3. **Login Redirect:** Map returns login page HTML instead of fiber map; DOM parse sees empty (22.20 pattern from BRAIN 22.1-22.25).
4. **Buffer Timing:** Writes may occur after test run ends prematurely (flush_backend/flush_local called at exit but process killed before completion).

**Next Step — Field Test Required:**
Created test tabs and redirected code. Need to:
1. Start fresh Chromium browser session (clear cookies)
2. Run precise_fiber_hunter with fresh login flow (not cached session)
3. Let it complete 60+ seconds (pass login, map load, at least one viewport capture)
4. Check GitHub artifact (latest.json) for classified_green/gold/grey counters (should show > 0)
5. Check test tabs for actual written rows
6. If test tabs empty but artifact shows counters > 0, investigate buffer/flush timing
7. If artifact shows counters = 0, investigate session/network layer

**Code Confidence:** Production flush, split flush, classification, routing all correct. No bugs found in those paths. Issue is pre-write (extraction, network, or session state).

---

## 22.29 2026-08-24 Unified Classifier Implementation

**Problem Solved:** Eliminated dual-classifier architecture that allowed GREEN→GOLD drift.
- precise_fiber_hunter.py had its own classify_wire() + environment overrides
- backend_classifier.py was the canonical classifier but was bypassed
- Unknown build codes could be forced to GOLD via OPTIMUS_UNKNOWN_CUSTOMER env var
- Risk: two paths could classify differently, causing regressions

**Solution Implemented (commit d72db00):**

1. **Single Classifier Source of Truth:**
   - Import `backend_classifier.classify_lead` (line 91)
   - Replace classify_wire() with unified classify_lead() (lines 637-665)
   - Preserve wire-specific logic: status text can override ("copper" in status → GOLD)
   - Delegate to backend_classifier for build-code decoding

2. **Unified Return Values:**
   - backend GREEN → "lead" (displays as GREEN)
   - backend GOLD → "copper_upgrade" (displays as ORANGE)
   - backend GREY → "customer" (displays as GREY)
   - backend CUSTOMER → "unknown_customer" (displays as UNKNOWN)

3. **Four Test Tabs (Clean Validation):**
   - TEST-Green-2026-08-24: GREEN non-customers (eligible fiber, no account)
   - TEST-Gold-2026-08-24: GOLD copper customers (upgrade targets)
   - TEST-Grey-2026-08-24: GREY fiber customers (existing subscribers, skip)
   - TEST-Unknown-2026-08-24: UNKNOWN undecodable customer build codes (visible, not on call list)

4. **Unknown Routing (Visibility + Safety):**
   - Added write_unknown_dots() function (lines 3409-3447)
   - Production flush routes unknown_customer → TEST-Unknown tab (line 2690+)
   - Initialize unknown_records, unknown_ct in flush (line 2598)
   - Call write_unknown_dots() independently (line 2815+)
   - **Why:** Undecodable codes silently vanished before (GREY has no sheet reach). Now visible for human review and safe (not on call list until verified).

5. **Hardened Append:**
   - commit_rows() already has 3-attempt retry + exponential backoff (lines 3285-3314)
   - Explicit SHEET COMMIT FAILED messages printed on retry (line 3303)
   - Successful batch committed printed on ACK (line 3309)
   - Parked to disk on all-attempts-failed (line 3311)

**Test Plan:**
Run precise_fiber_hunter with fresh browser session → capture 60+ seconds →
1. Terminal: Check counts printed (GREEN / GOLD / GREY / UNKNOWN > 0)
2. GitHub artifact (latest.json): Verify classified_* counters match terminal
3. TEST-Green tab: ≥1 non-customer address with timestamp
4. TEST-Gold tab: ≥1 copper customer with build code
5. TEST-Grey tab: ≥1 existing fiber customer with build code
6. TEST-Unknown tab: ≥1 undecodable customer for audit

**Proof of Correctness:** One address must appear in exactly ONE tab with matching classification. If addresses are split across tabs or duplicated, the classifier or dedupe has a bug.

## 22.30 END-TO-END GOLD VERIFIED — the pipeline is proven (2026-08-24, field session)

Patrick drove Prestonwood Forest (8231 Devonwood Ln, 77070) with all three colors
deliberately in view. Green flowed; TEST-Gold and TEST-Grey stayed empty while the
console counted 500+ confirmed copper. Two bugs, both in `precise_fiber_hunter.py`
on the hunter repo (`Go-High-Level-MCP-2026-Complete`, branch
`claude/optimus-map-tools-setup-6dcl6o`):

**Bug 1 — ORANGE routed as unknown.** `dot_color("copper_upgrade")` returns
`"ORANGE"`, but three paths checked only `"GOLD"`: the uploader's bucket routing
(~5657), coordinate-capture validation (~1954), pixel counting (~4023). Copper
customers were classified correctly and then filed as unknown. Fixed: every gold
check is now `in ("GOLD", "ORANGE")`.

**Bug 2 — THE KILLER: buckets wiped before their write.** In `uploader_main`,
`gold_records`/`grey_records` were cleared in the same block that clears
`main_sheet_rows` after the main-sheet append — but `write_gold_dots` /
`write_grey_dots` run AFTER that block. They received an empty list every single
cycle. This is why the gold tab could stay at zero forever while classification
counters climbed: **counters on screen and rows in the sheet are different code
paths — a climbing counter proves classification, not writing.** Buckets now
clear only after their own tab writes succeed (which also preserves them for
retry if a write fails).

Also added because Patrick asked for it directly: the uploader console prints
every GOLD address on its own line as it ships, plus `GREEN x__ ->` (first 5)
and `GREY x__ ->` (first 8) per batch. He wants addresses on the black screen,
not summaries.

**The verification, end to end (2026-08-24 ~16:26–16:39 CT):**
1. Laptop relaunched; `_feed/heartbeat.json` fingerprint `c6403a7c` == sha256
   head-8 of the file at commit `f15a5d5` (all fixes). That fingerprint match is
   the fast way to prove which commit a hunter PC is actually running.
2. Console: GREEN 6150 / GREY 2828 / GOLD 72, "0.0% of customer dots were a
   guess, not a decode."
3. TEST-Gold-2026-08-24 filled with real addresses: 14507 SOMMER…, 6302 NYOKA ST,
   14611 SOMMER…, 6214 NYOKA ST, 16105 SINGAPO…. TEST-Green passed 13,000 rows.
4. **Ground truth:** Patrick clicked 6214 NYOKA ST on the dealer map itself:
   "FIBER ELIGIBLE / Status: Existing Copper Customer / Subscriber BAN:
   ******231". The sheet's gold row matches AT&T's own popup exactly.

That last step is the standard for "gold works": a row in the gold tab whose dot,
clicked on the live map, says Existing Copper Customer. It happened. The chain
map dot → backend capture → classify_wire → ORANGE → gold bucket → TEST-Gold tab
is proven with zero guessed customers.

**Traps recorded so nobody re-learns them:**
- `optimus/_live/serviceability_raw.json` in the repo was a stale Aug-22 capture
  from ELGIN, TX. Reading it as "the current area" concluded "no copper here"
  while Patrick's live console showed 500+ confirmed copper. Repo `_live` files
  are whatever some past run left behind — check `_feed/heartbeat.json` (run_id,
  machine, fingerprint, updated_at) for what is running NOW, and trust the live
  console over stale repo files.
- The visual map legend and the backend JSON can disagree per-view; the popup
  status field ("Existing Copper Customer") is direct evidence and classify_wire
  already honors it before build codes.

## 22.31 `ip-co` — the unmapped code hiding gold (2026-08-25, DECISION PENDING)

Run `20260825-105030` (Beaumont, LAPTOP-FJEEPATI) classified 126,628 dots:
green 81,984 · fiber/grey 44,500 · **copper 0** · unknown 144. Zero copper out of
44,500 customers is not believable.

Exactly ONE build code came back undecodable:

| Code | Count this run | Sample address |
|---|---|---|
| **`ip-co`** | **288** | 229 DOWLEN RD RM 6B (Beaumont) |

`ip-rt` (IP **R**emote **T**erminal) is already CONFIRMED copper and on the gold
list. `ip-co` is almost certainly IP from the **C**entral **O**ffice — the same
IP-DSL family, copper last mile, just fed from the CO instead of a remote
terminal. If that reading is right, every `ip-co` dot is a $140 upgrade lead and
we have been filing them as UNKNOWN.

**NOT ADDED YET, ON PURPOSE.** The gold predicate is frozen (22.25) and a wrong
widening is exactly what once put existing fiber customers in front of a rep
(22.14). The rule stands: confirm on the map, THEN add to `build_codes.json`.

**To close this out:** pull up `229 DOWLEN RD RM 6B` on the dealer map and click
the dot. If the popup reads "Existing Copper Customer" (the way 6214 NYOKA ST did
on 2026-08-24, BRAIN 22.30), add `"ip-co"` to the `copper` list in
`build_codes.json` — it rides `_CORE_FILES`, so it deploys to every hunter PC on
next launch. If it reads as a fiber customer, add it to `fiber` instead and the
144 unknowns stop being noise.

Nothing is lost while this is undecided: UNKNOWN customers are written to
`Unknown Customers` / `Gold Recheck`, which is the recheck design doing its job.

## 22.32 THE 2026-08-25 ROADMAP — everything Patrick asked for, with status

Dumped in one go while in the field. Recorded here so none of it evaporates.
Status is honest: SHIPPED means it is in the code and pushed, QUEUED means
designed but not built, DECISION means it needs Patrick before anyone writes it.

### Shipped this session
| Item | Where it lives |
|---|---|
| Start/stop hotkeys | Ctrl+Shift+Pause (or Ctrl+Shift+P) = PAUSE, Ctrl+G = GO. Global, work while Chrome has focus. See CLAUDE.md controls table |
| **Map starts in 10 seconds** | `countdown_to_start(10)` runs before the FIRST pan so the view can be aimed by hand. Ctrl+G cuts it short; unattended runs skip it |
| Operator = typed INITIALS | `optimus_operator._ask()` — the six-name menu is gone. PS / ps / p.s. / "Patrick Siado" all become PS. Stamped on every lead |
| Timestamp on leads | Already there and always was: `Captured At` on every row of every tab, plus `Run ID` |
| AT&T build-out news | `intel_banner()` now PRINTS it. It was fetched every launch since August and never shown |
| Cable outage news | NEW `cable` bucket: Comcast/Xfinity/Spectrum/Charter/Cox/Optimum/Suddenlink/Altice + outage words, territory-filtered. A cable outage is the OPPOSITE of ours — their customers are down and we are the fix |
| Sheet cleanup | `CLEAN_SHEET.bat` — whitelist delete, CSV backup first, migrates TEST-Gold into Gold Confirmed, dedupes, then formats |
| Linked sheets Claude can read | Three IMPORTRANGE bridges in Patrick's Drive + `sheet_feed.py` (chunked JSON to GitHub) |
| Map scraper: resi + cell | Two columns only. `Resi?` from address shape; `Cell?` says `NO toll-free` or `LOOKUP` — never a guessed carrier |

### Queued — designed, not built
- **2x/day email: progress + analytics.** Source is `_feed/latest.json` (counts,
  phases, crash, undecoded codes) plus the sheet bridges. BLOCKED on one fact:
  **which address.** The session account is BHOLLAND@thefiberplug.com, the Drive
  owner is patricksiado@gmail.com. Do not guess — business analytics to the
  wrong inbox is not a recoverable mistake.
- **Fresh-area detector emails PATRICK ONLY.** Explicitly not a team broadcast
  yet. Reuses the existing freshness rule (green+gold dense, grey share low —
  see `backend_classifier.FRESH_MIN_ELIGIBLE`), which is already computed.
- **Cable outage HISTORY.** Live headlines work; nothing archives them. Wants a
  tab keyed by ZIP/city + date so "who went out here before" is answerable.

### Queued — the Cowork loop (fresh area -> money)
1. Fresh area detected **by Patrick or his own staff** -> DealMachine number
   added -> text sent -> loaded for auto-dialer calls.
2. **A business inside a fresh GREEN area gets flagged too.** The reason is
   specific: a fresh area may exist *because* of a business that was previously
   on the business list but NOT on the fiber-green list. That transition is the
   signal, not the business itself.
3. Carrier-aware routing: **if DealMachine says AT&T or Verizon, act
   accordingly** — different pitch per carrier. Design the branch, do not spend
   credits proving it on a hunch.

### DECISION — needs Patrick before a word of it reaches a customer
- **$15 cell service, iPhone 17 Pro Max $5.** The intent is to test willingness
  to bite, on a few emails first. Nothing goes out until Patrick confirms the
  REAL terms: what $15 buys, what the $5 is (down? per month? with trade?), and
  what the qualifying conditions are. Standing rule (CLAUDE.md): never quote a
  flat price, and business fiber is priced by speed tier. An offer this sharp
  gets scrutinised — wrong numbers in writing is the one mistake that costs more
  than a lost lead.
- **Long-term: does this work?** The measurement question. Nothing answers it
  today because nothing ties a lead to a close. `Run ID` + `Operator` are on
  every row precisely so this becomes answerable — the missing half is a
  disposition written back after the call.

## 22.33 HOW TO READ THE SHEET — settled 2026-08-25, do not relitigate

Patrick, emphatic: *"I don't want you or any other Claude I'm messing with to say
I can't understand the sheet or I can't read the sheet... that's almost the most
important thing we're dealing with here."* The short version is in CLAUDE.md so
every session loads it. This is the detail.

### What is PROVEN (tested this day, not assumed)
- `mcp__Google_Drive__get_file_metadata` on
  `1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA` returns the real file:
  "ATT FIBER LEADS", 7,726,944 bytes, owner patricksiado@gmail.com. **Access is
  real.**
- Full write→read round trip: created a sheet in his Drive with
  `mcp__Google_Drive__create_file` (CSV content) and read every value back with
  `mcp__Google_Drive__read_file_content`. Values came through exactly.

### The limitation to be honest about
The Drive connector reads a FILE, not a named TAB. It has no tab argument. So on
a multi-tab workbook you get what the connector chooses to return, and you cannot
say "give me Gold Confirmed" through that path.

**This is exactly why README and DASHBOARD were put in FRONT position** (janitor,
`_order_tabs`) and why `Precise Fiber` was moved LAST. Front-loading the small
summary tabs means the cheap read lands on something useful. It is an
architectural decision, not cosmetics — do not "tidy" the tab order back.

For tab-level addressing use, in order: the DASHBOARD numbers (usually enough),
`sheet_feed.py --tab "<name>"` (chunked JSON to GitHub, no Google auth), or
Autosheet when it has credits.

### The mistake made in this very session — do not repeat it
Autosheet returned `api-billing-empty-balance`, and I concluded and TOLD PATRICK
that I could not reach his sheet. That was wrong. I had never tried the Drive
connector. **One tool failing says nothing about the others.** Try every path
before reporting a limit, and never state a limit you have not personally tested
that day.

### Size, not permission
`Precise Fiber` is ~474k rows in a 7.7 MB file. Claude's spreadsheet ceiling is
around 30 MB, so the FILE is fine; the single tab is too long to swallow, and
pulling it whole is what killed Autosheet twice. Deliberately NOT attempted, and
should stay that way: ask for a bounded range, a ZIP, or read DASHBOARD.

### Still needing one click from Patrick (low priority now)
The three `BRIDGE — *` sheets use IMPORTRANGE and stay blank until he clicks
"Allow access" once per file. They were built before the Drive-connector path was
known. They are now a convenience for HIM on a phone, not the access route —
do not debug their blankness.

## 22.34 THE ECONOMICS, AND WHERE THE MONEY ACTUALLY IS (2026-08-25)

Patrick, on a day when door-to-door had just taken a setback and this channel is
"going kinda slow." His numbers, his words:

| Product | Pays |
|---|---|
| **Pack of phones (mobility)** | **~$2,000** |
| Business internet | ~$1,000 |
| Residential internet | ~$500 |

### The reframe that follows from his own data
Mobility pays **4x** a residential internet deal. And GREY dots — existing AT&T
fiber customers, which the legend says to skip as a lead — are the **best
mobility list in the business**: already AT&T, already on fiber, address on file,
and AT&T gives existing fiber customers a real bundle credit for adding a
wireless line (researched 2026-08-25: ~$25/mo off fiber, ~20% off wireless, 12
months, addresses must match).

**One run on 2026-08-25 classified 44,500 grey customers before lunch** and the
system filed every one under "ignore." Patrick has been asking to raise mobility
attachment; the list was already in his hands.

Grey stays a SKIP for *fiber* selling. It is a PRIME list for *mobility*.

### Staffing — the honest math
He has Filipino VAs willing to run the software. **Do not put them on the
software.** One laptop pulls millions of addresses a day unattended; discovery is
the one part that already scales without people. Ten operators produce ten times
more of the thing there is already too much of.

The constraint is **conversations**, not captures:
- 1 person part-time babysits several machines (they do hang and need resetting)
- 2–3 callers to START, aimed at the $2,000 and $1,000 products, not the $500 one
- Measure those first for two weeks, THEN scale — staffing ten against an
  unmeasured funnel is how the money goes

**Why "measure first" is not caution-for-its-own-sake:** the last measured batch
was Aug 21 — 100+ texts, **0 replies, 0 opt-outs**, still nothing four days
later. Nothing in the system records what happens on a call. Scaling a funnel
whose conversion nobody has ever seen multiplies an unknown.

### The size of the prize (researched 2026-08-25)
AT&T ended last year at **32M fiber locations**, expects **40M by end of this
year** — about **8M new locations in 2026, ~22,000 per day**. Organic run-rate 4M
/yr rising to 5M/yr through 2030, target 60M. Every new location is born GREEN.

**4M of that 8M is the Lumen acquisition** — locations that already have fiber and
simply become AT&T's. When it closes, ~4 million addresses turn sellable at once.
With a diff running you would see that wave the week it lands; without one you
hear it from a competitor.

### What is still missing (in priority order)
1. **The diff.** Sweep → wait → sweep → compare. It is the only way to know how
   much new fiber we FOUND, it powers the fresh-area detector, and it catches the
   ~22k/day that never make the news. Every row already carries Run ID +
   timestamp; nothing does the subtraction.
2. **Disposition writeback.** Until a call outcome lands next to the lead, "is
   this working" stays a feeling.
3. **Storage ceiling.** Google Sheets is 10M cells TOTAL across all tabs. Precise
   Fiber alone is ~5.7M at 474k rows × 12 cols. Footprint scale needs one row per
   ADDRESS (updated on color change) instead of one row per sighting — that fixes
   the ceiling AND makes the diff trivial.
4. **Widen the outage filter.** `optimus_web_intel.TERRITORY` is still a Texas
   city list. Territory is now the whole footprint (see CLAUDE.md); a cable
   outage anywhere AT&T sells is a phone/text selling event, even where we have
   no boots.

## 22.35 THE STORAGE CEILING — RESEARCHED, PLAN PARKED (2026-08-26)

**Status: PARKED. Patrick said "hold tight, remind me, I'll get back to it."**
Nothing below is built. Do not start it without his go-ahead.

### Where it stands the night this was written
The workbook is FULL. **1,911 parked batches** on the laptop, every write
failing, every run capturing perfectly and landing nothing. `FREE_SPACE.bat` is
written and deployed but **has never been run**. That is the unblock, and it
comes before any of the work below.

### The question he asked: is this a storage thing, and is it common?
Yes and yes. "Google Sheets as a database, outgrown" is one of the most common
failure modes there is. Optimus just hits it faster than most because a scanner
fills rows faster than humans ever could.

### THE CHEAP WIN, FOUND 2026-08-26 — DO THIS FIRST
**Google opened a beta in April 2026 that doubles the Sheets cell limit from
10M to 20M**, and it applies to EXISTING files, not just new ones. Register the
domain on a form, get allowlisted in waves. Opening big sheets also got ~30%
faster.

That is free headroom with no migration and no code. It does not change the
shape of the problem — a scanner will fill 20M too — but it buys months instead
of days. **Register before building anything.**
Source: workspaceupdates.googleblog.com/2026/04/faster-performance-and-doubled-cell-limits-in-Google-Sheets.html

### Sub-sheets that compile together: RESEARCHED AND REJECTED
Patrick asked about separate sub-sheets compiling into a master. It fails three
ways and should not be revisited:
  - IMPORTRANGE is one of the slowest functions in Sheets; past ~50 formulas the
    workbook crawls.
  - It needs a manual "Allow access" click PER FILE. The three BRIDGE sheets in
    his Drive are blank today for exactly this reason.
  - The footprint (~30M addresses) needs **37 spreadsheets** at 833k rows each.
    IMPORTRANGE cannot join them and nobody can query them.

### The shape change that actually fixes it (restates 22.34 #3)
**One row per ADDRESS, updated when its colour changes — not one row per
sighting.** Today every re-sweep APPENDS, which is why Precise Fiber is 474k
rows and climbing forever. Make re-sweeps UPDATE and the file stops growing once
an area is covered.

**This also makes the diff free.** Colour changed grey->green or copper->gold =
fiber just lit. That is the answer to "how do I find all the new fiber in the
footprint", and it is one shape change away. ~22,000 locations light up per day
and every one is born GREEN.

### The alternatives, priced (2026-08-26)
| Option | Verdict |
|---|---|
| 20M-cell beta | **First move.** Free, immediate, no migration |
| One row per address | **The real fix.** Stops growth; makes the diff trivial |
| BigQuery | Right endgame past 2-3 laptops. Google-native, free at this volume |
| Airtable | **Rule out on price** — $20-45 per editor per month, compounds with VAs |
| Baserow / NocoDB | Free and SQL-backed, but he would own a server |

### The pipeline he described, and what each stage costs
scrape on AT&T news -> AI detects new fiber -> DealMachine adds numbers ->
loaded to dialer and texted -> VAs qualify and warm-transfer to US closers ->
closed, followed up, entered in SARA Plus.

| Stage | State 2026-08-26 |
|---|---|
| Scrape guided by AT&T news | **DONE** — default behaviour, 21 states, cable outages ranked first |
| New fiber detected by AI | **NOT BUILT** — the diff. ~1 day, needs the shape change first |
| DealMachine adds numbers | Works manually. ~1 day to auto-enrich; SPENDS CREDITS, needs a daily cap |
| Load to dialer + text | **DONE** — 37 leads tagged into Dave's queue with notes |
| VA qualify -> warm transfer | **NOTHING EXISTS.** Scripts, routing, training — the real work |
| Close -> SARA Plus | Manual. No API seen for SARA |

### Multi-machine, settled 2026-08-26
Google's quota is **per SERVICE ACCOUNT, not per machine**, and every PC runs the
same `google_creds.json`. Two laptops each throttling to 50 writes/min sent
100/min against a ~60 ceiling and both crawled — it presents as "the network is
slow" or "AT&T is rate-limiting our IP", and it is neither. `--machines N` now
splits the budget. At 9 machines the write rate is fine (54/min) but the
workbook fills in ~31 minutes, so **storage is the wall, not the rate**. READS
are still unthrottled — that bites before 9 machines.

### The standing warning, unchanged from 22.34
Do NOT staff the software. One laptop pulls millions of addresses a day
unattended. The constraint is CONVERSATIONS, not captures. The last measured
batch (Aug 21, 100+ texts) got **0 replies and 0 opt-outs**, and nothing in the
system still records what happens on a call. Measure two weeks with 2-3 callers
aimed at the $2,000 mobility and $1,000 business products before adding anyone.

**And the best untouched asset is still GREY** — 44,500 existing AT&T fiber
customers classified in one run and filed under "ignore". Mobility pays ~4x a
residential internet deal.



## 22.36 THE NEWS-FOLLOW DISPATCH — FIRST FLIGHT (2026-08-27)

Built 2026-08-26 on Patrick's order ("I want new fiber discovered / build it
into the ai / 2 programs is enough / entire att footprint"). `follow_news_pass`
is now the hunter's DEFAULT: it pulls new-build + outage intel across the
21-state footprint, then flies the map to each named town and sweeps ~12 cells
before moving on. `--no-follow-news` or `--grid` restores the old behavior.
Patrick watched the first real flight and loved it: "it jumped to all the zips
on the list of new fiber builds... the zip code bounce may prove very
effective later."

Three findings from that flight, confirmed in code:

1. **Playwright clicks don't move the Windows cursor.** `search_zip` clicks
   and types via the DOM, so the visible hand never moves. Cosmetic — but it
   made the next two bugs look like "it did nothing".
2. **`search_zip` claims success without proof.** If no geocoder suggestion
   matches its selectors it presses Enter and `return True` — it NEVER
   verifies the map actually flew. Its own docstring records the previous
   version of this bug ("entered OKC but scraped elsewhere"). And
   `follow_news_pass` never zooms after flying: `zoom()` exists at line ~4680
   and the news path doesn't call it. Dots only render zoomed in, so the
   hunter can reach the right city at city height, see nothing, and hop on.
   Fix = verify movement (center coords or captured-feature flow) + zoom to
   dot level after each successful fly. WRITTEN LOCALLY, NOT PUSHED (Rule 0;
   Patrick is sending screenshots of the sequence first).
3. **Enter killed Chromium because the run had ENDED.** A finished target
   list falls out of `one_pass` to `input("Press Enter to close the
   browser...")`, buried under scroll. Fix queued: a finished news list rolls
   into a continuous sweep from the last target (a finished list must never
   mean an idle hunter — same law as an empty feed), and close should demand
   'q', never bare Enter.
