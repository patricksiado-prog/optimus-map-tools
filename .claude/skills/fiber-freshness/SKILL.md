---
name: fiber-freshness
description: Score and rank AT&T fiber zones by how recently they were lit, using the gold/grey/green dot mix from the Precise Fiber Hunter output. Use when asked to find fresh fiber, newly-lit streets, where to sell next, which zone to work, to analyze hunter output, or to build a target/door-knock list from captured dots.
---

# Fiber Freshness Scoring

Finds newly-lit fiber zones from hunter output so we get there before competitors.

## The dot legend (never confuse these)

| Dot | Means | Value |
|---|---|---|
| **GREEN** | Fiber-eligible, NOT a customer | The prize — sellable today |
| **GOLD/ORANGE** | AT&T customer still on COPPER | Upgrade target, and proof copper exists here |
| **GREY** | Already an AT&T FIBER customer | Skip — already sold, and a competitor got there |

## Core insight

**Grey share is a clock.** Grey only accumulates after fiber lights up and people buy.

- Low grey + high green/gold  →  **just lit, nobody has sold it yet**
- High grey                   →  **mature, picked over, competitors already worked it**

AT&T hits 30%+ penetration within 12 months of lighting a market, and mature cohorts
reach 30-50%. So roughly three-quarters of a street's lifetime penetration is decided in
year one. Being early beats being thorough.

## Freshness score

For a zone (street, block, or lat/lng cell — cluster to ~0.005 deg, about 3 blocks):

```
total    = green + gold + grey
grey_pct = grey / total

FRESHNESS = (1 - grey_pct) * 100
OPPORTUNITY = green + gold        # how many doors are actually sellable
```

Rank by FRESHNESS, break ties with OPPORTUNITY. Require `total >= 15` before scoring —
smaller samples are noise.

| Freshness | Grey share | Read | Action |
|---|---|---|---|
| 90-100 | <10% | **VIRGIN** — just lit | Drop everything, work it now |
| 70-89 | 10-30% | Early, still winnable | Work next |
| 40-69 | 30-60% | Maturing | Only if nothing fresher |
| <40 | >60% | Picked over | Skip |

**A zone with gold and NO grey is the single strongest signal we have.** It means copper
customers exist AND fiber is available AND literally nobody has converted yet.

## Procedure

1. Read the `Gold Dots` and `Precise Fiber` tabs of the ATT FIBER LEADS sheet
   (`1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA`).
2. Bucket rows into zones by rounding lat/lng to 3 decimals (~110m) or by street name.
3. Count green / gold / grey per zone. Compute FRESHNESS and OPPORTUNITY.
4. Drop zones with total < 15.
5. Sort by FRESHNESS desc, then OPPORTUNITY desc.
6. Report the top zones with street names, counts, and score — not raw rows.

## Enrichment (only after ranking)

Never enrich before ranking. Enrich only the top zones.

- Dedupe on **lat/lng first**. Apartment buildings share one coordinate — 26 units at one
  point costs 52 credits and returns one management LLC. Multi-unit = a property-manager
  phone call, not 26 texts.
- `dealmachine_enrich_latlng` costs 2 credits. **Do NOT pass the `fields` parameter** —
  it fails with "Reverse geocode enrichment failed". Omit it.
- Filter results to: `owner_occupied = true`, phone `type = wireless`,
  `do_not_call = false`. Expect ~70% usable, ~29% DNC-blocked.
- Pre-filter with the free `people` fields where possible (`has_wireless_phone`,
  `has_non_dnc_phone` are filterable) to avoid paying for records we will discard.
- Run `dealmachine_usage` (free) before any batch.

## Selling into a fresh zone

- Lead with the **copper retirement** — AT&T is retiring copper by 2029 and fiber-build
  areas convert by then. Gold-dot households have to move eventually. That is a true,
  urgent, non-salesy reason to call.
- Use the owner's name from DealMachine — it lifts door-open rates 10-15%.
- Never text a landline (Twilio error 30006) or a DNC-flagged number.
- One text, then a CALL. Opt-outs spike on message 2-3, so the second touch must not be
  another text.

## Output format

Rank table: Zone | Green | Gold | Grey | Freshness | Opportunity | Verdict.
Then name the single zone to work next and why.
