# Randomized one-segment SMS variants — 2026-09-05

Patrick: *"I still want it randomized w the offer but address and name are working so do it."*

**Every variant below is MEASURED, not eyeballed.** `sms_variants_check.py` in this folder
re-runs the check: it rejects any character outside GSM-7 (one such character forces UCS-2
at 67 chars/segment — that is what made the "James" template NINE segments), fills the
merge fields with worst-case values seen in this CRM (10-char first name, 36-char
address1), and adds GHL's 27-character appended STOP line. **All 20 pass at ONE SEGMENT.**

## Rules baked into every line
- Identifies as **"Patrick with AT&T Fiber"**. Never Optimus, never "James", never signs as AT&T itself.
- **No opt-out line** — GHL appends its own. Writing one doubles it, which is the clearest tell no human wrote the message.
- **No price.** If price comes up on the reply: *"in the $20s to $30s for the first year, I'll confirm your exact price before anything is ordered."* Business is by speed tier, never a residential figure.
- **No "10x faster", no "$30/month", no "2 free months", no "4 months free", no iPhone.** The 4-months claim in the live blast matches no AT&T promo I can find (current business offers are monthly discounts + free install).
- Plain ASCII only. **No bullets, no em dashes, no curly quotes, no emoji.**
- Address leads or sits in the first clause. These leads ARE the address.

## GREEN — not an AT&T customer. An availability notice, never a switch pitch.

1. `{{contact.first_name}} - Patrick with AT&T Fiber. Fiber is live at {{contact.address1}}. Who do you have for internet now?`
2. `Patrick with AT&T Fiber here. Fiber just reached {{contact.address1}}. Worth 2 min to see what's open to you?`
3. `{{contact.first_name}}, Patrick with AT&T Fiber. {{contact.address1}} can get fiber now. Want the speeds for it?`
4. `Patrick with AT&T Fiber. {{contact.address1}} is now in a fiber area. Who's your provider today?`
5. `{{contact.first_name}} - fiber went live on your street. Patrick with AT&T Fiber. Want what's available at {{contact.address1}}?`
6. `Patrick with AT&T Fiber. We just lit fiber at {{contact.address1}}. Upload matches download. Interested?`
7. `{{contact.first_name}}, this is Patrick with AT&T Fiber. Fiber is available at {{contact.address1}} now. Want details?`
8. `Patrick with AT&T Fiber. Checking in on {{contact.address1}} - fiber is open there now. What do you use today?`
9. `{{contact.first_name}} - AT&T fiber reached {{contact.address1}}. Patrick here. Want me to check your options?`
10. `Patrick with AT&T Fiber. {{contact.address1}} is fiber-ready. No evening slowdown. Want the tiers?`

## GOLD — existing AT&T customer on copper. An UPGRADE, no competitor to beat.

1. `{{contact.first_name}} - Patrick with AT&T Fiber. You're on copper at {{contact.address1}}. Fiber's there now. Want the upgrade?`
2. `Patrick with AT&T Fiber. {{contact.address1}} can move off copper to fiber. Same account. Want details?`
3. `{{contact.first_name}}, AT&T is retiring copper. Fiber is live at {{contact.address1}}. Patrick here - want to move up?`
4. `Patrick with AT&T Fiber. Your line at {{contact.address1}} can upgrade to fiber. Want me to check it?`
5. `{{contact.first_name}} - copper is being retired. {{contact.address1}} has fiber now. Patrick, AT&T. Interested?`
6. `Patrick with AT&T Fiber. {{contact.address1}} qualifies for a fiber upgrade. You keep your account. Want it?`
7. `{{contact.first_name}}, Patrick with AT&T Fiber. Fiber replaced the copper at {{contact.address1}}. Want to switch over?`
8. `Patrick with AT&T Fiber. Heads up - copper retires by 2029. {{contact.address1}} has fiber now. Want details?`
9. `{{contact.first_name}} - your service at {{contact.address1}} can go fiber. Patrick with AT&T. Worth a look?`
10. `Patrick with AT&T Fiber. {{contact.address1}} is eligible to upgrade from copper. Want the speeds?`

## Two things to fix before these go out at volume

**1. `address1` IS INCONSISTENT AND IT SHOWS IN THE MESSAGE.** Measured on live records:
James Barnes `address1` = `5717 Marigold Ave, Milton, FL, 32570` (36 chars, whole address),
Daniel Jacobs = `5673 Zinnia Ave` (15 chars, street only). So the same variant reads
*"Fiber is live at 5673 Zinnia Ave."* on one record and *"Fiber is live at 5717 Marigold
Ave, Milton, FL, 32570."* on another. Both fit one segment — the variants are budgeted for
the long form — but the short form reads far better. **Normalising `address1` to street-only
would improve every send.** Not done: that is a bulk CRM write and needs Patrick's go.

**2. Rotation.** If the sender has a spin/rotation feature, load all 10 of the matching
pool. If it does not, split the batch: variant 1 to the first tenth, variant 2 to the
next, and so on. **What must never happen is one variant to the whole list** — identical
bulk copy is what carriers filter on (error 30007).

## Verify before use
```
python3 templates/sms_variants_check.py
```
Re-run it after ANY edit. A single em dash or curly quote turns a 1-segment message into
a 3-segment one and nothing warns you.
