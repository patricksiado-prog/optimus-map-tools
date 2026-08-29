# CLAUDE.md — optimus-map-tools

**Read `INDEX.md` first, then `BRAIN.md`.** That is the whole onboarding.

---

## What this repo is

The **business brain and the skills**. Not the hunter — see below.

| File | What it is |
|---|---|
| `INDEX.md` | Start here. Where everything lives, how BRAIN works. |
| `BRAIN.md` | Long-term memory. 3,110 lines, 22 parts. **The single source of truth.** |
| `.claude/skills/` | Four skills that auto-load: `gold-dot-workup`, `fiber-freshness`, `new-build-outreach`, `close-rate` |
| `archive/` | Superseded docs. Kept, not deleted. Do not act on them. |

## The other repo — do not confuse them

**`patricksiado-prog/Go-High-Level-MCP-2026-Complete`**, branch
`claude/optimus-map-tools-setup-6dcl6o`, holds `optimus/` — the hunter itself
(`precise_fiber_hunter.py`, 5,127 lines). **The hunter self-updates from that repo, not
this one.** Push hunter code there.

That repo has its own `CLAUDE.md` covering the code, the update path, and the deploy
conventions. **Business context lives here in `BRAIN.md` and is not duplicated there.**

## How BRAIN.md works

- **Parts** are chronological, one per session: `## 2026-08-22 (part 22) — TITLE`
- **Sections** are numbered continuously and are the citable unit: `§107`, `§120`
- **Old entries are never deleted** — they are flagged superseded, and the newer entry
  says what it overturns. Deleting history hides *why* a decision changed and lets a
  future session re-adopt an abandoned idea.
- **When two sections disagree, the higher number wins.** Read the highest part first.
- **To add:** append a new part at the end. Never edit an old one except to flag it
  superseded.

**Do not put hard rules in BRAIN.md.** Patrick, verbatim: *"don't add hard rules" /
"don't make rules in brain that i have to deprogram."* It records what is **true**, not
what is **forbidden**.

## The doctrine, in case you read nothing else

| Dot | Means | Pays | Count |
|---|---|---|---|
| **GREEN** | fiber live, NOT an AT&T customer | **$500** | 460,313 |
| **GOLD** | fiber live, AT&T customer still on copper | **$140** | ~9,652 |
| GREY | already an AT&T fiber customer | — | never written to the sheet |

Green is 48x the volume and 3.6x the pay. **Gold is not the target** — gold density is a
timestamp saying a street was lit recently and nobody has sold it yet. Find the gold
cluster, work the green inside it. See BRAIN part 20.

**The binding constraint:** green has addresses but no phone numbers.

## Working conventions

- **The sheet** is `1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA`. `Precise Fiber` is
  474,075 rows and live. **Never read it wholesale** — create one temp tab, use bounded
  QUERY/COUNTIF, read the result, delete the tab. Pulling it whole fails with "request
  too large."
- **`Gold Dots` has no header row.** Data starts at row 1.
- **Never write placeholder text into a phone field.** The sheet once stored the literal
  string `(all DNC)` instead of digits and the numbers were lost. Actual digits, stored
  as text, always.
- **DealMachine `enrich_address` requires a ZIP** and hard-fails without one.
- **`estimate_cost=true` makes searches free.** Price before you spend.
- **Landlines cannot be texted** — Twilio 30006 is a carrier failure, not a compliance
  flag. Landline means phone call.
- **Quiet hours 8am–9pm** for any outbound texting.
- ⚠️ The `fiber-freshness` skill scores freshness as `1 - grey%`. **That formula cannot
  run** — grey is never written to the sheet. Gold density is the substitute.

## How Patrick wants to be talked to

Move fast, do the work, report results. He corrects hard and directly — take it and move
on, don't over-apologise. Full verbatim list is in `INDEX.md`.
