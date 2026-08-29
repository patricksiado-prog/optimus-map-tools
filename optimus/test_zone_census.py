"""
test_zone_census.py -- the freshness verdict must match what Patrick reads off
the map by eye.

Field rule (Patrick, from the map, 2026-08-18):
  "lots of grey = older area"
  "no grey, all gold + green = brand new"

Three real viewports from his own screenshots are encoded below. The census has
to reach the same verdict he does, or the ranking it produces is worthless.
"""
import sys
from optimus_dot_detect import zone_freshness

fails = []


def check(name, got, want):
    if got == want:
        print("  PASS  %s" % name)
    else:
        print("  FAIL  %s -- got %r, wanted %r" % (name, got, want))
        fails.append(name)


print("\n--- real viewports off the AT&T map ---")

# 1. Glencliffe / Birchglen / Dorrcrest / Coolshire (HP laptop screenshot).
#    Counted off the image: ~46 green, 3 gold, 3 grey. Patrick: brand new.
v, share = zone_freshness(green=46, gold=3, gray=3)
check("Prestonwood/Glencliffe -> FRESH", v, "FRESH")
check("  grey share under 12%", share < 0.12, True)

# 2. Prestonwood Forest Dr / Schaffer Ln (phone screenshot).
#    ~52 green, 9 gold, 5 grey. Patrick: new.
v2, share2 = zone_freshness(green=52, gold=9, gray=5)
check("Schaffer Ln -> FRESH", v2, "FRESH")

# 3. Southfield MI, Bonstelle Ave / Gateway Cir (phone screenshot).
#    ~24 green, 0 gold, 18 grey. Patrick: "lots of grey older area".
v3, share3 = zone_freshness(green=24, gold=0, gray=18)
check("Southfield Bonstelle -> MATURE", v3, "MATURE")
check("  grey share at/over 35%", share3 >= 0.35, True)

print("\n--- the boundaries hold ---")
check("all grey -> MATURE", zone_freshness(0, 0, 30)[0], "MATURE")
check("zero dots -> EMPTY", zone_freshness(0, 0, 0)[0], "EMPTY")
check("a few green, no grey, under the eligible floor -> WORKING",
      zone_freshness(3, 0, 0)[0], "WORKING")
check("gold counts toward the eligible floor, not just green",
      zone_freshness(4, 4, 0)[0], "FRESH")

print("\n--- gold is a freshness signal even though it is rare ---")
# 93 gold in 105,500 was the Vintage Park density. Gold alone is never a list,
# but its PRESENCE with no grey is the fingerprint of just-lit fiber.
fresh_with_gold, _ = zone_freshness(green=20, gold=6, gray=1)
mature_no_gold, _ = zone_freshness(green=20, gold=0, gray=20)
check("green+gold, no grey -> FRESH", fresh_with_gold, "FRESH")
check("green only, heavy grey -> MATURE", mature_no_gold, "MATURE")

print("\n--- census wiring ---")
sys.path.insert(0, ".")
from precise_fiber_hunter import CENSUS_TAB, CENSUS_HEADER
check("tab name", CENSUS_TAB, "Zone Census")
check("header carries grey% and verdict",
      ("Grey %" in CENSUS_HEADER) and ("Verdict" in CENSUS_HEADER), True)
check("header is 9 columns", len(CENSUS_HEADER), 9)

print("")
if fails:
    print("FAILED: %d" % len(fails)); sys.exit(1)
print("ALL ZONE-CENSUS TESTS PASSED")
