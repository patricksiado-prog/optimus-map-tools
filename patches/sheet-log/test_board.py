# Fake-gspread test for the follow-up board. Run from a clone of the hunter repo
# after applying sheet_log_block.py:  python3 test_board.py
# Needs pcola/plan.json from the 2026-09-03 session for the 141-row feed; if it
# is gone, replace `erows` with a few hand-written rows using the EH header.
import json, re, os, time
SRC = os.environ.get("SCRAPER", "optimus/standalone/maps_scraper_standalone.py")
src = open(SRC).read()

def grab(name):
    m = re.search(r"^(def %s\b.*?)(?=^\S)" % re.escape(name), src, re.S | re.M)
    assert m, name
    return m.group(1)

unit = re.search(r"^_UNIT = .*?\n(?=\S)", src, re.S | re.M)
suf  = re.search(r"^_SUF = .*?\n(?=\S)", src, re.S | re.M)
ns = {"json": json, "time": time, "re": re, "os": os}
code = "\n".join([
    'GH_REPO="x/y"', 'GH_BRANCH="b"', '_WRITE_STAMPS=[]', '_MACHINES=[1]',
    'GOLD_TAB="Gold Confirmed"', 'GREEN_BIZ_TAB="Fiber Green Biz"', 'ORANGE_BIZ_TAB="Upgrade Orange Biz"',
    '_MATCH={"leads":None}',
    'def _gh_token(): return None', 'def _sheet_throttle(max_per_min=50): pass',
    'PUTS={}', 'def gh_put(p,t): PUTS[p]=json.loads(t); return True',
    grab("_err_kind"), 'def _pf_spreadsheet(sh): return sh.split if sh.split else sh',
    suf.group(0),
    unit.group(0) if unit else "_UNIT = re.compile(r'\\b(APT|UNIT|STE|SUITE|#)\\s*\\S+')",
    grab("_norm_addr"),
    src[src.index("FEED_FOLDER_ID = "):src.index("def publish_tab_counts")],
])
exec(code, ns)
H = ns["ENRICHED_HEADER"]; E = ns["_E"]
print("header cols:", len(H), "| first 13:", H[:13] == ns["HUNTER_COLS"])

class WS:
    def __init__(s, title, rows=None, cols=26):
        s.title = title; s.rows = [list(r) for r in (rows or [])]; s.col_count = cols; s.id = 7; s.batch = []
    def get_all_values(s): return [list(r) for r in s.rows]
    def col_values(s, i): return [r[i-1] for r in s.rows if len(r) >= i]
    def row_values(s, i): return list(s.rows[i-1]) if len(s.rows) >= i else []
    def append_row(s, r, value_input_option=None): s.rows.append(list(r))
    def append_rows(s, rs, value_input_option=None):
        if getattr(s, "full", False): raise Exception("[400] would increase the number of cells above the limit of 10000000")
        s.rows.extend([list(r) for r in rs])
    def resize(s, cols=None): s.col_count = cols
    def update(s, rng, vals, value_input_option=None): s.rows[0] = list(vals[0])
    def batch_update(s, data, value_input_option=None):
        for d in data:
            m = re.match(r"([A-Z]+)(\d+):([A-Z]+)\d+", d["range"]); r = int(m.group(2)) - 1
            L = m.group(1); c0 = (26*(ord(L[0])-64)+ord(L[1])-65) if len(L) == 2 else ord(L)-65
            row = s.rows[r]; row += [""]*(c0+len(d["values"][0])-len(row)); row[c0:c0+len(d["values"][0])] = d["values"][0]; s.batch.append(d)
class Book:
    def __init__(s, client, full=False, split=None, title="book"):
        s.tabs = {}; s.full = full; s.split = split; s.fmt = []; s.client = client; s.title = title
    def worksheet(s, t):
        if t not in s.tabs: raise Exception("WorksheetNotFound")
        return s.tabs[t]
    @property
    def sheet1(s): return list(s.tabs.values())[0]
    def add_worksheet(s, title, rows, cols):
        if s.full: raise Exception("[400] would increase the number of cells above the limit of 10000000")
        s.tabs[title] = WS(title, cols=int(cols)); return s.tabs[title]
    def batch_update(s, body): s.fmt.append(body)
    def update_title(s, t): s.title = t
class Client:
    def __init__(s): s.files = {}
    def list_spreadsheet_files(s, title=None, folder_id=None):
        return [{"id": i, "name": b.title} for i, b in s.files.items()]
    def open_by_key(s, i): return s.files[i]
client = Client()

def feed(kind, header, rows, n):
    b = Book(client, title="OPTIMUS FEED %s %s" % (kind, n)); b.tabs["Sheet1"] = WS("Sheet1", [header] + rows); client.files[kind + str(n)] = b; return b

HC = ns["HUNTER_COLS"]
main = Book(client, full=True); split = Book(client); main.split = split; main.client = client
main.tabs["Gold Confirmed"] = WS("Gold Confirmed", [HC, ["5708 Zinnia Ave", "ORANGE", "2026-09-02 19:11", "", "", "run1", "PS", "30.65", "-87.05", "Milton", "FL", "32570", "Upgrade Customer - On Copper, Fiber Available"]])
GH = ["Address", "Captured At", "Lat", "Lng", "Build Code", "City", "State", "ZIP", "Run ID", "Operator", "Status"]
main.tabs["Grey Fiber Customers"] = WS("Grey Fiber Customers", [GH, ["6381 Rosebud Rd", "2026-09-02", "30.6", "-87.0", "fttp", "Milton", "FL", "32570", "run1", "PS", "Existing AT&T Customer"]])
BH = ["Business Name", "Phone", "Address", "Website", "Category", "Resi?", "Cell?"]
main.tabs["Fiber Green Biz"] = WS("Fiber Green Biz", [BH, ["Joe's Bait", "850-555-0100", "5504 Willard Norris Rd, Milton, FL", "", "bait", "", ""]])
main.tabs["Upgrade Orange Biz"] = WS("Upgrade Orange Biz", [BH]); main.tabs["Maps Businesses"] = WS("Maps Businesses", [BH])
ns["_MATCH"]["leads"] = {ns["_norm_addr"]("5656 Marigold Ave"): "GREEN"}

EH = ["address", "city", "state", "zip", "name", "cell", "phone_type", "enriched_at", "source", "pool", "ghl_contact_id", "likely_gold", "dnc", "colour"]
PLAN = os.environ.get("PLAN", "pcola/plan.json")
if os.path.exists(PLAN):
    plan = json.load(open(PLAN)); seen = set(); erows = []
    for e in plan:
        if not e.get("id") or e["id"] in seen: continue
        seen.add(e["id"])
        m = re.match(r"^(.*?),\s*([^,]+),\s*([A-Z]{2}),\s*(\d{5})\s*$", e["addr"]); st, city, stt, z = m.groups()
        erows.append([st, city, stt, z, "%s %s" % (e["first"], e["last"]), e["phone"], "landline" if "landline-call-only" in e["tags"] else "wireless",
                      "2026-09-03 00:45", "claude dealmachine->ghl", "pcola-fresh", e["id"], "YES" if e.get("attnet") else "", "YES" if "dnc-flagged" in e["tags"] else "", "unverified"])
else:
    erows = [[a, "Milton", "FL", "32570", "Person %d" % i, "+1850555%04d" % i, "wireless", "2026-09-03 00:45", "test", "pcola-fresh", "id%03d" % i, "", "YES", "unverified"]
             for i, a in enumerate(["5708 Zinnia Ave", "6381 Rosebud Rd", "5656 Marigold Ave", "5504 Willard Norris Rd", "1 Nowhere Ln"])]
N = len(erows)
feed("enriched", EH, erows, 1)
ids = [r[10] for r in erows]
feed("status", ["ghl_contact_id", "dialed", "last_call", "disposition", "dnd", "dead"],
     [[ids[0], "2", "2026-09-03", "CB", "", ""], [ids[1], "1", "2026-09-03", "NI", "", "YES"], ["NOPE", "9", "", "", "", ""]], 1)
feed("sales", ["sold_at", "address", "city", "state", "zip", "name", "cell", "product", "rep", "ghl_contact_id", "opportunity_id", "stage", "status"],
     [["2026-08-31", "1 Main St", "Houston", "TX", "77075", "M Majeed", "+17135550100", "Fiber 1 GIG", "Rep 3", "c1", "o1", "Won", "PAID"]], 1)
split.tabs["Sales Log"] = WS("Sales Log", [ns["SALES_HEADER"], ["2026-08-01", "9 Hand Typed Rd", "", "", "", "", "", "Fiber 300", "Rep 1", "", "typed by rep", "", "", "", "PAID", ""]])

# launch 1
ns["sync_sheet_log"](main)
el = split.tabs["Enriched Leads"]; sl = split.tabs["Sales Log"]
assert len(el.rows) - 1 == N and el.rows[0] == H, (len(el.rows), el.rows[0][:3])
byaddr = {r[0]: r for r in el.rows[1:]}
g = byaddr["5708 Zinnia Ave"]; print("gold row:", g[:3], g[E["Tab"]], g[E["Name"]], g[E["Cell"]])
assert g[1] == "ORANGE" and g[E["Tab"]] == "Gold Confirmed" and g[E["Name"]] and g[E["Cell"]].startswith("+1") and g[2] == "2026-09-02 19:11"
gr = byaddr["6381 Rosebud Rd"]; assert gr[1] == "GREY" and gr[E["Tab"]] == "Grey Fiber Customers" and gr[E["Status"]] == "Existing AT&T Customer", gr[:14]
gn = byaddr["5656 Marigold Ave"]; assert gn[1] == "GREEN" and gn[E["Tab"]] == "Precise Fiber", gn[:14]
bz = [r for r in el.rows[1:] if r[0].startswith("5504 Willard Norris Rd")][0]   # the hunter row's own address wins
assert bz[E["Business"]] == "Joe's Bait" and bz[E["Tab"]] == "Fiber Green Biz", bz[:14]
un = [r for r in el.rows[1:] if r[1] == "UNVERIFIED"]; print("unverified rows:", len(un), "| status text:", un[0][12])
assert un and un[0][E["City"]] == "Milton" and un[0][E["ZIP"]] == "32570"
s0 = byaddr[erows[0][0]]; print("status on", erows[0][0], "->", s0[E["Dialed"]:E["Status At"]+1])
assert s0[E["Disposition"]] == "CB" and byaddr[erows[1][0]][E["Dead"]] == "YES"
assert len(sl.rows) - 1 == 2 and sl.rows[1][1] == "9 Hand Typed Rd" and sl.rows[2][5] == "M Majeed"
landed_names = sorted(b.title for b in client.files.values()); print("feed files after launch 1:", landed_names)
assert all(t.startswith("LANDED ") for t in landed_names)
print("colour rules:", len(split.fmt), "|", split.fmt[0]["requests"][2]["addConditionalFormatRule"]["rule"]["booleanRule"]["condition"]["values"][0]["userEnteredValue"])
assert len(split.fmt) == 1
print("_landed:", ns["PUTS"]["optimus/_feed/_landed.json"])

# launch 2: nothing new
before = (len(el.rows), len(sl.rows), len(el.batch))
ns["sync_sheet_log"](main)
assert (len(el.rows), len(sl.rows), len(el.batch)) == before and ns["PUTS"]["optimus/_feed/_landed.json"].get("nothing_new")
print("launch 2: nothing new, nothing changed")

# launch 3: newer status overrides, re-sent people are not duplicated
feed("status", ["ghl_contact_id", "disposition"], [[ids[0], "PAID"]], 2)
feed("enriched", EH, erows[:3], 2)
ns["sync_sheet_log"](main)
assert len(el.rows) - 1 == N and byaddr[erows[0][0]][E["Disposition"]] == "PAID"
print("launch 3: re-sent people not duplicated, status overridden to PAID")

# full production, no split
lone = Book(client, full=True); lone.client = client
feed("enriched", EH, erows[:1], 3)
ns["sync_sheet_log"](lone)
assert "Enriched Leads" not in lone.tabs and any(b.title.startswith("OPTIMUS FEED enriched") for b in client.files.values())
print("full production: said out loud, feed left unlanded")

# foreign header on an existing tab is left alone
sp2 = Book(client); sp2.tabs["Enriched Leads"] = WS("Enriched Leads", [["Something", "Else"], ["x", "y"]])
m2 = Book(client, full=True, split=sp2); m2.client = client
ns["sync_sheet_log"](m2)
assert sp2.tabs["Enriched Leads"].rows == [["Something", "Else"], ["x", "y"]]
print("foreign header: tab untouched")
print("ALL TESTS PASS")
