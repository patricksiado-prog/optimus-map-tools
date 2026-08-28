---
name: daily-coverage-gap
description: Build Optimus's twice-daily coverage-gap report — cross-reference the leads sitting in the ATT FIBER LEADS sheet against what has actually been texted or called in GoHighLevel, against AT&T fiber build news, and against live cable/competitor outages, then email it to Patrick, Dave and Churchie — a morning edition that says what to work today and an evening edition that catches the replies that came in and have not been called back. It is also the daily manager of the machine, the data and the growth plan: it checks that GoHighLevel can actually send before anything else, audits data integrity, says where the next deal comes from, and carries three daily tips (a GHL tech tip, an AT&T fiber technology or phone benefit, and a sales tip). Use this whenever Patrick asks what hasn't been worked, which leads are going stale, where to point the scanner, what's new in fiber news, whether a competitor is down, what the team should do today, or for the daily/coverage/gap report by name. Also use it when he asks a narrower version of the same question — "what are we sitting on", "who hasn't been called", "any new builds", "is Comcast down" — because each of those is one section of this report and the other sections are the context that makes it actionable. Also use it when he asks whether texting is working, why a daily email stopped arriving, for a GHL or AT&T or sales tip, or where to grow.
---

# Daily coverage gap

Optimus captures leads far faster than it works them. On 2026-08-27 the sheet
held 772,768 rows and 40 people who had replied YES were sitting uncalled, the
oldest since June 30. A third of everyone who ever said yes had gone unreachable
before anyone dialed them. **The bottleneck is not lead supply. It is knowing
which of the leads we already own are worth touching today.**

That is what this report answers, by putting four things side by side:

| Source | Question it answers |
|---|---|
| The sheet | What do we own? |
| GoHighLevel | What have we actually touched? |
| Fiber build news | Where is there green we do NOT own yet? |
| Competitor outages | Whose internet is broken *right now*? |

The gap between column 1 and column 2 is the backlog. Column 3 aims the
scanner. Column 4 is the only one with a clock on it — a cable outage is a
same-day reason to call, and it is stale tomorrow.

Read `optimus-brain` first if you do not already have the dot legend, the sheet
IDs and the texting rules in context. This skill assumes them.

## Before you write a line: two rules that outrank the report

**Every number is a live read, today.** Never carry a figure forward from
yesterday's report or from memory. If a source cannot be reached, the report
says `COULDN'T READ — <why>` on that line. A guessed number is worse than a
missing one, because Patrick will act on it.

**No commission figures in anything except Patrick's copy.** Ed's standing
instruction (2026-08-27) is that commission numbers stay away from the VAs, and
Patrick agreed. Say "the upgrade" and "the higher-value sale", never $140 or
$500 or anything a rate can be reconstructed from. This is why the report is
assembled once and then **sent as three separate emails** rather than one with
three recipients — see Who gets what.

## 1. What we own — reading the sheet

`ATT FIBER LEADS` = `1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA`

**The direct read does not work and you should not burn time rediscovering
that.** The Drive connector has no range or tab parameter, so it exports the
whole workbook from tab 1, and `Precise Fiber`'s 645k+ rows consume the entire
character budget before tab 2. `DASHBOARD` and `README` — which older notes say
to read first — are not in the live tab list.

Use these instead, in order:

**a. Tab row counts** — `optimus/_feed/sheet/tabs.json` in the hunter repo
(`patricksiado-prog/Go-High-Level-MCP-2026-Complete`, branch
`claude/optimus-map-tools-setup-6dcl6o`). Public GitHub, no Google auth. Gives
every tab and its row count.

**Check its `at` timestamp and say how old it is.** This file is only rewritten
when the Maps Scraper runs. If it is two days stale, the counts are two days
stale, and the report must say so rather than presenting them as today's.

**b. Is the sheet actually growing?** `get_file_metadata` on the workbook
returns `modifiedTime` and `fileSize`. Compare `fileSize` against the previous
report's figure (keep it in the report so tomorrow can diff it). Precise Fiber
runs about **13 bytes per row**, so a 12,000-byte gain is roughly 900 new rows.
Rough, but it is the only live growth signal available without a tab read, and
it settles "is capture working" in one call.

**c. Capture truth** — `optimus/_feed/latest.json`. Report `classified_green`
and `written` **together, always**. They measure different things and the gap
between them is the story:

- A run classifying 306,332 green with ~800 rows landing is not broken. It is
  **re-sweeping ground we already own**, and dedupe is correctly throwing the
  rest away. The fix is new territory, not a code change.
- `written: 0` in `latest.json` does **not** prove nothing was saved. The
  uploader is a separate process and does not report into that counter. Confirm
  against the workbook's `modifiedTime` and `fileSize` before ever telling
  Patrick writes are broken — this exact mistake was made and corrected on
  2026-08-28.
- Also surface `auth_expired` and `last_phase`. If the last heartbeat says
  `LOGGED_OUT`, nothing is capturing at all and that belongs at the top of the
  report, not buried in a stats table.

## 2. What we've touched — GoHighLevel

Location `xZj500PjsflIQg2j9f9D`, via `command_connector` (the
`FRONTLINE_CONNECTOR` tools 403 on this location).

`search_contacts` matches tags **and** the source field, so a query is a blunt
instrument — searching `gold` returns businesses named "Golden Dryer Service".
Derive the colour from tags, never from the search text.

**Worked** — any of: `fiber-sms-sent`, `att-fiber-texted`, `warm-chase-sent`,
`fiber-dave`, `power dialer queue`, `zack-dialer-source`, `biz-call`.

**Answered** — `replied-yes`, `hot-lead`, `priority-callfirst`, `callback`,
`appt booked`.

**Closed or dead** — `sold`, `sold-won`, `not interested`,
`wavv-not-interested`, `excluded-vertical`.

**Unreachable, and this is where the money leaks** — check `dndSettings`, not
just tags. `SMS.status = "permanent"` with `STOP_KEYWORD` is a hard opt-out.
`SMS.status = "active"` set by workflow `bcaa33a6-cb0f-4b93-b749-8852e8bfe0a4`
is the STOP workflow and means the same thing. A contact can carry `hot-lead`
and be opted out at the same time — that combination is a lead dying in the
queue, and counting it as workable is the failure this report exists to catch.

**The number Patrick actually wants** is answered-but-never-closed, and how old
the oldest one is. Measured 2026-08-22: 22 `replied-yes`, 7 unreachable.
Measured 2026-08-27: 25 and 8. Report the trend, not just today's count —
a rising unreachable share means callbacks are too slow, which is a management
problem, not a data problem.

## 3. New builds — the news

`WebSearch` works from a Claude session and is the reliable path.
`optimus_web_intel.py` cannot be tested from a sandbox — `news.google.com`,
`bing.com` and `reddit.com` are refused by the agent proxy — so do not conclude
the feed is broken from here.

Search for the last 24-48 hours. Useful shapes:
- `AT&T fiber expansion <metro> <month year>`
- `AT&T fiber now available <city>`
- `"fiber" new construction <suburb> AT&T`

**Corporate press releases are almost useless for aiming a sweep and you should
say so rather than padding the report with them.** "725,000 locations across 38
neighborhoods" cannot point a scanner at a street. What is actually actionable:
a named town, subdivision or ZIP that has just been lit, especially in a metro
we have never swept.

Cross-reference every hit against what we own. A build in a metro already in the
sheet is noise. A build somewhere we have never scanned is the scan target, and
that is the line worth writing.

Territory is all **21 legacy ILEC states**. The Lumen states — AZ CO IA ID MN MT
NE NM OR UT WA — are **not** ours, however much fiber news they generate. Ignore
them.

## 4. Outages — the only same-day trigger

A household whose cable has been out since this morning is the most receptive
fiber prospect that exists, and tomorrow they will have forgotten. This section
is why the report is daily rather than weekly.

Search for live outages from Comcast/Xfinity and Spectrum in the markets where
we have leads — Houston, Beaumont, Angleton, La Porte, plus any metro from
section 3.

Sources that return a same-day answer:
- `istheservicedown.com/problems/comcast-xfinity/...` (has per-county pages)
- `downdetector.com`
- local TV news, which covers large outages fastest

**Report "no outages today" plainly when that is the answer.** A quiet day is
useful information and it keeps the section honest; a section that always finds
something is a section nobody trusts.

When there *is* an outage, the deliverable is not the outage — it is the
**overlap**: which of our green pockets sit inside it. Name the streets or ZIPs
and put them at the top of the call list.

## 5. GHL health — you are the manager of the machine

Run this **first**, before the sheet, before the news. If GHL cannot send, every
other section of the report is describing work that is not happening.

This section exists because of a real outage. On 2026-08-27 the account stopped
texting for over a day and nobody noticed: outbound SMS had been routed to a
placeholder conversation provider named **"SMS Demo Provider"**
(`6958de9aca6f38b289d7f65e`), every send returned `405`, and the contacts still
got tagged as though they had been messaged. Patrick spent a Zoom call with
support chasing an A2P problem that did not exist. Check the machine daily so
that never costs a day again.

**The five checks, in order:**

1. **Is the provider right?** The telephone / conversation provider must be
   **LeadConnector (LC Phone)**. If a custom provider is selected, sending is
   broken even though everything looks normal in the UI.
2. **Are recent sends real sends?** Pull recent outbound messages and look at two
   fields. A healthy send is `messageType: TYPE_SMS` with a `+1…` number in
   `from`. A broken one is `messageType: TYPE_CUSTOM_SMS` with a **provider name**
   in `from`. One glance settles it — do not theorise about carriers first.
3. **Any failed sends?** Count messages with `status: failed` in the last 24h and
   quote the `error` string verbatim. Read the code:
   - `405` — refused outright, the message never left GHL. Routing/config fault.
     Never carrier filtering.
   - `30006` — landline. We texted a number we should have called.
   - `30007` — carrier filtered it as spam. That IS a content problem: look at
     the template.
4. **Numbers and money.** Phone numbers still present on the location, and the
   billing wallet funded. Both are one call each and both silently kill sending.
5. **Ghost-sent contacts.** Anyone tagged `fiber-sms-sent` whose only outbound
   messages failed. Those rows read as worked and are not — they will get skipped
   by the team forever. Name the count and offer to strip the tag.

**Report it as one line when healthy.** "GHL: sending healthy, provider
LeadConnector, 0 failed in 24h." A green light stated plainly is what makes the
red light believable. When it is red, that goes at the very top of **Do this
today**, above outages.

**Also watch for the settings that drift.** Patrick, 2026-08-28, after support:
*"lead connector got clicked off and some other odd setting."* Settings get
clicked off by accident, by a snapshot push, or by a support agent mid-call. The
provider is the one that breaks sending outright; check it every single day.

## 6. Data integrity — you are the manager of the data

The lists are the product. A list with a wrong number in it costs a dial and a
reputation; a list that lies about what has been worked costs the lead entirely.

**Check daily:**

- **Writes are landing.** From `optimus/_feed/latest.json`: `written` and
  `failed_writes`. Report both, always. "Classified 126,628" means nothing if
  `written: 0` — that is brain rule 7 and it has misled a session before.
- **Sheet headroom.** The workbook has a hard 10,000,000-cell ceiling and has hit
  it. Report roughly how close it is. A tab is billed for its whole grid, not its
  rows.
- **Parked rows.** Any rows parked to disk awaiting replay, and whether the last
  launch replayed them.
- **Placeholder text in data fields.** Never allowed. A column once held the
  literal text `(all DNC)` where digits belonged and gold could not be texted for
  a day. Scan for non-numeric junk in phone columns and flag it loudly.
- **Rows that cannot be mailed.** Captured rows with no city/state/ZIP, and
  whether the backfill is still healing them.
- **Duplicates.** Contacts sharing a phone or email under different names.
- **DNC that is actually unknown.** Column F of `Fiber Green Biz` is a hand-typed
  call-status field, not a DNC check. Never report those rows as DNC-clear.

Where a check cannot run, say `COULDN'T READ — <why>`. Never guess a number and
never carry one forward from yesterday.

## 7. Sales expansion — where the next deal comes from

The gap sections say what is not being worked. This one says where to grow.

**Capacity math, honestly.** Dials available today × the connect rate we actually
observe × the close rate we actually observe. If the arithmetic does not reach
the goal, say so and name the constraint — reps, numbers, or scan volume. Do not
dress it up. The usual answer is that resi is capped by scanning and business is
capped by qualification, not by effort.

**Which pockets are producing.** Rank recent closes and replies by pocket, not by
row count. A pocket that produced two replies from forty dials outranks one that
produced none from three hundred.

**Where to scan next.** Never point the scanner at ground already swept — dwelling
on a worked pocket simulated 80% worse than sweeping outward. Prefer a metro with
no capture history, and prefer gold density as the freshness signal: thick gold
with little grey means fiber was lit recently and nobody has converted it.

**The business match.** Report the count of `Maps Businesses` rows that match a
scanner dot — that join is what turns ~38.5k blind rows into confirmed-fiber
business leads, and Patrick calls it the most important thing. Until the software
does it automatically, report that it is still not running rather than letting it
disappear.

**Channel coverage.** Who was texted but never called. Who was called but never
emailed. A lead worked on three channels converts far better than the same lead
texted once, and the enrichment already paid for the email address.

## 8. The scoreboard — the same numbers, every single day

Patrick, 2026-08-28, after the first full audit: *"add that stuff to my daily
emails."* The audit found things nobody had been watching. The fix is not to
audit again — it is to put those numbers in the email every day so a change gets
noticed the day it happens instead of a month later.

**Rules for the whole scoreboard:**

- **Same rows, same order, every day.** A row that disappears when the number is
  bad is worse than no scoreboard.
- **Read live. Never carry a figure forward** from yesterday's email or from
  memory. If a source is unreachable the row says `COULDN'T READ — <why>`.
- **Show the benchmark next to the number**, so it reads itself. A number alone
  needs a person to interpret it; a number beside its band does not.
- **An alarm row goes to the top of "Do this today"**, not just the table.
- **Cost rows are Patrick's copy only.** Spend is not a VA's business.

### Capture — from `optimus/_feed/latest.json` and the run feed

| Row | Source | Benchmark / baseline | Alarm when |
|---|---|---|---|
| Addresses classified, last run | `capture_truth.classified` | 452,736 in one 12h sweep (27 Aug) | Run is much shorter than the sweep window — a 3-second run means it launched and quit |
| Green / Grey / Unknown | `stage_counters` | 306,332 / 145,066 / 1,338 | — |
| **Penetration %** | grey ÷ (green + grey) | **32.1%** as of 27 Aug | Moves more than a few points — either new territory or a classifier change |
| **Gold classified** | `classified_gold` | Gold capture verified working 24 Aug | **ZERO IS AN ALARM.** Gold is the easiest sale we have; zero across a large sweep is not credible |
| Undecoded build codes | `undecoded_codes` | `ip-co` = 2,676 outstanding | Any new code appears, or the count grows |
| Auth expiries | `auth_expired` | 4 in the 27 Aug run | Above zero. Each one is a blackout where the map returns a login page |
| Written / failed writes | `dedupe` | Report **both**, always | Never diagnose the write path from `written: 0` alone — the uploader is a separate process. Confirm with sheet file size and modified time |
| Map ready | `map_ok`, `zoom_ok` | — | Either is false: capture may still work off the serviceability API, but aiming is blind |

### Pipeline — live read of GoHighLevel

| Row | Baseline 28 Aug | Alarm when |
|---|---|---|
| Opportunities open | 3,706 | — |
| **Won** | **0** | **Still zero. This is the standing alarm** until dispositions start |
| **Lost** | **0** | Same |
| Days since any disposition | never | Anything above 2 |

**Say this plainly whenever won and lost are both zero:** the pipeline is
write-only, so close rate, cost per customer and profit per activity cannot be
computed. Do not soften it and do not substitute a proxy — an invented ratio is
worse than an admitted gap.

### Outbound — GoHighLevel messages and calls, last 24h

| Row | Benchmark | Alarm when |
|---|---|---|
| Texts sent / delivered / failed | — | Any `TYPE_CUSTOM_SMS`, or any failure with a provider name in `from` |
| Text delivery % | — | Below 90%, or unmeasurable |
| Connect rate | 8–12% generic list, **18–22% verified direct-dial** | **Below 7% — that is a data, timing or caller-ID problem, not a rep problem.** Say so in those words |
| Dials per booked meeting | 25–35 typical, 12–18 top performers | Above 35 |
| Meeting-set rate | 2–3% average, 6–10% top | Below 2% |
| Replies today not yet called back | zero is the target | Any, and this leads the PM edition |

### Inventory — the sheet

| Row | Baseline 27 Aug | Alarm when |
|---|---|---|
| `Maps Businesses` unmatched | 38,481 | The match still is not running |
| Business-to-dot matches found | not built | Report "not built" rather than omitting the row |
| `Upgrade Orange Biz` | 62 | Not growing. Gold businesses are the most valuable slice we have and that tab is nearly empty |
| Contacts tagged sent that never delivered | unaudited | Above zero |

### Cost — Patrick's copy only

| Row | Baseline | Note |
|---|---|---|
| DealMachine credits remaining | 11,660 of 30,000, cycle ends 2 Sep | Flag when the cycle is within 5 days and credits are unspent — they do not roll over |
| Credits per callable lead | **~2.6** (309 rows, ~800 credits, Beaumont) | The one unit-economics figure that is solid today |
| Cost per customer | **NOT COMPUTABLE** | Requires closes to be recorded. Print the words, not a guess |
| Profit per activity | **NOT COMPUTABLE** | Same |

Keep printing the two NOT COMPUTABLE rows every day. They are the most useful
lines in the table — they are the standing reminder of what recording won and
lost would unlock, and the day they turn into real numbers is the day the
business becomes measurable.

## 9. The three daily tips

Every **AM** edition carries exactly three, one of each. Patrick asked for these
by name on 2026-08-28. They are short on purpose — a rep reads them on a phone
between dials.

1. **GHL TECH TIP** — one thing about the CRM that makes the day easier or
   prevents a silent failure.
2. **AT&T FIBER TECH / PHONE BENEFIT** — one true fact about the product that a
   rep can say out loud on a call. This is ammunition, not trivia.
3. **SALES TIP** — one behaviour that closes more.

**Rules for all three:**

- Two to four sentences. No preamble.
- It must be **true**. Never invent a speed, a promo, or a feature. If a number
  cannot be verified today, use a tip that needs no number.
- Never repeat a tip within 30 days. Track which have run.
- Prefer a tip tied to something that actually happened this week — a failure
  we just had, a competitor outage, a deal that closed.
- **Money rule:** customer-facing pricing and promos ARE allowed in tips, because
  reps cannot sell without them. **Commission, payout, per-lead value and revenue
  figures are never in a rep's or VA's copy** — that is Ed's standing rule about
  Ara and it is about what we get paid, not what the customer pays.

Refresh the libraries below with `WebSearch` when a tip touches a current price,
promo or speed tier — those change. The mechanics do not.

### GHL tech tip library

- A `405` on send means the request was refused outright and the message never
  left GHL. That is always routing or config, never a carrier.
- Two fields tell you if sending is healthy: a real send is `TYPE_SMS` with a
  phone number in `from`; a broken one is `TYPE_CUSTOM_SMS` with a provider name.
- Never write your own opt-out line. GHL appends `Reply STOP to unsubscribe.`
  automatically, and a doubled STOP line is the clearest tell that no human wrote
  the message.
- A2P has three gates: brand approved, campaign approved, and numbers attached to
  that campaign. "Your brand is approved" answers none of the other two.
- `30006` means you texted a landline. It fails and it counts against the sending
  number. Check the line type before the send, not after.
- `30007` means a carrier filtered the message as spam. That is a content
  problem — shorten it, personalise it, and take the price out.
- `lastMessageBody` only holds the most recent message, so scanning it will never
  find someone who replied and then got answered. Use tags and pipeline stage.
- A contact can carry `hot-lead` and be opted out at the same time. Always read
  `dndSettings` before counting a lead as reachable.
- A workflow can select its own SMS provider that overrides the account default.
  Fixing the account setting does not fix a workflow that has one hard-selected.
- A snapshot push can overwrite sub-account settings, including the telephone
  provider. Re-check sending after any snapshot.
- Duplicate contacts are matched on email and phone. Importing a list with a
  differently-formatted number creates a second record and splits the history.

### AT&T fiber tech / phone benefit library

- **Symmetrical speed is the real difference.** Fiber uploads as fast as it
  downloads. Cable does not — coax is asymmetric by design, so upload lags badly.
  That is the single most honest fiber-vs-cable line there is.
- **Upload is what people actually feel**: video calls that do not freeze, cloud
  backup, security cameras, and a card reader that does not hang. Ask what they
  do that pushes data up.
- **Fiber does not degrade with distance.** Light loses almost nothing over the
  run, so a customer far from the office gets the same speed as one next door.
  Cable slows the further you sit from the node.
- **No shared-node slowdown at 7pm.** Cable neighbours share bandwidth on a node;
  fiber is far less affected by congestion, weather and interference.
- **AT&T Fiber runs on XGS-PON**, which is what makes the multi-gig tiers
  possible. Tiers are 300 Mbps, 500 Mbps, 1 GIG and 5 GIG.
- **AT&T has already hit 20 Gbps symmetric** on a production network using
  25GS-PON in trials. The fiber going in the ground now has enormous headroom —
  useful against "I don't need that much speed."
- **Bundling wireless takes 20% off the fiber bill** — roughly $15–$25 a month
  depending on tier, and AT&T markets savings up to about $420 a year. Bundled
  fiber starts around $35/mo before taxes and fees.
- **Bundling also includes Internet Backup at no cost**, which matters to anyone
  who works from home or runs a register.
- **AT&T Phone – Advanced is the landline answer.** It keeps the customer's
  existing handsets and their number, but delivers dial tone over wireless or
  broadband instead of copper. Starts around $45/mo.
- **It has 24-hour battery backup and E911 location**, plus Call Protect spam
  blocking, caller ID, call waiting, call forwarding and 3-way. That backup line
  is what settles the older customer who is scared of losing the phone in an
  outage.
- **The copper clock is real and public.** AT&T is exiting copper across most of
  its wireline footprint by **end of 2029**, and aims for **no copper customers
  in wireless-first areas by end of 2027**. You are giving them a heads-up, not
  a pitch.
- **Migration happens either way — timing is the only thing they control.** That
  sentence is the whole gold pitch in one line.

### Sales tip library

- **Any reply gets a call the same hour.** People have opted out while waiting on
  a callback. The reply is the buying signal; the delay is what kills it.
- **3-way the warm one.** Do not finish it alone and do not promise a callback —
  conference Patrick in live, or Ed, Zack or Valmore. A warm customer cools fast.
- **Lead with copper retirement, not the promo.** It is true, it is urgent, and it
  reads as a heads-up. "Great news!" reads as a blast.
- **Never quote a flat price.** Residential is "in the $20s to $30s for the first
  year, I'll confirm your exact price before anything is ordered." Business is
  priced by speed tier — never put a residential figure on a business.
- **Gold is the easier sale.** They are already a customer on copper, so there is
  no competitor to beat. It is an upgrade, not a switch.
- **Text two or three times, spaced days apart, each one written fresh.** One text
  and done leaves replies on the table. Stop the moment someone replies or opts
  out.
- **Fewer better names beats more names.** A rep working 60 right numbers beats a
  rep working 300 wrong ones, and a huge list burns their day on people who
  cannot buy.
- **Read the tags before you dial.** `absentee-owner` means they do not live
  there — ask about the property, never "your home".
- **Never pitch a connection at a vacant house.** Talk to the owner about the
  property instead.
- **Ask a business what their upload does today.** They will tell you the pain
  before you have to sell anything.
- **Disposition honestly, immediately.** A lead marked wrong is worse than a lead
  not marked at all, because the next person trusts it.
- **A competitor outage is the only same-day clock we get.** A household whose
  cable died this morning is the most receptive prospect there is; tomorrow they
  have forgotten.

## Report structure

Use this shape. It is ordered by what a person should do first, not by how the
data was gathered.

```
# Optimus — coverage gap — <date>

## Do this today
<3 bullets max. Outage overlaps first, then the oldest unworked answered lead,
then anything time-boxed. If there is nothing urgent, say so — do not invent
urgency.>

## The backlog — what we own but have not worked
<answered-but-never-closed, with the oldest date. Unreachable count and the
trend. Then the big pools: green / gold / grey / businesses, with row counts
and how stale the counts are.>

## GHL health
<one line when green: provider, failed-send count in 24h. When red, this moves
to the top of "Do this today". Always name ghost-sent contacts if any.>

## Capture — is the machine working
<classified vs written, sheet growth in bytes and approximate rows, auth
failures, and the current phase. One line saying whether the sweep is on fresh
ground or re-scanning.>

## Data integrity
<writes landing, sheet headroom, parked rows, duplicates, placeholder junk,
rows that cannot be mailed. Silence here is a pass, but say so.>

## Where to grow
<capacity math and the real constraint, which pockets are producing, where to
point the scanner next, the business-match count.>

## Scoreboard
<the fixed tables from section 8. Same rows every day, live reads only, benchmark
beside each number. Alarm rows also appear at the top under "Do this today".
Cost rows in Patrick's copy only.>

## New builds worth scanning
<named places only. If the news gave nothing aimable, say that in one line.>

## Outages right now
<overlap with our pockets, or "none reported today".>

## Couldn't read
<every source that failed and why. Empty is fine and good.>

## Today's three  (AM edition only)
**GHL TECH TIP —** <2-4 sentences>
**AT&T FIBER TECH / PHONE BENEFIT —** <2-4 sentences>
**SALES TIP —** <2-4 sentences>
```

## 10. Tasks out of the inbox

Patrick, 2026-08-28: *"use my activities to help w production make suggestions
on tasks based on email"*. His inbox is where commitments get made and then
lost — a support ticket that blocks a campaign, a rep asking for leads, a
renewal about to hit. Read the last 7-10 days of `in:inbox` (skip promotions and
social) and pull out only what has an **action attached to it**.

What actually qualifies:

- **Anything blocking production.** A GoHighLevel campaign rejection, a Twilio
  or A2P registration problem, a suspended number, an API deprecation with a
  date. These stop money and they hide in support threads. Put them first.
- **A person waiting on him.** A rep asking for leads, a partner whose email is
  unanswered after 2+ days, a customer question in a thread that died. Name the
  person, the date, and what they asked.
- **Money with a date on it.** Invoices due, overdue notices, renewals,
  collections, trials converting. Amount and the day it hits.
- **His own commitments.** Search `in:sent` too — things he said he would do.
  An instruction he gave the team that nobody executed is the same as an
  unfinished task, and he will assume it is done.

What does not qualify, and should not pad the section: newsletters, receipts,
delivery notifications, surveys, marketing. If there is nothing actionable, say
"nothing new" — that is a real answer.

**Cross-check every instruction he gave against whether it happened.** On
2026-08-27 he emailed the team "I've got 2500 upgrade gold dots yall get speedy
dialing them ... Give him access and load in dialer for him plz". Speedy
(`sophiajones51419@gmail.com`) was never given access, because his address only
ever appeared in that one thread. Patrick had no way to know it had not
happened. That is exactly the class of miss this section exists to catch.

## 11. Activities and production

The other half of the same request: use what he logs to find what actually
drives output.

`LIFE LOG` (`1rwFjqK-oG8YuvNHFE_-4F4JuGg8JCzmE3RnjCeaFiZU`) has both the inputs
and the outputs on the same row — Workout, Food, Sober, Bible/Prayer next to
Dials Made, Leads Worked, Deals, Revenue. Once there are two or three weeks of
rows, that is a real answer to "what kind of day produces a sale": whether the
days he trains are the days he dials, whether deals cluster after a gym morning.

**Right now it cannot be answered and you must say so rather than implying a
pattern.** As of 2026-08-28 there are three dated rows (08-19 to 08-21), most
cells blank, one deal ever logged. Three rows is an anecdote. Report what is
actually in there, name the gap in one line, and move on.

What you CAN do today without waiting for data: report the input/output pair for
whatever days exist, so the connection becomes visible and logging starts to
feel worth doing. "You logged 1 lead worked on 08-19 and closed the Beaumont
deal the same day" is more motivating than an empty trend line, and it is true.

## Patrick's personal block — his copy only

Patrick, 2026-08-27: *"combine my stuff to an am pm / daily reflections aa goals
Bible stuff / plus all the work stuff"*. His two emails now carry both. This
replaced the standalone 8am brief — he does not want a third email.

**None of this ever appears in Dave's or Churchie's copy.** It is his recovery,
his goals and his health. Sending it to staff would be a real breach of trust,
and it is easy to do by accident if you assemble one body and vary the
recipients — which is the same failure mode as the commission figures.

Source for goals, food and activity is the **`OPTIMUS DAILY LOG`** Google Doc,
`1ZFFm58hjmJJTVF0GPs-TvUMgCq9qHMA4J9j-2Zv3Bk0`. GOALS sit at the top as a
standing block he rewrites when they change; dated FOOD / ACTIVITY / NOTES
entries run newest-first below.

**If he did not post, say so in one line and move on.** Do not nag, do not ask
why, do not repeat it in both editions. As of 2026-08-28 the GOALS block is
still empty bullets, so goal-checking has nothing to check against — state that
once, plainly, rather than inventing goals or silently skipping the section.

### Morning — reflection, passage, goals, yesterday's log

**The reflection is written fresh every day.** Never reproduce an entry from the
AA *Daily Reflections* book, *Twenty-Four Hours a Day*, or any published reader
— those are copyrighted and, more to the point, a photocopy is not a reflection.
Write a few sentences that could only have been written today.

Tone, and this matters more than the content: **steady, no advice, no praise, no
questions back.** He is not looking for a coach at 7am. Something to sit with,
not something to answer. Never tell him to rest, slow down, or stop working —
that is a standing rule about how he wants to be worked with, and it holds here
too.

**Bible passage** — a short one, quoted plainly with the reference. Same
restraint: let it stand on its own. No sermon, no three-point application, no
tying it back to his sales numbers. If a line of context genuinely helps, one
line. This section is newer than the rest, so if he wants a different shape —
a set reading plan, a psalm a day, longer passages — take the steer.

**Goals** — read the standing block, check each against what the work sections
actually show. That is the point of keeping them in the same email as the
numbers: "capture is up, goal says convert not collect" is a real observation.

**Yesterday's food and activity** — estimated calories and protein, and the
week's trend. Estimates are estimates; they are for the trend, not precision.
He writes it however it comes out ("2 tacos and a coffee") — read it that way.

### Evening — shorter

The evening personal block is deliberately light. He has been working all day
and the work sections are the substance at 5:30pm.

A brief evening reflection in the same voice — AA's nightly inventory is a real
practice and a natural fit, but keep it to a few sentences and keep it free of
verdicts. Then today's activity as logged, if he posted it, and one line on
goals only when the day actually moved one.

No Bible passage in the evening unless he asks for one. One a day is a
practice; two is homework.

## Two editions a day

Patrick, Dave and Churchie all get both. The two editions answer different
questions, and running only one of them loses the thing that actually leaks.

**MORNING — 7am Central — "what do I work today"**
Aim the day before dialing starts. Lead with anything on a clock: a competitor
outage overlapping a pocket we own, then the oldest reply still waiting on a
callback, then the queue itself.

**EVENING — 5:30pm Central — "who replied today and has not been called back"**
This is the one that protects the money. A third of everyone who ever replied to
us went unreachable before anyone dialed them, and the gap is almost always
overnight — someone answers at 2pm, nobody calls, by tomorrow they have moved on
or opted out. The evening edition exists to make that impossible to miss.

Its first section is always **replies received today that have not been called
back**, named, with the time they came in. If that list is empty, say so in one
line — that is a good day, not an empty section.

Then: what actually got worked today (calls made, texts sent, dispositions
written), what is still sitting untouched, and the top of tomorrow's queue so
nobody starts the morning deciding what to do.

5:30pm is deliberate. It is after the dialer window closes at 5, and still
comfortably inside quiet hours, so anyone named in it can be called tonight.

## Who gets what

**Patrick** (`patricksiado@gmail.com`) — everything. Capture health, scan
targets, counts, trends, and the money.

**Dave** (`davebd0816@gmail.com`) — the call queue and the callbacks. He is the
one dialing, so his copy leads with names and numbers, not diagnostics. Skip
capture health and scan targets; they are not his job.

**Churchie** (`churchiieoperationsva@gmail.com`) — the work queue and list
management: who to load, what to scrub, what came back.

**The three daily tips go in every copy.** Dave gets the sales tip and the
AT&T tech/phone benefit above all — that is what he says on the phone. Churchie
gets the GHL tech tip above all — she runs the machine. Send all three to
everyone anyway; they are short and the cross-training is worth it.

**No COMMISSION figures in Dave's or Churchie's copy.** Money we get paid lives
in Patrick's copy only. This is not squeamishness — it is a standing instruction
from Ed that Patrick agreed to, and the daily email is the most likely place to
break it by accident. Say "the upgrade" and "the higher-value sale".

**Customer-facing pricing is NOT the same thing and IS allowed.** A rep cannot
sell without knowing what the customer pays — the bundle discount, the tiers,
what AT&T Phone – Advanced costs. What must never appear is what *we* earn:
per-sale payout, per-lead value, revenue totals, anything a commission can be
reconstructed from. Ed's concern was Ara learning what an upgrade pays, not Ara
knowing the retail price of fiber.

**Send three separate emails, never one with three recipients.** The moment they
share a body, the money leaks into the VA copy. That has already happened once.

Subject lines carry the single most important finding so they read in a phone
notification without opening: `Coverage gap Aug 28 — Xfinity down in 77706, 34
green on those streets` beats `Daily report`. In the evening, the callback count
is almost always the headline: `EOD Aug 28 — 3 replies today, none called back`.

Append `Claude (for Patrick)` so nobody mistakes it for hand-written.

## Scheduling

Two routines, both bound to the session that created them — a fresh-session
routine carries no connectors on this org and would fire with no Gmail, Sheets
or GHL access, producing nothing.

| Edition | Cron (UTC) | Central | Routine |
|---|---|---|---|
| Morning | `0 12 * * *` | 7:00am | `trig_01JTQKnB2U5ihS1mC4rpX2qy` |
| Evening | `30 22 * * *` | 5:30pm | `trig_01RjAUBz16UNpdDzK2neCz37` |

Patrick's personal 8am brief (`trig_018JYaeTgaN8NToSs3RK2T3D`) is a **different
report** — health, goals, food, money-saving — and goes to him alone. Do not
fold either edition into it or let them drift into covering the same ground.
