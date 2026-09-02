---
name: gold-cluster-sweep
description: Run the full Optimus lead loop off a gold-dot cluster — find the dense pocket (gold means newly lit fiber nobody has worked), pull the green and gold addresses plus the small businesses on those streets, skip-trace cell numbers with DealMachine, send individually-written texts through GoHighLevel, then book the calls and door-knocks as assigned tasks and keep following up until every lead is closed or dead. Use this whenever Patrick asks to work a gold cluster, find where the gold is thick or where new fiber is, enrich an area, pull cell numbers for a street or ZIP or neighborhood, build or fire a text campaign off the fiber map, line up sales calls or in-person visits, hand leads to reps, or chase follow-ups — including when he names only a street or neighborhood, and including when he asks to keep it running in the background.
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

## Step 0: work the backlog before hunting anything new

Do this first, every time. The warmest leads in this business are already in the
CRM, not out on the map, and they cost nothing to find.

**People who already said yes.** Search contacts for the tag `replied-yes`, plus
`interested`, `client is interested`, `hot lead`, `hot-lead`, `warm`,
`commercial-warm`, `callback`, `call back`, `callback-scheduled`, `appt booked`,
`appt-was-set`, `needs-followup`. Exclude `not interested`,
`wavv-not-interested`, and the closed family (`sold`, `sold-won`, `command-sold`,
`command-won`, `fiber-won`, `mobility-sold`) so nobody re-pitches won business.

Then check whether each one is still reachable, because this is where the money
leaks: look at `dndSettings`. `SMS.status = "permanent"` with `STOP_KEYWORD`
means they opted out and are gone. `SMS.status = "active"` set by the STOP
workflow means the same thing in practice. A contact can be tagged both
`hot-lead` and opted-out at once — that combination is the sound of a lead dying
in the queue.

Measured on 2026-08-22: **22 contacts carried `replied-yes`. 7 were already
unreachable** — 3 hard opt-outs and 4 DND'd — and two of those seven had also
been tagged `hot-lead`. The other 15 had never been closed, the oldest sitting
since June 30. Nobody had looked. This is why Patrick's rule is *any reply gets a
call the same hour*, and why the backlog dig comes before new prospecting.

**Quotes that were sent and never closed.** A quote is the strongest buying
signal there is — they asked for a number. Search email for quotes sent to
customers. Search the *whole mailbox*, not just sent mail, because a quoting
system may copy him rather than send as him. Also check GHL `list_estimates` and
`list_invoices`.

Two things learned doing this: searching only `from:` his own address misses
system-generated quotes entirely, and a customer question left unanswered in a
thread is worth more than any cold lead on the map — one 2025 thread had a
customer asking twice for a full quote with no reply after.

Re-quote at today's pricing. Never resend an old number: promo windows move, and
device offers go stale within months.

**Contacts who replied but were never dispositioned.** `lastMessageBody` only
holds the most recent message, so anyone who replied and got answered shows as
outbound-last — scanning last messages will not find them. Use tags and pipeline
stage instead. And read replies before counting them: business missed-call
autoresponders read as engagement and are not.

Everything found here goes into a backlog tab with an owner, an action and a due
date, and gets worked before the next cluster.

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

### 4b. Small businesses on those same streets

A pocket of new fiber contains businesses as well as houses, and they are worth
more per door. Once you have the cluster's street names, check them against:

| Tab | What it is |
|---|---|
| `Upgrade Orange Biz` | **GOLD businesses — copper business customers. The highest-value slice we have.** |
| `Fiber Green Biz` | Green businesses (fiber live, not an AT&T customer) |
| `Maps Businesses` | Everything scraped from Google Maps: name, address, phone, website, category |

Gold businesses come first, always. A business already paying AT&T for copper is
an upgrade conversation with no competitor in it, and business fiber is worth
far more than a single residential line.

Two cautions that have already cost real money here:

- **Column F in `Fiber Green Biz` is a hand-typed call-status field, not a DNC
  check.** The Maps scraper never queries the DNC registry, so DNC status on
  those rows is genuinely unknown. Do not read "only 3 DNC" as a clean list.
- **Business addresses in these tabs are frequently street-only, with no city or
  ZIP.** That breaks `enrich_address`, and it has already produced a bad match —
  an Oklahoma 405 number joined onto a Texas "W Main St". Supply the ZIP from the
  cluster before enriching, and if a returned area code does not belong to the
  market, throw the row out rather than texting it.

**Getting a business owner's cell — the chain that works:**

1. **Home-based business?** `enrich_address` on the business address returns the
   owner: name, cell, line type, DNC. ~2 credits. The Google Maps business
   number is often the owner's personal cell already.
2. **Commercial building?** DealMachine returns `contacts: []` for LLC-owned
   property — it will not skip-trace an LLC. Go to the **free Texas Comptroller
   franchise tax search** (or SOSDirect at $1) for officers and their addresses,
   then `enrich_address` on the officer's **home** address.
3. **Never** run a name-only DealMachine search to find them. "BEVERIDGE"
   statewide is 141 people and 141 credits. Narrow by ZIP or use the home
   address.

Chains and franchises with a switchboard have no local telecom decision-maker.
Drop them rather than burning a message.

### 4c. THE ADDRESS GOES IN THE NOTE — ALWAYS

Patrick, 2026-09-03: *"I want the address in the notes always"*. Every lead note
**opens with the full street address and closes with it again**. These leads ARE
the address — "fiber is live at your address" is the entire pitch, and a rep who
has to hunt for it will not say it.

No address on the record? That is a job, not an exception: `enrich_phone` with
`include_properties` and take the **owner-occupied** property (or the one where
`is_resident` is true). ~1-3 credits. If DealMachine returns `no_match`, or the
record is LLC-owned (it will not skip-trace an LLC), write
**`ADDRESS UNKNOWN - ASK FOR IT ON THE CALL AND WRITE IT HERE`** as the first
line and say what you checked. Never leave it blank, never substitute a city.

### 5. Write the campaign tab

New tab, named for the pocket and date (`Grant Rd Cluster — Aug 24`). Columns:

`Priority | Address | City | State | ZIP | Dot Color | Owner | Phone | Phone Type | Message | Status | Notes`

Status starts at `READY - NOT SENT`. Blocked rows carry the reason. Notes hold
DNC status, co-owner alternates, and anything the next person needs.

### 6. Write the messages — every one different

Personalize each message individually. No two contacts may receive identical
text; duplicates get detected and do not count on the Operator Scorecard, and
identical bulk text is what gets a number flagged.

**Identity: "Patrick with AT&T Fiber." Never name the dealer brand.** Patrick,
2026-08-22, on seeing "Patrick with Optimus, an AT&T authorized dealer in
Brazoria County": *"eww fix this message / don't say optimus / we're att."* The
customer is buying AT&T Fiber and has never heard of the dealership; leading
with a company they do not recognise reads as a telemarketer. If a compliance
line is ever wanted back, "with AT&T Fiber (authorized dealer)" is three words,
not a clause.

**NEVER write opt-out language. GoHighLevel appends its own.** Verified against
the stored body of the Aug 21 send to Bartlett Ramsey: it ends
`Reply STOP to opt out.\nReply STOP to unsubscribe.` — ours, then GHL's. Every
message in that batch shipped a doubled opt-out, which is the single clearest
tell that a human did not write it. Write the message and stop; the STOP line
appears by itself.

**Keep the whole thing inside ONE SMS segment — 160 characters INCLUDING the
27 GHL appends.** So the body budget is ~130 characters. The Aug 21 message ran
388 characters, three segments, triple cost, and read as a brochure. Length is
not thoroughness; it is the thing that gets it ignored.

**No price in the first text.** Price turns a heads-up into a pitch and is most
of what made the old message long. Lead with availability; give the range when
they reply and ask.

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
- **Check the tags before writing.** `absentee-owner` means they do not live
  there — do not write "your address". Ask about the property, not their home.
  The Aug 21 message asked an absentee owner "if you've got someone in that
  house", which is nobody's idea of a friendly opener.

**Worked examples — all one segment, no opt-out line, no brand name:**

| Segment | Message |
|---|---|
| Green, absentee owner | `Bartlett - Patrick with AT&T Fiber. Fiber is now live at 508 E Miller in Angleton. Want me to check the options for that address?` |
| Green, owner-occupied | `Hi Maria - Patrick with AT&T Fiber. Fiber just went live on Whittaker Ln. Your address qualifies. Want me to send what's available?` |
| Gold, copper customer | `Hi Ray - Patrick with AT&T Fiber. You're on our copper line at 214 Dowlen. Copper is being retired and fiber is live there now. Want the upgrade details?` |
| Gold business | `Hi Dana - Patrick with AT&T Fiber. Fiber is live at your Dowlen Rd shop and you're still on copper. Upload speed is the big change. Worth a look?` |

These are shapes, not scripts — every message still has to differ from every
other one.

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

**Text non-responders 2-3 times, spaced a few days apart.** Patrick struck the
old one-text-only rule on 2026-08-27: people do reply on the second and third
touch, and stopping after one throws away most of what the list is worth. Each
message must be freshly written — a repeat of the first text reads as a robot
and is the thing that actually annoys people. Stop the sequence the instant
someone replies or opts out.

The old rule justified itself with "opt-outs spike on message two", which was
never measured — the one batch with real numbers (Aug 21, 100+ texts) produced
zero replies and zero opt-outs because no second message was ever sent. Track
the opt-out rate as touches increase and let it set the ceiling.

Calibration from a real batch: **100+ texts sent Aug 21 produced zero replies
and zero opt-outs.** Zero opt-outs means the copy is not burning anyone; zero
replies means texting alone does not close. The call is the conversion step, and
inbound replies need a callback the same hour — people have opted out while
waiting.

Beware false positives when reading replies: business missed-call autoresponders
("Sorry we missed your call…") look like engagement and are not. Read the actual
message before counting it.

### 8b. Hit every channel the lead gave you, not just SMS

A cell number is one channel. DealMachine usually returns **emails too** — often
two or three per owner — and the dialers are already built. A lead worked on
three channels converts far better than the same lead texted once, and it costs
nothing extra because the enrichment already paid for the data.

**Email.** `send_email` with `contactId`, a subject and a body. Worth it because
email carries what SMS cannot: the copper-retirement explanation, the speed
tiers, a real comparison. It also reaches the landline-only rows that SMS can
never touch, which is roughly 12% of any residential batch.

Keep it plain text and personal, not a marketing blast — a short note from
Patrick reads as a heads-up, an HTML template reads as spam and lands in
Promotions. Include an unsubscribe line: commercial email needs one, and the
same opt-out discipline that protects the sending number protects the domain.

**Dialer.** Loading a contact into a dialer workflow is `add_contact_to_workflow`
with `contactId` and `workflowId`:

**`Optimus Dave` NO LONGER EXISTS (verified 2026-08-27).** Enrolling against
`4985f898-...` returns `400 The workflow id is invalid`. Patrick rebuilt Dave's
queues on 2026-08-25 and split them business / residential. **List the live
workflows before enrolling anyone** — `ghl_list_workflows` — because these IDs
have now churned twice.

| Workflow | ID | Use for |
|---|---|---|
| **Dave-Fiber Bizz** | `b7681898-1a0b-4406-bb94-1684ea78cb9f` | businesses |
| **Dave-Fiber Riss** | `00482c14-461f-4ba6-b6e7-acc39ed8df4f` | residential ("Riss" = Res) |
| Optimus Dialer 2 — Zack Call Queue | `9d3c7d0c-8f6f-44a9-93f9-d55d78e3b4a8` | |
| Optimus Dialer 3 — Fiber Green Biz Auto Loop | `b21e43bd-75ee-45a1-8764-bce4f3ab0771` | |
| Optimus Fiber Biz — Power Dialer Queue | `41e00387-a766-4975-bbcd-627c684a3ee1` | |

**Never enroll into `Dave do not use`** (`49da9c64-9407-4765-8fbd-b78230493915`)
— published, and named that on purpose.

Both Dave queues are two steps, `Manual call` -> create opportunity in **AT&T
Leads** (`2V9thfxQpuhn6ZP0Peqt`), and carry **no trigger**. Nothing auto-dials
and nothing fires on its own, so a batch can be loaded at any hour — the call
is made by a human out of the manual dialer. Check that shape with
`ghl_get_workflow_full` before loading a queue you have not used before; a
published workflow with a `send_sms` step would text everyone you enrolled.

Load the landline-only rows and every gold business into a dialer rather than
dropping them. They were never dead leads, only un-textable ones.

### 8c. Which ZIPs to scan next

The hunter's opening banner reads `Fiber Zones` and prints the ZIPs turning up
the most NEW green, so the next sweep aims itself. If that tab is empty the
banner says so — run `fiber_zone_scanner.py` to populate it.

When picking between ZIPs, gold density is the signal: lots of gold and little
grey means fiber was lit recently and nobody has converted it. Public AT&T
announcements are not useful for this — they report at the level of "725,000
locations across 38 neighborhoods", which cannot aim a sweep at a street. Our own
gold data is finer-grained than anything published.

### 9. Turn interest into a booked visit, and hand it to a person

A text that gets a reply is not a sale — it is a lead with a clock on it. Every
lead needs an owner and a next action with a date, or it evaporates. Patrick's
own standing rule: **any reply gets a call the same hour.** People have opted out
while waiting for a callback.

**Track the lead.** `upsert_opportunity` into the right pipeline:

| Pipeline | ID | Stages |
|---|---|---|
| AT&T Leads (residential) | `2V9thfxQpuhn6ZP0Peqt` | Lead → Contacted → Closed/Won → Lost |
| AT&T Commercial (business) | `trc5dwodtc1LBYHikmiK` | Leads → DND → Closed/WON → Closed/LOST |

**Assign the work.** `create_contact_task` with `assignedTo`, a real `dueDate`,
and a title that says exactly what to do — "Call back: replied YES, wants
pricing" or "Door knock: 10519 Grant Rd, gold biz, copper upgrade". A task with
no assignee and no due date is a note, and notes do not get worked.

Route by what the lead needs:
- **Replied / warm** → call task, due within the hour.
- **Landline-only or no cell** → call task. These are not dead, they are just
  not textable.
- **Gold business** → in-person visit task. Businesses close in person far more
  than over SMS, and a gold business is the easiest conversation on the list.
- **No answer after the call** → door knock task in the same pocket, batched by
  street so one trip covers many addresses. This is the whole point of working a
  *cluster* rather than scattered leads.

**Booking a calendar appointment — read this before promising one.**

There is now an active calendar for this: **`Optimus Fiber Appointments`**, id
`jSOOC383RNxHIRwo6zV8`, 30-minute slots, auto-confirm. It was created on
2026-08-22 because all 27 pre-existing calendars were inactive and nothing could
be booked at all.

**It still needs open hours set in the GoHighLevel UI before booking works.**
This was tested, not assumed: with no availability configured, `get_free_slots`
returns nothing and `create_appointment` fails with *"The slot you have selected
is no longer available"* — even with `ignoreDateRange: true`. The MCP's
`update_calendar` has no parameter for open hours, so this is a one-time manual
step: open the calendar in GHL and set availability (Mon–Fri business hours).

Once hours exist: `get_free_slots` to find a real opening, then
`create_appointment` with `calendarId`, `contactId`, `startTime`, and
`assignedUserId`. Until then, use tasks with due dates and say plainly that a
task was created rather than reporting a booking that did not happen.

Dave is the one who dials. Do not invent rep assignments beyond what Patrick has
said — if you do not know who covers a pocket, leave the task unassigned and
flag it for him rather than guessing.

### 10. Follow up relentlessly — but not by text

"Follow up like crazy" is right, and the channel matters. Repeat texting is the
one thing that reliably destroys a sending number: opt-outs spike hard on message
two to someone who never answered message one. So the follow-up pressure goes
into **calls and doors**, not more SMS.

A cadence that fits the evidence:

| When | Action |
|---|---|
| Reply comes in | Call within the hour. Always. |
| Day 1, no reply | Call. |
| Day 3 | Call at a different time of day. |
| Day 5-7 | Door knock, batched with the rest of the pocket. |
| After that | One final call, then mark it Lost and stop. |

Marking it Lost matters. A pipeline clogged with leads nobody will ever reach
hides the ones that are live.

Every touch gets logged against the contact so the next person can see what
already happened. And when reading replies, check the actual message before
counting it — business missed-call autoresponders ("Sorry we missed your
call…") look like engagement and are not.

### 11. Keep it running

Work pockets one at a time and keep a **`Cluster Queue`** tab so the loop has a
memory: pocket name, centroid lat/lng, date worked, counts of green / gold /
business, how many were textable, sent, replies, opt-outs, and status
(`QUEUED` / `WORKING` / `SENT` / `EXHAUSTED`).

Without that tab every run re-finds the same dense pocket, because it is still
the densest. Check it first and skip what is already worked.

Each cycle: pick the next unworked pocket → enrich → stage → send inside the
window → book the calls and doors → work the follow-up cadence on everything
already out → log results back to the queue.

Two things stay human decisions no matter how automatic the rest becomes: **the
go on a send batch**, and **anything that would widen the blast radius** — a new
sending number, a much larger batch, or dropping the measurement gate. Staging,
enriching and queueing are safe to run unattended. Sending is not, because it
cannot be taken back.

## Checks worth running before you send

- Is every number in the send list `wireless`?
- Is every message different from every other?
- Does every message OMIT opt-out language? (GHL appends it — writing your own
  ships a doubled STOP line.)
- Is every message one segment: body under ~130 characters?
- Does any message name the dealer brand instead of AT&T Fiber? Fix it.
- Is it between 8am and 9pm Central?
- Does the phone column hold digits only — no labels, no parentheticals?
- Did you touch only your own tab?
