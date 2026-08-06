# Optimus Houston 200 — drip + AI appointment booking

Status: PLANNED. Not yet sent. Goal: drip 200 Houston fiber-hunter leads, GHL Conversation AI books appointments.

## The 3 pieces
1. LEADS: pull 200 Houston leads from the fiber-hunter master sheet (1FhO, Hunter Leads / Hunter Houston
   tabs) -> GHL contacts, tag `optimus-houston-200`, mobile numbers only (run number intelligence).
2. DRIP: GHL workflow -> trigger on the tag -> send SMS (booking CTA) -> Wait 1 min -> loop. Through A2P number.
3. AI BOOKING: GHL **Conversation AI** set to **Appointment Booking** mode + a connected calendar.
   On a lead reply, the bot converses and books. (Settings -> Conversation AI; needs a Calendar set up.)

## Cannot be run from a Claude session
The multi-hour drip and the live AI conversation must run on GHL (workflow + Conversation AI), not from
an ephemeral Claude session. Claude's role: load leads + messages, guide the GHL setup.

## Booking-CTA messages (rotate one per contact)
1. Hi, Patrick w/ AT&T. Fiber's available at your Houston address - 2 months free, $40s after. Got 15 min this week to get it set up? Reply a day/time. STOP to opt out
2. AT&T internet is ready at your address - 2 months free, low $40s. Want to grab a time to schedule it? Reply YES and I'll send slots. STOP to opt out
3. Quick one - AT&T fiber/Air is live at your spot. 2 months free, $40s after. When's good for a 10-min setup call? Reply a time. STOP to opt out
4. Hey, it's Patrick w/ AT&T. Your address qualifies - 2 months free, $40s. Want me to book your install window? Reply YES. STOP to opt out
5. Hi! AT&T has 2 months free + $40s plans at your address. Pick a time and I'll lock your appointment. Reply a day/time. STOP to opt out
6. Patrick here, AT&T. Fiber or Internet Air at you - free for 2 months, then $40s. Open this week for a quick call? Reply YES. STOP to opt out
7. Your Houston address is good for AT&T - 2 months free, low $40s. Reply with a time that works and I'll book it. STOP to opt out
8. Hey, AT&T fiber's available at your place. 2 months free, $40s after. Want the next open install slot? Reply YES. STOP to opt out

## Open for next session
- WHICH sheet tab / metro filter = the 200 Houston leads (Hunter Leads? Hunter Houston Dedup?)
- Confirm A2P number + sub-account (Frontline TXw28sw0Z2rl6tcCDhJY)
- Set up: a GHL Calendar + Conversation AI (Appointment Booking) before the drip goes out
