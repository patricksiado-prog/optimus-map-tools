"""
FIBER HUNTER (standalone) v2.0
================================
News-driven scanner. Independent of fiber_scan.py.
Own state files, own sheet tabs. Doesn't touch fiber_scan.

NIGHTLY FLOW:
  1. NEWS PASS — Reddit + regional newspapers + state news + BEAD
                 across 28 AT&T fiber states
  2. PIPELINE  — auto-promotes by article age:
                   6mo PERMIT  → CONSTRUCTION
                   1yr PERMIT  → LIT (call NOW)
                   14mo+       → SATURATED
  3. HUNT      — for each hot ZIP from pipeline:
                   - Click search bar, type ZIP, press Enter
                   - Wait 4 sec (let map travel)
                   - Click safe spot on map (calibrated by you)
                   - Press + three times (zoom in to neighborhood)
                   - Wait for dots to redraw
                   - Screenshot, count gold/green/gray dots
                   - If hot → 🔥 alert + write to sheet
                   - If dead → silent skip, next ZIP
  4. ALERTS    — 🔥 banner in console + row in "🔥 Hunter Alerts" tab

CALIBRATION (2 points only):
  a) Search bar position
  b) Safe empty spot on map (anywhere — your pick)

USAGE:
  python fiber_hunter.py --calibrate         # one-time setup
  python fiber_hunter.py --test              # type ZIPs manually
  python fiber_hunter.py --news-only         # news pass only
  python fiber_hunter.py --hunt              # full nightly
  python fiber_hunter.py --hunt --top 30     # hunt top 30 ZIPs
  python fiber_hunter.py --since 180         # 6mo lookback
"""

import os, sys, time, json, csv, argparse, re
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from urllib.parse import quote_plus

import requests

try:
    import pyautogui
    import numpy as np
    from PIL import Image, ImageGrab
    from scipy import ndimage
    SCAN_AVAILABLE = True
except ImportError:
    SCAN_AVAILABLE = False

try:
    import gspread
    from google.oauth2.service_account import Credentials
    SHEETS_AVAILABLE = True
except ImportError:
    SHEETS_AVAILABLE = False

VERSION = "2.0"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# ── AUTO-UPDATER ──────────────────────────────────────────────────
AUTO_UPDATE = True
GITHUB_REPO = "patricksiado-prog/optimus-map-tools"
GITHUB_FILE = "fiber_hunter.py"
GITHUB_BRANCH = "main"

def check_update():
    if not AUTO_UPDATE:
        return
    try:
        url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{GITHUB_FILE}"
        print("Checking for updates...")
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            print(f"  Update check failed (HTTP {r.status_code})")
            return
        remote = r.text
        m = re.search(r'VERSION\s*=\s*["\']([\d.]+)["\']', remote)
        if not m:
            return
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
SHEET_ID   = "15ymTkIGPWs6quB035l414ns5hkG9cQ5xr_W4ukd0OAA"

# Hunter has its OWN tabs — separate from fiber_scan
HUNTER_ALERTS_TAB = "Hunter Alerts"
HUNTER_LEADS_TAB  = "Hunter Leads"
PIPELINE_TAB      = "Fiber Pipeline"
LIT_TAB           = "Just Lit"
PERMIT_TAB        = "Permit Watch"
BEAD_TAB          = "BEAD Awards"

# Hunter has its OWN state files
PIPELINE_FILE  = "hunter_pipeline.json"
PROGRESS_FILE  = "hunter_progress.json"
CALIB_FILE     = "hunter_calib.json"
SEEN_NEWS_FILE = "hunter_seen.json"
HOT_ZIPS_FILE  = "hunter_hot_zips.txt"

# ── ZOOM/SCAN TIMING ──────────────────────────────────────────────
AUTO_ZOOM_CLICKS = 3
WAIT_AFTER_TYPING = 1.0
WAIT_AFTER_ENTER = 4.0
WAIT_BETWEEN_ZOOMS = 0.5
WAIT_AFTER_ZOOM = 1.5
SCREENSHOT_DELAY = 0.5
REQ_DELAY = 1.5
START_DELAY = 8

# ── ALERT THRESHOLDS ──────────────────────────────────────────────
ALERT_MIN_GOLD = 3
ALERT_VIRGIN_GOLD = 3
ALERT_VIRGIN_GRAY = 2
SKIP_IF_TOTAL_LT = 5
SKIP_IF_GRAY_PCT = 0.70

# ── COLOR DETECTION ───────────────────────────────────────────────
GOLD_DOT_MIN = (220, 160, 0)
GOLD_DOT_MAX = (255, 200, 60)
GREEN_DOT_MIN = (30, 130, 30)
GREEN_DOT_MAX = (100, 210, 80)
GRAY_DOT_MIN = (140, 140, 140)
GRAY_DOT_MAX = (200, 200, 200)
MIN_DOT_PIXELS = 8
MAX_DOT_PIXELS = 250
MAX_ASPECT_RATIO = 2.5
MIN_FILL_RATIO = 0.45

# ── MAP COORDS (loaded from CALIB_FILE) ───────────────────────────
SEARCH_X, SEARCH_Y = 200, 250
MAP_SAFE_X, MAP_SAFE_Y = 700, 600
MAP_LEFT, MAP_TOP = 50, 200
MAP_RIGHT, MAP_BOTTOM = 1350, 720
LAT_PER_PIXEL = -0.000015
LNG_PER_PIXEL =  0.000020

# AT&T's 28 fiber states
ATT_STATES = [
    "AL","AR","CA","CO","FL","GA","IA","ID","IL","IN","KS","KY",
    "LA","MI","MO","MS","NC","NE","NV","OH","OK","OR","SC","TN",
    "TX","UT","WA","WI",
]

STATE_NAMES = {
    "AL":"Alabama","AR":"Arkansas","CA":"California","CO":"Colorado",
    "FL":"Florida","GA":"Georgia","IA":"Iowa","ID":"Idaho",
    "IL":"Illinois","IN":"Indiana","KS":"Kansas","KY":"Kentucky",
    "LA":"Louisiana","MI":"Michigan","MO":"Missouri","MS":"Mississippi",
    "NC":"North Carolina","NE":"Nebraska","NV":"Nevada","OH":"Ohio",
    "OK":"Oklahoma","OR":"Oregon","SC":"South Carolina","TN":"Tennessee",
    "TX":"Texas","UT":"Utah","WA":"Washington","WI":"Wisconsin",
}

# ── KEYWORDS ──────────────────────────────────────────────────────
PERMIT_KW = [
    "att fiber permit","at&t fiber permit","att fiber installation",
    "at&t fiber installation","att fiber project","att fiber construction",
    "att fiber buildout","fiber optic permit","fiber installation notice",
    "att utility work","att fiber work","att right-of-way",
    "att fiber notification","att fiber subdivision","att fiber neighborhood",
    "fiber optic cable installation",
]
CONSTRUCTION_KW = [
    "att truck","att crew","att construction crew","att digging",
    "att trenching","fiber trenching","att door hanger","att door-hanger",
    "att flags in yard","fiber install in progress","att splicing",
]
LIT_KW = [
    "att fiber just","att fiber finally","att fiber arrived",
    "fiber went live","fiber turned on","att fiber ready",
    "att fiber available now","fiber lit up","fiber activated",
    "got att fiber","have att fiber",
]
ATT_CONTRACTORS = [
    "star construction","bethel industries","henkels & mccoy",
    "henkels and mccoy","mastec north america","mp nexlevel",
    "ervin cable","dycom industries","ansco & associates",
    "irby construction",
]
BEAD_KW = [
    "bead award","bead funding","bead program",
    "broadband equity access deployment","att bead","at&t bead",
    "broadband expansion award",
]

REDDIT_SUBS = [
    "ATT","Fios","HomeNetworking","ISP","internet",
    "houston","dallas","austin","sanantonio","atlanta","miami",
    "orlando","tampa","jacksonville","nashville","memphis",
    "charlotte","raleigh","chicago","indianapolis","stlouis",
    "kansascity","detroit","cleveland","columbus","milwaukee",
    "louisville","neworleans","birminghamal","huntsville",
    "okc","tulsa","littlerock","Sacramento","sandiego",
    "lasvegas","denver","phoenix","seattle","portland",
]

REGIONAL_PAPERS = [
    ("Dallas Morning News",       "dallasnews.com"),
    ("San Antonio Express-News",  "expressnews.com"),
    ("Austin American-Statesman", "statesman.com"),
    ("Atlanta Journal-Constitution", "ajc.com"),
    ("Tampa Bay Times",           "tampabay.com"),
    ("Miami Herald",              "miamiherald.com"),
    ("Orlando Sentinel",          "orlandosentinel.com"),
    ("Charlotte Observer",        "charlotteobserver.com"),
    ("Tennessean",                "tennessean.com"),
    ("Commercial Appeal Memphis", "commercialappeal.com"),
    ("AL.com",                    "al.com"),
    ("Times-Picayune",            "nola.com"),
    ("Chicago Tribune",           "chicagotribune.com"),
    ("Detroit Free Press",        "freep.com"),
    ("Indianapolis Star",         "indystar.com"),
    ("Cincinnati Enquirer",       "cincinnati.com"),
    ("Cleveland.com",             "cleveland.com"),
    ("Columbus Dispatch",         "dispatch.com"),
    ("Milwaukee Journal Sentinel","jsonline.com"),
    ("Kansas City Star",          "kansascity.com"),
    ("St. Louis Post-Dispatch",   "stltoday.com"),
    ("Louisville Courier-Journal","courier-journal.com"),
    ("Oklahoman",                 "oklahoman.com"),
    ("Tulsa World",               "tulsaworld.com"),
    ("Arkansas Democrat-Gazette", "arkansasonline.com"),
    ("Arizona Republic",          "azcentral.com"),
    ("Las Vegas Review-Journal",  "reviewjournal.com"),
    ("Denver Post",               "denverpost.com"),
    ("Seattle Times",             "seattletimes.com"),
    ("Oregonian",                 "oregonlive.com"),
    ("Salt Lake Tribune",         "sltrib.com"),
    ("LA Times",                  "latimes.com"),
    ("San Francisco Chronicle",   "sfchronicle.com"),
    ("Mercury News",              "mercurynews.com"),
    ("Sacramento Bee",            "sacbee.com"),
]


# ── HELPERS ───────────────────────────────────────────────────────
def now_str():
    return datetime.now().strftime("%m/%d/%Y %I:%M %p")

def today_iso():
    return datetime.now().strftime("%Y-%m-%d")

def safe_get(url, headers=None, timeout=15):
    try:
        h = {"User-Agent": USER_AGENT}
        if headers:
            h.update(headers)
        r = requests.get(url, headers=h, timeout=timeout)
        if r.status_code == 200:
            return r
    except:
        pass
    return None

ZIP_RE = re.compile(r"\b(\d{5})(?:-\d{4})?\b")

def extract_zips(text):
    if not text:
        return []
    return list({m.group(1) for m in ZIP_RE.finditer(text)})

def classify_text(text):
    if not text:
        return None, 0
    low = text.lower()
    permit = sum(1 for k in PERMIT_KW if k in low)
    contractor = sum(1 for c in ATT_CONTRACTORS if c in low)
    construction = sum(1 for k in CONSTRUCTION_KW if k in low)
    lit = sum(1 for k in LIT_KW if k in low)
    bead = sum(1 for k in BEAD_KW if k in low)
    has_att = "at&t" in low or "att fiber" in low or "att internet" in low
    if not has_att and contractor == 0 and bead == 0:
        return None, 0
    if bead >= 1:
        return "BEAD", bead*3 + permit + contractor
    if permit >= 1 or contractor >= 1:
        return "PERMIT", permit*2 + contractor*3
    if construction >= 1:
        return "CONSTRUCTION", construction*2
    if lit >= 1:
        return "LIT", lit
    location = ["street","avenue","road","drive","boulevard","subdivision",
                "neighborhood","my area","my street","just got","finally",
                "expansion","launch","rollout","announcement"]
    if has_att and any(w in low for w in location):
        return "LIT", 1
    return None, 0

def parse_pub_date(s):
    if not s:
        return None
    formats = ["%a, %d %b %Y %H:%M:%S","%Y-%m-%dT%H:%M:%S","%Y-%m-%d"]
    s = str(s)[:25].rstrip("Z").rstrip()
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt)
        except:
            continue
    return None

def stage_from_age(initial_stage, date_published):
    pub_dt = parse_pub_date(date_published)
    if not pub_dt:
        return initial_stage
    days_old = (datetime.now() - pub_dt).days
    if initial_stage == "BEAD":
        return "BEAD"
    if initial_stage == "CONSTRUCTION":
        if days_old > 180: return "SATURATED"
        if days_old > 90:  return "LIT"
        return "CONSTRUCTION"
    if initial_stage == "PERMIT":
        if days_old > 365: return "SATURATED"
        if days_old > 180: return "LIT"
        if days_old > 60:  return "CONSTRUCTION"
        return "PERMIT"
    if initial_stage == "LIT":
        if days_old > 180: return "SATURATED"
        return "LIT"
    return initial_stage


# ── PERSISTENCE ───────────────────────────────────────────────────
def load_pipeline():
    if os.path.exists(PIPELINE_FILE):
        try:
            with open(PIPELINE_FILE) as f:
                return json.load(f)
        except: pass
    return {"entries": {}, "last_run": None}

def save_pipeline(p):
    p["last_run"] = today_iso()
    with open(PIPELINE_FILE, "w") as f:
        json.dump(p, f, indent=2)

def load_seen():
    if os.path.exists(SEEN_NEWS_FILE):
        try:
            with open(SEEN_NEWS_FILE) as f:
                return set(json.load(f))
        except: pass
    return set()

def save_seen(seen):
    try:
        with open(SEEN_NEWS_FILE, "w") as f:
            json.dump(list(seen)[-5000:], f)
    except: pass

def make_key(item):
    return (item.get("url","")[:200] or item.get("title","")[:100]).lower()

def merge_pipeline(p, items):
    new = updated = 0
    stage_order = {"PERMIT":1,"BEAD":1,"CONSTRUCTION":2,"LIT":3,"SATURATED":4}
    for it in items:
        k = make_key(it)
        if not k: continue
        original_stage = it["stage"]
        aged_stage = stage_from_age(original_stage, it.get("date",""))
        it["stage"] = aged_stage
        if k in p["entries"]:
            e = p["entries"][k]
            e["last_seen"] = today_iso()
            e["score"] = max(e.get("score",0), it.get("score",0))
            if stage_order.get(it["stage"],0) > stage_order.get(e["stage"],0):
                e["stage"] = it["stage"]
                e["promoted_at"] = today_iso()
            updated += 1
        else:
            p["entries"][k] = {
                "key": k, "stage": it["stage"],
                "first_seen": today_iso(), "last_seen": today_iso(),
                "score": it.get("score",0),
                "title": it.get("title",""),
                "url": it.get("url",""),
                "snippet": it.get("snippet","")[:400],
                "date_published": it.get("date",""),
                "zips": it.get("zips", []),
                "original_stage": original_stage,
                "auto_promoted": (f"{original_stage}→{aged_stage}" if original_stage != aged_stage else ""),
            }
            new += 1
    return new, updated


# ── NEWS PASS ─────────────────────────────────────────────────────
def google_news(query, since_days=30):
    url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=en-US&gl=US&ceid=US:en"
    r = safe_get(url)
    if not r: return []
    items = []
    blocks = re.findall(r"<item>(.*?)</item>", r.text, re.DOTALL)
    cutoff = datetime.now() - timedelta(days=since_days)
    for b in blocks:
        title = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", b, re.DOTALL)
        link = re.search(r"<link>(.*?)</link>", b)
        desc = re.search(r"<description>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>", b, re.DOTALL)
        date = re.search(r"<pubDate>(.*?)</pubDate>", b)
        date_str = (date.group(1) if date else "").strip()
        try:
            dt = datetime.strptime(date_str[:25], "%a, %d %b %Y %H:%M:%S")
            if dt < cutoff: continue
        except: pass
        items.append({
            "title": (title.group(1) if title else "").strip(),
            "url": (link.group(1) if link else "").strip(),
            "snippet": re.sub(r"<[^>]+>", " ", (desc.group(1) if desc else "")).strip()[:600],
            "date": date_str[:25],
        })
    return items

def reddit_recent(sub, since_days=14, limit=50):
    url = f"https://www.reddit.com/r/{sub}/new.json?limit={limit}"
    r = safe_get(url, headers={"User-Agent": f"FiberHunter/{VERSION}"})
    if not r: return []
    try:
        posts = r.json().get("data", {}).get("children", [])
        cutoff = time.time() - since_days * 86400
        out = []
        for p in posts:
            d = p.get("data", {})
            if d.get("created_utc", 0) < cutoff: continue
            out.append({
                "title": d.get("title", ""),
                "snippet": d.get("selftext", "")[:500] or d.get("title", ""),
                "url": "https://reddit.com" + d.get("permalink", ""),
                "date": datetime.fromtimestamp(d.get("created_utc", 0)).strftime("%Y-%m-%d"),
            })
        return out
    except: return []

def run_news_pass(states, since_days=30):
    print("\n" + "=" * 60)
    print(f"NEWS PASS — {len(states)} states, last {since_days} days")
    print("=" * 60)
    seen = load_seen()
    all_items = []

    print("\n[1] State news queries...")
    for st in states:
        sn = STATE_NAMES.get(st, st)
        for q in [f'"AT&T fiber" "{sn}"',
                  f'"AT&T" fiber expansion "{sn}"',
                  f'BEAD "AT&T" "{sn}"']:
            print(f"  {st} '{q[:55]}'...", end=" ", flush=True)
            items = google_news(q, since_days)
            kept = 0
            for it in items:
                if it["url"] in seen: continue
                seen.add(it["url"])
                text = it["title"] + " " + it["snippet"]
                stage, score = classify_text(text)
                if stage:
                    it["stage"] = stage
                    it["score"] = score
                    it["zips"] = extract_zips(text)
                    all_items.append(it)
                    kept += 1
            print(kept)
            time.sleep(REQ_DELAY)

    print("\n[2] Regional newspapers...")
    for name, dom in REGIONAL_PAPERS:
        q = f'"AT&T fiber" site:{dom}'
        print(f"  {name[:30]:<30}...", end=" ", flush=True)
        items = google_news(q, since_days)
        kept = 0
        for it in items:
            if it["url"] in seen: continue
            seen.add(it["url"])
            text = it["title"] + " " + it["snippet"]
            stage, score = classify_text(text)
            if stage:
                it["stage"] = stage
                it["score"] = score + 1
                it["zips"] = extract_zips(text)
                all_items.append(it)
                kept += 1
        print(kept)
        time.sleep(REQ_DELAY)

    print("\n[3] Reddit subs...")
    for sub in REDDIT_SUBS:
        print(f"  r/{sub}...", end=" ", flush=True)
        posts = reddit_recent(sub, since_days=min(since_days, 14))
        kept = 0
        for p in posts:
            if p["url"] in seen: continue
            seen.add(p["url"])
            text = p["title"] + " " + p["snippet"]
            stage, score = classify_text(text)
            if stage:
                p["stage"] = stage
                p["score"] = score
                p["zips"] = extract_zips(text)
                all_items.append(p)
                kept += 1
        print(kept)
        time.sleep(REQ_DELAY)

    save_seen(seen)
    print(f"\nTotal new news signals: {len(all_items)}")
    return all_items


# ══════════════════════════════════════════════════════════════════
#  HUNT (scanning) — types ZIP, clicks map, zooms 3x, scans dots
# ══════════════════════════════════════════════════════════════════

def calibrate():
    print("\n" + "=" * 60)
    print("CALIBRATION — 2 points")
    print("=" * 60)
    print("\n1. Open youachieve.att.com, log in, see the fiber map\n")

    cfg = {}
    print("a) Hover mouse over the SEARCH BAR (where ZIP gets typed)")
    input("   Press Enter when ready: ")
    x, y = pyautogui.position()
    cfg["search_x"] = x
    cfg["search_y"] = y
    print(f"   Saved: ({x}, {y})\n")

    print("b) Hover mouse over a SAFE empty spot on the map")
    print("   (not search bar, not a button, not a popup, not a dot —")
    print("    just plain map area). This is where we click before zooming.")
    input("   Press Enter when ready: ")
    x, y = pyautogui.position()
    cfg["map_safe_x"] = x
    cfg["map_safe_y"] = y
    print(f"   Saved: ({x}, {y})\n")

    # Auto-derive screenshot bounds from safe-map point and screen size
    sw, sh = pyautogui.size()
    cfg["map_left"] = 0
    cfg["map_top"] = 200
    cfg["map_right"] = sw
    cfg["map_bottom"] = sh - 50
    print(f"   Map screenshot bounds: ({cfg['map_left']}, {cfg['map_top']}) "
          f"to ({cfg['map_right']}, {cfg['map_bottom']})")

    with open(CALIB_FILE, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"\nSaved to {CALIB_FILE}")
    return cfg

def load_calibration():
    global SEARCH_X, SEARCH_Y, MAP_SAFE_X, MAP_SAFE_Y
    global MAP_LEFT, MAP_TOP, MAP_RIGHT, MAP_BOTTOM
    if not os.path.exists(CALIB_FILE):
        return None
    with open(CALIB_FILE) as f:
        cfg = json.load(f)
    SEARCH_X = cfg["search_x"]
    SEARCH_Y = cfg["search_y"]
    MAP_SAFE_X = cfg["map_safe_x"]
    MAP_SAFE_Y = cfg["map_safe_y"]
    MAP_LEFT = cfg.get("map_left", 0)
    MAP_TOP = cfg.get("map_top", 200)
    MAP_RIGHT = cfg.get("map_right", 1366)
    MAP_BOTTOM = cfg.get("map_bottom", 720)
    return cfg

def search_and_zoom(zipcode):
    """Type ZIP, press Enter, click safe map spot, zoom 3x."""
    # 1. Click search bar
    pyautogui.click(SEARCH_X, SEARCH_Y)
    time.sleep(0.5)
    # 2. Clear any existing text
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(0.3)
    # 3. Type ZIP
    pyautogui.typewrite(zipcode, interval=0.05)
    # 4. Wait for autocomplete dropdown to appear
    time.sleep(WAIT_AFTER_TYPING)
    # 5. Press Enter (selects first suggestion or fires search)
    pyautogui.press("enter")
    # 6. Wait for map to travel
    time.sleep(WAIT_AFTER_ENTER)
    # 7. Click safe spot on map (defocuses search bar, gives map focus)
    pyautogui.click(MAP_SAFE_X, MAP_SAFE_Y)
    time.sleep(0.4)
    # 8. Zoom in N times
    for _ in range(AUTO_ZOOM_CLICKS):
        pyautogui.press("+")
        time.sleep(WAIT_BETWEEN_ZOOMS)
    # 9. Wait for dots to redraw at new zoom
    time.sleep(WAIT_AFTER_ZOOM)

def grab_map():
    return ImageGrab.grab(bbox=(MAP_LEFT, MAP_TOP, MAP_RIGHT, MAP_BOTTOM))

def find_dots(img, cmin, cmax):
    arr = np.array(img)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    mask = ((r >= cmin[0]) & (r <= cmax[0]) &
            (g >= cmin[1]) & (g <= cmax[1]) &
            (b >= cmin[2]) & (b <= cmax[2]))
    labeled, num = ndimage.label(mask)
    dots = []
    for i in range(1, num + 1):
        ys, xs = np.where(labeled == i)
        n = len(ys)
        if n < MIN_DOT_PIXELS or n > MAX_DOT_PIXELS: continue
        h = ys.max() - ys.min() + 1
        w = xs.max() - xs.min() + 1
        if h == 0 or w == 0: continue
        if max(h,w)/max(min(h,w),1) > MAX_ASPECT_RATIO: continue
        if n / float(h*w) < MIN_FILL_RATIO: continue
        dots.append((int(xs.mean()), int(ys.mean())))
    return dots

def zip_to_latlng(zipcode):
    try:
        r = safe_get(
            f"https://nominatim.openstreetmap.org/search?postalcode={zipcode}"
            "&country=US&format=json&limit=1",
            headers={"User-Agent": f"FiberHunter/{VERSION}"})
        if r:
            d = r.json()
            if d:
                return float(d[0]["lat"]), float(d[0]["lon"])
    except: pass
    return None, None

def reverse_geocode(lat, lng):
    time.sleep(1.1)
    try:
        r = safe_get(
            f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lng}"
            "&format=json&addressdetails=1&zoom=18&extratags=1",
            headers={"User-Agent": f"FiberHunter/{VERSION}"})
        if not r: return "", "UNKNOWN"
        d = r.json()
        a = d.get("address", {})
        house = a.get("house_number", "")
        road = a.get("road", "")
        addr = f"{house} {road}" if house and road else (road or "")
        if not addr: return "", "UNKNOWN"
        cls = str(d.get("class","")).lower()
        typ = str(d.get("type","")).lower()
        atype = str(d.get("addresstype","")).lower()
        combined = f"{cls} {typ} {atype}"
        commercial = any(s in combined for s in [
            "commercial","industrial","retail","office","shop",
            "supermarket","mall","warehouse","restaurant","fast_food",
            "cafe","bar","hotel","motel","hospital","clinic",
            "school","university","college","government","bank","pharmacy",
        ])
        residential = any(s in combined for s in [
            "house","residential","detached","terrace","apartments",
            "dormitory","bungalow","semidetached_house",
        ])
        if commercial: prop = "COMM"
        elif residential: prop = "RES"
        elif house: prop = "RES"
        else: prop = "UNKNOWN"
        return addr, prop
    except:
        return "", "UNKNOWN"

def hunt_zip(zipcode, news_context=None):
    """Hunt one ZIP. Returns (alert, leads).
    alert: dict or None — populated only if we found something hot
    leads: list of address dicts"""
    print(f"\n  🔍 {zipcode}...", end=" ", flush=True)

    center_lat, center_lng = zip_to_latlng(zipcode)
    if not center_lat:
        print("can't geocode, skip")
        return None, []

    try:
        search_and_zoom(zipcode)
    except Exception as e:
        print(f"map err: {e}")
        return None, []

    time.sleep(SCREENSHOT_DELAY)
    img = grab_map()
    gold = find_dots(img, GOLD_DOT_MIN, GOLD_DOT_MAX)
    green = find_dots(img, GREEN_DOT_MIN, GREEN_DOT_MAX)
    gray = find_dots(img, GRAY_DOT_MIN, GRAY_DOT_MAX)

    total = len(gold) + len(green) + len(gray)
    print(f"Gold:{len(gold)} Green:{len(green)} Gray:{len(gray)}")

    # Skip empty/dead zones silently
    if total < SKIP_IF_TOTAL_LT:
        print(f"     → too few dots, skipping silently")
        return None, []

    gray_pct = len(gray) / total if total else 0
    if gray_pct > SKIP_IF_GRAY_PCT:
        print(f"     → {int(gray_pct*100)}% gray, saturated, skipping")
        return None, []

    # Decide alert type
    is_virgin = (len(gold) >= ALERT_VIRGIN_GOLD and len(gray) <= ALERT_VIRGIN_GRAY)
    is_hot = (len(gold) >= ALERT_MIN_GOLD)
    is_fresh_green = (len(green) >= 20 and gray_pct < 0.30)

    if is_virgin:
        priority = "🔥🔥🔥 VIRGIN BUILD"
    elif is_hot:
        priority = "🔥🔥 HOT — gold present"
    elif is_fresh_green:
        priority = "🔥 FRESH GREEN ZONE"
    else:
        # Has dots but not exciting enough to alert
        return None, []

    print(f"     {priority}")

    alert = {
        "zip": zipcode,
        "priority": priority,
        "gold": len(gold),
        "green": len(green),
        "gray": len(gray),
        "scanned_at": now_str(),
        "news_title": (news_context or {}).get("title","")[:200],
        "news_url": (news_context or {}).get("url",""),
        "news_stage": (news_context or {}).get("stage",""),
    }

    # Geocode addresses (sample only — top dots, rate limit friendly)
    leads = []
    for color, dots in [("GOLD", gold[:30]), ("GREEN", green[:30])]:
        for px, py in dots:
            cx = (MAP_RIGHT - MAP_LEFT) // 2
            cy = (MAP_BOTTOM - MAP_TOP) // 2
            lat = round(center_lat + (py - cy) * LAT_PER_PIXEL, 6)
            lng = round(center_lng + (px - cx) * LNG_PER_PIXEL, 6)
            addr, prop = reverse_geocode(lat, lng)
            if not addr: continue
            leads.append({
                "zip": zipcode,
                "address": addr,
                "property_type": prop,
                "dot_color": color,
                "lat": lat, "lng": lng,
                "priority": priority,
                "news_source": (news_context or {}).get("title","")[:120],
                "scanned_at": now_str(),
            })
    return alert, leads


# ── SHEETS ────────────────────────────────────────────────────────
def connect_sheet():
    if not SHEETS_AVAILABLE or not os.path.exists(CREDS_FILE):
        return None
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets",
                  "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(CREDS_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        return client.open_by_key(SHEET_ID)
    except Exception as e:
        print(f"  Sheets err: {e}")
        return None

ALERT_HDR = ["Priority","ZIP","Gold","Green","Gray",
             "News Title","News Stage","News URL","Scanned At"]
LEAD_HDR = ["Priority","Address","Property","Dot","ZIP","Lat","Lng",
            "News Source","Scanned At"]
PIPE_HDR = ["Stage","Score","Title","URL","Published","First Seen",
            "Last Seen","ZIPs","Auto Promoted","Snippet"]

def write_alerts_to_sheet(ss, alerts):
    if not ss or not alerts: return
    try:
        try: ws = ss.worksheet(HUNTER_ALERTS_TAB)
        except:
            ws = ss.add_worksheet(HUNTER_ALERTS_TAB, rows=2000, cols=12)
        if not ws.get_all_values():
            ws.update(range_name="A1", values=[ALERT_HDR])
        rows = [[a["priority"], a["zip"], a["gold"], a["green"], a["gray"],
                 a["news_title"], a["news_stage"], a["news_url"], a["scanned_at"]]
                for a in alerts]
        ws.append_rows(rows, value_input_option="USER_ENTERED")
        print(f"  ✓ Wrote {len(rows)} alerts to '{HUNTER_ALERTS_TAB}'")
    except Exception as e:
        print(f"  Sheet err: {e}")

def write_leads_to_sheet(ss, leads):
    if not ss or not leads: return
    try:
        try: ws = ss.worksheet(HUNTER_LEADS_TAB)
        except:
            ws = ss.add_worksheet(HUNTER_LEADS_TAB, rows=10000, cols=12)
        if not ws.get_all_values():
            ws.update(range_name="A1", values=[LEAD_HDR])
        rows = [[L["priority"], L["address"], L["property_type"], L["dot_color"],
                 L["zip"], L["lat"], L["lng"], L["news_source"], L["scanned_at"]]
                for L in leads]
        ws.append_rows(rows, value_input_option="USER_ENTERED")
        print(f"  ✓ Wrote {len(rows)} leads to '{HUNTER_LEADS_TAB}'")
    except Exception as e:
        print(f"  Sheet err: {e}")

def write_pipeline_to_sheet(ss, pipeline):
    if not ss: return
    by_stage = defaultdict(list)
    for k, e in pipeline.get("entries", {}).items():
        row = [
            e.get("stage",""), e.get("score",0),
            e.get("title","")[:200], e.get("url",""),
            e.get("date_published",""), e.get("first_seen",""),
            e.get("last_seen",""),
            ", ".join(e.get("zips",[]))[:100],
            e.get("auto_promoted",""),
            e.get("snippet","")[:400],
        ]
        by_stage[e.get("stage","")].append(row)
    for stage in by_stage:
        by_stage[stage].sort(key=lambda r: -r[1])

    def write_tab(name, rows):
        try:
            try: ws = ss.worksheet(name)
            except: ws = ss.add_worksheet(name, rows=max(len(rows)+50,500), cols=12)
            ws.clear()
            ws.update(range_name="A1", values=[PIPE_HDR])
            if rows:
                ws.update(range_name="A2", values=rows)
            print(f"  ✓ {name} ({len(rows)})")
        except Exception as e:
            print(f"  Tab err {name}: {e}")

    all_rows = []
    for s in ["LIT","CONSTRUCTION","PERMIT","BEAD","SATURATED"]:
        all_rows.extend(by_stage.get(s, []))
    write_tab(PIPELINE_TAB, all_rows)
    write_tab(LIT_TAB, by_stage.get("LIT", []))
    write_tab(PERMIT_TAB, by_stage.get("PERMIT", []))
    write_tab(BEAD_TAB, by_stage.get("BEAD", []))


# ── HUNT MODE ─────────────────────────────────────────────────────
def collect_hot_zips(pipeline, top_n=30):
    """Pull ranked ZIPs from pipeline. LIT and CONSTRUCTION first."""
    stage_priority = {"LIT":4, "CONSTRUCTION":3, "PERMIT":2, "BEAD":1, "SATURATED":0}
    zip_scores = defaultdict(lambda: {"score":0, "best":None})
    for k, e in pipeline.get("entries", {}).items():
        for z in e.get("zips", []):
            sp = stage_priority.get(e.get("stage",""), 0)
            score = e.get("score",0) + sp * 10
            cur = zip_scores[z]
            if score > cur["score"]:
                cur["score"] = score
                cur["best"] = e
    ranked = sorted(zip_scores.items(), key=lambda x: -x[1]["score"])
    return ranked[:top_n]

def run_hunt(pipeline, top_n=30):
    print("\n" + "=" * 60)
    print(f"HUNT — top {top_n} hot ZIPs from pipeline")
    print("=" * 60)

    cfg = load_calibration()
    if not cfg:
        print("\n❌ No calibration. Run --calibrate first.")
        return [], []

    hot = collect_hot_zips(pipeline, top_n=top_n)
    if not hot:
        print("\nNo hot ZIPs in pipeline yet. Run --news-only first to build pipeline.")
        return [], []

    # Save for downstream tools
    with open(HOT_ZIPS_FILE, "w") as f:
        for z, _ in hot:
            f.write(z + "\n")
    print(f"Saved hot ZIPs to {HOT_ZIPS_FILE}")

    print(f"\n⚠ Make sure youachieve.att.com is open and visible.")
    print(f"⚠ DO NOT touch the mouse during scans.")
    print(f"\nStarting in {START_DELAY}s...")
    time.sleep(START_DELAY)

    all_alerts = []
    all_leads = []
    for i, (z, info) in enumerate(hot, 1):
        print(f"\n[{i}/{len(hot)}] ZIP {z} (score {info['score']})")
        try:
            alert, leads = hunt_zip(z, news_context=info.get("best"))
            if alert:
                all_alerts.append(alert)
                all_leads.extend(leads)
                # ALARM
                print("\n" + "🔥" * 30)
                print(f"  HOT ZIP: {z}  {alert['priority']}")
                print(f"  Gold:{alert['gold']} Green:{alert['green']} Gray:{alert['gray']}")
                print("🔥" * 30)
        except KeyboardInterrupt:
            print("\nStopped.")
            break
        except Exception as e:
            print(f"  err: {e}")

    return all_alerts, all_leads


# ── TEST MODE ─────────────────────────────────────────────────────
def test_mode():
    cfg = load_calibration()
    if not cfg:
        print("\n❌ No calibration. Run --calibrate first.")
        return
    print("\n" + "=" * 60)
    print("🧪 TEST MODE")
    print("=" * 60)
    print("\nType ZIPs one by one. Each gets scanned (auto-zooms in 3 levels).")
    print("Type 'q' to quit.\n")
    print(f"⚠ Make sure youachieve.att.com is open and visible.")
    print(f"⚠ DO NOT touch the mouse during scans.\n")
    input("Press Enter when ready... ")

    all_alerts = []
    all_leads = []

    while True:
        z = input("\n📍 ZIP to scan (or 'q'): ").strip()
        if z.lower() in ("q","quit","exit",""):
            break
        if not (z.isdigit() and len(z) == 5):
            print("  Enter a 5-digit ZIP")
            continue
        try:
            alert, leads = hunt_zip(z)
            if alert:
                all_alerts.append(alert)
                all_leads.extend(leads)
                print(f"\n  🔥 ALERT: {alert['priority']}")
            else:
                print(f"  💀 Nothing hot, moved on")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"  err: {e}")

    print(f"\n\nTest done. {len(all_alerts)} alerts, {len(all_leads)} leads.")
    if all_leads:
        ans = input("Write to Google Sheet? (y/n): ").strip().lower()
        if ans == "y":
            ss = connect_sheet()
            if ss:
                write_alerts_to_sheet(ss, all_alerts)
                write_leads_to_sheet(ss, all_leads)


# ── MAIN ──────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--calibrate", action="store_true",
                        help="2-point calibration (search bar + safe map spot)")
    parser.add_argument("--test", action="store_true",
                        help="Type ZIPs manually, scan each")
    parser.add_argument("--news-only", action="store_true",
                        help="Run news pass, skip scanning")
    parser.add_argument("--hunt", action="store_true",
                        help="Full nightly: news + hunt top ZIPs")
    parser.add_argument("--scan-only", action="store_true",
                        help="Skip news pass, just scan saved hot ZIPs")
    parser.add_argument("--top", type=int, default=30,
                        help="Top N ZIPs to hunt (default 30)")
    parser.add_argument("--since", type=int, default=180,
                        help="News lookback in days (default 180 = 6mo)")
    parser.add_argument("--state", type=str, default=None,
                        help="Limit to one state (e.g. AL, TX)")
    parser.add_argument("--no-sheet", action="store_true")
    parser.add_argument("--no-update", action="store_true")
    parser.add_argument("--reset", action="store_true",
                        help="Wipe pipeline state")
    args = parser.parse_args()

    if not args.no_update:
        check_update()

    print("\n" + "#" * 60)
    print(f"  FIBER HUNTER (standalone) v{VERSION}")
    print(f"  News + Pipeline + Hunt across {len(ATT_STATES)} states")
    print("#" * 60)

    if args.calibrate:
        if not SCAN_AVAILABLE:
            print("ERROR: pyautogui not installed")
            sys.exit(1)
        calibrate()
        return

    if args.test:
        if not SCAN_AVAILABLE:
            print("ERROR: pyautogui not installed")
            sys.exit(1)
        test_mode()
        return

    if args.reset and os.path.exists(PIPELINE_FILE):
        os.remove(PIPELINE_FILE)
        print("Pipeline reset.")

    states = [args.state] if args.state else ATT_STATES

    # NEWS PASS
    pipeline = load_pipeline()
    print(f"\nExisting pipeline: {len(pipeline.get('entries',{}))} entries")

    if not args.scan_only:
        items = run_news_pass(states, since_days=args.since)
        new, updated = merge_pipeline(pipeline, items)
        print(f"\n  New: {new}  Updated: {updated}")
        save_pipeline(pipeline)

        counts = Counter(e["stage"] for e in pipeline["entries"].values())
        print("\nPipeline by stage:")
        emojis = {"PERMIT":"🌱","BEAD":"💰","CONSTRUCTION":"🚧","LIT":"🔥","SATURATED":"💀"}
        for stage in ["PERMIT","BEAD","CONSTRUCTION","LIT","SATURATED"]:
            print(f"  {emojis.get(stage,'')} {stage:<14} {counts.get(stage, 0)}")

    # HUNT
    all_alerts = []
    all_leads = []
    if args.hunt or args.scan_only:
        all_alerts, all_leads = run_hunt(pipeline, top_n=args.top)

    # WRITE TO SHEET
    if not args.no_sheet:
        ss = connect_sheet()
        if ss:
            print("\nWriting to Google Sheet...")
            write_pipeline_to_sheet(ss, pipeline)
            if all_alerts:
                write_alerts_to_sheet(ss, all_alerts)
            if all_leads:
                write_leads_to_sheet(ss, all_leads)

    # SUMMARY
    print("\n" + "#" * 60)
    print("DONE")
    print("#" * 60)
    counts = Counter(e["stage"] for e in pipeline.get("entries",{}).values())
    print(f"Pipeline: {sum(counts.values())} entries total")
    if all_alerts:
        print(f"\n🔥 ALERTS THIS RUN: {len(all_alerts)}")
        for a in all_alerts[:10]:
            print(f"   {a['zip']}  {a['priority']}  Gold:{a['gold']}/Green:{a['green']}")
    if all_leads:
        print(f"\nLeads captured: {len(all_leads)}")


if __name__ == "__main__":
    main()
