# SMS Campaign — 300 contacts, 1 min apart (AT&T fiber / Internet Air)

Status: PLANNED for the day after 2026-06-04. Not yet sent.

## Offer (per Patrick)
- AT&T **fiber OR Internet Air**, whichever fits the address
- Pricing **in the $40s/mo**
- **2 months free**
- From Patrick / AT&T (never "Optimus"). Every text ends with an opt-out.

## Send rules
- 300 contacts, **one text per minute** (~5 hours total).
- **Mobile numbers only** (run GHL number intelligence first; landlines fail + hurt A2P trust).
- Send through the **A2P-registered** GHL number.
- Honor STOP/opt-outs (GHL auto-handles).

## How it sends (pick one tomorrow)
1. **GHL workflow (recommended):** import/tag the 300 -> smart list (Line type = Mobile) -> workflow:
   send SMS = the message field, **Wait 1 minute**, repeat. Runs on GHL infra through A2P.
2. **PC script:** a sender that loops the 300, sends via GHL API, `sleep(60)` between. Run on the PC.

## Message variations (rotate one per contact)
 1. Hi, it's Patrick with AT&T. Fiber's available at your address - 2 months free to try it, then plans in the $40s. Want me to lock it in? Reply STOP to opt out
 2. AT&T Internet Air is live at your address - wireless home internet, 2 months free, $40s after. Interested? Reply YES, or STOP to opt out
 3. Quick one - AT&T fiber just opened at your spot. First 2 months free, then low $40s/mo. Worth a look? Reply STOP to opt out
 4. Hey, Patrick w/ AT&T. Fiber or Internet Air at your address - start with 2 months free, $40s after. Reply YES. STOP to opt out
 5. Good news - your address qualifies for AT&T internet. 2 months on us, then $40s/mo. Want details? Reply STOP to opt out
 6. Hi! AT&T fiber/Air available at you. Try it 2 months free, plans start in the $40s. Reply YES and I'll set it up. STOP to opt out
 7. Patrick here with AT&T. Reliable home internet at your address - 2 free months, $40s after. 5-min setup? Reply STOP to opt out
 8. Your block's lit for AT&T. Fiber or Internet Air, 2 months free, low $40s. Interested? Reply YES. STOP to opt out
 9. Hi, AT&T has internet ready at your address - 2 months free, then $40s/mo, no big commitment. Reply STOP to opt out
10. Hey, it's Patrick w/ AT&T. 2 months free on fiber or Internet Air, $40s after. Want me to check your exact address? STOP to opt out

## Open for tomorrow
- WHICH 300? (a GHL tag / smart list, a metro, the imported business list, or cells from a specific source?)
- Which sub-account + A2P number (Frontline TXw28sw0Z2rl6tcCDhJY or Connect & Comm xZj500PjsflIQg2j9f9D)?
