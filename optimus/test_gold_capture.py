"""
test_gold_capture.py -- proves GOLD (copper-upgrade) dots survive the pipeline.

The bug this locks down: the legacy fallback classifier could only spot copper
from the literal word "copper" in popup text. The AT&T backend JSON never
contains that word -- it carries curr_ntwrk_bld_type_cd = "FTTN-BP" / "IP-RT".
So whenever backend_classifier.py was missing, every copper customer classified
as CUSTOMER, got treated as grey, and was silently dropped. Gold went to zero.

Run:  python test_gold_capture.py
"""
import sys

from optimus_dot_detect import (classify_status, STATUS_LEAD, STATUS_CUSTOMER,
                                STATUS_COPPER_UPGRADE)

fails = []


def check(name, got, want):
    if got == want:
        print("  PASS  %s" % name)
    else:
        print("  FAIL  %s -- got %r, wanted %r" % (name, got, want))
        fails.append(name)


print("\n--- legacy fallback: build code must decide copper vs fiber ---")
# real values straight out of the 105,500-record Vintage Park capture
check("FTTN-BP customer -> GOLD",
      classify_status(ban="BmrSnr!x", build="FTTN-BP"), STATUS_COPPER_UPGRADE)
check("IP-RT customer -> GOLD",
      classify_status(ban="BmrSnr!x", build="IP-RT"), STATUS_COPPER_UPGRADE)
check("FTTN customer -> GOLD",
      classify_status(ban="BmrSnr!x", build="FTTN"), STATUS_COPPER_UPGRADE)
check("IP-CO customer -> GOLD",
      classify_status(ban="BmrSnr!x", build="IP-CO"), STATUS_COPPER_UPGRADE)
check("FTTP-GPON customer -> GREY (already on fiber)",
      classify_status(ban="BmrSnr!x", build="FTTP-GPON"), STATUS_CUSTOMER)
check("lowercase fttn-bp still GOLD",
      classify_status(ban="x", build="fttn-bp"), STATUS_COPPER_UPGRADE)

print("\n--- green must be untouched by the change ---")
check("no ban, unavailable -> GREEN",
      classify_status(ban="", build="unavailable"), STATUS_LEAD)
check("no ban, no build -> GREEN",
      classify_status(ban=None, build=None), STATUS_LEAD)
check("no ban wins over a copper build code",
      classify_status(ban="", build="FTTN-BP"), STATUS_LEAD)

print("\n--- regression: the old behaviour that lost gold ---")
# before the fix this returned STATUS_CUSTOMER (-> dropped as grey)
old_style = classify_status(text="Subscriber", ban="x")
check("no build code at all -> still CUSTOMER (unchanged)",
      old_style, STATUS_CUSTOMER)

print("\n--- the sheet word for a gold dot ---")
sys.path.insert(0, ".")
from precise_fiber_hunter import DOT_COLOR, dot_color, GOLD_TAB, GOLD_HEADER
check("copper_upgrade writes as ORANGE", dot_color(STATUS_COPPER_UPGRADE), "ORANGE")
check("lead writes as GREEN", dot_color(STATUS_LEAD), "GREEN")
check("customer writes as GREY", dot_color(STATUS_CUSTOMER), "GREY")

print("\n--- gold cluster alert matches the word actually written ---")
gold_word = DOT_COLOR.get("copper_upgrade", "ORANGE")
rows = [["1 A ST", dot_color(STATUS_COPPER_UPGRADE), "t", "", ""],
        ["2 B ST", dot_color(STATUS_LEAD), "t", "", ""],
        ["3 C ST", dot_color(STATUS_COPPER_UPGRADE), "t", "", ""]]
check("alert finds 2 gold rows (was 0 before the fix)",
      len([r for r in rows if r[1] == gold_word]), 2)
check("comparing to the literal 'GOLD' still finds none (the old bug)",
      len([r for r in rows if r[1] == "GOLD"]), 0)

print("\n--- dedicated gold tab is configured ---")
check("tab name set", GOLD_TAB, "Gold Upgrade Leads")
check("header has 6 cols incl Area", len(GOLD_HEADER), 6)

print("")
if fails:
    print("FAILED: %d" % len(fails))
    sys.exit(1)
print("ALL GOLD-CAPTURE TESTS PASSED")
