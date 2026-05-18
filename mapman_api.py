#!/usr/bin/env python3
"""
MAPMAN_API v1.0 - Phone enrichment via Google Places API
Drop-in replacement for themapman.py. No browser, no Playwright.
Writes phones + biz names + Phone Source + Checked At to the same Hunter tabs
themapman uses, in the MASTER sheet 1FhO2BT...
"""

VERSION = "1.0"
GH_REPO = "patricksiado-prog/optimus-map-tools"
GH_FILE = "mapman_api.py"
GH_BRANCH = "main"
AUTO_UPDATE = True

SHEET_ID = "1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA"
DEFAULT_TAB_PREFIX = "Hunter"
API_KEY = "AIzaSyA9PJQJmf1LGFN3lATv8-se3tsIy6kCG9g"

PHONE_SOURCE_FOUND = "Google Maps"
PHONE_SOURCE_EMPTY = "Google Maps (no biz)"

RATE_DELAY = 0.1

import os, sys, re, time, json, argparse
from datetime import datetime
import urllib.request

def check_update():
    if not AUTO_UPDATE or "--no-update" in sys.argv:
        return
    try:
        url = f"https://raw.githubusercontent.com/{GH_REPO}/{GH_BRANCH}/{GH_FILE}"
        req = urllib.request.Request(url, headers={"User-Agent": "mapman-api"})
        with urllib.request.urlopen(req, timeout=10) as r:
            latest = r.read().decode("utf-8", errors="replace")
        m = re.search(r'VERSION\s*=\s*["\']([\d.]+)["\']', latest)
        if not m: return
        nv = m.group(1)
        if nv == VERSION:
            print(f"  Up to date (v{VERSION})")
            return
        print(f"  Updating to v{nv}...")
        with open(os.path.abspath(__file__), "w", encoding="utf-8") as f:
            f.write(latest)
        print("  Updated. Restart and run again.")
        sys.exit(0)
    except Exception as e:
        print(f"  Update check failed: {e}")

if "--no-update" not in sys.argv:
    check_update()

import requests
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]

CREDS_FILE = next((p for p in [
    r"C:\Users\patri\Desktop\google_creds.json",
    "/storage/emulated/0/Download/google_creds.json",
    os.path.join(os.path.expanduser("~"), "Desktop", "google_creds.json"),
    "google_creds.json",
] if os.path.exists(p)), "google_creds.json")

FIND_URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

_session = requests.Session()
_stats = {"find": 0, "details": 0, "errors": 0, "phones": 0, "biz": 0}


def now_str():
    return datetime.now().strftime("%m/%d/%Y %I:%M %p")


def col_letter(n):
    out = ""
    while n:
        n, rem = divmod(n - 1, 26)
        out = chr(65 + rem) + out
    return out


def _is_bad_phone(d):
    if len(d) != 10: return True
    ac = d[:3]
    if ac[0] in ('0', '1'): return True
    if ac in {'000','111','123','456','654','789','900','911','999','555'}: return True
    if d[3:6] in ('000','100','111','555'): return True
    if d[6:] in ('0000','1111'): return True
    return False


def fmt_phone(s):
    d = re.sub(r"\D", "", str(s or ""))
    if len(d) == 11 and d.startswith("1"): d = d[1:]
    if len(d) == 10 and not _is_bad_phone(d):
        return f"({d[:3]}) {d[3:6]}-{d[6:]}"
    return ""


def is_blank(v):
    return v is None or str(v).strip() == ""


COORD_RE = re.compile(r"^-?\d+\.\d+\s*,\s*-?\d+\.\d+$")


def is_coord_only(text):
    return bool(COORD_RE.match((text or "").strip()))


def looks_like_address(text):
    if not text: return False
    t = str(text).strip()
    if is_coord_only(t): return False
    if not re.search(r"\b\d{1,6}\b", t): return False
    sigs = (" st"," street"," rd"," road"," ave"," avenue"," dr"," drive",
            " ln"," lane"," blvd"," boulevard"," pkwy"," parkway"," way",
            " ct"," court"," cir"," circle"," hwy"," highway"," fwy",
            " loop"," trail"," trl"," place"," pl"," plaza"," ter")
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


def _is_echo_biz(biz, addr):
    if not biz or not addr: return False
    n = re.sub(r'[^a-z0-9\s]', ' ', biz.lower()).strip()
    a = re.sub(r'[^a-z0-9\s]', ' ', addr.lower()).strip()
    if not n or not a: return False
    if n == a: return True
    if n in a or a in n: return True
    return False


def find_place(address, city, state, zipc):
    parts = [address]
    if city: parts.append(city)
    if state: parts.append(state)
    if zipc: parts.append(zipc)
    query = ", ".join(parts)
    try:
        r = _session.get(FIND_URL, params={
            "input": query,
            "inputtype": "textquery",
            "fields": "place_id,name,formatted_address,types,business_status",
            "key": API_KEY,
        }, timeout=10)
        _stats["find"] += 1
        d = r.json()
        if d.get("status") == "OVER_QUERY_LIMIT":
            print("  QUOTA - pausing 60s")
            time.sleep(60)
            return None
        if d.get("status") not in ("OK", "ZERO_RESULTS"):
            print(f"  find err: {d.get('status')} {d.get('error_message','')}")
            _stats["errors"] += 1
            return {"name": "", "phone": "", "address": "", "src": PHONE_SOURCE_EMPTY}
        cands = d.get("candidates") or []
        if not cands:
            return {"name": "", "phone": "", "address": "", "src": PHONE_SOURCE_EMPTY}
        place = cands[0]
        types = place.get("types") or []
        no_biz_types = {"street_address","route","premise","subpremise",
                        "intersection","neighborhood","postal_code"}
        name = (place.get("name") or "").strip()
        addr = (place.get("formatted_address") or "").strip()
        if _is_echo_biz(name, address):
            name = ""
        if types and all(t in no_biz_types for t in types) and not name:
            return {"name": "", "phone": "", "address": addr, "src": PHONE_SOURCE_EMPTY}
        place_id = place.get("place_id")
        if not place_id:
            return {"name": name, "phone": "", "address": addr,
                    "src": PHONE_SOURCE_FOUND if name else PHONE_SOURCE_EMPTY}
        # Step 2: details for phone
        try:
            r2 = _session.get(DETAILS_URL, params={
                "place_id": place_id,
                "fields": "formatted_phone_number,name,formatted_address,business_status",
                "key": API_KEY,
            }, timeout=10)
            _stats["details"] += 1
            d2 = r2.json()
            res = d2.get("result") or {}
            if d2.get("status") != "OK":
                return {"name": name, "phone": "", "address": addr,
                        "src": PHONE_SOURCE_FOUND if name else PHONE_SOURCE_EMPTY}
            phone = fmt_phone(res.get("formatted_phone_number") or "")
            if phone: _stats["phones"] += 1
            rn = (res.get("name") or "").strip()
            if rn and not _is_echo_biz(rn, address):
                name = rn
            ra = (res.get("formatted_address") or "").strip()
            if ra: addr = ra
            if name: _stats["biz"] += 1
            if name or phone:
                return {"name": name, "phone": phone, "address": addr, "src": PHONE_SOURCE_FOUND}
            return {"name": "", "phone": "", "address": addr, "src": PHONE_SOURCE_EMPTY}
        except Exception as e:
            print(f"  details err: {e}")
            _stats["errors"] += 1
            return {"name": name, "phone": "", "address": addr,
                    "src": PHONE_SOURCE_FOUND if name else PHONE_SOURCE_EMPTY}
    except Exception as e:
        print(f"  find err: {e}")
        _stats["errors"] += 1
        return None


TAB_PRIORITY = ["Hunter Commercial", "Hunter Green Commercial",
                "Hunter Leads", "Hunter Residential", "Hunter Green Residential"]


def discover_tabs(ss, prefix):
    pl = prefix.strip().lower()
    return [w.title for w in ss.worksheets() if w.title.lower().startswith(pl)]


def order_tabs(tabs):
    pri = {n.lower(): i for i, n in enumerate(TAB_PRIORITY)}
    return sorted(tabs, key=lambda t: (pri.get(t.lower(), 999), t.lower()))


def parse_instance(s):
    if not s: return (None, None)
    m = re.match(r"^\s*(\d+)\s*of\s*(\d+)\s*$", s.lower())
    if not m: return (None, None)
    n, total = int(m.group(1)), int(m.group(2))
    return (n, total) if 1 <= n <= total else (None, None)


def enrich_tab(ss, tab_name, args, partition):
    print(f"\n=== {tab_name} ===")
    try:
        ws = ss.worksheet(tab_name)
    except gspread.WorksheetNotFound:
        print("    NOT FOUND - skip")
        return 0, 0
    data = ws.get_all_values()
    if len(data) < 2:
        print("    empty - skip")
        return 0, 0
    headers = data[0]
    headers = ensure_columns(ws, headers,
        ["Phone", "Business Name", "Business Address", "Phone Source", "Checked At"])
    if len(headers) > len(data[0]):
        data = ws.get_all_values()
        headers = data[0]
    c_addr = find_col(headers, "Address", "Address 1", "Street")
    c_phone = find_col(headers, "Phone", "Phone Number")
    c_biz = find_col(headers, "Business Name", "Name", "Business")
    c_baddr = find_col(headers, "Business Address", "Verified Address")
    c_psrc = find_col(headers, "Phone Source")
    c_chk = find_col(headers, "Checked At")
    c_zip = find_col(headers, "ZIP", "Zip", "Zip Code")
    c_city = find_col(headers, "City")
    c_state = find_col(headers, "State", "ST")
    c_ptype = find_col(headers, "Dot Type", "Type", "Property Type", "Category")
    if not c_addr:
        print("    NO Address column - skip")
        return 0, 0

    def cell(row, c):
        return row[c-1].strip() if c and c-1 < len(row) else ""

    city_filter = []
    if getattr(args, "city", ""):
        city_filter = [c.strip().lower() for c in args.city.split(",") if c.strip()]

    inst_n, inst_total = partition
    candidates = []
    skip_already = skip_no_addr = skip_filter = skip_part = skip_city = 0
    for r_idx, row in enumerate(data[1:], start=2):
        addr = cell(row, c_addr)
        if not addr or not looks_like_address(addr):
            skip_no_addr += 1
            continue
        if getattr(args, "commercial_only", False) and c_ptype:
            if "residential" in cell(row, c_ptype).lower():
                skip_filter += 1
                continue
        if city_filter:
            rc = cell(row, c_city).lower() if c_city else ""
            if not any(cf in rc for cf in city_filter):
                skip_city += 1
                continue
        if inst_n is not None:
            if (r_idx - 2) % inst_total != (inst_n - 1):
                skip_part += 1
                continue
        src_val = cell(row, c_psrc) if c_psrc else ""
        has_phone = bool(c_phone and cell(row, c_phone))
        if has_phone and src_val == PHONE_SOURCE_FOUND:
            skip_already += 1
            continue
        candidates.append({
            "row": r_idx, "addr": addr,
            "zip": cell(row, c_zip) if c_zip else "",
            "city": cell(row, c_city) if c_city else "",
            "state": cell(row, c_state) if c_state else "TX",
        })

    print(f"    candidates: {len(candidates)} (skip: already={skip_already} filter={skip_filter} city={skip_city} part={skip_part} noaddr={skip_no_addr})")
    if args.limit:
        candidates = candidates[:args.limit]
    if not candidates:
        return 0, 0

    cells_written = 0
    rows_written = 0
    pending = []

    def flush():
        if not pending: return 0
        for attempt in range(3):
            try:
                ws.batch_update(pending, value_input_option='USER_ENTERED')
                return len(pending)
            except Exception as e:
                if '429' in str(e) or 'Quota' in str(e):
                    print(f"      quota - waiting {30*(attempt+1)}s")
                    time.sleep(30*(attempt+1))
                else:
                    print(f"      write err: {e}")
                    time.sleep(3)
        return 0

    for i, c in enumerate(candidates, 1):
        result = find_place(c["addr"], c.get("city",""), c.get("state","TX"), c.get("zip",""))
        if not result:
            time.sleep(1)
            continue
        updates = []
        src = result.get("src") or PHONE_SOURCE_EMPTY
        if c_psrc:
            updates.append({"range": f"{col_letter(c_psrc)}{c['row']}", "values": [[src]]})
        if c_chk:
            updates.append({"range": f"{col_letter(c_chk)}{c['row']}", "values": [[now_str()]]})
        cur = data[c['row']-1] if c['row']-1 < len(data) else []

        def is_blank_cell(col):
            return col and is_blank(cur[col-1] if col-1 < len(cur) else "")

        row_had_data = False
        if c_phone and result.get("phone") and is_blank_cell(c_phone):
            updates.append({"range": f"{col_letter(c_phone)}{c['row']}", "values": [[result["phone"]]]})
            print(f"    [{i}/{len(candidates)}] r{c['row']} {c['addr'][:40]:40} -> + phone {result['phone']}")
            row_had_data = True
        if c_biz and result.get("name") and is_blank_cell(c_biz):
            updates.append({"range": f"{col_letter(c_biz)}{c['row']}", "values": [[result["name"]]]})
            if not row_had_data:
                print(f"    [{i}/{len(candidates)}] r{c['row']} {c['addr'][:40]:40} -> + biz {result['name'][:30]}")
            row_had_data = True
        if c_baddr and result.get("address") and is_blank_cell(c_baddr):
            updates.append({"range": f"{col_letter(c_baddr)}{c['row']}", "values": [[result["address"]]]})
            row_had_data = True
        if not row_had_data:
            print(f"    [{i}/{len(candidates)}] r{c['row']} {c['addr'][:40]:40} -> {src}")
        if updates:
            pending.extend(updates)
            cells_written += len(updates)
            if row_had_data:
                rows_written += 1
        if len(pending) >= 20:
            flush()
            pending.clear()
        time.sleep(RATE_DELAY)

    if pending:
        flush()
        pending.clear()
    print(f"\n    {tab_name}: {cells_written} cells, {rows_written} rows had real data")
    return cells_written, rows_written


def main():
    p = argparse.ArgumentParser(description=f"MAPMAN_API v{VERSION}")
    p.add_argument("--tab", help="single tab name")
    p.add_argument("--tab-prefix", default=DEFAULT_TAB_PREFIX)
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--city", default="")
    p.add_argument("--instance", default="")
    p.add_argument("--commercial-only", action="store_true")
    p.add_argument("--no-update", action="store_true")
    p.add_argument("--no-pick", action="store_true")
    p.add_argument("--no-spawn", action="store_true")
    args = p.parse_args()

    inst_n, inst_total = parse_instance(args.instance)
    inst_label = f"{inst_n}of{inst_total}" if inst_n else "single"

    print("\n" + "#"*60)
    print(f"  MAPMAN_API v{VERSION} - Google Places API enrichment")
    print(f"  Sheet: {SHEET_ID[:15]}...  Instance: {inst_label}")
    if args.city: print(f"  City filter: {args.city}")
    if args.commercial_only: print(f"  Commercial-only: YES")
    print("#"*60)

    if not os.path.exists(CREDS_FILE):
        sys.exit(f"\nERROR: google_creds.json not found")

    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    ss = gspread.authorize(creds).open_by_key(SHEET_ID)

    if args.tab:
        tabs = [args.tab]
    else:
        tabs = order_tabs(discover_tabs(ss, args.tab_prefix))
        if not tabs:
            sys.exit(f"No tabs starting with '{args.tab_prefix}'")
    print(f"\n  Tabs: {tabs}")

    t0 = time.time()
    total_cells = total_rows = 0
    try:
        for tab in tabs:
            c, r = enrich_tab(ss, tab, args, (inst_n, inst_total))
            total_cells += c
            total_rows += r
    except KeyboardInterrupt:
        print("\nInterrupted")

    elapsed = time.time() - t0
    cost = (_stats["find"] + _stats["details"]) * 0.017 / 1000
    print("\n" + "#"*60)
    print(f"  DONE in {elapsed:.0f}s")
    print(f"  {total_cells} cells, {total_rows} rows enriched")
    print(f"  API: {_stats['find']} find + {_stats['details']} details, {_stats['phones']} phones, {_stats['biz']} biz, {_stats['errors']} errors")
    print(f"  Cost: ~${cost:.2f}")
    print("#"*60)


if __name__ == "__main__":
    main()
