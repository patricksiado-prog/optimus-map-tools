# Fake-gspread, fake-GHL test for sync_ghl_status. Exec's only the SHEET LOG /
# GHL STATUS block of the scraper with a fake workbook and no network:
#   python3 test_ghl_sync.py            (SCRAPER=path overrides the source file)
import json, re, os, sys, time, types, io, tempfile, urllib.request, urllib.error
SRC = os.environ.get("SCRAPER", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                             "maps_scraper_standalone.py"))
src = open(SRC, encoding="utf-8").read()


def grab(name):
    m = re.search(r"^(def %s\b.*?)(?=^\S)" % re.escape(name), src, re.S | re.M)
    assert m, name
    return m.group(1)


unit = re.search(r"^_UNIT = .*?\n(?=\S)", src, re.S | re.M)
suf = re.search(r"^_SUF = .*?\n(?=\S)", src, re.S | re.M)
TMP = tempfile.mkdtemp()
FAKE_FILE = os.path.join(TMP, "maps_scraper_standalone.py")
SLEPT = []
fake_time = types.SimpleNamespace(time=time.time, strftime=time.strftime,
                                  sleep=lambda s: SLEPT.append(s))
ns = {"json": json, "time": fake_time, "re": re, "os": os, "io": io, "__file__": FAKE_FILE}
code = "\n".join([
    'GH_REPO="x/y"', 'GH_BRANCH="b"', '_WRITE_STAMPS=[]', '_MACHINES=[1]',
    'GOLD_TAB="Gold Confirmed"', 'GREEN_BIZ_TAB="Fiber Green Biz"', 'ORANGE_BIZ_TAB="Upgrade Orange Biz"',
    '_MATCH={"leads":None}',
    'THROTTLED=[0]', 'def _sheet_throttle(max_per_min=50): THROTTLED[0]+=1',
    'PUTS={}', 'def gh_put(p,t): PUTS[p]=json.loads(t); return True',
    grab("_err_kind"), 'def _pf_spreadsheet(sh): return sh.split if sh.split else sh',
    'def _gc(sh): raise AssertionError("_gc must not be needed by the GHL block")',
    suf.group(0), unit.group(0),
    grab("_norm_addr"),
    src[src.index("FEED_FOLDER_ID = "):src.index("def publish_tab_counts")],
])
exec(code, ns)
os.environ.pop("GHL_PIT_TOKEN", None)
H = ns["GHL_HEADER"]; G = ns["_G"]; HC = ns["HUNTER_COLS"]
assert H[:13] == HC and H[13:] == ["Tab", "Enriched", "Name", "Cell", "Email", "GHL Contact ID",
                                   "Disposition", "DND", "Last Updated", "Synced At"]
assert ns["GHL_TABS"] == ("Green", "Gold", "Grey", "Biz", "Fiber Biz")
pats = [p for p, _ in ns["STATUS_COLOURS"]]
assert pats.index("NO FIBER") < pats.index("^NO$|^NI$|NOT INTERESTED|DEAD|DNC"), pats
# the colour rules: first matching rule wins in Sheets, so prove no earlier rule grabs NO FIBER
for word, want in (("NO FIBER", "NO FIBER"), ("SOLD", "PAID|SOLD|INSTALLED"),
                   ("NI", "^NO$|^NI$|NOT INTERESTED|DEAD|DNC"), ("DNC", "^NO$|^NI$|NOT INTERESTED|DEAD|DNC"),
                   ("CB", "^CB|CALL ?BACK|MAYBE")):
    first = next(p for p, _ in ns["STATUS_COLOURS"] if re.search(p, word))
    assert first == want, (word, first)
print("header cols:", len(H), "| tabs:", ns["GHL_TABS"], "| NO FIBER rule sits before red")


# ---- fake gspread ---------------------------------------------------------
def _c0(L):
    n = 0
    for ch in L:
        n = n * 26 + ord(ch) - 64
    return n - 1


class WS:
    def __init__(s, title, rows=None, cols=26):
        s.title = title; s.rows = [list(r) for r in (rows or [])]; s.col_count = cols
        s.row_count = 1000; s.id = 7; s.updates = 0; s.cleared = 0; s.full = False
    def get_all_values(s): return [list(r) for r in s.rows]
    def col_values(s, i): return [r[i-1] for r in s.rows if len(r) >= i]
    def row_values(s, i): return list(s.rows[i-1]) if len(s.rows) >= i else []
    def append_row(s, r, value_input_option=None): s.rows.append(list(r))
    def resize(s, rows=None, cols=None):
        if rows: s.row_count = rows
        if cols: s.col_count = cols
    def clear(s): s.rows = []; s.cleared += 1
    def update(s, rng, vals, value_input_option=None):
        if s.full: raise Exception("[400] would increase the number of cells above the limit of 10000000")
        m = re.match(r"([A-Z]+)(\d+)(?::([A-Z]+)(\d+))?$", rng); assert m, rng
        r0, c0 = int(m.group(2)) - 1, _c0(m.group(1))
        if m.group(4):
            assert int(m.group(4)) - r0 == len(vals), (rng, len(vals))
        assert r0 + len(vals) <= s.row_count, ("grid too small", rng, s.row_count)
        assert c0 + max(len(v) for v in vals) <= s.col_count, ("grid too narrow", s.col_count)
        while len(s.rows) < r0 + len(vals): s.rows.append([])
        for i, v in enumerate(vals):
            row = s.rows[r0 + i]; row += [""] * (c0 + len(v) - len(row)); row[c0:c0 + len(v)] = list(v)
        s.updates += 1


class Book:
    def __init__(s, full=False, split=None, title="book"):
        s.tabs = {}; s.full = full; s.split = split; s.fmt = []; s.title = title
    def worksheet(s, t):
        if t not in s.tabs: raise Exception("WorksheetNotFound")
        return s.tabs[t]
    def add_worksheet(s, title, rows, cols):
        if s.full: raise Exception("[400] would increase the number of cells above the limit of 10000000")
        s.tabs[title] = WS(title, cols=int(cols)); s.tabs[title].row_count = int(rows); return s.tabs[title]
    def batch_update(s, body): s.fmt.append(body)


def hunter_books():
    main = Book(full=True); split = Book(); main.split = split
    main.tabs["Gold Confirmed"] = WS("Gold Confirmed", [HC,
        ["5708 Zinnia Ave", "ORANGE", "2026-09-02 19:11", "", "", "run1", "PS", "30.65", "-87.05", "Milton", "FL", "32570", "Upgrade Customer - On Copper, Fiber Available"],
        ["12 Copper Ln", "ORANGE", "2026-09-02 19:12", "", "", "run1", "PS", "30.66", "-87.06", "Milton", "FL", "32570", "Upgrade Customer - On Copper, Fiber Available"],
        ["34 Copper Ln", "ORANGE", "2026-09-02 19:13", "", "", "run1", "PS", "30.67", "-87.07", "Milton", "FL", "32570", "Upgrade Customer - On Copper, Fiber Available"],
        ["34 COPPER LANE", "ORANGE", "2026-09-02 19:14", "", "", "run1", "PS", "30.67", "-87.07", "Milton", "FL", "32570", "duplicate sighting of the row above"]])
    GH = ["Address", "Captured At", "Lat", "Lng", "Build Code", "City", "State", "ZIP", "Run ID", "Operator", "Status"]
    main.tabs["Grey Fiber Customers"] = WS("Grey Fiber Customers", [GH, ["6381 Rosebud Rd", "2026-09-02", "30.6", "-87.0", "fttp", "Milton", "FL", "32570", "run1", "PS", "Existing AT&T Customer"]])
    BH = ["Business Name", "Phone", "Address", "Website", "Category", "Resi?", "Cell?"]
    main.tabs["Fiber Green Biz"] = WS("Fiber Green Biz", [BH, ["Joe's Bait", "850-555-0100", "5504 Willard Norris Rd, Milton, FL", "", "bait", "", ""]])
    main.tabs["Upgrade Orange Biz"] = WS("Upgrade Orange Biz", [BH, ["Copper Cafe", "850-555-0200", "77 Copper Blvd, Milton, FL", "", "cafe", "", ""]])
    main.tabs["Maps Businesses"] = WS("Maps Businesses", [BH, ["Plain Shop", "850-555-0300", "9 Market St, Milton, FL", "", "shop", "", ""]])
    ns["_MATCH"]["leads"] = {ns["_norm_addr"]("5656 Marigold Ave"): "GREEN"}
    return main, split


# ---- fake GHL --------------------------------------------------------------
def contact(i, addr, tags, phone="+1850555%04d", **kw):
    c = {"id": "c%d" % i, "firstName": "Person", "lastName": str(i), "email": "p%d@x.com" % i,
         "address1": addr, "city": "Milton", "state": "FL", "postalCode": "32570",
         "tags": tags, "dateUpdated": "2026-09-04T10:00:00.000Z", "dnd": False}
    if phone:
        c["phone"] = phone % i if "%" in phone else phone
    c.update(kw)
    return c


PAGE1 = [contact(1, "5708 Zinnia Ave", ["alpha-t2-gold", "SOLD"]),
         contact(2, "6381 Rosebud Rd", ["service not available"], phone=None),
         contact(3, "1 Nowhere Ln", ["alpha-t5-green"])]
PAGE2 = [contact(4, "77 Copper Blvd", ["callback"], dnd=True),
         contact(5, "5656 Marigold Ave", ["not interested"],
                 dndSettings={"SMS": {"status": "permanent", "message": "STOP_KEYWORD"}})]
CALLS = []


class Resp:
    def __init__(s, body): s.body = json.dumps(body).encode("utf-8")
    def read(s): return s.body
    def __enter__(s): return s
    def __exit__(s, *a): return False


def fake_urlopen_factory(pages, fail_once_429=False):
    state = {"429": fail_once_429}
    def fake_urlopen(req, timeout=None):
        CALLS.append(req)
        assert req.get_header("Authorization") == "Bearer TESTTOKEN", req.header_items()
        assert req.get_header("Version") == "2021-07-28"
        url = req.full_url
        assert url.startswith("https://services.leadconnectorhq.com/contacts/?"), url
        assert "locationId=xZj500PjsflIQg2j9f9D" in url and "limit=100" in url
        m = re.search(r"startAfterId=([^&]+)", url)
        if not m:
            return Resp({"contacts": pages[0], "meta": {"startAfterId": "c3", "startAfter": 1700000000000, "total": 5}})
        assert m.group(1) == "c3" and "startAfter=1700000000000" in url, url
        if state["429"]:
            state["429"] = False
            raise urllib.error.HTTPError(url, 429, "Too Many Requests", {}, None)
        return Resp({"contacts": pages[1], "meta": {"total": 5}})
    return fake_urlopen


class Capture:
    def __enter__(s):
        s.buf = io.StringIO(); s.old = sys.stdout; sys.stdout = s.buf; return s
    def __exit__(s, *a):
        sys.stdout = s.old; s.text = s.buf.getvalue(); print(s.text, end="")
        return False


def by_id(ws):
    return {r[G["GHL Contact ID"]]: r for r in ws.rows[1:]}


# ==== 1. no token: one line, nothing written, no network =====================
main, split = hunter_books()
urllib.request.urlopen = fake_urlopen_factory([PAGE1, PAGE2])
with Capture() as cap:
    ns["sync_ghl_status"](main)
lines = [l for l in cap.text.splitlines() if l.strip()]
assert len(lines) == 1 and lines[0].startswith("  GHL STATUS: no ghl_token.txt next to the scraper") and "GHL_PIT_TOKEN" not in lines[0], lines
assert not split.tabs and not main.tabs.keys() - {"Gold Confirmed", "Grey Fiber Customers", "Fiber Green Biz", "Upgrade Orange Biz", "Maps Businesses"}
assert CALLS == [] and "optimus/_feed/_ghl_status.json" not in ns["PUTS"] and "optimus/_feed/gold_unenriched.json" not in ns["PUTS"]
print("1. no token: one line, nothing written, no network call")

# ==== 2. token in ghl_token.txt next to the script: five tabs in the SPLIT only ====
open(os.path.join(TMP, "ghl_token.txt"), "w").write("  TESTTOKEN\n")
urllib.request.urlopen = fake_urlopen_factory([PAGE1, PAGE2], fail_once_429=True)
with Capture() as cap:
    ns["sync_ghl_status"](main)
assert "TESTTOKEN" not in cap.text
assert len(CALLS) == 3 and SLEPT == [10], (len(CALLS), SLEPT)      # page1, 429, page2
assert sorted(split.tabs) == sorted(["Green", "Gold", "Grey", "Biz", "Fiber Biz"]), sorted(split.tabs)
assert set(main.tabs) == {"Gold Confirmed", "Grey Fiber Customers", "Fiber Green Biz", "Upgrade Orange Biz", "Maps Businesses"}
for t in ns["GHL_TABS"]:
    assert split.tabs[t].rows[0] == H, t
gold = by_id(split.tabs["Gold"])
g1 = gold["c1"]
assert g1[1] == "ORANGE" and g1[G["Tab"]] == "Gold Confirmed" and g1[G["Enriched"]] == "YES" \
    and g1[G["Disposition"]] == "SOLD" and g1[2] == "2026-09-02 19:11" and g1[G["Name"]] == "Person 1" \
    and g1[G["Cell"]] == "+18505550001" and g1[G["Email"]] == "p1@x.com" and g1[G["Synced At"]], g1
grey = by_id(split.tabs["Grey"])
g2 = grey["c2"]
assert g2[1] == "GREY" and g2[G["Enriched"]] == "NO" and g2[G["Cell"]] == "" \
    and g2[G["Disposition"]] == "NO FIBER" and g2[12] == "Existing AT&T Customer", g2
green = by_id(split.tabs["Green"])
g3 = green["c3"]
assert g3[1] == "UNVERIFIED" and g3[12] == "Not on the hunter map yet - colour unverified" \
    and g3[G["Tab"]] == "" and g3[0] == "1 Nowhere Ln" and g3[G["City"]] == "Milton" and g3[G["ZIP"]] == "32570", g3
g5 = green["c5"]
assert g5[1] == "GREEN" and g5[G["Tab"]] == "Precise Fiber" and g5[G["Disposition"]] == "NI" \
    and g5[G["DND"]] == "SMS STOP" and g5[12] == "Non-AT&T Customer - Can Get Fiber", g5
assert "c4" in gold and "c4" in by_id(split.tabs["Fiber Biz"]), "Upgrade Orange Biz row goes to Gold AND Fiber Biz"
g4 = gold["c4"]
assert g4[1] == "ORANGE" and g4[G["Tab"]] == "Upgrade Orange Biz" and g4[G["Business"]] == "Copper Cafe" \
    and g4[G["Disposition"]] == "CB" and g4[G["DND"]] == "SMS STOP", g4
assert len(split.tabs["Biz"].rows) == 1                     # header only: nobody on Maps Businesses
counts = {t: len(split.tabs[t].rows) - 1 for t in ns["GHL_TABS"]}
assert counts == {"Green": 2, "Gold": 2, "Grey": 1, "Biz": 0, "Fiber Biz": 1}, counts
assert len(split.fmt) == 5 and all(len(b["requests"]) == len(ns["STATUS_COLOURS"]) for b in split.fmt)
rep = ns["PUTS"]["optimus/_feed/_ghl_status.json"]
assert rep["contacts_read"] == 5 and rep["people"] == 5 and rep["pull_complete"] is True and rep["not_placed"] == 0
assert rep["tabs"]["Gold"] == {"people": 2, "enriched": 2, "sold": 1, "cb": 1, "ni": 0, "dnc": 0,
                               "no_fiber": 0, "sms_stop": 1, "unverified": 0, "written": True}, rep["tabs"]["Gold"]
assert "Person" not in json.dumps(rep) and "+1850" not in json.dumps(rep)     # no PII in the feed
assert "  GHL STATUS: 'Gold': 2 people (2 enriched, 1 sold, 1 CB, 0 NI, 0 no fiber)" in cap.text
assert "(PARTIAL)" not in cap.text
# the gold enrichment backlog: 3 unique gold dots on the map (4 rows), 1 of them in GHL
gu = ns["PUTS"]["optimus/_feed/gold_unenriched.json"]
assert gu["generated_at"] and gu["gold_dots_total"] == 3 and gu["in_ghl"] == 1 and gu["not_in_ghl"] == 2 \
    and "capped" not in gu, gu
assert sorted(a["address"] for a in gu["addresses"]) == ["12 Copper Ln", "34 Copper Ln"], gu["addresses"]
assert gu["addresses"][0] == {"address": "12 Copper Ln", "city": "Milton", "state": "FL", "zip": "32570",
                              "lat": "30.66", "lng": "-87.06", "captured_at": "2026-09-02 19:12"}, gu["addresses"][0]
gu_text = json.dumps(gu)
for c in PAGE1 + PAGE2:
    for k in ("firstName", "email", "phone", "id"):
        if c.get(k):
            assert c[k] not in gu_text, (k, c[k])
    assert "Person %s" % c["lastName"] not in gu_text
assert "5708 Zinnia" not in gu_text                                   # the one in GHL is not listed
assert rep["gold"] == {"gold_dots_total": 3, "in_ghl": 1, "not_in_ghl": 2} and "addresses" not in rep, rep
assert "  GHL STATUS: gold dots on the map: 3 unique, 1 in GHL (enriched), 2 not yet enriched -> _feed/gold_unenriched.json" in cap.text
print("2. five tabs in the split only; gold/grey/green/unverified/dual routing, SOLD/NO FIBER/CB/NI, DND, Enriched YES/NO all right")

# ==== 3. second run REPLACES: identical counts, no duplicates, no stacked colour rules ====
before = dict(counts); fmt_before = len(split.fmt); puts_before = len(ns["PUTS"])
urllib.request.urlopen = fake_urlopen_factory([PAGE1, PAGE2])
with Capture() as cap:
    ns["sync_ghl_status"](main)
after = {t: len(split.tabs[t].rows) - 1 for t in ns["GHL_TABS"]}
assert after == before, (before, after)
for t in ns["GHL_TABS"]:
    ids = [r[G["GHL Contact ID"]] for r in split.tabs[t].rows[1:]]
    assert len(ids) == len(set(ids)), (t, ids)
    assert split.tabs[t].cleared == 2 and split.tabs[t].updates == 2, (t, split.tabs[t].cleared, split.tabs[t].updates)
assert len(split.fmt) == fmt_before, "colour rules stacked on an existing tab"
print("3. second run: row counts identical, no duplicate ids, colour rules not re-added")

# ==== 4. a moved contact moves (source of truth is GHL) ======================
moved = [contact(1, "5708 Zinnia Ave", ["alpha-t2-gold", "not interested"]),
         contact(2, "6381 Rosebud Rd", [], phone=None),
         contact(3, "1 Nowhere Ln", [])]                        # c3 lost its tag -> placed nowhere
urllib.request.urlopen = fake_urlopen_factory([moved, PAGE2])
with Capture() as cap:
    ns["sync_ghl_status"](main)
assert by_id(split.tabs["Gold"])["c1"][G["Disposition"]] == "NI"
assert "c3" not in by_id(split.tabs["Green"]) and len(split.tabs["Green"].rows) - 1 == 1
assert "1 contact(s) on no hunter tab and carrying no colour tag" in cap.text
assert ns["PUTS"]["optimus/_feed/_ghl_status.json"]["not_placed"] == 1
print("4. tag change moves the person; no-map no-tag contact counted and not placed")

# ==== 5. big pull: >5,000 rows go in 5,000-row blocks and the grid is sized first ====
big = [contact(1000 + i, "1 Nowhere Ln", ["type-green"]) for i in range(5200)]
urllib.request.urlopen = fake_urlopen_factory([big[:3000], big[3000:]])
with Capture() as cap:
    ns["sync_ghl_status"](main)
gws = split.tabs["Green"]
assert len(gws.rows) - 1 == 5200 and gws.row_count >= 5201, (len(gws.rows), gws.row_count)
assert gws.updates == 3 + 2, gws.updates                        # 3 earlier runs + 2 blocks now
print("5. 5,200 rows -> 2 update blocks, grid resized to fit")
ns["GHL_GOLD_LIST_CAP"] = 1
with Capture() as cap:
    ns["sync_ghl_status"](main)
gu = ns["PUTS"]["optimus/_feed/gold_unenriched.json"]
assert gu["capped"] is True and len(gu["addresses"]) == 1 and gu["not_in_ghl"] == 3, gu   # no GHL gold contact now
ns["GHL_GOLD_LIST_CAP"] = 5000
print("5b. gold backlog list capped, said so, counts still whole")

# ==== 6. time box / non-429 HTTP error: keep what was read =================
def http_fail(req, timeout=None):
    CALLS.append(req)
    if "startAfterId" in req.full_url:
        raise urllib.error.HTTPError(req.full_url, 401, "Unauthorized", {}, None)
    return Resp({"contacts": PAGE1, "meta": {"startAfterId": "c3", "startAfter": 1}})
urllib.request.urlopen = http_fail
with Capture() as cap:
    ns["sync_ghl_status"](main)
assert "HTTP 401 -- using the 3 contact(s) read so far" in cap.text and "(PARTIAL)" in cap.text
assert ns["PUTS"]["optimus/_feed/_ghl_status.json"]["pull_complete"] is False
assert len(split.tabs["Gold"].rows) - 1 == 1                    # rewritten from the 3 it has
ns["GHL_PULL_SECS"] = -1
urllib.request.urlopen = fake_urlopen_factory([PAGE1, PAGE2])
with Capture() as cap:
    ns["sync_ghl_status"](main)
assert "using the 0 contact(s) read so far" in cap.text and "GHL STATUS: 0 contact(s) read" in cap.text
ns["GHL_PULL_SECS"] = 1200
print("6. HTTP 401 and the time box both stop the pull and keep what was read")

# ==== 7. split workbook did not open: one line, nothing written anywhere ====
lone = Book(full=True); lone.tabs.update(main.tabs); lone.split = None
urllib.request.urlopen = fake_urlopen_factory([PAGE1, PAGE2])
n_calls = len(CALLS); puts = dict(ns["PUTS"])
with Capture() as cap:
    ns["sync_ghl_status"](lone)
lines = [l for l in cap.text.splitlines() if l.strip()]
assert len(lines) == 1 and "split workbook did not open" in lines[0], lines
assert set(lone.tabs) == set(main.tabs) and len(CALLS) == n_calls and ns["PUTS"] == puts
print("7. split did not open: one line, nothing written, GHL not even called")

# ==== 8. split workbook FULL: said once, never retried ======================
m2, s2 = hunter_books(); s2.full = True
with Capture() as cap:
    ns["sync_ghl_status"](m2)
assert not s2.tabs and cap.text.count("10,000,000-cell") >= 1 and "NOT WRITTEN" in cap.text
m3, s3 = hunter_books(); s3.tabs["Green"] = WS("Green", [H]); s3.tabs["Green"].full = True
with Capture() as cap:
    ns["sync_ghl_status"](m3)
assert cap.text.count("remaining tabs are skipped") == 1 and "Gold" not in s3.tabs, list(s3.tabs)
assert all(not v["written"] for v in ns["PUTS"]["optimus/_feed/_ghl_status.json"]["tabs"].values())
print("8. FULL workbook: printed once, the other tabs skipped, nothing retried")

# ==== 9. nothing raises out of the block ====================================
def boom(req, timeout=None): raise RuntimeError("socket melted")
urllib.request.urlopen = boom
with Capture() as cap:
    ns["sync_ghl_status"](main)
assert "socket melted" in cap.text and "using the 0 contact(s)" in cap.text
class Bad:
    split = property(lambda s: (_ for _ in ()).throw(RuntimeError("workbook exploded")))
with Capture() as cap:
    ns["sync_ghl_status"](Bad())
assert cap.text.strip() == "(GHL STATUS skipped: workbook exploded)", cap.text
print("9. network and workbook failures are one printed line each, nothing raises")

# ==== 10. env token works too ================================================
os.remove(os.path.join(TMP, "ghl_token.txt")); os.environ["GHL_PIT_TOKEN"] = "TESTTOKEN"
urllib.request.urlopen = fake_urlopen_factory([PAGE1, PAGE2])
with Capture() as cap:
    ns["sync_ghl_status"](main)
assert "'Gold': 2 people" in cap.text and "TESTTOKEN" not in cap.text
os.environ.pop("GHL_PIT_TOKEN", None)
print("10. GHL_PIT_TOKEN fallback works, token never printed")
print("ALL TESTS PASS")
