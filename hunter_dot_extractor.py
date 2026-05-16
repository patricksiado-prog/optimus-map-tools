#!/usr/bin/env python3
"""
Hunter Screenshot Dot Extractor v1.4
Only complete addresses written to sheet.
Dedup by Drive file ID — never processes same image twice.
AUTO_UPDATE disabled to prevent self-overwrite.
"""

import re, os, json, time, glob
import numpy as np
from PIL import Image
from scipy import ndimage
import urllib.request
import requests
from datetime import datetime

try:
    import gspread
    from google.oauth2.service_account import Credentials
    SHEETS_OK = True
except ImportError:
    SHEETS_OK = False
    print("WARNING: gspread not installed. CSV only mode.")

VERSION = "1.4"

try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    pass

import os as _os
try:
    import certifi as _certifi
    _os.environ["REQUESTS_CA_BUNDLE"] = _certifi.where()
    _os.environ["SSL_CERT_FILE"] = _certifi.where()
except ImportError:
    pass

# ============================================================
# FIX 1: AUTO_UPDATE DISABLED — prevents self-overwrite with stale GitHub code
# ============================================================
AUTO_UPDATE = False
GITHUB_RAW_URL = "https://raw.githubusercontent.com/patricksiado-prog/optimus-map-tools/main/hunter_dot_extractor.py"
LOCAL_SCRIPT = os.path.abspath(__file__)

PHONE_DIR = "/storage/emulated/0/Download/hunter_screenshots"
PC_DIR = os.path.join(os.path.expanduser("~"), "Optimus", "hunter_screenshots")
SCREENSHOTS_DIR = PHONE_DIR if os.path.isdir(PHONE_DIR) else PC_DIR

CREDS_FILE = next((p for p in [
    r"C:\Users\patri\Desktop\google_creds.json",
    "/storage/emulated/0/Download/google_creds.json",
    "/sdcard/Download/google_creds.json",
    os.path.join(os.path.expanduser("~"), "Desktop", "google_creds.json"),
    os.path.join(os.path.expanduser("~"), "Download", "google_creds.json"),
    "google_creds.json",
] if os.path.exists(p)), "google_creds.json")

SHEET_NAME = "ATT FIBER LEADS"
SHEET_ID = "1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA"
DRIVE_SCREENSHOTS_FOLDER = "1Go9e5S6cGGxew8QRYhzMRBMw5HFfPoQV"
USE_DRIVE = True
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp")

MAX_DOTS_PER_SHOT = 200
SLEEP_BETWEEN_GEOCODE = 1.1
PAN_PIXELS = 150
LAT_PER_PIXEL = -0.000015
LNG_PER_PIXEL = 0.000020
COLS_PER_ZONE = 50
ROWS_PER_ZONE = 40
MAP_LEFT, MAP_TOP, MAP_RIGHT, MAP_BOTTOM = 50, 100, 1350, 720

GREEN_MIN = (30, 130, 30); GREEN_MAX = (100, 210, 80)
ORANGE_MIN = (220, 160, 0); ORANGE_MAX = (255, 200, 60)
GREY_MIN = (140, 140, 160); GREY_MAX = (190, 190, 210)

MIN_DOT_PIXELS = 3
MAX_DOT_PIXELS = 800
MAX_DOT_BBOX_AREA = 1500
MIN_DOT_COMPACTNESS = 0.45
MAX_DOT_ASPECT = 2.5
MIN_DOT_CLUSTERS = 1

BLANK_STD_THRESHOLD = 12.0
BLANK_CENTER_STD_THRESHOLD = 9.0
BLANK_BRIGHT_MEAN = 240
BLANK_DARK_MEAN = 30

ZIP_CENTROIDS = {
    '31405': (32.0478, -81.0997), '36607': (30.6850, -88.0567),
    '71301': (31.2932, -92.4666), '71328': (31.0865, -92.0782),
    '71360': (31.3225, -92.4334), '73007': (35.7228, -97.4400),
    '73013': (35.6528, -97.4781), '73034': (35.6850, -97.4781),
    '73049': (35.6964, -97.3753), '77002': (29.7572, -95.3656),
    '77003': (29.7424, -95.3535), '77004': (29.7282, -95.3613),
    '78617': (30.1391, -97.6172), '78702': (30.2647, -97.7186),
    '78704': (30.2415, -97.7666), '78721': (30.2748, -97.6839),
    '78725': (30.2638, -97.6261), '78739': (30.1862, -97.8950),
    '78741': (30.2386, -97.7250), '78742': (30.2331, -97.6839),
    '78744': (30.1932, -97.7430), '78745': (30.2200, -97.8000),
    '78747': (30.1456, -97.7464), '78748': (30.1700, -97.8330),
    '78749': (30.2167, -97.8550),
}

CITY_ALIASES = {
    'Pineville': (31.3225, -92.4334), 'Alexandria': (31.2932, -92.4666),
    'Savannah': (32.0478, -81.0997), 'Houston': (29.7572, -95.3656),
    'Austin': (30.2672, -97.7431), 'Edmond': (35.6528, -97.4781),
    'Norman': (35.2226, -97.4395), 'Biloxi': (30.3960, -88.8853),
    'Mobile': (30.6850, -88.0567), 'Gulfport': (30.3674, -89.0928),
    'Midland': (31.9974, -102.0779), 'Odessa': (31.8457, -102.3676),
    'Bossier': (32.5160, -93.7321), 'Shreveport': (32.5252, -93.7502),
    'Lafayette': (30.2241, -92.0198), 'Baton': (30.4515, -91.1871),
    'NewOrleans': (29.9511, -90.0715),
}

RES_SUFFIXES = {'lane','ln','court','ct','cove','cv','way','place','pl','circle','cir','trail','trl','crossing','xing','run','hollow','glen','meadow','terrace','ter','path','pass','walk','loop','bend','point','pt','ridge','crest','springs'}
COMM_SUFFIXES = {'boulevard','blvd','highway','hwy','freeway','fwy','parkway','pkwy','expressway','expy','turnpike','plaza','square','sq'}
GRID_TOKENS = {"st","street","ave","avenue","1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th","main","broadway","market","union"}
SUBDIVISION_WORDS = {"estates","oaks","meadows","hills","creek","springs","village","ridge","pines","subdivision"}

# ============================================================
# DEDUPLICATION
# ============================================================
PROCESSED_LOG = "hunter_processed_drive_ids.txt"

def load_processed_ids():
    if not os.path.exists(PROCESSED_LOG):
        return set()
    ids = set()
    with open(PROCESSED_LOG, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                ids.add(line.split("|", 1)[0])
    return ids

def is_processed(file_id, processed_ids):
    return file_id in processed_ids

def mark_processed(file_id, filename):
    with open(PROCESSED_LOG, "a", encoding="utf-8") as f:
        f.write(f"{file_id}|{filename}\n")

def auto_update():
    if not AUTO_UPDATE: return
    try:
        print("Checking GitHub for updates...")
        r = requests.get(GITHUB_RAW_URL, timeout=10)
        if r.status_code != 200: print("GitHub update check failed"); return
        remote_code = r.text
        with open(LOCAL_SCRIPT, "r", encoding="utf-8") as f:
            local_code = f.read()
        if remote_code != local_code:
            print("New version found. Updating...")
            with open(LOCAL_SCRIPT, "w", encoding="utf-8") as f:
                f.write(remote_code)
            print("Updated. Restarting..."); os._exit(0)
        print("Already up to date.")
    except Exception as e:
        print(f"Auto-update skipped: {e}")

# ============================================================
# FIX 3: parse_filename supports BOTH old and new Hunter filename formats
# ============================================================
def parse_filename(fn):
    """
    Supports multiple Hunter filename formats:
    OLD: i1_scan01_31405_Center_r04_c04_005145.png
    NEW: i1_s01_31405_Center_r04_c04_005145.png
         i1_scan01_Pineville_Center_r00_c12_003019.png
         i1_s01_Pineville_Center_r00_c12_003019.png
    """
    base = os.path.basename(fn)
    
    # Format 1: i#_scan##_ZONE_r##_c##_##.ext (old, with leading zeros)
    m = re.match(r"i(\d+)_scan(\d+)_(.+?)_r(\d+)_c(\d+)_(\d+)\.(png|jpg|jpeg|webp)$", base, re.I)
    if m:
        return {"instance": int(m.group(1)), "scan": int(m.group(2)), "zone": m.group(3), "row": int(m.group(4)), "col": int(m.group(5))}
    
    # Format 2: i#_s##_ZONE_r##_c##_##.ext (new short scan prefix)
    m = re.match(r"i(\d+)_s(\d+)_(.+?)_r(\d+)_c(\d+)_(\d+)\.(png|jpg|jpeg|webp)$", base, re.I)
    if m:
        return {"instance": int(m.group(1)), "scan": int(m.group(2)), "zone": m.group(3), "row": int(m.group(4)), "col": int(m.group(5))}
    
    # Format 3: i#_scan##_ZONE_r##_c##.ext (no timestamp suffix)
    m = re.match(r"i(\d+)_scan(\d+)_(.+?)_r(\d+)_c(\d+)\.(png|jpg|jpeg|webp)$", base, re.I)
    if m:
        return {"instance": int(m.group(1)), "scan": int(m.group(2)), "zone": m.group(3), "row": int(m.group(4)), "col": int(m.group(5))}
    
    # Format 4: i#_s##_ZONE_r##_c##.ext (no timestamp, short prefix)
    m = re.match(r"i(\d+)_s(\d+)_(.+?)_r(\d+)_c(\d+)\.(png|jpg|jpeg|webp)$", base, re.I)
    if m:
        return {"instance": int(m.group(1)), "scan": int(m.group(2)), "zone": m.group(3), "row": int(m.group(4)), "col": int(m.group(5))}
    
    return None

def decode_zone(zone):
    parts = zone.split('_', 1)
    prefix = parts[0]
    dirname = parts[1] if len(parts) > 1 else 'Center'
    if dirname == 'Center': return prefix, 0, 0
    m = re.match(r'R(\d+)([TRBL])(\d+)', dirname)
    if not m: return prefix, None, None
    ring, side, n = int(m.group(1)), m.group(2), int(m.group(3))
    if side == 'T': return prefix, -ring + n, -ring
    if side == 'R': return prefix, ring, -ring + 1 + n
    if side == 'B': return prefix, ring - 1 - n, ring
    if side == 'L': return prefix, -ring, ring - 1 - n
    return prefix, None, None

def filename_origin(fn):
    info = parse_filename(fn)
    if not info: return None
    prefix, ox, oy = decode_zone(info["zone"])
    coords = ZIP_CENTROIDS.get(prefix) or CITY_ALIASES.get(prefix)
    if not coords or ox is None or oy is None: return None
    base_lat, base_lng = coords
    zlat = ROWS_PER_ZONE * PAN_PIXELS * abs(LAT_PER_PIXEL)
    zlng = COLS_PER_ZONE * PAN_PIXELS * LNG_PER_PIXEL
    return (base_lat + oy * zlat, base_lng + ox * zlng, info["row"], info["col"], prefix, info["instance"], info["scan"])

def pixel_to_latlng(px, py, row, col, sl, sg):
    lat = sl - (row * PAN_PIXELS * abs(LAT_PER_PIXEL)) - (py * abs(LAT_PER_PIXEL))
    lng = sg + (col * PAN_PIXELS * LNG_PER_PIXEL) + (px * LNG_PER_PIXEL)
    return round(lat, 6), round(lng, 6)

def _is_dot_shape(size, ys, xs):
    if size < MIN_DOT_PIXELS or size > MAX_DOT_PIXELS: return False
    h = ys.max() - ys.min() + 1
    w = xs.max() - xs.min() + 1
    if h * w > MAX_DOT_BBOX_AREA: return False
    if size / (h * w) < MIN_DOT_COMPACTNESS: return False
    if max(h, w) / max(min(h, w), 1) > MAX_DOT_ASPECT: return False
    return True

def count_dot_clusters(img, cmin, cmax):
    try:
        arr = np.array(img.convert("RGB"))
        r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
        mask = ((r>=cmin[0])&(r<=cmax[0])&(g>=cmin[1])&(g<=cmax[1])&(b>=cmin[2])&(b<=cmax[2]))
        labeled, num = ndimage.label(mask)
        count = 0
        for i in range(1, num+1):
            ys, xs = np.where(labeled==i)
            if _is_dot_shape(len(ys), ys, xs): count += 1
        return count
    except Exception: return 0

def is_blank_map(img):
    try:
        arr = np.array(img.convert("RGB"))
        whole_std = float(arr.std())
        whole_mean = float(arr.mean())
        if whole_std < BLANK_STD_THRESHOLD: return True
        if whole_mean >= BLANK_BRIGHT_MEAN: return True
        if whole_mean <= BLANK_DARK_MEAN: return True
        h, w = arr.shape[:2]
        center = arr[h//4:3*h//4, w//4:3*w//4]
        if float(center.std()) < BLANK_CENTER_STD_THRESHOLD: return True
        return False
    except Exception: return True

def find_dots(cropped_img, cmin, cmax):
    arr = np.array(cropped_img.convert("RGB"))
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    mask = ((r>=cmin[0])&(r<=cmax[0])&(g>=cmin[1])&(g<=cmax[1])&(b>=cmin[2])&(b<=cmax[2]))
    labeled, num = ndimage.label(mask)
    dots = []
    for i in range(1, num+1):
        ys, xs = np.where(labeled==i)
        sz = len(ys)
        if _is_dot_shape(sz, ys, xs): dots.append((int(xs.mean()), int(ys.mean()), int(sz)))
    return dots

_geo_cache = {}

def reverse_geocode(lat, lng):
    key = f"{lat:.6f},{lng:.6f}"
    if key in _geo_cache: return _geo_cache[key]
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lng}&format=json&addressdetails=1&zoom=18"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "FiberHunter/5.18"})
        with urllib.request.urlopen(req, timeout=8) as r:
            d = json.loads(r.read())
        a = d.get("address", {})
        addr = ""
        if a.get("house_number") and a.get("road"): addr = f"{a['house_number']} {a['road']}"
        elif a.get("road"): addr = a["road"]
        result = {"address": addr, "city": a.get("city") or a.get("town") or a.get("village") or "", "state": a.get("state", ""), "zip": a.get("postcode", "")}
        _geo_cache[key] = result
        time.sleep(SLEEP_BETWEEN_GEOCODE)
        return result
    except Exception:
        _geo_cache[key] = {}
        return {}

def is_complete_address(address, city, state):
    if not address or not city or not state: return False
    a = address.strip()
    if not re.match(r"^\d+\s+[A-Za-z]", a): return False
    if len(a) < 8: return False
    a_lower = a.lower()
    junk = ["unnamed","unknown","service road","frontage road","footway","path","trail","cycleway","parking lot","driveway","alley","access road","private road","unclassified","track","bridleway","steps","platform","construction","proposed","abandoned"]
    if any(j in a_lower for j in junk): return False
    bare_abbr = re.search(r"^\d+\s+(rd\b|st\b|ave\b|dr\b|ln\b|ct\b|blvd\b|hwy\b|pkwy\b)$", a_lower)
    if bare_abbr: return False
    return True

def smart_classify(address, state, biz_name="", city=""):
    a = (address or "").lower().strip()
    b = (biz_name or "").lower().strip()
    score = 0
    parts = a.split()
    for tok in parts[-3:]:
        clean = tok.strip(".,#0123456789")
        if clean in RES_SUFFIXES: score -= 3
        if clean in COMM_SUFFIXES: score += 3
    grid_hits = sum(1 for tok in parts if tok.strip(".,#") in GRID_TOKENS)
    if grid_hits >= 1: score += 2
    directional_hits = sum(1 for tok in parts if tok in ("n","s","e","w"))
    if directional_hits >= 1: score += 2
    if b and b not in ("none","no biz","unknown"): score += 5
    for word in SUBDIVISION_WORDS:
        if word in a: score -= 4
    return "COMMERCIAL" if score > 0 else "RESIDENTIAL"

def get_drive_token():
    from google.auth.transport.requests import Request
    scopes = ["https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=scopes)
    creds.refresh(Request())
    return creds.token

def list_drive_files():
    if not os.path.exists(CREDS_FILE):
        print("No google_creds.json - Drive disabled")
        return [], None
    try:
        token = get_drive_token()
        url = "https://www.googleapis.com/drive/v3/files"
        params = {"q": f"'{DRIVE_SCREENSHOTS_FOLDER}' in parents and trashed=false", "spaces": "drive", "fields": "files(id,name)", "pageSize": 1000}
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(url, params=params, headers=headers, verify=False, timeout=10)
        files = r.json().get("files", [])
        image_files = [f for f in files if f.get("name", "").lower().endswith(IMAGE_EXTS)]
        print(f"Found {len(image_files)} images in Drive ({len(files)} total files)")
        return image_files, token
    except Exception as e:
        print(f"Drive error: {e}")
        return [], None

def fetch_image_from_drive(file_id, token, retries=3):
    from io import BytesIO
    dl_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
    headers = {"Authorization": f"Bearer {token}"}
    for attempt in range(retries):
        try:
            r = requests.get(dl_url, headers=headers, timeout=30)
            if r.status_code == 200: return BytesIO(r.content)
            print(f"  Drive download attempt {attempt+1}: HTTP {r.status_code}")
        except requests.exceptions.ReadTimeout:
            print(f"  Drive timeout (attempt {attempt+1}/{retries})")
            time.sleep(2 ** attempt)
        except Exception as e:
            print(f"  Drive error: {e}")
            break
    return None

def connect_sheets():
    if not SHEETS_OK: return None
    if not os.path.exists(CREDS_FILE):
        print(f"  WARNING: {CREDS_FILE} missing - sheets disabled")
        return None
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(CREDS_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        try: ss = client.open_by_key(SHEET_ID)
        except: ss = client.open(SHEET_NAME)
        existing = [ws.title for ws in ss.worksheets()]
        tabs = {}
        for tname, headers in [
            ("Hunter Commercial", ["Address","Business Name","Dot Type","City","State","Zip","Zone","Instance","Scan #","Status","Rep","Date","Phone","Notes","Verified Color"]),
            ("Hunter Residential", ["Address","Dot Type","City","State","Zip","Zone","Instance","Scan #","Status","Rep","Date","Verified Color"]),
        ]:
            if tname not in existing:
                ws = ss.add_worksheet(title=tname, rows=1000, cols=len(headers))
                ws.append_row(headers)
            else:
                ws = ss.worksheet(tname)
            tabs[tname] = ws
        print("  Connected to Google Sheets")
        return tabs
    except Exception as e:
        print(f"  Sheet error: {e}")
        return None

def _process_img(fn, img, sl, sg, row, col, zipc, instance, scan, tabs):
    cropped = img.crop((MAP_LEFT, MAP_TOP, MAP_RIGHT, MAP_BOTTOM))
    if is_blank_map(cropped): return {"file": fn, "status": "BLANK_SKIP"}
    green_clusters = count_dot_clusters(cropped, GREEN_MIN, GREEN_MAX)
    orange_clusters = count_dot_clusters(cropped, ORANGE_MIN, ORANGE_MAX)
    if green_clusters < MIN_DOT_CLUSTERS and orange_clusters < MIN_DOT_CLUSTERS:
        return {"file": fn, "status": "NO_CLUSTERS"}
    green = find_dots(cropped, GREEN_MIN, GREEN_MAX)
    orange = find_dots(cropped, ORANGE_MIN, ORANGE_MAX)
    results = []
    written_count = 0
    now = datetime.now().strftime("%m/%d/%Y %I:%M %p")
    for color, dots in [("GREEN", green), ("ORANGE", orange)]:
        for px, py, cluster_size in dots[:MAX_DOTS_PER_SHOT]:
            full_x = px + MAP_LEFT
            full_y = py + MAP_TOP

            lat, lng = pixel_to_latlng(full_x, full_y, row, col, sl, sg)

            geo = reverse_geocode(lat, lng)
            if not geo or "address" not in geo:
                continue

            address = geo.get("address", "")
            city = geo.get("city", "")
            state = geo.get("state", "")
            geocoded_zip = geo.get("zip", "")

            # STRICT COMPLETE ADDRESS GATE
            if not is_complete_address(address, city, state):
                continue

            ptype = smart_classify(address, state, "", city)
            verified_color = "GREEN" if color == "GREEN" else "GOLD"

            result = {
                "file": fn,
                "zip": zipc,
                "row": row,
                "col": col,
                "color": color,
                "lat": lat,
                "lng": lng,
                "address": address,
                "city": city,
                "state": state,
                "geocoded_zip": geocoded_zip,
                "ptype": ptype,
                "verified_color": verified_color,
            }

            results.append(result)
            written_count += 1

            # WRITE TO SHEET
            if tabs:
                try:
                    if ptype == "COMMERCIAL":
                        tabs["Hunter Commercial"].append_row([
                            address,
                            "",
                            f"{color} dot",
                            city,
                            state,
                            geocoded_zip,
                            zipc,
                            str(instance),
                            str(scan),
                            "New",
                            "Patri",
                            now,
                            "",
                            "",
                            verified_color,
                        ])
                    else:
                        tabs["Hunter Residential"].append_row([
                            address,
                            f"{color} dot",
                            city,
                            state,
                            geocoded_zip,
                            zipc,
                            str(instance),
                            str(scan),
                            "New",
                            "Patri",
                            now,
                            verified_color,
                        ])

                except Exception as e:
                    print(f"    Sheet write error: {e}")

    return {
        "file": fn,
        "status": "OK",
        "green_count": len(green),
        "orange_count": len(orange),
        "written": written_count,
        "results": results,
    }


def process_one_img(fn, img, tabs):
    origin = filename_origin(fn)

    if not origin:
        return {"file": fn, "status": "SKIP no zip centroid"}

    sl, sg, row, col, zipc, instance, scan = origin

    return _process_img(
        fn,
        img,
        sl,
        sg,
        row,
        col,
        zipc,
        instance,
        scan,
        tabs
    )


def process_one(path, tabs):
    fn = os.path.basename(path)

    origin = filename_origin(fn)

    if not origin:
        return {"file": fn, "status": "SKIP no zip centroid"}

    sl, sg, row, col, zipc, instance, scan = origin

    try:
        img = Image.open(path)
    except Exception as e:
        return {"file": fn, "status": f"BAD_IMG: {e}"}

    return _process_img(
        fn,
        img,
        sl,
        sg,
        row,
        col,
        zipc,
        instance,
        scan,
        tabs
    )


def main():
    auto_update()

    print("=" * 70)
    print(f"HUNTER DOT EXTRACTOR v{VERSION}")
    print("ONLY COMPLETE ADDRESSES WRITTEN TO SHEET")
    print("DEDUP BY DRIVE FILE ID ENABLED")
    print("AUTO UPDATE DISABLED")
    print("=" * 70)

    tabs = connect_sheets()

    if not tabs:
        print("ERROR: Google Sheets not connected.")
        input("Press Enter to close...")
        return

    if USE_DRIVE:

        files, token = list_drive_files()

        if not files:
            print("No images found in Drive.")
            input("Press Enter to close...")
            return

        total = len(files)

        comm_count = 0
        res_count = 0
        skipped_count = 0

        already_skipped = 0
        newly_processed = 0

        processed_ids = load_processed_ids()

        print(f"Loaded {len(processed_ids)} processed Drive IDs")

        for i, f in enumerate(files, 1):

            fn = f["name"]
            file_id = f["id"]

            # DEDUP
            if is_processed(file_id, processed_ids):
                print(f"[{i}/{total}] {fn} - SKIP already processed")
                already_skipped += 1
                continue

            print(f"[{i}/{total}] {fn}")

            try:

                buf = fetch_image_from_drive(file_id, token)

                if not buf:
                    print("  SKIP - download failed")
                    skipped_count += 1
                    continue

                img = Image.open(buf)

                r = process_one_img(fn, img, tabs)

                if r.get("status") != "OK":
                    print(f"  {r.get('status')}")
                else:

                    print(
                        f"  G={r['green_count']} "
                        f"O={r['orange_count']} "
                        f"WRITTEN={r.get('written', 0)}"
                    )

                    for row in r.get("results", []):

                        ptype = row.get("ptype", "?")

                        if ptype == "COMMERCIAL":
                            comm_count += 1
                        else:
                            res_count += 1

                        print(
                            f"    {row['color']}: "
                            f"{row['address']} ({ptype})"
                        )

                # MARK PROCESSED
                mark_processed(file_id, fn)
                processed_ids.add(file_id)

                newly_processed += 1

            except Exception as e:
                print(f"  FATAL on {fn}: {e}")
                continue

        print("\n" + "=" * 70)
        print("COMPLETE")
        print(f"  Total images: {total}")
        print(f"  Previously processed skipped: {already_skipped}")
        print(f"  Newly processed this run: {newly_processed}")
        print(f"  Download failures: {skipped_count}")
        print(f"  Commercial: {comm_count}")
        print(f"  Residential: {res_count}")
        print("=" * 70)

    else:

        if not os.path.isdir(SCREENSHOTS_DIR):
            print(f"ERROR: dir not found: {SCREENSHOTS_DIR}")
            input("Press Enter to close...")
            return

        shots = []

        for ext in IMAGE_EXTS:
            shots.extend(
                glob.glob(os.path.join(SCREENSHOTS_DIR, f"*{ext}"))
            )

        shots = sorted(shots)

        total = len(shots)

        comm_count = 0
        res_count = 0

        for i, path in enumerate(shots, 1):

            try:
                r = process_one(path, tabs)

            except Exception as e:
                print(f"  FATAL: {e}")
                continue

            if r.get("status") != "OK":
                print(
                    f"[{i}/{total}] "
                    f"{r['file']}: {r.get('status')}"
                )
                continue

            print(
                f"[{i}/{total}] "
                f"{r['file']}: "
                f"G={r['green_count']} "
                f"O={r['orange_count']}"
            )

            for row in r.get("results", []):

                ptype = row.get("ptype", "?")

                if ptype == "COMMERCIAL":
                    comm_count += 1
                else:
                    res_count += 1

                print(
                    f"    {row['color']}: "
                    f"{row['address']} ({ptype})"
                )

        print("\n" + "=" * 70)
        print("COMPLETE")
        print(f"  Commercial: {comm_count}")
        print(f"  Residential: {res_count}")
        print("=" * 70)

    input("Press Enter to close...")


if __name__ == "__main__":
    main()