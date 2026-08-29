---
name: close-rate
description: Measure what actually converts — text reply rates, opt-out rates, speed-to-lead, and closing ratio by segment, copy, carrier and dot colour. Use when asked how we're doing, what's converting, why deals aren't closing, to analyse texts or replies, to compare copy or markets, to work out cost per deal, or to plan how many leads are needed to hit a sales target.
---

# Close Rate

Turns outreach into arithmetic. Every claim about "what works" here has to come from a
measured number or it does not go in the report.

## The funnel, and where it actually leaks

Six stages. Measure every one — a ratio is meaningless without the stage above it.

| # | Stage | Where the number lives |
|---|---|---|
| 1 | **Loaded** | contacts created, by tag |
| 2 | **Sent** | outbound SMS in `search_conversations` |
| 3 | **Delivered** | sent minus 30006/undelivered errors |
| 4 | **Replied** | inbound messages, split STOP vs real |
| 5 | **Positive** | replies that are not STOP/unsubscribe |
| 6 | **Closed** | opportunity marked won |

**The measured leak is between 5 and 6.** 22 `replied-yes` contacts, 0 closed, 7 went DND
while waiting. That is not a lead-generation problem, it is a follow-up problem, and no
amount of new leads fixes it. Check stage 5→6 before anyone asks for more leads.

## Benchmarks to judge against

Ours, measured — use these, not industry averages:

| Campaign | Sent | Positive | Closed | Rate |
|---|---|---|---|---|
| Deer Park resi | 246 | 9 (3.7%) | 0 | 0% |
| ARA OKC commercial | 838 | 2 | 1 | 0.12% |
| La Porte resi | 8 | 0 | 0 | 8 STOPs |
| Best team era | — | — | 130 in 23 days, 11 reps | 5.7/day |

External benchmarks worth knowing: opt-out under **3.5%** per send is healthy, **0–1.5%**
is well run. Contact rates fall **80% after 5 minutes**; the first responder wins ~**50%**
of deals.

**A campaign is burning the number, not underperforming, when STOPs exceed 20% of
inbound.** A measured slice of `harvey.resi` came back 72 bare STOPs out of 76 inbound —
95%. Stop and rewrite at that point; do not scale.

## How to pull the numbers

```
search_conversations(status="unread", limit=100)     # then parse locally
get_sms_reports / get_call_reports                   # aggregate view
search_opportunities(pipelineId=..., status="won")   # stage 6
```

Never read 100 conversations into context. Pull them, write to a file, parse with a
script, report only the ratios and the named exceptions.

Classify inbound with a regex, not by eye:

```python
STOP = re.fullmatch(r'\s*(stop|unsubscribe|quit|end|cancel)\W*', body, re.I)
```

## Cut the numbers by these, always

A blended rate hides everything that matters:

- **Dot colour** — gold (copper upgrade) vs green (competitive switch). Gold should win by
  a wide margin. If it does not, the classifier is suspect before the copy is.
- **Carrier** — AT&T Mobility subscribers get the bundle pitch. The CSV export carries
  `phone_N_carrier`; the API does not.
- **Line usage** — `usage_12_months` of Heavy/Very Heavy is a demonstrably live line.
  Minimal or "no usage in 2 months" numbers deflate every rate below them.
- **Market** — DNC share tracks home value: Broun St ~$170k was 71% reachable, Westgate
  ~$300k was 17%.
- **Copy version** — one variable at a time, or the comparison proves nothing.
- **Day of week** — Friday ran ~60% hotter than any other weekday in the archives.

## Cost per deal

```
cost/lead   = (credits x $0.006) / reachable_contacts
cost/deal   = cost/lead / close_rate
```

At 2.83 credits/address and $179 per 30,000, a reachable lead costs roughly **$0.03**.
That means **lead cost is never the constraint** — rep time and the monthly export cap
are. Do not optimise the cheap number.

## Working backwards from a sales target

```
deals_needed / close_rate = positives needed
positives / reply_rate    = sends needed
sends / reachable_rate    = contacts needed
contacts x 2.83           = credits needed
```

Run this before promising a number. If the credits needed exceed the monthly cap, the
target is not reachable through the phone channel and the answer has to come from door
knocking or MDUs instead — see below.

## The two non-linear levers

Everything above scales linearly with rep hours. These do not:

- **MDU / property managers.** 13504 Schroeder Rd is ~60 orange units behind one manager.
  8550 Phelan Blvd is 26. One conversation, dozens of installs. Find every apartment
  cluster in a fresh zone before knocking a single house.
- **Door knocking costs zero credits.** The dealer map gives addresses free; DealMachine
  is only needed for a *phone number*. The export cap binds the phone channel only. With
  464,899 addresses captured, door density is limited by feet, not by budget.

## Reporting format

Short. Ratios, then the exceptions by name.

```
Beaumont fresh · 61 reachable · 10 sent (AT&T + heavy use probe)
delivered 10 · replied 3 (30%) · stop 0 (0%) · positive 3
gate: clear, scaling to the next 13
unworked: Bruce Johnson, Brian Ferguson - replied, never called back
```

Always name the unworked positives. They are the most valuable rows in the report and the
only ones that require a human today.
