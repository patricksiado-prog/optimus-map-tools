---
name: new-build-outreach
description: Run the full loop on a fresh AT&T fiber build — find the newest sweep, build the call list, create the contacts in GHL, send the first text, and run the follow-up cadence. Use when asked to see the new build, work the new fiber, text the list, follow up, run outreach, start a campaign, or push new leads into the dialer. Covers batch sizing, opt-out monitoring, the day-by-day cadence, and what to do when someone replies.
---

# New Build Outreach

`fiber-freshness` says WHERE. `gold-dot-workup` says WHO. This skill is what you
actually DO to them, and what you do next.

Never run this end-to-end without stopping at the approval gate in Step 4. Texting is
outward-facing and unrecallable.

## Step 1 — see the new build

The newest sweep is a capture DATE, not a place. `Precise Fiber` has no city and no
coordinates (see the timestamp trick in `gold-dot-workup`), so the only way to see
"what's new" is to census column C.

Build a temp tab and count rows per date, split GREEN / ORANGE.

**The trap that will cost you an hour.** `Precise Fiber` column C is a TEXT string
(`2026-08-19 09:31:12`), not a date value. So:

- Date-range `COUNTIFS(">="&DATEVALUE(...))` returns **0**. Numbers never match text.
- Wildcard `COUNTIF(C:C, A2&"*")` also returns **0** if your date spine in column A got
  auto-converted to real dates by Sheets — `A2&"*"` becomes `"46174*"`.

The formula that actually works, and is immune to both:

```
=COUNTIF('Precise Fiber'!$C:$C, TEXT($A2,"yyyy-mm-dd")&"*")
=COUNTIFS('Precise Fiber'!$C:$C, TEXT($A2,"yyyy-mm-dd")&"*", 'Precise Fiber'!$B:$B,"ORANGE")
```

`TEXT()` forces the spine back to a string whether Sheets converted it or not.

**Always prove the census before you trust it.** Put these side by side and compare:

```
=COUNTA('Precise Fiber'!A2:A)        vs   =SUM(your total column)
=COUNTIF('Precise Fiber'!B:B,"ORANGE") vs =SUM(your orange column)
```

If they don't reconcile, the census is wrong — not the data. A helper-column approach
(`=LEFT('Precise Fiber'!C2,10)` filled down 459k rows) silently fills only ~13k rows and
produces a confident, completely fabricated answer. Do not use helper columns on this tab.

Read it this way:

| Signal | Means |
|---|---|
| A date that appears at all | The hunter ran that day |
| Several distinct hour blocks in one date | Several separate sweep sessions — usually different geography |
| ORANGE share climbing vs. prior sweeps | Copper-heavy neighborhood. **Best turf we get.** |
| ORANGE share near zero | New-construction subdivision. Everyone's already fiber or nobody's AT&T. Low value. |

A "new build" worth working is a date with a **meaningful ORANGE count**, not the biggest
row count. 10,000 green dots in a master-planned community is worth less than 400 gold
dots on 1960s copper.

**Gold detection only started 2026-08-17.** All 8,264 ORANGE dots in the file come from
exactly three sweeps — Aug 17 (4,042), Aug 18 (3,202), Aug 19 (1,020). Every sweep before
that reads 100% GREEN, ~450,000 rows of it. That is a *classifier artifact, not ground
truth*: those older sweeps were captured before the gold logic ran, so an unknown share of
those "green" dots are actually copper customers. Never tell anyone the older markets have
no gold — say the older sweeps were never scored, and re-sweep to find out.

## Step 1b — find out WHERE it is (do not skip)

`Precise Fiber` has no city. The sweep runs off whatever seed the hunter was pointed at,
which is **not necessarily the market we sell in**. Confirm geography before spending a
single credit.

The `Gold Dots` tab has lat/lng and **no header row** — data starts at row 1:
`A`=Address, `B`=Captured At (text), `C`=Latitude, `D`=Longitude.

Cross-reference a few street names from the new sweep against `Gold Dots` and read the
coordinates. Rough anchors for this operation:

| Lat / Lng | Market |
|---|---|
| ~29.7, -95.4 | Houston |
| ~29.2, -95.4 | Angleton / Brazoria County |
| ~30.1, -94.1 | Beaumont |
| ~32.8, -96.75 | **Dallas** — not our turf |

This is not hypothetical: the 2026-08-19 sweep came back at **32.79, -96.75 — Old East
Dallas**, 240 miles from Houston. A beautiful 1,020-dot gold list nobody on the team can
door-knock. Check the coordinates first, every time.

Delete the temp tab when done reading it. Never pull 459k rows into context.

## Step 2 — build the list

Hand off to `gold-dot-workup`. Non-negotiables from that skill that this loop depends on:

- **Sample 12 addresses and measure the DNC rate before enriching the whole sweep.**
  Textable share has measured anywhere from 17% to 71% depending on home value.
- Dedupe on address/coordinate first — apartment buildings burn credits and return one LLC.
- Budget **2.83 DealMachine credits per address**, not 2.

## Step 3 — size the batch

Do not load the whole sweep. Send in batches and let each batch report before the next.

| Batch | Size | Purpose |
|---|---|---|
| Probe | 25-40 | Measures reply rate and opt-out rate on this copy, this number, this market |
| Working | 100-150/day | Only after the probe clears the gate below |
| Never | "the whole list" | One bad blast costs sender reputation that credits cannot buy back |

**The gate.** After the probe, count inbound replies:

- STOP / unsubscribe under 10% of inbound -> proceed
- 10-20% -> rewrite the copy before scaling
- **over 20% -> stop. Do not scale.** Change the copy AND rotate the sending number.

This is not theoretical. A measured slice of the `harvey.resi` campaign in
Frontline Direct came back **72 bare STOPs out of 76 inbound messages** — 95%. That number
is what a burned number and burned copy look like. Check it every batch.

## Step 4 — the first text (APPROVAL GATE)

**Show the copy and the recipient list to Patrick and get a yes before sending.** Always.
No exceptions, no "I'll just do the first few."

Rules the copy must obey:

- **Never text a landline.** Twilio returns error 30006 and it counts against the number.
- **Never text a DNC number.** DNC blocks calls too — those go to door knock / CREATE REFERRAL.
- **Never quote a flat price.** Fiber 300 is $55 base, less promo (12 months only), less
  autopay, less wireless-bundle. Say "in the $20s to $30s for the first year, I'll confirm
  your exact price before anything is ordered." A hard number quoted in a text gets disputed
  on the install call and kills the order.
- Lead with the copper retirement, not the promo. It's true, it's urgent, and it reads as a
  heads-up instead of a pitch:

  > AT&T is retiring the copper network your address is on by 2029, and fiber is already
  > live on your street. You can move now while the new-customer promo is on, or move later
  > without it.

- One message. Then stop. Opt-outs spike hard on message two to a non-responder.

## Step 5 — into the dialer

GHL has no dialer API. `add_contact_to_workflow` / `remove_contact_from_workflow` is the
only lever that exists — enrolling a contact in the dialer workflow is how it reaches the queue.

| Thing | State |
|---|---|
| `Optimus Fiber Biz — Power Dialer Queue` | **Working. Use this one.** |
| `Optimus Dialer 2` | **Broken** — Add Tag sits at node position 0, so every contact gets tagged "not interested" and ejected on entry. Verified empirically. Don't enroll anyone until the node is moved. |
| Workflow re-entry | **Blocked by default.** A contact already enrolled will silently no-op. Not a bug — check enrollment before concluding the tool failed. |
| `triggers: []` from the API | Means nothing. The field isn't populated even for workflows that demonstrably fire. Never conclude "no trigger" from this. |
| Dispositions | Only save when the rep clicks **"Next call"** inside the Power Dialer. Setting it on the contact record does not stick. |

## Step 6 — the follow-up cadence

The follow-up is where the money is and it is the step that always gets skipped.

| When | Action | Condition |
|---|---|---|
| Day 0 | Text #1 | wireless + DNC-clear |
| Day 0, +2-4h | **Call** | no reply to text #1 |
| Day 2 | Call again, different time of day | still no contact |
| Day 4 | Text #2 | **only if they replied to something.** Never to a cold non-responder. |
| Day 7 | Door knock / CREATE REFERRAL on the dealer map | no contact by phone |
| Day 14 | Close the loop or park it | — |

Two hard stops:
- **A "STOP" is permanent.** Tag `dnd`, remove from every workflow, never re-add. Do not
  let a later batch re-import them.
- **Friday is the best day** in the measured data. Front-load the week's probe batches there.

### When they reply

| Reply | Do this |
|---|---|
| "YES" / interested | **Call within minutes, not hours.** Speed-to-lead is the whole game. |
| A question about price | Answer with the range, then move to a call. Never quote flat. |
| "Send me a link/flyer" | We don't have one. Offer the call. Don't stall the thread. |
| STOP / unsubscribe | Tag `dnd`, remove from all workflows, done |
| Silence | Cadence above. Do not send a second text. |

**Check the unread inbox before starting any new batch.** Live leads with open
opportunities have been found sitting unanswered underneath a pile of STOPs. Working the
existing inbox beats adding to it — every unanswered "yes" is a lead already paid for.

## Where things live

| | |
|---|---|
| Frontline Direct | `TXw28sw0Z2rI6tcCDhJY` — connector has full read/write |
| T-OPTIMUS Houston | `xZj500PjsflIQg2j9f9D` — users listable, but `get_location` returns **403**. Not in the connector's location scope; can't write there until it's added. |
| Hunter output | `1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA` |

## What to report back

After every batch, a short line — not a report:

```
Batch 3 · Angleton gold · 120 sent
replies 9 · yes 4 · stop 2 (1.7%) · calls booked 2
gate: clear, proceeding
```

If the gate fails, say so first and stop. Don't scale a burning campaign.
