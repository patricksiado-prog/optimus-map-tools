---
name: daily-coverage-gap
description: Build Optimus's twice-daily coverage-gap report — cross-reference the leads sitting in the ATT FIBER LEADS sheet against what has actually been texted or called in GoHighLevel, against AT&T fiber build news, and against live cable/competitor outages, then email it to Patrick, Dave and Churchie — a morning edition that says what to work today and an evening edition that catches the replies that came in and have not been called back. Use this whenever Patrick asks what hasn't been worked, which leads are going stale, where to point the scanner, what's new in fiber news, whether a competitor is down, what the team should do today, or for the daily/coverage/gap report by name. Also use it when he asks a narrower version of the same question — "what are we sitting on", "who hasn't been called", "any new builds", "is Comcast down" — because each of those is one section of this report and the other sections are the context that makes it actionable.
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

**No dollar figures in Dave's or Churchie's copy.** Money lives in Patrick's
only. This is not squeamishness — it is a standing instruction from Ed that
Patrick agreed to, and the daily email is the most likely place to break it by
accident. Say "the upgrade" and "the higher-value sale".

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
