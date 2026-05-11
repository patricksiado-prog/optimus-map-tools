
def check_update():
    try:
        import urllib.request as u,os,sys,re
        url="https://raw.githubusercontent.com/"+GITHUB_REPO+"/"+GITHUB_BRANCH+"/"+GITHUB_FILE
        code=u.urlopen(url,timeout=10).read().decode()
        m=re.search('VERSION.*?([0-9]+[.][0-9.]+)',code)
        if not m or m.group(1)==VERSION:return
        print("Updating to v"+m.group(1))
        open(__file__,"w").write(code)
        os.execv(sys.executable,[sys.executable]+sys.argv)
    except Exception as e:print("Update skip:",e)

def load_geo_cache():
    global _geo_cache
    if os.path.exists(GEO_CACHE_FILE):
        try:
            with open(GEO_CACHE_FILE) as f:
                _geo_cache = json.load(f)
        except:
            _geo_cache = {}

def save_geo_cache():
    try:
        with open(GEO_CACHE_FILE, "w") as f:
            json.dump(_geo_cache, f)
    except:
        pass

def _rate_limit():
    with _geo_lock:
        wait = GEO_RATE - (time.time() - _geo_last[0])
        if wait > 0:
            time.sleep(wait)
        _geo_last[0] = time.time()

def now_str():
    return datetime.now().strftime("%m/%d/%Y %I:%M %p")

def _is_dot_shape(size, ys, xs):
    if size < MIN_DOT_PIXELS or size > MAX_DOT_PIXELS: return False
    h = int(ys.max()) - int(ys.min()) + 1
    w = int(xs.max()) - int(xs.min()) + 1
    if h * w > MAX_DOT_BBOX_AREA: return False
    if float(size) / float(h * w) < MIN_DOT_COMPACTNESS: return False
    if float(max(h, w)) / float(max(min(h, w), 1)) > MAX_DOT_ASPECT: return False
    return True

def _in_legend(cx, cy):
    for x0, y0, x1, y1 in LEGEND_EXCLUDE_BBOXES:
        if x0 <= cx <= x1 and y0 <= cy <= y1: return True
    return False

def is_blank_map(img):
    try:
        arr = np.array(img.convert("RGB"))
        if arr.std() < BLANK_STD_THRESHOLD: return True
        if arr.mean() >= BLANK_BRIGHT_MEAN:  return True
        if arr.mean() <= BLANK_DARK_MEAN:    return True
        h, w = arr.shape[:2]
        if arr[h//4:3*h//4, w//4:3*w//4].std() < BLANK_CENTER_STD: return True
        return False
    except:
        return True

def is_dark(path):
    try:
        return np.array(Image.open(path).convert("RGB")).mean() < 55
    except:
        return True

def count_dot_clusters(img, cmin, cmax):
    try:
        arr = np.array(img.convert("RGB"))
        r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
        mask = ((r>=cmin[0])&(r<=cmax[0])&(g>=cmin[1])&(g<=cmax[1])&(b>=cmin[2])&(b<=cmax[2]))
        labeled, num = ndimage.label(mask)
        count = 0
        for i in range(1, num+1):
            ys, xs = np.where(labeled == i)
            if _is_dot_shape(len(ys), ys, xs) and not _in_legend(int(xs.mean()), int(ys.mean())):
                count += 1
        return count
    except:
        return 0

def find_dots(path, cmin, cmax):
    try:
        img = Image.open(path).convert("RGB")
        arr = np.array(img)
        r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
        mask = ((r>=cmin[0])&(r<=cmax[0])&(g>=cmin[1])&(g<=cmax[1])&(b>=cmin[2])&(b<=cmax[2]))
        labeled, num = ndimage.label(mask)
        dots = []
        for i in range(1, num+1):
            ys, xs = np.where(labeled == i)
            sz = len(ys)
            if not _is_dot_shape(sz, ys, xs): continue
            cx, cy = int(xs.mean()), int(ys.mean())
            if _in_legend(cx, cy): continue
            dots.append((cx, cy, sz))
        return dots
    except:
        return []

def geocode(lat, lng):
    key = "%.6f,%.6f" % (lat, lng)
    with _geo_lock:
        if key in _geo_cache:
            cached = _geo_cache[key]
            return tuple(cached) if cached else None
    _rate_limit()
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lng, "format": "json",
                    "addressdetails": 1, "extratags": 1, "zoom": 18},
            headers={"User-Agent": "FiberScan/1.0"}, timeout=GEOCODE_TIMEOUT)
        d = r.json()
        if "address" not in d or not d["address"]:
            with _geo_lock: _geo_cache[key] = None
            return None
        a = d["address"]
        house  = a.get("house_number") or ""
        street = a.get("road") or a.get("pedestrian") or ""
        city   = a.get("city") or a.get("town") or a.get("village") or ""
        state  = a.get("state") or ""
        zipc   = a.get("postcode") or ""
        if not (house and street):
            with _geo_lock: _geo_cache[key] = None
            return None
        full = "%s %s" % (house, street)
        biz = ""
        extra = d.get("extratags") or {}
        if isinstance(extra, dict):
            biz = extra.get("name") or ""
        result = (full, street, city, state, zipc, biz)
        with _geo_lock: _geo_cache[key] = list(result)
        return result
    except:
        with _geo_lock: _geo_cache[key] = None
        return None

def pixel_to_latlng(px, py, row, col, sl, sg):
    lat = sl - (row * PAN_PIXELS * abs(LAT_PER_PIXEL)) - (py * abs(LAT_PER_PIXEL))
    lng = sg + (col * PAN_PIXELS * LNG_PER_PIXEL)     + (px * LNG_PER_PIXEL)
    return round(lat, 6), round(lng, 6)

def get_phone_maps(pw, address, city, state):
    query = "%s %s %s" % (address, city, state)
    try:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.google.com/maps/search/" +
                  requests.utils.quote(query), timeout=PHONE_TIMEOUT * 1000)
        page.wait_for_timeout(3000)
        content = page.content()
        browser.close()
        m = re.search(r'(\+?1?\s*[\(\-\.]?\d{3}[\)\-\.\s]\s*\d{3}[\-\.\s]\d{4})', content)
        if m:
            phone = re.sub(r'[^\d+]', '', m.group(1))
            if len(phone) >= 10:
                return phone
    except:
        pass
    return ""

TAB_HEADERS = {
    "Hunter Leads": [
        "Address", "Business Name", "Dot Type", "Property Type",
        "City", "State", "Zip", "Zone", "Instance", "Scan #",
        "Status", "Rep", "Date", "Phone", "Lat", "Lng",
        "Verified Color", "Dot Confidence", "Source Screenshot", "Scan Status",
    ],
    "Hunter Green Commercial": [
        "Address", "Business Name", "City", "State", "Zip",
        "Zone", "Instance", "Scan #", "Date", "Phone", "Lat", "Lng", "Verified Color",
    ],
    "Hunter Green Residential": [
        "Address", "City", "State", "Zip",
        "Zone", "Instance", "Scan #", "Date", "Lat", "Lng", "Verified Color",
    ],
    "Hunter Commercial": [
        "Address", "Business Name", "Dot Type", "City", "State", "Zip",
        "Zone", "Instance", "Scan #", "Status", "Rep", "Date", "Phone", "Notes", "Verified Color",
    ],
    "Hunter Residential": [
        "Address", "Dot Type", "City", "State", "Zip",
        "Zone", "Instance", "Scan #", "Status", "Rep", "Date", "Verified Color",
    ],
}

def connect_sheets():
    if not os.path.exists(CREDS_FILE):
        print("No google_creds.json — Sheets disabled.")
        return None
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets",
                  "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(CREDS_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        ss = client.open(SHEET_NAME)
        existing_tabs = [ws.title for ws in ss.worksheets()]
        tabs = {}
        for tname, headers in TAB_HEADERS.items():
            if tname not in existing_tabs:
                ws = ss.add_worksheet(title=tname, rows=1000, cols=max(20, len(headers)))
                ws.append_row(headers)
            else:
                ws = ss.worksheet(tname)
            tabs[tname] = ws
        print("Connected to Google Sheets.")
        return tabs
    except Exception as e:
        print("Sheets error: %s" % e)
        return None

def grab_map():
    return ImageGrab.grab(bbox=(MAP_LEFT, MAP_TOP, MAP_RIGHT, MAP_BOTTOM))

def dots_on_screen():
    img = grab_map()
    if is_blank_map(img): return False
    return (count_dot_clusters(img, GREEN_MIN, GREEN_MAX) >= MIN_DOT_CLUSTERS or
            count_dot_clusters(img, ORANGE_MIN, ORANGE_MAX) >= MIN_DOT_CLUSTERS or
            count_dot_clusters(img, GREY_MIN, GREY_MAX) >= MIN_DOT_CLUSTERS)

def wait_for_map(max_wait=MAX_WAIT_DOTS):
    start = time.time()
    while time.time() - start < max_wait:
        if dots_on_screen(): return True
        time.sleep(POLL_INTERVAL)
    return False

def pan(direction):
    pyautogui.moveTo(MAP_CX, MAP_CY)
    if direction == "right":
        pyautogui.drag(-PAN_PIXELS, 0, duration=0.2, button="left", _pause=False)
    elif direction == "left":
        pyautogui.drag(PAN_PIXELS, 0, duration=0.2, button="left", _pause=False)
    elif direction == "down":
        pyautogui.drag(0, -PAN_PIXELS, duration=0.2, button="left", _pause=False)
    time.sleep(WAIT_AFTER_PAN)

def calibrate_button():
    if os.path.exists(BUTTON_FILE):
        with open(BUTTON_FILE) as f:
            pos = json.load(f)
        print("  Search button: saved at (%d, %d)" % (pos["x"], pos["y"]))
        if input("  Recalibrate? (y/n, default n): ").strip().lower() != "y":
            return pos["x"], pos["y"]
    print("\nHover mouse over AT&T 'Search this area' button.")
    input("Then press Enter: ")
    x, y = pyautogui.position()
    with open(BUTTON_FILE, "w") as f:
        json.dump({"x": x, "y": y}, f)
    return x, y

def screenshot_cell(scan_num, zone_name, row, col):
    ts = datetime.now().strftime("%H%M%S")
    fn = os.path.join(SCREENSHOTS_DIR,
        "slow_scan%02d_%s_r%02d_c%02d_%s.png" % (scan_num, zone_name, row, col, ts))
    pyautogui.screenshot(fn)
    return fn

def spiral_offsets():
    yield (0, 0, "Center")
    ring = 1
    while True:
        for x in range(-ring, ring+1): yield (x, -ring, "R%dT%d"%(ring, x+ring))
        for y in range(-ring+1, ring+1): yield (ring, y, "R%dR%d"%(ring, y+ring))
        for x in range(ring-1, -ring-1, -1): yield (x, ring, "R%dB%d"%(ring, x+ring))
        for y in range(ring-1, -ring, -1): yield (-ring, y, "R%dL%d"%(ring, y+ring))
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

def lookup_city(name):
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": name + " USA", "format": "json", "limit": 1},
            headers={"User-Agent": "FiberScan/1.0"}, timeout=6)
        d = r.json()
        if d:
            return float(d[0]["lat"]), float(d[0]["lon"]), d[0].get("display_name", name)
    except:
        pass
    return None, None, None

def get_city():
    while True:
        e = input("\nEnter city or ZIP to start spiral from: ").strip()
        if not e: continue
        lat, lng, name = lookup_city(e)
        if lat is None:
            print("  Not found. Try again.")
            continue
        short = name.split(",")[0].strip() if "," in name else name
        print("  Found: %s" % name)
        return lat, lng, short

def process_cell(shot, zone, city_name, row, col, tabs, pw, scan_num, existing, counters):
    if is_dark(shot):
        counters["blank"] += 1; return
    try:
        img = Image.open(shot).convert("RGB")
    except:
        counters["blank"] += 1; return
    if is_blank_map(img):
        counters["blank"] += 1; return

    sl = zone["start_lat"]
    sg = zone["start_lng"]
    zone_name = zone["name"]

    g_cl  = count_dot_clusters(img, GREEN_MIN,  GREEN_MAX)
    o_cl  = count_dot_clusters(img, ORANGE_MIN, ORANGE_MAX)
    gr_cl = count_dot_clusters(img, GREY_MIN,   GREY_MAX)
    if g_cl < 1 and o_cl < 1 and gr_cl < 1:
        counters["empty"] += 1; return

    g_dots  = find_dots(shot, GREEN_MIN,  GREEN_MAX)
    o_dots  = find_dots(shot, ORANGE_MIN, ORANGE_MAX)
    gr_dots = find_dots(shot, GREY_MIN,   GREY_MAX)
    all_dots = (
        [("FIBER ELIGIBLE (Green)", d) for d in g_dots] +
        [("UPGRADE ELIGIBLE (Gold/Orange)", d) for d in o_dots] +
        [("EXISTING FIBER (Grey)", d) for d in gr_dots]
    )

    shot_base = os.path.basename(shot)

    for dot_type, dot in all_dots:
        px, py, sz = dot
        lat, lng = pixel_to_latlng(px, py, row, col, sl, sg)
        res = geocode(lat, lng)
        if res is None:
            counters["geo_fail"] += 1; continue
        full, street, gcity, state, zipc, biz = res

        norm = full.lower().strip()
        if norm in existing:
            counters["skip"] += 1; continue
        existing.add(norm)

        is_green = "green" in dot_type.lower()
        is_gold  = "gold"  in dot_type.lower()
        is_grey  = "grey"  in dot_type.lower()
        vc = "GREEN" if is_green else ("GOLD" if is_gold else "GREY")

        # Wait for phone before moving on
        phone = ""
        if not is_grey:
            print("  [PHONE] %s..." % full[:45], end=" ", flush=True)
            phone = get_phone_maps(pw, full, gcity, state)
            print(phone if phone else "not found")

        ptype = "RESIDENTIAL"
        for w in ["commercial","office","retail","restaurant","shop","store",
                  "business","plaza","blvd","pkwy","suite","industrial"]:
            if w in (street or "").lower() or w in (full or "").lower():
                ptype = "COMMERCIAL"; break

        tag = "GREY" if is_grey else ("COMM" if ptype == "COMMERCIAL" else "RES")
        print("  %s: %s | %s" % (tag, full[:45], phone or "no phone"))

        now = now_str()
        if tabs:
            tabs["Hunter Leads"].append_row([
                full, biz, dot_type, ptype, gcity, state, zipc,
                zone_name, "SlowHunter", str(scan_num), "New", REP_NAME, now,
                phone, str(lat), str(lng), vc, str(sz), shot_base, "OK",
            ])
            time.sleep(0.3)
            if not is_grey:
                if ptype == "COMMERCIAL":
                    tabs["Hunter Commercial"].append_row([
                        full, biz, dot_type, gcity, state, zipc,
                        zone_name, "SlowHunter", str(scan_num),
                        "New", REP_NAME, now, phone, "", vc,
                    ])
                    time.sleep(0.3)
                    if is_green:
                        tabs["Hunter Green Commercial"].append_row([
                            full, biz, gcity, state, zipc,
                            zone_name, "SlowHunter", str(scan_num),
                            now, phone, str(lat), str(lng), vc,
                        ])
                        time.sleep(0.3)
                else:
                    tabs["Hunter Residential"].append_row([
                        full, dot_type, gcity, state, zipc,
                        zone_name, "SlowHunter", str(scan_num),
                        "New", REP_NAME, now, vc,
                    ])
                    time.sleep(0.3)
                    if is_green:
                        tabs["Hunter Green Residential"].append_row([
                            full, gcity, state, zipc,
                            zone_name, "SlowHunter", str(scan_num),
                            now, str(lat), str(lng), vc,
                        ])
                        time.sleep(0.3)
        counters["new"] += 1

def main():
    print("\n" + "#"*60)
    print("  SLOW HUNTER v%s" % VERSION)
    print("  Fiber + phone per cell — no pan until phones written")
    print("#"*60)

    lat0, lng0, city_name = get_city()
    btn_x, btn_y = calibrate_button()
    tabs = connect_sheets()
    load_geo_cache()

    existing = set()
    if tabs:
        try:
            vals = tabs["Hunter Leads"].get_all_values()
            headers = vals[0] if vals else []
            phone_col = next((i for i, h in enumerate(headers) if "phone" in h.lower()), 13)
            for r in vals[1:]:
                if r and r[0]:
                    # v1.2 fix: only skip if phone already populated
                    has_phone = phone_col < len(r) and r[phone_col].strip()
                    if has_phone:
                        existing.add(r[0].lower().strip())
            print("Loaded %d existing addresses with phones (v1.2)" % len(existing))
        except:
            pass

    scan_num = 1
    counters = {"new": 0, "skip": 0, "blank": 0, "empty": 0, "geo_fail": 0}
