---
name: gold-dot-workup
description: Turn captured AT&T gold/green dots into a dialable, named, phone-verified lead list. Use when asked for leads, phone numbers, a call list, a dial list, owner names, to enrich addresses, to work a city or street, or to find who lives at captured addresses. Covers finding a sweep by timestamp when coordinates are missing, DealMachine enrichment, DNC filtering, and building the output sheet.
---

# Gold Dot Workup

Captured dot -> named human with a phone number you are allowed to call.

## What the colors mean (get this right first)

The AT&T dealer map ONLY plots addresses where fiber is already available.

- **GOLD / ORANGE** = fiber live + they already pay AT&T + still on copper.
  **Easiest sale in the business — an upgrade, not a switch.** AT&T retires copper by
  2029, so they migrate either way.
- **GREEN** = fiber live + NOT an AT&T customer. Competitive displacement. Harder.
- **GREY** = already a fiber customer. Skip. (Never written to the sheet anyway.)

Work gold before green, always.

## Step 1 — find the addresses

Two tabs hold dots, and they behave differently:

| Tab | Has lat/lng? | How to search |
|---|---|---|
| `Gold Dots` | **yes** | coordinate box |
| `Precise Fiber` (~459k rows) | **no** | see the timestamp trick |

**THE TIMESTAMP TRICK.** `Precise Fiber` has no city and no coordinates, but the hunter
sweeps one area at a time — so a capture window IS a geography. To recover a sweep:

```
=COUNTIFS('Precise Fiber'!C:C,"2026-08-17*",'Precise Fiber'!B:B,"ORANGE")
=QUERY('Precise Fiber'!A:C,"select A,C where B='ORANGE' and C starts with '2026-08-17'",0)
```

Searching `Precise Fiber` by street name gives false positives (a "BEAUMONT HWY" search
returns Houston addresses). Searching `Gold Dots` by coordinates misses everything that
landed in `Precise Fiber`. **When a city seems absent, it usually is not — find its
capture date and filter on that.**

Always work on a temporary tab, read the result, then delete the tab. Never read 459k rows
into memory.

## Step 2 — sample before committing

**Enrich ~12 addresses first and measure the DNC rate.** Measured results vary hugely:

| Market | Home value | Textable |
|---|---|---|
| Beaumont / Broun St | ~$170k | 71% |
| Angleton / E Miller | $185-308k | 42% |
| Beaumont / Westgate | $260-306k | 17% |

**DNC registration rises with home value.** A 6-address sample once produced a wrong
"door-only" verdict that the next 6 reversed. Twelve minimum.

Cheap markets -> text campaign. Expensive markets -> door knock and CREATE REFERRAL.

## Step 3 — enrich

- `dealmachine_enrich_address` with `full_address` + `contact_audience: "owners"` —
  works without coordinates and RETURNS lat/lng, so it also backfills the missing
  coordinates.
- `dealmachine_enrich_latlng` when you already have coordinates.
  **Never pass the `fields` parameter — it fails with "Reverse geocode enrichment failed."**
- Run `dealmachine_usage` (free) first. `property_count`, `filters`, `fields`, `whoami`
  are all free — use them to scope before spending.
- **Dedupe on lat/lng or address first.** Apartment buildings share one parcel; 26 units at
  one coordinate costs 52 credits and returns one management LLC.

**Cost: 1 property credit + 1 per person returned. Measured average 2.83/address**, not 2.
Multi-owner records can hit 6. Budget accordingly.

## Step 4 — triage every result

| Condition | Action |
|---|---|
| wireless + `do_not_call: false` | **TEXT then CALL** |
| landline + `do_not_call: false` | **CALL only** — texting a landline fails, Twilio 30006 |
| all numbers `do_not_call: true` | **DOOR KNOCK / CREATE REFERRAL** — DNC blocks calls too |
| no contact record | **DOOR KNOCK / CREATE REFERRAL** |
| conflicting records, out-of-state area codes | **VERIFY FIRST** — name-collision match |

DNC never blocks a door knock or a CREATE REFERRAL on the dealer map. A DNC-flagged gold
dot is still a live lead — just not a phone lead.

## Step 5 — rank by warmth

Highest first:
1. **Email domain `@att.net`** — already an AT&T customer, strongest possible signal
2. `owner_occupied = true` — the resident decides; a landlord may not
3. `year_built` pre-1970 — copper-era wiring, long tenure
4. 100% equity + decades of tenure — owned outright, never switched
5. **Landlord** (`owner_occupied` false) — different pitch, may own multiple units
6. **MDU / apartment cluster** — one property manager, dozens of units. Highest leverage
   in the whole dataset. Look for many units sharing one address or coordinate.

## Step 6 — the output sheet

Columns: `Priority | Name | Phone 1 | Phone 1 Type | Phone 2 | Email | Address | City |
Dot Color | Built | Home Value | Equity % | Owner Occupied | Action | Why | Called |
Result | Notes`

Priority key: 1 = wireless DNC-clear · 2 = landline/business call-only · 3 = verify ·
4 = DNC, door only · 5 = no contact data · 6 = needs enrichment.

Format phones as **plain text** or Sheets mangles them. Freeze and bold row 1. Color GOLD
orange and GREEN green. Leave `Called` and `Result` empty for the rep.

If the user wants something simple and separate rather than another tab in a 15-tab
workbook, create a standalone sheet with `Google_Drive create_file`
(`contentMimeType: text/csv`) — it lands in their Drive, owned by them.

## The pitch that goes with it

> AT&T is retiring the copper network your address is on by 2029, and fiber is already
> live on your street. You can move now while the new-customer promo is on, or move later
> without it.

True, urgent, gives a reason-why, and it is a heads-up rather than a sales pitch.

**On price — never quote a flat figure.** Fiber 300 is $55 base, minus $15 promo (12 months
only), minus $10 autopay, minus $5/line wireless bundle. Best case ~$25 for year one, then
~$40-45. Say "in the $20s to $30s for the first year, I'll confirm your exact price before
anything is ordered."

## Sending

Never text a landline or a DNC number. One message, then a CALL — opt-outs spike on message
two. Get the copy and the recipient list approved before sending; a bad blast costs sender
reputation that credits cannot buy back.
