# -*- coding: utf-8 -*-
"""Pure-logic test for the TX/NON-TX routing + LEGEND + seed/overlay merge.
Exec's the real helper source out of the scraper with stubs for Google."""
import re, sys
src = open("optimus/standalone/maps_scraper_standalone.py", encoding="utf-8").read()
def grab(name):
    m = re.search(r"^def %s\(.*?(?=^def |\Z)" % name, src, re.S | re.M)
    assert m, name; return m.group(0)
def grab_assign(name):
    m = re.search(r"^%s = .*?$" % name, src, re.M); assert m, name; return m.group(0)
ns = {}
# constants + tiny stubs the helpers touch
exec(grab_assign("TX_ZIP_PREFIXES"), ns)
exec(grab_assign("LEGEND_TAB"), ns)
ns["_s"] = lambda v: "" if v is None else str(v).strip()
ns["_sheet_throttle"] = lambda: None
HUNTER_COLS = ["Address","Dot Color","Captured At","Business","Phone","Run ID","Operator","Lat","Lng","City","State","ZIP","Status"]
GHL_HEADER = HUNTER_COLS + ["Tab","Enriched","Name","Cell","Email","GHL Contact ID","Disposition","DND","Last Updated","Synced At"]
ns["_G"] = {h: i for i, h in enumerate(GHL_HEADER)}
exec(grab("_route_state"), ns); exec(grab("_legend_rows"), ns)
_route_state, _legend_rows, _G = ns["_route_state"], ns["_legend_rows"], ns["_G"]

def row(state="", zip_="", addr="1 Main St", color="GOLD"):
    r = [""] * len(GHL_HEADER); r[0]=addr; r[1]=color; r[_G["State"]]=state; r[_G["ZIP"]]=zip_; return r

# 1. routing
assert _route_state(row("TX")) == "TX"
assert _route_state(row("texas")) == "TX"
assert _route_state(row("FL", "34952")) == "NON-TX"
assert _route_state(row("", "77515")) == "TX"          # blank state, Houston ZIP
assert _route_state(row("", "73301")) == "TX"          # Austin 733xx
assert _route_state(row("", "34952")) == "NON-TX"
assert _route_state(row("", "")) == "NON-TX"           # unknown -> NON-TX, visible
print("routing OK")

# 2. seed + overlay merge, mirrored from sync_ghl_status
GOLD_TAB, GREEN_BIZ_TAB, ORANGE_BIZ_TAB = "Gold Confirmed", "Fiber Green Biz", "Upgrade Orange Biz"
GHL_TABS = ("Green","Gold","Grey","Biz","Fiber Biz")
ROUTE = {"Precise Fiber": ("Green",), GOLD_TAB: ("Gold",), ORANGE_BIZ_TAB: ("Gold","Fiber Biz"),
         "Grey Fiber Customers": ("Grey",), "Maps Businesses": ("Biz",), GREEN_BIZ_TAB: ("Fiber Biz",)}
stamp = "2026-09-05 16:40:00"
def hrow(addr, state, zip_): 
    r = [""]*len(HUNTER_COLS); r[0]=addr; r[1]="GOLD"; r[9]="X"; r[10]=state; r[11]=zip_; return r
known = {"321 e cedar st apt 2|77515": (GOLD_TAB, hrow("321 E CEDAR ST APT 2","TX","77515")),
         "2349 se hallahan st|34952": (GOLD_TAB, hrow("2349 SE HALLAHAN ST","FL","34952")),
         "11650 jones rd|77070":      (GREEN_BIZ_TAB, hrow("11650 Jones Rd","TX","77070")),
         "5673 zinnia ave|32570":     ("Precise Fiber", hrow("5673 Zinnia Ave","FL","32570"))}  # green: NOT seeded
per = {t: {} for t in GHL_TABS}; blank = ["NO","","","","","","","",stamp]; seeded = 0
for k,(tab,h) in known.items():
    if tab not in (GOLD_TAB, ORANGE_BIZ_TAB, GREEN_BIZ_TAB): continue
    r = list(h)+[tab]+list(blank)
    for t in ROUTE[tab]: per[t]["A:"+k]=r; seeded+=1
assert seeded == 3 and len(per["Gold"]) == 2 and len(per["Fiber Biz"]) == 1 and len(per["Green"]) == 0
# overlay: Sandefur enriched at the FL gold address; Jacobs green in FL with no seed
def ghlrow(addr, state, zip_, name, cell, tabs):
    r = [""]*len(GHL_HEADER); r[0]=addr; r[1]="GOLD" if "Gold" in tabs else "GREEN"
    r[_G["State"]]=state; r[_G["ZIP"]]=zip_; r[_G["Enriched"]]="YES"; r[_G["Name"]]=name; r[_G["Cell"]]=cell
    r[_G["Disposition"]]="SOLD" if name.startswith("Joseph") else ""; r[_G["Synced At"]]=stamp; return tabs, r
contacts = [("g1","2349 se hallahan st|34952", ghlrow("2349 SE HALLAHAN ST","FL","34952","Joseph S","+12672433439",("Gold",))),
            ("g2","5673 zinnia ave|32570",    ghlrow("5673 Zinnia Ave","FL","32570","Daniel J","+19257658999",("Green",)))]
for gid,k,(tabs,r) in contacts:
    for t in tabs:
        d = per[t]
        if k and ("A:"+k) in d: d["A:"+k] = r
        else: d["G:"+gid] = r
assert len(per["Gold"]) == 2, "seed replaced, not duplicated"
assert per["Gold"]["A:2349 se hallahan st|34952"][_G["Enriched"]] == "YES"
assert per["Gold"]["A:321 e cedar st apt 2|77515"][_G["Enriched"]] == "NO"
assert len(per["Green"]) == 1
# 3. route per book
tx  = {t: [r for r in per[t].values() if _route_state(r)=="TX"] for t in GHL_TABS}
ntx = {t: [r for r in per[t].values() if _route_state(r)=="NON-TX"] for t in GHL_TABS}
assert len(tx["Gold"]) == 1 and len(ntx["Gold"]) == 1
assert len(tx["Fiber Biz"]) == 1 and len(ntx["Fiber Biz"]) == 0
assert len(tx["Green"]) == 0 and len(ntx["Green"]) == 1
assert ntx["Gold"][0][_G["Disposition"]] == "SOLD"      # the colour-coded sale lands in NON-TX
print("seed/overlay/route OK: TX gold=%d fiberbiz=%d | NON-TX gold=%d green=%d" % (
      len(tx["Gold"]), len(tx["Fiber Biz"]), len(ntx["Gold"]), len(ntx["Green"])))

# 4. legend: human-readable, both states, no commission figures
for st in ("TX","NON-TX"):
    L = _legend_rows(st, stamp); text = " ".join(a+" "+b for a,b in L)
    for must in ("BLUE","RED","GREEN","GREY","Enriched","NEVER re-enrich","Grey never ships","Dot Color","UNVERIFIED", st):
        assert must in text, must
    assert "$140" not in text and "$500" not in text, "commission figure in LEGEND"
    assert all(len(r)==2 for r in L)
print("legend OK (%d rows)" % len(L))
print("ALL PASS")
