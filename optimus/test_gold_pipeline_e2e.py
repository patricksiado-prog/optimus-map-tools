"""
test_gold_pipeline_e2e.py -- end-to-end proof that GOLD dot capture works.

The other gold test exercises classify_status() in isolation. That is not the
same question as "does gold capture WORK". This one pushes REAL AT&T backend
records through the whole chain the hunter actually uses:

    backend JSON record
      -> lead_from_dict()      (extract + carry raw + compose full address)
      -> _lead_status()        (classify via backend_classifier, fallback below)
      -> dot_color()           (legend word written to the sheet)
      -> the row that lands on 'Precise Fiber'

It locks down the 2026-08-20 defect Patrick caught on the map: dots the sheet
called GOLD were GREY (existing fiber customers) when clicked. Two paths caused
it -- a "copper" word-match on the status text that ran BEFORE AT&T's own build
code, and "CUSTOMER" (undecodable build code) falling through into that same
word-match. Both are asserted here.

Run:  python test_gold_pipeline_e2e.py
"""
import sys

from precise_fiber_hunter import lead_from_dict, _lead_status, dot_color

fails = []


def check(name, got, want):
    if got == want:
        print("  PASS  %s" % name)
    else:
        print("  FAIL  %s -- got %r, wanted %r" % (name, got, want))
        fails.append(name)


def capture(rec):
    """Run one backend record through the real pipeline; return (color, lead)."""
    ld = lead_from_dict(rec)
    if ld is None:
        return None, None
    return dot_color(_lead_status(ld)), ld


def att(address, ban, build, status="", city="HOUSTON", state="TX", zipc="77051",
        lat="29.700000", lng="-95.400000"):
    """A record shaped exactly like the AT&T serviceability payload."""
    return {"zip": zipc, "address": address, "city": city, "state": state,
            "latitude": lat, "longitude": lng,
            "subscriber_ban": ban, "subscriber_ban_masked": ban,
            "curr_ntwrk_bld_type_cd": build, "status": status,
            "speed": "", "miles_from_claim": "0.10137", "missing_supl": 0}


print("\n=== 1. the three legend colors, straight off real build codes ===")
c, _ = capture(att("4202 REED RD", "", "unavailable", "FIBER ELIGIBLE"))
check("no BAN + 'unavailable' -> GREEN (the GREEN-0 case)", c, "GREEN")

c, _ = capture(att("4314 PHLOX ST", "*****033", "fttn-bp", "Existing Copper Customer"))
check("BAN + fttn-bp -> ORANGE (real gold)", c, "ORANGE")

c, _ = capture(att("4316 ALVIN ST", "*****033", "ip-rt", "Existing Copper Customer"))
check("BAN + ip-rt -> ORANGE (legacy copper terminal)", c, "ORANGE")

c, _ = capture(att("4320 MAGGIE ST", "*****033", "fttp-gpon", "Fiber customer"))
check("BAN + fttp-gpon -> GREY (already sold)", c, "GREY")


print("\n=== 2. THE REGRESSION Patrick caught: grey wearing gold's coat ===")
c, _ = capture(att("4321 BRINKLEY ST", "*****033", "fttp-gpon",
                   "Fiber customer - copper retirement complete"))
check("fiber build code + 'copper' in status text -> GREY", c, "GREY")

c, _ = capture(att("4322 LARKSPUR ST", "*****033", "ftth",
                   "Copper migration finished, now on fiber"))
check("ftth + 'copper' in status text -> GREY", c, "GREY")

c, _ = capture(att("4323 ALVIN ST", "*****033", "xgspon",
                   "Existing customer - copper migration"))
check("UNKNOWN build code + 'copper' in text -> GREY (safe default)", c, "GREY")

c, _ = capture(att("4325 LARKSPUR ST", "*****033", "", "copper"))
check("customer, NO build code, 'copper' text -> GREY (cannot confirm)", c, "GREY")


print("\n=== 3. gold must not be lost while we make grey safer ===")
for code in ("fttn-bp", "fttn", "ip-rt", "iprt", "copper", "ipbb", "adsl", "vdsl", "dsl"):
    c, _ = capture(att("100 TEST ST", "*****033", code, "Existing Copper Customer"))
    check("copper code %-8s still ORANGE" % code, c, "ORANGE")


print("\n=== 4. the address that reaches the sheet is complete ===")
_, ld = capture(att("4332 MAGGIE ST", "*****033", "fttn-bp"))
check("full address composed", ld["address"], "4332 MAGGIE ST, HOUSTON TX 77051")
check("street kept separately", ld["street"], "4332 MAGGIE ST")
check("city carried", ld["city"], "HOUSTON")
check("zip carried", ld["zip"], "77051")

_, ld = capture(att("5415 GURLEY AVE", "*****033", "fttn-bp",
                    city="DALLAS", zipc="75223"))
check("Dallas is distinguishable from Houston",
      ld["address"], "5415 GURLEY AVE, DALLAS TX 75223")

_, ld = capture(att("116 E ASH ST", "*****033", "fttn-bp", city="", state="", zipc=""))
check("degrades gracefully when AT&T omits city/state/zip",
      ld["address"], "116 E ASH ST")


print("\n=== 5. GeoJSON feature shape (the other payload AT&T returns) ===")
feat = {"type": "Feature",
        "geometry": {"type": "Point", "coordinates": [-95.4, 29.7]},
        "properties": att("4330 CLOVER ST", "*****033", "fttn-bp",
                          "Existing Copper Customer")}
c, ld = capture(feat)
check("GeoJSON copper customer -> ORANGE", c, "ORANGE")
check("GeoJSON address complete", ld["address"], "4330 CLOVER ST, HOUSTON TX 77051")


print("\n=== 6. the row actually written to 'Precise Fiber' ===")
rows = []
for rec in (att("1 GREEN ST", "", "unavailable", "FIBER ELIGIBLE"),
            att("2 GOLD ST", "*****033", "fttn-bp", "Existing Copper Customer"),
            att("3 GREY ST", "*****033", "fttp-gpon", "Fiber customer"),
            att("4 TRAP ST", "*****033", "fttp-gpon", "copper retirement complete")):
    color, ld = capture(rec)
    rows.append([ld["address"], color, "2026-08-19 23:38:40"])

check("green rows", sum(1 for r in rows if r[1] == "GREEN"), 1)
check("gold rows", sum(1 for r in rows if r[1] == "ORANGE"), 1)
check("grey rows (incl. the trap)", sum(1 for r in rows if r[1] == "GREY"), 2)
check("the trap row is NOT on the call list",
      [r[0] for r in rows if r[1] == "ORANGE"], ["2 GOLD ST, HOUSTON TX 77051"])

print("\n" + "=" * 62)
if fails:
    print("FAILED (%d): %s" % (len(fails), ", ".join(fails)))
    sys.exit(1)
print("ALL GOLD-PIPELINE E2E TESTS PASSED -- gold capture works end to end.")
