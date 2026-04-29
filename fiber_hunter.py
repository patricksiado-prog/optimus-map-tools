"""
FIBER HUNTER v5.0 - fiber_scan unchained from Houston
=========================================================
EXACT same engine as fiber_scan v10.0:
  - Same expanding spiral motion
  - Same dot detection (freeway-safe orange)
  - Same hot zone alerts (Greenfield, New Fiber, Gold Surge, Conversions)
  - Same geocoding + background processor
  - Same Google Sheet writes
  - Same resume on Ctrl+C

DIFFERENT from fiber_scan:
  - No PRESET_CITIES dict (asks fresh every run, no Houston defaults)
  - No CITY_FILE (never remembers last city — clean slate each time)
  - Separate state files (hunter_*.json) so it doesn't conflict
    with fiber_scan running on the same machine
  - Separate sheet tabs ("Hunter Leads", "Hunter Green", etc.)
  - Different progress + history files (own state)

WORKFLOW:
  1. Ask ChatGPT/news for hot AT&T fiber ZIPs (any city, any state)
  2. Run: python fiber_hunter.py
  3. Type the ZIP or city name
  4. Calibrate "Search this area" button (or use saved)
  5. Spiral begins — expanding zones forever until Ctrl+C
  6. Leads land in your sheet under Hunter tabs

USAGE:
  pip install pyautogui pillow scipy numpy requests gspread google-auth
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
VERSION = "5.6"

# ── AUTO-UPDATER (same pattern as fiber_scan v10.0) ────────────────
AUTO_UPDATE = True
GITHUB_REPO = "patricksiado-prog/optimus-map-tools"
GITHUB_FILE = "fiber_hunter.py"
GITHUB_BRANCH = "main"

def check_update():
    """Pull latest fiber_hunter.py from GitHub and self-update."""
    if not AUTO_UPDATE:
        return
    try:
        url = ("https://raw.githubusercontent.com/%s/%s/%s"
               % (GITHUB_REPO, GITHUB_BRANCH, GITHUB_FILE))
        print("Checking for updates...")
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            print("  Update check failed (HTTP %d), continuing"
                  % r.status_code)
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
            print("  Local v%s is newer than remote v%s"
                  % (VERSION, remote_version))
            return
        print("  Updating to v%s..." % remote_version)
        with open(__file__, "w", encoding="utf-8") as f:
            f.write(remote_code)
        print("  Updated! Restarting...")
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print("  Update err (continuing): %s" % str(e)[:100])


# ── CONFIG ─────────────────────────────────────────────────────────
CREDS_FILE = "google_creds.json"
SHEET_NAME = "ATT FIBER LEADS"

# Hunter has its OWN files — won't conflict with fiber_scan
SCREENSHOTS_DIR = "hunter_screenshots"
PROGRESS_FILE = "hunter_progress.json"
HISTORY_FILE = "hunter_zone_history.json"
BUTTON_FILE = "hunter_button_pos.json"
GEO_CACHE = "hunter_geocode_cache.json"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# ── TIMING / MOTION (matched to fiber_scan v10.0) ────────────────
WAIT_AFTER_PAN = 1.5
MAX_WAIT_DOTS = 6.0
POLL_INTERVAL = 0.12
PAN_PIXELS = 150
MIN_DOT_PIXELS = 3
CLUSTER_THRESHOLD = 15
START_DELAY = 10
BATCH_SIZE = 12
GEOCODE_TIMEOUT = 7
PHONE_TIMEOUT = 3
GEO_RATE = 1.2

GREENFIELD_GREEN_MIN = 80
GREENFIELD_GOLD_MAX = 20
GREENFIELD_BLUE_MAX = 30

MAP_LEFT, MAP_TOP, MAP_RIGHT, MAP_BOTTOM = 50, 100, 1350, 720
MAP_CX = (MAP_LEFT + MAP_RIGHT) // 2
MAP_CY = (MAP_TOP + MAP_BOTTOM) // 2

# Color ranges (matched to fiber_scan v10.0 - freeway-safe)
ORANGE_MIN = (220, 160, 0)
ORANGE_MAX = (255, 200, 60)
GREEN_MIN = (30, 130, 30)
GREEN_MAX = (100, 210, 80)
BLUE_MIN = (50, 80, 180)
BLUE_MAX = (120, 160, 255)

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

# NO PRESET_CITIES — every run asks fresh.
# Look up via Nominatim every time. Out-of-town hunting needs zero bias.

def now_str():
    return datetime.now().strftime("%m/%d/%Y %I:%M %p")

def spiral_offsets():
    """Infinite expanding-square spiral. Yields (offset_x, offset_y, label).
    Same as fiber_scan — runs forever until Ctrl+C breaks the loop."""
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

def count_color_img(img, cmin, cmax):
    arr = np.array(img)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    return int(((r >= cmin[0]) & (r <= cmax[0]) &
                (g >= cmin[1]) & (g <= cmax[1]) &
                (b >= cmin[2]) & (b <= cmax[2])).sum())

def dots_on_screen():
    img = grab_map()
    o = count_color_img(img, ORANGE_MIN, ORANGE_MAX)
    g = count_color_img(img, GREEN_MIN, GREEN_MAX)
    return (o >= CLUSTER_THRESHOLD or g >= CLUSTER_THRESHOLD), o, g

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

def count_color(img, cmin, cmax):
    return count_color_img(img, cmin, cmax)

def find_dots(path, cmin, cmax):
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
            if len(ys) >= MIN_DOT_PIXELS:
                dots.append((int(xs.mean()), int(ys.mean())))
        return dots
    except:
        return []

def pixel_to_latlng(px, py, row, col, sl, sg):
    lat = sl - (row * PAN_PIXELS * abs(LAT_PER_PIXEL)) - (py * abs(LAT_PER_PIXEL))
    lng = sg + (col * PAN_PIXELS * LNG_PER_PIXEL) + (px * LNG_PER_PIXEL)
    return round(lat, 6), round(lng, 6)

_geo_cache = {}
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
    # No "Houston" fallback — let geocoder return whatever city it actually is
    city = a.get("city") or a.get("town") or a.get("village") or ""
    state = a.get("state") or ""
    # Convert "Texas" to "TX" but otherwise keep state names as-is
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
    elif street:
        full = "%s (no #)" % street
    else:
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

# Built-in city fallback (lat, lng) for when Nominatim is rate-limited/down.
# Covers most AT&T fiber footprint cities.
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
    "charlotte":(35.2271,-80.8431),"raleigh":(35.7796,-78.6382),
    "greensboro":(36.0726,-79.7920),"columbia":(34.0007,-81.0348),
    "charleston":(32.7765,-79.9311),"louisville":(38.2527,-85.7585),
    "lexington":(38.0406,-84.5037),"indianapolis":(39.7684,-86.1581),
    "chicago":(41.8781,-87.6298),"milwaukee":(43.0389,-87.9065),
    "detroit":(42.3314,-83.0458),"grand rapids":(42.9634,-85.6681),
    "cleveland":(41.4993,-81.6944),"columbus":(39.9612,-82.9988),
    "cincinnati":(39.1031,-84.5120),"st louis":(38.6270,-90.1994),
    "kansas city":(39.0997,-94.5786),"oklahoma city":(35.4676,-97.5164),
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
# Offline ZIP lookup via pgeocode — covers EVERY US ZIP, no API needed.
# pip install pgeocode (one-time, then it's offline + instant)
try:
    import pgeocode
    _ZIP_DB = pgeocode.Nominatim('us')
    PGEOCODE_OK = True
except Exception:
    _ZIP_DB = None
    PGEOCODE_OK = False


def lookup_city(name):
    """Try Nominatim → Photon → built-in fallback dict."""
    n = name.strip().lower()
    # Try Nominatim
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
    # Try Photon
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
    # Built-in fallback
    if n in BUILTIN_CITIES:
        lat, lng = BUILTIN_CITIES[n]
        return lat, lng, name.title() + " (built-in)"
    return None, None, None


def lookup_zip(z):
    """pgeocode (offline, every US ZIP) → Nominatim → Photon."""
    # Primary: pgeocode offline DB — fastest, most reliable, covers every US ZIP
    if PGEOCODE_OK:
        try:
            row = _ZIP_DB.query_postal_code(z)
            lat = float(row.latitude)
            lng = float(row.longitude)
            place = str(row.place_name) if row.place_name else z
            state = str(row.state_code) if row.state_code else ""
            # pgeocode returns NaN floats for invalid ZIPs
            if lat == lat and lng == lng:  # NaN check
                return lat, lng, f"{place}, {state}".strip(", ")
        except:
            pass
    # Fallback 1: Nominatim
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
    # Fallback 2: Photon
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
    """No CITY_FILE memory — fresh prompt every run.
    Out-of-town hunter has zero bias toward any past location."""
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
        # Trim long display names like "78702, East Austin, Travis County, Texas, USA"
        # to just first comma-separated chunk for cleaner zone naming
        short_name = name.split(",")[0].strip() if "," in name else name
        return lat, lng, short_name

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
        # SEPARATE tabs from fiber_scan — prefixed with "Hunter"
        configs = {
            "Hunter Leads": ["Address", "Business Name", "Dot Type", "Property Type",
                             "City", "State", "Zip", "Zone", "Instance", "Scan #",
                             "Status", "Rep", "Date", "Phone", "Lat", "Lng"],
            "Hunter Green Commercial": ["Address", "Business Name", "City", "State", "Zip",
                                        "Zone", "Instance", "Scan #", "Date", "Phone", "Lat", "Lng"],
            "Hunter Green Residential": ["Address", "City", "State", "Zip",
                                         "Zone", "Instance", "Scan #", "Date", "Lat", "Lng"],
            "Hunter Commercial": ["Address", "Business Name", "Dot Type", "City", "State", "Zip",
                                  "Zone", "Instance", "Scan #", "Status", "Rep", "Date", "Phone", "Notes"],
            "Hunter Residential": ["Address", "Dot Type", "City", "State", "Zip",
                                   "Zone", "Instance", "Scan #", "Status", "Rep", "Date"],
            "Hunter Hot Zones": ["Date", "Zone", "City", "Instance", "Change", "Details",
                                 "Scan #", "Action"],
            "Hunter Changes": ["Date", "Address", "Change", "Details", "Zone", "City",
                               "Instance", "Scan #"],
        }
        for tname, headers in configs.items():
            if tname not in existing:
                ws = ss.add_worksheet(title=tname, rows=1000, cols=20)
                ws.append_row(headers)
            else:
                ws = ss.worksheet(tname)
            tabs[tname] = ws
        print("Connected to Google Sheets.")
        return tabs
    except Exception as e:
        print("Sheets error: %s" % e)
        return None

def get_existing(tabs):
    existing = set()
    if not tabs:
        return existing
    try:
        vals = tabs["Hunter Leads"].get_all_values()
        for row in vals[1:]:
            if row and row[0]:
                key = "%s|%s" % (row[0].strip(),
                                 row[2].strip() if len(row) > 2 else "")
                existing.add(key)
    except:
        pass
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
        }
        self.t = threading.Thread(target=self._run, daemon=True)
        self.t.start()
        print("  Background processor started")

    def submit(self, shot, zone, city, row, col, ts):
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
        if is_dark(shot):
            return
        zone_name = zone["name"]
        sl = zone["start_lat"]
        sg = zone["start_lng"]
        try:
            img = Image.open(shot).convert("RGB")
        except:
            return
        o_px = count_color(img, ORANGE_MIN, ORANGE_MAX)
        g_px = count_color(img, GREEN_MIN, GREEN_MAX)
        b_px = count_color(img, BLUE_MIN, BLUE_MAX)
        alerts = check_hot_zone(zone_name, city, row, col, o_px, g_px, b_px,
                                self.history, self.tabs, self.scan_num, self.instance)
        self.counters["hot"] += len(alerts)
        for a in alerts:
            if "GREENFIELD" in a:
                self.counters["greenfield"] += 1
            print("  !! %s" % a)
        if o_px < CLUSTER_THRESHOLD and g_px < CLUSTER_THRESHOLD:
            return
        o_dots = find_dots(shot, ORANGE_MIN, ORANGE_MAX)
        g_dots = find_dots(shot, GREEN_MIN, GREEN_MAX)
        all_dots = ([("UPGRADE ELIGIBLE (Gold/Orange)", d) for d in o_dots] +
                    [("FIBER ELIGIBLE (Green)", d) for d in g_dots])
        for dot_type, (px, py) in all_dots:
            lat, lng = pixel_to_latlng(px, py, row, col, sl, sg)
            res = geocode(lat, lng)
            if res is None:
                self.counters["failed"] += 1
                continue
            full, street, gcity, state, zipc, ptype, biz = res
            ptype = smart_classify(full, street, ptype, zipc)
            if ptype == "COMMERCIAL" and zipc:
                KNOWN_COMMERCIAL_ZIPS.add(zipc)
            is_green = "Green" in dot_type
            dup = "%s|%s" % (full, dot_type)
            if dup in self.existing:
                self.counters["skip"] += 1
                continue
            self.existing.add(dup)
            self.counters["new"] += 1
            phone = ""
            tag = "COMM" if ptype == "COMMERCIAL" else "RES"
            print("  %s [I%d]: %s %s" % (
                tag, self.instance, full[:50],
                ("[%s]" % biz) if biz else "",
            ))
            inst = self.inst_tag
            now = now_str()
            sheet_write(self.tabs, "Hunter Leads", [
                full, biz, dot_type, ptype, gcity, state, zipc,
                zone_name, inst, str(self.scan_num), "New", REP_NAME, now,
                phone, str(lat), str(lng),
            ], full)
            if ptype == "COMMERCIAL":
                if is_green:
                    self.counters["g_comm"] += 1
                else:
                    self.counters["o_comm"] += 1
                sheet_write(self.tabs, "Hunter Commercial", [
                    full, biz, dot_type, gcity, state, zipc,
                    zone_name, inst, str(self.scan_num), "New", REP_NAME, now,
                    phone, "",
                ], full)
                if is_green:
                    sheet_write(self.tabs, "Hunter Green Commercial", [
                        full, biz, gcity, state, zipc,
                        zone_name, inst, str(self.scan_num), now, phone,
                        str(lat), str(lng),
                    ], full)
            else:
                if is_green:
                    self.counters["g_res"] += 1
                else:
                    self.counters["o_res"] += 1
                sheet_write(self.tabs, "Hunter Residential", [
                    full, dot_type, gcity, state, zipc,
                    zone_name, inst, str(self.scan_num), "New", REP_NAME, now,
                ], full)
                if is_green:
                    sheet_write(self.tabs, "Hunter Green Residential", [
                        full, gcity, state, zipc,
                        zone_name, inst, str(self.scan_num), now,
                        str(lat), str(lng),
                    ], full)

    def stop(self):
        self.running = False
        self.t.join(timeout=120)
        flush_all(self.tabs)
        save_history(self.history)
        save_geo_cache()

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

def screenshot(scan_num, zone_name, row, col, instance):
    ts = datetime.now().strftime("%H%M%S")
    fn = os.path.join(SCREENSHOTS_DIR,
        "i%d_scan%02d_%s_r%02d_c%02d_%s.png" % (
            instance, scan_num, zone_name, row, col, ts))
    pyautogui.screenshot(fn)
    return fn

def scan_cell(zone, city, row, col, btn_x, btn_y, processor, scan_num, instance):
    pyautogui.click(btn_x, btn_y)
    found, o, g = wait_for_dots()
    shot = screenshot(scan_num, zone["name"], row, col, instance)
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

def main():
    check_update()
    print("\n" + "#" * 60)
    print("  FIBER HUNTER v%s" % VERSION)
    print("  Same engine as fiber_scan — runs in any city")
    print("#" * 60)
    if PGEOCODE_OK:
        print("  ZIP lookup: pgeocode (offline, every US ZIP) ✓")
    else:
        print("  ZIP lookup: API only (install pgeocode for offline:")
        print("              pip install pgeocode)")

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
    print("\n⚠ Make sure youachieve.att.com is OPEN and showing your area.")
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
        processor.stop()
    c = processor.counters
    print("\n" + "=" * 60)
    print("DONE")
    print("New: %d | Skipped dups: %d | Hot zones: %d | Greenfield: %d" % (
        c["new"], c["skip"], c["hot"], c["greenfield"]))
    print("Geocode failures (skipped): %d" % c["failed"])
    print("GOLD: Res=%d Comm=%d  |  GREEN: Res=%d Comm=%d" % (
        c["o_res"], c["o_comm"], c["g_res"], c["g_comm"]))
    print("=" * 60)

if __name__ == "__main__":
    main()
