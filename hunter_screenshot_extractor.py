import re, os, json, time, csv, glob
import numpy as np
from PIL import Image
from scipy import ndimage
import urllib.request

VERSION = "0.2"

PHONE_DIR = "/storage/emulated/0/Download/hunter_screenshots"
PC_DIR = os.path.join(os.path.expanduser("~"), "Optimus", "hunter_screenshots")
SCREENSHOTS_DIR = PHONE_DIR if os.path.isdir(PHONE_DIR) else PC_DIR
OUTPUT_CSV = os.path.join(os.path.dirname(SCREENSHOTS_DIR) or ".", "extracted_dots.csv")

MAX_DOTS_PER_SHOT = 3
SLEEP_BETWEEN_GEOCODE = 1.1
DELETE_JUNK = False

PAN_PIXELS = 150
LAT_PER_PIXEL = -0.000015
LNG_PER_PIXEL = 0.000020
COLS_PER_ZONE = 50
ROWS_PER_ZONE = 40
MAP_LEFT, MAP_TOP, MAP_RIGHT, MAP_BOTTOM = 50, 100, 1350, 720

GREEN_MIN = (30, 130, 30); GREEN_MAX = (100, 210, 80)
GOLD_MIN = (220, 160, 0); GOLD_MAX = (255, 200, 60)
GREY_MIN = (140, 140, 160); GREY_MAX = (190, 190, 210)

MIN_DOT_PIXELS = 3
MAX_DOT_PIXELS = 800
MAX_DOT_BBOX_AREA = 1500
MIN_DOT_COMPACTNESS = 0.45
MAX_DOT_ASPECT = 2.5

ZIP_CENTROIDS = {
    '36607': (30.6850, -88.0567), '71301': (31.2932, -92.4666),
    '71328': (31.0865, -92.0782), '71360': (31.3225, -92.4334),
    '73007': (35.7228, -97.4400), '73013': (35.6528, -97.4781),
    '73034': (35.6850, -97.4781), '73049': (35.6964, -97.3753),
    '77002': (29.7572, -95.3656), '77003': (29.7424, -95.3535),
    '77004': (29.7282, -95.3613), '78617': (30.1391, -97.6172),
    '78702': (30.2647, -97.7186), '78704': (30.2415, -97.7666),
    '78721': (30.2748, -97.6839), '78725': (30.2638, -97.6261),
    '78739': (30.1862, -97.8950), '78741': (30.2386, -97.7250),
    '78742': (30.2331, -97.6839), '78744': (30.1932, -97.7430),
    '78745': (30.2200, -97.8000), '78747': (30.1456, -97.7464),
    '78748': (30.1700, -97.8330), '78749': (30.2167, -97.8550),
}

def parse_filename(fn):
    m = re.match(r'i(\d+)_scan(\d+)_(.+?)_r(\d+)_c(\d+)_(\d+)\.png', fn)
    if not m:
        return None
    return dict(zone=m.group(3), row=int(m.group(4)), col=int(m.group(5)))

def decode_zone(zone):
    parts = zone.split('_', 1)
    prefix = parts[0]
    dirname = parts[1] if len(parts) > 1 else 'Center'
    if dirname == 'Center':
        return prefix, 0, 0
    m = re.match(r'R(\d+)([TRBL])(\d+)', dirname)
    if not m:
        return prefix, None, None
    ring, side, n = int(m.group(1)), m.group(2), int(m.group(3))
    if side == 'T': return prefix, -ring + n, -ring
    if side == 'R': return prefix, ring, -ring + 1 + n
    if side == 'B': return prefix, ring - 1 - n, ring
    if side == 'L': return prefix, -ring, ring - 1 - n
    return prefix, None, None

def filename_origin(fn):
    info = parse_filename(fn)
    if not info:
        return None
    prefix, ox, oy = decode_zone(info['zone'])
    if prefix not in ZIP_CENTROIDS or ox is None or oy is None:
        return None
    zip_lat, zip_lng = ZIP_CENTROIDS[prefix]
    zlat = ROWS_PER_ZONE * PAN_PIXELS * abs(LAT_PER_PIXEL)
    zlng = COLS_PER_ZONE * PAN_PIXELS * LNG_PER_PIXEL
    return (zip_lat + oy * zlat, zip_lng + ox * zlng, info['row'], info['col'], prefix)

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

def find_dots(cropped_img, cmin, cmax):
    arr = np.array(cropped_img.convert("RGB"))
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    mask = ((r >= cmin[0]) & (r <= cmax[0]) & (g >= cmin[1]) & (g <= cmax[1]) & (b >= cmin[2]) & (b <= cmax[2]))
    labeled, num = ndimage.label(mask)
    dots = []
    for i in range(1, num + 1):
        ys, xs = np.where(labeled == i)
        if _is_dot_shape(len(ys), ys, xs):
            dots.append((int(xs.mean()), int(ys.mean())))
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
        if a.get("house_number") and a.get("road"):
            addr = f"{a['house_number']} {a['road']}"
        elif a.get("road"):
            addr = a['road']
        result = {"address": addr, "city": a.get("city") or a.get("town") or a.get("village") or "", "state": a.get("state", ""), "zip": a.get("postcode", "")}
        _geo_cache[key] = result
        time.sleep(SLEEP_BETWEEN_GEOCODE)
        return result
    except Exception as e:
        return {"error": str(e)[:80]}

def process_one(path):
    fn = os.path.basename(path)
    origin = filename_origin(fn)
    if not origin:
        return {"file": fn, "status": "SKIP no zip centroid"}
    sl, sg, row, col, zipc = origin
    try:
        img = Image.open(path)
    except Exception as e:
        return {"file": fn, "status": f"BAD_IMG: {e}"}

    cropped = img.crop((MAP_LEFT, MAP_TOP, MAP_RIGHT, MAP_BOTTOM))
    green = find_dots(cropped, GREEN_MIN, GREEN_MAX)
    gold = find_dots(cropped, GOLD_MIN, GOLD_MAX)
    grey = find_dots(cropped, GREY_MIN, GREY_MAX)

    results = []
    for color, dots in [("GREEN", green), ("GOLD", gold)]:
        for px, py in dots[:MAX_DOTS_PER_SHOT]:
            full_x = px + MAP_LEFT
            full_y = py + MAP_TOP
            lat, lng = pixel_to_latlng(full_x, full_y, row, col, sl, sg)
            geo = reverse_geocode(lat, lng)
            results.append({"file": fn, "zip": zipc, "row": row, "col": col, "color": color, "pixel_x": px, "pixel_y": py, "full_pixel_x": full_x, "full_pixel_y": full_y, "lat": lat, "lng": lng, "address": geo.get("address", ""), "city": geo.get("city", ""), "state": geo.get("state", ""), "geocoded_zip": geo.get("zip", ""), "geo_error": geo.get("error", "")})
    return {"file": fn, "status": "OK", "green_count": len(green), "gold_count": len(gold), "grey_count": len(grey), "results": results}

def main():
    if not os.path.isdir(SCREENSHOTS_DIR):
        print(f"ERROR: dir not found: {SCREENSHOTS_DIR}")
        input("Press Enter to close...")
        return
    shots = sorted(glob.glob(os.path.join(SCREENSHOTS_DIR, "*.png")))
    print(f"Found {len(shots)} screenshots")

    fieldnames = ["file","zip","row","col","color","pixel_x","pixel_y","full_pixel_x","full_pixel_y","lat","lng","address","city","state","geocoded_zip","geo_error"]
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for i, path in enumerate(shots, 1):
            r = process_one(path)
            if r.get("status") != "OK":
                print(f"[{i}/{len(shots)}] {r['file']}: {r.get('status')}")
                continue
            print(f"[{i}/{len(shots)}] {r['file']}: G={r['green_count']} O={r['gold_count']} grey={r['grey_count']}")
            for row in r["results"]:
                w.writerow(row); f.flush()
                print(f"    {row['color']}: {row['lat']},{row['lng']} {row.get('address','')}")
    print(f"\nDONE. Output: {OUTPUT_CSV}")
    input("Press Enter to close...")

if __name__ == "__main__":
    main()
