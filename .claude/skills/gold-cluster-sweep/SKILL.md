---
name: gold-cluster-sweep
description: Find a dense gold-dot cluster from the ATT FIBER LEADS sheet, pull the green and gold addresses in that pocket, skip-trace them for cell numbers with DealMachine, write a campaign tab, and send individually-written texts through GoHighLevel. Use this whenever Patrick asks to work a gold cluster, find where the gold is thick, build or fire a text campaign off the fiber map, get cell numbers for an area or street, run a neighborhood or corridor sweep, or says anything like "grab the cells around X and text them" — including when he names only a street, ZIP, or neighborhood and not the word "cluster".
---

# Gold Cluster Sweep

Turn a dense pocket of gold dots into a batch of texts that are actually
deliverable, without burning credits or the sending number.

## Why gold marks the spot

- **GREEN** = fiber is live, they are *not* an AT&T customer. **$500.** The prize.
- **GOLD/ORANGE** = fiber is live and they *are* an AT&T customer still on copper.
  **$140.** Easiest sale in the business — it is an upgrade, not a switch, so
  there is no competitor to beat.
- **GREY** = already on AT&T fiber. Skip. Grey is never written to the sheet at
  all, so you will never see it and must not build logic that expects it.

Green pays 3.6x more and is ~48x the volume, so green is the money. But gold is
the *compass*: a pocket thick with copper customers means nobody in that pocket
has converted yet, which means nobody has worked it. That is the only freshness
signal that survives — capture dates record when *we looked*, not when AT&T lit
the street.

Work gold first inside a cluster anyway. It closes faster, and a closed gold
call warms the street for the green ones.

## System facts you need

| Thing | Value |
|---|---|
| Master sheet `ATT FIBER LEADS` | `1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA` |
| GHL location — T-OPTIMUS Houston | `xZj500PjsflIQg2j9f9D` |
| `Gold Dots` tab | **NO header row.** A=Address, B=Captured At, C=Lat, D=Lng |
| `Precise Fiber` tab | ~474k rows, GREEN+ORANGE only, **no city, no coordinates** |

**Never read `Precise Fiber` wholesale.** It has crashed Autosheet twice with
"request too large". Create one temp tab, put bounded `QUERY`/`COUNTIF`
formulas in it, read the small result, delete the temp tab.

**Never edit hunter-owned tabs:** `Precise Fiber`, `Gold Dots`, `Maps Businesses`,
`Fiber Green Biz`, `Upgrade Orange Biz`, `Enriched Leads`, `Hunter Status`,
`Backend Comm`, `New Fiber Alerts`, `_Dedupe Lock`. The hunter writes to these
constantly and your edit will collide with a live sweep. Make your own tab.

## The sweep

### 1. Find the cluster

Export `Gold Dots` (A:D, no header) and run the bundled script:

```bash
python3 scripts/find_clusters.py gold_dots.csv --top 10
```

It grids the coordinates, merges touching cells so a cluster follows a corridor
instead of being chopped into circles, and ranks by gold count. Read
`rows_skipped_bad_coords` — rows with missing or 0,0 coordinates are reported,
not silently dropped, because a cluster you cannot trust is worse than none.

Each cluster reports a `profile`:

- **commercial-leaning** (BLVD/RD/HWY/DR/PKWY/AVE) — where businesses actually
  are. Cullen, Reed, Phelan, Westgate, Grant, Jones.
- **residential-leaning** (LN/CT/CIR/PL) — subdivisions.

This distinction matters because ranking gold by raw count sorts you straight
into subdivisions: the top gold streets by volume have had **zero** businesses
on them. If Patrick wants business gold, take a commercial-leaning cluster even
if a residential one is denser. If he wants green volume, dense residential is
fine. When in doubt, ask which he is after — it changes the whole batch.

### 2. Pull green and gold in that pocket

Gold comes straight from the cluster (it carries coordinates).

Green is harder and you should be honest about it: `Precise Fiber` has **no
coordinates and no city**, so you cannot select green geographically. Join by
the **street names** the cluster reports, via a bounded QUERY in a temp tab:

```
=QUERY('Precise Fiber'!A:Z, "select * where upper(A) contains 'GRANT RD' limit 300", 0)
```

Street-name matching is approximate — a long road leaves the pocket. Keep the
house-number range near the cluster's addresses, and say plainly in the campaign
tab that green rows were matched by street, not by coordinate.

### 3. Skip-trace for cell numbers

Check `dealmachine_usage` first (free, instant). Then:

- **Gold dots have lat/lng → use `dealmachine_enrich_latlng`.** No ZIP needed.
  This is the unlock for gold, whose addresses are street-only.
- **Green rows are street-only → `dealmachine_enrich_address` REQUIRES a ZIP**
  and fails hard without one. Take the ZIP from the cluster's gold rows in the
  same pocket.
- Pass `contact_audience: "owners"`.

**Cost, measured:** about **1–2 credits per address**, not the ~6 written in
older notes. A real 25-address residential run cost **39 credits** total.
Credits **deduplicate within a billing cycle**, so re-pulling an address you
already pulled this cycle is free.

`enrich_address` and `enrich_latlng` have **no `estimate_cost` flag** (unlike
`property_search`/`people_search`/`enrich_name`, where it makes the call free).
So **probe one address first**, read the actual `credits.used`, then batch. Never
run a large batch on an assumed price.

Two things DealMachine will not do, so don't burn credits discovering them again:
- **Commercial / LLC-owned property returns `contacts: []`.** It will not
  skip-trace an LLC.
- **`enrich_phone` returns `no_match` for business lines.** It holds people, not
  businesses. It cannot type-check a business number.

Home-based businesses are the exception and the gift: a full owner record with
cell, line type and DNC status for ~2 credits, and the Google Maps business
number often *is* the owner's personal cell.

### 4. Filter — this is where batches are won or lost

For each enriched row pick **one wireless number**:

- **Wireless only. Never text a landline** — Twilio error 30006, and it counts
  against the sending number. Expect roughly **12% of residential rows to be
  landline-only**, so a 25-row list is not a 25-message send. Mark those
  `BLOCKED - landline only` and route them to a call instead.
- Prefer a DNC-clear line when the owner has several, and prefer the local area
  code over an out-of-state one.
- No contact returned → `BLOCKED - no owner contact`. Do not guess.
- **DNC listed is not a blocker** — record it in Notes and send anyway, with
  opt-out language in the message. That is Patrick's standing call: AT&T is fine
  with it provided opt-outs are honored and the language is present.

**Never write placeholder text into a phone or status field.** A column once
held the literal text `(all DNC)` where the digits belonged — the numbers were
fetched and thrown away, and gold could not be texted for a day. Digits, stored
as plain text, or a truly empty cell.

### 5. Write the campaign tab

New tab, named for the pocket and date (`Grant Rd Cluster — Aug 24`). Columns:

`Priority | Address | City | State | ZIP | Dot Color | Owner | Phone | Phone Type | Message | Status | Notes`

Status starts at `READY - NOT SENT`. Blocked rows carry the reason. Notes hold
DNC status, co-owner alternates, and anything the next person needs.

### 6. Write the messages — every one different

Personalize each message individually. No two contacts may receive identical
text; duplicates get detected and do not count on the Operator Scorecard, and
identical bulk text is what gets a number flagged.

What actually works:

- **Lead with copper retirement, not the promo.** AT&T is retiring copper —
  Phase 1 by 2027, Phase 2 by 2029. It is true, it is urgent, and it reads as a
  heads-up rather than a pitch.
- **Gold:** they are already a customer on copper. "You get migrated either way;
  the only thing you control is the timing."
- **Green:** fiber is newly live at their address. Not a switch pitch — an
  availability notice.
- **Never quote a flat price.** Residential: "in the $20s to $30s for the first
  year, I'll confirm your exact price before anything is ordered."
- **Business fiber is priced by SPEED TIER. Never use the residential
  $20s–$30s figures on a business.** Say pricing depends on the tier and you
  will confirm the real number first.
- Name something concrete about them — the street, the trade, what fiber upload
  actually fixes for that kind of work.
- End with opt-out language.

### 7. Send

**Quiet hours: 8am–9pm Central.** Check the clock in `America/Chicago` before
sending anything. A batch was correctly held at 11:19 PM for exactly this.

Create the GHL contacts **inside sending hours, not before**. Several published
workflows in the location can enroll new contacts and place calls or texts; if
you stage contacts at 3am you risk firing outreach at 3am. Building the tab
overnight is fine — creating contacts is not.

Then per row: `upsert_contact` (name, wireless number, address, tags like
`gold-dot`/`green-dot` and the pocket name) → `send_sms` with the message from
the tab, verbatim → write `SENT` plus the timestamp back to Status.

Watch for 30006. **Stop the batch after two failures** and find out why before
continuing.

### 8. Measure before scaling

Probe **25–40**, then stop and read the result:

- **under 10% engaged → STOP.** The copy is wrong.
- **10–20% → rewrite the copy** before sending more.
- **over 20% opting out → stop and rotate the sending number.**

**One text, then a CALL.** Do not send a second text to someone who did not
answer the first — that is where opt-outs spike.

Calibration from a real batch: **100+ texts sent Aug 21 produced zero replies
and zero opt-outs.** Zero opt-outs means the copy is not burning anyone; zero
replies means texting alone does not close. The call is the conversion step, and
inbound replies need a callback the same hour — people have opted out while
waiting.

Beware false positives when reading replies: business missed-call autoresponders
("Sorry we missed your call…") look like engagement and are not. Read the actual
message before counting it.

## Checks worth running before you send

- Is every number in the send list `wireless`?
- Is every message different from every other?
- Does every message carry opt-out language?
- Is it between 8am and 9pm Central?
- Does the phone column hold digits only — no labels, no parentheticals?
- Did you touch only your own tab?
