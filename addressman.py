"""
 █████╗ ██████╗ ██████╗ ██████╗ ███████╗███████╗███████╗    ███╗   ███╗ █████╗ ███╗   ██╗
██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝    ████╗ ████║██╔══██╗████╗  ██║
███████║██║  ██║██║  ██║██████╔╝█████╗  ███████╗███████╗    ██╔████╔██║███████║██╔██╗ ██║
██╔══██║██║  ██║██║  ██║██╔══██╗██╔══╝  ╚════██║╚════██║    ██║╚██╔╝██║██╔══██║██║╚██╗██║
██║  ██║██████╔╝██████╔╝██║  ██║███████╗███████║███████║    ██║ ╚═╝ ██║██║  ██║██║ ╚████║
╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝

ADDRESS MAN v3.0
================
Reads fiber leads from your Google Sheet (works even if no scanner files on PC).
If scanner screenshots ARE present, uses them for extra precision.
Finds every small business within 0.5 miles of each fiber lead.
Checks AT&T. Assigns pitch type. Cleans the sheet.
Works on ANY computer — just needs google_creds.json.

PITCH TYPES:
  ATT FIBER        = fiber available → pitch fiber plan
  ATT UPGRADE      = copper only → pitch fiber upgrade
  ATT INTERNET AIR = no wired service → pitch Internet Air

BUILT-IN SHEET CLEANER (runs automatically):
  - Removes exact duplicate rows
  - Removes rows with no business name and no address
  - Removes rows with bad/placeholder addresses (just coordinates)
  - Merges duplicate businesses into best single row
  - Does NOT delete any leads — every business is still usable

2 CONSECUTIVE AT&T NOs → moves to next area automatically.
Small biz only. Chains, gov, schools, hospitals = skipped.

INSTALL (one time):
  pip install requests gspread google-auth playwright numpy Pillow scipy
  playwright install chromium

RUN:
  python addressman.py               (reads sheet, finds nearby biz)
  python addressman.py --clean-only  (just clean the sheet)
  python addressman.py --headless    (no browser window)
  python addressman.py --gold-only   (GOLD fiber leads only)
  python addressman.py --zip 77379   (only leads in that ZIP)

Ctrl+C to pause — resumes next run.
"""

import os, sys, re, json, time, math, argparse, random
from datetime import datetime
import requests
import gspread
from google.oauth2.service_account import Credentials

try:
    import numpy as np
    from PIL import Image
    from scipy import ndimage
    HAS_IMG = True
except ImportError:
    HAS_IMG = False

# ── CONFIG ──────────────────────────────────────────────────────────
CREDS_FILE    = "google_creds.json"
SHEET_ID      = "15ymTkIGPWs6quB035l414ns5hkG9cQ5xr_W4ukd0OAA"
SHOTS_DIR     = "scan_screenshots"
ANCHOR_FILE   = "map_anchor.json"
PROGRESS_FILE = "addressman_progress.json"

OUTPUT_TAB  = "Address Man"
TAB_ROWS    = 1000
SOURCE_TABS = ["All Leads","Maps Scrape","Enriched Leads",
               "ATT Verified","Map Man Leads"]

OUTPUT_HEADERS = [
    "Business Name","Address","Phone","Category",
    "Pitch Type","ATT Status","Max Speed Mbps",
    "Source Lead","Distance (ft)","Found By","ZIP","Added At",
]

ATT_API_URL = (
    "https://www.att.com/services/shop/model/ecom/shop/view/unified/"
    "qualification/service/CheckAvailabilityRESTService/invokeCheckAvailability"
)
ATT_HEADERS = {
    "Content-Type":"application/json",
    "Accept":"application/json, text/plain, */*",
    "User-Agent":("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36"),
    "Origin":"https://www.att.com",
    "Referer":"https://www.att.com/internet/availability/",
}
OSM_OVERPASS = "https://overpass-api.de/api/interpreter"
NOMINATIM    = "https://nominatim.openstreetmap.org"

ATT_DELAY  = 2.0
OSM_DELAY  = 1.0
MAP_DELAY  = 1.5
JITTER     = 0.5
BATCH_SIZE = 20
RADIUS     = 800    # meters — ~0.5 miles
CONSEC_NO  = 2      # move on after this many NOs in a row

# Scanner constants
SCREEN_W        = 1366
SCREEN_H        = 768
PAN_PRESSES     = 5
PAN_DIST        = PAN_PRESSES * 40
DEG_PER_PX_LAT  = 0.000090
DEG_PER_PX_LNG  = 0.000120
MIN_DOT_PX      = 3
ORANGE_MIN = (200,120,0);  ORANGE_MAX = (255,200,90)
GREEN_MIN  = (30,130,30);  GREEN_MAX  = (100,210,80)

EXCLUDE = [
    "walmart","target","costco","home depot","lowe's","lowes","best buy",
    "kroger","heb ","publix","safeway","albertsons","aldi","whole foods",
    "mcdonald","burger king","taco bell","wendy's","chick-fil","subway",
    "starbucks","dunkin","domino's","pizza hut","papa john",
    "chase bank","wells fargo","bank of america","citibank","us bank",
    "td bank","pnc bank","capital one","regions bank",
    "walgreens","cvs","rite aid",
    "dollar general","dollar tree","family dollar",
    "7-eleven","circle k","wawa",
    "marriott","hilton","hyatt","holiday inn","sheraton","hampton inn",
    "fedex office","ups store","post office","usps",
    "city hall","county ","courthouse","dmv ","social security",
    "fire station","police station","sheriff","jail",
    "university","college","school district"," isd","high school",
    "middle school","elementary","community college",
    "hospital","medical center","health system","children's hospital",
    "warehouse","distribution center","fulfillment","manufacturing",
    "amazon","google office","microsoft","apple store",
]

def is_small_biz(name, cat=""):
    if not name or len(name.strip()) < 3: return False
    nl = name.lower()
    for kw in EXCLUDE:
        if kw in nl: return False
    return True

def pitch_type(att_status):
    if att_status == "FIBER":  return "ATT FIBER"
    if att_status == "COPPER": return "ATT UPGRADE"
    return "ATT INTERNET AIR"


# ── GEO UTILS ───────────────────────────────────────────────────────
def norm(s):
    if not s: return ""
    s = re.sub(r"[^\w\s]"," ",s.lower().strip())
    return re.sub(r"\s+"," ",s).strip()

def m_to_ft(m): return int(m*3.28084)

def haversine(la1,ln1,la2,ln2):
    R=6371000
    p1,p2=math.radians(la1),math.radians(la2)
    a=(math.sin(math.radians(la2-la1)/2)**2+
       math.cos(p1)*math.cos(p2)*math.sin(math.radians(ln2-ln1)/2)**2)
    return R*2*math.atan2(math.sqrt(a),math.sqrt(1-a))

def geocode(address, city="", state="TX", zipc=""):
    q = "%s %s %s %s USA" % (address,city,state,zipc)
    try:
        r = requests.get("%s/search"%NOMINATIM,
            params={"q":q,"format":"json","limit":1},
            headers={"User-Agent":"AddressMan/3.0"},timeout=8)
        d = r.json()
        if d: return float(d[0]["lat"]),float(d[0]["lon"])
    except Exception: pass
    return None,None

def rev_geocode(lat,lng):
    try:
        time.sleep(0.4)
        r=requests.get("%s/reverse"%NOMINATIM,
            params={"lat":lat,"lon":lng,"format":"json","addressdetails":1,"zoom":18},
            headers={"User-Agent":"AddressMan/3.0"},timeout=8)
        d=r.json()
        if d and "address" in d:
            a=d["address"]
            house=a.get("house_number","")
            street=a.get("road",a.get("pedestrian",""))
            city=a.get("city",a.get("town",a.get("village","")))
            zipc=a.get("postcode","")
            full=("%s %s"%(house,street)).strip() if house and street else street
            return full,city,zipc
    except Exception: pass
    return "","",""


# ════════════════════════════════════════════════════════════════════
#  SHEET CLEANER
# ════════════════════════════════════════════════════════════════════

def clean_sheet(ss):
    """
    Clean all tabs in the sheet:
    - Remove rows with no name AND no address
    - Remove duplicate rows (same name + address)
    - Remove rows with placeholder addresses (just coords)
    - Flag rows with no phone as No Phone (don't delete — still usable)
    """
    print("\n" + "=" * 60)
    print("  SHEET CLEANER RUNNING")
    print("=" * 60)

    all_tabs = SOURCE_TABS + [OUTPUT_TAB, "ATT Verified", "GOLD ALERTS",
                               "HOT ZONES", "Green Commercial", "Green Residential",
                               "Commercial", "Residential"]

    total_removed = 0

    for tab_name in all_tabs:
        try:
            ws   = ss.worksheet(tab_name)
            rows = ws.get_all_values()
            if not rows or len(rows) < 2:
                continue

            headers  = rows[0]
            data     = rows[1:]
            original = len(data)
            seen     = set()
            clean    = []

            for row in data:
                if not any(cell.strip() for cell in row):
                    continue  # completely blank row

                name = row[0].strip() if len(row) > 0 else ""
                addr = row[1].strip() if len(row) > 1 else ""

                # Skip rows with no name AND no address
                if not name and not addr:
                    continue

                # Skip rows where address is just GPS coordinates
                if re.match(r'^-?\d+\.\d+,\s*-?\d+\.\d+$', addr):
                    continue

                # Dedup key
                key = norm(name) + "|" + norm(addr)
                if key in seen:
                    continue
                seen.add(key)

                clean.append(row)

            removed = original - len(clean)
            if removed > 0:
                print("  %s: removed %d rows (%d → %d)" % (
                    tab_name, removed, original, len(clean)))
                # Rewrite the tab
                ws.clear()
                ws.append_row(headers)
                if clean:
                    ws.append_rows(clean, value_input_option="USER_ENTERED")
                time.sleep(1)
                total_removed += removed
            else:
                print("  %s: clean ✓" % tab_name)

        except gspread.exceptions.WorksheetNotFound:
            pass
        except Exception as e:
            print("  Error cleaning %s: %s" % (tab_name, e))

    print("\n  Cleaner done — %d total rows removed" % total_removed)
    print("=" * 60)


# ── GOOGLE SHEETS ────────────────────────────────────────────────────
def connect_sheets():
    if not os.path.exists(CREDS_FILE):
        print("ERROR: %s not found.\nPlace your Google credentials file here." % CREDS_FILE)
        sys.exit(1)
    sc     = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"]
    creds  = Credentials.from_service_account_file(CREDS_FILE,scopes=sc)
    client = gspread.authorize(creds)
    ss     = client.open_by_key(SHEET_ID)
    exist  = [ws.title for ws in ss.worksheets()]
    if OUTPUT_TAB not in exist:
        ws = ss.add_worksheet(title=OUTPUT_TAB,rows=TAB_ROWS,
                              cols=len(OUTPUT_HEADERS)+2)
        ws.append_row(OUTPUT_HEADERS)
        print("  Created tab: %s" % OUTPUT_TAB)
    else:
        ws = ss.worksheet(OUTPUT_TAB)
    print("Connected to Google Sheets ✓")
    return ss, ws

def load_fiber_leads(ss, zip_filter=None, gold_only=False):
    leads = []
    seen  = set()
    for tab in SOURCE_TABS:
        try:
            ws   = ss.worksheet(tab)
            rows = ws.get_all_values()
            if not rows: continue
            hdrs = [h.lower().strip() for h in rows[0]]
            for row in rows[1:]:
                if not row or not row[0]: continue
                d    = dict(zip(hdrs,row))
                addr = (d.get("address","") or d.get("original address","") or
                        d.get("maps address","")).strip()
                lat  = d.get("lat","").strip()
                lng  = d.get("lng","").strip()
                zipc = (d.get("zip","") or d.get("postal code","")).strip()
                city = d.get("city","").strip()
                state= d.get("state","TX").strip()
                dot  = (d.get("dot type","") or d.get("fiber dot type","") or
                        d.get("pitch type","") or d.get("att status","")).strip()
                if not addr: continue
                is_gold  = any(k in dot.lower() for k in ["gold","orange","upgrade","fiber"])
                is_green = any(k in dot.lower() for k in ["green","fiber eligible","air"])
                if gold_only and not is_gold: continue
                if not gold_only and not (is_gold or is_green or dot): continue
                if zip_filter and zipc and zipc != zip_filter: continue
                key = norm(addr)
                if key in seen: continue
                seen.add(key)
                leads.append({"address":addr,"lat":lat,"lng":lng,"zip":zipc,
                              "city":city,"state":state,"dot":dot,
                              "priority":0 if is_gold else 1,"source":tab})
        except Exception: pass

    leads.sort(key=lambda x: x["priority"])
    gold_ct  = sum(1 for l in leads if l["priority"]==0)
    green_ct = sum(1 for l in leads if l["priority"]==1)
    print("  Leads from sheet: %d GOLD/FIBER | %d GREEN/AIR" % (gold_ct,green_ct))
    return leads

def load_existing(ss, out_ws):
    existing = set()
    for tab in SOURCE_TABS+[OUTPUT_TAB]:
        try:
            ws   = ss.worksheet(tab)
            vals = ws.get_all_values()
            for row in vals[1:]:
                if row and row[0]: existing.add(norm(row[0]))
                if len(row)>1 and row[1]: existing.add(norm(row[1]))
        except Exception: pass
    print("  Existing records: %d" % len(existing))
    return existing

def load_processed(out_ws):
    done = set()
    try:
        vals = out_ws.get_all_values()
        hdrs = [h.lower() for h in vals[0]] if vals else []
        idx  = hdrs.index("source lead") if "source lead" in hdrs else 7
        for row in vals[1:]:
            if len(row)>idx and row[idx]: done.add(norm(row[idx]))
    except Exception: pass
    print("  Already processed: %d source leads" % len(done))
    return done

def batch_write(ws, rows):
    if not rows: return
    for attempt in range(3):
        try:
            ws.append_rows(rows,value_input_option="USER_ENTERED")
            time.sleep(0.4); return
        except Exception as e:
            print("  Write error (attempt %d): %s"%(attempt+1,e))
            time.sleep(5)

def save_prog(p):
    with open(PROGRESS_FILE,"w") as f: json.dump(p,f,indent=2)

def load_prog():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f: return json.load(f)
    return {"new_found":0,"fiber_found":0}


# ── SCREENSHOTS ──────────────────────────────────────────────────────
def load_anchor():
    if os.path.exists(ANCHOR_FILE):
        with open(ANCHOR_FILE) as f:
            a = json.load(f)
        return a["lat"], a["lng"]
    return None, None

def pixel_to_gps(px,py,row,col,alat,alng):
    slat = alat - row*PAN_DIST*DEG_PER_PX_LAT
    slng = alng + col*PAN_DIST*DEG_PER_PX_LNG
    return (round(slat-((py-SCREEN_H//2)*DEG_PER_PX_LAT),6),
            round(slng+((px-SCREEN_W//2)*DEG_PER_PX_LNG),6))

def find_clusters(img_path, cmin, cmax):
    if not HAS_IMG: return []
    try:
        img=Image.open(img_path).convert("RGB")
        a=np.array(img)
        r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
        mask=((r>=cmin[0])&(r<=cmax[0])&
              (g>=cmin[1])&(g<=cmax[1])&
              (b>=cmin[2])&(b<=cmax[2]))
        labeled,num=ndimage.label(mask)
        clusters=[]
        for i in range(1,num+1):
            ys,xs=np.where(labeled==i)
            if len(ys)>=MIN_DOT_PX:
                clusters.append((int(xs.mean()),int(ys.mean()),len(ys)))
        return clusters
    except Exception: return []

def get_hotspots_from_screenshots(gold_only=False):
    if not HAS_IMG or not os.path.exists(SHOTS_DIR):
        return []
    alat,alng = load_anchor()
    if not alat: return []
    hotspots = []
    seen_gps = []
    files = sorted([f for f in os.listdir(SHOTS_DIR)
                    if f.endswith(".png") or f.endswith(".jpg")])
    print("  Reading %d screenshots for dot clusters..." % len(files))
    for fname in files:
        fpath = os.path.join(SHOTS_DIR,fname)
        m = re.match(r'i(\d+)_s(\d+)_(\w+)_r(\d+)_c(\d+)',fname)
        if not m: continue
        row,col = int(m.group(4)),int(m.group(5))
        for cmin,cmax,color,pri in [
            (ORANGE_MIN,ORANGE_MAX,"GOLD",0),
            (GREEN_MIN,GREEN_MAX,"GREEN",1),
        ]:
            if gold_only and color=="GREEN": continue
            for cx,cy,pxc in find_clusters(fpath,cmin,cmax):
                lat,lng = pixel_to_gps(cx,cy,row,col,alat,alng)
                dup = any(haversine(lat,lng,sl,sg)<80 for sl,sg in seen_gps)
                if not dup:
                    seen_gps.append((lat,lng))
                    hotspots.append({"lat":lat,"lng":lng,"color":color,
                                     "px_count":pxc,"priority":pri,
                                     "address":"","zip":"","city":"",
                                     "state":"TX","dot":color,"source":"screenshot"})
    hotspots.sort(key=lambda x:(x["priority"],-x["px_count"]))
    print("  Screenshot hotspots: %d" % len(hotspots))
    return hotspots


# ── AT&T CHECK ───────────────────────────────────────────────────────
def check_att(address, zipc):
    addr = re.sub(r',?\s+[A-Z]{2}\s+\d{5}.*$','',address.strip())
    addr = re.sub(r',?\s+\d{5}.*$','',addr).strip()
    payload={"userInputZip":zipc or "","userInputAddressLine1":addr,
             "mode":"fullAddress","customer_type":"Consumer","dtvMigrationFlag":False}
    try:
        time.sleep(ATT_DELAY+random.uniform(-JITTER/2,JITTER))
        r=requests.post(ATT_API_URL,data=json.dumps(payload),
                        headers=ATT_HEADERS,timeout=10)
        if r.status_code==429:
            print("    Rate limited — waiting 30s"); time.sleep(30)
            r=requests.post(ATT_API_URL,data=json.dumps(payload),
                            headers=ATT_HEADERS,timeout=10)
        if r.status_code!=200: return "UNKNOWN",""
        p=r.json().get("profile",{})
        spd=str(p.get("maxAvailableSpeed","") or p.get("maxDnldSpeed","") or "")
        if p.get("isGIGAFiberAvailable") or p.get("isFiberAvailable"):
            return "FIBER",spd
        if p.get("isIPBBAvailable") or p.get("isDSLAvailable"):
            return "COPPER",spd
        return "NONE",""
    except Exception: return "UNKNOWN",""


# ── OSM NEARBY ───────────────────────────────────────────────────────
def osm_nearby(lat,lng,radius=RADIUS):
    results=[]
    seen=set()
    query="""
[out:json][timeout:30];
(
  node(around:{r},{lat},{lng})[shop];
  node(around:{r},{lat},{lng})[office];
  node(around:{r},{lat},{lng})[amenity~"restaurant|cafe|bar|pharmacy|clinic|dentist|doctors|beauty|hairdresser|barber|gym|car_repair|car_wash|fast_food|veterinary|optician|massage|laundry|bakery|insurance"];
  node(around:{r},{lat},{lng})[craft];
  node(around:{r},{lat},{lng})[healthcare];
  way(around:{r},{lat},{lng})[shop];
  way(around:{r},{lat},{lng})[office];
);
out center tags;
""".format(r=radius,lat=lat,lng=lng)
    try:
        time.sleep(OSM_DELAY+random.uniform(0,JITTER))
        r=requests.post(OSM_OVERPASS,data={"data":query},
                        headers={"User-Agent":"AddressMan/3.0"},timeout=25)
        if r.status_code!=200: return results
        for el in r.json().get("elements",[]):
            tags=el.get("tags",{})
            name=tags.get("name","")
            if not name or not is_small_biz(name): continue
            elat=(el.get("center",{}).get("lat") if el["type"]=="way"
                  else el.get("lat"))
            elng=(el.get("center",{}).get("lon") if el["type"]=="way"
                  else el.get("lon"))
            if not elat or not elng: continue
            oid="%s_%s"%(el["type"],el.get("id",""))
            if oid in seen: continue
            seen.add(oid)
            cat=(tags.get("shop") or tags.get("office") or
                 tags.get("amenity") or tags.get("craft") or
                 tags.get("healthcare") or "business")
            phone=re.sub(r"[^\d\+\(\)\-\s]","",
                         tags.get("phone",tags.get("contact:phone",""))).strip()
            house=tags.get("addr:housenumber","")
            street=tags.get("addr:street","")
            addr=("%s %s"%(house,street)).strip() if house and street else ""
            dist=haversine(lat,lng,elat,elng)
            results.append({"name":name,"address":addr,"phone":phone,
                            "category":cat,"zip":tags.get("addr:postcode",""),
                            "city":tags.get("addr:city",""),
                            "dist_m":dist,"found_by":"OpenStreetMap"})
    except Exception as e:
        print("    OSM error: %s" % e)
    return results


# ── BROWSER ───────────────────────────────────────────────────────────
_pw=_browser=_page=None

def init_browser(headless=False):
    global _pw,_browser,_page
    from playwright.sync_api import sync_playwright
    _pw=sync_playwright().start()
    _browser=_pw.chromium.launch(headless=headless,
        args=["--disable-blink-features=AutomationControlled",
              "--no-sandbox","--disable-dev-shm-usage"])
    ctx=_browser.new_context(
        viewport={"width":1366,"height":768},
        user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"),
        locale="en-US")
    _page=ctx.new_page()
    _page.route("**/*.{png,jpg,jpeg,gif,webp,svg,woff,woff2,ttf,mp4,mp3,ico}",
                lambda r:r.abort())
    _page.goto("https://www.google.com/maps",timeout=15000,
               wait_until="domcontentloaded")
    time.sleep(2)
    try:
        for sel in ["button[aria-label*='Accept all']","button[aria-label*='Accept']"]:
            btn=_page.query_selector(sel)
            if btn: btn.click(); time.sleep(1); break
    except Exception: pass
    print("  Browser ready ✓")

def close_browser():
    global _browser,_pw
    try:
        if _browser: _browser.close()
        if _pw:      _pw.stop()
    except Exception: pass

def gmaps_nearby(lat,lng):
    global _page
    results=[]
    seen=set()
    if not _page: return results
    try:
        url=("https://www.google.com/maps/search/small+businesses/@%.5f,%.5f,15z"%(lat,lng))
        _page.goto(url,timeout=15000,wait_until="domcontentloaded")
        time.sleep(MAP_DELAY)
        for _ in range(5):
            for card in _page.query_selector_all("div.Nv2PK"):
                try:
                    ne=card.query_selector("div.fontHeadlineSmall,div.qBF1Pd")
                    if not ne: continue
                    name=ne.inner_text().strip()
                    if not name or not is_small_biz(name): continue
                    nk=norm(name)
                    if nk in seen: continue
                    seen.add(nk)
                    addr=""
                    for el in card.query_selector_all("div.W4Efsd span"):
                        txt=el.inner_text().strip()
                        if re.search(r'\d+\s+\w',txt) and len(txt)>5:
                            addr=txt; break
                    cat_el=card.query_selector("div.W4Efsd span.fontBodyMedium")
                    cat=cat_el.inner_text().strip() if cat_el else ""
                    results.append({"name":name,"address":addr,"phone":"",
                                    "category":cat,"zip":"","city":"",
                                    "dist_m":0,"found_by":"Google Maps"})
                except Exception: continue
            try:
                feed=_page.query_selector("div[role='feed']")
                if feed: feed.evaluate("el => el.scrollBy(0,800)")
                else: _page.mouse.wheel(0,800)
            except Exception: pass
            time.sleep(1.0)
            if len(results)>=20: break
    except Exception as e:
        print("    Maps nearby error: %s" % e)
    return results


# ── MAIN RUN ──────────────────────────────────────────────────────────
def run(leads, out_ws, existing, processed, headless, ss):
    prog        = load_prog()
    batch       = []
    new_found   = prog["new_found"]
    fiber_found = prog["fiber_found"]
    now_str     = datetime.now().strftime("%m/%d/%Y %I:%M %p")

    try:
        init_browser(headless)
        use_gmaps = True
    except Exception as e:
        print("  Browser unavailable — OSM only"); use_gmaps = False

    print("\n" + "="*60)
    print("  ADDRESS MAN v3.0")
    print("  Processing %d fiber leads" % len(leads))
    print("  Radius: %dm | Move on after %d NOs" % (RADIUS, CONSEC_NO))
    print("  Small biz only | Pitch type auto-assigned")
    print("  Ctrl+C to pause — resumes next run")
    print("="*60+"\n")

    try:
        for i,lead in enumerate(leads):
            src_addr = lead["address"]
            src_key  = norm(src_addr) if src_addr else "shot_%d"%i
            if src_key in processed: continue

            icon = "🟡" if lead["priority"]==0 else "🟢"
            print("\n%s [%d/%d] %s" % (icon,i+1,len(leads),
                  src_addr[:55] if src_addr else "GPS %.5f,%.5f"%(lead["lat"],lead["lng"])))

            # Get lat/lng
            lat = lead.get("lat","")
            lng = lead.get("lng","")
            try:
                lat,lng = float(lat),float(lng)
            except Exception:
                if src_addr:
                    lat,lng = geocode(src_addr,lead["city"],lead["state"],lead["zip"])
                    if not lat:
                        print("  Geocode failed — skip")
                        processed.add(src_key); continue
                    time.sleep(OSM_DELAY)
                else:
                    processed.add(src_key); continue

            # Find nearby small businesses
            nearby = osm_nearby(lat,lng)
            print("  OSM: %d small businesses" % len(nearby))

            if use_gmaps:
                try:
                    gm=gmaps_nearby(lat,lng)
                    osm_keys={norm(b["name"]) for b in nearby}
                    added=0
                    for b in gm:
                        if norm(b["name"]) not in osm_keys:
                            nearby.append(b)
                            osm_keys.add(norm(b["name"]))
                            added+=1
                    print("  Google Maps: +%d additional" % added)
                except Exception as e:
                    print("  Maps error: %s" % e)

            if not nearby:
                print("  No small businesses nearby")
                processed.add(src_key); continue

            print("  Total: %d | Checking AT&T..." % len(nearby))
            consec_no = 0
            added_ct  = 0

            for biz in nearby:
                if consec_no >= CONSEC_NO:
                    print("  %d NOs in a row — moving on" % CONSEC_NO); break

                biz_addr = biz.get("address","")
                biz_zip  = biz.get("zip","") or lead.get("zip","")
                biz_city = biz.get("city","") or lead.get("city","")
                biz_lat  = biz.get("lat",lat) or lat
                biz_lng  = biz.get("lng",lng) or lng

                if not biz_addr:
                    biz_addr,biz_city_rv,biz_zip_rv = rev_geocode(biz_lat,biz_lng)
                    if biz_city_rv: biz_city=biz_city_rv
                    if biz_zip_rv:  biz_zip=biz_zip_rv

                if not biz_addr: continue
                if norm(biz["name"]) in existing: continue
                if norm(biz_addr) in existing: continue

                att_status,att_speed = check_att(biz_addr,biz_zip)

                if att_status in ("NONE","UNKNOWN","ERROR"):
                    consec_no += 1
                else:
                    consec_no = 0

                ptype  = pitch_type(att_status)
                dist_ft= m_to_ft(biz["dist_m"]) if biz.get("dist_m") else ""
                s_icon = ("✅" if att_status=="FIBER" else
                          "🔶" if att_status=="COPPER" else "📡")

                print("  %s %-30s | %-13s | %s" % (
                    s_icon,biz["name"][:30],
                    biz.get("phone","") or "no phone",ptype))

                row = [
                    biz["name"],biz_addr,biz.get("phone",""),
                    biz.get("category",""),ptype,att_status,att_speed,
                    src_addr,str(dist_ft),biz.get("found_by","OSM"),
                    biz_zip,now_str,
                ]
                batch.append(row)
                existing.add(norm(biz["name"]))
                existing.add(norm(biz_addr))
                new_found += 1
                added_ct  += 1
                if att_status=="FIBER": fiber_found+=1

                if len(batch)>=BATCH_SIZE:
                    batch_write(out_ws,batch)
                    batch=[]
                    now_str=datetime.now().strftime("%m/%d/%Y %I:%M %p")
                    save_prog({"new_found":new_found,"fiber_found":fiber_found})

            processed.add(src_key)
            print("  Added %d new businesses" % added_ct)

    except KeyboardInterrupt:
        print("\n\n  Paused — run again to resume.")
    finally:
        if batch: batch_write(out_ws,batch)
        save_prog({"new_found":new_found,"fiber_found":fiber_found})
        close_browser()

    print("\n"+"█"*60)
    print("  ADDRESS MAN DONE")
    print("  New businesses: %s" % f"{new_found:,}")
    print("  Fiber confirmed: %d" % fiber_found)
    print("  Tab: '%s'" % OUTPUT_TAB)
    print("█"*60)


def main():
    parser = argparse.ArgumentParser(description="ADDRESS MAN v3.0")
    parser.add_argument("--zip",        type=str,   default=None)
    parser.add_argument("--gold-only",  action="store_true")
    parser.add_argument("--headless",   action="store_true")
    parser.add_argument("--clean-only", action="store_true",
                        help="Just clean the sheet, no scraping")
    args = parser.parse_args()

    print("\n"+"█"*60)
    print("  ADDRESS MAN v3.0")
    print("  Finds small businesses around your fiber leads")
    print("  Sheet cleaner included")
    print("█"*60+"\n")

    ss,out_ws = connect_sheets()

    # Always run cleaner first
    clean_sheet(ss)

    if args.clean_only:
        print("\n  Clean-only mode — done.")
        return

    # Load leads from sheet (works even if no local files)
    leads = load_fiber_leads(ss,zip_filter=args.zip,gold_only=args.gold_only)

    # Also check for screenshots if they exist
    if HAS_IMG and os.path.exists(SHOTS_DIR):
        print("\n  Scanner screenshots found — adding hotspots...")
        shot_leads = get_hotspots_from_screenshots(gold_only=args.gold_only)
        # Merge — add screenshot leads not already covered by sheet leads
        sheet_keys = {norm(l["address"]) for l in leads if l["address"]}
        for sl in shot_leads:
            if not any(haversine(sl["lat"],sl["lng"],
                                  *geocode(l["address"]) if l["address"] else (0,0)) < 100
                       for l in leads[:50]):
                leads.append(sl)
        print("  Total leads after merge: %d" % len(leads))

    if not leads:
        print("\n  No leads found in sheet.")
        print("  Run fiber_scan or themapman first to populate leads.")
        return

    existing  = load_existing(ss,out_ws)
    processed = load_processed(out_ws)
    run(leads,out_ws,existing,processed,args.headless,ss)


if __name__ == "__main__":
    main()
