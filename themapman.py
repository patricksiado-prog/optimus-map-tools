"""
THE MAP MAN v6.1 — COMMERCIAL PRIORITY PHONE BUILDER
====================================================

MAIN PURPOSE:
- Priority #1: update your existing Commercial tab.
- Priority #2: add new small businesses to Commercial.
- Priority #3: create/update All Biz Phones as a master backup list.

WHAT IT DOES:
- Scans a ZIP code with Google Maps + OpenStreetMap.
- Gets business name, address, phone, category when available.
- Excludes large corporations, government buildings, schools, hospitals, etc.
- If a found business matches an existing Commercial row by address or name,
  it updates that existing row instead of duplicating it.
- If no match, it adds a new row to Commercial.
- Also writes found businesses to All Biz Phones.
- Marks every row: NOT FIBER VALIDATED.
- Does NOT send addresses to AT&T.
- Does NOT validate fiber.

INSTALL ON EACH COMPUTER:
  python -m pip install requests gspread google-auth playwright
  python -m playwright install chromium

TEST PLAYWRIGHT:
  python -c "from playwright.sync_api import sync_playwright; print('playwright works')"

RUN:
  python themapman.py --zip 77027
  python themapman.py --zip 77027 --headless

ENRICH ONLY EXISTING COMMERCIAL ROWS:
  python themapman.py --enrich-only
  python themapman.py --enrich-only --headless

RESET ZIP PROGRESS:
  Delete mapman_progress.json
"""

import os
import sys
import re
import json
import time
import argparse
import random
from datetime import datetime

import requests
import gspread
from google.oauth2.service_account import Credentials


# ── CONFIG ──────────────────────────────────────────────────────────

CREDS_FILE = "google_creds.json"

# Your Google Sheet ID
SHEET_ID = "15ymTkIGPWs6quB035l414ns5hkG9cQ5xr_W4ukd0OAA"

COMMERCIAL_TAB = "Commercial"
ALL_BIZ_TAB = "All Biz Phones"

PROGRESS_FILE = "mapman_progress.json"

START_ROWS = 1000
BATCH_SIZE = 20

NOMINATIM = "https://nominatim.openstreetmap.org"
OSM_OVERPASS = "https://overpass-api.de/api/interpreter"

OSM_DELAY = 1.0
MAP_DELAY = 2.2
JITTER = 0.5

GRID_STEP = 0.03
SEARCH_RADIUS_METERS = 600

COMMERCIAL_HEADERS = [
    "Business Name",
    "Address",
    "Phone",
    "Category",
    "City",
    "State",
    "ZIP",
    "Lead Type",
    "Data Source",
    "Phone Source",
    "Fiber Validation Status",
    "Fiber Validation Method",
    "Pitch Type",
    "Notes",
    "Found By",
    "Added At",
]

ALL_BIZ_HEADERS = [
    "Business Name",
    "Address",
    "Phone",
    "Category",
    "City",
    "State",
    "ZIP",
    "Lead Type",
    "Data Source",
    "Phone Source",
    "Fiber Validation Status",
    "Fiber Validation Method",
    "Pitch Type",
    "Notes",
    "Source ZIP",
    "Found By",
    "Added At",
]

SEARCH_CATEGORIES = [
    "small businesses",
    "local businesses",
    "businesses",
    "companies",
    "shops",
    "stores",
    "services",
    "commercial businesses",
    "professional services",

    "restaurants",
    "mexican restaurants",
    "chinese restaurants",
    "italian restaurants",
    "seafood restaurants",
    "steakhouses",
    "bbq restaurants",
    "breakfast restaurants",
    "brunch restaurants",
    "takeout restaurants",
    "fast food",
    "cafes",
    "coffee shops",
    "bakeries",
    "donut shops",
    "dessert shops",
    "ice cream shops",
    "juice bars",
    "smoothie shops",
    "food trucks",
    "catering",
    "bars",
    "sports bars",
    "lounges",
    "hookah lounges",

    "auto repair shops",
    "mechanics",
    "car repair",
    "truck repair",
    "diesel repair",
    "body shops",
    "collision repair",
    "paint and body shops",
    "tire shops",
    "used tire shops",
    "oil change",
    "brake repair",
    "transmission repair",
    "auto glass",
    "windshield repair",
    "car wash",
    "detail shops",
    "mobile detailing",
    "towing companies",
    "car dealerships",
    "used car dealers",
    "motorcycle repair",
    "muffler shops",
    "inspection stations",

    "hair salons",
    "barber shops",
    "nail salons",
    "beauty salons",
    "eyebrow threading",
    "lash studios",
    "waxing salons",
    "spas",
    "day spas",
    "massage",
    "massage therapy",
    "tanning salons",
    "tattoo shops",
    "piercing shops",
    "med spas",
    "skin care clinics",

    "medical offices",
    "clinics",
    "doctors",
    "family practice",
    "primary care",
    "urgent care",
    "dentists",
    "orthodontists",
    "oral surgeons",
    "chiropractors",
    "physical therapy",
    "occupational therapy",
    "pediatric clinics",
    "dermatologists",
    "eye doctors",
    "optometrists",
    "eye care",
    "hearing aid centers",
    "pharmacies",
    "compounding pharmacies",
    "medical spas",
    "therapy offices",
    "counseling offices",
    "veterinary clinics",
    "animal hospitals",
    "pet groomers",
    "pet boarding",
    "dog daycare",

    "law offices",
    "attorneys",
    "personal injury lawyers",
    "family lawyers",
    "immigration lawyers",
    "criminal defense lawyers",
    "tax attorneys",
    "accounting firms",
    "accountants",
    "bookkeeping",
    "tax services",
    "payroll services",
    "insurance offices",
    "insurance agencies",
    "real estate offices",
    "realtors",
    "property management companies",
    "mortgage brokers",
    "loan offices",
    "title companies",
    "financial advisors",
    "notary services",
    "consultants",
    "business consultants",
    "staffing agencies",
    "employment agencies",

    "contractors",
    "general contractors",
    "roofing contractors",
    "roofers",
    "plumbers",
    "electricians",
    "HVAC contractors",
    "air conditioning repair",
    "heating repair",
    "painters",
    "flooring contractors",
    "tile contractors",
    "carpet installers",
    "drywall contractors",
    "concrete contractors",
    "masonry contractors",
    "fence contractors",
    "deck builders",
    "garage door repair",
    "window installers",
    "door installers",
    "glass companies",
    "landscapers",
    "lawn care",
    "tree services",
    "irrigation companies",
    "pool services",
    "pool repair",
    "pest control",
    "cleaning services",
    "house cleaning",
    "commercial cleaning",
    "janitorial services",
    "pressure washing",
    "moving companies",
    "junk removal",
    "restoration companies",
    "water damage restoration",
    "fire damage restoration",
    "foundation repair",
    "handyman services",
    "appliance repair",
    "locksmiths",

    "retail stores",
    "boutiques",
    "clothing stores",
    "shoe stores",
    "jewelry stores",
    "watch repair",
    "gift shops",
    "florists",
    "furniture stores",
    "mattress stores",
    "appliance stores",
    "electronics stores",
    "electronics repair",
    "phone repair",
    "computer repair",
    "camera stores",
    "music stores",
    "bookstores",
    "toy stores",
    "sporting goods stores",
    "bike shops",
    "hardware stores",
    "paint stores",
    "lighting stores",
    "flooring stores",
    "tile stores",
    "carpet stores",
    "home decor stores",
    "thrift stores",
    "consignment shops",
    "pawn shops",
    "smoke shops",
    "vape shops",

    "marketing agencies",
    "advertising agencies",
    "web design",
    "graphic design",
    "printing shops",
    "sign shops",
    "screen printing",
    "embroidery shops",
    "promotional products",
    "photographers",
    "videographers",
    "event planners",
    "event venues",
    "wedding venues",
    "party rentals",
    "equipment rental",
    "office supply stores",
    "coworking spaces",
    "shipping services",
    "mailbox rental",
    "pack and ship",
    "courier services",
    "security companies",
    "alarm companies",
    "IT services",
    "computer support",
    "managed IT services",

    "gyms",
    "fitness centers",
    "personal trainers",
    "yoga studios",
    "pilates studios",
    "martial arts",
    "boxing gyms",
    "dance studios",
    "daycare centers",
    "preschools",
    "child care",
    "tutoring centers",
    "learning centers",
    "music lessons",
    "driving schools",
    "trade schools",
    "training centers",

    "machine shops",
    "welding shops",
    "fabrication shops",
    "metal suppliers",
    "manufacturing companies",
    "industrial supply",
    "electrical supply",
    "plumbing supply",
    "HVAC supply",
    "building materials",
    "lumber yards",
    "granite suppliers",
    "stone suppliers",
    "cabinet makers",
    "sign manufacturers",
    "commercial printers",
    "logistics companies",
    "freight companies",
    "trucking companies",
    "warehouses",
    "storage facilities",
    "self storage",

    "laundromats",
    "dry cleaners",
    "tailors",
    "alterations",
    "shoe repair",
    "watch repair",
    "travel agencies",
    "taxi services",
    "limo services",
    "car rental",
    "party stores",
    "check cashing",
    "money transfer",
    "funeral homes",
    "cemeteries",
    "churches",
    "nonprofits",
]

EXCLUDE = [
    "walmart", "target", "costco", "home depot", "lowes", "lowe's", "best buy",
    "kroger", "heb ", "h-e-b", "publix", "safeway", "albertsons", "aldi",
    "whole foods", "sam's club", "sams club",

    "mcdonald", "burger king", "taco bell", "wendy", "chick-fil", "subway",
    "starbucks", "dunkin", "domino", "pizza hut", "papa john", "popeyes",
    "kfc", "jack in the box", "whataburger", "sonic drive", "dairy queen",

    "chase bank", "wells fargo", "bank of america", "citibank", "us bank",
    "td bank", "pnc bank", "capital one", "regions bank", "frost bank",

    "walgreens", "cvs", "rite aid",
    "dollar general", "dollar tree", "family dollar",
    "7-eleven", "7 eleven", "circle k", "wawa", "shell", "chevron", "exxon",
    "valero", "texaco", "bp gas",

    "marriott", "hilton", "hyatt", "holiday inn", "sheraton", "hampton inn",
    "la quinta", "motel 6", "comfort inn", "best western",

    "fedex office", "ups store", "post office", "usps",

    "city hall", "county ", "courthouse", "dmv ", "social security",
    "fire station", "police station", "sheriff", "jail", "prison",
    "government", "municipal", "public works",

    "university", "college", "school district", " isd", "high school",
    "middle school", "elementary", "community college", "academy",

    "hospital", "medical center", "health system", "children's hospital",
    "memorial hermann", "methodist hospital", "hca houston",

    "warehouse", "distribution center", "fulfillment", "manufacturing plant",
    "amazon", "google office", "microsoft", "apple store",
]


# ── HELPERS ─────────────────────────────────────────────────────────

def norm(s):
    if not s:
        return ""
    s = str(s).lower().strip()
    s = re.sub(r"[^\w\s]", " ", s)
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
    phone = phone.replace("Phone:", "")
    phone = phone.replace("Call phone number", "")
    phone = phone.replace("tel:", "")
    phone = phone.strip()

    digits = re.sub(r"\D", "", phone)

    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]

    if len(digits) == 10:
        return "(%s) %s-%s" % (digits[:3], digits[3:6], digits[6:])

    return phone


def extract_phone_from_text(text):
    if not text:
        return ""

    patterns = [
        r"\(?\b\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b",
        r"\b1[-.\s]\d{3}[-.\s]\d{3}[-.\s]\d{4}\b",
    ]

    for p in patterns:
        m = re.search(p, text)
        if m:
            return clean_phone(m.group(0))

    return ""


def is_small_biz(name, category=""):
    if not name or len(str(name).strip()) < 3:
        return False

    combined = (str(name) + " " + str(category or "")).lower()

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

    street_words = (
        " st", " street", " rd", " road", " ave", " avenue", " dr", " drive",
        " ln", " lane", " blvd", " boulevard", " pkwy", " parkway",
        " way", " ct", " court", " cir", " circle", " hwy", " highway",
        " loop", " fwy", " freeway", " trail", " trl", " place", " pl",
        " suite", " ste", " park", " plaza",
    )

    tl = " " + t.lower()
    return bool(re.search(r"\d{2,}", t)) and any(w in tl for w in street_words)


def address_key(addr):
    a = norm(addr)
    a = re.sub(r"\bste\b|\bsuite\b|\bunit\b|\bapt\b", "", a)
    a = re.sub(r"\s+", " ", a).strip()
    return a


def same_address(a, b):
    if not a or not b:
        return False

    ak = address_key(a)
    bk = address_key(b)

    if ak == bk:
        return True

    anum = re.findall(r"\b\d{2,6}\b", ak)
    bnum = re.findall(r"\b\d{2,6}\b", bk)

    if not anum or not bnum:
        return False

    if anum[0] != bnum[0]:
        return False

    aw = set(ak.split())
    bw = set(bk.split())

    return len(aw.intersection(bw)) >= 3


# ── SHEETS ──────────────────────────────────────────────────────────

def connect_sheets():
    if not os.path.exists(CREDS_FILE):
        print("\nERROR: %s not found." % CREDS_FILE)
        print("Put google_creds.json in the same folder as themapman.py")
        sys.exit(1)

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    ss = client.open_by_key(SHEET_ID)

    commercial_ws = get_or_create_tab(ss, COMMERCIAL_TAB, COMMERCIAL_HEADERS)
    allbiz_ws = get_or_create_tab(ss, ALL_BIZ_TAB, ALL_BIZ_HEADERS)

    print("Connected to Google Sheets!")
    return commercial_ws, allbiz_ws


def get_or_create_tab(ss, title, headers):
    try:
        ws = ss.worksheet(title)
    except gspread.exceptions.WorksheetNotFound:
        ws = ss.add_worksheet(title=title, rows=START_ROWS, cols=len(headers))
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
        last_col = col_letter(len(new_headers))
        ws.update(range_name="A1:%s1" % last_col, values=[new_headers])
        print("  Added missing columns to: %s" % title)

    return ws


def load_commercial_rows(ws):
    vals = ws.get_all_values()

    if not vals:
        return [], {}, set()

    headers = [h.lower().strip() for h in vals[0]]
    rows = []
    seen = set()

    for row_num, row in enumerate(vals[1:], start=2):
        d = {}

        for i, h in enumerate(headers):
            d[h] = row[i].strip() if len(row) > i else ""

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


def load_existing_allbiz(ws):
    vals = ws.get_all_values()
    seen = set()

    if not vals:
        return seen

    headers = [h.lower().strip() for h in vals[0]]
    name_idx = headers.index("business name") if "business name" in headers else 0
    addr_idx = headers.index("address") if "address" in headers else 1
    phone_idx = headers.index("phone") if "phone" in headers else 2

    for row in vals[1:]:
        name = row[name_idx].strip() if len(row) > name_idx else ""
        addr = row[addr_idx].strip() if len(row) > addr_idx else ""
        phone = row[phone_idx].strip() if len(row) > phone_idx else ""

        if name or addr:
            seen.add(norm(name) + "|" + address_key(addr))
        if name:
            seen.add("NAME|" + norm(name))
        if phone:
            seen.add("PHONE|" + norm(phone))

    return seen


def append_rows(ws, rows):
    if not rows:
        return True

    for attempt in range(3):
        try:
            ws.append_rows(rows, value_input_option="USER_ENTERED")
            time.sleep(0.4)
            return True
        except Exception as e:
            print("  Sheet append error attempt %d: %s" % (attempt + 1, e))
            time.sleep(5)

    return False


def batch_update(ws, updates):
    if not updates:
        return True

    for attempt in range(3):
        try:
            ws.batch_update(updates, value_input_option="USER_ENTERED")
            time.sleep(0.4)
            return True
        except Exception as e:
            print("  Sheet update error attempt %d: %s" % (attempt + 1, e))
            time.sleep(5)

    return False


# ── ZIP / GEO ───────────────────────────────────────────────────────

def zip_to_bounds(zipcode):
    print("\n  Looking up ZIP %s..." % zipcode)

    try:
        r = requests.get(
            "%s/search" % NOMINATIM,
            params={
                "postalcode": zipcode,
                "country": "US",
                "format": "json",
                "limit": 1,
                "addressdetails": 1,
            },
            headers={"User-Agent": "TheMapMan/6.1"},
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
        state = a.get("state", "")

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


# ── PROGRESS ────────────────────────────────────────────────────────

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


# ── OSM ─────────────────────────────────────────────────────────────

def osm_nearby(lat, lng, radius=SEARCH_RADIUS_METERS):
    results = []
    seen = set()

    query = """
[out:json][timeout:30];
(
  node(around:{r},{lat},{lng})[shop];
  node(around:{r},{lat},{lng})[office];
  node(around:{r},{lat},{lng})[craft];
  node(around:{r},{lat},{lng})[healthcare];
  node(around:{r},{lat},{lng})[amenity~"restaurant|cafe|bar|pharmacy|clinic|dentist|doctors|beauty|hairdresser|barber|gym|car_repair|car_wash|fast_food|veterinary|optician|massage|laundry|bakery|insurance|bank|fuel"];
  way(around:{r},{lat},{lng})[shop];
  way(around:{r},{lat},{lng})[office];
  way(around:{r},{lat},{lng})[craft];
  way(around:{r},{lat},{lng})[healthcare];
  way(around:{r},{lat},{lng})[amenity~"restaurant|cafe|bar|pharmacy|clinic|dentist|doctors|beauty|hairdresser|barber|gym|car_repair|car_wash|fast_food|veterinary|optician|massage|laundry|bakery|insurance|bank|fuel"];
);
out center tags;
""".format(r=radius, lat=lat, lng=lng)

    try:
        time.sleep(OSM_DELAY + random.uniform(0, JITTER))

        r = requests.post(
            OSM_OVERPASS,
            data={"data": query},
            headers={"User-Agent": "TheMapMan/6.1"},
            timeout=30,
        )

        if r.status_code != 200:
            return results

        for el in r.json().get("elements", []):
            tags = el.get("tags", {})
            name = tags.get("name", "").strip()

            category = (
                tags.get("shop")
                or tags.get("office")
                or tags.get("amenity")
                or tags.get("craft")
                or tags.get("healthcare")
                or "business"
            )

            if not is_small_biz(name, category):
                continue

            oid = "%s_%s" % (el.get("type", ""), el.get("id", ""))
            if oid in seen:
                continue

            seen.add(oid)

            phone = clean_phone(
                tags.get("phone", "")
                or tags.get("contact:phone", "")
                or tags.get("telephone", "")
            )

            house = tags.get("addr:housenumber", "")
            street = tags.get("addr:street", "")
            addr = ("%s %s" % (house, street)).strip() if house and street else ""

            city = tags.get("addr:city", "")
            state = tags.get("addr:state", "TX")

            if state.lower() == "texas":
                state = "TX"

            zipc = tags.get("addr:postcode", "")

            results.append({
                "name": name,
                "address": addr,
                "phone": phone,
                "category": category,
                "city": city,
                "state": state,
                "zip": zipc,
                "found_by": "OpenStreetMap",
                "phone_source": "OpenStreetMap" if phone else "No phone found",
            })

    except Exception as e:
        print("    OSM error: %s" % e)

    return results


# ── GOOGLE MAPS ─────────────────────────────────────────────────────

_pw = None
_browser = None
_page = None


def init_browser(headless=False):
    global _pw, _browser, _page

    print("\n  Python running this script:")
    print("  %s" % sys.executable)

    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:
        print("\n  PLAYWRIGHT NOT FOUND FOR THIS PYTHON.")
        print("  Error: %s" % e)
        print("\n  Fix it with these commands in this same Command Prompt:")
        print("  python -m pip install playwright")
        print("  python -m playwright install chromium")
        print("\n  Then test:")
        print("  python -c \"from playwright.sync_api import sync_playwright; print('playwright works')\"")
        raise

    _pw = sync_playwright().start()

    _browser = _pw.chromium.launch(
        headless=headless,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ],
    )

    ctx = _browser.new_context(
        viewport={"width": 1366, "height": 768},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        locale="en-US",
    )

    _page = ctx.new_page()

    _page.goto("https://www.google.com/maps", timeout=20000, wait_until="domcontentloaded")
    time.sleep(2)

    try:
        for sel in [
            "button[aria-label*='Accept all']",
            "button[aria-label*='Accept']",
            "button:has-text('Accept all')",
        ]:
            btn = _page.query_selector(sel)
            if btn:
                btn.click()
                time.sleep(1)
                break
    except Exception:
        pass

    print("  Browser ready")


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


def extract_phone_from_maps_page():
    global _page

    selectors = [
        "button[data-item-id^='phone']",
        "button[aria-label^='Phone:']",
        "button[aria-label*='Phone']",
        "div[aria-label^='Phone:']",
    ]

    for sel in selectors:
        try:
            for el in _page.query_selector_all(sel):
                label = el.get_attribute("aria-label") or ""
                txt = text_safe(el)
                phone = extract_phone_from_text(label + " " + txt)
                if phone:
                    return phone
        except Exception:
            pass

    try:
        body = _page.inner_text("body")
        phone = extract_phone_from_text(body)
        if phone:
            return phone
    except Exception:
        pass

    return ""


def extract_address_from_maps_page():
    global _page

    selectors = [
        "button[data-item-id='address']",
        "button[aria-label^='Address:']",
        "button[aria-label*='Address']",
    ]

    for sel in selectors:
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

        url = "https://www.google.com/maps/search/%s/@%.5f,%.5f,14z" % (
            q.replace(" ", "+"),
            lat,
            lng,
        )

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
                    category_guess = category

                    cat_el = card.query_selector("div.W4Efsd span.fontBodyMedium")
                    if cat_el:
                        cat_text = cat_el.inner_text().strip()
                        if cat_text:
                            category_guess = cat_text

                    if not is_small_biz(name, category_guess):
                        continue

                    nk = norm(name)
                    if nk in seen:
                        continue
                    seen.add(nk)

                    addr = ""
                    phone = extract_phone_from_text(card_text)

                    for el in card.query_selector_all("div.W4Efsd span"):
                        txt = el.inner_text().strip()
                        if looks_like_address(txt):
                            addr = txt
                            break

                    try:
                        card.click()
                        time.sleep(1.8)

                        detail_phone = extract_phone_from_maps_page()
                        detail_addr = extract_address_from_maps_page()

                        if detail_phone:
                            phone = detail_phone
                        if detail_addr:
                            addr = detail_addr

                    except Exception:
                        pass

                    results.append({
                        "name": name,
                        "address": addr,
                        "phone": clean_phone(phone),
                        "category": category_guess,
                        "city": city,
                        "state": state,
                        "zip": zipcode,
                        "found_by": "Google Maps",
                        "phone_source": "Google Maps" if phone else "No phone found",
                    })

                except Exception:
                    continue

            try:
                feed = _page.query_selector("div[role='feed']")
                if feed:
                    feed.evaluate("el => el.scrollBy(0, 1000)")
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


def google_lookup_existing_phone(name, address, city="", state="TX", zipc=""):
    global _page

    if not _page:
        return "", ""

    q = "%s %s %s %s phone" % (name, address, city, zipc)

    try:
        url = "https://www.google.com/maps/search/%s" % q.replace(" ", "+")
        _page.goto(url, timeout=20000, wait_until="domcontentloaded")
        time.sleep(2.5)

        phone = extract_phone_from_maps_page()
        detail_addr = extract_address_from_maps_page()

        if not phone:
            try:
                body = _page.inner_text("body")
                phone = extract_phone_from_text(body)
            except Exception:
                pass

        return clean_phone(phone), detail_addr

    except Exception:
        return "", ""


# ── ROW BUILDERS ────────────────────────────────────────────────────

def make_commercial_row(biz, zipcode, city, state):
    now = datetime.now().strftime("%m/%d/%Y %I:%M %p")

    return [
        biz.get("name", ""),
        biz.get("address", ""),
        biz.get("phone", ""),
        biz.get("category", ""),
        biz.get("city", "") or city,
        biz.get("state", "") or state,
        biz.get("zip", "") or zipcode,
        "Commercial",
        biz.get("found_by", ""),
        biz.get("phone_source", "No phone found"),
        "NOT FIBER VALIDATED",
        "Not checked with AT&T",
        "NEEDS FIBER VALIDATION",
        "Small business lead from map search. Phone added when available. Fiber availability not confirmed.",
        biz.get("found_by", ""),
        now,
    ]


def make_allbiz_row(biz, zipcode, city, state):
    now = datetime.now().strftime("%m/%d/%Y %I:%M %p")

    return [
        biz.get("name", ""),
        biz.get("address", ""),
        biz.get("phone", ""),
        biz.get("category", ""),
        biz.get("city", "") or city,
        biz.get("state", "") or state,
        biz.get("zip", "") or zipcode,
        "Commercial",
        biz.get("found_by", ""),
        biz.get("phone_source", "No phone found"),
        "NOT FIBER VALIDATED",
        "Not checked with AT&T",
        "NEEDS FIBER VALIDATION",
        "Small business lead from map search. Phone added when available. Fiber availability not confirmed.",
        zipcode,
        biz.get("found_by", ""),
        now,
    ]


def enrich_commercial_from_biz(commercial_rows, commercial_header_map, biz):
    biz_addr = biz.get("address", "")
    biz_name = biz.get("name", "")
    biz_phone = biz.get("phone", "")
    biz_cat = biz.get("category", "")
    biz_city = biz.get("city", "")
    biz_state = biz.get("state", "")
    biz_zip = biz.get("zip", "")
    found_by = biz.get("found_by", "")
    phone_source = biz.get("phone_source", "")

    if not biz_addr and not biz_name:
        return []

    for row in commercial_rows:
        row_addr = (
            row.get("address", "")
            or row.get("property address", "")
            or row.get("street address", "")
            or row.get("full address", "")
        )

        row_name = row.get("business name", "")
        row_phone = row.get("phone", "")

        match = False

        if biz_addr and row_addr and same_address(biz_addr, row_addr):
            match = True

        if not match and biz_name and row_name and norm(biz_name) == norm(row_name):
            match = True

        if not match:
            continue

        row_num = row["_row_num"]
        updates = []

        def add_update(header_name, value, overwrite=False):
            h = header_name.lower()
            if h in commercial_header_map and value:
                existing_value = row.get(h, "")
                if overwrite or not existing_value:
                    col = commercial_header_map[h] + 1
                    updates.append({
                        "range": "%s%d" % (col_letter(col), row_num),
                        "values": [[value]],
                    })

        add_update("Business Name", biz_name)
        add_update("Phone", biz_phone)
        add_update("Category", biz_cat)
        add_update("City", biz_city)
        add_update("State", biz_state)
        add_update("ZIP", biz_zip)

        add_update("Lead Type", "Commercial", overwrite=True)
        add_update("Data Source", found_by, overwrite=True)
        add_update("Phone Source", phone_source or "No phone found", overwrite=True)
        add_update("Fiber Validation Status", "NOT FIBER VALIDATED", overwrite=True)
        add_update("Fiber Validation Method", "Not checked with AT&T", overwrite=True)
        add_update("Pitch Type", "NEEDS FIBER VALIDATION", overwrite=True)
        add_update("Notes", "Existing Commercial row enriched from map data. Fiber availability not confirmed.", overwrite=True)
        add_update("Found By", found_by, overwrite=True)
        add_update("Added At", datetime.now().strftime("%m/%d/%Y %I:%M %p"), overwrite=True)

        return updates

    return []


# ── ENRICH ONLY ─────────────────────────────────────────────────────

def enrich_only_existing(commercial_ws, commercial_rows, commercial_header_map):
    print("\n" + "=" * 60)
    print("  ENRICH EXISTING COMMERCIAL ROWS WITH PHONE NUMBERS")
    print("=" * 60)

    updates = []
    added = 0

    for row in commercial_rows:
        row_num = row["_row_num"]
        name = row.get("business name", "")
        addr = row.get("address", "")
        phone = row.get("phone", "")
        city = row.get("city", "")
        state = row.get("state", "TX")
        zipc = row.get("zip", "")

        if phone:
            continue

        if not name and not addr:
            continue

        print("  Row %d: looking up phone for %s" % (row_num, name or addr))

        found_phone, detail_addr = google_lookup_existing_phone(name, addr, city, state, zipc)

        if not found_phone:
            print("       No phone found")
            continue

        print("       Found phone: %s" % found_phone)

        def add_update(header_name, value):
            h = header_name.lower()
            if h in commercial_header_map:
                col = commercial_header_map[h] + 1
                updates.append({
                    "range": "%s%d" % (col_letter(col), row_num),
                    "values": [[value]],
                })

        add_update("Phone", found_phone)
        add_update("Phone Source", "Google Maps Enrichment")
        add_update("Fiber Validation Status", "NOT FIBER VALIDATED")
        add_update("Fiber Validation Method", "Not checked with AT&T")
        add_update("Pitch Type", "NEEDS FIBER VALIDATION")
        add_update("Notes", "Phone enriched from Google Maps. Fiber availability not confirmed.")
        add_update("Added At", datetime.now().strftime("%m/%d/%Y %I:%M %p"))

        if detail_addr and not addr:
            add_update("Address", detail_addr)

        added += 1

        if len(updates) >= 25:
            batch_update(commercial_ws, updates)
            updates = []
            print("       Saved updates ✓")

    if updates:
        batch_update(commercial_ws, updates)
        print("       Saved final updates ✓")

    return added


# ── MAIN RUN ────────────────────────────────────────────────────────

def run(zipcode, commercial_ws, allbiz_ws, headless):
    clat, clng, south, west, north, east, city, state = zip_to_bounds(zipcode)
    grid = build_grid(south, west, north, east)
    prog = load_progress(zipcode)

    print("\n" + "=" * 60)
    print("  THE MAP MAN v6.1 — ZIP %s" % zipcode)
    print("  City: %s, %s" % (city, state))
    print("  PRIORITY: enrich existing Commercial first")
    print("  Then add new businesses to Commercial")
    print("  Also saves to All Biz Phones")
    print("  Fiber status: NOT FIBER VALIDATED")
    print("  Grid squares: %d | Categories: %d" % (len(grid), len(SEARCH_CATEGORIES)))
    print("=" * 60 + "\n")

    if prog.get("grid_idx", 0) > 0:
        print("  Previous run found — resuming at grid %d/%d" % (
            prog["grid_idx"] + 1,
            len(grid),
        ))

        if input("  Resume? (y/n, default y): ").strip().lower() == "n":
            prog = {"zip": zipcode, "grid_idx": 0, "cat_idx": 0, "total": 0}
            save_progress(prog)

    try:
        init_browser(headless)
        use_gmaps = True
    except Exception as e:
        print("  Browser unavailable (%s) — OSM only" % e)
        use_gmaps = False

    commercial_rows, commercial_header_map, commercial_seen = load_commercial_rows(commercial_ws)
    allbiz_seen = load_existing_allbiz(allbiz_ws)

    commercial_append_batch = []
    allbiz_append_batch = []
    commercial_update_batch = []

    total_found = 0
    total_added_commercial = 0
    total_added_allbiz = 0
    total_enriched = 0
    phones_found = 0

    try:
        for gi in range(prog.get("grid_idx", 0), len(grid)):
            lat, lng = grid[gi]
            cat_start = prog.get("cat_idx", 0) if gi == prog.get("grid_idx", 0) else 0

            for ci in range(cat_start, len(SEARCH_CATEGORIES)):
                cat = SEARCH_CATEGORIES[ci]

                prog.update({
                    "zip": zipcode,
                    "grid_idx": gi,
                    "cat_idx": ci,
                    "total": total_added_allbiz,
                })
                save_progress(prog)

                print("\n  [%d/%d] %.4f_%.4f | %s" % (
                    gi + 1,
                    len(grid),
                    lat,
                    lng,
                    cat,
                ))

                osm_results = osm_nearby(lat, lng, radius=SEARCH_RADIUS_METERS)

                gm_results = []
                if use_gmaps:
                    gm_results = gmaps_search(lat, lng, cat, zipcode, city, state)

                combined = list(osm_results)
                known_names = {norm(b.get("name", "")) for b in combined}

                for b in gm_results:
                    if norm(b.get("name", "")) not in known_names:
                        combined.append(b)
                        known_names.add(norm(b.get("name", "")))

                print("  Found %d small businesses" % len(combined))
                total_found += len(combined)

                for biz in combined:
                    name = biz.get("name", "").strip()
                    addr = biz.get("address", "").strip()
                    phone = clean_phone(biz.get("phone", ""))

                    biz["phone"] = phone

                    if not name:
                        continue

                    if not is_small_biz(name, biz.get("category", "")):
                        continue

                    if phone:
                        phones_found += 1

                    key = norm(name) + "|" + address_key(addr)
                    name_key = "NAME|" + norm(name)
                    addr_key = "ADDR|" + address_key(addr)

                    # Priority #1: enrich existing Commercial row.
                    updates = enrich_commercial_from_biz(
                        commercial_rows,
                        commercial_header_map,
                        biz,
                    )

                    if updates:
                        commercial_update_batch.extend(updates)
                        total_enriched += 1
                    else:
                        # Priority #2: add new business to Commercial.
                        if (
                            key not in commercial_seen
                            and name_key not in commercial_seen
                            and (not addr or addr_key not in commercial_seen)
                        ):
                            commercial_seen.add(key)
                            commercial_seen.add(name_key)

                            if addr:
                                commercial_seen.add(addr_key)

                            commercial_append_batch.append(make_commercial_row(biz, zipcode, city, state))
                            total_added_commercial += 1

                    # Priority #3: save master copy to All Biz Phones.
                    if key not in allbiz_seen and name_key not in allbiz_seen:
                        allbiz_seen.add(key)
                        allbiz_seen.add(name_key)
                        allbiz_append_batch.append(make_allbiz_row(biz, zipcode, city, state))
                        total_added_allbiz += 1

                    print("  + %-35s | phone: %s | %s" % (
                        name[:35],
                        phone if phone else "none",
                        biz.get("found_by", ""),
                    ))

                    if len(commercial_update_batch) >= 30:
                        batch_update(commercial_ws, commercial_update_batch)
                        commercial_update_batch = []
                        print("  Saved Commercial enrichment updates ✓")

                    if len(commercial_append_batch) >= BATCH_SIZE:
                        append_rows(commercial_ws, commercial_append_batch)
                        commercial_append_batch = []
                        print("  Saved new Commercial rows ✓")

                    if len(allbiz_append_batch) >= BATCH_SIZE:
                        append_rows(allbiz_ws, allbiz_append_batch)
                        allbiz_append_batch = []
                        print("  Saved All Biz Phones rows ✓")

                commercial_rows, commercial_header_map, commercial_seen = load_commercial_rows(commercial_ws)

    except KeyboardInterrupt:
        print("\n\n  Paused — run again to resume.")

    finally:
        if commercial_update_batch:
            batch_update(commercial_ws, commercial_update_batch)

        if commercial_append_batch:
            append_rows(commercial_ws, commercial_append_batch)

        if allbiz_append_batch:
            append_rows(allbiz_ws, allbiz_append_batch)

        prog.update({"total": total_added_allbiz})
        save_progress(prog)

        close_browser()

    print("\n" + "#" * 60)
    print("  THE MAP MAN DONE")
    print("#" * 60)
    print("  Businesses found             : %d" % total_found)
    print("  Enriched existing Commercial : %d" % total_enriched)
    print("  Added new to Commercial      : %d" % total_added_commercial)
    print("  Added to All Biz Phones      : %d" % total_added_allbiz)
    print("  Phone numbers found          : %d" % phones_found)
    print("  Fiber status                 : NOT FIBER VALIDATED")
    print("#" * 60)


# ── ENTRY ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="THE MAP MAN v6.1")

    parser.add_argument("--zip", type=str, default=None)
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--enrich-only", action="store_true")

    args = parser.parse_args()

    print("\n" + "#" * 60)
    print("  THE MAP MAN v6.1")
    print("  Commercial phone builder + enricher")
    print("  Priority: update existing Commercial first")
    print("  Does NOT fiber validate")
    print("#" * 60)

    commercial_ws, allbiz_ws = connect_sheets()

    commercial_rows, commercial_header_map, commercial_seen = load_commercial_rows(commercial_ws)

    if args.enrich_only:
        try:
            init_browser(args.headless)
        except Exception as e:
            print("Browser could not start: %s" % e)
            sys.exit(1)

        updated = enrich_only_existing(commercial_ws, commercial_rows, commercial_header_map)

        close_browser()

        print("\n" + "#" * 60)
        print("  ENRICHMENT DONE")
        print("  Existing Commercial phones added: %d" % updated)
        print("#" * 60)
        return

    zipcode = args.zip or input("\n  Enter ZIP code: ").strip()

    if not re.match(r"^\d{5}$", zipcode):
        print("  Invalid ZIP.")
        sys.exit(1)

    run(zipcode, commercial_ws, allbiz_ws, args.headless)


if __name__ == "__main__":
    main()