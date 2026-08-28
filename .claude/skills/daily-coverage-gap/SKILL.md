---
name: daily-coverage-gap
description: Build Optimus's daily coverage-gap report — cross-reference the leads sitting in the ATT FIBER LEADS sheet against what has actually been texted or called in GoHighLevel, against AT&T fiber build news, and against live cable/competitor outages, then email it to Patrick and Churchie. Use this whenever Patrick asks what hasn't been worked, which leads are going stale, where to point the scanner, what's new in fiber news, whether a competitor is down, what the team should do today, or for the daily/coverage/gap report by name. Also use it when he asks a narrower version of the same question — "what are we sitting on", "who hasn't been called", "any new builds", "is Comcast down" — because each of those is one section of this report and the other sections are the context that makes it actionable.
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

**No commission figures in the copy that reaches Churchie.** She is a VA. Ed's
standing instruction (2026-08-27) is that commission numbers stay away from the
VAs, and Patrick agreed. Say "the upgrade" and "the higher-value sale", never
$140 or $500 or anything a rate can be reconstructed from. This is why the
report is assembled once and then **sent as two different emails** — see
Delivery.

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

## Capture — is the machine working
<classified vs written, sheet growth in bytes and approximate rows, auth
failures, and the current phase. One line saying whether the sweep is on fresh
ground or re-scanning.>

## New builds worth scanning
<named places only. If the news gave nothing aimable, say that in one line.>

## Outages right now
<overlap with our pockets, or "none reported today".>

## Couldn't read
<every source that failed and why. Empty is fine and good.>
```

## Delivery

**Two emails, not one.** Same findings, different copy.

**Patrick** (`patricksiado@gmail.com`) — the full report, all sections, numbers
included. He is the one who acts on capture health and scan targets.

**Churchie** (`churchiieoperationsva@gmail.com`) — the "Do this today" and
backlog sections only, framed as a work queue: who to call, which list, why now.
Drop capture diagnostics, drop scan targets, and **drop every dollar figure**.
She needs the actions, not the machinery or the economics.

Subject line carries the single most important finding, so it reads in a
notification without opening: `Coverage gap Aug 28 — Xfinity down in 77706, 34
green on those streets` beats `Daily report`.

Append `Claude (for Patrick)` at the end so nobody mistakes it for hand-written.

## Scheduling

Patrick wants this daily. He already has a separate 8am brief
(`trig_018JYaeTgaN8NToSs3RK2T3D`) covering health, goals and sales — **this is a
different report and must not be folded into that one.**

Create it with `create_trigger`, fresh session per fire, cron in **UTC**. Central
is UTC-5 in summer, so 7am Central is `0 12 * * *`. Put it before the 8am brief
so the outage list is in hand at the start of the calling day.

The prompt for a fresh-session trigger must be standalone — it starts with no
memory of this conversation. Have it invoke this skill by name and state both
recipients.
