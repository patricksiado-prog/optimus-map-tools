#!/usr/bin/env python3
"""
THE MAP MAN — Hunter sheet enricher v10.23.1
"""

VERSION = "10.23.3"
SHEET_ID  = "1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA"
DEFAULT_TAB_PREFIX = "Hunter"
GH_REPO   = "patricksiado-prog/optimus-map-tools"
GH_FILE   = "themapman.py"
GH_BRANCH = "main"

PHONE_SOURCE_FOUND = "Google Maps"
PHONE_SOURCE_EMPTY = "Google Maps (no biz)"
PLACES_API_KEY = "AIzaSyA9PJQJmf1LGFN3lATv8-se3tsIy6kCG9g"

import os, sys, re, time, json, argparse, base64
from datetime import datetime
from pathlib import Path
import urllib.request
import requests

TOKEN_PATHS = [
    Path("/storage/emulated/0/Download/github_token.txt"),
    Path("C:/Users/patri/Downloads/github_token.txt"),
    Path.home() / "Downloads" / "github_token.txt",
    Path.home() / "optimus" / "github_token.txt",
    Path.cwd() / "github_token.txt",
]

def _read_token():
    env = os.environ.get("GITHUB_TOKEN", "").strip()
    if env: return env
    for p in TOKEN_PATHS:
        try:
            if p.exists():
                t = p.read_text(errors="replace").strip()
                if t: return t
        except Exception:
            pass
    return ""

def check_update():
    import os
    try:
        url = ("https://raw.githubusercontent.com/%s/%s/%s"
               % (GH_REPO, GH_BRANCH, GH_FILE))
        req = urllib.request.Request(url, headers={"User-Agent": "themapman-update"})
        with urllib.request.urlopen(req, timeout=10) as r:
            latest = r.read().decode("utf-8", errors="replace")
        m = re.search(r"VERSION\s*=\s*[\"']([\.\d]+)[\"']", latest)
        new_ver = m.group(1) if m else None
        if not new_ver or new_ver == VERSION:
            print(f"  Up to date (v{VERSION})")
            return
        print(f"  Updating to v{new_ver}...")
        with open(os.path.abspath(__file__), "w", encoding="utf-8") as f:
            f.write(latest)
        print("  Updated! Restarting...")
        import subprocess
        subprocess.Popen([sys.executable, os.path.abspath(__file__)] + sys.argv[1:])
        sys.exit(0)
    except Exception as e:
        print(f"  Update check failed: {e}")

if "--no-update" not in sys.argv:
    check_update()

import gspread
try:
    from drive_commander import check_command, notify_make
    _COMMANDER = True
except ImportError:
    _COMMANDER = False
    def check_command(): return ('IDLE', '')
    def notify_make(s): pass
from google.oauth2.service_account import Credentials
from playwright.sync_api import sync_playwright

CREDS_FILE = next((p for p in [
    r"C:\Users\patri\Desktop\google_creds.json",
    "/storage/emulated/0/Download/google_creds.json",
    os.path.join(os.path.expanduser("~"), "Desktop", "google_creds.json"),
    "google_creds.json",
] if os.path.exists(p)), "google_creds.json")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]

ELIGIBLE_KEYWORDS = ("green", "fiber", "upgrade", "eligible", "gold")
PAGE_TIMEOUT = 30000
SETTLE_DELAY = 3.5
RATE_DELAY   = 1.0


def now_str():
    return datetime.now().strftime("%m/%d/%Y %I:%M %p")

def col_letter(n):
    out = ""
    while n:
        n, rem = divmod(n - 1, 26)
        out = chr(65 + rem) + out
    return out

def _is_bad_phone_number(d):
    if len(d) != 10: return True
    ac = d[:3]
    if ac[0] in ('0', '1'): return True
    _GARBAGE = {'000','111','123','456','654','789','900','911','999','555'}
    if ac in _GARBAGE: return True
    ex = d[3:6]
    if ex in ('000','100','111','555'): return True
    if d[6:] in ('0000','1111'): return True
    return False

def fmt_phone(s):
    d = re.sub(r"\D", "", str(s or ""))
    if len(d) == 11 and d.startswith("1"): d = d[1:]
    return f"({d[:3]}) {d[3:6]}-{d[6:]}" if len(d) == 10 and not _is_bad_phone_number(d) else ""

def is_blank(v):
    return v is None or str(v).strip() == ""

def is_eligible(status):
    s = (status or "").lower()
    return any(k in s for k in ELIGIBLE_KEYWORDS)

COORD_RE = re.compile(r"^-?\d+\.\d+\s*,\s*-?\d+\.\d+$")

def is_coord_only(text):
    return bool(COORD_RE.match((text or "").strip()))

def looks_like_address(text):
    if not text: return False
    t = str(text).strip()
    if is_coord_only(t): return False
    if not re.search(r"\b\d{1,6}\b", t): return False
    sigs = (" st", " street", " rd", " road", " ave", " avenue",
            " dr", " drive", " ln", " lane", " blvd", " boulevard",
            " pkwy", " parkway", " way", " ct", " court", " cir",
            " circle", " hwy", " highway", " fwy", " freeway",
            " loop", " trail", " trl", " place", " pl", " plaza",
            " ter", " terrace", " row", " path", " sq", " square")
    return any(sig in (" " + t.lower()) for sig in sigs)

def find_col(headers, *cands):
    low = [h.strip().lower() for h in headers]
    for c in cands:
        if c.lower() in low:
            return low.index(c.lower()) + 1
    return None

def ensure_columns(ws, headers, needed):
    low = [h.strip().lower() for h in headers]
    new_cols = [c for c in needed if c.lower() not in low]
    if not new_cols:
        return headers
    new_headers = list(headers) + new_cols
    try:
        ws.resize(rows=max(ws.row_count, 5000), cols=max(len(new_headers), 25))
    except Exception:
        pass
    last = col_letter(len(new_headers))
    ws.update(range_name=f"A1:{last}1", values=[new_headers])
    print(f"    Added columns: {new_cols}")
    return new_headers

ABBREV_MAP = {
    "street": "st", "road": "rd", "avenue": "ave", "drive": "dr",
    "lane": "ln", "boulevard": "blvd", "parkway": "pkwy",
    "court": "ct", "circle": "cir", "highway": "hwy", "freeway": "fwy",
    "trail": "trl", "place": "pl", "terrace": "ter", "square": "sq",
    "north": "n", "south": "s", "east": "e", "west": "w",
    "northeast": "ne", "northwest": "nw", "southeast": "se", "southwest": "sw",
    "suite": "ste", "apartment": "apt", "building": "bldg",
}

def normalize_address(addr):
    if not addr: return ""
    s = str(addr).lower().strip()
    s = re.sub(r"[,\.]", " ", s)
    s = re.sub(r"\s+", " ", s)
    tokens = s.split()
    out = []
    for t in tokens:
        out.append(ABBREV_MAP.get(t, t))
    return " ".join(out).strip()

_pw = _browser = _page = None

def init_browser(headless=True):
    global _pw, _browser, _page
    _pw = sync_playwright().start()
    _browser = _pw.chromium.launch(
        headless=headless,
        args=["--disable-blink-features=AutomationControlled",
              "--no-sandbox", "--disable-dev-shm-usage"])
    ctx = _browser.new_context(
        viewport={"width": 1366, "height": 768},
        user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"),
        locale="en-US")
    _page = ctx.new_page()
    print("  Browser ready")

def close_browser():
    global _browser, _pw
    try:
        if _browser: _browser.close()
        if _pw: _pw.stop()
    except Exception:
        pass

PANEL_NAME_REJECT = {"results", "sponsored", "directions", "search results",
                     "places", "you", "your places", "saved", "timeline"}

def safe_text(el):
    try: return el.inner_text().strip()
    except Exception: return ""

def panel_name():
    try: _page.wait_for_selector("h1.DUwDvf", timeout=2500)
    except Exception: pass
    for sel in ("h1.DUwDvf", "h1.fontHeadlineLarge", "h1"):
        try:
            el = _page.query_selector(sel)
            if el:
                t = safe_text(el)
                if t and t.lower().strip() not in PANEL_NAME_REJECT:
                    return t
        except Exception:
            pass
    return ""

def panel_phone():
    selectors = ("a[href^='tel:']",
                 "button[aria-label^='Phone:']",
                 "button[aria-label*='Phone:']",
                 "button[data-item-id='phone']")
    for sel in selectors:
        try:
            for el in _page.query_selector_all(sel):
                lbl = el.get_attribute("aria-label") or ""
                href = el.get_attribute("href") or ""
                txt = safe_text(el)
                m = re.search(r"[\(]?\d{3}[\)]?[\s\-\.]?\d{3}[\s\-\.]?\d{4}",
                              lbl + " " + href + " " + txt)
                if m:
                    p = fmt_phone(m.group(0))
                    if p: return p
        except Exception:
            pass
    return ""

def panel_address():
    selectors = ("button[data-item-id='address']",
                 "button[aria-label^='Address:']",
                 "button[aria-label*='Address:']")
    for sel in selectors:
        try:
            for el in _page.query_selector_all(sel):
                lbl = el.get_attribute("aria-label") or ""
                txt = safe_text(el)
                val = (lbl + " " + txt).replace("Address:", "").strip()
                val = re.sub(r"\s+", " ", val)
                if re.search(r"\b\d{1,6}\b", val):
                    return val
        except Exception:
            pass
    return ""

_last_zip = {"val": None}


def _places_api_fallback(address, zipc=""):
    """v10.23.3: Google Places fallback when browser Maps finds no phone."""
    try:
        q = str(address or "").strip()
        if not q:
            return {"name": "", "phone": "", "address": ""}
        if zipc and re.match(r"^\d{5}$", str(zipc).strip()):
            q += " " + str(zipc).strip()

        r = requests.get(
            "https://maps.googleapis.com/maps/api/place/findplacefromtext/json",
            params={
                "input": q,
                "inputtype": "textquery",
                "fields": "place_id,name,formatted_address,types,business_status",
                "key": PLACES_API_KEY,
            },
            timeout=12,
        )
        d = r.json()
        if d.get("status") != "OK" or not d.get("candidates"):
            return {"name": "", "phone": "", "address": ""}

        place = d["candidates"][0]
        pid = place.get("place_id", "")
        name = (place.get("name") or "").strip()
        addr = (place.get("formatted_address") or "").strip()

        if pid:
            r2 = requests.get(
                "https://maps.googleapis.com/maps/api/place/details/json",
                params={
                    "place_id": pid,
                    "fields": "formatted_phone_number,name,formatted_address,business_status",
                    "key": PLACES_API_KEY,
                },
                timeout=12,
            )
            d2 = r2.json()
            if d2.get("status") == "OK":
                res = d2.get("result") or {}
                phone = fmt_phone(res.get("formatted_phone_number") or "")
                rn = (res.get("name") or name or "").strip()
                ra = (res.get("formatted_address") or addr or "").strip()
                return {"name": rn, "phone": phone, "address": ra}

        return {"name": name, "phone": "", "address": addr}
    except Exception as e:
        print(f"      places fallback err: {str(e)[:80]}")
        return {"name": "", "phone": "", "address": ""}


def maps_lookup_raw(address, zipc=""):
    if not address or not looks_like_address(address):
        return None
    try:
        q = address.strip()
        if zipc and re.match(r"^\d{5}$", str(zipc).strip()):
            q += " " + str(zipc).strip()
        same_zip = (zipc and zipc == _last_zip["val"])
        smart_timeout = 2500 if same_zip else 5000
        _last_zip["val"] = zipc or _last_zip["val"]
        reused = False
        try:
            if "google.com/maps" in _page.url:
                box = _page.query_selector("input#searchboxinput")
                if box:
                    old_url = _page.url
                    box.click()
                    _page.keyboard.press("Control+A")
                    _page.keyboard.press("Backspace")
                    box.type(q, delay=20)
                    box.press("Enter")
                    try:
                        _page.wait_for_load_state("networkidle", timeout=1500)
                    except Exception:
                        pass
                    if _page.url == old_url:
                        reused = False
                    else:
                        reused = True
        except Exception:
            reused = False
        if not reused:
            url = "https://www.google.com/maps/search/" + q.replace(" ", "+")
            _page.goto(url, timeout=PAGE_TIMEOUT, wait_until="domcontentloaded")
            try:
                _page.wait_for_load_state("networkidle", timeout=1500)
            except Exception:
                pass
        try:
            _page.wait_for_selector(
                "h1.DUwDvf, a[href^='tel:'], button[aria-label^='Phone:'], div[role='article']",
                timeout=smart_timeout)
        except Exception:
            pass
        time.sleep(0.35)
        if "/place/" not in _page.url:
            clicked = False
            for sel in ("a.hfpxzc", "div.Nv2PKd a", "div[role='article'] a"):
                try:
                    el = _page.query_selector(sel)
                    if el:
                        el.click()
                        clicked = True
                        break
                except Exception:
                    pass
            if clicked:
                try:
                    _page.wait_for_selector("h1.DUwDvf", timeout=3000)
                except Exception:
                    pass
                time.sleep(0.25)
        out = {"name": panel_name(), "phone": panel_phone(), "address": panel_address()}
        if not out.get("phone"):
            fb = _places_api_fallback(address, zipc)
            if fb.get("phone"):
                print(f"      + api phone {fb.get('phone')}")
                out["phone"] = fb.get("phone", "")
                if fb.get("name"):
                    out["name"] = fb.get("name", out.get("name", ""))
                if fb.get("address"):
                    out["address"] = fb.get("address", out.get("address", ""))
        return out
    except Exception as e:
        print(f"      lookup err: {e}")
        fb = _places_api_fallback(address, zipc)
        return fb if (fb.get("phone") or fb.get("name")) else None

class AddressCache:
    def __init__(self):
        self._d = {}
        self._hits = 0
        self._misses = 0
        self._added = 0

    def get(self, addr):
        k = normalize_address(addr)
        if k in self._d:
            self._hits += 1
            return self._d[k]
        self._misses += 1
        return None

    def put(self, addr, result_dict):
        if not addr: return
        k = normalize_address(addr)
        if k and k not in self._d:
            self._d[k] = result_dict
            self._added += 1

    def stats(self):
        return f"cache: {len(self._d)} entries, {self._hits} hits, {self._misses} misses"

    def __len__(self):
        return len(self._d)

def build_cache_from_sheet(ss, tab_names):
    cache = AddressCache()
    print(f"\n  Building cache from {len(tab_names)} tab(s)...")
    for tab_name in tab_names:
        try:
            ws = ss.worksheet(tab_name)
        except gspread.WorksheetNotFound:
            continue
        try:
            data = ws.get_all_values()
        except Exception as e:
            continue
        if len(data) < 2: continue
        headers = data[0]
        c_addr = find_col(headers, "Address", "Address 1", "Street")
        c_phone = find_col(headers, "Phone", "Phone Number")
        c_biz = find_col(headers, "Business Name", "Name", "Business")
        c_baddr = find_col(headers, "Business Address", "Verified Address", "Confirmed Address")
        c_src = find_col(headers, "Phone Source")
        if not c_addr or not c_src: continue
        loaded = 0
        for row in data[1:]:
            def cell(c):
                return row[c-1].strip() if c and c-1 < len(row) else ""
            addr = cell(c_addr)
            src = cell(c_src)
            if not addr or src != PHONE_SOURCE_FOUND: continue
            cache.put(addr, {
                "name":    cell(c_biz)   if c_biz   else "",
                "phone":   cell(c_phone) if c_phone else "",
                "address": cell(c_baddr) if c_baddr else "",
                "src":     src,
            })
            loaded += 1
        if loaded:
            print(f"    {tab_name}: loaded {loaded} cached rows")
    print(f"  Cache built: {len(cache)} unique addresses\n")
    return cache

def _is_address_echo(name, input_addr):
    if not name or not input_addr:
        return False
    n = normalize_address(name)
    a = normalize_address(input_addr)
    if not n or not a:
        return False
    if n == a:
        return True
    if n in a or a in n:
        longer = n if len(n) > len(a) else a
        shorter = a if longer is n else n
        extra = longer.replace(shorter, "", 1).strip()
        extra_tokens = extra.split()
        if not extra_tokens:
            return True
        if all(re.match(r"^[a-z]+$|^\d{5}$|^[a-z]{2}$", t) for t in extra_tokens):
            return True
    return False

def sanitize_result(result, input_addr):
    if not result:
        return {"name": "", "phone": "", "address": "", "src": PHONE_SOURCE_EMPTY}
    name  = (result.get("name") or "").strip()
    phone = (result.get("phone") or "").strip()
    addr  = (result.get("address") or "").strip()
    if name and _is_address_echo(name, input_addr):
        name = ""
    if name:
        _n = name.strip().rstrip('.,').lower()
        _road_sigs = (' dr',' ave',' blvd',' st',' rd',' ln',
                      ' way',' pkwy',' hwy',' fwy',' loop')
        if any(_n.endswith(s) for s in _road_sigs):
            name = ''
        elif re.match(r'^[a-z]{2}\s+\d{5}$', _n):
            name = ''
        elif re.match(r'^[a-z\s]+,\s*[a-z]{2}\s+\d{5}$', _n):
            name = ''
    if not (name or phone):
        return {"name": "", "phone": "", "address": "", "src": PHONE_SOURCE_EMPTY}
    return {"name": name, "phone": phone, "address": addr, "src": PHONE_SOURCE_FOUND}

def maps_lookup_cached(cache, address, zipc=""):
    cached = cache.get(address)
    if cached is not None:
        return cached, True
    raw = maps_lookup_raw(address, zipc)
    if not raw or (not raw.get("name") and not raw.get("phone")):
        time.sleep(0.5)
        raw2 = maps_lookup_raw(address, zipc)
        if raw2 and (raw2.get("name") or raw2.get("phone")):
            raw = raw2
    result = sanitize_result(raw, address)
    if result.get("src") == PHONE_SOURCE_FOUND:
        cache.put(address, result)
    return result, False

TAB_PRIORITY_ORDER = [
    "Hunter Commercial",
    "Hunter Green Commercial",
    "Hunter Leads",
    "Hunter Residential",
    "Hunter Green Residential",
]

def discover_tabs(ss, prefix):
    pl = prefix.strip().lower()
    return [w.title for w in ss.worksheets()
            if w.title.lower().startswith(pl)]

def order_tabs(tabs):
    priority = {n.lower(): i for i, n in enumerate(TAB_PRIORITY_ORDER)}
    def key(t):
        return (priority.get(t.lower(), 999), t.lower())
    return sorted(tabs, key=key)

def parse_instance(s):
    if not s: return (None, None)
    m = re.match(r"^\s*(\d+)\s*of\s*(\d+)\s*$", s.lower())
    if not m: return (None, None)
    n, total = int(m.group(1)), int(m.group(2))
    if n < 1 or total < 1 or n > total: return (None, None)
    return (n, total)

_ROAD_SFX_201 = {
    'st','street','rd','road','ave','avenue','dr','drive',
    'ln','lane','blvd','boulevard','pkwy','parkway',
    'ct','court','cir','circle','hwy','highway',
    'pl','place','ter','terrace','trl','trail',
    'way','loop','sq','square','row','path',
}
_ABBREV_201 = {
    'street':'st','road':'rd','avenue':'ave','drive':'dr',
    'lane':'ln','boulevard':'blvd','parkway':'pkwy',
    'court':'ct','circle':'cir','highway':'hwy',
    'freeway':'fwy','place':'pl','terrace':'ter',
    'trail':'trl','north':'n','south':'s','east':'e','west':'w',
    'southwest':'sw','southeast':'se','northwest':'nw','northeast':'ne',
}

def _addr_norm_201(s):
    if not s: return ''
    s = re.sub(r'[^a-z0-9\s]', ' ', str(s).lower())
    s = re.sub(r'\s+', ' ', s).strip()
    return ' '.join(_ABBREV_201.get(t, t) for t in s.split())

def _is_echo_biz(biz, addr):
    if not biz: return False
    n = re.sub(r'[^a-z\s]', ' ', biz.lower()).strip()
    toks = n.split()
    if toks and _ABBREV_201.get(toks[-1], toks[-1]) in _ROAD_SFX_201:
        return True
    if re.match(r'^[a-z]{2}\s+\d{5}$', n): return True
    if re.match(r'^[a-z\s]+,\s*[a-z]{2}\s+\d{5}$', n): return True
    if not addr: return False
    nb = _addr_norm_201(biz); na = _addr_norm_201(addr)
    if not nb or not na: return False
    if nb == na: return True
    if nb in na or na in nb:
        longer = nb if len(nb) > len(na) else na
        shorter = na if longer is nb else nb
        extra = longer.replace(shorter, '', 1).strip().split()
        if not extra: return True
        if all(re.match(r'[a-z]+|\d{5}|[a-z]{2}', t) for t in extra):
            return True
    return False

def _street_key(addr, zipc=''):
    if not addr: return ''
    m = re.match(r'^\d+\s+(.*)', addr.strip())
    base = m.group(1) if m else addr
    key = re.sub(r'\s+', ' ', base.lower().strip())
    return key + '|' + str(zipc).strip() if zipc else key

def _group_by_street(candidates):
    groups = {}
    for c in candidates:
        k = _street_key(c.get('addr',''), c.get('zip',''))
        groups.setdefault(k or '__single__', []).append(c)
    return groups

def _scrape_street_list(street_name, city, state, zipc):
    global _page
    q = street_name
    if city:  q += ' ' + city
    if state: q += ' ' + state
    if zipc:  q += ' ' + zipc
    url = 'https://www.google.com/maps/search/' + q.strip().replace(' ','+')
    results = []
    try:
        _page.goto(url, timeout=8000, wait_until='domcontentloaded')
        try:
            _page.wait_for_selector("div[role='article'], h1.DUwDvf", timeout=2000)
        except Exception: pass
        time.sleep(0.5)
        if '/place/' in _page.url:
            n=panel_name(); p=panel_phone(); a=panel_address()
            if n or p: results.append({'name':n,'phone':p,'address':a})
            return results
        cards = []
        for sel in ("div[role='article']", 'div.Nv2PK'):
            try:
                cards = _page.query_selector_all(sel)
                if cards: break
            except Exception: pass
        for card in cards[:25]:
            try:
                txt = card.inner_text(); n = ''
                for ns in ('div.fontHeadlineSmall','div.qBF1Pd'):
                    try:
                        el = card.query_selector(ns)
                        if el: n=el.inner_text().strip().split('\n')[0]; break
                    except Exception: pass
                pm = re.search(r'[\(]?\d{3}[\)]?[\s\-\.]?\d{3}[\s\-\.]?\d{4}', txt)
                p = fmt_phone(pm.group(0)) if pm else ''
                a = ''
                for line in txt.split('\n'):
                    line = line.strip()
                    if looks_like_address(line): a = line; break
                if n and a: results.append({'name':n,'phone':p,'address':a})
            except Exception: pass
    except Exception as e:
        print(f'  [street-batch] err: {e}')
    return results

def _match_panel_to_cands(panel_results, street_cands):
    matched = {}
    for c in street_cands:
        m_row = re.search(r'\b(\d{2,6})\b', c.get('addr',''))
        if not m_row: continue
        row_num = int(m_row.group(1))
        row_street = re.sub(r'^\d+\s+', '', c.get('addr','').lower()).strip()
        for r in panel_results:
            m_res = re.search(r'\b(\d{2,6})\b', r.get('address',''))
            if not m_res: continue
            try:
                res_num = int(m_res.group(1))
                res_street = re.sub(r'^\d+\s+', '', r.get('address','').lower()).strip()
                if res_num == row_num and row_street[:20] in res_street and r.get('phone'):
                    matched[c['row']] = {'phone':r['phone'],
                        'name':r.get('name',''), 'biz_addr':r.get('address','')}
                    break
            except Exception: pass
    return matched

def process_street_batch(street_key, street_cands, ws,
                         c_phone, c_biz, c_baddr, c_psrc, c_chk, cache):
    if not street_cands: return set()
    s = street_cands[0]
    street_name = street_key.split('|')[0].strip()
    panel = _scrape_street_list(
        street_name, s.get('city',''), s.get('state','TX'), s.get('zip',''))
    if not panel: return set()
    matched = _match_panel_to_cands(panel, street_cands)
    if not matched: return set()
    handled = set()
    for row_idx, hit in matched.items():
        phone = fmt_phone(hit['phone'])
        if not phone: continue
        updates = []
        if c_phone: updates.append({'range':f'{col_letter(c_phone)}{row_idx}','values':[[phone]]})
        if c_biz and hit['name']: updates.append({'range':f'{col_letter(c_biz)}{row_idx}','values':[[hit['name']]]})
        if c_baddr and hit['biz_addr']: updates.append({'range':f'{col_letter(c_baddr)}{row_idx}','values':[[hit['biz_addr']]]})
        if c_psrc: updates.append({'range':f'{col_letter(c_psrc)}{row_idx}','values':[[PHONE_SOURCE_FOUND]]})
        if c_chk: updates.append({'range':f'{col_letter(c_chk)}{row_idx}','values':[[now_str()]]})
        if updates:
            for attempt in range(3):
                try:
                    fresh = [{'range':u['range'],'values':u['values']} for u in updates]
                    ws.batch_update(fresh, value_input_option='USER_ENTERED'); break
                except Exception as e: time.sleep(30*(attempt+1) if '429' in str(e) else 3)
        src_addr = next((c['addr'] for c in street_cands if c['row']==row_idx),'')
        if src_addr and cache:
            cache.put(src_addr,{'name':hit['name'],'phone':phone,
                                 'address':hit['biz_addr'],'src':PHONE_SOURCE_FOUND})
        print(f'    [batch] r{row_idx}: {src_addr[:35]} -> {phone}')
        handled.add(row_idx)
    return handled

import urllib.parse as _urlparse_v1021

def _block_key(addr, zip_code=''):
    m = re.match(r'^(\d+)\s+(.+)', addr.strip())
    if not m: return None
    block = (int(m.group(1)) // 100) * 100
    street = re.sub(r'\s+', ' ', m.group(2).strip().lower())
    return f'{block}_{street}_{zip_code}'

def _scrape_block_panel(street_name, city, state, zip_code, candidates_map):
    found = {}
    q = f'{street_name} {city} {state} {zip_code}'.strip()
    url = 'https://www.google.com/maps/search/' + _urlparse_v1021.quote_plus(q)
    try:
        try:
            _page.evaluate("() => window.stop()")
        except Exception:
            pass
        _page.goto(url, timeout=8000, wait_until='domcontentloaded')
        try:
            _page.wait_for_selector("div[role='article'], h1.DUwDvf", timeout=2000)
        except Exception: pass
        try: _page.keyboard.press('PageDown'); time.sleep(0.4)
        except Exception: pass
        time.sleep(0.5)
        cards = []
        for sel in ("div[role='article']", 'div.Nv2PK'):
            try:
                cards = _page.query_selector_all(sel)
                if cards: break
            except Exception: pass
        for card in cards[:20]:
            try:
                txt = card.inner_text()
                lines = [ln.strip() for ln in txt.split('\n') if ln.strip()]
                if not lines: continue
                biz_name = lines[0]
                phone = ''
                for ln in lines:
                    ph = re.search(r'\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]\d{4}', ln)
                    if ph:
                        phone = fmt_phone(ph.group()); break
                addr_line = ''
                for ln in lines:
                    if looks_like_address(ln): addr_line = ln; break
                if not phone: continue
                num_m = re.search(r'^(\d+)\b', addr_line.strip())
                if not num_m: continue
                num = num_m.group(1)
                nm_pat = r'^' + re.escape(num) + r'\b'
                for cand_addr in candidates_map:
                    if re.match(nm_pat, cand_addr.strip()) and phone:
                        found[cand_addr] = {'name': biz_name, 'phone': phone}
            except Exception: pass
    except Exception as _e:
        print(f'  [block-batch] err: {_e}')
    return found


STATUS_WEBHOOK = "https://hook.us2.make.com/28eg5dfsd8woey4a6y71napuq7tc9o6w"

def post_status(msg):
    try:
        import urllib.request as _ur, json as _json
        data = _json.dumps({"status": msg, "script": "mapman"}).encode()
        req = _ur.Request(STATUS_WEBHOOK, data=data, method="POST",
            headers={"Content-Type": "application/json", "User-Agent": "mapman/1.0"})
        _ur.urlopen(req, timeout=5)
    except Exception:
        pass

def enrich_tab(ss, tab_name, args, cache, partition):
    print(f"\n=== {tab_name} ===")
    try:
        ws = ss.worksheet(tab_name)
    except gspread.WorksheetNotFound:
        print("    NOT FOUND — skip"); return 0, 0

    data = ws.get_all_values()
    if len(data) < 2:
        print("    empty — skip"); return 0, 0
    headers = data[0]

    headers = ensure_columns(ws, headers,
        ["Phone", "Business Name", "Business Address", "Phone Source", "Checked At"])
    if len(headers) > len(data[0]):
        data = ws.get_all_values()
        headers = data[0]

    c_addr  = find_col(headers, "Address", "Address 1", "Street")
    c_phone = find_col(headers, "Phone", "Phone Number")
    c_biz   = find_col(headers, "Business Name", "Name", "Business")
    c_baddr = find_col(headers, "Business Address", "Verified Address", "Confirmed Address")
    c_psrc  = find_col(headers, "Phone Source")
    c_chk   = find_col(headers, "Checked At", "Phone Checked At")
    c_zip   = find_col(headers, "ZIP", "Zip", "Zip Code", "Postal Code")
    c_city  = find_col(headers, "City")
    c_state = find_col(headers, "State", "ST")
    c_ptype = find_col(headers, "Dot Type", "Type", "Property Type", "Lead Type", "Category")

    if not c_addr:
        print("    NO Address column — skip"); return 0, 0

    def cell(row, c):
        return row[c-1].strip() if c and c-1 < len(row) else ""

    city_filter = []
    if getattr(args, "city", ""):
        city_filter = [c.strip().lower() for c in args.city.split(",") if c.strip()]

    c_date = find_col(headers, "Date", "Last Scanned", "Date Found", "Checked At", "Phone Checked At")
    candidates = []
    skip_coord = skip_no_num = skip_already = skip_no_addr = skip_filter = skip_partition = skip_city = 0
    inst_n, inst_total = partition

    for r_idx, row in enumerate(data[1:], start=2):
        addr = cell(row, c_addr)
        if not addr: skip_no_addr += 1; continue
        if is_coord_only(addr): skip_coord += 1; continue
        if not looks_like_address(addr): skip_no_num += 1; continue
        if getattr(args, "commercial_only", False) and c_ptype:
            if "residential" in cell(row, c_ptype).lower():
                skip_filter += 1; continue
        if city_filter:
            row_city = cell(row, c_city).lower() if c_city else ""
            if not any(cf in row_city for cf in city_filter):
                skip_city += 1; continue
        if inst_n is not None:
            if (r_idx - 2) % inst_total != (inst_n - 1):
                skip_partition += 1; continue
        _src_val   = cell(row, c_psrc) if c_psrc else ""
        _has_phone = bool(c_phone and cell(row, c_phone))
        _biz_val      = cell(row, c_biz) if c_biz else ""
        _biz_is_echo  = bool(_biz_val) and _is_echo_biz(_biz_val, addr)
        _has_real_biz = _has_phone and not _biz_is_echo
        _fully_resolved = (_has_phone and _src_val == PHONE_SOURCE_FOUND)
        if _fully_resolved: skip_already += 1; continue
        candidates.append({
            "row":  r_idx, "addr": addr,
            "zip":  cell(row, c_zip)   if c_zip   else "",
            "date": cell(row, c_date)  if c_date  else "",
            "city": cell(row, c_city)  if c_city  else "",
            "state":cell(row, c_state) if c_state else "TX",
            "prop_type": ("commercial" if "commercial" in tab_name.lower()
                          else (cell(row, c_ptype) if c_ptype else "")),
        })

    print(f"    candidates: {len(candidates)}")
    print(f"    skipped: coord={skip_coord} no#={skip_no_num} already={skip_already} filtered={skip_filter}")

    if args.limit:
        candidates = candidates[:args.limit]
    if not candidates:
        return 0, 0

    def _flush_pending(ws, pending):
        if not pending: return
        for attempt in range(3):
            try:
                safe = json.loads(json.dumps(pending))
                ws.batch_update(safe, value_input_option='USER_ENTERED')
                return
            except Exception as e:
                msg = str(e)
                if '429' in msg or 'Quota' in msg:
                    wait = 30 * (attempt + 1)
                    print(f'      quota hit, waiting {wait}s ...')
                    time.sleep(wait)
                else:
                    print(f'      write err {attempt+1}: {e}')
                    time.sleep(3)

    _block_done = set()
    _block_map = {}
    for _bi, _bc in enumerate(candidates):
        _bk = _block_key(_bc['addr'], _bc.get('zip',''))
        if _bk: _block_map.setdefault(_bk, []).append((_bc, _bi))
    for _bk, _bgroup in _block_map.items():
        if len(_bgroup) < 2: continue
        _anchor = _bgroup[0][0]
        _cands_m = {x[0]['addr']: x[0] for x in _bgroup}
        _street_m = re.sub(r'^\d+\s+', '', _anchor['addr']).strip()
        _bresults = _scrape_block_panel(
            _street_m, _anchor.get('city',''),
            _anchor.get('state','TX'), _anchor.get('zip',''), _cands_m)
        for _ba, _bres in _bresults.items():
            for _bc2, _bi2 in _bgroup:
                if _bc2['addr'] != _ba: continue
                _block_done.add(_bi2)
                _upd = []
                _ph = fmt_phone(_bres.get('phone',''))
                if _ph and c_phone:
                    _upd.append({'range': f'{col_letter(c_phone)}{_bc2["row"]}', 'values': [[_ph]]})
                    _upd.append({'range': f'{col_letter(c_psrc)}{_bc2["row"]}', 'values': [[PHONE_SOURCE_FOUND]]})
                if _bres.get('name') and c_biz:
                    _upd.append({'range': f'{col_letter(c_biz)}{_bc2["row"]}', 'values': [[_bres['name']]]})
                if _upd:
                    _flush_pending(ws, _upd)

    _pending_updates = []
    _real_lookups = [0]
    _consec_empty = [0]

    _street_groups = _group_by_street(candidates)
    _batched_rows = set()
    for _sk, _sg in _street_groups.items():
        if len(_sg) < 4 or _sk == '__single__': continue
        _done = process_street_batch(_sk, _sg, ws, c_phone, c_biz, c_baddr, c_psrc, c_chk, cache)
        _batched_rows |= _done

    written_cells = 0
    written_rows = 0
    cache_hits_local = 0

    for i, c in enumerate(candidates, 1):
        if i-1 in _block_done: continue
        if c["row"] in _batched_rows: continue
        result, was_cached = maps_lookup_cached(cache, c["addr"], c["zip"])
        if was_cached:
            cache_hits_local += 1
        if not was_cached:
            if result.get("src") == PHONE_SOURCE_EMPTY:
                _consec_empty[0] += 1
                if _consec_empty[0] >= 5:
                    print(f"  5 empties — forcing browser reload")
                    try:
                        close_browser()
                        init_browser(headless=not args.visible)
                    except Exception: pass
                    _consec_empty[0] = 0
            else:
                _consec_empty[0] = 0

        print(f"    [{i}/{len(candidates)}] r{c['row']}: {c['addr'][:60]}")
        updates = []
        src_val = result.get("src") or PHONE_SOURCE_EMPTY
        if c_psrc:
            updates.append({"range": f"{col_letter(c_psrc)}{c['row']}", "values": [[src_val]]})
        if c_chk:
            updates.append({"range": f"{col_letter(c_chk)}{c['row']}", "values": [[now_str()]]})
        cur = data[c['row'] - 1] if c['row'] - 1 < len(data) else []
        def is_target_blank(col): return col and is_blank(cur[col-1] if col-1 < len(cur) else "")
        row_had_data = False
        if c_phone and result.get("phone") and is_target_blank(c_phone):
            updates.append({"range": f"{col_letter(c_phone)}{c['row']}", "values": [[result["phone"]]]})
            print(f"      + phone {result['phone']}"); row_had_data = True
        _cur_biz_val = cur[c_biz-1].strip() if c_biz and c_biz-1 < len(cur) else ""
        _biz_writable = is_target_blank(c_biz) or _is_echo_biz(_cur_biz_val, c["addr"])
        if c_biz and result.get("name") and _biz_writable:
            updates.append({"range": f"{col_letter(c_biz)}{c['row']}", "values": [[result["name"]]]})
            print(f"      + biz   {result['name']}"); row_had_data = True
        if c_baddr and result.get("address") and is_target_blank(c_baddr):
            updates.append({"range": f"{col_letter(c_baddr)}{c['row']}", "values": [[result["address"]]]})
            row_had_data = True
        if updates:
            _pending_updates.extend(updates)
            written_cells += len(updates)
            if row_had_data: written_rows += 1
        if len(_pending_updates) >= 10:
            _flush_pending(ws, _pending_updates)
            _pending_updates.clear()
        if i % 50 == 0:
            post_status(f"mapman [{i}/{len(candidates)}] {tab_name} | phones:{written_rows}")
        if not was_cached:
            time.sleep(RATE_DELAY)
            _real_lookups[0] += 1
            if _real_lookups[0] % 200 == 0:
                print('  200 lookups — restarting browser...')
                close_browser()
                init_browser(headless=not args.visible)

    _flush_pending(ws, _pending_updates)
    post_status(f"DONE {tab_name} cells:{written_cells} phones:{written_rows}")
    print(f"\n    {tab_name}: wrote {written_cells} cells, {written_rows} rows had real data")
    return written_cells, written_rows


def pick_city_interactive():
    METROS = [
        ("Houston metro       (Houston, Bellaire)",                      "Houston,Bellaire"),
        ("Austin metro        (Austin, Hornsby Bend)",                   "Austin,Hornsby Bend"),
        ("OKC metro           (OK City, Edmond, Midwest City, Choctaw)", "Oklahoma City,Edmond,Midwest City,Choctaw"),
        ("MS Gulf Coast       (Biloxi, Ocean Springs, Gulfport)",        "Biloxi,Ocean Springs,Gulfport"),
        ("ALL cities          (no filter, runs everything)",             ""),
    ]
    print("\n" + "=" * 60)
    print("  THE MAP MAN  -  pick where to enrich")
    print("=" * 60)
    for i, (label, _) in enumerate(METROS, 1):
        print(f"    {i}. {label}")
    print()
    if sys.platform == "win32":
        try:
            import msvcrt
            while msvcrt.kbhit(): msvcrt.getch()
        except Exception: pass
    failures = 0
    while True:
        try:
            choice = input("  Pick (1-5, or Enter for ALL): ").strip()
        except (EOFError, KeyboardInterrupt):
            return ""
        if choice == "": return ""
        if choice.isdigit() and 1 <= int(choice) <= len(METROS):
            return METROS[int(choice)-1][1]
        failures += 1
        if failures >= 3: return ""
        print("  Invalid pick. Try again.")


def main():
    global RATE_DELAY
    p = argparse.ArgumentParser(description=f"THE MAP MAN v{VERSION}")
    p.add_argument("--tab", help="single tab name")
    p.add_argument("--tab-prefix", default=DEFAULT_TAB_PREFIX)
    p.add_argument("--visible", action="store_true")
    p.add_argument("--fiber-only", action="store_true")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--instance", default="")
    p.add_argument("--city", default="")
    p.add_argument("--no-cache", action="store_true")
    p.add_argument("--no-update", action="store_true")
    p.add_argument("--no-pick", action="store_true")
    p.add_argument("--commercial-only", action="store_true")
    p.add_argument("--no-spawn", action="store_true")
    p.add_argument("--named-only", action="store_true")
    args = p.parse_args()

    if (not args.city and not args.tab and sys.stdin.isatty() and not args.no_pick):
        args.city = pick_city_interactive()

    if "--instance" not in sys.argv and not getattr(args, "no_spawn", False):
        import subprocess
        child = [sys.executable, os.path.abspath(__file__),
                 "--instance", "2of2", "--no-pick", "--no-spawn"]
        if args.city: child += ["--city", args.city]
        if args.no_cache: child.append("--no-cache")
        if getattr(args, "commercial_only", False): child.append("--commercial-only")
        kwargs = {}
        if os.name == "nt":
            kwargs["creationflags"] = subprocess.CREATE_NEW_CONSOLE
        try:
            subprocess.Popen(child, **kwargs)
            print("  Spawned instance 2of2")
        except Exception as e:
            print(f"  Could not spawn: {e}")
        args.instance = "1of2"

    inst_n, inst_total = parse_instance(args.instance)
    inst_label = f"{inst_n}of{inst_total}" if inst_n else "single"

    if inst_total and inst_total > 1:
        RATE_DELAY = float(max(1, inst_total))

    print("\n" + "#" * 60)
    print(f"  THE MAP MAN v{VERSION}")
    print(f"  Mode: ALL rows incl. residential")
    print(f"  Instance: {inst_label}  (rate delay {RATE_DELAY}s/row)")
    if args.city:
        print(f"  City filter: {args.city}")
    print("#" * 60)

    if not os.path.exists(CREDS_FILE):
        sys.exit(f"\nERROR: {CREDS_FILE} not found")

    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    ss = gspread.authorize(creds).open_by_key(SHEET_ID)

    if args.tab:
        tabs = [args.tab]
    else:
        tabs = order_tabs(discover_tabs(ss, args.tab_prefix))
        if not tabs:
            sys.exit(f"\nNo tabs found starting with '{args.tab_prefix}'")

    if args.no_cache:
        cache = AddressCache()
    else:
        cache = build_cache_from_sheet(ss, tabs)

    post_status(f"STARTED mapman v{VERSION} city:{getattr(args,'city','ALL')}")
    init_browser(headless=not args.visible)
    total_cells = total_rows = 0
    try:
        for tab in tabs:
            c, r = enrich_tab(ss, tab, args, cache, (inst_n, inst_total))
            total_cells += c
            total_rows  += r
    finally:
        close_browser()

    print("\n" + "#" * 60)
    print(f"  DONE. {total_cells} cells written, {total_rows} rows had real data.")
    print(f"  Final {cache.stats()}")
    print("#" * 60)


if __name__ == "__main__":
    main()
