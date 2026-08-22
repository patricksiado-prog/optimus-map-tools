# Optimus Session Log

## 2026-08-22 01:30–02:30 CT — Claude
**SESSION GOAL:** Measure the Aug 21 send, then enrich + stage the Devonwood 25. Session opened at 1:30 AM CT so nothing could be texted (quiet hours 8am–9pm).

### Aug 21 close-rate measurement — the first real one
Pulled the full conversation index for T-OPTIMUS (4,685 conversations) sorted by last activity.

- The 100 most recently active threads are ALL from Aug 21, spanning 13:06–18:11 CT, and **every one is outbound-last**.
- Nothing has arrived in the location since 18:11 on Aug 21.
- **Replies: 0. Opt-outs/STOPs: 0.**

Batch composition by tag across those 100: 46 `beaumont`, 40 `optimus-fiber-biz`, 30 `fiber-sms-sent`, 11 `angleton` (the personalized "Hi {name} — Patrick with Optimus" copy), 6 `gold-dot`/`upgrade-140`, 5 `green-dot`/`fiber-500`.

**Two threads that look like replies in the inbox are business auto-responders, not humans:**
- Boost The Heights — "Boost here! Sorry we missed your call…" (missed-call autoresponder)
- Cleanzen Houston — "We are sorry we missed your call… Joy" (missed-call autoresponder)

Do not count either as engagement. Zero opt-outs on 100+ sends is worth noting on its own — the copy is not provoking STOPs.

### Devonwood 25 — enriched and staged
All 25 addresses on Devonwood Ln carry ZIP 77070, so `enrich_address` worked on every one. **25/25 matched, 100% hit rate.**

**Cost: 39 credits, not the ~150 estimated.** 14,217 → 14,178. Dedupe within the billing cycle did most of the work.

Results written to tab `Devonwood Campaign — Aug 21`, columns G/H/I/K/L, with `{FIRST}` resolved in the column J message per row:
- **20 rows READY - NOT SENT** (owner name + wireless number + DNC status)
- **5 rows BLOCKED:**
  - rows 5, 13, 15 (8226, 8203, 8130) — **landline only**, do not text, Twilio 30006 risk
  - rows 4, 21 (8227, 8115) — property matched but DealMachine returned **zero contacts**

Of the 20 textable: 13 DNC-clear, 7 DNC-listed. All messages carry opt-out language.

### Hard-won facts from this session
- **`enrich_address` real cost is 1–2 credits per address, not the ~6 written in older parts of the brain.** Across 25 addresses it averaged 1.56. A 4-owner household (8114) was the single most expensive at 4.
- **`enrich_address` has no `estimate_cost` parameter** — unlike `property_search`/`people_search`/`enrich_name`, you cannot preview its cost for free. Probe one address to measure, then batch.
- **Landline rate on residential skip-trace is roughly 3 in 25 (12%) with no wireless alternative on file.** Budget for that shrinkage on any residential text batch — a 25-row list is not a 25-message send.
- **`att.net` in an owner's email is a usable corroborating signal for the GOLD (copper customer) read.** Two of the five gold dots came back with it — 8218 Devonwood (RUFBURT@ATT.NET) and 8210 Devonwood (SHARON.DURFEY@ATT.NET).
- **The same signal appeared on a GREEN dot — 8230 Devonwood, owner email LAFLEUR.D@ATT.NET.** Given gold currently reads 2.05% of the file against 9–11% visible by eye on the map, this is a data point supporting the under-call theory. Flagged in the row's Notes. It is suggestive, not proof — att.net addresses persist long after someone leaves AT&T.
- **`get_sms_reports` is dead on this connector** — GHL returns 404 on `/reporting/sms`. Measure sends by walking the conversation index instead.
- **`search_conversations` returns max 100 per call with no offset parameter**, but it is sorted by last-message-date descending, so the top of the list is a reliable read on the most recent activity in a location.
- **Workflow `Optimus Dave` (published, the primary dialer) has `triggers: []`** — manual enrollment only. Its call windows are Mon–Fri 09:00–17:00. It will not auto-grab newly created contacts. Other published workflows were not individually inspected.

### Blocked this session
- **`send_later` / scheduling was denied by the auto-mode classifier again.** Same as the previous session. A morning send could not be queued, so the Devonwood batch has to be fired by a live session inside 8am–9pm CT.

### State at session end
- `Gold Biz Campaign — READY` — 36 rows still READY - NOT SENT, verified intact, phones present as raw digits. Untouched this session.
- `Devonwood Campaign — Aug 21` — 20 READY, 5 BLOCKED, nothing sent.
- DealMachine: 14,178 credits remaining, cycle ends Sep 2.

---

# BRAIN CANDIDATE — PART 22 (2026-08-22, overnight session)

**Written here, not into BRAIN.md, on purpose.** The BRAIN.md in this repo is a
50-line stub last touched 2026-05-02. Patrick reported pushing a 2,889-line
BRAIN.md as commit c73d2f0 with a Part 21; that commit is not a valid object in
either optimus-map-tools or go-high-level-mcp-2026-complete, and the largest
BRAIN.md on any branch of this repo is 231 lines
(`claude/att-fiber-leads-dedupe-lqr67f`). Rather than fragment the brain across
two files, this section is parked here to be merged once the real file is
located. Everything below was measured this session, not recalled.

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
