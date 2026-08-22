#!/usr/bin/env python3
"""Generate one randomized, one-segment SMS per lead. No two alike.

Enforces, mechanically, every rule the Aug 21 batch broke:
  * "Patrick with AT&T Fiber" -- never the dealer brand
  * NO opt-out line (GoHighLevel appends its own; writing one doubles it)
  * body <= 133 chars so body + GHL's 27-char append stays in ONE segment
  * no price in the first text
  * absentee owners are asked about the property, never "your address"
  * every message differs from every other

Input CSV needs: first_name, address, street, city, dot (GREEN|GOLD),
optionally absentee (1/0). Output CSV adds `message` and `chars`.

    python3 write_messages.py leads.csv out.csv --seed 7
"""
import argparse, csv, hashlib, random, re, sys

GHL_APPEND = 27          # "\nReply STOP to unsubscribe."
ONE_SEGMENT = 160
MAX_BODY = ONE_SEGMENT - GHL_APPEND      # 133

# Shapes, not scripts. {n}=name {s}=street {a}=address {c}=city
# AREA shapes: fiber is live in the AREA and we offer to CHECK the address.
# Never assert a specific address qualifies unless it came off a verified dot --
# DealMachine-sourced leads are not fiber-verified and the claim would be unbacked.
GREEN = [
    "Hi {n} - Patrick with AT&T Fiber. Fiber just went live on {s}. Want me to check if your address can get it?",
    "{n} - Patrick with AT&T Fiber. AT&T fiber is now live in your part of {c}. Want me to check what your address can get?",
    "Hi {n}, Patrick with AT&T Fiber. Fiber reached {s} this month. Want me to look up what you qualify for?",
    "{n} - Patrick with AT&T Fiber. {s} just got fiber. Copper is being retired, so worth knowing your options. Interested?",
    "Hi {n} - Patrick with AT&T Fiber. We lit fiber near {s} in {c}. Want me to check your address?",
    "{n}, Patrick with AT&T Fiber here. Fiber is live around {s} now. Happy to check what speeds you can get. Interested?",
    "Hi {n} - Patrick with AT&T Fiber. Fiber just reached {s}. Want to know what you qualify for?",
    "{n} - Patrick with AT&T Fiber. Fiber is live on {s} now. Want me to check your address?",
    "Hi {n}, Patrick with AT&T Fiber. {s} has fiber now. Want the speeds and options?",
    "{n} - Patrick with AT&T Fiber. Fiber went live near you in {c}. Want me to check your street?",
    "Hi {n}, Patrick with AT&T Fiber. AT&T just lit fiber on {s}. Worth checking your address?",
]
GREEN_ABSENTEE = [
    "{n} - Patrick with AT&T Fiber. Fiber is now live at {a} in {c}. Want me to check the options for that address?",
    "Hi {n}, Patrick with AT&T Fiber. AT&T fiber just went live on {s}. Your property at {a} is covered. Worth a look?",
    "{n} - Patrick with AT&T Fiber. Fiber went live on {s} in {c}. If anyone's in that property it's an easy add. Interested?",
    "Hi {n} - Patrick with AT&T Fiber. {a} now has fiber available. Want me to send what the property qualifies for?",
]
GOLD = [
    "Hi {n} - Patrick with AT&T Fiber. You're on our copper line at {a}. Copper is being retired and fiber is live there now. Details?",
    "{n} - Patrick with AT&T Fiber. Fiber is live on {s} and you're still on copper. It's an upgrade, not a switch. Want the details?",
    "Hi {n}, Patrick with AT&T Fiber. Your line at {a} is copper. We're retiring it by 2027 and fiber is ready now. Want to move up?",
    "{n} - Patrick with AT&T Fiber. Copper on {s} is being retired. Fiber is already live at your place. Want me to set the upgrade?",
    "Hi {n} - Patrick with AT&T Fiber. You get migrated off copper either way; you only control the timing. Fiber is live on {s}. Interested?",
    "{n}, Patrick with AT&T Fiber. Fiber reached {s} in {c}. You're an existing customer so the upgrade is simple. Want details?",
    # short variants -- keep the copper angle when the address eats the budget
    "Hi {n} - Patrick with AT&T Fiber. Copper on {s} is retiring and fiber is live. Upgrade details?",
    "{n} - Patrick with AT&T Fiber. You're on copper at {a}. Fiber is live there now. Interested?",
    "Hi {n}, Patrick with AT&T Fiber. Copper is being retired on {s}. Fiber is ready. Want the upgrade?",
    "{n} - Patrick with AT&T Fiber. Fiber beat copper to {s}. You're due an upgrade. Want details?",
]


def _title(s):
    """Title-case a street without mangling ordinals: 8TH -> 8th, not 8Th."""
    out = []
    for w in str(s).split():
        t = w.title()
        if len(w) > 2 and w[0].isdigit() and w[-2:].lower() in ("th", "st", "nd", "rd"):
            t = w[:-2] + w[-2:].lower()
        out.append(t)
    return " ".join(out)


def pick(rows, seed=None):
    rnd = random.Random(seed)
    seen, out = set(), []
    for r in rows:
        name = (r.get("first_name") or "").strip().title() or "there"
        street = _title((r.get("street") or "").strip())
        addr = _title((r.get("address") or "").strip())
        city = (r.get("city") or "").strip().title()
        gold = (r.get("dot") or "").strip().upper().startswith("G") and \
               (r.get("dot") or "").strip().upper() != "GREEN"
        absentee = str(r.get("absentee") or "").strip() in ("1", "true", "yes", "Y")
        pool = GOLD if gold else (GREEN_ABSENTEE if absentee else GREEN)

        msg, order = None, list(range(len(pool)))
        rnd.shuffle(order)
        for i in order:
            cand = pool[i].format(n=name, s=street or city, a=addr, c=city)
            cand = " ".join(cand.split())
            if len(cand) <= MAX_BODY and cand.lower() not in seen:
                msg = cand
                break
        if msg is None:                      # too long or all shapes used
            base = ("Hi %s - Patrick with AT&T Fiber. Copper on %s is retiring, fiber is live. Details?"
                    % (name, street or city)) if gold else \
                   ("Hi %s - Patrick with AT&T Fiber. Fiber is live on %s. Want the details?"
                    % (name, street or city))
            short = base
            alts = ["%s - Patrick with AT&T Fiber. Fiber is now live on %s. Interested?" % (name, street or city),
                    "%s - Patrick with AT&T Fiber. %s has fiber now. Worth a look?" % (name, street or city),
                    "Hi %s, Patrick with AT&T Fiber. Fiber reached %s. Interested?" % (name, street or city)]
            for alt in alts:
                if short.lower() in seen and len(alt) <= MAX_BODY:
                    short = alt
            msg = short
        seen.add(msg.lower())
        r = dict(r)
        r["message"], r["chars"], r["segments_with_append"] = msg, len(msg), 1 if len(msg) + GHL_APPEND <= ONE_SEGMENT else 2
        out.append(r)
    return out


def audit(rows):
    """Refuse to hand over a batch that breaks a rule. Loud, not silent."""
    bad = []
    msgs = [r["message"] for r in rows]
    if len(set(m.lower() for m in msgs)) != len(msgs):
        bad.append("duplicate messages present")
    for r in rows:
        m = r["message"]
        if len(m) > MAX_BODY:
            bad.append("over %d chars: %s" % (MAX_BODY, m[:50]))
        # Match opt-out PHRASING, not the bare substring: "Christopher" contains
        # "stop", and a naive check silently blocks every Christopher forever.
        if re.search(r"\b(reply|text|send)\s+stop\b|\bstop\s+to\s+(opt|unsub)|"
                     r"\bunsubscribe\b|\bopt[\s-]?out\b", m, re.I):
            bad.append("contains opt-out language: %s" % m[:50])
        for brand in ("optimus", "frontline"):
            if brand in m.lower():
                bad.append("names the dealer brand: %s" % m[:50])
        if "$" in m:
            bad.append("price in first text: %s" % m[:50])
        for claim in ("address qualifies", "is covered", "you qualify for it"):
            if claim in m.lower():
                bad.append("unbacked per-address fiber claim: %s" % m[:50])
    return bad


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("infile"); ap.add_argument("outfile")
    ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.infile)))
    out = pick(rows, a.seed)
    problems = audit(out)
    if problems:
        print("REFUSING TO WRITE -- %d rule violations:" % len(problems))
        for p in problems[:10]:
            print("   " + p)
        sys.exit(1)
    w = csv.DictWriter(open(a.outfile, "w", newline=""), fieldnames=list(out[0].keys()))
    w.writeheader(); w.writerows(out)
    print("%d messages, all unique, all one segment -> %s" % (len(out), a.outfile))
