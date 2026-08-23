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
