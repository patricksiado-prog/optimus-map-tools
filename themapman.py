"""
THE MAP MAN v9.3
================
TWO PROGRAMS IN ONE:

  1. FIBER SCAN ENRICHER
     Reads your fiber scan output (All Leads / Green Commercial / Commercial tabs)
     Searches Google Maps for each address
     Clicks the exact business panel — matches by address OR name
     Saves phone ONLY if the panel confirms it's the right place
     Writes enriched leads to "Ready To Call"

  2. ZIP SCRAPER
     Finds every small/home-based business in a ZIP code
     Safe phone mode: panel match required before saving any number
     Dense grid (0.015 step) catches hidden/home businesses
     Massive exclude list blocks all national chains and big corps

Bad phone detection:
  - Hardcoded known bad numbers blocked
  - Any phone appearing 3+ times in same run is flagged and dropped

INSTALL:
  python -m pip install requests gspread google-auth playwright
  python -m playwright install chromium

RUN:
  python themapman.py --enrich-only          enrich fiber scan tabs only
  python themapman.py --zip 77034            scrape ZIP + enrich
  python themapman.py --zip 77034 --headless no browser window
  python themapman.py --enrich-only --limit 50  test with 50 rows
"""

import os, sys, re, time, argparse
from datetime import datetime
from collections import Counter

import requests, gspread
from google.oauth2.service_account import Credentials

VERSION    = "9.4"

# ── AUTO UPDATE ───────────────────────────────────────────────────────
GITHUB_USER   = "patricksiado-prog"
GITHUB_REPO   = "optimus-map-tools"
GITHUB_BRANCH = "main"
THIS_FILE     = "themapman.py"
GITHUB_RAW    = "https://raw.githubusercontent.com/%s/%s/%s/%s" % (
    GITHUB_USER, GITHUB_REPO, GITHUB_BRANCH, THIS_FILE)

def check_update():
    print("  Checking for updates...")
    try:
        import hashlib
        r = requests.get(GITHUB_RAW, timeout=10)
        if r.status_code != 200:
            print("  GitHub unreachable — running v%s" % VERSION); return
        latest = r.text
        with open(os.path.abspath(__file__), "r", encoding="utf-8") as f:
            current = f.read()
        if hashlib.md5(latest.encode()).hexdigest() == hashlib.md5(current.encode()).hexdigest():
            print("  Up to date (v%s)" % VERSION); return
        m = re.search(r'''^\s*VERSION\s*=\s*["\\'](.*?)["\']''', latest, re.MULTILINE)
        new_ver = m.group(1) if m else "?"
        print("  Updating to v%s..." % new_ver)
        with open(os.path.abspath(__file__), "w", encoding="utf-8") as f:
            f.write(latest)
        print("  Updated! Restarting...")
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print("  Update check failed: %s" % e)

check_update()

CREDS_FILE = "google_creds.json"
SHEET_ID   = "15ymTkIGPWs6quB035l414ns5hkG9cQ5xr_W4ukd0OAA"
TAB_ROWS   = 5000
NOMINATIM  = "https://nominatim.openstreetmap.org"

# ── TAB NAMES ──────────────────────────────────────────────────────────
READY_TAB      = "Ready To Call"
COMMERCIAL_TAB = "Commercial"
GREEN_TAB      = "Green Commercial"
ALL_LEADS_TAB  = "All Leads"          # fiber scan main output

# ── HEADERS ────────────────────────────────────────────────────────────
READY_HEADERS = [
    "Business Name", "Phone", "Address", "City", "State", "ZIP",
    "Fiber Status", "Category", "Source", "Matched By", "Added At",
]
COMMERCIAL_HEADERS = [
    "Business Name", "Address", "Phone", "Category", "City", "State", "ZIP",
    "Lead Type", "Data Source", "Phone Source", "Notes", "Found By", "Added At",
]
GREEN_HEADERS = [
    "Address", "Business Name", "City", "State", "ZIP", "Zone",
    "Instance", "Scan #", "Date", "Lat", "Lng",
    "Phone", "Phone Source", "Phone Checked At",
]

# ── TIMING ─────────────────────────────────────────────────────────────
MAP_DELAY   = 2.5
CLICK_DELAY = 2.8
BATCH_SIZE  = 20
GRID_STEP   = 0.015    # tighter = more dense/hidden biz coverage

# ── KNOWN BAD PHONES ───────────────────────────────────────────────────
KNOWN_BAD_PHONES = {
    "(832) 899-4658",
}

# ── SEARCH CATEGORIES (home-biz heavy) ────────────────────────────────
SEARCH_CATEGORIES = [
    "home based business","small businesses","mobile notary","notary public",
    "tax preparation","bookkeeping services","accounting services",
    "insurance agent","real estate agent","mortgage broker","credit repair",
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
    "barber","hair stylist","braids","lash tech","lash studio",
    "nail tech","nail salon","makeup artist","esthetician","waxing",
    "massage therapist","med spa","tattoo artist","pet groomer",
    "dog walker","pet sitter","dog trainer","seamstress","alterations",
    "tailor","custom t shirts","embroidery","screen printing","sign shop",
    "computer repair","phone repair","appliance repair","locksmith",
    "bail bonds","immigration services","translation services",
    "process server","security company","staffing agency",
    "restaurants","auto repair shops","hair salons","nail salons",
    "dentists","insurance offices","real estate offices","gyms","retail stores",
    "law offices","accounting tax offices","daycare centers","pharmacies",
    "veterinary clinics","massage spa","printing shops","florists","dry cleaners",
    "mechanics","body shops","tire shops","barber shops","beauty salons",
    "medical offices","chiropractors","physical therapy","orthodontists",
    "optometrists","pet groomers","coffee shops","bakeries","bars",
    "food trucks","marketing agencies","IT services","moving companies",
    "cleaning services","landscapers","jewelry stores","clothing boutiques",
    "shoe stores","gift shops","pawn shops","smoke shops","churches",
    "nonprofits","funeral homes","tax preparation","tutoring centers",
]

# ── EXCLUDE — NATIONAL CHAINS & BIG CORPS ─────────────────────────────
EXCLUDE = [
    # Big box retail
    "walmart","sam's club","target","costco","home depot","lowe's","lowes",
    "best buy","ikea","bed bath","tj maxx","ross dress","marshalls","burlington",
    "old navy","gap ","h&m","zara","forever 21","victoria's secret","bath & body",
    "ulta beauty","sephora","dollar general","dollar tree","family dollar","five below",
    "big lots","tuesday morning","party city","michaels","hobby lobby","jo-ann",
    # Grocery
    "kroger","heb ","h-e-b","publix","safeway","albertsons","aldi","whole foods",
    "trader joe's","sprouts","randalls","fiesta mart","food lion","meijer",
    "winn-dixie","wegmans","giant","stop & shop","hyvee","hy-vee",
    # Fast food / national chains
    "mcdonald","burger king","taco bell","wendy's","chick-fil","subway","sonic drive",
    "dairy queen","whataburger","popeyes","kfc ","raising cane","wingstop","zaxby",
    "jack in the box","del taco","carl's jr","hardee","checkers","rally's",
    "five guys","shake shack","in-n-out","smashburger",
    "panda express","chipotle","qdoba","moe's southwest",
    "domino's","pizza hut","papa john","little caesar",
    "starbucks","dunkin","tim horton","panera","jason's deli",
    "jersey mike","firehouse subs","jimmy john","potbelly",
    "olive garden","red lobster","applebee's","chili's","outback steakhouse",
    "texas roadhouse","longhorn steakhouse","buffalo wild wings","hooters",
    "denny's","ihop","waffle house","cracker barrel",
    "golden corral","sizzler",
    # Banks
    "chase bank","wells fargo","bank of america","citibank","us bank",
    "td bank","pnc bank","capital one","regions bank","frost bank",
    "bb&t","suntrust","truist","fifth third","comerica","m&t bank",
    "navy federal","usaa","ally bank","citizens bank","keybank",
    "huntington bank","bbva","hsbc","santander bank",
    # Drug / health chains
    "walgreens","cvs ","rite aid","duane reade",
    # Gas / convenience
    "7-eleven","circle k","wawa","sheetz","casey's","racetrac",
    "shell ","chevron","exxon","valero","texaco","bp ","sunoco","marathon",
    "speedway","kwik trip","love's travel","pilot flying","flying j",
    # Hotels
    "marriott","hilton","hyatt","holiday inn","sheraton","westin","w hotel",
    "hampton inn","la quinta","motel 6","super 8","days inn","comfort inn",
    "best western","quality inn","sleep inn","econolodge","red roof","extended stay",
    "residence inn","courtyard by","fairfield inn","springhill suites",
    "embassy suites","doubletree","aloft hotel","four seasons","ritz-carlton",
    "crowne plaza","kimpton","omni hotel","loews hotel","wyndham",
    # Auto chains
    "jiffy lube","valvoline","firestone","goodyear","midas ","pep boys",
    "advance auto","autozone","o'reilly auto","napa auto","discount tire",
    "america's tire","mavis discount","monro muffler","meineke",
    "take 5 oil","express oil","grease monkey",
    "carmax","carvana","autonation","sonic automotive",
    "toyota of ","honda of ","ford of ","chevrolet of ","nissan of ",
    "hyundai of ","kia of ","mazda of ","subaru of ","bmw of ",
    "mercedes-benz of ","lexus of ","infiniti of ","cadillac of ",
    # Shipping / office
    "fedex office","fedex ground","ups store","ups freight",
    "post office","usps","dhl","staples ","office depot","officemax",
    # Gym chains
    "planet fitness","la fitness","24 hour fitness","anytime fitness","gold's gym",
    "snap fitness","crunch fitness","equinox","lifetime fitness","orange theory",
    "f45 training","pure barre","soulcycle",
    # Hair chains
    "great clips","supercuts","sport clips","fantastic sams","cost cutters",
    "hair cuttery","regis salon","smartstyle","first choice","floyd's barbershop",
    "sally beauty",
    # Pet chains
    "petco","petsmart","pet supplies plus","petland",
    # Home services chains
    "servpro","servicemaster","stanley steemer","molly maid","merry maids",
    "two men and a truck","college hunks","1-800-got-junk",
    "terminix","orkin","rollins ","truly nolen","aptive",
    "tru green","lawn doctor","scotts lawn","brightview",
    # Office space / coworking chains
    "regus ","regus-","iwg ","wework","spaces coworking","industrious","hq network",
    "united states postal","the ubc","virtual office",
    # Storage
    "public storage","extra space","life storage","cubesmart","u-haul",
    "simply self storage","storage mart","iron mountain",
    # Government / institutions
    "city hall","county ","courthouse","dmv ","social security",
    "fire station","police station","police department","sheriff","constable",
    "jail","prison","detention","government","municipal","public works",
    "state of texas","city of houston","city of dallas","city of austin",
    "irs ","post office","usps","department of",
    # Schools
    "university","college ","school district"," isd","high school","middle school",
    "elementary school","community college","junior college","vocational school",
    # Hospitals / health systems
    "hospital","medical center","health system","health network",
    "children's hospital","memorial hermann","methodist hospital","hca ",
    "ascension","dignity health","kaiser","intermountain","tenet health",
    "concentra","nextcare","patient first","city md","davita","fresenius",
    # Tech / big corp
    "amazon","apple store","microsoft","google ","meta ","facebook office",
    "at&t store","t-mobile store","verizon store","sprint store",
    "best buy mobile","cricket wireless store","boost mobile store",
    # Entertainment chains
    "amc theatre","regal cinema","cinemark","dave & buster","main event",
    "topgolf","bowlero","chuck e. cheese",
]

# Extra signals that flag a large corporation even if name isn't listed
BIG_BIZ_SIGNALS = [
    "corporate headquarters","corporate office","regional office","national chain",
    "fortune 500","publicly traded","nyse:","nasdaq:",
    "holdings llc","holdings inc","properties llc","properties inc",
    "management corp","solutions corp","services corp","group inc",
    "enterprises inc","international inc","international corp",
    "nationwide ","corporate campus","distribution center",
    "fulfillment center","manufacturing facility","processing plant",
    "headquarters","corporate hq",
]

# ── GLOBALS ────────────────────────────────────────────────────────────
_pw = _browser = _page = None


# ── HELPERS ────────────────────────────────────────────────────────────
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
    words = [" st"," street"," rd"," road"," ave"," avenue"," dr"," drive",
             " ln"," lane"," blvd"," boulevard"," pkwy"," parkway"," way",
             " ct"," court"," cir"," circle"," hwy"," highway"," fwy",
             " freeway"," loop"," trail"," trl"," place"," pl"," plaza",
             " suite"," ste"," terrace"," ter"]
    low = " " + t.lower()
    return any(w in low for w in words)

def street_number(text):
    m = re.search(r"\b(\d{2,6})\b", str(text or ""))
    return m.group(1) if m else ""

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
    combined = (str(name) + " " + str(cat or "")).lower()
    for kw in EXCLUDE:
        if kw in combined: return False
    for sig in BIG_BIZ_SIGNALS:
        if sig in combined: return False
    if re.match(r"^[\d\s,.-]+$", str(name).strip()): return False
    return True

def is_bad_phone(phone, extra_bad=set()):
    if not phone: return False
    return phone in KNOWN_BAD_PHONES or phone in extra_bad


# ── SHEETS ─────────────────────────────────────────────────────────────
def connect_sheets():
    if not os.path.exists(CREDS_FILE):
        print("\nERROR: google_creds.json not found."); sys.exit(1)
    scopes = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"]
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    ss     = client.open_by_key(SHEET_ID)
    ready_ws  = get_or_create_tab(ss, READY_TAB,      READY_HEADERS)
    comm_ws   = get_or_create_tab(ss, COMMERCIAL_TAB, COMMERCIAL_HEADERS)
    green_ws  = get_or_create_tab(ss, GREEN_TAB,      GREEN_HEADERS, required=False)
    # All Leads tab is read-only — fiber scan writes it, we just read it
    try:    all_leads_ws = ss.worksheet(ALL_LEADS_TAB)
    except: all_leads_ws = None
    print("Connected to Google Sheets ✓")
    return ss, ready_ws, comm_ws, green_ws, all_leads_ws

def get_or_create_tab(ss, title, headers, required=True):
    try:
        ws = ss.worksheet(title)
    except gspread.exceptions.WorksheetNotFound:
        if not required: return None
        ws = ss.add_worksheet(title=title, rows=TAB_ROWS, cols=max(len(headers), 20))
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
        try: ws.resize(rows=max(len(vals)+2000, TAB_ROWS), cols=max(len(new_hdrs), 20))
        except: pass
        ws.update(range_name="A1:%s1" % col_letter(len(new_hdrs)), values=[new_hdrs])
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
    if not rows: return
    for attempt in range(3):
        try:
            ws.append_rows(rows, value_input_option="USER_ENTERED")
            time.sleep(0.5); return
        except Exception as e:
            print("  Append error attempt %d: %s" % (attempt+1, e)); time.sleep(5)

def batch_update_safe(ws, updates):
    if not updates: return
    for attempt in range(3):
        try:
            ws.batch_update(updates, value_input_option="USER_ENTERED")
            time.sleep(0.5); return
        except Exception as e:
            print("  Batch update error attempt %d: %s" % (attempt+1, e)); time.sleep(5)

def ensure_phone_cols(ws):
    """Make sure Phone, Phone Source, Phone Checked At columns exist."""
    vals = ws.get_all_values()
    if not vals: return header_map(ws)
    needed  = ["Phone", "Phone Source", "Phone Checked At"]
    headers = list(vals[0])
    existing = [h.lower().strip() for h in headers]
    changed = False
    for col in needed:
        if col.lower() not in existing:
            headers.append(col); existing.append(col.lower()); changed = True
    if changed:
        try: ws.resize(rows=max(len(vals)+2000, TAB_ROWS), cols=max(len(headers), 20))
        except: pass
        ws.update(range_name="A1:%s1" % col_letter(len(headers)), values=[headers])
        print("  Added phone columns to tab.")
    return header_map(ws)


# ── BROWSER ────────────────────────────────────────────────────────────
def init_browser(headless=False):
    global _pw, _browser, _page
    from playwright.sync_api import sync_playwright
    _pw      = sync_playwright().start()
    _browser = _pw.chromium.launch(
        headless=headless,
        args=["--disable-blink-features=AutomationControlled",
              "--no-sandbox","--disable-dev-shm-usage"])
    ctx = _browser.new_context(
        viewport={"width": 1366, "height": 768},
        user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"),
        locale="en-US")
    _page = ctx.new_page()
    _page.goto("https://www.google.com/maps", timeout=25000, wait_until="domcontentloaded")
    time.sleep(2)
    print("  Browser ready ✓")

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
    for sel in ["div.Nv2PK", "div[role='article']"]:
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
                if txt: return txt
                lbl = el.get_attribute("aria-label") or ""
                if lbl: return lbl.strip()
        except: pass
    return ""

def panel_name():
    global _page
    for sel in ["h1.DUwDvf","h1.fontHeadlineLarge","h1"]:
        try:
            el = _page.query_selector(sel)
            if el:
                txt = safe_text(el)
                if txt: return txt
        except: pass
    return ""

def panel_phone():
    global _page
    for sel in ["button[data-item-id^='phone']","button[aria-label^='Phone:']",
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
    for sel in ["button[data-item-id='address']","button[aria-label^='Address:']",
                "button[aria-label*='Address:']"]:
        try:
            for el in _page.query_selector_all(sel):
                label = el.get_attribute("aria-label") or ""
                txt   = safe_text(el)
                val   = (label + " " + txt).replace("Address:","").strip()
                if looks_like_address(val): return val
        except: pass
    return ""

def click_card_and_extract(card, expected_name="", expected_address=""):
    """
    Click a card, wait for its panel, extract phone+address.
    Only returns a phone if the panel CONFIRMS it matches the expected
    business name or address. No match = no phone saved.
    """
    global _page
    try: _page.keyboard.press("Escape"); time.sleep(0.3)
    except: pass

    cname = card_name(card) or expected_name
    try:
        card.click()
    except:
        try:
            link = card.query_selector("a.hfpxzc")
            if link: link.click()
            else: return None
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
            print("       SKIP — panel mismatch | card: %s | panel: %s" % (cname[:30], pname[:30]))
        pphone = ""

    return {
        "card_name": cname, "panel_name": pname,
        "phone": pphone, "address": paddr, "matched_by": matched_by,
    }


# ── FIBER SCAN ENRICHER ────────────────────────────────────────────────
def lookup_by_address(address, business_name="", city="", state="TX", zipc=""):
    """
    Search Maps for an address from the fiber scan.
    Click the matching business panel.
    Return phone only if address or name matches confirmed.
    """
    global _page
    if not address or not looks_like_address(address):
        print("       Skipping — not a real address: %s" % str(address)[:60])
        return None

    # Build clean tight query
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

        # Maps went straight to a single place panel
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
                "name": pname or business_name,
                "phone": pphone,
                "address": paddr or address,
                "matched_by": matched_by,
                "source": "Google Maps",
            }

        # Multiple results — try first 3 cards
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
        print("       Lookup error: %s" % e)
        return None

def enrich_tab(ws, tab_name, ready_ws, all_bad_phones, limit=None):
    """
    Read a tab from the fiber scan output.
    For every row with a real address but missing/bad phone:
      → search Maps, panel-match, get phone
      → update the row in place
      → add to Ready To Call with fiber status
    """
    if not ws:
        print("  Tab not found: %s — skipping" % tab_name); return 0

    hmap = ensure_phone_cols(ws)
    vals = ws.get_all_values()
    if not vals or len(vals) < 2: return 0

    # Detect any new repeated phones in this tab
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

    print("\n" + "=" * 60)
    print("  ENRICHING: %s" % tab_name)
    print("  Rows to fix: %d (missing or bad phone)" % len(rows_to_fix))
    if tab_bad - all_bad_phones:
        print("  Detected bad repeated phones: %s" % ", ".join(tab_bad - all_bad_phones))
    print("=" * 60)

    done = 0
    ready_batch = []

    for i, item in enumerate(rows_to_fix, start=1):
        print("\n  [%d/%d] Row %d | %s" % (i, len(rows_to_fix), item["row_num"], item["address"][:55]))
        if item["old_phone"]:
            print("       Replacing bad phone: %s" % item["old_phone"])

        found = lookup_by_address(
            item["address"], business_name=item["name"],
            city=item["city"], state=item["state"], zipc=item["zip"])

        if not found or not found.get("phone"):
            print("       No safe phone found"); continue

        new_phone = found["phone"]
        if is_bad_phone(new_phone, tab_bad):
            print("       Found phone is still bad, skipping: %s" % new_phone); continue

        print("       ✓ Phone: %s | matched by: %s" % (new_phone, found.get("matched_by","")))

        # Refresh hmap in case columns shifted
        hmap = header_map(ws)

        updates = []
        if "phone" in hmap:
            updates.append({"range": "%s%d" % (col_letter(hmap["phone"]), item["row_num"]),
                            "values": [[new_phone]]})
        if "phone source" in hmap:
            updates.append({"range": "%s%d" % (col_letter(hmap["phone source"]), item["row_num"]),
                            "values": [["Google Maps — panel confirmed"]]})
        if "phone checked at" in hmap:
            updates.append({"range": "%s%d" % (col_letter(hmap["phone checked at"]), item["row_num"]),
                            "values": [[now_str()]]})
        if updates:
            batch_update_safe(ws, updates)

        # Add to Ready To Call
        biz_name = found.get("name") or item["name"] or item["address"]
        ready_batch.append([
            biz_name, new_phone,
            found.get("address") or item["address"],
            item["city"], item["state"], item["zip"],
            item["fiber_status"],           # fiber status from scan
            "Fiber Scan Lead",
            tab_name,
            found.get("matched_by",""),
            now_str(),
        ])
        if len(ready_batch) >= BATCH_SIZE:
            append_rows_safe(ready_ws, ready_batch)
            ready_batch = []

        done += 1

    if ready_batch:
        append_rows_safe(ready_ws, ready_batch)

    print("\n  Done: %d phones added/fixed in %s" % (done, tab_name))
    return done


# ── ZIP SCRAPER ────────────────────────────────────────────────────────
def scrape_category(lat, lng, zipcode, city, state, category, max_cards=25):
    global _page
    query = "%s in %s" % (category, zipcode)
    url   = "https://www.google.com/maps/search/%s" % query.replace(" ", "+")
    results = []; seen = set(); phone_counter = Counter()

    try:
        _page.goto(url, timeout=25000, wait_until="domcontentloaded")
        time.sleep(MAP_DELAY)
        processed = 0; scroll_round = 0

        while processed < max_cards and scroll_round < 5:
            cards = get_cards()
            if not cards: break

            for card in cards[processed:]:
                if processed >= max_cards: break
                cname = card_name(card); processed += 1
                if not cname: continue
                if not is_small_biz(cname, category): continue
                nk = norm(cname)
                if nk in seen: continue
                seen.add(nk)

                print("    Opening: %s" % cname[:45])
                result = click_card_and_extract(card, expected_name=cname)
                if not result: continue

                pname = result["panel_name"] or cname
                phone = result["phone"]
                addr  = result["address"]

                if phone:
                    phone_counter[phone] += 1
                    if phone_counter[phone] >= 2 or is_bad_phone(phone):
                        print("       Repeated/bad phone, blanking: %s" % phone)
                        phone = ""

                print("       %s | %s" % (("✓ " + phone) if phone else "no safe phone", pname[:30]))

                results.append({
                    "name": pname, "phone": phone, "address": addr,
                    "category": category, "city": city, "state": state,
                    "zip": zipcode, "source": "Google Maps",
                    "matched_by": result["matched_by"],
                })

            try:
                feed = _page.query_selector("div[role='feed']")
                if feed: feed.evaluate("el => el.scrollBy(0, 1500)")
                else: _page.mouse.wheel(0, 1500)
            except: pass
            time.sleep(1.2); scroll_round += 1

    except Exception as e:
        print("    Category error: %s" % e)
    return results

def zip_to_bounds(zipcode):
    print("\n  Looking up ZIP %s..." % zipcode)
    r = requests.get("%s/search" % NOMINATIM,
        params={"postalcode": zipcode, "country": "US", "format": "json",
                "limit": 1, "addressdetails": 1},
        headers={"User-Agent": "TheMapMan/9.3"}, timeout=10)
    data = r.json()
    if not data: print("  ZIP not found."); sys.exit(1)
    d = data[0]; clat = float(d["lat"]); clng = float(d["lon"])
    a = d.get("address", {})
    city  = a.get("city") or a.get("town") or a.get("village") or a.get("county") or zipcode
    state = a.get("state", "TX")
    if state.lower() == "texas": state = "TX"
    if "boundingbox" in d:
        bb = d["boundingbox"]; pad = GRID_STEP
        south = float(bb[0])-pad; north = float(bb[1])+pad
        west  = float(bb[2])-pad; east  = float(bb[3])+pad
    else:
        pad = GRID_STEP*2
        south=clat-pad; north=clat+pad; west=clng-pad; east=clng+pad
    print("  ZIP %s -> %s, %s" % (zipcode, city, state))
    return clat, clng, south, west, north, east, city, state

def build_grid(south, west, north, east):
    grid = []; lat = south
    while lat <= north + 0.001:
        lng = west
        while lng <= east + 0.001:
            grid.append((round(lat,5), round(lng,5)))
            lng = round(lng+GRID_STEP, 5)
        lat = round(lat+GRID_STEP, 5)
    return grid

def run_zip(zipcode, ready_ws, comm_ws, limit=None):
    clat, clng, south, west, north, east, city, state = zip_to_bounds(zipcode)
    grid = build_grid(south, west, north, east)

    print("\n" + "=" * 60)
    print("  SCRAPING ZIP: %s  |  Grid: %d  |  Categories: %d" % (
        zipcode, len(grid), len(SEARCH_CATEGORIES)))
    print("  Safe phone mode ON — panel match required")
    print("=" * 60)

    ready_batch = []; comm_batch = []; seen = set(); checked = 0

    try:
        for gi, (lat, lng) in enumerate(grid, start=1):
            for category in SEARCH_CATEGORIES:
                checked += 1
                print("\n  Grid %d/%d | %s" % (gi, len(grid), category))
                businesses = scrape_category(lat, lng, zipcode, city, state, category)

                for biz in businesses:
                    name  = biz.get("name","")
                    phone = biz.get("phone","")
                    addr  = biz.get("address","")
                    if not name or not is_small_biz(name, biz.get("category","")): continue
                    key = norm(name) + "|" + norm(addr)
                    if key in seen: continue
                    seen.add(key)

                    comm_batch.append([
                        name, addr, phone, biz.get("category",""),
                        city, state, zipcode, "Commercial", "Google Maps",
                        "Google Maps panel confirmed" if phone else "No safe phone",
                        "Panel match required — safe mode", "The Map Man v9.3", now_str(),
                    ])
                    if phone:
                        ready_batch.append([
                            name, phone, addr, city, state, zipcode,
                            "", biz.get("category",""), "Google Maps ZIP Scrape",
                            biz.get("matched_by",""), now_str(),
                        ])

                if len(comm_batch) >= BATCH_SIZE:
                    append_rows_safe(comm_ws, comm_batch); comm_batch = []
                if len(ready_batch) >= BATCH_SIZE:
                    append_rows_safe(ready_ws, ready_batch)
                    print("  ✓ Saved %d to Ready To Call" % len(ready_batch))
                    ready_batch = []

                if limit and checked >= limit: raise KeyboardInterrupt

    except KeyboardInterrupt:
        print("\n  Stopping — saving what's done...")
    finally:
        if comm_batch:  append_rows_safe(comm_ws, comm_batch)
        if ready_batch: append_rows_safe(ready_ws, ready_batch)
    print("\nZIP scrape done.")


# ── MAIN ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="THE MAP MAN v%s" % VERSION)
    parser.add_argument("--zip",          type=str, default=None)
    parser.add_argument("--enrich-only",  action="store_true")
    parser.add_argument("--headless",     action="store_true")
    parser.add_argument("--limit",        type=int, default=None,
                        help="Max rows to enrich per tab (for testing)")
    args = parser.parse_args()

    print("\n" + "#" * 60)
    print("  THE MAP MAN v%s" % VERSION)
    print("  Safe phone: panel match required before any number is saved")
    print("  Fiber scan enricher: adds phones to All Leads / Green Commercial")
    print("  ZIP scraper: dense grid, home-biz categories, big chain blocked")
    print("#" * 60 + "\n")

    ss, ready_ws, comm_ws, green_ws, all_leads_ws = connect_sheets()
    init_browser(args.headless)

    try:
        # ── STEP 1: Enrich fiber scan output tabs ──────────────────────
        print("\n  STEP 1: Enriching fiber scan tabs with phone numbers...")

        # All Leads tab (main fiber scan output — read only, no phone column by default)
        # We enrich it by adding phone columns and updating in place
        if all_leads_ws:
            enrich_tab(all_leads_ws, ALL_LEADS_TAB, ready_ws,
                       KNOWN_BAD_PHONES, limit=args.limit)

        # Green Commercial (fiber-confirmed addresses — hottest leads)
        enrich_tab(green_ws, GREEN_TAB, ready_ws,
                   KNOWN_BAD_PHONES, limit=args.limit)

        # Commercial tab (any already-collected leads missing phones)
        enrich_tab(comm_ws, COMMERCIAL_TAB, ready_ws,
                   KNOWN_BAD_PHONES, limit=args.limit)

        if args.enrich_only:
            print("\n  Enrich-only mode — done.")
            return

        # ── STEP 2: Scrape new businesses from ZIP ─────────────────────
        zipcode = args.zip or input("\n  Enter ZIP code to scrape: ").strip()
        if not re.match(r"^\d{5}$", zipcode):
            print("  Invalid ZIP."); sys.exit(1)

        print("\n  STEP 2: Scraping ZIP %s for new small businesses..." % zipcode)
        run_zip(zipcode, ready_ws, comm_ws, limit=args.limit)

    finally:
        close_browser()


if __name__ == "__main__":
    main()
