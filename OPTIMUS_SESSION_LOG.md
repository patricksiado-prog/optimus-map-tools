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

**Findings from this session are recorded in `BRAIN.md` as Part 22.**
They are kept there rather than duplicated here so there is exactly one
current copy of each fact.
