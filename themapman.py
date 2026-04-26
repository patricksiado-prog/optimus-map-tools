"""
THE MAP MAN v7.1
================
Combined Map Man + Address Man in one program.
Finds small businesses in a ZIP code.
Gets phone numbers from Google Maps.
Writes a clean "Ready To Call" tab you can dial directly from.
Also enriches your existing Green Commercial leads with phone numbers.
Auto-updates from GitHub on every run.

FIXED in v7.1:
- TAB_ROWS changed from 50000 to 1000 to avoid Google Sheets 10,000,000-cell limit.
- get_or_create_tab() creates small tabs and lets Google Sheets grow naturally.

READY TO CALL tab columns:
  Business Name | Phone | Address | City | ZIP |
  Fiber Status | Pitch | Category | Found By | Added

INSTALL one time:
  python -m pip install requests gspread google-auth playwright
  python -m playwright install chromium

RUN:
  python themapman.py --zip 77003
  python themapman.py --zip 77002
  python themapman.py --enrich-only
  python themapman.py --headless
"""

import os, sys, re, json, time, argparse, random, hashlib, math
from datetime import datetime
import requests, gspread
from google.oauth2.service_account import Credentials

# ── AUTO UPDATE ───────────────────────────────────────────────────────
VERSION       = "7.1"
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
            print("  GitHub unreachable — running v%s" % VERSION)
            return
        latest = r.text
        with open(os.path.abspath(__file__), "r", encoding="utf-8") as f:
            current = f.read()
        if hashlib.md5(latest.encode()).hexdigest() == hashlib.md5(current.encode()).hexdigest():
            print("  Up to date (v%s)" % VERSION)
            return
        m = re.search(r'^VERSION\s*=\s*["\'](.+?)["\']', latest, re.MULTILINE)
        print("  Updating to v%s..." % (m.group(1) if m else "?"))
        with open(os.path.abspath(__file__), "w", encoding="utf-8") as f:
            f.write(latest)
        print("  Updated! Restarting...")
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print("  Update check failed: %s" % e)

check_update()

# ── CONFIG ────────────────────────────────────────────────────────────
CREDS_FILE    = "google_creds.json"
SHEET_ID      = "15ymTkIGPWs6quB035l414ns5hkG9cQ5xr_W4ukd0OAA"
PROGRESS_FILE = "mapman_progress.json"

# IMPORTANT FIX:
# Do NOT pre-create huge 50,000-row tabs. Google Sheets has a 10M-cell limit.
# Start small. append_rows() will add rows as needed.
TAB_ROWS      = 1000

READY_TAB      = "Ready To Call"
COMMERCIAL_TAB = "Commercial"
ALL_BIZ_TAB    = "All Biz Phones"

READY_HEADERS = [
    "Business Name", "Phone", "Address", "City", "State", "ZIP",
    "Fiber Status", "Pitch", "Category", "Source", "Added At",
]

COMMERCIAL_HEADERS = [
    "Business Name", "Address", "Phone", "Category", "City", "State", "ZIP",
    "Lead Type", "Data Source", "Phone Source", "Fiber Validation Status",
    "Fiber Validation Method", "Pitch Type", "Notes", "Found By", "Added At",
]

ALL_BIZ_HEADERS = [
    "Business Name", "Address", "Phone", "Category", "City", "State", "ZIP",
    "Lead Type", "Data Source", "Phone Source", "Fiber Validation Status",
    "Fiber Validation Method", "Pitch Type", "Notes", "Source ZIP", "Found By", "Added At",
]

NOMINATIM    = "https://nominatim.openstreetmap.org"
OSM_OVERPASS = "https://overpass-api.de/api/interpreter"
ATT_API_URL  = (
    "https://www.att.com/services/shop/model/ecom/shop/view/unified/"
    "qualification/service/CheckAvailabilityRESTService/invokeCheckAvailability"
)
ATT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
    "Origin": "https://www.att.com",
    "Referer": "https://www.att.com/internet/availability/",
}

OSM_DELAY  = 1.0
MAP_DELAY  = 2.2
ATT_DELAY  = 2.0
JITTER     = 0.5
BATCH_SIZE = 20
GRID_STEP  = 0.03
RADIUS     = 600

SEARCH_CATEGORIES = [
    "small businesses","restaurants","auto repair shops","hair salons","nail salons",
    "dentists","insurance offices","real estate offices","gyms fitness","retail stores",
    "law offices","accounting tax offices","daycare centers","pharmacies",
    "veterinary clinics","massage spa","printing shops","florists","dry cleaners",
    "contractors plumbers electricians","mechanics","body shops","tire shops",
    "barber shops","beauty salons","medical offices","chiropractors",
    "physical therapy","orthodontists","optometrists","pet groomers",
    "coffee shops","bakeries","bars","food trucks","catering",
    "marketing agencies","web design","IT services","security companies",
    "moving companies","cleaning services","pest control","landscapers",
    "roofing contractors","painting contractors","flooring stores",
    "jewelry stores","clothing stores","shoe stores","gift shops",
    "electronics repair","phone repair","computer repair","appliance repair",
    "locksmith","towing companies","car wash","detail shops",
    "tattoo shops","lash studios","waxing salons","med spas",
    "staffing agencies","financial advisors","mortgage brokers","title companies",
    "event venues","photographers","videographers","party rentals",
    "tutoring centers","music lessons","martial arts","yoga studios","boxing gyms",
    "laundromats","alterations","shoe repair","pawn shops","smoke shops",
    "machine shops","welding shops","cabinet makers","sign shops",
    "trucking companies","courier services","warehouses","self storage",
    "churches","nonprofits","funeral homes",
]

EXCLUDE = [
    "walmart","target","costco","home depot","lowes","lowe's","best buy",
    "kroger","heb ","h-e-b","publix","safeway","albertsons","aldi","whole foods",
    "sam's club","mcdonald","burger king","taco bell","wendy","chick-fil","subway",
    "starbucks","dunkin","domino","pizza hut","papa john","popeyes","kfc",
    "whataburger","sonic drive","dairy queen","chase bank","wells fargo",
    "bank of america","citibank","us bank","td bank","pnc bank","capital one",
    "regions bank","frost bank","walgreens","cvs","rite aid","dollar general",
    "dollar tree","family dollar","7-eleven","circle k","wawa","shell","chevron",
    "exxon","valero","texaco","marriott","hilton","hyatt","holiday inn","sheraton",
    "hampton inn","la quinta","motel 6","comfort inn","best western",
    "fedex office","ups store","post office","usps","city hall","county ",
    "courthouse","dmv ","social security","fire station","police station",
    "sheriff","jail","prison","government","municipal","public works",
    "university","college","school district"," isd","high school","middle school",
    "elementary","community college","academy","hospital","medical center",
    "health system","children's hospital","memorial hermann","methodist hospital",
    "warehouse","distribution center","fulfillment","manufacturing plant",
    "amazon","google office","microsoft","apple store",
]

# ── HELPERS ───────────────────────────────────────────────────────────
def norm(s):
    if not s:
        return ""
    s = re.sub(r"[^\w\s]", " ", str(s).lower().strip())
    return re.sub(r"\s+", " ", s).strip()

def col_letter(n):
    out = ""
    while n:
        n, rem = divmod(n - 1, 26)
        out = chr(65 + rem) + out
    return out

def clean_phone(phone):
    if not phone:
        return ""
    phone = str(phone).strip()
    for rm in ["Phone:", "Call phone number", "tel:"]:
        phone = phone.replace(rm, "")
    phone = phone.strip()
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) == 10:
        return "(%s) %s-%s" % (digits[:3], digits[3:6], digits[6:])
    return phone

def extract_phone(text):
    if not text:
        return ""
    for p in [r"\(?\b\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", r"\b1[-.\s]\d{3}[-.\s]\d{3}[-.\s]\d{4}\b"]:
        m = re.search(p, text)
        if m:
            return clean_phone(m.group(0))
    return ""

def is_small_biz(name, cat=""):
    if not name or len(str(name).strip()) < 3:
        return False
    combined = (str(name) + " " + str(cat or "")).lower()
    for kw in EXCLUDE:
        if kw in combined:
            return False
    return True

def looks_like_address(text):
    if not text:
        return False
    t = str(text).strip()
    if re.match(r"^-?\d+\.\d+,\s*-?\d+\.\d+$", t):
        return False
    sw = [" st", " street", " rd", " road", " ave", " avenue", " dr", " drive", " ln", " lane", " blvd", " boulevard", " pkwy", " parkway", " way", " ct", " court", " hwy", " highway", " loop", " fwy", " freeway", " trail", " trl", " place", " pl", " suite", " ste", " park", " plaza"]
    tl = " " + t.lower()
    return bool(re.search(r"\d{2,}", t)) and any(w in tl for w in sw)

def address_key(addr):
    a = norm(addr)
    a = re.sub(r"\bste\b|\bsuite\b|\bunit\b|\bapt\b", "", a)
    return re.sub(r"\s+", " ", a).strip()

def same_address(a, b):
    if not a or not b:
        return False
    ak, bk = address_key(a), address_key(b)
    if ak == bk:
        return True
    anum = re.findall(r"\b\d{2,6}\b", ak)
    bnum = re.findall(r"\b\d{2,6}\b", bk)
    if not anum or not bnum or anum[0] != bnum[0]:
        return False
    return len(set(ak.split()) & set(bk.split())) >= 3

def haversine(la1, ln1, la2, ln2):
    R = 6371000
    p1, p2 = math.radians(la1), math.radians(la2)
    a = (math.sin(math.radians(la2 - la1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(ln2 - ln1) / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def pitch_type(att_status):
    if att_status == "FIBER":
        return "ATT FIBER"
    if att_status == "COPPER":
        return "ATT UPGRADE"
    return "ATT INTERNET AIR"

# ── SHEETS ────────────────────────────────────────────────────────────
def connect_sheets():
    if not os.path.exists(CREDS_FILE):
        print("\nERROR: %s not found.\nPut google_creds.json in the same folder as themapman.py" % CREDS_FILE)
        sys.exit(1)
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    ss = client.open_by_key(SHEET_ID)
    ready_ws = get_or_create_tab(ss, READY_TAB, READY_HEADERS)
    comm_ws = get_or_create_tab(ss, COMMERCIAL_TAB, COMMERCIAL_HEADERS)
    allbiz_ws = get_or_create_tab(ss, ALL_BIZ_TAB, ALL_BIZ_HEADERS)
    print("Connected to Google Sheets ✓")
    return ss, ready_ws, comm_ws, allbiz_ws

def get_or_create_tab(ss, title, headers):
    try:
        ws = ss.worksheet(title)
    except gspread.exceptions.WorksheetNotFound:
        # FIX: create a small starting tab to avoid Google Sheets 10M-cell limit.
        # Google Sheets will grow automatically when append_rows() is used.
        ws = ss.add_worksheet(title=title, rows=TAB_ROWS, cols=len(headers))
        ws.update(range_name="A1", values=[headers])
        print("  Created tab: %s" % title)
        return ws

    vals = ws.get_all_values()
    if not vals:
        ws.update(range_name="A1", values=[headers])
        return ws

    existing_headers = vals[0]
    lower = [h.lower().strip() for h in existing_headers]
    new_headers = list(existing_headers)
    changed = False

    for h in headers:
        if h.lower() not in lower:
            new_headers.append(h)
            lower.append(h.lower())
            changed = True

    if changed:
        ws.update(range_name="A1:%s1" % col_letter(len(new_headers)), values=[new_headers])
        print("  Updated columns in: %s" % title)

    return ws

def load_ready_seen(ws):
    seen = set()
    try:
        vals = ws.get_all_values()
        for row in vals[1:]:
            if row and row[0]:
                seen.add(norm(row[0]))
            if len(row) > 1 and row[1]:
                seen.add("PHONE|" + norm(row[1]))
            if len(row) > 2 and row[2]:
                seen.add("ADDR|" + norm(row[2]))
    except Exception:
        pass
    print("  Ready To Call: %d existing" % len(seen))
    return seen

def load_commercial_rows(ws):
    vals = ws.get_all_values()
    if not vals:
        return [], {}, set()
    headers = [h.lower().strip() for h in vals[0]]
    rows = []
    seen = set()
    for row_num, row in enumerate(vals[1:], start=2):
        d = {h: (row[i].strip() if len(row) > i else "") for i, h in enumerate(headers)}
        d["_row_num"] = row_num
        rows.append(d)
        name = d.get("business name", "")
        addr = d.get("address", "")
        phone = d.get("phone", "")
        if name or addr:
            seen.add(norm(name) + "|" + address_key(addr))
        if name:
            seen.add("NAME|" + norm(name))
        if addr:
            seen.add("ADDR|" + address_key(addr))
        if phone:
            seen.add("PHONE|" + norm(phone))
    return rows, {h: i for i, h in enumerate(headers)}, seen

def load_allbiz_seen(ws):
    seen = set()
    try:
        vals = ws.get_all_values()
        if not vals:
            return seen
        hdrs = [h.lower().strip() for h in vals[0]]
        ni = hdrs.index("business name") if "business name" in hdrs else 0
        ai = hdrs.index("address") if "address" in hdrs else 1
        pi = hdrs.index("phone") if "phone" in hdrs else 2
        for row in vals[1:]:
            name = row[ni].strip() if len(row) > ni else ""
            addr = row[ai].strip() if len(row) > ai else ""
            phone = row[pi].strip() if len(row) > pi else ""
            if name or addr:
                seen.add(norm(name) + "|" + address_key(addr))
            if name:
                seen.add("NAME|" + norm(name))
            if phone:
                seen.add("PHONE|" + norm(phone))
    except Exception:
        pass
    return seen

def load_green_commercial(ss):
    leads = []
    try:
        ws = ss.worksheet("Green Commercial")
        rows = ws.get_all_values()
        if not rows:
            return leads
        hdrs = [h.lower().strip() for h in rows[0]]
        for row_num, row in enumerate(rows[1:], start=2):
            d = dict(zip(hdrs, row))
            addr = d.get("address", "").strip()
            name = d.get("business name", "").strip()
            city = d.get("city", "").strip()
            state = d.get("state", "TX").strip()
            zipc = d.get("zip", "").strip()
            lat = d.get("lat", "").strip()
            lng = d.get("lng", "").strip()
            if not addr or "(no number)" in addr.lower():
                continue
            leads.append({"address": addr, "name": name, "city": city, "state": state, "zip": zipc, "lat": lat, "lng": lng, "row_num": row_num, "source": "Green Commercial"})
    except Exception as e:
        print("  Warning reading Green Commercial: %s" % e)
    print("  Green Commercial leads to enrich: %d" % len(leads))
    return leads

def append_rows_safe(ws, rows):
    if not rows:
        return True
    for attempt in range(3):
        try:
            ws.append_rows(rows, value_input_option="USER_ENTERED")
            time.sleep(0.4)
            return True
        except Exception as e:
            print("  Append error attempt %d: %s" % (attempt + 1, e))
            time.sleep(5)
    return False

def batch_update_safe(ws, updates):
    if not updates:
        return True
    for attempt in range(3):
        try:
            ws.batch_update(updates, value_input_option="USER_ENTERED")
            time.sleep(0.4)
            return True
        except Exception as e:
            print("  Update error attempt %d: %s" % (attempt + 1, e))
            time.sleep(5)
    return False

def load_progress(zipcode):
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                p = json.load(f)
            if p.get("zip") == zipcode:
                return p
        except Exception:
            pass
    return {"zip": zipcode, "grid_idx": 0, "cat_idx": 0, "total": 0}

def save_progress(p):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(p, f, indent=2)

# ── ZIP / GRID ─────────────────────────────────────────────────────────
def zip_to_bounds(zipcode):
    print("\n  Looking up ZIP %s..." % zipcode)
    try:
        r = requests.get(
            "%s/search" % NOMINATIM,
            params={"postalcode": zipcode, "country": "US", "format": "json", "limit": 1, "addressdetails": 1},
            headers={"User-Agent": "TheMapMan/7.1"},
            timeout=10,
        )
        data = r.json()
        if not data:
            print("  ZIP %s not found." % zipcode)
            sys.exit(1)
        d = data[0]
        clat = float(d["lat"])
        clng = float(d["lon"])
        a = d.get("address", {})
        city = a.get("city") or a.get("town") or a.get("village") or a.get("county") or zipcode
        state = a.get("state", "TX")
        if state.lower() == "texas":
            state = "TX"
        if "boundingbox" in d:
            bb = d["boundingbox"]
            pad = GRID_STEP
            south = float(bb[0]) - pad
            north = float(bb[1]) + pad
            west = float(bb[2]) - pad
            east = float(bb[3]) + pad
        else:
            pad = GRID_STEP * 3
            south = clat - pad
            north = clat + pad
            west = clng - pad
            east = clng + pad
        print("  ZIP %s -> %s, %s" % (zipcode, city, state))
        return clat, clng, south, west, north, east, city, state
    except Exception as e:
        print("  ZIP lookup failed: %s" % e)
        sys.exit(1)

def build_grid(south, west, north, east):
    grid = []
    lat = south
    while lat <= north + 0.001:
        lng = west
        while lng <= east + 0.001:
            grid.append((round(lat, 5), round(lng, 5)))
            lng = round(lng + GRID_STEP, 5)
        lat = round(lat + GRID_STEP, 5)
    return grid

# ── AT&T CHECK ────────────────────────────────────────────────────────
def check_att(address, zipc):
    addr = re.sub(r',?\s+[A-Z]{2}\s+\d{5}.*$', '', address.strip())
    addr = re.sub(r',?\s+\d{5}.*$', '', addr).strip()
    payload = {"userInputZip": zipc or "", "userInputAddressLine1": addr, "mode": "fullAddress", "customer_type": "Consumer", "dtvMigrationFlag": False}
    try:
        time.sleep(ATT_DELAY + random.uniform(-JITTER / 2, JITTER))
        r = requests.post(ATT_API_URL, data=json.dumps(payload), headers=ATT_HEADERS, timeout=10)
        if r.status_code == 429:
            print("    Rate limited — waiting 30s")
            time.sleep(30)
            r = requests.post(ATT_API_URL, data=json.dumps(payload), headers=ATT_HEADERS, timeout=10)
        if r.status_code != 200:
            return "UNKNOWN", ""
        p = r.json().get("profile", {})
        spd = str(p.get("maxAvailableSpeed", "") or p.get("maxDnldSpeed", "") or "")
        if p.get("isGIGAFiberAvailable") or p.get("isFiberAvailable"):
            return "FIBER", spd
        if p.get("isIPBBAvailable") or p.get("isDSLAvailable"):
            return "COPPER", spd
        return "NONE", ""
    except Exception:
        return "UNKNOWN", ""

# ── OSM ───────────────────────────────────────────────────────────────
def osm_nearby(lat, lng, radius=RADIUS):
    results = []
    seen = set()
    query = """
[out:json][timeout:30];
(
  node(around:{r},{lat},{lng})[shop];
  node(around:{r},{lat},{lng})[office];
  node(around:{r},{lat},{lng})[craft];
  node(around:{r},{lat},{lng})[healthcare];
  node(around:{r},{lat},{lng})[amenity~"restaurant|cafe|bar|pharmacy|clinic|dentist|doctors|beauty|hairdresser|barber|gym|car_repair|car_wash|fast_food|veterinary|optician|massage|laundry|bakery|insurance"];
  way(around:{r},{lat},{lng})[shop];
  way(around:{r},{lat},{lng})[office];
  way(around:{r},{lat},{lng})[craft];
  way(around:{r},{lat},{lng})[healthcare];
);
out center tags;
""".format(r=radius, lat=lat, lng=lng)
    try:
        time.sleep(OSM_DELAY + random.uniform(0, JITTER))
        r = requests.post(OSM_OVERPASS, data={"data": query}, headers={"User-Agent": "TheMapMan/7.1"}, timeout=30)
        if r.status_code != 200:
            return results
        for el in r.json().get("elements", []):
            tags = el.get("tags", {})
            name = tags.get("name", "").strip()
            cat = tags.get("shop") or tags.get("office") or tags.get("amenity") or tags.get("craft") or tags.get("healthcare") or "business"
            if not is_small_biz(name, cat):
                continue
            oid = "%s_%s" % (el.get("type", ""), el.get("id", ""))
            if oid in seen:
                continue
            seen.add(oid)
            phone = clean_phone(tags.get("phone", "") or tags.get("contact:phone", "") or tags.get("telephone", ""))
            house = tags.get("addr:housenumber", "")
            street = tags.get("addr:street", "")
            addr = ("%s %s" % (house, street)).strip() if house and street else ""
            state = tags.get("addr:state", "TX")
            if state.lower() == "texas":
                state = "TX"
            elat = (el.get("center", {}).get("lat") if el["type"] == "way" else el.get("lat"))
            elng = (el.get("center", {}).get("lon") if el["type"] == "way" else el.get("lon"))
            results.append({"name": name, "address": addr, "phone": phone, "category": cat, "city": tags.get("addr:city", ""), "state": state, "zip": tags.get("addr:postcode", ""), "lat": elat, "lng": elng, "found_by": "OpenStreetMap", "phone_source": "OpenStreetMap" if phone else "No phone found"})
    except Exception as e:
        print("    OSM error: %s" % e)
    return results

# ── BROWSER ───────────────────────────────────────────────────────────
_pw = _browser = _page = None

def init_browser(headless=False):
    global _pw, _browser, _page
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        print("\n  PLAYWRIGHT NOT FOUND.\n  Run: python -m pip install playwright\n  Then: python -m playwright install chromium")
        raise
    _pw = sync_playwright().start()
    _browser = _pw.chromium.launch(headless=headless, args=["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-dev-shm-usage"])
    ctx = _browser.new_context(viewport={"width": 1366, "height": 768}, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", locale="en-US")
    _page = ctx.new_page()
    _page.goto("https://www.google.com/maps", timeout=20000, wait_until="domcontentloaded")
    time.sleep(2)
    try:
        for sel in ["button[aria-label*='Accept all']", "button[aria-label*='Accept']", "button:has-text('Accept all')"]:
            btn = _page.query_selector(sel)
            if btn:
                btn.click()
                time.sleep(1)
                break
    except Exception:
        pass
    print("  Browser ready ✓")

def close_browser():
    global _browser, _pw
    try:
        if _browser:
            _browser.close()
        if _pw:
            _pw.stop()
    except Exception:
        pass

def text_safe(el):
    try:
        return el.inner_text().strip()
    except Exception:
        return ""

def extract_phone_from_page():
    global _page
    for sel in ["button[data-item-id^='phone']", "button[aria-label^='Phone:']", "button[aria-label*='Phone']", "div[aria-label^='Phone:']"]:
        try:
            for el in _page.query_selector_all(sel):
                label = el.get_attribute("aria-label") or ""
                txt = text_safe(el)
                phone = extract_phone(label + " " + txt)
                if phone:
                    return phone
        except Exception:
            pass
    try:
        body_text = _page.inner_text("body")
        phone = extract_phone(body_text)
        if phone:
            return phone
    except Exception:
        pass
    return ""

def extract_address_from_page():
    global _page
    for sel in ["button[data-item-id='address']", "button[aria-label^='Address:']", "button[aria-label*='Address']"]:
        try:
            for el in _page.query_selector_all(sel):
                label = el.get_attribute("aria-label") or ""
                txt = text_safe(el)
                val = (label + " " + txt).replace("Address:", "").strip()
                if looks_like_address(val):
                    return val
        except Exception:
            pass
    return ""

def gmaps_search(lat, lng, category, zipcode, city="", state="TX"):
    global _page
    results = []
    seen = set()
    if not _page:
        return results
    try:
        q = "%s in %s" % (category, zipcode)
        url = "https://www.google.com/maps/search/%s/@%.5f,%.5f,14z" % (q.replace(" ", "+"), lat, lng)
        _page.goto(url, timeout=20000, wait_until="domcontentloaded")
        time.sleep(MAP_DELAY)
        for _ in range(4):
            cards = _page.query_selector_all("div.Nv2PK")
            for card in cards:
                try:
                    ne = card.query_selector("div.fontHeadlineSmall,div.qBF1Pd")
                    if not ne:
                        continue
                    name = ne.inner_text().strip()
                    if not name:
                        continue
                    card_text = text_safe(card)
                    cat_guess = category
                    cat_el = card.query_selector("div.W4Efsd span.fontBodyMedium")
                    if cat_el:
                        ct = cat_el.inner_text().strip()
                        if ct:
                            cat_guess = ct
                    if not is_small_biz(name, cat_guess):
                        continue
                    nk = norm(name)
                    if nk in seen:
                        continue
                    seen.add(nk)
                    addr = ""
                    phone = extract_phone(card_text)
                    for el in card.query_selector_all("div.W4Efsd span"):
                        txt = el.inner_text().strip()
                        if looks_like_address(txt):
                            addr = txt
                            break
                    try:
                        card.click()
                        time.sleep(1.8)
                        dp = extract_phone_from_page()
                        da = extract_address_from_page()
                        if dp:
                            phone = dp
                        if da:
                            addr = da
                    except Exception:
                        pass
                    results.append({"name": name, "address": addr, "phone": clean_phone(phone), "category": cat_guess, "city": city, "state": state, "zip": zipcode, "lat": lat, "lng": lng, "found_by": "Google Maps", "phone_source": "Google Maps" if phone else "No phone found"})
                except Exception:
                    continue
            try:
                feed = _page.query_selector("div[role='feed']")
                if feed:
                    feed.evaluate("el => el.scrollBy(0,1000)")
                else:
                    _page.mouse.wheel(0, 1000)
            except Exception:
                pass
            time.sleep(1.0)
            if len(results) >= 25:
                break
    except Exception as e:
        print("    Maps error: %s" % e)
    return results

def google_lookup_phone(name, address, city="", state="TX", zipc=""):
    global _page
    if not _page:
        return "", ""
    q = "%s %s %s %s phone" % (name, address, city, zipc)
    try:
        url = "https://www.google.com/maps/search/%s" % q.replace(" ", "+")
        _page.goto(url, timeout=20000, wait_until="domcontentloaded")
        time.sleep(2.5)
        phone = extract_phone_from_page()
        addr = extract_address_from_page()
        if not phone:
            try:
                body_text = _page.inner_text("body")
                phone = extract_phone(body_text)
            except Exception:
                pass
        return clean_phone(phone), addr
    except Exception:
        return "", ""

# ── ROW BUILDERS ──────────────────────────────────────────────────────
def make_ready_row(biz, att_status, zipcode, city, state):
    now = datetime.now().strftime("%m/%d/%Y %I:%M %p")
    return [
        biz.get("name", ""), biz.get("phone", ""), biz.get("address", ""),
        biz.get("city", "") or city, biz.get("state", "") or state, biz.get("zip", "") or zipcode,
        att_status, pitch_type(att_status), biz.get("category", ""),
        biz.get("found_by", ""), now,
    ]

def make_commercial_row(biz, zipcode, city, state):
    now = datetime.now().strftime("%m/%d/%Y %I:%M %p")
    return [biz.get("name", ""), biz.get("address", ""), biz.get("phone", ""), biz.get("category", ""), biz.get("city", "") or city, biz.get("state", "") or state, biz.get("zip", "") or zipcode, "Commercial", biz.get("found_by", ""), biz.get("phone_source", "No phone found"), "NOT FIBER VALIDATED", "Not checked with AT&T", "NEEDS FIBER VALIDATION", "Small business lead. Fiber availability not confirmed.", biz.get("found_by", ""), now]

def make_allbiz_row(biz, zipcode, city, state):
    now = datetime.now().strftime("%m/%d/%Y %I:%M %p")
    return [biz.get("name", ""), biz.get("address", ""), biz.get("phone", ""), biz.get("category", ""), biz.get("city", "") or city, biz.get("state", "") or state, biz.get("zip", "") or zipcode, "Commercial", biz.get("found_by", ""), biz.get("phone_source", "No phone found"), "NOT FIBER VALIDATED", "Not checked with AT&T", "NEEDS FIBER VALIDATION", "Small business lead.", zipcode, biz.get("found_by", ""), now]

# ── ENRICH GREEN COMMERCIAL ───────────────────────────────────────────
def enrich_green_commercial(ss, ready_ws, ready_seen, headless=False):
    print("\n" + "=" * 60)
    print("  ENRICHING GREEN COMMERCIAL (fiber confirmed businesses)")
    print("  These are your hottest leads — fiber is confirmed here")
    print("=" * 60)

    leads = load_green_commercial(ss)
    if not leads:
        print("  No Green Commercial leads found — run fiber_scan.py first")
        return 0

    try:
        init_browser(headless)
        use_browser = True
    except Exception:
        print("  Browser unavailable — skipping phone lookup")
        use_browser = False

    ready_batch = []
    done = 0
    now = datetime.now().strftime("%m/%d/%Y %I:%M %p")

    try:
        for i, lead in enumerate(leads):
            name = lead["name"]
            addr = lead["address"]
            city = lead["city"]
            state = lead["state"]
            zipc = lead["zip"]
            print("\n  [%d/%d] %s" % (i + 1, len(leads), addr[:55]))
            phone = ""
            if use_browser:
                phone, detail_addr = google_lookup_phone(name, addr, city, state, zipc)
                if detail_addr and not addr:
                    addr = detail_addr
            if phone:
                print("       Phone: %s" % phone)
            else:
                print("       No phone found")
            name_key = norm(name)
            phone_key = "PHONE|" + norm(phone)
            if name_key in ready_seen and phone and phone_key in ready_seen:
                print("       Already in Ready To Call — skip")
                continue
            att_status, att_speed = check_att(addr, zipc) if addr and zipc else ("FIBER", "")
            ptype = pitch_type(att_status)
            s_icon = "✅" if att_status == "FIBER" else ("🔶" if att_status == "COPPER" else "📡")
            print("       %s %s | phone: %s" % (s_icon, ptype, phone or "none"))
            row = [name, phone, addr, city, state, zipc, att_status, ptype, "Commercial (Fiber Confirmed)", "Green Commercial", now]
            ready_batch.append(row)
            ready_seen.add(name_key)
            if phone:
                ready_seen.add(phone_key)
            done += 1
            if len(ready_batch) >= BATCH_SIZE:
                append_rows_safe(ready_ws, ready_batch)
                ready_batch = []
                now = datetime.now().strftime("%m/%d/%Y %I:%M %p")
                print("  Saved %d to Ready To Call ✓" % done)
    except KeyboardInterrupt:
        print("\n  Paused.")
    finally:
        if ready_batch:
            append_rows_safe(ready_ws, ready_batch)
        if use_browser:
            close_browser()

    print("\n  Green Commercial enriched: %d leads added to Ready To Call" % done)
    return done

# ── MAIN SCRAPE ───────────────────────────────────────────────────────
def run(zipcode, ss, ready_ws, comm_ws, allbiz_ws, headless):
    clat, clng, south, west, north, east, city, state = zip_to_bounds(zipcode)
    grid = build_grid(south, west, north, east)
    prog = load_progress(zipcode)

    print("\n" + "=" * 60)
    print("  THE MAP MAN v%s — ZIP %s" % (VERSION, zipcode))
    print("  City: %s, %s" % (city, state))
    print("  Grid: %d squares | Categories: %d" % (len(grid), len(SEARCH_CATEGORIES)))
    print("  Writes to: Ready To Call + Commercial + All Biz Phones")
    print("  Ctrl+C to pause — resumes next run")
    print("=" * 60 + "\n")

    if prog.get("grid_idx", 0) > 0:
        print("  Previous run found — resuming at grid %d/%d" % (prog["grid_idx"] + 1, len(grid)))
        if input("  Resume? (y/n, default y): ").strip().lower() == "n":
            prog = {"zip": zipcode, "grid_idx": 0, "cat_idx": 0, "total": 0}
            save_progress(prog)

    try:
        init_browser(headless)
        use_gmaps = True
    except Exception as e:
        print("  Browser unavailable (%s) — OSM only" % e)
        use_gmaps = False

    ready_seen = load_ready_seen(ready_ws)
    comm_rows, comm_header_map, comm_seen = load_commercial_rows(comm_ws)
    allbiz_seen = load_allbiz_seen(allbiz_ws)

    ready_batch = []
    comm_append = []
    allbiz_append = []
    total_found = 0
    total_ready = 0
    phones_found = 0

    try:
        for gi in range(prog.get("grid_idx", 0), len(grid)):
            lat, lng = grid[gi]
            cat_start = prog.get("cat_idx", 0) if gi == prog.get("grid_idx", 0) else 0
            for ci in range(cat_start, len(SEARCH_CATEGORIES)):
                cat = SEARCH_CATEGORIES[ci]
                prog.update({"zip": zipcode, "grid_idx": gi, "cat_idx": ci, "total": total_ready})
                save_progress(prog)
                print("\n  [%d/%d] %.4f_%.4f | %s" % (gi + 1, len(grid), lat, lng, cat))
                osm = osm_nearby(lat, lng, radius=RADIUS)
                gm = gmaps_search(lat, lng, cat, zipcode, city, state) if use_gmaps else []
                combined = list(osm)
                known = {norm(b.get("name", "")) for b in combined}
                for b in gm:
                    if norm(b.get("name", "")) not in known:
                        combined.append(b)
                        known.add(norm(b.get("name", "")))
                print("  Found %d small businesses" % len(combined))
                total_found += len(combined)

                for biz in combined:
                    name = biz.get("name", "").strip()
                    addr = biz.get("address", "").strip()
                    phone = clean_phone(biz.get("phone", ""))
                    biz["phone"] = phone
                    if not name or not is_small_biz(name, biz.get("category", "")):
                        continue
                    if phone:
                        phones_found += 1
                    key = norm(name) + "|" + address_key(addr)
                    name_key = "NAME|" + norm(name)
                    addr_key = "ADDR|" + address_key(addr)
                    biz_zip = biz.get("zip", "") or zipcode
                    biz_city = biz.get("city", "") or city
                    biz_state = biz.get("state", "TX") or state

                    if addr and biz_zip:
                        att_status, att_speed = check_att(addr, biz_zip)
                    else:
                        att_status, att_speed = "NOT CHECKED", ""

                    ptype = pitch_type(att_status) if att_status not in ("NOT CHECKED", "UNKNOWN") else "NEEDS VALIDATION"
                    s_icon = "✅" if att_status == "FIBER" else ("🔶" if att_status == "COPPER" else "📡")
                    print("  %s %-32s | %-14s | %s" % (s_icon, name[:32], phone or "no phone", ptype))

                    if phone and norm(name) not in ready_seen:
                        ready_batch.append(make_ready_row(biz, att_status, zipcode, biz_city, biz_state))
                        ready_seen.add(norm(name))
                        if phone:
                            ready_seen.add("PHONE|" + norm(phone))
                        total_ready += 1

                    if key not in comm_seen and name_key not in comm_seen:
                        comm_seen.add(key)
                        comm_seen.add(name_key)
                        if addr:
                            comm_seen.add(addr_key)
                        comm_append.append(make_commercial_row(biz, zipcode, biz_city, biz_state))

                    if key not in allbiz_seen and name_key not in allbiz_seen:
                        allbiz_seen.add(key)
                        allbiz_seen.add(name_key)
                        allbiz_append.append(make_allbiz_row(biz, zipcode, biz_city, biz_state))

                    if len(ready_batch) >= BATCH_SIZE:
                        append_rows_safe(ready_ws, ready_batch)
                        ready_batch = []
                        print("  Saved %d to Ready To Call ✓" % total_ready)
                    if len(comm_append) >= BATCH_SIZE:
                        append_rows_safe(comm_ws, comm_append)
                        comm_append = []
                    if len(allbiz_append) >= BATCH_SIZE:
                        append_rows_safe(allbiz_ws, allbiz_append)
                        allbiz_append = []

                comm_rows, comm_header_map, comm_seen = load_commercial_rows(comm_ws)

    except KeyboardInterrupt:
        print("\n\n  Paused — run again to resume.")
    finally:
        if ready_batch:
            append_rows_safe(ready_ws, ready_batch)
        if comm_append:
            append_rows_safe(comm_ws, comm_append)
        if allbiz_append:
            append_rows_safe(allbiz_ws, allbiz_append)
        prog.update({"total": total_ready})
        save_progress(prog)
        close_browser()

    print("\n" + "#" * 60)
    print("  THE MAP MAN DONE")
    print("  Businesses found       : %d" % total_found)
    print("  Added to Ready To Call : %d (with phone numbers)" % total_ready)
    print("  Phone numbers found    : %d" % phones_found)
    print("  Ready To Call tab is your dialing list")
    print("#" * 60)

def main():
    parser = argparse.ArgumentParser(description="THE MAP MAN v%s" % VERSION)
    parser.add_argument("--zip", type=str, default=None)
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--enrich-only", action="store_true", help="Only enrich existing Green Commercial leads with phones")
    args = parser.parse_args()

    print("\n" + "#" * 60)
    print("  THE MAP MAN v%s" % VERSION)
    print("  Finds businesses | Gets phones | Builds Ready To Call list")
    print("#" * 60 + "\n")

    ss, ready_ws, comm_ws, allbiz_ws = connect_sheets()
    ready_seen = load_ready_seen(ready_ws)

    if args.enrich_only:
        enrich_green_commercial(ss, ready_ws, ready_seen, args.headless)
        return

    print("\n  Step 1: Enriching existing Green Commercial leads first...")
    enrich_green_commercial(ss, ready_ws, ready_seen, args.headless)

    zipcode = args.zip or input("\n  Enter ZIP code to scrape: ").strip()
    if not re.match(r"^\d{5}$", zipcode):
        print("  Invalid ZIP.")
        sys.exit(1)

    print("\n  Step 2: Scraping ZIP %s for new businesses..." % zipcode)
    run(zipcode, ss, ready_ws, comm_ws, allbiz_ws, args.headless)

if __name__ == "__main__":
    main()
