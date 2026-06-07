# AI GHL Sales Robot — AT&T Fiber (Patrick / Command)

The always-on robot lives in **GHL Conversation AI** ("AI Employee"). This file is its
brain (persona + script + booking rules) plus the exact GHL setup. Runs 24/7 inside
GHL — no Claude chat needs to be open.

Account: **Command / Connect & Comm** (xZj500PjsflIQg2j9f9D). A2P number already approved.

---

## The 3 parts of the robot
1. **Outbound** — GHL Workflow drips the opening SMS to tagged leads (1 msg/min).
2. **Brain** — Conversation AI replies as "Patrick," qualifies, handles objections.
3. **Booking** — Conversation AI in **Appointment Booking** mode drops them on a Calendar.

---

## ROBOT PERSONA (paste into Conversation AI -> "Bot training" / personality)

You are Patrick, a local AT&T sales rep in Houston. You are warm, brief, and human —
texting, not emailing. Keep replies under 2 short sentences. Never sound like a bot,
never use corporate jargon, never use emojis more than rarely. You sell AT&T home
internet (Fiber and Internet Air) and AT&T cell bundles. You are NOT "Optimus" — you
are Patrick with AT&T. Your only goal on every message: get the person to agree to a
short appointment/call, then book it.

Rules:
- Always brand as AT&T. Never say "Optimus."
- If they ask price: home internet is in the $40s/mo, 2 months free, free install, no
  contract. Cell bundle: 5 unlimited lines $50/mo + the new iPhone 17.
- If interested at all -> offer 2 specific time windows and book the soonest they accept.
- If they say STOP / not interested / wrong number -> politely stop, do not push.
- If they ask something you don't know -> say Patrick will confirm on the call, and book.
- Never invent promos beyond the facts above.

## OFFER FACTS (the only claims the robot may make)
- AT&T Fiber or Internet Air, plans in the **$40s/mo**
- **2 months free**, **free install**, **no contract**
- Bundle: **5 unlimited lines $50/mo** + **new iPhone 17**
- CTA: book a short call/appointment with Patrick

## OPENING SMS (outbound, the workflow sends one of these — rotate)
1. Hi, it's Patrick w/ AT&T. Fiber's available at your Houston address - 2 months free, $40s after. Got 15 min this week to set it up? Reply a day/time.
2. AT&T internet is ready at your address - 2 months free, low $40s. Want to grab a time to schedule? Reply YES and I'll send slots.
3. Hey, Patrick w/ AT&T here. Your address qualifies - 2 months free, $40s, free install, no contract. Open this week for a quick call? Reply YES.
4. Quick one - AT&T fiber/Air is live at your spot. 2 months free, $40s after. When's good for a 10-min call? Reply a time.
(GHL auto-appends the opt-out line; do not add "Reply STOP".)

## LA PORTE DRIP - fiber $40s + free trial (randomized, sender Patrick 832-247-4060)
Rotate one per contact; vary wording so no two are identical. Tag: laporte-77571. Account: Command.
No filler openers - lead with the offer.
1. AT&T Fiber is available at your La Porte address - in the $40s with a free trial. Call or text Patrick, AT&T, at 832-247-4060. Text NO to unsubscribe from Command & Conq.
2. Your La Porte address now qualifies for AT&T Fiber - $40s/mo, free trial to start. Patrick, AT&T: 832-247-4060. Text NO to opt out, Command & Conq.
3. AT&T Fiber is live in your neighborhood - low $40s with a free trial. Call or text Patrick at 832-247-4060. Text NO to unsubscribe, Command & Conq.
4. Fiber is available at your address - AT&T, $40s/mo, free trial included. Reach Patrick at 832-247-4060. Text NO to stop. Command & Conq.
5. AT&T Fiber at your La Porte address: $40s a month, free trial. Call or text Patrick, 832-247-4060. Text NO to unsubscribe from Command & Conq.
6. Your address is fiber-ready with AT&T - $40s/mo plus a free trial. Patrick, AT&T: 832-247-4060. Text NO to opt out, Command & Conq.
7. AT&T Fiber is now available in La Porte - $40s, free trial. Call or text Patrick at 832-247-4060. Text NO to unsubscribe. Command & Conq.
8. Fiber at your address - AT&T, in the $40s with a free trial. Patrick: 832-247-4060, call or text. Text NO to stop. Command & Conq.

## PROMO-HOOK DRIP v2 (verified AT&T offers, randomized, A/B graphics, 30s pacing)
Verified promos (att.com, June 2026): 20% bundle discount -> $40s/mo; up to $150 ($50/$100/$150
by speed) w/ wireless bundle - AT&T ISSUES THIS AS A VISA REWARD CARD; Patrick converts it to a
BILL CREDIT for the customer, so all messaging says "bill credit" (accurate to what they receive);
AT&T covers switch cancellation fees; no contract; no data caps; up to 5 GIG. DO NOT use the $200
offer (expired 6/1/26). "Free trial / 2 mo
free" UNVERIFIED - confirm on att.com before using. Lead with the catch, no filler.
1. AT&T Fiber is live in La Porte - in the $40s when you bundle, plus up to a $150 bill credit. Call or text Patrick, AT&T: 832-247-4060. Text NO to unsubscribe, Command & Conq.
2. Switch to AT&T Fiber - we cover your current provider's cancellation fees, $40s/mo, no contract. Patrick, AT&T: 832-247-4060. Text NO to opt out, Command & Conq.
3. AT&T Fiber at your address: $40s/mo, no annual contract, no data caps. Up to $150 bill credit. Call/text Patrick 832-247-4060. Text NO to stop, Command & Conq.
4. Fiber's available in La Porte - up to $150 AT&T bill credit + $40s/mo with bundle. Patrick, AT&T: 832-247-4060. Text NO to unsubscribe, Command & Conq.
5. AT&T Fiber - speeds up to 5 GIG, $40s/mo, no data caps. We'll cover your switch fees. Patrick: 832-247-4060, call or text. Text NO to stop, Command & Conq.
6. Your La Porte address qualifies for AT&T Fiber - $40s/mo + up to $150 bill credit. Call or text Patrick 832-247-4060. Text NO to opt out, Command & Conq.
7. AT&T Fiber in La Porte: no contract, no data caps, $40s/mo. Switching? We cover your cancellation fees. Patrick, AT&T: 832-247-4060. Text NO to unsubscribe, Command & Conq.
8. Get AT&T Fiber at your address - $40s/mo, up to $150 bill credit, up to 5 GIG. Call/text Patrick 832-247-4060. Text NO to stop, Command & Conq.
9. AT&T Fiber's now in your neighborhood - $40s with bundle, $150 bill credit, no contract. Patrick: 832-247-4060. Text NO to opt out, Command & Conq.
10. Fiber at your La Porte address - AT&T, $40s/mo, we pay your switch fees, no data caps. Call or text Patrick 832-247-4060. Text NO to unsubscribe, Command & Conq.

## LIVE A/B DESIGN (La Porte 190, run from Command via GHL workflow)
3 arms, pre-split into 3 tagged CSVs (so the A/B is reliable, no GHL "Split" action needed).
Graphics (MMS) cost more than SMS -> capped to every 10th of the AT&T arm to keep MMS spend tiny.
- ARM 1 - `ab-plain-sms` (95): NO "AT&T" anywhere, plain SMS. Tests if dropping the brand lifts replies.
- ARM 2 - `ab-att-sms`  (85): AT&T-branded, plain SMS.
- ARM 3 - `ab-att-mms`  (10): AT&T-branded + the promo IMAGE (MMS). Every 10th of the AT&T arm only.
Files (PII, /home/user, not committed): laporte_plain_sms.csv, laporte_att_sms.csv, laporte_att_mms.csv.

### Spintax messages (GHL randomizes {a|b|c} per send)
ARM 1 (ab-plain-sms, SMS, no AT&T):
`Fiber {is live|is now available} in your La Porte neighborhood - {$40s/mo|in the $40s}, up to a $150 bill credit, and we cover your switch fees. {Call or text|Text or call} Patrick: 832-247-4060. Text NO to unsubscribe, Command & Conq.`
ARM 2 (ab-att-sms, SMS, AT&T):
`AT&T Fiber {is live in|is now available in|just launched in} La Porte - {$40s/mo with bundle|in the $40s when you bundle}, plus up to a $150 bill credit. {Call or text|Text or call} Patrick, AT&T: 832-247-4060. Text NO to unsubscribe, Command & Conq.`
ARM 3 (ab-att-mms, MMS, AT&T): same as ARM 2 + attach the AT&T promo image.

## HOW TO RUN THE 30s DRIP (Command, GHL workflow)
1. Import the 3 CSVs into Command (Contacts -> Import). Tags auto-apply.
2. Three tag-triggered workflows (one per arm):
   - Trigger = Contact Tag added (`ab-plain-sms` / `ab-att-sms` / `ab-att-mms`)
   - Action = Send SMS with that arm's spintax; ARM 3 also attaches the image (MMS step).
   - Settings -> Drip Mode ON -> 2 events per 1 minute (~1 text / 30 sec).
3. Inbound (shared): Conversation AI (Appointment Booking) + a Calendar books replies.
4. Opt-out: STOP auto-honored; add a workflow: inbound contains "NO" -> Set DND.
5. TEST FIRST: import 2-3 test contacts (Patrick's own numbers, one per arm), confirm picture vs
   text + no "AT&T" in ARM 1 + AI books + NO sets DND. THEN import the real CSVs (that = launch).
6. TRACK by tag: reply + appointment rate per arm. Keep the winner; then consider the 129 DNC bucket.
SAFETY: tested to Patrick's phone first (done). Mobile-only. Honor STOP/NO. Skip DNC bucket.

## OBJECTION SNIPPETS (for the brain)
- "Too expensive" -> It's actually in the $40s with 2 months free and no contract. Want me to lock that in?
- "Already have internet" -> Totally fine - most folks switch for the 2 free months + lower price. Worth a 10-min look?
- "Send info" -> I can text the details, but the deal's fastest on a quick call. What time today or tomorrow?
- "Who is this" -> Patrick with AT&T - your address came up as fiber-eligible. Want the details?

---

## GHL SETUP (UI - do once, in the Command sub-account)
1. **Calendar** (required for booking): Settings -> Calendars -> create "AT&T Fiber Appts",
   set your availability. (Booking can't work without this.)
2. **Conversation AI**: Settings -> Conversation AI ->
   - Mode: **Appointment Booking**
   - Connect the calendar from step 1
   - Paste the PERSONA above into the bot personality/training
   - Set business context = AT&T fiber, Houston
3. **Workflow** (the outbound drip):
   - Trigger: Contact tag added = `att-fiber-robot`
   - Action: Send SMS (one of the OPENING SMS, use a rotation/spintax)
   - Wait 1 minute, then next contact (throttle so you don't blast)
   - Enable Conversation AI to take over on reply
4. **Turn it on**: tag a small batch (5-10 leads) with `att-fiber-robot` first. Watch it
   send + reply + book. Then scale to 200.

## SAFETY
- Test with 5 leads before scaling. Mobile numbers only (run number intelligence).
- Robot must honor STOP/opt-out (GHL DND handles this; the persona reinforces it).
- Booking goes to the Calendar; double-check the first few land correctly.
