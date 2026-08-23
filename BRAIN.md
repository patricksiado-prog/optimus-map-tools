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
