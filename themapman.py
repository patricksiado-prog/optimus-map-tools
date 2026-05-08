#!/usr/bin/env python3
"""
THE MAP MAN — Hunter sheet enricher v10.7
=========================================
Enriches every tab named Hunter* with Phone + Business Name +
Business Address via Google Maps. Writes back IN PLACE.

NEW IN v10.7:
- Interactive city picker on startup. When themapman.py is run
  without --city or --tab AND stdin is a tty, shows a numbered
  metro menu (Houston / Austin / OKC / MS Gulf Coast / ALL).
  Skip with --no-pick or by passing --city/--tab explicitly.
- Tab priority order: Hunter Commercial first. (v10.6 briefly
  swapped Green Commercial first; v10.7 reverted that swap.)

CARRIED FROM v10.5:
- --city "Name1,Name2" flag for targeted metro enrichment
  (case-insensitive substring match against the City column).

CARRIED FROM v10.4:
- sanitize_result() rejects address-as-name pollution. When
  Maps returns input address itself as h1 (no real biz at the
  location), v10.4+ treats result as empty instead of writing
  the address into the Business Name column.
- _is_address_echo() handles abbreviation variants
  (Drive→dr, Avenue→ave) and city/state/zip suffix.

CARRIED FROM v10.3:
- TAB_PRIORITY_ORDER constant: Hunter Commercial first, then
  Green Commercial, Leads, Residential, Green Residential.

CARRIED FROM v10.2:
- Sheet-based cache pre-load (skips already-queried addresses
  cross-machine and cross-restart).
- In-memory cache during run.
- --instance N/M flag for parallel runs.
- RATE_DELAY auto-scales with instance count
  (single=1s, 2-way=2s, 4-way=4s).
- Address normalization for cache keys.
- Phone Source stamped on every queried row.

USAGE:
  python themapman.py                              # picker on tty
  python themapman.py --city "Oklahoma City"       # OKC only
  python themapman.py --city "Houston,Bellaire"    # Houston metro
  python themapman.py --city "Austin" --no-pick    # skip picker
  python themapman.py --tab "Hunter Leads"         # single tab
  python themapman.py --instance 1of2 --no-pick    # parallel partition
  python themapman.py --no-cache                   # skip cache pre-load
  python themapman.py --no-update                  # skip auto-update
  python themapman.py --limit 10                   # cap per tab (test)

OKC PARALLEL (2 instances):
  PC A: python themapman.py --city "Oklahoma City,Edmond,Midwest City,Choctaw" --instance 1of2 --no-pick
  PC B: python themapman.py --city "Oklahoma City,Edmond,Midwest City,Choctaw" --instance 2of2 --no-pick

REPO: patricksiado-prog/optimus-map-tools (public for read,
authenticated for push). Auto-update on launch fetches the raw
file via Contents API; works with or without a valid token for
read on a public repo, but the push scripts still require a
token with Contents:write scope.
"""

VERSION   = "10.8"
SHEET_ID  = "12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag"
DEFAULT_TAB_PREFIX = "Hunter"
GH_REPO   = "patricksiado-prog/optimus-map-tools"
GH_FILE   = "themapman.py"
GH_BRANCH = "main"

PHONE_SOURCE_FOUND = "Google Maps"
PHONE_SOURCE_EMPTY = "Google Maps (no biz)"

import os, sys, re, time, json, argparse, base64
from datetime import datetime
from pathlib import Path
import urllib.request


# ─── AUTO-UPDATE (token-aware, private repo) ─────────────────────────
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
    print("  Checking GitHub for updates...")
    tok = _read_token()
    if not tok:
        print("  No token — skipping update check.")
        return
    try:
        url = (f"https://api.github.com/repos/{GH_REPO}"
               f"/contents/{GH_FILE}?ref={GH_BRANCH}")
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"token {tok}")
        req.add_header("Accept", "application/vnd.github.v3+json")
        req.add_header("User-Agent", "themapman-update")
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
        latest = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
        m = re.search(r'^\s*VERSION\s*=\s*["\']([^"\']+)["\']',
                      latest, re.MULTILINE)
        new_ver = m.group(1) if m else None
        if not new_ver or new_ver == VERSION:
            print(f"  Up to date (v{VERSION})")
            return
        print(f"  Updating to v{new_ver}...")
        with open(os.path.abspath(__file__), "w", encoding="utf-8") as f:
            f.write(latest)
        print("  Updated! Restart required.")
        # On Windows, os.execv breaks stdin (cmd.exe and the new python
        # process fight over the console handle). Exit cleanly and let
        # the user re-run. On Linux/Mac, os.execv works fine.
        if sys.platform == "win32":
            print("  Re-run the same command to use v" + new_ver + ".")
            sys.exit(0)
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print(f"  Update check failed: {e}")

if "--no-update" not in sys.argv:
    check_update()


# ─── DEPS ────────────────────────────────────────────────────────────
import gspread
from google.oauth2.service_account import Credentials
from playwright.sync_api import sync_playwright

CREDS_FILE = "google_creds.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]

ELIGIBLE_KEYWORDS = ("green", "fiber", "upgrade", "eligible", "gold")
PAGE_TIMEOUT = 30000
SETTLE_DELAY = 2.5
RATE_DELAY   = 1.0


# ─── BASIC HELPERS ───────────────────────────────────────────────────
def now_str():
    return datetime.now().strftime("%m/%d/%Y %I:%M %p")

def col_letter(n):
    out = ""
    while n:
        n, rem = divmod(n - 1, 26)
        out = chr(65 + rem) + out
    return out

def fmt_phone(s):
    d = re.sub(r"\D", "", str(s or ""))
    if len(d) == 11 and d.startswith("1"): d = d[1:]
    return f"({d[:3]}) {d[3:6]}-{d[6:]}" if len(d) == 10 else ""

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
    if "(no" in t.lower() or "no #" in t.lower() or "no number" in t.lower():
        return False
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
        ws.resize(rows=max(ws.row_count, 5000),
                  cols=max(len(new_headers), 25))
    except Exception:
        pass
    last = col_letter(len(new_headers))
    ws.update(range_name=f"A1:{last}1", values=[new_headers])
    print(f"    Added columns: {new_cols}")
    return new_headers


# ─── ADDRESS NORMALIZATION (for cache keys) ──────────────────────────
ABBREV_MAP = {
    "street": "st", "road": "rd", "avenue": "ave", "drive": "dr",
    "lane": "ln", "boulevard": "blvd", "parkway": "pkwy",
    "court": "ct", "circle": "cir", "highway": "hwy", "freeway": "fwy",
    "trail": "trl", "place": "pl", "terrace": "ter", "square": "sq",
    "north": "n", "south": "s", "east": "e", "west": "w",
    "northeast": "ne", "northwest": "nw",
    "southeast": "se", "southwest": "sw",
    "suite": "ste", "apartment": "apt", "building": "bldg",
}

def normalize_address(addr):
    """Lowercase, collapse whitespace, expand to canonical abbreviations.
    '611 East Beach Drive' and '611 E Beach Dr' both → '611 e beach dr'."""
    if not addr: return ""
    s = str(addr).lower().strip()
    s = re.sub(r"[,\.]", " ", s)
    s = re.sub(r"\s+", " ", s)
    tokens = s.split()
    out = []
    for t in tokens:
        out.append(ABBREV_MAP.get(t, t))
    return " ".join(out).strip()


# ─── BROWSER ─────────────────────────────────────────────────────────
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
    print("  Browser ready ✓")

def close_browser():
    global _browser, _pw
    try:
        if _browser: _browser.close()
        if _pw: _pw.stop()
    except Exception:
        pass


# ─── GOOGLE MAPS PANEL SCRAPING ──────────────────────────────────────
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
    selectors = ("button[data-item-id='phone']",
                 "button[aria-label^='Phone:']",
                 "button[aria-label*='Phone:']",
                 "a[href^='tel:']")
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

def maps_lookup_raw(address, zipc=""):
    """Direct Maps query. Returns dict or None.
    Use maps_lookup() for cached version."""
    if not address or not looks_like_address(address):
        return None
    try:
        _page.evaluate("""() => {
            const h = document.querySelector('h1.DUwDvf');
            if (h) h.innerText = '';
        }""")
    except Exception:
        pass
    try:
        q = address.strip()
        if zipc and re.match(r"^\d{5}$", str(zipc).strip()):
            q += " " + str(zipc).strip()
        url = "https://www.google.com/maps/search/" + q.replace(" ", "+")
        _page.goto(url, timeout=PAGE_TIMEOUT, wait_until="domcontentloaded")
        time.sleep(SETTLE_DELAY)
        if "/place/" in _page.url:
            return {"name": panel_name(), "phone": panel_phone(),
                    "address": panel_address()}
        for sel in ("a.hfpxzc", "div.Nv2PKd a", "div[role='article'] a"):
            try:
                el = _page.query_selector(sel)
                if el:
                    el.click()
                    time.sleep(SETTLE_DELAY)
                    break
            except Exception:
                pass
        return {"name": panel_name(), "phone": panel_phone(),
                "address": panel_address()}
    except Exception as e:
        print(f"      lookup err: {e}")
        return None


# ─── ADDRESS CACHE (in-memory, populated from sheet on startup) ──────
class AddressCache:
    """{normalized_address: {"name", "phone", "address", "src"}}"""
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
    """Pre-load cache: walk all listed tabs, capture every row with
    Phone Source populated. That row was queried in a past run, so
    we know what Maps said about that address."""
    cache = AddressCache()
    print(f"\n  Building cross-run cache from {len(tab_names)} tab(s)...")
    for tab_name in tab_names:
        try:
            ws = ss.worksheet(tab_name)
        except gspread.WorksheetNotFound:
            continue
        try:
            data = ws.get_all_values()
        except Exception as e:
            print(f"    {tab_name}: read error {e}")
            continue
        if len(data) < 2: continue
        headers = data[0]
        c_addr = find_col(headers, "Address", "Address 1", "Street")
        c_phone = find_col(headers, "Phone", "Phone Number")
        c_biz = find_col(headers, "Business Name", "Name", "Business")
        c_baddr = find_col(headers, "Business Address",
                           "Verified Address", "Confirmed Address")
        c_src = find_col(headers, "Phone Source")
        if not c_addr or not c_src: continue
        loaded = 0
        for row in data[1:]:
            def cell(c):
                return row[c-1].strip() if c and c-1 < len(row) else ""
            addr = cell(c_addr)
            src = cell(c_src)
            if not addr or not src: continue
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
    """True if the returned name is just the input address echoed back
    (Maps returns h1 = address when no real business is at the location)."""
    if not name or not input_addr:
        return False
    n = normalize_address(name)
    a = normalize_address(input_addr)
    if not n or not a:
        return False
    # Exact match
    if n == a:
        return True
    # One contains the other and the other has no extra business words
    # E.g. name "9316 Dogwood Ave" vs input "9316 Dogwood Avenue Biloxi MS"
    if n in a or a in n:
        # Check the longer one doesn't have non-address words after the match
        longer = n if len(n) > len(a) else a
        shorter = a if longer is n else n
        extra = longer.replace(shorter, "", 1).strip()
        # If the only extra tokens look like city/state/zip, still an echo
        extra_tokens = extra.split()
        if not extra_tokens:
            return True
        if all(re.match(r"^[a-z]+$|^\d{5}$|^[a-z]{2}$", t) for t in extra_tokens):
            return True
    return False


def sanitize_result(result, input_addr):
    """Drop address-as-name pollution. If Maps returned the input
    address itself (or a near-echo) as the biz name, treat as no biz."""
    if not result:
        return {"name": "", "phone": "", "address": "", "src": PHONE_SOURCE_EMPTY}
    name  = (result.get("name") or "").strip()
    phone = (result.get("phone") or "").strip()
    addr  = (result.get("address") or "").strip()

    if name and _is_address_echo(name, input_addr):
        name = ""

    if not (name or phone):
        return {"name": "", "phone": "", "address": "", "src": PHONE_SOURCE_EMPTY}
    return {"name": name, "phone": phone, "address": addr,
            "src": PHONE_SOURCE_FOUND}


def maps_lookup_cached(cache, address, zipc=""):
    """Cache-aware lookup. Returns (result_dict, was_cached_bool)."""
    cached = cache.get(address)
    if cached is not None:
        return cached, True
    raw = maps_lookup_raw(address, zipc)
    result = sanitize_result(raw, address)
    cache.put(address, result)
    return result, False


# ─── TAB DISCOVERY ───────────────────────────────────────────────────
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
    """Sort discovered tabs by TAB_PRIORITY_ORDER. Tabs not in the
    priority list go to the end in alphabetical order."""
    priority = {n.lower(): i for i, n in enumerate(TAB_PRIORITY_ORDER)}
    def key(t):
        return (priority.get(t.lower(), 999), t.lower())
    return sorted(tabs, key=key)


# ─── PARTITION ───────────────────────────────────────────────────────
def parse_instance(s):
    """Parse '1of4' → (1, 4). Returns (None, None) if invalid."""
    if not s: return (None, None)
    m = re.match(r"^\s*(\d+)\s*of\s*(\d+)\s*$", s.lower())
    if not m: return (None, None)
    n, total = int(m.group(1)), int(m.group(2))
    if n < 1 or total < 1 or n > total: return (None, None)
    return (n, total)


# ─── ENRICH ONE TAB ──────────────────────────────────────────────────
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
    print(f"    headers: {headers}")

    headers = ensure_columns(ws, headers,
        ["Phone", "Business Name", "Business Address",
         "Phone Source", "Checked At"])
    if len(headers) > len(data[0]):
        data = ws.get_all_values()
        headers = data[0]

    c_addr  = find_col(headers, "Address", "Address 1", "Street")
    c_phone = find_col(headers, "Phone", "Phone Number")
    c_biz   = find_col(headers, "Business Name", "Name", "Business")
    c_baddr = find_col(headers, "Business Address",
                       "Verified Address", "Confirmed Address")
    c_psrc  = find_col(headers, "Phone Source")
    c_chk   = find_col(headers, "Checked At", "Phone Checked At")
    c_zip   = find_col(headers, "ZIP", "Zip", "Zip Code", "Postal Code")
    c_stat  = find_col(headers, "Type", "Fiber Status", "Status",
                       "Dot Type", "Property Type")
    c_city  = find_col(headers, "City")

    if not c_addr:
        print("    NO Address column — skip"); return 0, 0

    print(f"    cols: addr={c_addr} phone={c_phone} biz={c_biz} "
          f"biz_addr={c_baddr} src={c_psrc} chk={c_chk} zip={c_zip} "
          f"city={c_city}")

    def cell(row, c):
        return row[c-1].strip() if c and c-1 < len(row) else ""

    # Parse city filter from args (comma-separated, case-insensitive)
    city_filter = []
    if getattr(args, "city", ""):
        city_filter = [c.strip().lower() for c in args.city.split(",") if c.strip()]
    if city_filter and c_city is None:
        print(f"    --city set but tab has no City column — skip")
        return 0, 0

    candidates = []
    skip_coord = skip_no_num = skip_already = skip_no_addr = skip_filter = 0
    skip_partition = skip_city = 0
    inst_n, inst_total = partition

    for r_idx, row in enumerate(data[1:], start=2):
        addr = cell(row, c_addr)
        if not addr:
            skip_no_addr += 1; continue
        if is_coord_only(addr):
            skip_coord += 1; continue
        if not looks_like_address(addr):
            skip_no_num += 1; continue
        if args.fiber_only and c_stat and not is_eligible(cell(row, c_stat)):
            skip_filter += 1; continue
        # City filter
        if city_filter:
            row_city = cell(row, c_city).lower()
            if not any(cf in row_city for cf in city_filter):
                skip_city += 1; continue
        # Partition filter
        if inst_n is not None:
            if (r_idx - 2) % inst_total != (inst_n - 1):
                skip_partition += 1; continue
        # Already-queried check
        if c_psrc and cell(row, c_psrc):
            skip_already += 1; continue
        candidates.append({
            "row": r_idx, "addr": addr,
            "zip": cell(row, c_zip) if c_zip else "",
        })

    print(f"    candidates: {len(candidates)}  "
          f"(skipped: coord={skip_coord} no#={skip_no_num} "
          f"already={skip_already} filtered={skip_filter} "
          f"blank={skip_no_addr} other-instance={skip_partition} "
          f"other-city={skip_city})")

    if args.limit:
        candidates = candidates[:args.limit]
        print(f"    limited to {len(candidates)}")
    if not candidates:
        return 0, 0

    written_cells = 0
    written_rows  = 0
    cache_hits_local = 0
    for i, c in enumerate(candidates, 1):
        marker = ""
        before_hits = cache._hits
        result, was_cached = maps_lookup_cached(cache, c["addr"], c["zip"])
        if was_cached:
            cache_hits_local += 1
            marker = " (cached)"
        print(f"    [{i}/{len(candidates)}] r{c['row']}: {c['addr'][:60]}{marker}")

        updates = []
        row_had_data = False
        # Always stamp Phone Source + Checked At so this row gets cached
        src_val = result.get("src") or PHONE_SOURCE_EMPTY
        if c_psrc:
            updates.append({"range": f"{col_letter(c_psrc)}{c['row']}",
                            "values": [[src_val]]})
        if c_chk:
            updates.append({"range": f"{col_letter(c_chk)}{c['row']}",
                            "values": [[now_str()]]})
        # Write data fields if present and the target cell is currently blank
        cur = data[c['row'] - 1] if c['row'] - 1 < len(data) else []
        def is_target_blank(col): return col and is_blank(cur[col-1] if col-1 < len(cur) else "")

        if c_phone and result.get("phone") and is_target_blank(c_phone):
            updates.append({"range": f"{col_letter(c_phone)}{c['row']}",
                            "values": [[result["phone"]]]})
            print(f"      + phone {result['phone']}"); row_had_data = True
        if c_biz and result.get("name") and is_target_blank(c_biz):
            updates.append({"range": f"{col_letter(c_biz)}{c['row']}",
                            "values": [[result["name"]]]})
            print(f"      + biz   {result['name']}"); row_had_data = True
        if c_baddr and result.get("address") and is_target_blank(c_baddr):
            updates.append({"range": f"{col_letter(c_baddr)}{c['row']}",
                            "values": [[result["address"]]]})
            print(f"      + baddr {result['address']}"); row_had_data = True

        if updates:
            for attempt in range(3):
                try:
                    ws.batch_update(updates,
                                    value_input_option="USER_ENTERED")
                    written_cells += len(updates)
                    if row_had_data: written_rows += 1
                    break
                except Exception as e:
                    msg = str(e)
                    if "429" in msg or "Quota" in msg or "RESOURCE_EXHAUSTED" in msg:
                        wait = 30 * (attempt + 1)
                        print(f"      quota hit, waiting {wait}s ...")
                        time.sleep(wait)
                    else:
                        print(f"      write err {attempt+1}: {e}")
                        time.sleep(3)
        # Slow down only on real Maps lookups, not cache hits
        if not was_cached:
            time.sleep(RATE_DELAY)

    print(f"\n    {tab_name}: wrote {written_cells} cells, "
          f"{written_rows} rows had real data, "
          f"{cache_hits_local} cache hits (no Maps call)")
    return written_cells, written_rows


# ─── MAIN ────────────────────────────────────────────────────────────
def pick_city_interactive():
    """Show city options at startup. Return comma-separated city filter
    (empty string = no filter / all cities). Called only when no --city
    flag was passed and stdin is a tty.

    Defensive against broken stdin (Windows .py file-association
    launches share the console with cmd.exe; input() can return
    garbage). After 3 invalid picks or any EOF, defaults to ALL."""
    METROS = [
        ("Houston metro       (Houston, Bellaire)",                          "Houston,Bellaire"),
        ("Austin metro        (Austin, Hornsby Bend)",                       "Austin,Hornsby Bend"),
        ("OKC metro           (OK City, Edmond, Midwest City, Choctaw)",     "Oklahoma City,Edmond,Midwest City,Choctaw"),
        ("MS Gulf Coast       (Biloxi, Ocean Springs, Gulfport)",            "Biloxi,Ocean Springs,Gulfport"),
        ("ALL cities          (no filter, runs everything)",                 ""),
    ]
    print("\n" + "=" * 60)
    print("  THE MAP MAN  -  pick where to enrich")
    print("=" * 60)
    for i, (label, _) in enumerate(METROS, 1):
        print(f"    {i}. {label}")
    print()

    # Drain any pre-buffered junk on Windows (cmd.exe leftovers).
    if sys.platform == "win32":
        try:
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        except Exception:
            pass

    failures = 0
    while True:
        try:
            choice = input("  Pick (1-5, or Enter for ALL): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("  No input received - defaulting to ALL.")
            print("  TIP: launch via mapman.bat to avoid this.")
            return ""
        if choice == "":
            return ""
        if choice.isdigit() and 1 <= int(choice) <= len(METROS):
            return METROS[int(choice)-1][1]
        failures += 1
        if failures >= 3:
            print("  Too many invalid picks - defaulting to ALL.")
            print("  TIP: launch via mapman.bat for proper input handling.")
            return ""
        print("  Invalid pick. Try again.")


def main():
    p = argparse.ArgumentParser(description=f"THE MAP MAN v{VERSION}")
    p.add_argument("--tab", help="single tab name (overrides discovery)")
    p.add_argument("--tab-prefix", default=DEFAULT_TAB_PREFIX,
                   help=f"tab prefix to discover (default: {DEFAULT_TAB_PREFIX})")
    p.add_argument("--visible", action="store_true",
                   help="show Chromium window")
    p.add_argument("--fiber-only", action="store_true",
                   help="restrict to fiber-eligible rows")
    p.add_argument("--limit", type=int, default=0,
                   help="cap rows per tab (testing)")
    p.add_argument("--instance", default="",
                   help="parallel partition: 1of2, 2of4, etc.")
    p.add_argument("--city", default="",
                   help="filter to rows in these cities (comma-separated, case-insensitive)")
    p.add_argument("--no-cache", action="store_true",
                   help="skip startup cache pre-load")
    p.add_argument("--no-update", action="store_true",
                   help="skip GitHub auto-update")
    p.add_argument("--no-pick", action="store_true",
                   help="skip interactive city picker")
    args = p.parse_args()

    # Interactive city picker — runs only if no --city/--tab passed
    # AND we're attached to a terminal. Skip for headless/CI/script use.
    if (not args.city and not args.tab and sys.stdin.isatty()
            and not args.no_pick):
        args.city = pick_city_interactive()

    inst_n, inst_total = parse_instance(args.instance)
    inst_label = f"{inst_n}of{inst_total}" if inst_n else "single"

    # Auto-scale RATE_DELAY based on instance count to stay under
    # Sheets API write quota (60 batches/min/user).
    # single=1s, 2-way=2s, 4-way=4s, etc.
    global RATE_DELAY
    if inst_total and inst_total > 1:
        RATE_DELAY = float(max(1, inst_total))

    print("\n" + "#" * 60)
    print(f"  THE MAP MAN v{VERSION}")
    print(f"  Goal: Phone + Business Name + Business Address (in place)")
    print(f"  Mode: {'fiber-eligible only' if args.fiber_only else 'ALL rows incl. residential'}")
    print(f"  Instance: {inst_label}  (rate delay {RATE_DELAY}s/row)")
    if args.city:
        print(f"  City filter: {args.city}")
    print("#" * 60)

    if not os.path.exists(CREDS_FILE):
        sys.exit(f"\nERROR: {CREDS_FILE} not found in current folder")

    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    ss = gspread.authorize(creds).open_by_key(SHEET_ID)

    if args.tab:
        tabs = [args.tab]
        print(f"\n  Single tab mode: {args.tab}")
    else:
        tabs = discover_tabs(ss, args.tab_prefix)
        tabs = order_tabs(tabs)
        print(f"\n  Discovered tabs (prefix '{args.tab_prefix}'): {tabs}")
        if not tabs:
            sys.exit(f"\nNo tabs found starting with '{args.tab_prefix}'")
        print(f"  Processing in priority order (commercial first).")

    # Build cross-run cache from sheet
    if args.no_cache:
        print("\n  --no-cache passed; skipping startup cache load.")
        cache = AddressCache()
    else:
        cache = build_cache_from_sheet(ss, tabs)

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
