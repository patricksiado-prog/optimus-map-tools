"""
THE MAP MAN v9.9
=================
WHAT'S NEW vs 9.8:
  - HUNTER COMMERCIAL ENRICHMENT (renamed from Hunter Green Commercial)
  - Filter accepts ALL ELIGIBLE rows (FIBER ELIGIBLE + UPGRADE ELIGIBLE)
  - Business Name writeback when found via Google Maps panel
  - No interactive ZIP prompt - defaults to Houston metro

USAGE:
  python themapman.py --att-leads --dry-run --limit 25     # preview
  python themapman.py --att-leads --headless               # enrich live
  python themapman.py --att-leads --since-date 2026-05-03 --headless
  python themapman.py --headless                           # full Houston run
  python themapman.py --zip 77034 --headless               # single ZIP
"""

import os, sys, re, time, argparse
from datetime import datetime
from collections import Counter

import requests, gspread
from google.oauth2.service_account import Credentials

VERSION = "9.9"

# AUTO UPDATE
GITHUB_USER   = "patricksiado-prog"
GITHUB_REPO   = "optimus-map-tools"
GITHUB_BRANCH = "main"
THIS_FILE     = "themapman.py"
GITHUB_RAW    = "https://raw.githubusercontent.com/%s/%s/%s/%s" % (
    GITHUB_USER, GITHUB_REPO, GITHUB_BRANCH, THIS_FILE)

def check_update():
    print("  Checking for updates...")
    try:
        r = requests.get(GITHUB_RAW, timeout=10)
        if r.status_code != 200:
            print("  GitHub unreachable - running v%s" % VERSION); return
        latest = r.text
        m = re.search(r'^\s*VERSION\s*=\s*["\'](.*?)["\']\s*$',
                      latest, re.MULTILINE)
        new_ver = m.group(1) if m else None
        if not new_ver or new_ver == VERSION:
            print("  Up to date (v%s)" % VERSION); return
        print("  Updating to v%s ..." % new_ver)
        with open(os.path.abspath(__file__), "w", encoding="utf-8") as f:
            f.write(latest)
        print("  Updated! Restarting...")
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print("  Update check failed: %s" % e)

check_update()

CREDS_FILE = "google_creds.json"
SHEET_ID   = "12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag"
TAB_ROWS   = 5000
NOMINATIM  = "https://nominatim.openstreetmap.org"

# TABS / HEADERS
READY_TAB      = "Ready To Call"
COMMERCIAL_TAB = "Commercial"
GREEN_TAB      = "Green Commercial"
ALL_LEADS_TAB  = "All Leads"
VERIFIED_TAB   = "Verified Fiber"

READY_HEADERS = [
    "Business Name","Phone","Address","City","State","ZIP",
    "Fiber Status","Category","Source","Matched By","Added At",
]
COMMERCIAL_HEADERS = [
    "Business Name","Address","Phone","Category","City","State","ZIP",
    "Lead Type","Data Source","Phone Source","Notes","Found By","Added At",
]
GREEN_HEADERS = [
    "Address","Business Name","City","State","ZIP","Zone",
    "Instance","Scan #","Date","Lat","Lng",
    "Phone","Phone Source","Phone Checked At",
]
VERIFIED_HEADERS = [
    "Business Name","Address","Phone","City","State","ZIP",
    "Category","Source","Verified By","Captured At",
]

# TIMING
MAP_DELAY    = 2.5
CLICK_DELAY  = 2.8
PANEL_CLEAR_TIMEOUT = 2000
BATCH_SIZE   = 20
GRID_STEP    = 0.015

# KNOWN BAD PHONES
KNOWN_BAD_PHONES = {
    "(832) 899-4658",
}

PANEL_NAME_REJECT = {
    "results","sponsored","directions","search results",
    "places","you","your places","saved","timeline",
}

# HOUSTON METRO ZIPS
HOUSTON_METRO_ZIPS = [
    "77002","77003","77004","77005","77006","77007","77008","77009","77010",
    "77011","77012","77013","77014","77015","77016","77017","77018","77019",
    "77020","77021","77022","77023","77024","77025","77026","77027","77028",
    "77029","77030","77031","77033","77034","77035","77036","77038","77040",
    "77041","77042","77043","77044","77045","77046","77047","77048","77049",
    "77050","77051","77053","77054","77055","77056","77057","77058","77059",
    "77060","77061","77062","77063","77064","77065","77066","77067","77068",
    "77069","77070","77071","77072","77073","77074","77075","77076","77077",
    "77078","77079","77080","77081","77082","77083","77084","77085","77086",
    "77087","77088","77089","77090","77091","77092","77093","77094","77095",
    "77096","77098","77099",
    "77338","77339","77345","77346","77373","77375","77377","77379","77380",
    "77381","77382","77384","77386","77388","77389","77396","77401","77407",
    "77417","77429","77433","77449","77450","77459","77469","77471","77477",
    "77478","77479","77489","77493","77494","77498",
    "77573","77584","77586","77587","77598",
]

# SEARCH CATEGORIES
SEARCH_CATEGORIES = [
    "home based business","small businesses","mobile notary","notary public",
    "tax preparation","bookkeeping services","accounting services",
    "insurance agent","mortgage broker","credit repair",
    "business consultant","marketing consultant","web design","graphic designer",
    "photographer","videographer","event planner","party rentals",
    "balloon decorator","catering","meal prep service","home bakery",
    "custom cakes","food truck","private chef","cleaning service",
    "house cleaning","maid service","laundry service","mobile detail",
    "car detailing","mobile mechanic","auto repair","towing service",
    "handyman","plumber","electrician","hvac contractor","roofing contractor",
    "painting contractor","flooring contractor","landscaping","lawn care",
    "pest control","fence contractor","pressure washing","pool cleaning",
    "moving company","courier service","delivery service","home daycare",
    "child care","private tutor","music lessons","piano teacher",
    "dance instructor","personal trainer","yoga instructor","boxing trainer",
    "tattoo artist","pet groomer","dog walker","pet sitter","dog trainer",
    "seamstress","alterations","tailor","custom t shirts","embroidery",
    "screen printing","sign shop","computer repair","phone repair",
    "appliance repair","locksmith","bail bonds","immigration services",
    "translation services","process server","security company",
    "staffing agency",
    "restaurants","auto repair shops","dentists",
    "real estate offices","gyms","retail stores","tax offices",
    "daycare centers","veterinary clinics","printing shops","florists",
    "dry cleaners","mechanics","body shops","tire shops",
    "medical offices","chiropractors","physical therapy","orthodontists",
    "optometrists","pet groomers","coffee shops","bakeries","bars",
    "food trucks","marketing agencies","it services","moving companies",
    "cleaning services","landscapers","jewelry stores","clothing boutiques",
    "shoe stores","gift shops","pawn shops","smoke shops",
    "funeral homes","tutoring centers",
]

# EXCLUDE - chains/big corp
EXCLUDE = [
    "walmart","sam's club","target","costco","home depot","lowes",
    "best buy","ikea","bed bath","tj maxx","ross dress","marshalls","burlington",
    "old navy","gap ","h&m","zara","forever 21","victoria's secret","bath & body",
    "ulta beauty","sephora","dollar general","dollar tree","family dollar",
    "five below","big lots","tuesday morning","party city","michaels",
    "hobby lobby","jo-ann",
    "kroger","heb ","h-e-b","publix","safeway","albertsons","aldi",
    "whole foods","trader joe's","sprouts","randalls","fiesta mart",
    "food lion","meijer","winn-dixie","wegmans","giant","stop & shop",
    "mcdonald's","burger king","taco bell","wendy's","chick-fil","subway",
    "sonic drive","dairy queen","whataburger","popeyes","kfc ",
    "raising cane","wingstop","zaxby's","jack in the box","del taco",
    "carl's jr","hardee's","checkers","rally's","five guys","shake shack",
    "in-n-out","smashburger","panda express","chipotle","qdoba",
    "moe's southwest","domino's","pizza hut","papa john","little caesar",
    "starbucks","dunkin","tim horton","panera","jason's deli",
    "jersey mike's","firehouse subs","jimmy john","potbelly",
    "olive garden","red lobster","applebee's","chili's","outback steakhouse",
    "texas roadhouse","longhorn steakhouse","buffalo wild wings","hooters",
    "denny's","ihop","waffle house","cracker barrel","golden corral","sizzler",
    "chase bank","wells fargo","bank of america","citibank","us bank",
    "td bank","pnc bank","capital one","regions bank","frost bank",
    "bb&t","suntrust","truist","fifth third","comerica","m&t bank",
    "navy federal","usaa","ally bank","citizens bank","keybank",
    "huntington bank","bbva","hsbc","santander bank",
    "walgreens","cvs ","rite aid","duane reade",
    "7-eleven","circle k","wawa","sheetz","casey's","racetrac",
    "shell ","chevron","exxon","valero","texaco","bp ","sunoco","marathon",
    "speedway","kwik trip","loves travel","pilot flying","flying j",
    "advance auto","autozone","o'reilly auto","napa auto","discount tire",
    "america's tire","firestone","goodyear","michelin","midas ","pep boys",
    "carmax","carvana","autonation","sonic automotive",
    "toyota of ","honda of ","ford of ","chevrolet of ","nissan of ",
    "hyundai of ","kia of ","mazda of ","subaru of ","bmw of ",
    "mercedes-benz of ","lexus of ","infiniti of ","cadillac of ",
    "fedex office","fedex ground","ups store","ups freight",
    "post office","usps","dhl","staples ","office depot","officemax",
    "planet fitness","la fitness","24 hour fitness","anytime fitness",
    "gold's gym","snap fitness","crunch fitness","equinox","lifetime fitness",
    "orange theory","f45 training","pure barre","soulcycle",
    "great clips","supercuts","sport clips","fantastic sams","cost cutters",
    "hair cuttery","regis salon","smartstyle","first choice",
    "floyd's barbershop","sally beauty",
    "petco","petsmart","pet supplies plus","petland",
    "servpro","servicemaster","stanley steemer","molly maid","merry maids",
    "two men and a truck","college hunks","1-800-got-junk",
    "termimite","orkin","truly nolen","aptive",
    "tru green","lawn doctor","scotts lawn",
    "regus ","wework","spaces coworking","industrious",
    "public storage","extra space","life storage","cubesmart","u-haul",
    "city hall","county ","courthouse","dmv ","social security",
    "fire station","police station","police department","sheriff",
    "constable","jail","prison","detention","government","municipal",
    "public works","state of texas","city of houston","department of",
    "irs ",
    "university","community college","junior college","college "," isd ",
    "high school","middle school","elementary school","school district",
    "hospital","medical center","health system","health network",
    "children's hospital","memorial herman","methodist hospital","hca ",
    "ascension","dignity health","kaiser","tenet health",
    "concentra","nextcare","davita","fresenius","md anderson",
    " law office"," law firm","attorneys at law","personal injury law",
    " llp ","p.l.l.c","pllc ",
    "re/max ","remax ","century 21","keller williams","coldwell banker","berkshire hathaway",
    "credit union","jackson hewitt",
    "h&r block","liberty tax",
    "apple store","microsoft","at&t store","t-mobile store",
    "verizon store","sprint store","cricket wireless store","boost mobile store",
    "amc theatre","regal cinema","cinemark","dave & buster's","main event",
    "topgolf","bowlero","chuck e. cheese",
    "state farm","allstate","geico","progressive insurance","farmers insurance",
]

BIG_BIZ_SIGNALS = [
    "corporate headquarters","corporate office","regional office",
    "national chain","fortune 500","publicly traded","nyse:","nasdaq:",
    "holdings llc","holdings inc","management corp","solutions corp",
    "services corp","group inc","enterprises inc","international inc",
    "international corp","corporate campus","distribution center",
    "fulfillment center","manufacturing facility","processing plant",
    "headquarters","corporate hq",
]

_pw = _browser = _page = None

FIBER_ADDR_KEYS    = set()
FIBER_STREET_INDEX = {}

# HELPERS
def now_str():
    return datetime.now().strftime("%m/%d/%Y %I:%M %p")

def norm(s):
    if not s: return ""
    s = re.sub(r"[^\w\s]", " ", str(s).lower().strip())
    return re.sub(r"\s+", " ", s).strip()

def col_letter(n):
    out = ""
    while n:
        n, rem = divmod(n - 1, 26)
        out = chr(65 + rem) + out
    return out

def clean_phone(phone):
    if not phone: return ""
    digits = re.sub(r"\D", "", str(phone))
    if len(digits) == 11 and digits.startswith("1"): digits = digits[1:]
    if len(digits) == 10:
        return "(%s) %s-%s" % (digits[:3], digits[3:6], digits[6:])
    return ""

def extract_phone(text):
    if not text: return ""
    for pat in [r"\(?\b\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b",
                r"\b1[-.\s]\d{3}[-.\s]\d{3}[-.\s]\d{4}\b"]:
        m = re.search(pat, text)
        if m: return clean_phone(m.group(0))
    return ""

def looks_like_address(text):
    if not text: return False
    t = str(text).strip()
    if re.match(r"^-?\d+\.\d+,\s*-?\d+\.\d+$", t): return False
    if not re.search(r"\b\d{2,6}\b", t): return False
    words = [" st", " street"," rd"," road"," ave"," avenue"," dr"," drive",
             " ln"," lane"," blvd"," boulevard"," pkwy"," parkway"," way",
             " ct"," court"," cir"," circle"," hwy"," highway"," fwy",
             " freeway"," loop"," trail"," trl"," place"," pl"," plaza",
             " suite"," ste"," terrace"," ter"]
    low = " " + t.lower()
    return any(w in low for w in words)

def street_number(text):
    m = re.search(r"\b(\d{2,6})\b", str(text or ""))
    return m.group(1) if m else ""

STREET_SUFFIX_MAP = {
    "street": "st","st.": "st","road": "rd","rd.": "rd",
    "avenue": "ave","ave.": "ave","drive": "dr","dr.": "dr",
    "boulevard": "blvd","blvd.": "blvd","lane": "ln","ln.": "ln",
    "court": "ct","ct.": "ct","circle": "cir","cir.": "cir",
    "highway": "hwy","hwy.": "hwy","parkway": "pkwy","pkwy.": "pkwy",
    "freeway": "fwy","fwy.": "fwy","place": "pl","pl.": "pl",
}

def address_norm(addr):
    if not addr: return ""
    s = norm(addr)
    return " ".join(STREET_SUFFIX_MAP.get(t, t) for t in s.split())

def street_name_only(addr):
    if not addr: return ""
    n = address_norm(addr)
    num = street_number(addr)
    if num:
        n = re.sub(r"\b" + re.escape(num) + r"\b", "", n).strip()
    toks = [t for t in n.split() if t][:3]
    return " ".join(toks)

def addr_key(addr):
    num = street_number(addr)
    if not num: return ""
    sname = street_name_only(addr)
    if not sname: return ""
    return num + "|" + sname

def fiber_status_for(addr):
    if not addr: return "", ""
    k = addr_key(addr)
    sname = street_name_only(addr)
    num   = street_number(addr)

    if k and k in FIBER_ADDR_KEYS:
        return "VERIFIED FIBER", "exact-address match"

    if sname and sname in FIBER_STREET_INDEX:
        verified = FIBER_STREET_INDEX[sname]
        if num and verified:
            try:
                ni = int(num)
                close = [v for v in verified if abs(v - ni) <= 50]
                if close:
                    return "LIKELY FIBER", "same-block match (~%d)" % min(
                        abs(v - ni) for v in close)
            except: pass
        return "MAYBE FIBER", "same-street match"

    return "", ""

def address_match(a, b):
    if not a or not b: return False
    a_num = street_number(a); b_num = street_number(b)
    if a_num and b_num and a_num != b_num: return False
    aw = set(norm(a).split()); bw = set(norm(b).split())
    common = aw & bw
    return len(common) >= 3 or (a_num and b_num and a_num == b_num and len(common) >= 2)

def name_match(a, b):
    if not a or not b: return False
    an = norm(a); bn = norm(b)
    if an == bn: return True
    aw = set(an.split()); bw = set(bn.split())
    if not aw or not bw: return False
    common = aw & bw
    return len(common) >= 2 or len(common) >= min(len(aw), len(bw))

def is_small_biz(name, cat=""):
    if not name or len(str(name).strip()) < 3: return False
    combined = (str(name) + "  " + str(cat or "")).lower()
    for kw in EXCLUDE:
        if kw in combined: return False
    for sig in BIG_BIZ_SIGNALS:
        if sig in combined: return False
    if re.match(r"^[\d\s,.\-]+$", str(name).strip()): return False
    return True

def is_bad_phone(phone, extra_bad=None):
    if not phone: return False
    if extra_bad is None: extra_bad = set()
    return phone in KNOWN_BAD_PHONES or phone in extra_bad

# v9.9 HUNTER ENRICHER (FIBER + UPGRADE ELIGIBLE rows)
HUNTER_SHEET_ID = "12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag"

def enrich_hunter_leads(tab_name="Hunter Commercial", since_date_str=None, dry_run=False, limit=None):
    """v9.9 - Enrich Hunter Commercial tab (FIBER + UPGRADE ELIGIBLE) with biz name+phone via Google Maps"""
    scopes = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"]
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    ss     = client.open_by_key(HUNTER_SHEET_ID)
    ws     = ss.worksheet(tab_name)
    vals = ws.get_all_values()
    if not vals or len(vals) < 2:
        print("  No data"); return 0

    headers = {h.lower().strip(): i+1 for i, h in enumerate(vals[0])}

    def col(name):
        return headers.get(name.lower())

    addr_idx  = col("address")
    type_idx  = col("type")
    phone_idx = col("phone")
    date_idx  = col("date")
    name_idx  = col("business name")
    city_idx  = col("city")
    state_idx = col("state")
    zip_idx   = col("zip")

    since = None
    if since_date_str:
        try: since = datetime.strptime(since_date_str, "%Y-%m-%d")
        except: pass

    def cell(row, idx):
        return row[idx-1].strip() if idx and idx <= len(row) else ""

    candidates = []
    for row_num, row in enumerate(vals[1:], start=2):
        addr = cell(row, addr_idx)
        if not addr or not looks_like_address(addr): continue
        if "(no #" in addr.lower(): continue

        if type_idx:
            typ = cell(row, type_idx)
            # v9.9: accept FIBER ELIGIBLE and UPGRADE ELIGIBLE
            if "ELIGIBLE" not in typ.upper(): continue

        if since and cell(row, date_idx):
            try:
                rd = datetime.strptime(cell(row, date_idx).split()[0], "%m/%d/%Y")
                if rd < since: continue
            except: pass

        if cell(row, phone_idx):
            continue

        candidates.append({
            "row_num": row_num,
            "address": addr,
            "name": cell(row, name_idx),
            "city": cell(row, city_idx),
            "state": cell(row, state_idx) or "TX",
            "zip": cell(row, zip_idx),
        })

        if limit and len(candidates) >= limit:
            break

    print("  Candidates: %d from %s" % (len(candidates), tab_name))

    if dry_run:
        for c in candidates[:20]:
            print("    row %d: %s | %s %s %s" % (
                c["row_num"], c["address"][:50], c["city"], c["state"], c["zip"]))
        return len(candidates)

    done = 0
    for i, c in enumerate(candidates, start=1):
        found = lookup_by_address(
            c["address"],
            business_name=c["name"],
            city=c["city"],
            state=c["state"],
            zipc=c["zip"]
        )

        if not found or not found.get("phone"):
            continue

        phone = found["phone"]
        if is_bad_phone(phone):
            continue

        updates = [{
            "range": "%s%d" % (col_letter(phone_idx), c["row_num"]),
            "values": [[phone]]
        }]

        # v9.9: also write Business Name back when mapman found one
        # and the existing Business Name cell is empty
        biz_found = (found.get("name") or "").strip()
        if biz_found and name_idx and not c["name"]:
            updates.append({
                "range": "%s%d" % (col_letter(name_idx), c["row_num"]),
                "values": [[biz_found]]
            })

        batch_update_safe(ws, updates)
        done += 1

    print("  Done: %d phones enriched from %s" % (done, tab_name))
    return done

# SHEETS
def connect_sheets():
    if not os.path.exists(CREDS_FILE):
        print("\nERROR: google_creds.json not found."); sys.exit(1)
    scopes = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"]
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    ss     = client.open_by_key(SHEET_ID)
    ready_ws    = get_or_create_tab(ss, READY_TAB,      READY_HEADERS)
    comm_ws     = get_or_create_tab(ss, COMMERCIAL_TAB, COMMERCIAL_HEADERS)
    green_ws    = get_or_create_tab(ss, GREEN_TAB,      GREEN_HEADERS, required=False)
    verified_ws = get_or_create_tab(ss, VERIFIED_TAB,   VERIFIED_HEADERS)
    try:    all_leads_ws = ss.worksheet(ALL_LEADS_TAB)
    except: all_leads_ws = None
    print("Connected to Google Sheets")
    return ss, ready_ws, comm_ws, green_ws, all_leads_ws, verified_ws

def get_or_create_tab(ss, title, headers, required=True):
    try:
        ws = ss.worksheet(title)
    except gspread.exceptions.WorksheetNotFound:
        if not required: return None
        ws = ss.add_worksheet(title=title, rows=TAB_ROWS,
                              cols=max(len(headers), 20))
        ws.update(range_name="A1", values=[headers])
        print("  Created tab: %s" % title); return ws
    vals = ws.get_all_values()
    if not vals:
        ws.update(range_name="A1", values=[headers]); return ws
    existing = [h.lower().strip() for h in vals[0]]
    new_hdrs = list(vals[0]); changed = False
    for h in headers:
        if h.lower() not in existing:
            new_hdrs.append(h); existing.append(h.lower()); changed = True
    if changed:
        try: ws.resize(rows=max(len(vals)+2000, TAB_ROWS),
                       cols=max(len(new_hdrs), 20))
        except: pass
        ws.update(range_name="A1:%s1" % col_letter(len(new_hdrs)),
                  values=[new_hdrs])
        print("  Updated columns: %s" % title)
    return ws

def header_map(ws):
    vals = ws.get_all_values()
    if not vals: return {}
    return {h.lower().strip(): i + 1 for i, h in enumerate(vals[0])}

def get_cell(row, hmap, names):
    for name in names:
        idx = hmap.get(name.lower())
        if idx and len(row) >= idx:
            v = str(row[idx - 1]).strip()
            if v: return v
    return ""

def append_rows_safe(ws, rows):
    if not ws or not rows: return
    for attempt in range(3):
        try:
            ws.append_rows(rows, value_input_option="USER_ENTERED")
            time.sleep(0.5); return
        except Exception as e:
            print("  Append err %d: %s" % (attempt+1, e)); time.sleep(5)

def batch_update_safe(ws, updates):
    if not updates: return
    for attempt in range(3):
        try:
            ws.batch_update(updates, value_input_option="USER_ENTERED")
            time.sleep(0.5); return
        except Exception as e:
            print("  Batch update err %d: %s" % (attempt+1, e)); time.sleep(5)

def ensure_phone_cols(ws):
    vals = ws.get_all_values()
    if not vals: return header_map(ws)
    needed = ["Phone","Phone Source","Phone Checked At"]
    headers = list(vals[0])
    existing = [h.lower().strip() for h in headers]
    changed = False
    for col in needed:
        if col.lower() not in existing:
            headers.append(col); existing.append(col.lower()); changed = True
    if changed:
        try: ws.resize(rows=max(len(vals)+2000, TAB_ROWS),
                       cols=max(len(headers), 20))
        except: pass
        ws.update(range_name="A1:%s1" % col_letter(len(headers)),
                  values=[headers])
        print("  Added phone columns to tab.")
    return header_map(ws)

def build_fiber_index(green_ws, all_leads_ws):
    global FIBER_ADDR_KEYS, FIBER_STREET_INDEX
    FIBER_ADDR_KEYS = set()
    FIBER_STREET_INDEX = {}
    sources = []
    if green_ws: sources.append(green_ws)
    if all_leads_ws: sources.append(all_leads_ws)
    for ws in sources:
        try:
            vals = ws.get_all_values()
            if not vals or len(vals) < 2: continue
            hmap = {h.lower().strip(): i for i, h in enumerate(vals[0])}
            addr_i = hmap.get("address")
            if addr_i is None: continue
            for row in vals[1:]:
                if addr_i >= len(row): continue
                addr = str(row[addr_i]).strip()
                if not addr: continue
                k = addr_key(addr)
                if k: FIBER_ADDR_KEYS.add(k)
                sname = street_name_only(addr)
                num = street_number(addr)
                if sname and num:
                    try:
                        FIBER_STREET_INDEX.setdefault(sname, []).append(int(num))
                    except: pass
        except Exception as e:
            print("  Fiber index err: %s" % e)
    print("  Fiber index: %d exact addrs, %d streets" % (
        len(FIBER_ADDR_KEYS), len(FIBER_STREET_INDEX)))

# ENRICHER
def lookup_by_address(address, business_name="", city="", state="TX", zipc=""):
    global _page
    if not address or not looks_like_address(address):
        print("    Skipping - not a real address: %s" % str(address)[:60])
        return None

    parts = [address]
    if zipc and re.match(r"^\d{5}$", zipc.strip()):
        parts.append(zipc.strip())
    elif city:
        parts.append(city + " " + (state or "TX"))
    q = " ".join(parts)

    try:
        url = "https://www.google.com/maps/search/%s" % q.replace(" ", "+")
        _page.goto(url, timeout=25000, wait_until="domcontentloaded")
        time.sleep(MAP_DELAY)

        if "/place/" in _page.url:
            pname  = panel_name()
            pphone = panel_phone()
            paddr  = panel_address()
            if pphone in KNOWN_BAD_PHONES: pphone = ""
            matched_by = ""
            if address and paddr and address_match(address, paddr):
                matched_by = "address"
            elif business_name and pname and name_match(business_name, pname):
                matched_by = "name"
            if not matched_by: pphone = ""
            return {
                "name": pname or business_name, "phone": pphone,
                "address": paddr or address, "matched_by": matched_by,
                "source": "Google Maps",
            }

        cards = get_cards()
        if not cards: return None

        for card in cards[:3]:
            result = click_card_and_extract(
                card, expected_name=business_name, expected_address=address)
            if result and result["phone"]:
                return {
                    "name": result["panel_name"] or result["card_name"] or business_name,
                    "phone": result["phone"],
                    "address": result["address"] or address,
                    "matched_by": result["matched_by"],
                    "source": "Google Maps",
                }
        return None

    except Exception as e:
        print("    Lookup error: %s" % e)
        return None

def enrich_tab(ws, tab_name, ready_ws, all_bad_phones, limit=None):
    if not ws:
        print("  Tab not found: %s - skipping" % tab_name); return 0

    hmap = ensure_phone_cols(ws)
    vals = ws.get_all_values()
    if not vals or len(vals) < 2: return 0

    phone_counts = Counter()
    for row in vals[1:]:
        p = get_cell(row, hmap, ["phone"])
        if p: phone_counts[p] += 1
    tab_bad = {p for p, c in phone_counts.items() if c >= 3}
    tab_bad.update(all_bad_phones)

    rows_to_fix = []
    for row_num, row in enumerate(vals[1:], start=2):
        name  = get_cell(row, hmap, ["business name","name"])
        addr  = get_cell(row, hmap, ["address","street address"])
        phone = get_cell(row, hmap, ["phone"])
        city  = get_cell(row, hmap, ["city"])
        state = get_cell(row, hmap, ["state"]) or "TX"
        zipc  = get_cell(row, hmap, ["zip","zip code","postal code"])
        fstat = get_cell(row, hmap, ["type","fiber status","status"])

        if not addr or not looks_like_address(addr): continue
        needs_fix = (not phone) or is_bad_phone(phone, tab_bad)
        if not needs_fix: continue

        rows_to_fix.append({
            "row_num": row_num, "name": name, "address": addr,
            "city": city, "state": state, "zip": zipc,
            "fiber_status": fstat, "old_phone": phone,
        })
        if limit and len(rows_to_fix) >= limit: break

    print("\n" + "="*60)
    print("  ENRICHING: %s" % tab_name)
    print("  Rows to fix: %d" % len(rows_to_fix))
    print("="*60)

    done = 0
    ready_batch = []

    for i, item in enumerate(rows_to_fix, start=1):
        print("\n  [%d/%d] Row %d | %s" % (
            i, len(rows_to_fix), item["row_num"], item["address"][:55]))
        if item["old_phone"]:
            print("    Replacing bad phone: %s" % item["old_phone"])

        found = lookup_by_address(
            item["address"], business_name=item["name"],
            city=item["city"], state=item["state"], zipc=item["zip"])

        if not found or not found.get("phone"):
            print("    No safe phone found"); continue

        new_phone = found["phone"]
        if is_bad_phone(new_phone, tab_bad):
            print("    Phone still bad, skipping: %s" % new_phone); continue

        print("    Phone: %s | matched by: %s" % (
            new_phone, found.get("matched_by","")))

        hmap = header_map(ws)
        updates = []
        if "phone" in hmap:
            updates.append({"range": "%s%d" % (col_letter(hmap["phone"]), item["row_num"]),
                           "values": [[new_phone]]})
        if "phone source" in hmap:
            updates.append({"range": "%s%d" % (col_letter(hmap["phone source"]), item["row_num"]),
                           "values": [["Google Maps - panel confirmed"]]})
        if "phone checked at" in hmap:
            updates.append({"range": "%s%d" % (col_letter(hmap["phone checked at"]), item["row_num"]),
                            "values": [[now_str()]]})
        if updates:
            batch_update_safe(ws, updates)

        biz_name = found.get("name") or item["name"] or item["address"]
        addr_out = found.get("address") or item["address"]
        fiber_stat, fiber_match = fiber_status_for(addr_out)
        ready_batch.append([
            biz_name, new_phone, addr_out,
            item["city"], item["state"], item["zip"],
            fiber_stat or item["fiber_status"],
            "Fiber Scan Lead", tab_name,
            found.get("matched_by",""), now_str(),
        ])
        if len(ready_batch) >= BATCH_SIZE:
            append_rows_safe(ready_ws, ready_batch)
            ready_batch = []
        done += 1

    if ready_batch:
        append_rows_safe(ready_ws, ready_batch)

    print("\n  Done: %d phones added/fixed in %s" % (done, tab_name))
    return done

# BROWSER
def init_browser(headless=False):
    global _pw, _browser, _page
    from playwright.sync_api import sync_playwright
    _pw      = sync_playwright().start()
    _browser = _pw.chromium.launch(
        headless=headless,
        args=["--disable-blink-features=AutomationControlled",
              "--no-sandbox","--disable-dev-shm-usage"])
    ctx = _browser.new_context(
        viewport={"width":1366,"height":768},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/122.0.0.0 Safari/537.36",
        locale="en-US")
    _page = ctx.new_page()
    _page.goto("https://www.google.com/maps", timeout=25000,
               wait_until="domcontentloaded")
    time.sleep(2)
    print("  Browser ready")

def close_browser():
    global _browser, _pw
    try:
        if _browser: _browser.close()
        if _pw: _pw.stop()
    except: pass

def safe_text(el):
    try: return el.inner_text().strip()
    except: return ""

def get_cards():
    global _page
    for sel in ["div.Nv2PKd","div[role='article']"]:
        try:
            cards = _page.query_selector_all(sel)
            if cards: return cards
        except: pass
    return []

def card_name(card):
    for sel in ["div.fontHeadlineSmall","div.qBF1Pd","a.hfpxzc"]:
        try:
            el = card.query_selector(sel)
            if el:
                txt = safe_text(el)
                if txt: return txt.split("\n")[0].strip()
                lbl = el.get_attribute("aria-label") or ""
                if lbl: return lbl.strip().split("\n")[0]
        except: pass
    return ""

def panel_name():
    global _page
    try: _page.wait_for_selector("h1.DUwDvf", timeout=2500)
    except: pass
    for sel in ["h1.DUwDvf","h1.fontHeadlineLarge"]:
        try:
            el = _page.query_selector(sel)
            if el:
                txt = safe_text(el)
                if txt and txt.lower().strip() not in PANEL_NAME_REJECT:
                    return txt
        except: pass
    return ""

def panel_phone():
    global _page
    for sel in ["button[data-item-id='phone']","button[aria-label^='Phone:']",
                "button[aria-label*='Phone:']","a[href^='tel:']"]:
        try:
            for el in _page.query_selector_all(sel):
                label = el.get_attribute("aria-label") or ""
                href  = el.get_attribute("href") or ""
                txt   = safe_text(el)
                phone = extract_phone(label + " " + href + " " + txt)
                if phone: return phone
        except: pass
    return ""

def panel_address():
    global _page
    for sel in ["button[data-item-id='address']",
                "button[aria-label^='Address:']",
                "button[aria-label*='Address:']"]:
        try:
            for el in _page.query_selector_all(sel):
                label = el.get_attribute("aria-label") or ""
                txt   = safe_text(el)
                val   = (label + " " + txt).replace("Address:", "").strip()
                if looks_like_address(val): return val
        except: pass
    return ""

def wait_for_stale_panel_to_clear():
    global _page
    try:
        _page.evaluate("() => { const h = document.querySelector('h1.DUwDvf'); if (h) h.innerText = ''; }")
    except: pass
    time.sleep(0.3)

def click_card_and_extract(card, expected_name="", expected_address=""):
    global _page
    try: _page.keyboard.press("Escape"); time.sleep(0.3)
    except: pass

    cname = card_name(card) or expected_name
    wait_for_stale_panel_to_clear()

    clicked = False
    try:
        link = card.query_selector("a.hfpxzc")
        if link:
            link.click(); clicked = True
    except: pass
    if not clicked:
        try: card.click()
        except: return None

    time.sleep(CLICK_DELAY)

    pname  = panel_name()
    pphone = panel_phone()
    paddr  = panel_address()

    if pphone in KNOWN_BAD_PHONES: pphone = ""

    matched_by = ""
    if expected_address and paddr and address_match(expected_address, paddr):
        matched_by = "address"
    elif expected_name and pname and name_match(expected_name, pname):
        matched_by = "name"
    elif cname and pname and name_match(cname, pname):
        matched_by = "card name"
    else:
        if pphone:
            print("        SKIP - panel mismatch | card: %s | panel: %s" % (
                cname[:30], pname[:30]))
        pphone = ""

    return {
        "card_name": cname, "panel_name": pname,
        "phone": pphone, "address": paddr, "matched_by": matched_by,
    }

# ZIP / HOUSTON RUNS
def run_zip(zipcode, ready_ws, comm_ws, verified_ws, seen_keys, seen_phones, phone_counter, limit=None):
    print("\n  Running ZIP: %s" % zipcode)
    print("  (full ZIP scan logic - placeholder for v9.7 categorical search)")

def run_houston(ready_ws, comm_ws, verified_ws, limit=None):
    print("\n  Running Houston metro (%d ZIPs)..." % len(HOUSTON_METRO_ZIPS))
    seen_keys, seen_phones, phone_counter = set(), set(), Counter()
    for i, zipcode in enumerate(HOUSTON_METRO_ZIPS, start=1):
        print("\n  [%d/%d] ZIP %s" % (i, len(HOUSTON_METRO_ZIPS), zipcode))
        run_zip(zipcode, ready_ws, comm_ws, verified_ws,
                seen_keys, seen_phones, phone_counter, limit=limit)

# MAIN
def main():
    parser = argparse.ArgumentParser(description="THE MAP MAN v%s" % VERSION)
    parser.add_argument("--zip",         type=str, default=None)
    parser.add_argument("--houston",     action="store_true")
    parser.add_argument("--enrich-only", action="store_true")
    parser.add_argument("--headless",    action="store_true")
    parser.add_argument("--limit",       type=int, default=None)
    parser.add_argument("--att-leads",   action="store_true", help="v9.9: enrich Hunter Commercial tab")
    parser.add_argument("--since-date",  type=str, help="Only rows with date >= this (YYYY-MM-DD)")
    parser.add_argument("--dry-run",     action="store_true", help="Print candidates only, no browser")
    args = parser.parse_args()

    print("\n" + "#"*60)
    print("  THE MAP MAN v%s" % VERSION)
    print("  Hunter Commercial enrichment (FIBER + UPGRADE ELIGIBLE)")
    print("#"*60 + "\n")

    # v9.9: Hunter enrichment path
    if args.att_leads:
        if not args.dry_run:
            init_browser(args.headless)
        try:
            enrich_hunter_leads(tab_name="Hunter Commercial",
                               since_date_str=args.since_date,
                               dry_run=args.dry_run, limit=args.limit)
        finally:
            if not args.dry_run:
                close_browser()
        return

    ss, ready_ws, comm_ws, green_ws, all_leads_ws, verified_ws = connect_sheets()

    print("\nBuilding fiber-verified address index...")
    build_fiber_index(green_ws, all_leads_ws)

    init_browser(args.headless)

    try:
        print("\n  STEP 1: Enriching fiber scan tabs...")
        if all_leads_ws:
            enrich_tab(all_leads_ws, ALL_LEADS_TAB, ready_ws,
                       KNOWN_BAD_PHONES, limit=args.limit)
        enrich_tab(green_ws, GREEN_TAB, ready_ws,
                   KNOWN_BAD_PHONES, limit=args.limit)
        enrich_tab(comm_ws, COMMERCIAL_TAB, ready_ws,
                   KNOWN_BAD_PHONES, limit=args.limit)

        if args.enrich_only:
            print("\n  Enrich-only mode - done.")
            return

        # v9.9: no more ZIP prompt - default to Houston metro
        if args.zip:
            if not re.match(r"^\d{5}$", args.zip):
                print("  Invalid ZIP."); sys.exit(1)
            seen_keys, seen_phones, phone_counter = set(), set(), Counter()
            run_zip(args.zip, ready_ws, comm_ws, verified_ws,
                   seen_keys, seen_phones, phone_counter, limit=args.limit)
        else:
            run_houston(ready_ws, comm_ws, verified_ws, limit=args.limit)

    finally:
        close_browser()

if __name__ == "__main__":
    main()
