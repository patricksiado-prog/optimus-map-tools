"""
FIBER HUNTER v4.0 - SPIRAL HUNTER
====================================
Mirrors fiber_scan's tested motion + detection. Adds:
  - Type a ZIP at start (sets seed location)
  - Pure square spiral, expands forever until Ctrl+C
  - Writes to its OWN "Hunter Alerts" + "Hunter Leads" tabs
  - Doesn't touch fiber_scan's data

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
VERSION = "4.0"

# ── AUTO-UPDATER ──────────────────────────────────────────────────
AUTO_UPDATE = True
GITHUB_REPO = "patricksiado-prog/optimus-map-tools"
GITHUB_FILE = "fiber_hunter.py"
GITHUB_BRANCH = "main"

def check_update():
    if not AUTO_UPDATE: return
    try:
        url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{GITHUB_FILE}"
        print("Checking for updates...")
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            print(f"  Update check failed (HTTP {r.status_code})")
            return
        remote = r.text
        m = re.search(r'VERSION\s*=\s*["\']([\d.]+)["\']', remote)
        if not m: return
        rv = m.group(1)
        if rv == VERSION:
            print(f"  Up to date (v{VERSION})")
            return
        def vt(v): return tuple(int(x) for x in v.split("."))
        if vt(rv) <= vt(VERSION):
            print(f"  Local v{VERSION} newer than remote v{rv}")
            return
        print(f"  Updating to v{rv}...")
        with open(__file__, "w", encoding="utf-8") as f:
            f.write(remote)
        print("  Restarting...")
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print(f"  Update err: {str(e)[:100]}")


# ── CONFIG ────────────────────────────────────────────────────────
CREDS_FILE = "google_creds.json"
SHEET_NAME = "ATT FIBER LEADS"

# Hunter has its OWN files — separate from fiber_scan
PROGRESS_FILE = "hunter_progress.json"
HISTORY_FILE  = "hunter_zone_history.json"
BUTTON_FILE   = "hunter_button_pos.json"
GEO_CACHE     = "hunter_geocode_cache.json"
SCREENSHOTS_DIR = "hunter_screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Hunter has its OWN sheet tabs
HUNTER_LEADS_TAB    = "Hunter Leads"
HUNTER_ALERTS_TAB   = "Hunter Alerts"
HUNTER_GREEN_TAB    = "Hunter Green"
HUNTER_GOLD_TAB     = "Hunter Gold"

# ── TIMING / MOTION (copied from fiber_scan, tested values) ──────
WAIT_AFTER_PAN     = 1.5
MAX_WAIT_DOTS      = 6.0
POLL_INTERVAL      = 0.12
PAN_PIXELS         = 150
MIN_DOT_PIXELS     = 3
CLUSTER_THRESHOLD  = 15
START_DELAY        = 10
BATCH_SIZE         = 12
GEOCODE_TIMEOUT    = 7
GEO_RATE           = 1.2
WAIT_AFTER_SEARCH  = 4.0   # for jump-to-ZIP

# Greenfield alert thresholds
GREENFIELD_GREEN_MIN = 80
GREENFIELD_GOLD_MAX  = 20
GREENFIELD_BLUE_MAX  = 30

# Map screenshot bounds (same as fiber_scan)
MAP_LEFT   = 50
MAP_TOP    = 100
MAP_RIGHT  = 1350
MAP_BOTTOM = 720
MAP_CX = (MAP_LEFT + MAP_RIGHT) // 2
MAP_CY = (MAP_TOP + MAP_BOTTOM) // 2

# Color ranges (matched to fiber_scan v10.0 - freeway-safe)
# ORANGE tightened so freeway pixels don't get counted as gold dots.
# If real gold dots stop detecting on YOUR monitor, loosen by 5:
#   First try:  (215,155,0) -> (255,200,65)
#   If needed:  (210,150,0) -> (255,200,70)
ORANGE_MIN = (220, 160, 0)
ORANGE_MAX = (255, 200, 60)
GREEN_MIN  = (30, 130, 30)
GREEN_MAX  = (100, 210, 80)
BLUE_MIN   = (50, 80, 180)
BLUE_MAX   = (120, 160, 255)

LAT_PER_PIXEL = -0.000015
LNG_PER_PIXEL =  0.000020
REP_NAME = "Patri"

KNOWN_COMMERCIAL_ZIPS = set()

COMMERCIAL_TYPES = [
    "commercial","retail","office","industrial","warehouse",
    "supermarket","mall","hotel","restaurant","fast_food",
    "cafe","bar","hospital","clinic","school","university",
    "government","bank","pharmacy","shop","store","building",
    "business","company","plaza","tower","center","centre",
    "suite","pkwy","parkway","blvd","corporate","logistics",
    "distribution","manufacturing","medical","dental",
    "automotive","dealership","terminal","port","airport",
]

RESIDENTIAL_TYPES = [
    "house","apartments","residential","detached","terrace",
    "dormitory","condo","flat","dwelling","home","bungalow",
    "villa","subdivision","estates",
]

COMMERCIAL_STREET_WORDS = [
    "industrial","commerce","corporate","business","trade",
    "enterprise","market","distribution","logistics","pkwy",
    "parkway","plaza","center","blvd","highway","freeway",
    "expressway","loop","port","terminal","airport",
]


# ── HELPERS ───────────────────────────────────────────────────────
def now_str():
    return datetime.now().strftime("%m/%d/%Y %I:%M %p")


# ── SQUARE SPIRAL GENERATOR ───────────────────────────────────────
def spiral_pan_directions():
    """Yields ('right'|'left'|'down'|'up', step_count) instructions for
    an expanding square spiral. Generates infinite sequence —
    walk one cell at a time forever."""
    directions = ["right", "down", "left", "up"]
    leg = 1
    di = 0
    while True:
        for _ in range(2):
            d = directions[di % 4]
            for _ in range(leg):
                yield d
            di += 1
        leg += 1


# ── CALIBRATE SEARCH BUTTON ──────────────────────────────────────
def calibrate_search_button():
    """Calibrate the 'Search this area' button position."""
    if os.path.exists(BUTTON_FILE):
        with open(BUTTON_FILE) as f:
            pos = json.load(f)
        print(f"\n  Saved 'Search this area' button: ({pos['x']}, {pos['y']})")
        ans = input("  Recalibrate? (y/n, default n): ").strip().lower()
        if ans != "y":
            return pos["x"], pos["y"]
    print("\nHover mouse over the AT&T 'Search this area' button.")
    input("Then press Enter: ")
    x, y = pyautogui.position()
    print(f"  Saved ({x}, {y})")
    with open(BUTTON_FILE, "w") as f:
        json.dump({"x": x, "y": y}, f)
    return x, y


# ── MAP DRIVING ───────────────────────────────────────────────────
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

def pixel_to_latlng_rel(px, py, total_dx, total_dy, seed_lat, seed_lng):
    """Convert pixel position in current screenshot to lat/lng,
    given the total cumulative drag from the seed point."""
    cx = (MAP_RIGHT - MAP_LEFT) // 2
    cy = (MAP_BOTTOM - MAP_TOP) // 2
    # The map has been panned (-total_dx, -total_dy) pixels relative to seed
    # (drag direction is opposite of map travel direction)
    map_offset_x = -total_dx
    map_offset_y = -total_dy
    px_offset = (px - cx) - map_offset_x
    py_offset = (py - cy) - map_offset_y
    lat = seed_lat + py_offset * LAT_PER_PIXEL
    lng = seed_lng + px_offset * LNG_PER_PIXEL
    return round(lat, 6), round(lng, 6)


# ── PAN + DRAG (matched to fiber_scan) ────────────────────────────
def pan(direction):
    """Pan the map by PAN_PIXELS in given direction.
    Drag is INVERSE of map travel: drag right = map pans left = view goes right."""
    pyautogui.moveTo(MAP_CX, MAP_CY)
    if direction == "right":
        pyautogui.drag(-PAN_PIXELS, 0, duration=0.2, button="left", _pause=False)
    elif direction == "left":
        pyautogui.drag(PAN_PIXELS, 0, duration=0.2, button="left", _pause=False)
    elif direction == "down":
        pyautogui.drag(0, -PAN_PIXELS, duration=0.2, button="left", _pause=False)
    elif direction == "up":
        pyautogui.drag(0, PAN_PIXELS, duration=0.2, button="left", _pause=False)
    time.sleep(WAIT_AFTER_PAN)


# ── GEOCODING (copied from fiber_scan) ────────────────────────────
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
    except: pass

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
            headers={"User-Agent": "FiberHunter/4.0"},
            timeout=GEOCODE_TIMEOUT,
        )
        d = r.json()
        if "address" in d and d["address"]:
            return d
    except: pass
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
                    "state": p.get("state", "TX"),
                    "postcode": p.get("postcode", ""),
                    "amenity": p.get("name", ""),
                },
                "type": p.get("type", ""), "class": "", "addresstype": "",
            }
    except: pass
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
    city = a.get("city") or a.get("town") or a.get("village") or ""
    state = a.get("state") or "TX"
    if state.lower() == "texas":
        state = "TX"
    zipc = a.get("postcode") or ""
    biz = ""
    for k in ["amenity","shop","office","building","industrial",
              "commercial","tourism","healthcare","leisure"]:
        biz = a.get(k) or ""
        if biz: break
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


# ── ZIP LOOKUP (geocode the seed) ─────────────────────────────────
def lookup_zip(z):
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"postalcode": z, "country": "US", "format": "json", "limit": 1},
            headers={"User-Agent": "FiberHunter/4.0"}, timeout=6,
        )
        d = r.json()
        if d:
            return float(d[0]["lat"]), float(d[0]["lon"]), d[0].get("display_name", z)
    except: pass
    return None, None, None


# ── SHEETS ────────────────────────────────────────────────────────
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
        configs = {
            HUNTER_LEADS_TAB: ["Address","Business Name","Dot Type","Property Type",
                               "City","State","Zip","Step","Date","Phone","Lat","Lng",
                               "Seed ZIP"],
            HUNTER_ALERTS_TAB: ["Date","Step","Alert Type","Details","Seed ZIP","Action"],
            HUNTER_GREEN_TAB: ["Address","Business Name","Property","City","State","Zip",
                               "Step","Date","Phone","Lat","Lng","Seed ZIP"],
            HUNTER_GOLD_TAB:  ["Address","Business Name","Property","City","State","Zip",
                               "Step","Date","Phone","Lat","Lng","Seed ZIP"],
        }
        for tname, headers in configs.items():
            if tname not in existing:
                ws = ss.add_worksheet(title=tname, rows=100000, cols=20)
                ws.append_row(headers)
            else:
                ws = ss.worksheet(tname)
            tabs[tname] = ws
        print("Connected to Google Sheets.")
        return tabs
    except Exception as e:
        print(f"Sheets error: {e}")
        return None

def get_existing(tabs):
    existing = set()
    if not tabs:
        return existing
    try:
        vals = tabs[HUNTER_LEADS_TAB].get_all_values()
        for row in vals[1:]:
            if row and row[0]:
                key = "%s|%s" % (row[0].strip(),
                                 row[2].strip() if len(row) > 2 else "")
                existing.add(key)
    except: pass
    print(f"Loaded {len(existing)} existing hunter leads")
    return existing


_buffers = {}
_buf_lock = threading.Lock()

def sheet_write(tabs, tab, row, addr=""):
    if not tabs:
        return
    with _buf_lock:
        _buffers.setdefault(tab, []).append(row)
        n = len(_buffers[tab])
    print(f"  SHEET: {tab}: {addr or (row[0] if row else '')}")
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
            print(f"  write err {tab}: {e}")
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
    except: pass


# ── HOT ZONE ALERTS ───────────────────────────────────────────────
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE) as f:
                return json.load(f)
        except: pass
    return {}

def save_history(h):
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(h, f, indent=2)
    except: pass

def check_hot_zone(step_n, total_dx, total_dy, o, g, b, history,
                   tabs, seed_zip):
    """Greenfield + new fiber + gold surge alerts."""
    key = f"step_{step_n}_{total_dx}_{total_dy}"
    now = now_str()
    alerts = []
    has = (o >= CLUSTER_THRESHOLD) or (g >= CLUSTER_THRESHOLD)

    # GREENFIELD: lots of green, almost no gold/blue = brand new
    if (g >= GREENFIELD_GREEN_MIN and o <= GREENFIELD_GOLD_MAX
            and b <= GREENFIELD_BLUE_MAX):
        prev_gf = history.get(key, {}).get("greenfield", False)
        if not prev_gf:
            msg = (f"GREENFIELD step {step_n} G:{g} O:{o} B:{b}")
            alerts.append(msg)
            log_sheet(tabs, HUNTER_ALERTS_TAB, [
                now, str(step_n), "GREENFIELD",
                f"G:{g} O:{o} B:{b}", seed_zip, "PRIORITY 1 - KNOCK NOW",
            ])
        history.setdefault(key, {})["greenfield"] = True

    # NEW FIBER: was empty, now has dots
    if key in history:
        prev = history[key]
        was_empty = prev.get("empty", True)
        if was_empty and has and b < CLUSTER_THRESHOLD:
            alerts.append(f"NEW FIBER step {step_n} G:{g} O:{o}")
            log_sheet(tabs, HUNTER_ALERTS_TAB, [
                now, str(step_n), "NEW FIBER",
                f"Was empty, now {g}G {o}O", seed_zip, "PRIORITY 1",
            ])
        elif prev.get("orange", 0) >= CLUSTER_THRESHOLD and o < CLUSTER_THRESHOLD:
            alerts.append(f"GOLD GONE step {step_n}")
            log_sheet(tabs, HUNTER_ALERTS_TAB, [
                now, str(step_n), "CONVERSIONS",
                f"Gold dropped from {prev.get('orange', 0)} to {o}",
                seed_zip, "Customers signed up",
            ])
        elif o > prev.get("orange", 0) + 300:
            alerts.append(f"GOLD SURGE step {step_n}")
            log_sheet(tabs, HUNTER_ALERTS_TAB, [
                now, str(step_n), "GOLD SURGE",
                f"Was {prev.get('orange', 0)} now {o}", seed_zip, "PRIORITY 2",
            ])

    history.setdefault(key, {}).update({
        "orange": o, "green": g, "blue": b,
        "empty": not has, "ts": now,
    })
    return alerts


# ── BACKGROUND PROCESSOR ──────────────────────────────────────────
class Processor:
    def __init__(self, tabs, existing, history, seed_zip, seed_lat, seed_lng):
        self.tabs = tabs
        self.existing = existing
        self.history = history
        self.seed_zip = seed_zip
        self.seed_lat = seed_lat
        self.seed_lng = seed_lng
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

    def submit(self, shot, step_n, total_dx, total_dy):
        self.q.put((shot, step_n, total_dx, total_dy))

    def _run(self):
        while self.running or not self.q.empty():
            try:
                item = self.q.get(timeout=1.0)
            except queue.Empty:
                continue
            try:
                self._process(*item)
            except Exception as e:
                print(f"  bg err: {e}")
            self.q.task_done()

    def _process(self, shot, step_n, total_dx, total_dy):
        if is_dark(shot):
            return
        try:
            img = Image.open(shot).convert("RGB")
        except:
            return
        o_px = count_color(img, ORANGE_MIN, ORANGE_MAX)
        g_px = count_color(img, GREEN_MIN, GREEN_MAX)
        b_px = count_color(img, BLUE_MIN, BLUE_MAX)

        alerts = check_hot_zone(step_n, total_dx, total_dy,
                                o_px, g_px, b_px,
                                self.history, self.tabs, self.seed_zip)
        self.counters["hot"] += len(alerts)
        for a in alerts:
            if "GREENFIELD" in a:
                self.counters["greenfield"] += 1
            print(f"  !! {a}")

        if o_px < CLUSTER_THRESHOLD and g_px < CLUSTER_THRESHOLD:
            return

        o_dots = find_dots(shot, ORANGE_MIN, ORANGE_MAX)
        g_dots = find_dots(shot, GREEN_MIN, GREEN_MAX)
        all_dots = (
            [("UPGRADE ELIGIBLE (Gold/Orange)", d) for d in o_dots] +
            [("FIBER ELIGIBLE (Green)", d) for d in g_dots]
        )

        for dot_type, (px, py) in all_dots:
            lat, lng = pixel_to_latlng_rel(px, py, total_dx, total_dy,
                                            self.seed_lat, self.seed_lng)
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
            print(f"  {tag} step{step_n}: {full[:50]}{(' ['+biz+']') if biz else ''}")
            now = now_str()

            sheet_write(self.tabs, HUNTER_LEADS_TAB, [
                full, biz, dot_type, ptype, gcity, state, zipc,
                str(step_n), now, phone, str(lat), str(lng), self.seed_zip,
            ], full)

            if is_green:
                if ptype == "COMMERCIAL":
                    self.counters["g_comm"] += 1
                else:
                    self.counters["g_res"] += 1
                sheet_write(self.tabs, HUNTER_GREEN_TAB, [
                    full, biz, ptype, gcity, state, zipc,
                    str(step_n), now, phone, str(lat), str(lng), self.seed_zip,
                ], full)
            else:
                if ptype == "COMMERCIAL":
                    self.counters["o_comm"] += 1
                else:
                    self.counters["o_res"] += 1
                sheet_write(self.tabs, HUNTER_GOLD_TAB, [
                    full, biz, ptype, gcity, state, zipc,
                    str(step_n), now, phone, str(lat), str(lng), self.seed_zip,
                ], full)

    def stop(self):
        self.running = False
        self.t.join(timeout=120)
        flush_all(self.tabs)
        save_history(self.history)
        save_geo_cache()


# ── JUMP TO SEED ZIP ──────────────────────────────────────────────
def jump_to_zip(zipcode):
    """Type ZIP into search bar (we don't know its location, so click search
    button area then send the ZIP). Actually fiber_scan only uses the
    'Search this area' button — we need a different way to seed.

    Approach: Manual. We tell the user to navigate the map to the seed ZIP
    BEFORE the script starts. Script just starts spiraling from wherever
    the map currently is.

    This is simpler and more reliable than trying to auto-search.
    """
    pass  # left empty - user navigates manually


# ── MAIN ──────────────────────────────────────────────────────────
def main():
    check_update()

    print("\n" + "#" * 60)
    print(f"  FIBER HUNTER v{VERSION} — SPIRAL HUNTER")
    print(f"  Mirrors fiber_scan v10.0 motion + detection")
    print(f"  Spiral pattern, runs until Ctrl+C")
    print("#" * 60)

    # Get seed ZIP
    print("\nWhat ZIP do you want to spiral from?")
    print("(You should have YouAchieve already navigated to this ZIP)")
    seed_zip = input("Seed ZIP: ").strip()
    if not (seed_zip.isdigit() and len(seed_zip) == 5):
        print("Need a 5-digit ZIP. Exiting.")
        return

    # Geocode the seed ZIP for lat/lng reference
    print(f"\nLooking up {seed_zip}...")
    seed_lat, seed_lng, seed_name = lookup_zip(seed_zip)
    if not seed_lat:
        print(f"Couldn't geocode {seed_zip}. Exiting.")
        return
    print(f"  Found: {seed_name}")
    print(f"  Center: ({seed_lat}, {seed_lng})")

    # Calibrate
    btn_x, btn_y = calibrate_search_button()

    # Connect sheets
    tabs = connect_sheets()
    existing = get_existing(tabs)
    history = load_history()
    load_geo_cache()

    print("\n" + "=" * 60)
    print(f"READY  |  Seed ZIP: {seed_zip} ({seed_name})")
    print(f"Pan: {PAN_PIXELS}px per step  |  Spiral pattern")
    print(f"\n⚠ MAKE SURE youachieve.att.com IS ON {seed_zip}")
    print(f"⚠ Map should already show the area you want to spiral from")
    print(f"\nStarting in {START_DELAY} sec.")
    print("Ctrl+C to stop. Hot leads write to sheet automatically.")
    print("=" * 60)
    time.sleep(START_DELAY)

    processor = Processor(tabs, existing, history, seed_zip, seed_lat, seed_lng)

    # SCAN seed location FIRST (no pan)
    step_n = 0
    total_dx = 0
    total_dy = 0
    print(f"\n[Step {step_n}] Scanning seed location...")
    pyautogui.click(btn_x, btn_y)
    found, o, g = wait_for_dots()
    ts = datetime.now().strftime("%H%M%S")
    fn = os.path.join(SCREENSHOTS_DIR, f"step{step_n:04d}_{ts}.png")
    pyautogui.screenshot(fn)
    print(f"  O:{o} G:{g}")
    processor.submit(fn, step_n, total_dx, total_dy)

    # SPIRAL forever until Ctrl+C
    try:
        for direction in spiral_pan_directions():
            step_n += 1
            print(f"\n[Step {step_n}] Pan {direction}...")
            pan(direction)
            # Track cumulative drag (drag distance moves opposite of map)
            if direction == "right":
                total_dx -= PAN_PIXELS
            elif direction == "left":
                total_dx += PAN_PIXELS
            elif direction == "down":
                total_dy -= PAN_PIXELS
            elif direction == "up":
                total_dy += PAN_PIXELS

            # Click "Search this area" → wait for dots → screenshot
            pyautogui.click(btn_x, btn_y)
            found, o, g = wait_for_dots()
            ts = datetime.now().strftime("%H%M%S")
            fn = os.path.join(SCREENSHOTS_DIR, f"step{step_n:04d}_{ts}.png")
            pyautogui.screenshot(fn)
            print(f"  O:{o} G:{g}")
            processor.submit(fn, step_n, total_dx, total_dy)
    except KeyboardInterrupt:
        print("\n\n⛔ Ctrl+C — stopping.")

    # Cleanup
    print("\nFinishing background processing...")
    processor.q.join()
    processor.stop()

    c = processor.counters
    print("\n" + "=" * 60)
    print("DONE")
    print(f"Steps spiraled: {step_n}")
    print(f"New leads: {c['new']} | Skipped dups: {c['skip']}")
    print(f"Hot zones: {c['hot']} | Greenfield alerts: {c['greenfield']}")
    print(f"Geocode failures: {c['failed']}")
    print(f"GOLD: Res={c['o_res']} Comm={c['o_comm']}")
    print(f"GREEN: Res={c['g_res']} Comm={c['g_comm']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
