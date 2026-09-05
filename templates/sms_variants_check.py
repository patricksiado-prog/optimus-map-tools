# -*- coding: utf-8 -*-
# GSM-7 basic set. Anything outside it forces UCS-2 (67 chars/segment) -> instant multi-segment.
GSM = set(
 "@£$¥èéùìòÇ\nØø\rÅå"
 "Δ_ΦΓΛΩΠΨΣΘΞÆæßÉ"
 " !\"#¤%&'()*+,-./0123456789:;<=>?"
 "¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§"
 "¿abcdefghijklmnopqrstuvwxyzäöñüà")
EXT = set("^{}\\[~]|€")   # GSM-7 extended: costs 2 characters each

# worst-case merge values seen in this CRM
NAME_MAX = 10                        # "Stephanie"
ADDR_MAX = 36                        # "5717 Marigold Ave, Milton, FL, 32570"
GHL_APPEND = len("\nReply STOP to unsubscribe.")   # 27

def cost(s):
    n = 0
    for c in s:
        if c in EXT: n += 2
        elif c in GSM: n += 1
        else: return None, c          # non-GSM char -> UCS-2, reject
    return n, None

def check(v):
    filled = v.replace("{{contact.first_name}}", "X"*NAME_MAX).replace("{{contact.address1}}", "X"*ADDR_MAX)
    n, bad = cost(filled)
    if n is None: return None, "NON-GSM CHAR %r -> would force UCS-2" % bad
    total = n + GHL_APPEND
    return total, ("OK 1 segment" if total <= 160 else "*** %d chars = %d segments" % (total, -(-total//153)))

GREEN = [
 "{{contact.first_name}} - Patrick with AT&T Fiber. Fiber is live at {{contact.address1}}. Who do you have for internet now?",
 "Patrick with AT&T Fiber here. Fiber just reached {{contact.address1}}. Worth 2 min to see what's open to you?",
 "{{contact.first_name}}, Patrick with AT&T Fiber. {{contact.address1}} can get fiber now. Want the speeds for it?",
 "Patrick with AT&T Fiber. {{contact.address1}} is now in a fiber area. Who's your provider today?",
 "{{contact.first_name}} - fiber went live on your street. Patrick with AT&T Fiber. Want what's available at {{contact.address1}}?",
 "Patrick with AT&T Fiber. We just lit fiber at {{contact.address1}}. Upload matches download. Interested?",
 "{{contact.first_name}}, this is Patrick with AT&T Fiber. Fiber is available at {{contact.address1}} now. Want details?",
 "Patrick with AT&T Fiber. Checking in on {{contact.address1}} - fiber is open there now. What do you use today?",
 "{{contact.first_name}} - AT&T fiber reached {{contact.address1}}. Patrick here. Want me to check your options?",
 "Patrick with AT&T Fiber. {{contact.address1}} is fiber-ready. No evening slowdown. Want the tiers?",
]

GOLD = [
 "{{contact.first_name}} - Patrick with AT&T Fiber. You're on copper at {{contact.address1}}. Fiber's there now. Want the upgrade?",
 "Patrick with AT&T Fiber. {{contact.address1}} can move off copper to fiber. Same account. Want details?",
 "{{contact.first_name}}, AT&T is retiring copper. Fiber is live at {{contact.address1}}. Patrick here - want to move up?",
 "Patrick with AT&T Fiber. Your line at {{contact.address1}} can upgrade to fiber. Want me to check it?",
 "{{contact.first_name}} - copper is being retired. {{contact.address1}} has fiber now. Patrick, AT&T. Interested?",
 "Patrick with AT&T Fiber. {{contact.address1}} qualifies for a fiber upgrade. You keep your account. Want it?",
 "{{contact.first_name}}, Patrick with AT&T Fiber. Fiber replaced the copper at {{contact.address1}}. Want to switch over?",
 "Patrick with AT&T Fiber. Heads up - copper retires by 2029. {{contact.address1}} has fiber now. Want details?",
 "{{contact.first_name}} - your service at {{contact.address1}} can go fiber. Patrick with AT&T. Worth a look?",
 "Patrick with AT&T Fiber. {{contact.address1}} is eligible to upgrade from copper. Want the speeds?",
]

for label, pool in (("GREEN - availability notice", GREEN), ("GOLD - copper upgrade", GOLD)):
    print("="*72); print(label); print("="*72)
    for i, v in enumerate(pool, 1):
        n, note = check(v)
        print("%2d. [%s]" % (i, note))
        print("    " + v)
    print()
