# -*- coding: utf-8 -*-
import importlib.util, sys
spec = importlib.util.spec_from_file_location("chk", "templates/sms_variants_check.py")
GSM = set("@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>?¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà")
EXT = set("^{}\\[~]|€")
NAME_MAX, ADDR_MAX, APPEND = 10, 36, 27
def check(v):
    f = v.replace("{{contact.first_name}}","X"*NAME_MAX).replace("{{contact.address1}}","X"*ADDR_MAX)
    n=0
    for c in f:
        if c in EXT: n+=2
        elif c in GSM: n+=1
        else: return "*** NON-GSM %r" % c
    t=n+APPEND
    return "OK 1 seg (%d)"%t if t<=160 else "*** %d chars = %d segs"%(t,-(-t//153))

POOLS = {
"GREEN - second touch (3-5 days after touch 1, no reply)": [
 "{{contact.first_name}}, Patrick again - AT&T Fiber. Still able to get {{contact.address1}} on fiber. Worth a look?",
 "Circling back on {{contact.address1}}. Patrick with AT&T Fiber. Want me to check what's open there?",
 "{{contact.first_name}} - Patrick, AT&T Fiber. Fiber's still available at {{contact.address1}}. Want the speeds?",
 "Following up on the fiber at {{contact.address1}}. Patrick with AT&T. Bad time, or want details?",
 "{{contact.first_name}}, checking back. {{contact.address1}} can still get fiber. Patrick with AT&T Fiber.",
],
"GREEN - third touch (a week later, last one)": [
 "{{contact.first_name}} - last note from me. Fiber is open at {{contact.address1}} if you want it. Patrick, AT&T.",
 "Patrick with AT&T Fiber. I'll leave it here - {{contact.address1}} has fiber when you're ready. Want details?",
 "{{contact.first_name}}, closing this out. Fiber at {{contact.address1}} whenever you want it. Patrick, AT&T.",
],
"GOLD - second touch": [
 "{{contact.first_name}}, Patrick again. Your copper line at {{contact.address1}} can still move to fiber. Interested?",
 "Following up - {{contact.address1}} is still eligible to upgrade off copper. Patrick with AT&T Fiber.",
 "{{contact.first_name}} - AT&T Fiber. The upgrade at {{contact.address1}} is still open. Want me to check it?",
 "Patrick, AT&T Fiber. Copper retires by 2029 and {{contact.address1}} has fiber now. Want to move?",
 "{{contact.first_name}}, circling back on the fiber upgrade for {{contact.address1}}. Worth 2 minutes?",
],
"BUSINESS - speed tier, never a residential figure": [
 "{{contact.first_name}}, Patrick with AT&T Business Fiber. Fiber is live at {{contact.address1}}. What's your upload now?",
 "Patrick, AT&T Business Fiber. {{contact.address1}} can get fiber. How many lines do you run there?",
 "{{contact.first_name}} - AT&T Business Fiber reached {{contact.address1}}. Want the tiers for your business?",
 "Patrick with AT&T Business Fiber. {{contact.address1}} is fiber-ready. Does your upload slow you down?",
 "{{contact.first_name}}, Patrick, AT&T Business Fiber. Fiber at {{contact.address1}} now. Want options for the shop?",
],
"REPLIED YES but never called - the 24-name backlog": [
 "{{contact.first_name}}, Patrick with AT&T Fiber. You asked about fiber at {{contact.address1}} - still want it?",
 "Patrick, AT&T Fiber. You said yes on fiber for {{contact.address1}} a while back. Still interested?",
 "{{contact.first_name}} - my fault for the delay. Fiber at {{contact.address1}} is still open. Want it?",
 "Patrick with AT&T Fiber. Picking up where we left off on {{contact.address1}}. Good time to talk?",
],
"AFTER A MISSED CALL - they rang us": [
 "{{contact.first_name}}, Patrick with AT&T Fiber returning your call about {{contact.address1}}. Good time now?",
 "Sorry I missed you - Patrick, AT&T Fiber. Calling about fiber at {{contact.address1}}. When suits?",
 "{{contact.first_name}} - Patrick, AT&T Fiber. Missed your call on {{contact.address1}}. Want me to try again?",
],
}
for label, pool in POOLS.items():
    print("="*70); print(label); print("="*70)
    for i,v in enumerate(pool,1):
        print("%2d. [%s]\n    %s" % (i, check(v), v))
    print()
