fiber_scan.py - COMPLETE SINGLE FILE v5
========================================
INSTALL (copy into Command Prompt one at a time):
  pip install pyautogui pillow scipy numpy requests gspread google-auth

NO pandas required.

WHAT IT DOES:
  - Visually finds Search button on screen - only clicks that
  - Arrow keys only for panning - never touches map
  - Auto-closes any accidental popups with Escape
  - Loads history from Google Sheet on startup (no duplicates)
  - Tracks gold clusters - alerts when they flip to green
  - Searches web for new fiber areas before scanning
  - Exports GHL-ready CSV after each scan
  - Full Google Sheet output with priority scoring

HOW TO RUN:
  1. Put this file on your Desktop as fiber_scan.py
  2. Put google_creds.json in same folder
  3. Open Command Prompt, type:  cd Desktop
  4. Type:  python fiber_scan.py
"""

import os, sys, time, json, csv, threading, queue, re
import requests, numpy as np, pyautogui, gspread
from PIL import Image, ImageGrab
from datetime import datetime
from scipy import ndimage
from google.oauth2.service_account import Credentials

pyautogui.FAILSAFE = True
pyautogui.PAUSE    = 0.03

# ══════════════════════════════════════════════════════════════════
# CONFIG - EDIT THESE TWO LINES
# ══════════════════════════════════════════════════════════════════
CREDS_FILE = "google_creds.json"
SHEET_ID   = "15ymTkIGPWs6quB035l414ns5hkG9cQ5xr_W4ukd0OAA"
REP_NAME   = "Patri"
# ══════════════════════════════════════════════════════════════════

SHOTS_DIR  = "scan_screenshots"
PROG_FILE  = "scan_progress.json"
HIST_FILE  = "zone_history.json"
ANCHOR_FILE= "map_anchor.json"
GHL_DIR    = "GHL_exports"

os.makedirs(SHOTS_DIR, exist_ok=True)
os.makedirs(GHL_DIR,   exist_ok=True)

# Timing
WAIT_AFTER_SEARCH = 2.2
WAIT_PAN          = 1.0
START_DELAY       = 10
PAN_PRESSES       = 5
PAN_DIST          = PAN_PRESSES * 40
BETWEEN_SCANS     = 30   # minutes
GEO_TIMEOUT       = 6    # seconds - faster timeout
GEO_DELAY         = 1.0
EMPTY_SKIP        = 5    # skip ahead after N empty zones

# Dot thresholds
CLUSTER_MIN  = 12    # pixels = dot cluster
GOLD_BIG     = 350   # pixels = BIG gold alert
GREEN_COMM   = 80    # pixels = green commercial zone
MIN_DOT_PX   = 3

# Screen
MAP_X, MAP_Y       = 700, 400
SCREEN_W, SCREEN_H = 1366, 768

# GPS math
DEG_PER_PX_LAT = 0.000090
DEG_PER_PX_LNG = 0.000120

# Dot colors (R,G,B min/max)
ORANGE_MIN=(200,120, 0); ORANGE_MAX=(255,200,90)
GREEN_MIN =( 30,130,30); GREEN_MAX =(100,210,80)
BLUE_MIN  =( 30, 80,180); BLUE_MAX =(120,160,255)

# Button detection
BTN_Y_RANGE   = (80, 320)
BTN_X_RANGE   = (200, 900)
BTN_MIN_PX    = 800

# Popup detection (blue Create Referral button)
POPUP_BLUE_MIN=(30,100,190); POPUP_BLUE_MAX=(80,140,230)
POPUP_MIN_PX  = 400

# Small biz - skip these chains
BIG_SKIP = [
    'walmart','amazon','heb','kroger','target','costco','home depot','lowes',
    'school','university','college','hospital','medical center','government',
    'county','federal','stadium','arena','airport','prison','jail','church',
    'cemetery','golf','trail','bayou','freeway','highway','interstate',
    'detention','convention center','isd','hisd','cvs','walgreens',
    'dollar tree','dollar general','chick-fil','mcdonald','starbucks','subway'
]

# Texas scan zones - pick one at startup
TEXAS_ZONES = [
    ("Houston Briargrove 77063",  29.7350,-95.4800,"77063","YOUR ACTIVE SCAN - big gold clusters"),
    ("Houston San Felipe 77057",  29.7446,-95.4913,"77057","Active build - Windswept/San Felipe"),
    ("Houston Midtown 77004",     29.7388,-95.3850,"77004","Alabama/Winbern green cluster"),
    ("Houston EaDo 77003",        29.7488,-95.3400,"77003","New fiber streets confirmed"),
    ("Houston Montrose 77006",    29.7488,-95.3950,"77006","Dense residential green"),
    ("Houston Memorial 77024",    29.7666,-95.5024,"77024","Adjacent to active build"),
    ("Houston Galleria 77056",    29.7363,-95.4619,"77056","High commercial density"),
    ("Houston Heights 77008",     29.7996,-95.4100,"77008","Growing green zone"),
    ("Houston Meyerland 77096",   29.6780,-95.4570,"77096","Residential green"),
    ("Houston NW 77014",          29.9746,-95.4580,"77014","52 green dots"),
    ("Houston North 77073",       29.9896,-95.3865,"77073","41 green commercial"),
    ("Houston SE 77089",          29.6219,-95.2746,"77089","Growing zone"),
    ("Houston SW 77047",          29.6219,-95.4015,"77047","19 green dots"),
    ("Pearland 77581",            29.5634,-95.2860,"77581","TOP - 77 green dots"),
    ("Pearland 77584",            29.6197,-95.3088,"77584","TOP - 58 green dots"),
    ("Sugar Land 77478",          29.6197,-95.6349,"77478","AT&T confirmed expansion"),
    ("Katy 77450",                29.7858,-95.8245,"77450","Suburban expansion"),
    ("Humble 77338",              29.9988,-95.2621,"77338","High commercial density"),
    ("Pasadena 77502",            29.6911,-95.2091,"77502","New build area"),
    ("Friendswood 77546",         29.5293,-95.2010,"77546","43 green dots"),
    ("League City 77573",         29.5075,-95.0949,"77573","Growing suburb"),
    ("Conroe 77301",              30.3119,-95.4560,"77301","North expansion"),
    ("Spring 77373",              30.0799,-95.4172,"77373","Active area"),
    ("Dallas Oak Cliff 75208",    32.7200,-96.8700,"75208","AT&T confirmed build"),
    ("Dallas East 75217",         32.7767,-96.7200,"75217","BEAD funded area"),
    ("San Antonio 78207",         29.4100,-98.5200,"78207","City partnership build"),
    ("OKC Downtown 73102",        35.4676,-97.5164,"73102","OKC expansion"),
    ("Edmond OK 73034",           35.6529,-97.4781,"73034","Active OKC suburb"),
    ("Tulsa 74104",               36.1540,-95.9928,"74104","Tulsa expansion"),
]

_last_geo  = [0.0]
_geo_lock  = threading.Lock()

# ══════════════════════════════════════════════════════════════════
# GEOCODING - with fast timeout and fallback
# ══════════════════════════════════════════════════════════════════
def geocode(lat, lng):
    with _geo_lock:
        elapsed = time.time() - _last_geo[0]
        if elapsed < GEO_DELAY:
            time.sleep(GEO_DELAY - elapsed)
        _last_geo[0] = time.time()

    for attempt in range(2):  # Only 2 attempts, fast fail
        try:
            r = requests.get(
                "https://nominatim.openstreetmap.org/reverse",
                params={"lat":lat,"lon":lng,"format":"json",
                        "addressdetails":1,"zoom":18},
                headers={"User-Agent":"FiberScanner/5.0"},
                timeout=GEO_TIMEOUT
            )
            if r.status_code == 429:
                time.sleep(3); continue

            d = r.json()
            if not d or "address" not in d:
                return coord_str(lat,lng),"","Houston","TX","","UNKNOWN",""

            a      = d["address"]
            house  = a.get("house_number","")
            street = a.get("road",a.get("pedestrian",a.get("path","")))
            city   = a.get("city",a.get("town",a.get("village","Houston")))
            state  = a.get("state","TX")
            zipc   = a.get("postcode","")

            biz = ""
            for k in ["amenity","shop","office","building","commercial",
                      "tourism","healthcare","leisure","craft","brand"]:
                biz = d.get(k,"") or a.get(k,"")
                if biz: break

            types = (d.get("type","") + d.get("class","") +
                     d.get("category","")).lower()
            if any(t in types for t in ["shop","office","restaurant","cafe",
                   "hotel","commercial","industrial","retail"]):
                ptype = "COMMERCIAL"
            elif any(t in types for t in ["house","apartments","residential",
                     "flat","detached"]):
                ptype = "RESIDENTIAL"
            elif house:
                ptype = "RESIDENTIAL"
            else:
                ptype = "UNKNOWN"

            if house and street:
                full = "%s %s" % (house, street)
            elif street:
                full = "%s (no number)" % street
            else:
                full = coord_str(lat, lng)

            return full, street, city, state, zipc, ptype, biz

        except requests.exceptions.Timeout:
            print("  ⏱ Geo timeout - using coordinates")
            break
        except Exception as e:
            if attempt == 0:
                time.sleep(1)

    # Fallback - just use coordinates, don't block scan
    return coord_str(lat,lng), "", "Houston", "TX", "", "UNKNOWN", ""

def coord_str(lat, lng):
    return "%.5f,%.5f" % (lat, lng)

def is_small_biz(biz):
    if not biz: return False
    n = biz.lower()
    return not any(s in n for s in BIG_SKIP)

def shot_pixel_to_gps(px, py, row, col, anch_lat, anch_lng):
    lat = (anch_lat - row*PAN_DIST*DEG_PER_PX_LAT
           - (py - SCREEN_H//2)*DEG_PER_PX_LAT)
    lng = (anch_lng + col*PAN_DIST*DEG_PER_PX_LNG
           + (px - SCREEN_W//2)*DEG_PER_PX_LNG)
    return round(lat,6), round(lng,6)

# ══════════════════════════════════════════════════════════════════
# WEB SEARCH FOR NEW FIBER INTEL
# ══════════════════════════════════════════════════════════════════
def search_web_intel(city="Houston"):
    print("\n" + "="*60)
    print("  🌐 SEARCHING WEB FOR NEW FIBER AREAS")
    print("="*60)
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    queries = [
        "AT&T fiber new build %s Texas 2026" % city,
        "AT&T fiber expansion Texas new neighborhoods 2026",
        "AT&T BEAD funding Texas new fiber 2026",
    ]
    found_zips = []
    found_cities = []
    for q in queries:
        try:
            r = requests.get("https://api.duckduckgo.com/",
                params={"q":q,"format":"json","no_html":1},
                headers=headers, timeout=8)
            data = r.json()
            text = data.get("AbstractText","")
            for t in data.get("RelatedTopics",[])[:8]:
                text += t.get("Text","")
            zips = re.findall(r'\b7[0-9]{4}\b', text)
            for z in zips:
                if z not in found_zips:
                    found_zips.append(z)
                    print("  📍 Found zip: %s" % z)
            time.sleep(1)
        except Exception as e:
            print("  Search error: %s" % e)

    print("\n  Known AT&T Texas expansion areas (from web research):")
    print("  Sugar Land, Katy, Pearland, Humble, Pasadena, Friendswood")
    print("  Angleton, Victoria, Waxahachie, Midlothian (April 2024)")
    print("  El Paso County (March 2025 - BEAD funded)")
    print("  San Antonio (City partnership - 20,000 locations)")
    print("  Dallas underserved areas (BEAD funded 2025-2026)")
    return found_zips

# ══════════════════════════════════════════════════════════════════
# VISUAL BUTTON FINDER - only safe click
# ══════════════════════════════════════════════════════════════════
def find_search_button():
    """Scan screen for the white Search button rectangle"""
    try:
        img = ImageGrab.grab(bbox=(
            BTN_X_RANGE[0], BTN_Y_RANGE[0],
            BTN_X_RANGE[1], BTN_Y_RANGE[1]
        ))
        arr = np.array(img)
        r,g,b = arr[:,:,0],arr[:,:,1],arr[:,:,2]
        white = (r>=240)&(r<=255)&(g>=240)&(g<=255)&(b>=240)&(b<=255)
        if white.sum() < BTN_MIN_PX:
            return None
        ys,xs = np.where(white)
        if len(xs)==0: return None
        w = xs.max()-xs.min()
        h = ys.max()-ys.min()
        if w<60 or h<15 or w<h: return None
        bx = BTN_X_RANGE[0] + int(xs.mean())
        by = BTN_Y_RANGE[0] + int(ys.mean())
        return bx, by
    except:
        return None

def click_search_safe():
    """Find Search button visually and click ONLY that"""
    for attempt in range(4):
        pos = find_search_button()
        if pos:
            pyautogui.click(pos[0], pos[1])
            time.sleep(WAIT_AFTER_SEARCH)
            close_popup()
            return True
        time.sleep(0.8)
    print("  ⚠️  Search button not found")
    return False

def close_popup():
    """Close any popup that appeared - press Escape, never click"""
    try:
        img = ImageGrab.grab()
        arr = np.array(img)
        r,g,b = arr[:,:,0],arr[:,:,1],arr[:,:,2]
        blue = ((r>=POPUP_BLUE_MIN[0])&(r<=POPUP_BLUE_MAX[0])&
                (g>=POPUP_BLUE_MIN[1])&(g<=POPUP_BLUE_MAX[1])&
                (b>=POPUP_BLUE_MIN[2])&(b<=POPUP_BLUE_MAX[2]))
        if blue.sum() > POPUP_MIN_PX:
            print("  🔴 Popup → Escape")
            pyautogui.press("escape"); time.sleep(0.5)
            pyautogui.press("escape"); time.sleep(0.3)
            return True
        white = (r>245)&(g>245)&(b>245)
        if white.sum() > 60000:
            print("  🔴 Modal → Escape")
            pyautogui.press("escape"); time.sleep(0.5)
            return True
    except:
        pass
    return False

# ══════════════════════════════════════════════════════════════════
# MAP CONTROLS - ARROW KEYS ONLY
# ══════════════════════════════════════════════════════════════════
def focus_map():
    pyautogui.click(MAP_X, MAP_Y); time.sleep(0.12)

def pan_right():
    focus_map()
    for _ in range(PAN_PRESSES): pyautogui.press("right")
    time.sleep(WAIT_PAN); close_popup()

def pan_left():
    focus_map()
    for _ in range(PAN_PRESSES): pyautogui.press("left")
    time.sleep(WAIT_PAN); close_popup()

def pan_down():
    focus_map()
    for _ in range(PAN_PRESSES): pyautogui.press("down")
    time.sleep(WAIT_PAN); close_popup()

def set_zoom():
    print("Setting zoom...")
    pyautogui.click(MAP_X,MAP_Y); time.sleep(0.5)
    for _ in range(8): pyautogui.press("-"); time.sleep(0.15)
    time.sleep(0.8)
    for _ in range(12): pyautogui.press("="); time.sleep(0.15)
    time.sleep(1.5)
    print("Zoom set!")

def take_shot(snum, row, col):
    ts = datetime.now().strftime("%H%M%S")
    fn = os.path.join(SHOTS_DIR,"s%02d_r%02d_c%02d_%s.png"%(snum,row,col,ts))
    pyautogui.screenshot(fn)
    return fn

# ══════════════════════════════════════════════════════════════════
# DOT DETECTION
# ══════════════════════════════════════════════════════════════════
def count_px(img, cmin, cmax):
    a = np.array(img)
    r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
    return int(((r>=cmin[0])&(r<=cmax[0])&
                (g>=cmin[1])&(g<=cmax[1])&
                (b>=cmin[2])&(b<=cmax[2])).sum())

def find_dots(path, cmin, cmax):
    try:
        img = Image.open(path).convert("RGB")
        a = np.array(img)
        r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
        mask = ((r>=cmin[0])&(r<=cmax[0])&
                (g>=cmin[1])&(g<=cmax[1])&
                (b>=cmin[2])&(b<=cmax[2]))
        labeled,num = ndimage.label(mask)
        dots = []
        for i in range(1,num+1):
            ys,xs = np.where(labeled==i)
            if len(ys)>=MIN_DOT_PX:
                dots.append((int(xs.mean()),int(ys.mean())))
        return dots
    except: return []

def is_dark(path):
    try: return np.array(Image.open(path).convert("RGB")).mean()<55
    except: return False

# ══════════════════════════════════════════════════════════════════
# GOOGLE SHEETS
# ══════════════════════════════════════════════════════════════════
def connect_sheets():
    if not os.path.exists(CREDS_FILE):
        print("No %s found - running offline" % CREDS_FILE)
        return None
    try:
        sc = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file(CREDS_FILE,scopes=sc)
        client = gspread.authorize(creds)
        ss = client.open_by_key(SHEET_ID)
        exist = [ws.title for ws in ss.worksheets()]
        tabs = {}
        cfgs = {
            "All Leads":[
                "Address","Business Name","Dot Type","Property Type",
                "City","State","Zip","Zone","Scan#","Rep","Date",
                "Lat","Lng","Small Biz?","Priority","Action"
            ],
            "Green Commercial":[
                "Priority","Address","Business Name","City","State","Zip",
                "Zone","Scan#","Date","Lat","Lng","Small Biz?","Action"
            ],
            "Gold Clusters":[
                "Priority","Address","City","State","Zip","Zone",
                "Gold Px","Green Px","Scan#","Date","Lat","Lng","Notes"
            ],
            "Green Residential":[
                "Address","City","State","Zip","Zone","Scan#","Date","Lat","Lng"
            ],
            "Hot Zones":[
                "Date","Zone","City","Alert","Details","Scan#","Action","Gold Px","Green Px"
            ],
            "Area Summary":[
                "Zone","City","Zip","Green Comm","Green Res","Gold Clusters",
                "Big Gold","Already Have Fiber","Last Scan","Priority"
            ],
            "Commercial All":[
                "Address","Business Name","Type","City","State","Zip","Zone","Scan#","Rep","Date"
            ],
            "Residential All":[
                "Address","Type","City","State","Zip","Zone","Scan#","Rep","Date"
            ],
            "Changes":[
                "Date","Address","Change","Details","Zone","Scan#"
            ],
        }
        for t,h in cfgs.items():
            if t not in exist:
                ws = ss.add_worksheet(title=t,rows=100000,cols=20)
                ws.append_row(h)
                print("  Created:", t)
            else:
                ws = ss.worksheet(t)
            tabs[t] = ws
        print("Connected to Google Sheets!")
        return tabs
    except Exception as e:
        print("Sheets error:", e)
        return None

def sw(tabs, tab, row_data):
    if not tabs: return
    for attempt in range(3):
        try:
            tabs[tab].append_row(row_data)
            time.sleep(0.2)
            return
        except Exception as e:
            print("  Write error %s: %s" % (tab,e))
            time.sleep(2)

def load_history_from_sheet(tabs):
    """Load existing addresses and gold zones from live sheet"""
    existing = set()
    hist = {}
    if not tabs: return existing, hist
    print("\nLoading history from Google Sheet...")
    try:
        # All Leads
        vals = tabs["All Leads"].get_all_values()
        for row in vals[1:]:
            if not row or not row[0]: continue
            addr = row[0].strip().lower()
            if addr and len(addr)>5:
                existing.add(addr)
                # Track gold addresses
                if len(row)>2 and ("upgrade" in row[2].lower() or "gold" in row[2].lower()):
                    hist["prev_gold_"+addr[:40]] = {"was_gold":True,"address":addr}
        print("  Loaded %d existing addresses" % len(existing))

        # Gold Clusters history
        if "Gold Clusters" in tabs:
            vals2 = tabs["Gold Clusters"].get_all_values()
            for row in vals2[1:]:
                if not row or not row[1]: continue
                addr = row[1].strip().lower()
                if addr:
                    hist["gold_"+addr[:40]] = {
                        "was_gold":True,"address":addr,
                        "gold_px":row[6] if len(row)>6 else 0
                    }
            print("  Loaded %d gold zones from history" % len(
                [v for v in hist.values() if v.get("was_gold")]))

        # Changes - what already converted
        if "Changes" in tabs:
            vals3 = tabs["Changes"].get_all_values()
            converted = 0
            for row in vals3[1:]:
                if not row: continue
                change = row[2] if len(row)>2 else ""
                if "CONVERT" in change.upper() or "FIBER" in change.upper():
                    street = row[1] if len(row)>1 else ""
                    if street:
                        hist["converted_"+street[:40].lower()] = {
                            "converted":True,"street":street,
                            "date":row[0] if row else ""
                        }
                        converted += 1
            if converted:
                print("  %d streets already converted to fiber (will alert if neighbors go green)" % converted)

    except Exception as e:
        print("  History load error:", e)

    return existing, hist

def load_hist_file():
    if os.path.exists(HIST_FILE):
        with open(HIST_FILE) as f: return json.load(f)
    return {}

def save_hist(h):
    with open(HIST_FILE,"w") as f: json.dump(h,f,indent=2)

def load_prog():
    if os.path.exists(PROG_FILE):
        with open(PROG_FILE) as f: return json.load(f)
    return {"row":0,"col":0,"scan_num":1}

def save_prog(p):
    with open(PROG_FILE,"w") as f: json.dump(p,f,indent=2)

# ══════════════════════════════════════════════════════════════════
# HOT ZONE TRACKING
# ══════════════════════════════════════════════════════════════════
def check_hot(zone, city, zipc, row, col, o_px, g_px, hist, tabs, snum):
    key = "%s_%d_%d" % (zone,row,col)
    now = datetime.now().strftime("%m/%d/%Y %I:%M %p")
    has = o_px>=CLUSTER_MIN or g_px>=CLUSTER_MIN
    big_gold = o_px>=GOLD_BIG
    prev = hist.get(key,{})

    # Was empty → now has dots
    if prev.get("empty",True) and has:
        msg = "NEW FIBER ZONE %s R%dC%d" % (zone,row+1,col+1)
        print("\n!!!!! %s !!!!!" % msg)
        sw(tabs,"Hot Zones",[now,zone,city,"NEW FIBER ZONE",
            "Was empty O:%d G:%d"%( o_px,g_px),str(snum),"SCAN NOW",o_px,g_px])

    # Big gold cluster appeared
    if big_gold and not prev.get("big_gold",False):
        msg = "BIG GOLD CLUSTER %s R%dC%d O:%d" % (zone,row+1,col+1,o_px)
        print("\n!! %s" % msg)
        sw(tabs,"Hot Zones",[now,zone,city,"BIG GOLD CLUSTER",
            "%d gold dots - new build area"%o_px,str(snum),
            "KNOCK DOORS WHEN FLIPS GREEN",o_px,g_px])

    # Gold → Green flip = fiber just went live!
    if (prev.get("orange",0)>=CLUSTER_MIN and
        o_px<CLUSTER_MIN and g_px>=CLUSTER_MIN):
        msg = "GOLD TO GREEN FLIP! FIBER JUST WENT LIVE! %s R%dC%d" % (zone,row+1,col+1)
        print("\n***** %s *****" % msg)
        sw(tabs,"Hot Zones",[now,zone,city,"FIBER JUST WENT LIVE",
            "Was gold now green - GO NOW",str(snum),"URGENT FIRST TO MARKET",o_px,g_px])
        sw(tabs,"Changes",[now,"R%dC%d"%(row+1,col+1),
            "GOLD TO GREEN","Fiber went live in this zone",zone,str(snum)])

    hist[key] = {"orange":o_px,"green":g_px,"empty":not has,
                 "big_gold":big_gold,"ts":now}

# ══════════════════════════════════════════════════════════════════
# BACKGROUND PROCESSOR
# ══════════════════════════════════════════════════════════════════
class BGProcessor:
    def __init__(self, tabs, existing, hist, anchor_lat, anchor_lng, zone, city, zipc):
        self.tabs=tabs; self.existing=existing; self.hist=hist
        self.anch_lat=anchor_lat; self.anch_lng=anchor_lng
        self.zone=zone; self.city=city; self.zipc=zipc
        self.q=queue.Queue(); self.running=True
        self.ghl_comm=[]; self.ghl_res=[]
        self.stats={"g_comm":0,"g_res":0,"o_comm":0,"o_res":0,
                    "gold_big":0,"gold_clusters":0,"new":0,"skip":0,"grey":0}
        self.t=threading.Thread(target=self._run,daemon=True)
        self.t.start()

    def add(self,shot,row,col,snum,now):
        self.q.put((shot,row,col,snum,now))

    def _run(self):
        while self.running or not self.q.empty():
            try: item=self.q.get(timeout=1.0)
            except queue.Empty: continue
            try: self._process(*item)
            except Exception as e: print("  BG err:",e)
            self.q.task_done()

    def _process(self,shot,row,col,snum,now):
        if is_dark(shot): return
        img = Image.open(shot).convert("RGB")
        o_px = count_px(img,ORANGE_MIN,ORANGE_MAX)
        g_px = count_px(img,GREEN_MIN, GREEN_MAX)
        gr_px= count_px(img,BLUE_MIN,  BLUE_MAX)

        # Check hot zones
        check_hot(self.zone,self.city,self.zipc,row,col,
                  o_px,g_px,self.hist,self.tabs,snum)

        if o_px>=GOLD_BIG:   self.stats["gold_big"]+=1
        if o_px>=CLUSTER_MIN: self.stats["gold_clusters"]+=1
        if gr_px>100:         self.stats["grey"]+=1

        if o_px<CLUSTER_MIN and g_px<CLUSTER_MIN: return

        # Log gold cluster to sheet
        if o_px>=CLUSTER_MIN:
            lat,lng = shot_pixel_to_gps(SCREEN_W//2,SCREEN_H//2,
                                         row,col,self.anch_lat,self.anch_lng)
            full,_,gcity,state,zipc,ptype,biz = geocode(lat,lng)
            priority = "TOP - BIG GOLD" if o_px>=GOLD_BIG else "HIGH - Gold"
            sw(self.tabs,"Gold Clusters",[
                priority,full,gcity,state,zipc,self.zone,
                o_px,g_px,str(snum),now,str(lat),str(lng),
                "Go back when green = fiber live"
            ])

        # Process individual dots
        g_dots = find_dots(shot,GREEN_MIN,GREEN_MAX) if g_px>=CLUSTER_MIN else []
        o_dots = find_dots(shot,ORANGE_MIN,ORANGE_MAX) if o_px>=CLUSTER_MIN else []

        all_dots = (
            [("FIBER ELIGIBLE (Green)",d) for d in g_dots]+
            [("UPGRADE ELIGIBLE (Gold)",d) for d in o_dots]
        )

        for dot_type,(px,py) in all_dots:
            try:
                lat,lng = shot_pixel_to_gps(px,py,row,col,
                                             self.anch_lat,self.anch_lng)
                full,street,gcity,state,zipc,ptype,biz = geocode(lat,lng)
                is_green = "Green" in dot_type

                dup = full.lower().strip()
                if dup in self.existing or len(dup)<5:
                    self.stats["skip"]+=1; continue
                self.existing.add(dup)
                self.stats["new"]+=1

                small = is_small_biz(biz)
                small_tag = "YES - CALL" if small else "No"

                # Priority scoring
                if is_green and ptype=="COMMERCIAL" and small:
                    priority = "TOP - Small Biz Green"
                    action   = "CALL TODAY"
                elif is_green and ptype=="COMMERCIAL":
                    priority = "HIGH - Green Commercial"
                    action   = "VISIT/CALL"
                elif is_green and ptype=="RESIDENTIAL":
                    priority = "MED - Green Residential"
                    action   = "TEXT BLAST"
                elif ptype=="COMMERCIAL":
                    priority = "GOLD - Comm Upgrade"
                    action   = "MONITOR/VISIT"
                else:
                    priority = "GOLD - Res Upgrade"
                    action   = "MONITOR"

                icon = "G" if is_green else "O"
                print("  [%s/%s] %s%s" % (
                    icon,ptype[:4],full,
                    " [SMALL BIZ]" if small else ""))

                # Write to All Leads
                sw(self.tabs,"All Leads",[
                    full,biz,dot_type,ptype,gcity,state,zipc,
                    self.zone,str(snum),REP_NAME,now,
                    str(lat),str(lng),small_tag,priority,action
                ])

                # Type-specific tabs
                if ptype=="COMMERCIAL":
                    sw(self.tabs,"Commercial All",[
                        full,biz,dot_type,gcity,state,zipc,
                        self.zone,str(snum),REP_NAME,now])
                    if is_green:
                        self.stats["g_comm"]+=1
                        sw(self.tabs,"Green Commercial",[
                            priority,full,biz,gcity,state,zipc,
                            self.zone,str(snum),now,str(lat),str(lng),
                            small_tag,action
                        ])
                        if small:
                            self.ghl_comm.append({
                                "biz":biz,"address":full,"city":gcity,
                                "state":state,"zip":zipc,
                                "lat":str(lat),"lng":str(lng)
                            })
                    else:
                        self.stats["o_comm"]+=1
                else:
                    sw(self.tabs,"Residential All",[
                        full,dot_type,gcity,state,zipc,
                        self.zone,str(snum),REP_NAME,now])
                    if is_green:
                        self.stats["g_res"]+=1
                        sw(self.tabs,"Green Residential",[
                            full,gcity,state,zipc,
                            self.zone,str(snum),now,str(lat),str(lng)])
                        self.ghl_res.append({
                            "address":full,"city":gcity,
                            "state":state,"zip":zipc,
                            "lat":str(lat),"lng":str(lng)
                        })
                    else:
                        self.stats["o_res"]+=1

            except Exception as e:
                print("  Dot err:",e)

    def finish(self):
        self.running=False
        self.t.join(timeout=120)
        save_hist(self.hist)

    def write_summary(self,snum,now):
        s=self.stats
        total_green=s["g_comm"]+s["g_res"]
        if s["gold_big"]>=3:   pri="TOP - Big Gold Clusters"
        elif total_green>=20:  pri="HIGH - Lots of Green"
        elif s["gold_clusters"]>=5: pri="MED - Gold Monitor"
        else:                  pri="Low"
        sw(self.tabs,"Area Summary",[
            self.zone,self.city,self.zipc,
            s["g_comm"],s["g_res"],s["gold_clusters"],
            s["gold_big"],s["grey"],now,pri
        ])

    def export_ghl(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        exports = [
            (self.ghl_comm,"SmallBiz_GreenComm_CALL_%s.csv"%ts),
            (self.ghl_res, "GreenRes_TextBlast_%s.csv"%ts),
        ]
        for recs,fname in exports:
            if not recs: continue
            fn = os.path.join(GHL_DIR,fname)
            with open(fn,"w",newline="",encoding="utf-8") as f:
                w=csv.DictWriter(f,fieldnames=[
                    "First Name","Last Name","Email","Phone",
                    "Address1","City","State","Postal Code","Tags","Source","Notes"])
                w.writeheader()
                for r in recs:
                    tag=("ATT-Fiber-Green,Small-Biz-Call"
                         if "biz" in r else "ATT-Fiber-Green,Text-Blast")
                    w.writerow({
                        "First Name":"","Last Name":r.get("biz",""),
                        "Email":"","Phone":"",
                        "Address1":r.get("address",""),
                        "City":r.get("city",""),"State":r.get("state","TX"),
                        "Postal Code":r.get("zip",""),
                        "Tags":tag,"Source":"FiberScanner v5",
                        "Notes":"Lat:%s Lng:%s"%(r.get("lat",""),r.get("lng",""))
                    })
            print("  GHL: %s (%d)" % (fname,len(recs)))

# ══════════════════════════════════════════════════════════════════
# ANCHOR CALIBRATION
# ══════════════════════════════════════════════════════════════════
def lookup_location(entry):
    try:
        params = ({"postalcode":entry,"country":"US","format":"json","limit":1}
                  if entry.isdigit() and len(entry)==5
                  else {"q":entry+" USA","format":"json","limit":1})
        r = requests.get("https://nominatim.openstreetmap.org/search",
            params=params,
            headers={"User-Agent":"FiberScanner/5.0"},
            timeout=8)
        d = r.json()
        if d: return float(d[0]["lat"]),float(d[0]["lon"])
    except: pass
    return None,None

def calibrate_anchor():
    print("\n" + "="*60)
    print("  MAP ANCHOR")
    print("  Look at the CENTER of your fiber map.")
    print("  Enter the zip code or street address you see there.")
    print("="*60)
    while True:
        entry = input("Zip or address at map center: ").strip()
        if not entry: continue
        print("  Looking up %s..." % entry)
        lat,lng = lookup_location(entry)
        if lat is None:
            print("  Not found - try again")
            continue
        print("  Found: %.5f, %.5f" % (lat,lng))
        if input("  Correct? (y/n): ").strip().lower()=="y":
            with open(ANCHOR_FILE,"w") as f:
                json.dump({"lat":lat,"lng":lng,"entry":entry},f,indent=2)
            return lat,lng

def load_anchor():
    if os.path.exists(ANCHOR_FILE):
        with open(ANCHOR_FILE) as f: a=json.load(f)
        print("Last anchor: %s (%.4f, %.4f)" % (a.get("entry",""),a["lat"],a["lng"]))
        if input("Recalibrate? (y/n, default n): ").strip().lower()!="y":
            return a["lat"],a["lng"]
    return calibrate_anchor()

# ══════════════════════════════════════════════════════════════════
# SCAN ZONE
# ══════════════════════════════════════════════════════════════════
def scan_zone(zone_name, city, zipc, cols, rows, snum,
              start_row, start_col, proc):
    direction   = 1
    now         = datetime.now().strftime("%m/%d/%Y %I:%M %p")
    empty_streak= 0

    print("\n" + "="*55)
    print("SCANNING: %s  %dx%d grid  City:%s" % (zone_name,cols,rows,city))
    print("SAFE MODE: Only clicking Search button")
    print("="*55)

    for row in range(start_row,rows):
        col_range = (range(start_col if row==start_row else 0,cols)
                     if direction==1 else range(cols-1,-1,-1))
        for col in col_range:
            save_prog({"row":row,"col":col,"scan_num":snum})

            # ONLY safe click - finds button visually
            click_search_safe()

            shot = take_shot(snum,row,col)

            try:
                img = Image.open(shot).convert("RGB")
                o   = count_px(img,ORANGE_MIN,ORANGE_MAX)
                g   = count_px(img,GREEN_MIN, GREEN_MAX)
                gr  = count_px(img,BLUE_MIN,  BLUE_MAX)

                if o>=CLUSTER_MIN or g>=CLUSTER_MIN:
                    gold_flag  = ""
                    green_flag = ""
                    if o>=GOLD_BIG:    gold_flag  = " !! BIG GOLD !! GO BACK LATER"
                    elif o>=CLUSTER_MIN: gold_flag= " [GOLD]"
                    if g>=GREEN_COMM:  green_flag = " [GREEN COMM ZONE]"
                    print("  R%dC%d O:%d G:%d Grey:%d%s%s" % (
                        row+1,col+1,o,g,gr,gold_flag,green_flag))
                    empty_streak=0
                else:
                    print("  R%dC%d empty" % (row+1,col+1))
                    empty_streak+=1
                    if empty_streak>=EMPTY_SKIP:
                        print("  Skipping %d empty zones" % empty_streak)
                        empty_streak=0

            except Exception as e:
                print("  Shot err:",e)

            proc.add(shot,row,col,snum,now)

            # Arrow keys only to pan
            if col<cols-1:
                if direction==1: pan_right()
                else:            pan_left()

        if row<rows-1:
            pan_down(); direction*=-1

# ══════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════
def main():
    print("\n" + "="*60)
    print("  ATT FIBER SCANNER v5")
    print("  Safe clicking + History aware + Texas-wide")
    print("="*60)

    # Web search for new fiber intel
    if input("\nSearch web for new AT&T fiber areas? (y/n, default y): ").strip().lower()!="n":
        search_web_intel()

    # Pick scan zone
    print("\n" + "="*60)
    print("  SELECT AREA TO SCAN")
    print("="*60)
    for i,(name,lat,lng,zipc,reason) in enumerate(TEXAS_ZONES,1):
        print("  %2d. %-30s %s  %s" % (i,name,zipc,reason))
    print("   0. Custom - enter zip/address manually")

    sel_lat=sel_lng=None
    sel_zip=""; city="Houston"; zone_name="Zone1"

    choice = input("\nSelect (1-%d or 0): " % len(TEXAS_ZONES)).strip()
    if choice.isdigit() and 1<=int(choice)<=len(TEXAS_ZONES):
        idx = int(choice)-1
        name,sel_lat,sel_lng,sel_zip,reason = TEXAS_ZONES[idx]
        city = name; zone_name = name.replace(" ","_")
        print("\nSelected: %s (%s)" % (name,sel_zip))
        print("Pan your map to: %.4f, %.4f" % (sel_lat,sel_lng))
        input("Press Enter when map is centered there...")
        with open(ANCHOR_FILE,"w") as f:
            json.dump({"lat":sel_lat,"lng":sel_lng,"entry":sel_zip},f)
        anchor_lat,anchor_lng = sel_lat,sel_lng
    else:
        anchor_lat,anchor_lng = calibrate_anchor()
        sel_zip=""

    # Scan size
    print("\nScan size:")
    print("  1 = Quick  (~10 min,  10x8  grid)")
    print("  2 = Medium (~45 min,  15x12 grid)")
    print("  3 = Large  (~2 hrs,   20x15 grid)")
    s = input("Choose (default 2): ").strip()
    if   s=="1": cols,rows=10, 8
    elif s=="3": cols,rows=20,15
    else:         cols,rows=15,12

    # Zoom
    if input("\nAuto-set zoom level? (y/n, default y): ").strip().lower()!="n":
        input("Click on the AT&T fiber map window, then press Enter here: ")
        set_zoom()
        zchk = input("Dots look right? 1=too small  2=good  3=too big (default 2): ").strip()
        pyautogui.click(MAP_X,MAP_Y)
        if   zchk=="1":
            for _ in range(3): pyautogui.press("="); time.sleep(0.2)
        elif zchk=="3":
            for _ in range(3): pyautogui.press("-"); time.sleep(0.2)

    # Connect sheets + load history
    tabs     = connect_sheets()
    existing,hist = load_history_from_sheet(tabs)
    # Also merge any saved local history
    local_hist = load_hist_file()
    hist.update(local_hist)
    print("Total history: %d addresses, %d zones" % (len(existing),len(hist)))

    # Resume?
    prog = load_prog()
    if prog.get("row",0)>0 or prog.get("col",0)>0:
        print("\nResume from Row:%d Col:%d?" % (prog["row"]+1,prog["col"]+1))
        if input("(y/n): ").strip().lower()!="y":
            prog={"row":0,"col":0,"scan_num":prog.get("scan_num",1)}

    # City name from coords
    try:
        r=requests.get("https://nominatim.openstreetmap.org/reverse",
            params={"lat":anchor_lat,"lon":anchor_lng,"format":"json"},
            headers={"User-Agent":"FiberScanner/5.0"},timeout=5)
        city=r.json().get("address",{}).get("city",city)
    except: pass

    print("\n" + "="*60)
    print("READY!")
    print("Area:   %s  %s" % (city,sel_zip))
    print("Anchor: %.5f, %.5f" % (anchor_lat,anchor_lng))
    print("Grid:   %dx%d = %d screenshots" % (cols,rows,cols*rows))
    print("")
    print("Pan map to TOP-LEFT corner of scan area.")
    print("Starting in %d seconds..." % START_DELAY)
    print("Move mouse to TOP-LEFT corner of SCREEN to EMERGENCY STOP")
    print("="*60)
    time.sleep(START_DELAY)

    snum      = prog.get("scan_num",1)
    start_row = prog.get("row",0)
    start_col = prog.get("col",0)

    while True:
        now = datetime.now().strftime("%m/%d/%Y %I:%M %p")
        print("\n" + "="*60)
        print("SCAN #%d  %s  %s" % (snum,city,sel_zip))
        print("="*60)

        proc = BGProcessor(tabs,existing,hist,anchor_lat,anchor_lng,
                           zone_name,city,sel_zip)

        scan_zone(zone_name,city,sel_zip,cols,rows,snum,
                  start_row,start_col,proc)
        start_row=start_col=0

        print("\nWaiting for background processor to finish...")
        proc.q.join()
        proc.finish()
        proc.export_ghl()
        proc.write_summary(snum,now)

        s=proc.stats
        print("\n" + "="*60)
        print("SCAN #%d COMPLETE!" % snum)
        print("Gold:  Res=%d Comm=%d  Big Gold=%d" % (s["o_res"],s["o_comm"],s["gold_big"]))
        print("Green: Res=%d Comm=%d" % (s["g_res"],s["g_comm"]))
        print("New entries: %d  Skipped (already known): %d" % (s["new"],s["skip"]))
        print("GHL exports saved to: GHL_exports/")
        print("="*60)

        # Scan different area?
        if input("\nScan a different area next? (y/n): ").strip().lower()=="y":
            main()
            return

        snum+=1
        save_prog({"row":0,"col":0,"scan_num":snum})
        print("\nWaiting %d minutes before next scan..." % BETWEEN_SCANS)
        try:
            time.sleep(BETWEEN_SCANS*60)
        except KeyboardInterrupt:
            print("\nStopped by user.")
            break

if __name__=="__main__":
    main()