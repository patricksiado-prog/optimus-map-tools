#!/usr/bin/env python3
"""
hunter_enrich.py — minimal Hunter sheet enricher.

ONE JOB: read Hunter Green Commercial + Hunter Commercial,
find rows missing Phone or Business Name (and that are fiber-eligible),
enrich via Google Maps, write IN PLACE to the same row.

No run_zip. No run_houston. No fiber index dependency.
Run alongside themapman.py — does not replace it.

Usage:
    python hunter_enrich.py            # both tabs, headless, fiber-eligible only
    python hunter_enrich.py --visible  # show Chromium window
    python hunter_enrich.py --all      # ignore fiber status, enrich everything
    python hunter_enrich.py --limit 50 # cap rows enriched per tab
    python hunter_enrich.py --tab "Hunter Green Commercial"
"""
import argparse, os, re, sys, time
import gspread
from google.oauth2.service_account import Credentials
from playwright.sync_api import sync_playwright

VERSION   = "1.0"
SHEET_ID  = "12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag"
TABS      = ["Hunter Green Commercial", "Hunter Commercial"]
CREDS     = "google_creds.json"
SCOPES    = ["https://www.googleapis.com/auth/spreadsheets"]
ELIGIBLE  = ("fiber", "upgrade", "eligible", "gold", "green")
RATE_SLP  = 1.0


def get_ss():
    if not os.path.exists(CREDS):
        sys.exit(f"missing {CREDS}")
    c = Credentials.from_service_account_file(CREDS, scopes=SCOPES)
    return gspread.authorize(c).open_by_key(SHEET_ID)


def is_eligible(status: str) -> bool:
    s = (status or "").lower()
    return any(k in s for k in ELIGIBLE)


def blank(v) -> bool:
    return v is None or str(v).strip() == ""


def fmt_phone(raw: str) -> str:
    d = re.sub(r"\D", "", str(raw or ""))
    if len(d) == 11 and d.startswith("1"):
        d = d[1:]
    return f"({d[:3]}) {d[3:6]}-{d[6:]}" if len(d) == 10 else ""


def find_col(headers, *cands):
    for c in cands:
        for i, h in enumerate(headers):
            if h.strip().lower() == c.lower():
                return i + 1
    return None


def maps_lookup(page, address):
    """Return (business_name, formatted_phone) or (None, None)."""
    try:
        q = re.sub(r"\s+", "+", address.strip())
        page.goto(f"https://www.google.com/maps/search/{q}", timeout=30000)
        page.wait_for_timeout(2500)
        name, phone = None, None
        try:
            n = page.locator("h1").first.inner_text(timeout=2000).strip()
            if n and n.lower() != "results":
                name = n
        except Exception:
            pass
        try:
            lbl = page.locator('button[aria-label^="Phone:"]').first.get_attribute(
                "aria-label", timeout=2000
            ) or ""
            m = re.search(r"Phone:\s*([\d\s\-\(\)+]+)", lbl)
            if m:
                phone = fmt_phone(m.group(1))
        except Exception:
            pass
        return name, phone
    except Exception as e:
        print(f"    lookup err: {e}")
        return None, None


def enrich_tab(ss, tab_name, page, args):
    print(f"\n=== {tab_name} ===")
    try:
        ws = ss.worksheet(tab_name)
    except gspread.WorksheetNotFound:
        print("  NOT FOUND — skip"); return 0
    data = ws.get_all_values()
    if len(data) < 2:
        print("  empty"); return 0
    headers = data[0]
    print(f"  headers: {headers}")

    c_addr  = find_col(headers, "Address", "Address 1", "Street")
    c_phone = find_col(headers, "Phone", "Phone Number")
    c_biz   = find_col(headers, "Business Name", "Name", "Business")
    c_stat  = find_col(headers, "Fiber Status", "Status")
    if not c_addr:
        print("  NO ADDRESS COLUMN — skip"); return 0
    print(f"  cols: addr={c_addr} phone={c_phone} biz={c_biz} stat={c_stat}")

    candidates = []
    for r_idx, row in enumerate(data[1:], start=2):
        def cell(c): return row[c - 1] if c and c - 1 < len(row) else ""
        addr = cell(c_addr).strip()
        if not addr:
            continue
        if not args.all and c_stat and not is_eligible(cell(c_stat)):
            continue
        need_p = bool(c_phone) and blank(cell(c_phone))
        need_b = bool(c_biz)   and blank(cell(c_biz))
        if not (need_p or need_b):
            continue
        candidates.append((r_idx, addr, need_p, need_b))

    print(f"  candidates: {len(candidates)}")
    if args.limit:
        candidates = candidates[:args.limit]
        print(f"  (limited to {len(candidates)})")

    written = 0
    for i, (r_idx, addr, need_p, need_b) in enumerate(candidates, start=1):
        print(f"  [{i}/{len(candidates)}] row {r_idx}: {addr[:70]}")
        biz, phone = maps_lookup(page, addr)
        if need_p and phone:
            ws.update_cell(r_idx, c_phone, phone)
            print(f"    + phone {phone}"); written += 1
        if need_b and biz:
            ws.update_cell(r_idx, c_biz, biz)
            print(f"    + biz   {biz}"); written += 1
        time.sleep(RATE_SLP)
    print(f"  wrote {written} cells")
    return written


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--visible", action="store_true", help="show Chromium window")
    p.add_argument("--all", action="store_true", help="ignore fiber status filter")
    p.add_argument("--limit", type=int, default=0, help="max rows per tab")
    p.add_argument("--tab", help="single tab name (default: both Hunter tabs)")
    args = p.parse_args()

    print(f"hunter_enrich v{VERSION}")
    ss = get_ss()
    tabs = [args.tab] if args.tab else TABS
    total = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not args.visible)
        page = browser.new_context().new_page()
        for t in tabs:
            total += enrich_tab(ss, t, page, args)
        browser.close()
    print(f"\nTOTAL CELLS WRITTEN: {total}")


if __name__ == "__main__":
    main()
