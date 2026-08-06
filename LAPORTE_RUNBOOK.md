# La Porte AT&T Fiber Drip — Operation Runbook

Plain-English summary of what we're doing and how to run it.

## The goal
Text **190 fiber-eligible homes** in a newly-lit La Porte (77571) fiber zone, have **AI answer
replies and book appointments**, all sent from **Patrick's own GHL account (Command / Connect &
Comm)** — NOT Zack's Frontline account.

## The cast (so the connectors stop being confusing)
- **Frontline Direct** (location TXw28...) = **Zack's** account. Connector name: `ghl-full`.
  We do NOT run the campaign here. (This Claude Code chat only has THIS one — used for door lookups.)
- **Command / Connect & Comm** (location xZj500...) = **Patrick's** account. Connector name: `command`.
  This is where the drip runs.
- Both connectors live in the **Claude app**. A Claude Code chat only gets the connectors that
  existed when it started — which is why this chat has `ghl-full` but not `command`.

## The leads (190, cleaned + split for an A/B test)
From the uploaded list, filtered to mobile-only, non-DNC, deduped. Split into 3 tagged files:
- `laporte_plain_sms.csv` (95) → tag `ab-plain-sms` → SMS, **no "AT&T"** mention
- `laporte_att_sms.csv` (85) → tag `ab-att-sms` → SMS, **AT&T**-branded
- `laporte_att_mms.csv` (10) → tag `ab-att-mms` → **AT&T + promo image** (MMS; capped to every
  10th because MMS costs more)
A/B question: does naming AT&T (and adding a picture) lift or hurt replies?

## The message (randomized per send, all 3 arms in AI_SALES_BOT.md)
Offer (truthful, verified June 2026): fiber **in the $40s** (20% bundle discount), **up to $150
bill credit** (AT&T issues a reward card; Patrick converts it to a bill credit), **we cover your
switch/cancellation fees**, **no contract, no data caps, up to 5 GIG**.
Sender = **Patrick, 832-247-4060**. Opt-out = "Text NO to unsubscribe from Command & Conq."

## How it runs (pick one)
**A) New Claude Code chat + `command` connector (recommended — Claude does the texting from Command):**
  1. Open a NEW Claude Code chat (it will load the `command` connector, which this older chat missed).
  2. Attach the 3 CSVs (a fresh container won't have them — they're not in git, they're PII).
  3. Paste the handoff prompt (in chat history / the "copy for new claude code" message).
  4. It creates the contacts in Command, drips 1 every 30 sec, randomized, starts with 2 for a
     test, waits for "go," then continues. AI answers replies + books. Skips NO/STOP.

**B) GHL native workflow (no connector, runs 24/7 inside Command):**
  Import the 3 CSVs into Command → 3 tag-triggered workflows (Send SMS + Drip Mode 2/min) →
  Conversation AI (Appointment Booking) for replies. Full steps in AI_SALES_BOT.md.

## Inbound / booking
AI handles replies and books appointments. For 24/7 (overnight) replies, GHL **Conversation AI**
(Appointment Booking mode + a Calendar) is the always-on engine — set up once in Command.

## Door-knocking (live, in THIS Frontline chat)
While canvassing, send an address → I look up the resident (name, mobile, clean vs DNC), add them
to the CRM tagged `door-knocked`/`follow-up`, and fire a personalized follow-up text from Frontline.
(Done so far: 3110 Hamilton = Claudette Saldana [not home, DNC]; 3118 Fondren = Danajo Barnhardt
[texted + tagged follow-up].)

## Status
- [x] Leads cleaned + split into 3 tagged CSVs (190)
- [x] Messages written (3 arms, randomized, bill-credit framing) — AI_SALES_BOT.md
- [x] Test texts verified to Patrick's phone
- [ ] Launch the Command drip (via new Code chat OR GHL workflow)
- [ ] AT&T promo image uploaded to Command Media Library (for the 10 MMS)
- [ ] Conversation AI + Calendar enabled in Command (for 24/7 booking)
