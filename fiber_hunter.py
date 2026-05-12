"""
FIBER HUNTER v5.7 SHIP-WITH-FIX
================================================================================
For: ChatGPT push lead. Replaces v5.6 on patricksiado-prog/optimus-map-tools main.
Diff against current repo HEAD before push (BRAIN claims v5.0; Drive copy v5.6;
current HEAD must be verified by ChatGPT).

CHANGES vs v5.6:

1. CLASSIFICATION CLEANUP
   - is_blank_map(img) - rejects loading/timeout/uniform screenshots.
   - count_dot_clusters() - connected-component count with size + shape filter.
   - find_dots() returns (x, y, cluster_size) for Dot Confidence telemetry.
   - dots_on_screen() and wait_for_dots() gate on cluster count, not pixel total.
   - Hot-zone alerts (check_hot_zone) still pixel-total based - unchanged.

2. SHAPE FILTER (NEW - PARK FRAGMENTATION FIX)
   - _is_dot_shape() helper: bbox area cap, compactness floor, aspect ratio cap.
   - Real fiber dots are compact (size/bbox >= 0.45) and roughly circular
     (aspect <= 2.5). Park slivers, freeway markers, water borders all rejected.
   - Used by count_dot_clusters AND find_dots so detection stays consistent.

3. FOUR-COLOR CLASSIFICATION (Green / Gold / Grey / Blank)
   - GREY_MIN / GREY_MAX added (desaturated, NOT aliased to BLUE).
   - Per-dot path now 3-color collection in priority order Green > Gold > Grey.
   - Hot-zone alerts still use BLUE_MIN/BLUE_MAX (kept for backward compat).

4. GREEN-WINS DEDUP (4-state, lowercase-safe)
   - get_existing() returns dict[address] -> set(dot_types).
   - All "in" checks use t.lower() so canonical-vs-legacy strings still match.
   - Priority chain:
       (none)        + Green -> write OK
       (none)        + Gold  -> write OK
       (none)        + Grey  -> write SOCIAL_PROOF
       Grey          + Gold  -> write GOLD_OVER_GREY
       Grey          + Green -> write GREEN_OVER_GREY
       Gold          + Green -> write GREEN_OVER_GOLD
       Green/Gold    + Grey  -> skip (existing stronger)
       Green         + Gold  -> skip (existing stronger)
       Green/Gold/Grey same -> skip

5. TAB ROUTING
   - Hunter Leads master gets every classified row (Green/Gold/Grey).
   - Hunter Commercial / Residential get Green + Gold only.
   - Hunter Green Commercial / Green Residential get Green only.
   - Grey rows stay in master Hunter Leads only - do NOT pollute verticals.

6. NEW SCHEMA FIELDS (per ChatGPT v5.7 spec)
   - Hunter Leads: + Verified Color, Dot Confidence, Source Screenshot, Scan Status.
   - All other Hunter tabs: + Verified Color (cross-tab consistency).
   - One-shot header migration extends existing tabs at startup.

7. NEW COUNTERS
   - blank_skip, park_skip
   - grey, green_over_gold, green_over_grey, gold_over_grey

UNCHANGED:
   - Auto-update mechanism, spiral motion, geocoding stack, hot-zone alert math,
     resume-on-Ctrl+C, all CLI behavior.

USAGE:
   pip install pyautogui pillow scipy numpy requests gspread google-auth pgeocode
   python fiber_hunter.py
   Ctrl+C to stop. Resumes next run.
"""

import os, sys, time, json, threading, queue, re
import requests, numpy as np, pyautogui, gspread
from PIL import Image, ImageGrab
from datetime import datetime
from scipy import ndimage
from google.oauth2.service_account import Credentials

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.03
VERSION = "5.17"

# AUTO-UPDATER
AUTO_UPDATE = True
GITHUB_REPO = "patricksiado-prog/optimus-map-tools"
GITHUB_FILE = "fiber_hunter.py"
GITHUB_BRANCH = "main"

def check_update():
    if not AUTO_UPDATE:
        return
    try:
        url = ("https://raw.githubusercontent.com/%s/%s/%s"
               % (GITHUB_REPO, GITHUB_BRANCH, GITHUB_FILE))
        print("Checking for updates...")
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            print("  Update check failed (HTTP %d), continuing" % r.status_code)
            return
        remote_code = r.text
        m = re.search(r'VERSION\s*=\s*["\']([\d.]+)["\']', remote_code)
        if not m:
            print("  Couldn't read remote version, continuing")
            return
        remote_version = m.group(1)
        if remote_version == VERSION:
            print("  Up to date (v%s)" % VERSION)
            return
        def vtuple(v): return tuple(int(x) for x in v.split("."))
        if vtuple(remote_version) <= vtuple(VERSION):
            print("  Local v%s is newer than remote v%s" % (VERSION, remote_version))
            return
        print("  Updating to v%s..." % remote_version)
        with open(__file__, "w", encoding="utf-8") as f:
            f.write(remote_code)
        print("  Updated! Restarting...")
        if os.name == "nt":
            print("  Run: python fiber_hunter.py")
            sys.exit(0)
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print("  Update err (continuing): %s" % str(e)[:100])


# CONFIG
CREDS_FILE = "google_creds.json"
SHEET_NAME = "ATT FIBER LEADS"
SCREENSHOTS_DIR = "hunter_screenshots"
DRIVE_SCREENSHOTS_FOLDER = "1g5kE9cJFlx5LChmDXSVpU2jUqUPMVd0B"
PROGRESS_FILE = "hunter_progress.json"
HISTORY_FILE = "hunter_zone_history.json"
BUTTON_FILE = "hunter_button_pos.json"
GEO_CACHE = "hunter_geocode_cache.json"
PROCESSED_MANIFEST = os.path.join(SCREENSHOTS_DIR,
    "hunter_processed_manifest.json")  # v5.17

def load_processed_manifest():
    try:
        with open(PROCESSED_MANIFEST) as _mf: return set(json.load(_mf))
    except: return set()

def save_processed_manifest(s):
    try:
        with open(PROCESSED_MANIFEST,"w") as _mf: json.dump(sorted(s),_mf)
    except: pass
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

WAIT_AFTER_PAN = 1.5
MAX_WAIT_DOTS = 4.0
POLL_INTERVAL = 0.12
PAN_PIXELS = 150
START_DELAY = 10
BATCH_SIZE = 12
GEOCODE_TIMEOUT = 7
PHONE_TIMEOUT = 3
GEO_RATE = 1.2

# v5.7 size + shape filter
MIN_DOT_PIXELS = 3
MAX_DOT_PIXELS = 800
MAX_DOT_BBOX_AREA = 1500
MIN_DOT_COMPACTNESS = 0.45
MAX_DOT_ASPECT = 2.5
MIN_DOT_CLUSTERS = 1
CLUSTER_THRESHOLD = 15

# v5.7 blank-map detection
BLANK_STD_THRESHOLD = 12.0
BLANK_CENTER_STD_THRESHOLD = 9.0
BLANK_BRIGHT_MEAN = 240
BLANK_DARK_MEAN = 30

# Hot-zone alert thresholds (unchanged)
GREENFIELD_GREEN_MIN = 80
GREENFIELD_GOLD_MAX = 20
GREENFIELD_BLUE_MAX = 30

MAP_LEFT, MAP_TOP, MAP_RIGHT, MAP_BOTTOM = 50, 100, 1350, 720
MAP_CX = (MAP_LEFT + MAP_RIGHT) // 2
MAP_CY = (MAP_TOP + MAP_BOTTOM) // 2

# Color ranges
ORANGE_MIN = (220, 160, 0)
ORANGE_MAX = (255, 200, 60)
GREEN_MIN  = (30, 130, 30)
GREEN_MAX  = (100, 210, 80)
# BLUE retained for hot-zone alert math (legacy)
BLUE_MIN   = (50, 80, 180)
BLUE_MAX   = (120, 160, 255)
# v5.7 GREY: desaturated existing-customer dot range (Grok to verify)
GREY_MIN   = (140, 140, 160)
GREY_MAX   = (190, 190, 210)

GREY_DOT_TYPE = "EXISTING FIBER (Grey)"

LAT_PER_PIXEL = -0.000015
LNG_PER_PIXEL = 0.000020
REP_NAME = "Patri"
KNOWN_COMMERCIAL_ZIPS = set()
COLS_PER_ZONE = 50
ROWS_PER_ZONE = 40

COMMERCIAL_TYPES = [
    "commercial", "retail", "office", "industrial", "warehouse",
    "supermarket", "mall", "hotel", "restaurant", "fast_food",
    "cafe", "bar", "hospital", "clinic", "school", "university",
    "government", "bank", "pharmacy", "shop", "store", "building",
    "business", "company", "plaza", "tower", "center", "centre",
    "suite", "pkwy", "parkway", "blvd", "corporate", "logistics",
    "distribution", "manufacturing", "medical", "dental",
    "automotive", "dealership", "terminal", "port", "airport",
]
RESIDENTIAL_TYPES = [
    "house", "apartments", "residential", "detached", "terrace",
    "dormitory", "condo", "flat", "dwelling", "home", "bungalow",
    "villa", "subdivision", "estates",
]
COMMERCIAL_STREET_WORDS = [
    "industrial", "commerce", "corporate", "business", "trade",
    "enterprise", "market", "distribution", "logistics", "pkwy",
    "parkway", "plaza", "center", "blvd", "highway", "freeway",
    "expressway", "loop", "port", "terminal", "airport",
]


def now_str():
    return datetime.now().strftime("%m/%d/%Y %I:%M %p")

def spiral_offsets():
    yield (0, 0, "Center")
    ring = 1
    while True:
        for x in range(-ring, ring + 1):
            yield (x, -ring, "R%dT%d" % (ring, x + ring))
        for y in range(-ring + 1, ring + 1):
            yield (ring, y, "R%dR%d" % (ring, y + ring))
        for x in range(ring - 1, -ring - 1, -1):
            yield (x, ring, "R%dB%d" % (ring, x + ring))
        for y in range(ring - 1, -ring, -1):
            yield (-ring, y, "R%dL%d" % (ring, y + ring))
        ring += 1

def zone_at(lat0, lng0, prefix, ox, oy, dirname):
    zlat = ROWS_PER_ZONE * PAN_PIXELS * abs(LAT_PER_PIXEL)
    zlng = COLS_PER_ZONE * PAN_PIXELS * LNG_PER_PIXEL
    return {
        "name": "%s_%s" % (prefix, dirname),
        "cols": COLS_PER_ZONE, "rows": ROWS_PER_ZONE,
        "start_lat": lat0 + oy * zlat,
        "start_lng": lng0 + ox * zlng,
    }

def calibrate_search_button():
    if os.path.exists(BUTTON_FILE):
        with open(BUTTON_FILE) as f:
            pos = json.load(f)
        print("  Search button: saved at (%d, %d)" % (pos["x"], pos["y"]))
        if input("  Recalibrate? (y/n, default n): ").strip().lower() != "y":
            return pos["x"], pos["y"]
    print("\nHover mouse over the AT&T 'Search this area' button.")
    input("Then press Enter: ")
    x, y = pyautogui.position()
    print("  Saved (%d, %d)" % (x, y))
    with open(BUTTON_FILE, "w") as f:
        json.dump({"x": x, "y": y}, f)
    return x, y

def grab_map():
    return ImageGrab.grab(bbox=(MAP_LEFT, MAP_TOP, MAP_RIGHT, MAP_BOTTOM))


# v5.7 PIXEL / CLUSTER / SHAPE MATH

def count_color_img(img, cmin, cmax):
    """Raw pixel count in color range. Used by hot-zone alerts only."""
    arr = np.array(img)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    return int(((r >= cmin[0]) & (r <= cmax[0]) &
                (g >= cmin[1]) & (g <= cmax[1]) &
                (b >= cmin[2]) & (b <= cmax[2])).sum())

def count_color(img, cmin, cmax):
    return count_color_img(img, cmin, cmax)

def _is_dot_shape(size, ys, xs):
    """v5.7: shape-compactness filter.
    Real fiber dots are roughly circular. Reject park slivers, skinny
    freeway/road markers, and oversized blobs.
    """
    if size < MIN_DOT_PIXELS or size > MAX_DOT_PIXELS:
        return False
    y_min = int(ys.min()); y_max = int(ys.max())
    x_min = int(xs.min()); x_max = int(xs.max())
    h = y_max - y_min + 1
    w = x_max - x_min + 1
    bbox_area = h * w
    if bbox_area > MAX_DOT_BBOX_AREA:
        return False
    compactness = float(size) / float(bbox_area)
    if compactness < MIN_DOT_COMPACTNESS:
        return False
    short = max(min(h, w), 1)
    aspect = float(max(h, w)) / float(short)
    if aspect > MAX_DOT_ASPECT:
        return False
    return True

def count_dot_clusters(img, cmin, cmax):
    """v5.7: connected-component count. Each cluster also passes
    shape-compactness check so park slivers and skinny markers are filtered."""
    try:
        if hasattr(img, "convert"):
            arr = np.array(img.convert("RGB"))
        else:
            arr = np.array(img)
        r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
        mask = ((r >= cmin[0]) & (r <= cmax[0]) &
                (g >= cmin[1]) & (g <= cmax[1]) &
                (b >= cmin[2]) & (b <= cmax[2]))
        labeled, num = ndimage.label(mask)
        count = 0
        for i in range(1, num + 1):
            ys, xs = np.where(labeled == i)
            sz = len(ys)
            if _is_dot_shape(sz, ys, xs):
                count += 1
        return count
    except Exception:
        return 0

def is_blank_map(img):
    """v5.7: detect blank/loading/timeout/error-state screenshots.
    Returns True if the image should NOT be classified as having dots."""
    try:
        if hasattr(img, "convert"):
            arr = np.array(img.convert("RGB"))
        else:
            arr = np.array(img)
        whole_std = float(arr.std())
        whole_mean = float(arr.mean())
        if whole_std < BLANK_STD_THRESHOLD:
            return True
        if whole_mean >= BLANK_BRIGHT_MEAN:
            return True
        if whole_mean <= BLANK_DARK_MEAN:
            return True
        h, w = arr.shape[:2]
        center = arr[h // 4 : 3 * h // 4, w // 4 : 3 * w // 4]
        if float(center.std()) < BLANK_CENTER_STD_THRESHOLD:
            return True
        return False
    except Exception:
        return True

def dots_on_screen():
    """v5.7: 3-color cluster gate. Returns (found, o_pixels, g_pixels).
    Pixel totals retained for legacy hot-zone alert math."""
    img = grab_map()
    if is_blank_map(img):
        return False, 0, 0
    o_px = count_color_img(img, ORANGE_MIN, ORANGE_MAX)
    g_px = count_color_img(img, GREEN_MIN, GREEN_MAX)
    o_clusters    = count_dot_clusters(img, ORANGE_MIN, ORANGE_MAX)
    g_clusters    = count_dot_clusters(img, GREEN_MIN,  GREEN_MAX)
    grey_clusters = count_dot_clusters(img, GREY_MIN,   GREY_MAX)
    found = (o_clusters >= MIN_DOT_CLUSTERS or
             g_clusters >= MIN_DOT_CLUSTERS or
             grey_clusters >= MIN_DOT_CLUSTERS)
    return found, o_px, g_px

def wait_for_dots(max_wait=MAX_WAIT_DOTS):
    start = time.time()
    while time.time() - start < max_wait:
        found, o, g = dots_on_screen()
        if found:
            return True, o, g
        time.sleep(POLL_INTERVAL)
    return False, 0, 0

def is_dark(path):
    try:
        return np.array(Image.open(path).convert("RGB")).mean() < 55
    except:
        return True

def find_dots(path, cmin, cmax):
    """v5.7: returns list of (x, y, cluster_size). Same shape filter as
    count_dot_clusters so detection and per-dot pickup stay consistent."""
    try:
        img = Image.open(path).convert("RGB")
        arr = np.array(img)
        r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
        mask = ((r >= cmin[0]) & (r <= cmax[0]) &
                (g >= cmin[1]) & (g <= cmax[1]) &
                (b >= cmin[2]) & (b <= cmax[2]))
        labeled, num = ndimage.label(mask)
        dots = []
        for i in range(1, num + 1):
            ys, xs = np.where(labeled == i)
            sz = len(ys)
            if _is_dot_shape(sz, ys, xs):
                dots.append((int(xs.mean()), int(ys.mean()), int(sz)))
        return dots
    except:
        return []

def pixel_to_latlng(px, py, row, col, sl, sg):
    lat = sl - (row * PAN_PIXELS * abs(LAT_PER_PIXEL)) - (py * abs(LAT_PER_PIXEL))
    lng = sg + (col * PAN_PIXELS * LNG_PER_PIXEL) + (px * LNG_PER_PIXEL)
    return round(lat, 6), round(lng, 6)


# GEOCODING (unchanged from v5.6)
_geo_cache = {}
_phone_cache = {}  # v5.8: OSM phones
_geo_lock = threading.Lock()
_geo_last = [0.0]

def load_geo_cache():
    global _geo_cache
    if os.path.exists(GEO_CACHE):
        try:
            with open(GEO_CACHE) as f:
                _geo_cache = json.load(f)
        except:
            _geo_cache = {}

def save_geo_cache():
    try:
        with open(GEO_CACHE, "w") as f:
            json.dump(_geo_cache, f)
    except:
        pass

def _rate_limit():
    with _geo_lock:
        wait = GEO_RATE - (time.time() - _geo_last[0])
        if wait > 0:
            time.sleep(wait)
        _geo_last[0] = time.time()

def _nominatim_reverse(lat, lng):
    _rate_limit()
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lng, "format": "json",
                    "addressdetails": 1, "extratags": 1, "zoom": 18},
            headers={"User-Agent": "FiberScan/1.0"},
            timeout=GEOCODE_TIMEOUT,
        )
        d = r.json()
        if "address" in d and d["address"]:
            return d
    except:
        pass
    return None

def _photon_reverse(lat, lng):
    try:
        r = requests.get(
            "https://photon.komoot.io/reverse",
            params={"lat": lat, "lon": lng, "limit": 1},
            timeout=GEOCODE_TIMEOUT,
        )
        d = r.json()
        feats = d.get("features", [])
        if feats:
            p = feats[0].get("properties", {})
            return {
                "address": {
                    "house_number": p.get("housenumber", ""),
                    "road": p.get("street", ""),
                    "city": p.get("city", "") or p.get("town", "") or p.get("locality", ""),
                    "state": p.get("state", ""),
                    "postcode": p.get("postcode", ""),
                    "amenity": p.get("name", ""),
                },
                "type": p.get("type", ""), "class": "", "addresstype": "",
            }
    except:
        pass
    return None


PHONE_TIMEOUT = 15

def get_phone_and_biz(address, city, state):
    try:
        import re as _re
        from playwright.sync_api import sync_playwright
        query = (address + " " + city + " " + state).replace(" ", "+")
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://www.google.com/maps/search/" + query,
                      timeout=PHONE_TIMEOUT * 1000)
            page.wait_for_timeout(3000)
            content = page.content()
            browser.close()
        phone = ""
        m = _re.search(r"(\+?1?[\s\(]?\d{3}[\)\-\.\s]\s*\d{3}[\-\.\s]\d{4})", content)
        if m:
            digits = _re.sub(r"[^\d]", "", m.group(1))
            if len(digits) >= 10:
                phone = digits[-10:]
        biz = ""
        bm = _re.search(r'"name":"([^"]{3,80})"', content)
        if bm:
            biz = bm.group(1).strip()
        return phone, biz
    except:
        pass
    return "", ""

def geocode(lat, lng):
    key = "%.6f,%.6f" % (lat, lng)
    with _geo_lock:
        if key in _geo_cache:
            cached = _geo_cache[key]
            return tuple(cached) if cached else None
    d = _nominatim_reverse(lat, lng)
    if not d:
        time.sleep(0.5)
        d = _nominatim_reverse(lat, lng)
    if not d:
        d = _photon_reverse(lat, lng)
    if not d or "address" not in d or not d["address"]:
        with _geo_lock:
            _geo_cache[key] = None
        return None
    a = d["address"]
    if not isinstance(a, dict):
        with _geo_lock:
            _geo_cache[key] = None
        return None
    house = a.get("house_number") or ""
    street = a.get("road") or a.get("pedestrian") or a.get("path") or ""
    city = a.get("city") or a.get("town") or a.get("village") or ""
    state = a.get("state") or ""
    state_abbrev = {
        "alabama":"AL","arkansas":"AR","california":"CA","colorado":"CO",
        "florida":"FL","georgia":"GA","iowa":"IA","idaho":"ID",
        "illinois":"IL","indiana":"IN","kansas":"KS","kentucky":"KY",
        "louisiana":"LA","michigan":"MI","missouri":"MO","mississippi":"MS",
        "north carolina":"NC","nebraska":"NE","nevada":"NV","ohio":"OH",
        "oklahoma":"OK","oregon":"OR","south carolina":"SC","tennessee":"TN",
        "texas":"TX","utah":"UT","washington":"WA","wisconsin":"WI",
    }
    if state.lower() in state_abbrev:
        state = state_abbrev[state.lower()]
    zipc = a.get("postcode") or ""
    extra = {}  # v5.17: init before loop
    biz = ""
    for k in ["amenity", "shop", "office", "building", "industrial",
              "commercial", "tourism", "healthcare", "leisure"]:
        biz = a.get(k) or ""
        if biz:
            break
    if not biz:
        extra = d.get("extratags") or {}
        if isinstance(extra, dict):
            biz = extra.get("name", "") or ""
    _osm_ph = ""
    if isinstance(extra, dict):
        _osm_ph = (extra.get("phone") or extra.get("contact:phone") or
                   extra.get("contact:mobile") or "")
        if _osm_ph:
            import re as _re
            _osm_ph = _re.sub(r"[^\d+\-\(\) ]", "", str(_osm_ph)).strip()
    if _osm_ph:
        with _geo_lock:
            _phone_cache["%.6f,%.6f" % (lat, lng)] = _osm_ph
    types = (str(d.get("type") or "") + str(d.get("class") or "") +
             str(d.get("addresstype") or "")).lower()
    if any(t in types for t in COMMERCIAL_TYPES):
        ptype = "COMMERCIAL"
    elif any(t in types for t in RESIDENTIAL_TYPES):
        ptype = "RESIDENTIAL"
    elif house:
        ptype = "RESIDENTIAL"
    else:
        ptype = "UNKNOWN"
    if house and street:
        full = "%s %s" % (house, street)
    else:
        # v5.8: no house number = write nothing
        with _geo_lock:
            _geo_cache[key] = None
        return None
    result = (full, street, city, state, zipc, ptype, biz)
    with _geo_lock:
        _geo_cache[key] = list(result)
    return result

def smart_classify(full, street, ptype, zipcode):
    if ptype == "COMMERCIAL":
        return "COMMERCIAL"
    score = 0
    sl = (street or "").lower()
    for w in COMMERCIAL_STREET_WORDS:
        if w in sl:
            score += 3
            break
    if not any(c.isdigit() for c in (full or "")[:5]) and street:
        score += 2
    if zipcode in KNOWN_COMMERCIAL_ZIPS:
        score += 2
    if score >= 3:
        return "COMMERCIAL"
    if ptype == "UNKNOWN" and score >= 2:
        return "COMMERCIAL"
    return ptype if ptype != "UNKNOWN" else "RESIDENTIAL"


# BUILT-IN CITY FALLBACK (unchanged)
BUILTIN_CITIES = {
    "houston":(29.7604,-95.3698),"austin":(30.2672,-97.7431),
    "dallas":(32.7767,-96.7970),"san antonio":(29.4241,-98.4936),
    "fort worth":(32.7555,-97.3308),"el paso":(31.7619,-106.4850),
    "atlanta":(33.7490,-84.3880),"savannah":(32.0809,-81.0912),
    "tampa":(27.9506,-82.4572),"miami":(25.7617,-80.1918),
    "orlando":(28.5383,-81.3792),"jacksonville":(30.3322,-81.6557),
    "nashville":(36.1627,-86.7816),"memphis":(35.1495,-90.0490),
    "knoxville":(35.9606,-83.9207),"chattanooga":(35.0456,-85.3097),
    "birmingham":(33.5186,-86.8104),"huntsville":(34.7304,-86.5861),
    "mobile":(30.6954,-88.0399),"montgomery":(32.3668,-86.3000),
    "new orleans":(29.9511,-90.0715),"baton rouge":(30.4515,-91.1871),
    "shreveport":(32.5252,-93.7502),"jackson":(32.2988,-90.1848),
    "biloxi":(30.3960,-88.8853),"gulfport":(30.3674,-89.0928),
    "ocean springs":(30.4113,-88.7825),
    "charlotte":(35.2271,-80.8431),"raleigh":(35.7796,-78.6382),
    "greensboro":(36.0726,-79.7920),"columbia":(34.0007,-81.0348),
    "charleston":(32.7765,-79.9311),"louisville":(38.2527,-85.7585),
    "lexington":(38.0406,-84.5037),"indianapolis":(39.7684,-86.1581),
    "chicago":(41.8781,-87.6298),"milwaukee":(43.0389,-87.9065),
    "detroit":(42.3314,-83.0458),"grand rapids":(42.9634,-85.6681),
    "cleveland":(41.4993,-81.6944),"columbus":(39.9612,-82.9988),
    "cincinnati":(39.1031,-84.5120),"st louis":(38.6270,-90.1994),
    "kansas city":(39.0997,-94.5786),"oklahoma city":(35.4676,-97.5164),
    "edmond":(35.6528,-97.4781),"midwest city":(35.4495,-97.3967),
    "choctaw":(35.4978,-97.2700),"norman":(35.2226,-97.4395),
    "tulsa":(36.1540,-95.9928),"little rock":(34.7465,-92.2896),
    "des moines":(41.5868,-93.6250),"omaha":(41.2565,-95.9345),
    "wichita":(37.6872,-97.3301),"phoenix":(33.4484,-112.0740),
    "tucson":(32.2226,-110.9747),"las vegas":(36.1699,-115.1398),
    "albuquerque":(35.0844,-106.6504),"salt lake city":(40.7608,-111.8910),
    "denver":(39.7392,-104.9903),"boise":(43.6150,-116.2023),
    "los angeles":(34.0522,-118.2437),"san francisco":(37.7749,-122.4194),
    "san diego":(32.7157,-117.1611),"san jose":(37.3382,-121.8863),
    "sacramento":(38.5816,-121.4944),"fresno":(36.7378,-119.7871),
    "seattle":(47.6062,-122.3321),"portland":(45.5152,-122.6784),
    "round rock":(30.5083,-97.6789),"kyle":(29.9893,-97.8772),
    "buda":(30.0855,-97.8403),"georgetown":(30.6333,-97.6779),
    "pflugerville":(30.4394,-97.6200),"cedar park":(30.5052,-97.8203),
}

try:
    import pgeocode
    _ZIP_DB = pgeocode.Nominatim('us')
    PGEOCODE_OK = True
except Exception:
    _ZIP_DB = None
    PGEOCODE_OK = False


def lookup_city(name):
    n = name.strip().lower()
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": name + " USA", "format": "json", "limit": 1},
            headers={"User-Agent": "FiberScan/1.0"}, timeout=6,
        )
        d = r.json()
        if d:
            return float(d[0]["lat"]), float(d[0]["lon"]), d[0].get("display_name", name)
    except:
        pass
    try:
        r = requests.get(
            "https://photon.komoot.io/api",
            params={"q": name + " USA", "limit": 1}, timeout=6,
        )
        d = r.json()
        feats = d.get("features", [])
        if feats:
            coords = feats[0]["geometry"]["coordinates"]
            return float(coords[1]), float(coords[0]), feats[0].get("properties", {}).get("name", name)
    except:
        pass
    if n in BUILTIN_CITIES:
        lat, lng = BUILTIN_CITIES[n]
        return lat, lng, name.title() + " (built-in)"
    return None, None, None

def lookup_zip(z):
    if PGEOCODE_OK:
        try:
            row = _ZIP_DB.query_postal_code(z)
            lat = float(row.latitude)
            lng = float(row.longitude)
            place = str(row.place_name) if row.place_name else z
            state = str(row.state_code) if row.state_code else ""
            if lat == lat and lng == lng:
                return lat, lng, ("%s, %s" % (place, state)).strip(", ")
        except:
            pass
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"postalcode": z, "country": "US", "format": "json", "limit": 1},
            headers={"User-Agent": "FiberScan/1.0"}, timeout=6,
        )
        d = r.json()
        if d:
            return float(d[0]["lat"]), float(d[0]["lon"]), d[0].get("display_name", z)
    except:
        pass
    try:
        r = requests.get(
            "https://photon.komoot.io/api",
            params={"q": z + " USA", "limit": 1}, timeout=6,
        )
        d = r.json()
        feats = d.get("features", [])
        if feats:
            coords = feats[0]["geometry"]["coordinates"]
            return float(coords[1]), float(coords[0]), z
    except:
        pass
    return None, None, None

def get_city():
    while True:
        e = input("\nEnter city or ZIP to start spiral from: ").strip()
        if not e:
            continue
        if e.isdigit() and len(e) == 5:
            lat, lng, name = lookup_zip(e)
        else:
            lat, lng, name = lookup_city(e)
        if lat is None:
            print("  Not found. Try again.")
            continue
        print("  Found: %s" % name)
        short_name = name.split(",")[0].strip() if "," in name else name
        return lat, lng, short_name


# SHEETS - v5.7 schema with header migration
TAB_HEADERS = {
    "Hunter Leads": [
        "Address", "Business Name", "Dot Type", "Property Type",
        "City", "State", "Zip", "Zone", "Instance", "Scan #",
        "Status", "Rep", "Date", "Phone", "Lat", "Lng",
        "Verified Color", "Dot Confidence", "Source Screenshot", "Scan Status",
    ],
    "Hunter Green Commercial": [
        "Address", "Business Name", "City", "State", "Zip",
        "Zone", "Instance", "Scan #", "Date", "Phone", "Lat", "Lng",
        "Verified Color",
    ],
    "Hunter Green Residential": [
        "Address", "City", "State", "Zip",
        "Zone", "Instance", "Scan #", "Date", "Lat", "Lng",
        "Verified Color",
    ],
    "Hunter Commercial": [
        "Address", "Business Name", "Dot Type", "City", "State", "Zip",
        "Zone", "Instance", "Scan #", "Status", "Rep", "Date", "Phone", "Notes",
        "Verified Color",
    ],
    "Hunter Residential": [
        "Address", "Dot Type", "City", "State", "Zip",
        "Zone", "Instance", "Scan #", "Status", "Rep", "Date",
        "Verified Color",
    ],
    "Hunter Hot Zones": [
        "Date", "Zone", "City", "Instance", "Change", "Details",
        "Scan #", "Action",
    ],
    "Hunter Changes": [
        "Date", "Address", "Change", "Details", "Zone", "City",
        "Instance", "Scan #",
    ],
}

def connect_sheets():
    if not os.path.exists(CREDS_FILE):
        print("No google_creds.json - Sheets disabled.")
        return None
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets",
                  "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(CREDS_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        ss = client.open(SHEET_NAME)
        existing = [ws.title for ws in ss.worksheets()]
        tabs = {}
        for tname, headers in TAB_HEADERS.items():
            if tname not in existing:
                ws = ss.add_worksheet(title=tname, rows=1000, cols=max(20, len(headers)))
                ws.append_row(headers)
            else:
                ws = ss.worksheet(tname)
                try:
                    current = ws.row_values(1)
                    if len(current) < len(headers):
                        new_cols = headers[len(current):]
                        full_row = list(current) + new_cols
                        ws.update(values=[full_row], range_name="A1")
                        print("  Extended headers for %s: +%d cols (%s)"
                              % (tname, len(new_cols), ", ".join(new_cols)))
                except Exception as he:
                    print("  Header migration warn (%s): %s" % (tname, he))
            tabs[tname] = ws
        print("Connected to Google Sheets.")
        return tabs
    except Exception as e:
        print("Sheets error: %s" % e)
        return None

def get_existing(tabs):
    """v5.7: returns dict[address] -> set(dot_types). Lowercase-tolerant."""
    existing = {}
    if not tabs:
        return existing
    try:
        vals = tabs["Hunter Leads"].get_all_values()
        if not vals:
            return existing
        header = vals[0]
        try:
            vc_idx = header.index("Verified Color")
        except ValueError:
            vc_idx = -1
        for row in vals[1:]:
            if not row or not row[0]:
                continue
            addr = row[0].strip()
            if vc_idx >= 0 and vc_idx < len(row) and row[vc_idx].strip():
                vc = row[vc_idx].strip().lower()
                if vc == "green":
                    dot = "FIBER ELIGIBLE (Green)"
                elif vc == "gold":
                    dot = "UPGRADE ELIGIBLE (Gold/Orange)"
                elif vc == "grey" or vc == "gray":
                    dot = GREY_DOT_TYPE
                else:
                    dot = row[2].strip() if len(row) > 2 else ""
            else:
                dot = row[2].strip() if len(row) > 2 else ""
            existing.setdefault(addr, set()).add(dot)
    except Exception as e:
        print("  get_existing warn: %s" % e)
    print("Loaded %d existing hunter addresses" % len(existing))
    return existing

_buffers = {}
_buf_lock = threading.Lock()

def sheet_write(tabs, tab, row, addr=""):
    if not tabs:
        return
    with _buf_lock:
        _buffers.setdefault(tab, []).append(row)
        n = len(_buffers[tab])
    print("  SHEET: wrote to %s: %s" % (tab, addr or (row[0] if row else "")))
    if n >= BATCH_SIZE:
        with _buf_lock:
            _flush(tabs, tab)

def _flush(tabs, tab):
    buf = _buffers.get(tab, [])
    if buf and tabs:
        try:
            tabs[tab].append_rows(buf)
            time.sleep(0.6)
        except Exception as e:
            print("  write err %s: %s" % (tab, e))
        _buffers[tab] = []

def flush_all(tabs):
    if not tabs:
        return
    with _buf_lock:
        for tab in list(_buffers.keys()):
            _flush(tabs, tab)

def log_sheet(tabs, tab, row):
    if not tabs:
        return
    try:
        tabs[tab].append_row(row)
    except:
        pass

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return {}

def save_history(h):
    with open(HISTORY_FILE, "w") as f:
        json.dump(h, f, indent=2)


# HOT-ZONE ALERTS (unchanged from v5.6 - still pixel-total based)
def check_hot_zone(zone_name, city, row, col, o, g, b, history, tabs, scan_num, instance):
    key = "%s_%d_%d" % (zone_name, row, col)
    now = now_str()
    inst = "Instance%d" % instance
    alerts = []
    has = (o >= CLUSTER_THRESHOLD) or (g >= CLUSTER_THRESHOLD)
    if (g >= GREENFIELD_GREEN_MIN and o <= GREENFIELD_GOLD_MAX
            and b <= GREENFIELD_BLUE_MAX):
        prev_gf = history.get(key, {}).get("greenfield", False)
        if not prev_gf:
            msg = ("GREENFIELD ZONE %s R%dC%d Green:%d Gold:%d Blue:%d"
                   % (zone_name, row + 1, col + 1, g, o, b))
            alerts.append(msg)
            log_sheet(tabs, "Hunter Hot Zones", [
                now, zone_name, city, inst, "GREENFIELD ZONE",
                "G:%d O:%d B:%d" % (g, o, b),
                str(scan_num), "PRIORITY 1 - KNOCK FIRST",
            ])
        history.setdefault(key, {})["greenfield"] = True
    else:
        if key in history:
            history[key]["greenfield"] = False
    if key in history:
        prev = history[key]
        was_empty = prev.get("empty", True)
        if was_empty and has and b < CLUSTER_THRESHOLD:
            alerts.append("NEW FIBER %s R%dC%d G:%d O:%d" %
                          (zone_name, row + 1, col + 1, g, o))
            log_sheet(tabs, "Hunter Hot Zones", [
                now, zone_name, city, inst, "NEW FIBER ZONE",
                "Was empty now %dG+%dO" % (g, o),
                str(scan_num), "PRIORITY 1 - TODAY",
            ])
        elif prev.get("orange", 0) >= CLUSTER_THRESHOLD and o < CLUSTER_THRESHOLD:
            alerts.append("GOLD GONE %s R%dC%d" %
                          (zone_name, row + 1, col + 1))
            log_sheet(tabs, "Hunter Changes", [
                now, "", "CONVERSIONS", "Gold dropped",
                zone_name, city, inst, str(scan_num),
            ])
        elif o > prev.get("orange", 0) + 300:
            alerts.append("GOLD SURGE %s R%dC%d" %
                          (zone_name, row + 1, col + 1))
            log_sheet(tabs, "Hunter Hot Zones", [
                now, zone_name, city, inst, "GOLD SURGE",
                "Was %d now %d" % (prev.get("orange", 0), o),
                str(scan_num), "PRIORITY 2",
            ])
    history.setdefault(key, {}).update({
        "orange": o, "green": g, "blue": b,
        "empty": not has, "ts": now,
    })
    return alerts


# PROCESSOR - v5.7 four-state classification
class Processor:
    def __init__(self, tabs, existing, history, scan_num, instance):
        self.tabs = tabs
        self.existing = existing
        self.history = history
        self.scan_num = scan_num
        self.instance = instance
        self.inst_tag = "Instance%d" % instance
        self.q = queue.Queue()
        self.running = True
        self.counters = {
            "new": 0, "skip": 0, "hot": 0, "failed": 0,
            "o_res": 0, "o_comm": 0, "g_res": 0, "g_comm": 0,
            "greenfield": 0,
            "blank_skip": 0,
            "park_skip": 0,
            "grey": 0,
            "green_over_gold": 0,
            "green_over_grey": 0,
            "gold_over_grey": 0,
        }
        self.t = threading.Thread(target=self._run, daemon=True)
        self.t.start()
        print("  Background processor started")

    def submit(self, shot, zone, city, row, col, ts):
        if not hasattr(self,"_submitted_shots"): self._submitted_shots=set()
        self._submitted_shots.add(shot)
        self.q.put((shot, zone, city, row, col, ts))

    def _run(self):
        while self.running or not self.q.empty():
            try:
                item = self.q.get(timeout=1.0)
            except queue.Empty:
                continue
            try:
                self._process(*item)
            except Exception as e:
                print("  bg err: %s" % e)
            self.q.task_done()

    def _process(self, shot, zone, city, row, col, ts):
        # GATE 1: dark/black timeout
        if is_dark(shot):
            self.counters["blank_skip"] += 1
            return

        zone_name = zone["name"]
        sl = zone["start_lat"]
        sg = zone["start_lng"]

        try:
            img = Image.open(shot).convert("RGB")
        except:
            self.counters["blank_skip"] += 1
            return

        # GATE 2: blank/loading/uniform
        if is_blank_map(img):
            self.counters["blank_skip"] += 1
            print("  BLANK skip [I%d %s R%dC%d]" %
                  (self.instance, zone_name, row + 1, col + 1))
            return

        # Pixel totals retained for hot-zone alerts
        o_px = count_color(img, ORANGE_MIN, ORANGE_MAX)
        g_px = count_color(img, GREEN_MIN,  GREEN_MAX)
        b_px = count_color(img, BLUE_MIN,   BLUE_MAX)

        # Real cluster counts gate row writes (3-color)
        o_clusters    = count_dot_clusters(img, ORANGE_MIN, ORANGE_MAX)
        g_clusters    = count_dot_clusters(img, GREEN_MIN,  GREEN_MAX)
        grey_clusters = count_dot_clusters(img, GREY_MIN,   GREY_MAX)

        alerts = check_hot_zone(zone_name, city, row, col, o_px, g_px, b_px,
                                self.history, self.tabs, self.scan_num, self.instance)
        self.counters["hot"] += len(alerts)
        for a in alerts:
            if "GREENFIELD" in a:
                self.counters["greenfield"] += 1
            print("  !! %s" % a)

        # GATE 3: zero clusters of any color = parks/empty
        if (o_clusters    < MIN_DOT_CLUSTERS and
            g_clusters    < MIN_DOT_CLUSTERS and
            grey_clusters < MIN_DOT_CLUSTERS):
            self.counters["park_skip"] += 1
            return

        o_dots    = find_dots(shot, ORANGE_MIN, ORANGE_MAX)
        g_dots    = find_dots(shot, GREEN_MIN,  GREEN_MAX)
        grey_dots = find_dots(shot, GREY_MIN,   GREY_MAX)

        # Priority order: Green > Gold > Grey
        all_dots = ([("FIBER ELIGIBLE (Green)",        d) for d in g_dots]    +
                    [("UPGRADE ELIGIBLE (Gold/Orange)", d) for d in o_dots])

        shot_basename = os.path.basename(shot)

        for dot_type, dot in all_dots:
            px, py, cluster_size = dot
            lat, lng = pixel_to_latlng(px, py, row, col, sl, sg)
            res = geocode(lat, lng)
            if res is None:
                self.counters["failed"] += 1
                continue
            full, street, gcity, state, zipc, ptype, biz = res
            ptype = smart_classify(full, street, ptype, zipc)
            if ptype == "COMMERCIAL" and zipc:
                KNOWN_COMMERCIAL_ZIPS.add(zipc)

            # v5.7: lowercase classification
            dot_lower = dot_type.lower()
            is_green = "green" in dot_lower
            is_gold  = "gold"  in dot_lower
            is_grey  = "grey"  in dot_lower
            verified_color = ("GREEN" if is_green else
                              ("GOLD" if is_gold else "GREY"))

            existing_types = self.existing.get(full, set())
            existing_lower = [t.lower() for t in existing_types]
            has_green = any("green" in t for t in existing_lower)
            has_gold  = any("gold"  in t for t in existing_lower)
            has_grey  = any("grey"  in t for t in existing_lower)

            scan_status = "OK"

            # SKIP rules (existing wins unless incoming is stronger)
            if is_green and has_green:
                self.counters["skip"] += 1; continue
            if is_gold and (has_gold or has_green):
                self.counters["skip"] += 1; continue
            if is_grey and (has_grey or has_gold or has_green):
                self.counters["skip"] += 1; continue

            # UPGRADE annotations
            if is_green and has_gold:
                self.counters["green_over_gold"] += 1
                scan_status = "GREEN_OVER_GOLD"
            elif is_green and has_grey and not has_gold:
                self.counters["green_over_grey"] += 1
                scan_status = "GREEN_OVER_GREY"
            elif is_gold and has_grey and not has_green:
                self.counters["gold_over_grey"] += 1
                scan_status = "GOLD_OVER_GREY"
            elif is_grey:
                scan_status = "SOCIAL_PROOF"

            self.existing.setdefault(full, set()).add(dot_type)
            self.counters["new"] += 1
            phone = _phone_cache.get("%.6f,%.6f" % (lat, lng), "")
            if (is_green or (is_gold and ptype == "COMMERCIAL")) and not phone:
                try:
                    _p, _b = get_phone_and_biz(full, gcity, state)
                    if _p: phone = _p
                    if _b and not biz: biz = _b
                except: pass
            tag = "GREY" if is_grey else ("COMM" if ptype == "COMMERCIAL" else "RES")
            print("  %s [I%d]: %s %s" % (
                tag, self.instance, full[:50],
                ("[%s]" % biz) if biz else "",
            ))
            inst = self.inst_tag
            now = now_str()

            # Hunter Leads master gets every classified row
            sheet_write(self.tabs, "Hunter Leads", [
                full, biz, dot_type, ptype, gcity, state, zipc,
                zone_name, inst, str(self.scan_num), "New", REP_NAME, now,
                phone, str(lat), str(lng),
                verified_color, str(cluster_size), shot_basename, scan_status,
            ], full)

            # v5.7: Grey stays in master only - never pollutes verticals
            if is_grey:
                self.counters["grey"] += 1
                continue

            if ptype == "COMMERCIAL":
                if is_green:
                    self.counters["g_comm"] += 1
                else:
                    self.counters["o_comm"] += 1
                sheet_write(self.tabs, "Hunter Commercial", [
                    full, biz, dot_type, gcity, state, zipc,
                    zone_name, inst, str(self.scan_num), "New", REP_NAME, now,
                    phone, "", verified_color,
                ], full)
                if is_green:
                    sheet_write(self.tabs, "Hunter Green Commercial", [
                        full, biz, gcity, state, zipc,
                        zone_name, inst, str(self.scan_num), now, phone,
                        str(lat), str(lng), verified_color,
                    ], full)
            else:
                if is_green:
                    self.counters["g_res"] += 1
                else:
                    self.counters["o_res"] += 1
                sheet_write(self.tabs, "Hunter Residential", [
                    full, dot_type, gcity, state, zipc,
                    zone_name, inst, str(self.scan_num), "New", REP_NAME, now,
                    verified_color,
                ], full)
                if is_green:
                    sheet_write(self.tabs, "Hunter Green Residential", [
                        full, gcity, state, zipc,
                        zone_name, inst, str(self.scan_num), now,
                        str(lat), str(lng), verified_color,
                    ], full)

    def stop(self):
        self.running = False
        self.t.join(timeout=120)
        flush_all(self.tabs)
        save_history(self.history)
        save_geo_cache()


# PROGRESS / MOTION (unchanged from v5.6)
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE) as f:
                return json.load(f)
        except:
            pass
    return {"zone_seq": 0, "row": 0, "col": 0, "scan_num": 1}

def save_progress(p):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(p, f)

def pan(direction):
    pyautogui.moveTo(MAP_CX, MAP_CY)
    if direction == "right":
        pyautogui.drag(-PAN_PIXELS, 0, duration=0.2, button="left", _pause=False)
    elif direction == "left":
        pyautogui.drag(PAN_PIXELS, 0, duration=0.2, button="left", _pause=False)
    elif direction == "down":
        pyautogui.drag(0, -PAN_PIXELS, duration=0.2, button="left", _pause=False)
    time.sleep(WAIT_AFTER_PAN)

def upload_screenshot_to_drive(local_path):
    """v5.9: upload PNG to Drive so all machines share screenshots."""
    try:
        import google.auth.transport.requests as _gtr
        _scopes = ["https://www.googleapis.com/auth/drive"]
        _creds = Credentials.from_service_account_file(CREDS_FILE, scopes=_scopes)
        _creds.refresh(_gtr.Request())
        _token = _creds.token
        _fname = os.path.basename(local_path)
        with open(local_path, "rb") as _f:
            _img = _f.read()
        _bnd = "fhboundary"
        _meta = json.dumps({"name": _fname,
                            "parents": [DRIVE_SCREENSHOTS_FOLDER]}).encode()
        _ext = os.path.splitext(local_path)[1].lower()
        _mime = {".png":"image/png",".json":"application/json"}.get(
            _ext,"application/octet-stream")  # v5.17
        _body = (b"--" + _bnd.encode() + b"\r\n"
                 b"Content-Type: application/json; charset=UTF-8\r\n\r\n" +
                 _meta + b"\r\n"
                 b"--" + _bnd.encode() + b"\r\n"
                 + ("Content-Type: %s\r\n\r\n" % _mime).encode() +
                 _img + b"\r\n"
                 b"--" + _bnd.encode() + b"--")
        requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers={"Authorization": "Bearer " + _token,
                     "Content-Type": "multipart/related; boundary=" + _bnd},
            data=_body, timeout=20)
    except Exception:
        pass

def screenshot(scan_num, zone_name, row, col, instance, zone_obj=None):
    ts = datetime.now().strftime("%H%M%S")
    fn = os.path.join(SCREENSHOTS_DIR,
        "i%d_scan%02d_%s_r%02d_c%02d_%s.png" % (
            instance, scan_num, zone_name, row, col, ts))
    pyautogui.screenshot(fn)
    upload_screenshot_to_drive(fn)  # v5.9
    if zone_obj:
        try:
            sc = fn.replace(".png",".json")
            with open(sc,"w") as _sf:
                json.dump({"zone":zone_obj,"row":row,"col":col,
                    "scan_num":scan_num,"instance":instance},_sf)
            upload_screenshot_to_drive(sc)  # v5.17 MIME-correct
        except: pass
    return fn

def scan_cell(zone, city, row, col, btn_x, btn_y, processor, scan_num, instance):
    pyautogui.click(btn_x, btn_y)
    found, o, g = wait_for_dots()
    shot = screenshot(scan_num, zone["name"], row, col, instance, zone_obj=zone)
    print("  [I%d %s R%dC%d] O:%d G:%d" % (
        instance, zone["name"], row + 1, col + 1, o, g))
    processor.submit(shot, zone, city, row, col, now_str())

def scan_zone(zone, city, start_row, start_col, btn_x, btn_y,
              processor, scan_num, instance, zone_seq):
    name = zone["name"]
    cols = zone["cols"]
    rows = zone["rows"]
    direction = 1
    print("\n" + "=" * 50)
    print("ZONE #%d: %s  (%dx%d)" % (zone_seq, name, cols, rows))
    print("=" * 50)
    for row in range(start_row, rows):
        if direction == 1:
            col_iter = range(start_col if row == start_row else 0, cols)
        else:
            col_iter = range(cols - 1, -1, -1)
        for col in col_iter:
            save_progress({"zone_seq": zone_seq, "row": row, "col": col,
                           "scan_num": scan_num})
            scan_cell(zone, city, row, col, btn_x, btn_y, processor, scan_num, instance)
            if col < cols - 1 and direction == 1:
                pan("right")
            elif col > 0 and direction == -1:
                pan("left")
        if row < rows - 1:
            pan("down")
            direction *= -1


def reprocess_screenshots(processor):
    import glob
    manifest = load_processed_manifest()
    submitted = getattr(processor,"_submitted_shots",set())
    pending = [p for p in sorted(glob.glob(os.path.join(SCREENSHOTS_DIR,"*.png")))
               if os.path.basename(p) not in manifest and p not in submitted]
    if not pending:
        print("  Auto-reprocess: nothing new."); return
    viable = []
    for p in pending:
        sc = p.replace(".png",".json")
        if os.path.exists(sc):
            try:
                m = json.load(open(sc))
                if "zone" in m and "start_lat" in m.get("zone",{}):
                    viable.append((p,m))
            except: pass
    if not viable:
        print("  Auto-reprocess: no valid sidecars (v5.17+ only)."); return
    print("\n  Auto-reprocess: %d screenshots..." % len(viable))
    done = set()
    for p,m in viable:
        processor.submit(p,m["zone"],"reprocess",m["row"],m["col"],
                         __import__("datetime").datetime.now().strftime("%m/%d/%Y %I:%M %p"))
        done.add(os.path.basename(p))
    processor.q.join()
    manifest.update(done)
    save_processed_manifest(manifest)
    try: upload_screenshot_to_drive(PROCESSED_MANIFEST)
    except: pass
    print("  Done. Manifest: %d total." % len(manifest))


# MAIN
def main():
    check_update()
    print("\n" + "#" * 60)
    print("  FIBER HUNTER v%s SHIP-WITH-FIX" % VERSION)
    print("  4-state Green/Gold/Grey/Blank + shape filter + lowercase dedup")
    print("#" * 60)
    if PGEOCODE_OK:
        print("  ZIP lookup: pgeocode (offline) OK")
    else:
        print("  ZIP lookup: API only")

    lat, lng, city_name = get_city()
    btn_x, btn_y = calibrate_search_button()
    tabs = connect_sheets()
    existing = get_existing(tabs)
    history = load_history()
    progress = load_progress()
    load_geo_cache()
    instance = 1
    scan_num = progress.get("scan_num", 1)
    start_zone_seq = progress.get("zone_seq", 0)
    start_row = progress.get("row", 0)
    start_col = progress.get("col", 0)
    if start_zone_seq > 0 or start_row > 0 or start_col > 0:
        print("\nResume from zone seq %d, R%d C%d?" % (
            start_zone_seq, start_row + 1, start_col + 1))
        if input("(y/n): ").strip().lower() != "y":
            start_zone_seq = 0
            start_row = 0
            start_col = 0
            save_progress({"zone_seq": 0, "row": 0, "col": 0,
                           "scan_num": scan_num})
    print("\n" + "=" * 60)
    print("READY  |  Spiraling from current map position")
    print("Pan: %d px  |  Zone: %dx%d" % (
        PAN_PIXELS, COLS_PER_ZONE, ROWS_PER_ZONE))
    print("\n[!] Make sure youachieve.att.com is OPEN and showing your area.")
    print("\nStarting in %d sec." % START_DELAY)
    print("Ctrl+C to stop.  Picks up next time.")
    print("=" * 60)
    time.sleep(START_DELAY)
    processor = Processor(tabs, existing, history, scan_num, instance)
    try:
        for zone_seq, (ox, oy, dirname) in enumerate(spiral_offsets()):
            if zone_seq < start_zone_seq:
                continue
            zone = zone_at(lat, lng, city_name.replace(" ", "")[:10],
                           ox, oy, dirname)
            scan_zone(zone, city_name,
                start_row if zone_seq == start_zone_seq else 0,
                start_col if zone_seq == start_zone_seq else 0,
                btn_x, btn_y, processor, scan_num, instance, zone_seq)
            save_progress({"zone_seq": zone_seq + 1, "row": 0, "col": 0,
                           "scan_num": scan_num})
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        print("\nFinishing background processing...")
        processor.q.join()
        reprocess_screenshots(processor)  # v5.17
        processor.stop()
    c = processor.counters
    print("\n" + "=" * 60)
    print("DONE")
    print("New: %d | Skipped dups: %d | Hot zones: %d | Greenfield: %d" % (
        c["new"], c["skip"], c["hot"], c["greenfield"]))
    print("Blank/timeout rejected: %d | Park/no-cluster rejected: %d" % (
        c["blank_skip"], c["park_skip"]))
    print("Grey social-proof rows: %d" % c["grey"])
    print("Green-over-Gold: %d | Green-over-Grey: %d | Gold-over-Grey: %d" % (
        c["green_over_gold"], c["green_over_grey"], c["gold_over_grey"]))
    print("Geocode failures (skipped): %d" % c["failed"])
    print("GOLD: Res=%d Comm=%d  |  GREEN: Res=%d Comm=%d" % (
        c["o_res"], c["o_comm"], c["g_res"], c["g_comm"]))
    print("=" * 60)


if __name__ == "__main__":
    main()

