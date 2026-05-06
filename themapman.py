#!/usr/bin/env python3
"""
THE MAP MAN — Hunter sheet enricher
====================================
ONE JOB: read Hunter Green Commercial, find rows missing
Phone / Business Name / Business Address, look up via Google Maps,
write back IN PLACE on the same row.

Run on PC laptop (needs Playwright + Chromium):
  python themapman.py                  # full pass, headless
  python themapman.py --visible        # show browser window
  python themapman.py --limit 10       # cap rows for testing
  python themapman.py --tab "Hunter Green Commercial"
  python themapman.py --all            # ignore fiber-status filter
  python themapman.py --no-update      # skip GitHub auto-update

Auto-pulls latest themapman.py from private GitHub repo on launch.
Reads token from any of:
  - env var GITHUB_TOKEN
  - /storage/emulated/0/Download/github_token.txt   (Pydroid)
  - C:\\Users\\patri\\Downloads\\github_token.txt   (PC)
  - ~/Downloads/github_token.txt
  - ~/optimus/github_token.txt
  - ./github_token.txt
"""

VERSION   = "10.0"
SHEET_ID  = "12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag"
DEFAULT_TAB = "Hunter Green Commercial"
GH_REPO   = "patricksiado-prog/optimus-map-tools"
GH_FILE   = "themapman.py"
GH_BRANCH = "main"

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
    print("  Checking for updates...")
    tok = _read_token()
    if not tok:
        print("  No token found — skipping update check.")
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
        print("  Updated! Restarting...")
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


# ─── HELPERS ─────────────────────────────────────────────────────────
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

def looks_like_address(text):
    if not text: return False
    t = str(text).strip()
    if not re.search(r"\b\d{2,6}\b", t): return False
    sigs = (" st", " street", " rd", " road", " ave", " avenue",
            " dr", " drive", " ln", " lane", " blvd", " boulevard",
            " pkwy", " parkway", " way", " ct", " court", " cir",
            " circle", " hwy", " highway", " fwy", " freeway",
            " loop", " trail", " trl", " place", " pl", " plaza")
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
                  cols=max(len(new_headers), 20))
    except Exception:
        pass
    last = col_letter(len(new_headers))
    ws.update(range_name=f"A1:{last}1", values=[new_headers])
    print(f"  Added columns: {new_cols}")
    return new_headers


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
                m = re.search(r"[\(]?\d{3}[\)]?[\s\-\.]\d{3}[\s\-\.]\d{4}",
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
                if looks_like_address(val):
                    return val
        except Exception:
            pass
    return ""

def maps_lookup(address, zipc=""):
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
        if zipc and re.match(r"^\d{5}$", zipc.strip()):
            q += " " + zipc.strip()
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
        print(f"    lookup err: {e}")
        return None


# ─── MAIN ENRICHER ───────────────────────────────────────────────────
def enrich(tab_name, args):
    print(f"\n=== {tab_name} ===")
    if not os.path.exists(CREDS_FILE):
        sys.exit(f"ERROR: {CREDS_FILE} not found in current folder")
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    ss = gspread.authorize(creds).open_by_key(SHEET_ID)
    try:
        ws = ss.worksheet(tab_name)
    except gspread.WorksheetNotFound:
        sys.exit(f"ERROR: tab '{tab_name}' not found in sheet")
    data = ws.get_all_values()
    if len(data) < 2:
        print("  empty"); return
    headers = data[0]
    print(f"  headers: {headers}")

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
    c_zip   = find_col(headers, "ZIP", "Zip", "Postal Code")
    c_stat  = find_col(headers, "Type", "Fiber Status", "Status")

    if not c_addr:
        sys.exit("ERROR: no Address column found in tab")
    print(f"  cols: addr={c_addr} phone={c_phone} biz={c_biz} "
          f"biz_addr={c_baddr} zip={c_zip} stat={c_stat}")

    def cell(row, c):
        return row[c-1].strip() if c and c-1 < len(row) else ""

    candidates = []
    for r_idx, row in enumerate(data[1:], start=2):
        addr = cell(row, c_addr)
        if not addr or not looks_like_address(addr): continue
        if "(no #" in addr.lower(): continue
        if not args.all and c_stat and not is_eligible(cell(row, c_stat)):
            continue
        need_p = bool(c_phone) and is_blank(cell(row, c_phone))
        need_b = bool(c_biz)   and is_blank(cell(row, c_biz))
        need_a = bool(c_baddr) and is_blank(cell(row, c_baddr))
        if not (need_p or need_b or need_a): continue
        candidates.append({
            "row": r_idx, "addr": addr,
            "zip": cell(row, c_zip) if c_zip else "",
            "need_p": need_p, "need_b": need_b, "need_a": need_a,
        })

    print(f"  candidates: {len(candidates)}")
    if args.limit:
        candidates = candidates[:args.limit]
        print(f"  (limited to {len(candidates)})")
    if not candidates:
        return

    init_browser(headless=not args.visible)
    written = 0
    try:
        for i, c in enumerate(candidates, 1):
            print(f"\n  [{i}/{len(candidates)}] r{c['row']}: {c['addr'][:70]}")
            found = maps_lookup(c["addr"], c["zip"])
            if not found:
                print("    no result"); continue
            updates = []
            if c["need_p"] and found["phone"]:
                updates.append({"range": f"{col_letter(c_phone)}{c['row']}",
                                "values": [[found["phone"]]]})
                print(f"    + phone {found['phone']}")
            if c["need_b"] and found["name"]:
                updates.append({"range": f"{col_letter(c_biz)}{c['row']}",
                                "values": [[found["name"]]]})
                print(f"    + biz   {found['name']}")
            if c["need_a"] and found["address"]:
                updates.append({"range": f"{col_letter(c_baddr)}{c['row']}",
                                "values": [[found["address"]]]})
                print(f"    + baddr {found['address']}")
            if updates and c_psrc:
                updates.append({"range": f"{col_letter(c_psrc)}{c['row']}",
                                "values": [["Google Maps"]]})
            if updates and c_chk:
                updates.append({"range": f"{col_letter(c_chk)}{c['row']}",
                                "values": [[now_str()]]})
            if updates:
                for attempt in range(3):
                    try:
                        ws.batch_update(updates,
                                        value_input_option="USER_ENTERED")
                        written += len(updates)
                        break
                    except Exception as e:
                        print(f"    write err {attempt+1}: {e}")
                        time.sleep(3)
            time.sleep(RATE_DELAY)
    finally:
        close_browser()
    print(f"\n  TOTAL CELLS WRITTEN: {written}")


def main():
    p = argparse.ArgumentParser(description=f"THE MAP MAN v{VERSION}")
    p.add_argument("--tab", default=DEFAULT_TAB)
    p.add_argument("--visible", action="store_true")
    p.add_argument("--all", action="store_true")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--no-update", action="store_true")
    args = p.parse_args()

    print("\n" + "#" * 60)
    print(f"  THE MAP MAN v{VERSION}")
    print(f"  Tab: {args.tab}")
    print("  Goal: Phone + Business Name + Business Address (in place)")
    print("#" * 60 + "\n")

    enrich(args.tab, args)


if __name__ == "__main__":
    main()
