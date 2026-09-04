"""Proves gold+grey now dedupe, using the REAL _dd_dedupe_tab against a fake
workbook. Mirrors the actual tab shapes and the real duplication we measured."""
import sys, types, importlib.util, io, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
src = io.open('maps_scraper_standalone.py', encoding='utf-8').read()
ns = {}
# execute only the dedupe block (no selenium / gspread imports)
start = src.index('# PERIODIC BACKGROUND DEDUPE')
end   = src.index('def start_periodic_dedupe')
# the GHL STATUS block (2026-09-04) sits between the dedupe code and
# start_periodic_dedupe and needs the whole module; stop before it.
if '# GHL STATUS (2026-09-04)' in src[start:end]:
    end = src.index('# GHL STATUS (2026-09-04)')
ns["HERE"] = "/tmp/fix"
exec("import os, csv, time, socket, json\n" + src[start:end], ns)

class WS:
    _n = [0]
    def __init__(s, title, vals):
        WS._n[0] += 1
        s.title, s._v, s.id = title, [r[:] for r in vals], WS._n[0]
    def get_all_values(s): return [r[:] for r in s._v]
    def batch_update(s, reqs, value_input_option=None):
        body = reqs[0]["values"]
        for i, row in enumerate(body):
            while len(s._v) < i + 2: s._v.append([])
            s._v[i + 1] = row[:]
    @property
    def spreadsheet(s): return s
    def batch_update_ss(s, req): pass
class SS:
    def __init__(s, tabs): s.t = {k: WS(k, v) for k, v in tabs.items()}
    def worksheet(s, n):
        if n not in s.t: raise Exception("no tab " + n)
        return s.t[n]
    def add_worksheet(s, title, rows, cols):
        s.t[title] = WS(title, [["", ""]]); return s.t[title]
    def batch_update(s, req):
        rg = req["requests"][0]["deleteDimension"]["range"]
        for w in s.t.values():
            if w.id == rg["sheetId"]:
                del w._v[rg["startIndex"]:rg["endIndex"]]
for w in ("WS",): pass
WS.spreadsheet = property(lambda s: types.SimpleNamespace(batch_update=s._ss.batch_update))

GOLD_H = ["Address","Captured At","Lat","Lng","Business","Phone","Run ID",
          "Operator","City","State","ZIP","Tier","Build Code","Status"]
GREY_H = ["Address","Captured At","Lat","Lng","Build Code","City","State","ZIP",
          "Run ID","Operator"]
def gold(addr, n, full=True):
    return [[addr,"2026-08-26","29.6","-95.3","","", "r1","PS",
             "HOUSTON" if full else "","TX" if full else "","77075" if full else "",
             "VERIFIED_GOLD","",""] for _ in range(n)]

gold_rows = gold("7631 FUQUA ST, HOUSTON TX 77075", 96) \
          + gold("800 N ARCOLA ST, ANGLETON TX 77515", 50) \
          + gold("611 E MYRTLE ST, ANGLETON TX 77515", 22) \
          + gold("1112 N ARCOLA ST, ANGLETON TX 77515", 2) \
          + gold("101 SOMMERMEYER ST, HOUSTON TX 77080", 1)
# one skinny duplicate that must LOSE to its fuller twin
gold_rows.append(["7631 FUQUA ST, HOUSTON TX 77075"] + [""]*13)
grey_rows = [["555 BELVEDERE DR, BEAUMONT TX 77706","2026-08-26","30.1","-94.1",
              "fttp-gpon","BEAUMONT","TX","77706","r1","PS"] for _ in range(40)] \
          + [["1495 BELVEDERE DR, BEAUMONT TX 77706","2026-08-26","30.1","-94.1",
              "fttp-gpon","BEAUMONT","TX","77706","r1","PS"]]

sh = SS({"Gold Confirmed": [GOLD_H] + gold_rows,
         "Grey Fiber Customers": [GREY_H] + grey_rows})
for w in sh.t.values(): w._ss = sh

_, _, pf_key, pf_score, _ = ns["_dd_keys"]()
ns["_dd_backup_csv"] = lambda tab, vals: None      # no disk writes in the test

fails = []
for tab, exp_unique in (("Gold Confirmed", 5), ("Grey Fiber Customers", 2)):
    before = len(sh.worksheet(tab).get_all_values()) - 1
    removed = ns["_dd_dedupe_tab"](sh, tab, pf_key, pf_score)
    after = sh.worksheet(tab).get_all_values()
    body = after[1:]
    uniq = sorted(set(r[0] for r in body))
    print("%-22s %5d rows -> %d unique (removed %d)" % (tab, before, len(body), removed))
    if len(body) != exp_unique: fails.append("%s kept %d, expected %d" % (tab, len(body), exp_unique))
    if len(uniq) != len(body):  fails.append("%s still has duplicate addresses" % tab)
    if after[0] != ([GOLD_H, GREY_H][tab.startswith("Grey")]): fails.append("%s header changed" % tab)

# the skinny 7631 row must have lost to the full one
g = sh.worksheet("Gold Confirmed").get_all_values()[1:]
fuqua = [r for r in g if r[0].startswith("7631 FUQUA")][0]
if fuqua[8] != "HOUSTON": fails.append("kept the SKINNY 7631 row, not the full one")
else: print("kept the FULLEST 7631 Fuqua row (City=HOUSTON), not the skinny twin")

# second pass must be a no-op
if ns["_dd_dedupe_tab"](sh, "Gold Confirmed", pf_key, pf_score) != 0:
    fails.append("second pass removed rows -- not idempotent")
else: print("second pass removed 0 rows -- idempotent")

# a tab that does not exist must not crash
if ns["_dd_dedupe_tab"](sh, "Nope", pf_key, pf_score) != 0: fails.append("missing tab not handled")
else: print("missing tab returns 0, no crash")

print()
print("*** FAILED: " + "; ".join(fails) if fails else "ALL TESTS PASS")
sys.exit(1 if fails else 0)
