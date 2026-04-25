"""
VALIDATOR MAN v1.3 — COMMERCIAL SAME-TAB VERSION
================================================

WHAT THIS VERSION DOES:
- Does NOT create a new Google Sheet tab.
- Does NOT create 50,000 / 100,000 / 1,000,000 row tabs.
- Writes results into your existing Commercial tab.
- Adds result columns to the right side of Commercial if missing.
- Skips Residential tabs by default.
- Skips fake/header rows like "address".
- Does not label TIMEOUT/ERROR as ATT INTERNET AIR.
- Keeps writing to Google Sheets.

INSTALL:
  pip install requests gspread google-auth

RUN:
  python validatorman.py

OR:
  python validatorman.py --tab "Commercial"

FOR RECHECKING ROWS THAT ALREADY HAVE ATT STATUS:
  python validatorman.py --tab "Commercial" --force

SLOWER / SAFER:
  python validatorman.py --tab "Commercial" --delay 3
"""

import os
import sys
import re
import json
import time
import argparse
import random
from datetime import datetime

import requests
import gspread
from google.oauth2.service_account import Credentials


# ── CONFIG ──────────────────────────────────────────────────────────

CREDS_FILE = "google_creds.json"
SHEET_ID = "15ymTkIGPWs6quB035l414ns5hkG9cQ5xr_W4ukd0OAA"

# Default tab to write on.
DEFAULT_TAB = "Commercial"

# These tabs will not be processed unless you specifically use --tab.
SKIP_TABS = {
    "validator man",
    "gold alerts",
    "hot zones",
    "changes",
    "residential",
    "green residential",
    "green res",
    "resi",
}

# Result columns added to the right side of Commercial if missing.
RESULT_HEADERS = [
    "ATT Status",
    "Pitch Type",
    "Max Speed Mbps",
    "Fiber Available",
    "Service Type",
    "Checked At",
]

NAME_HEADERS = [
    "business name",
    "name",
    "company",
    "company name",
    "last name",
]

ADDRESS_HEADERS = [
    "address",
    "address1",
    "address 1",
    "street",
    "street address",
    "original address",
    "maps address",
    "property address",
    "full address",
    "mailing address",
    "location",
]

CITY_HEADERS = [
    "city",
    "town",
]

STATE_HEADERS = [
    "state",
    "st",
]

ZIP_HEADERS = [
    "zip",
    "zipcode",
    "zip code",
    "postal code",
    "postalcode",
    "postal",
]

ATT_API_URL = (
    "https://www.att.com/services/shop/model/ecom/shop/view/unified/"
    "qualification/service/CheckAvailabilityRESTService/invokeCheckAvailability"
)

ATT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Origin": "https://www.att.com",
    "Referer": "https://www.att.com/internet/availability/",
    "Accept-Language": "en-US,en;q=0.9",
}

BASE_DELAY = 2.0
JITTER = 0.8
SAVE_BATCH_SIZE = 20


# ── BASIC HELPERS ───────────────────────────────────────────────────

def norm(s):
    if not s:
        return ""
    s = str(s)
    s = re.sub(r"[^\w\s]", " ", s.lower().strip())
    return re.sub(r"\s+", " ", s).strip()


def col_letter(n):
    """1 -> A, 2 -> B, etc."""
    out = ""
    while n:
        n, rem = divmod(n - 1, 26)
        out = chr(65 + rem) + out
    return out


def first_value(row_dict, keys):
    for key in keys:
        val = row_dict.get(key, "")
        if val:
            return str(val).strip()
    return ""


def pitch_type(att_status):
    if att_status == "FIBER":
        return "ATT FIBER"
    if att_status == "COPPER":
        return "ATT UPGRADE"
    if att_status == "NONE":
        return "ATT INTERNET AIR"
    return "CHECK AGAIN"


def clean_address_for_att(address):
    address = str(address or "").strip()
    address = re.sub(r",?\s+[A-Z]{2}\s+\d{5}.*$", "", address)
    address = re.sub(r",?\s+\d{5}.*$", "", address)
    return address.strip()


def extract_zip(*texts):
    for text in texts:
        if not text:
            continue
        m = re.search(r"\b\d{5}(?:-\d{4})?\b", str(text))
        if m:
            return m.group(0)[:5]
    return ""


def looks_like_address(text):
    if not text:
        return False

    t = str(text).strip()

    if norm(t) in ["address", "street address", "property address", "full address"]:
        return False

    if re.match(r"^-?\d+\.\d+,\s*-?\d+\.\d+$", t):
        return False

    street_words = (
        " st", " street", " rd", " road", " ave", " avenue", " dr", " drive",
        " ln", " lane", " blvd", " boulevard", " pkwy", " parkway",
        " way", " ct", " court", " cir", " circle", " hwy", " highway",
        " loop", " fwy", " freeway", " trail", " trl", " place", " pl",
        " tunnel", " suite", " ste",
    )

    tl = " " + t.lower()

    return bool(re.search(r"\d{2,}", t)) and any(w in tl for w in street_words)


def is_fake_address(addr):
    a = norm(addr)
    fake_values = {
        "",
        "address",
        "street address",
        "property address",
        "full address",
        "maps address",
        "original address",
        "location",
    }
    return a in fake_values


def find_address_from_row(row, headers):
    """
    First tries known address columns.
    If that fails, scans the whole row for something that looks like a street address.
    """
    row_dict = {}

    for i, h in enumerate(headers):
        val = row[i].strip() if i < len(row) else ""
        row_dict[h] = val

    addr = first_value(row_dict, ADDRESS_HEADERS)
    if addr and not is_fake_address(addr):
        return addr

    for cell in row:
        if looks_like_address(cell):
            return str(cell).strip()

    return ""


# ── GOOGLE SHEETS ───────────────────────────────────────────────────

def connect_sheets():
    if not os.path.exists(CREDS_FILE):
        print("\nERROR: %s not found." % CREDS_FILE)
        print("Put google_creds.json in the same folder as this script.")
        sys.exit(1)

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    ss = client.open_by_key(SHEET_ID)

    print("Connected to Google Sheets ✓")
    return ss


def ensure_result_columns(ws, headers):
    """
    Adds result columns to the right side of the existing tab if missing.
    Does NOT create a new tab.
    """
    lower_headers = [h.lower().strip() for h in headers]
    updated_headers = list(headers)

    changed = False

    for h in RESULT_HEADERS:
        if h.lower() not in lower_headers:
            updated_headers.append(h)
            lower_headers.append(h.lower())
            changed = True

    if changed:
        last_col = col_letter(len(updated_headers))
        ws.update([updated_headers], "A1:%s1" % last_col)
        print("  Added result columns to: %s" % ws.title)

    index = {}
    for i, h in enumerate(updated_headers):
        index[h.lower().strip()] = i + 1

    return updated_headers, index


def get_tabs_to_process(ss, tab_filter=None):
    """
    If --tab is used, process only that exact tab.
    If no --tab is used, process Commercial by default.
    """
    if tab_filter:
        try:
            return [ss.worksheet(tab_filter)]
        except gspread.exceptions.WorksheetNotFound:
            print("ERROR: Tab not found: %s" % tab_filter)
            sys.exit(1)

    try:
        return [ss.worksheet(DEFAULT_TAB)]
    except gspread.exceptions.WorksheetNotFound:
        print("ERROR: Could not find default tab: %s" % DEFAULT_TAB)
        print("Available tabs:")
        for ws in ss.worksheets():
            print(" - %s" % ws.title)
        print("\nRun with the exact tab name, for example:")
        print('python validatorman.py --tab "Commercial"')
        sys.exit(1)


def safe_batch_update(ws, updates):
    if not updates:
        return

    for attempt in range(3):
        try:
            ws.batch_update(updates, value_input_option="USER_ENTERED")
            return True
        except Exception as e:
            print("  Sheet save error attempt %d: %s" % (attempt + 1, e))
            time.sleep(5)

    return False


# ── AT&T CHECK ──────────────────────────────────────────────────────

def check_att(address, zipc, delay):
    addr_line = clean_address_for_att(address)

    payload = {
        "userInputZip": zipc,
        "userInputAddressLine1": addr_line,
        "mode": "fullAddress",
        "customer_type": "Consumer",
        "dtvMigrationFlag": False,
    }

    try:
        time.sleep(delay + random.uniform(-JITTER / 2, JITTER))

        r = requests.post(
            ATT_API_URL,
            data=json.dumps(payload),
            headers=ATT_HEADERS,
            timeout=10,
        )

        if r.status_code == 429:
            print("    ⚠ Rate limited — waiting 30 seconds")
            time.sleep(30)
            r = requests.post(
                ATT_API_URL,
                data=json.dumps(payload),
                headers=ATT_HEADERS,
                timeout=10,
            )

        if r.status_code != 200:
            return "ERROR", "NO", "", "ERROR_%d" % r.status_code

        profile = r.json().get("profile", {})

        spd = str(
            profile.get("maxAvailableSpeed", "")
            or profile.get("maxDnldSpeed", "")
            or ""
        )

        svc = (
            profile.get("serviceType", "")
            or profile.get("networkType", "")
        )

        if profile.get("isGIGAFiberAvailable") or profile.get("isFiberAvailable"):
            return "FIBER", "YES", spd, svc or "FIBER"

        if profile.get("isIPBBAvailable") or profile.get("isDSLAvailable"):
            return "COPPER", "NO", spd, svc or "COPPER/DSL"

        return "NONE", "NO", "", "NO SERVICE"

    except requests.exceptions.Timeout:
        return "TIMEOUT", "NO", "", "TIMEOUT"
    except requests.exceptions.ConnectionError:
        return "CONN_ERROR", "NO", "", "NO CONNECTION"
    except Exception as e:
        return "ERROR", "NO", "", str(e)[:40]


# ── MAIN PROCESS ────────────────────────────────────────────────────

def process_tab(ws, delay, force=False):
    print("\n" + "=" * 60)
    print("Checking COMMERCIAL tab: %s" % ws.title)
    print("=" * 60)

    if ws.title.lower().strip() in SKIP_TABS:
        print("  Skipping residential/non-commercial tab: %s" % ws.title)
        return {
            "checked": 0,
            "fiber": 0,
            "copper": 0,
            "air": 0,
            "errors": 0,
        }

    rows = ws.get_all_values()

    if not rows or len(rows) < 2:
        print("  No rows found.")
        return {
            "checked": 0,
            "fiber": 0,
            "copper": 0,
            "air": 0,
            "errors": 0,
        }

    headers_raw = rows[0]
    headers_raw, col_index = ensure_result_columns(ws, headers_raw)
    headers = [h.lower().strip() for h in headers_raw]

    att_col = col_index["att status"]
    pitch_col = col_index["pitch type"]
    speed_col = col_index["max speed mbps"]
    fiber_col = col_index["fiber available"]
    service_col = col_index["service type"]
    checked_col = col_index["checked at"]

    checked = 0
    fiber_ct = 0
    copper_ct = 0
    air_ct = 0
    error_ct = 0
    skipped = 0

    updates = []

    for row_num, row in enumerate(rows[1:], start=2):
        row_padded = row + [""] * (len(headers_raw) - len(row))

        row_dict = {}
        for i, h in enumerate(headers):
            row_dict[h] = row_padded[i].strip() if i < len(row_padded) else ""

        old_att_status = row_dict.get("att status", "").strip()

        if old_att_status and not force:
            skipped += 1
            continue

        addr = find_address_from_row(row, headers)

        if not addr:
            continue

        if is_fake_address(addr):
            continue

        if re.match(r"^-?\d+\.\d+,\s*-?\d+\.\d+$", addr):
            continue

        city = first_value(row_dict, CITY_HEADERS)
        state = first_value(row_dict, STATE_HEADERS) or "TX"
        zipc = first_value(row_dict, ZIP_HEADERS)

        if not zipc:
            zipc = extract_zip(addr, " ".join(row))

        if not zipc:
            print("  Row %d skipped — no ZIP found: %s" % (row_num, addr[:60]))
            continue

        name = first_value(row_dict, NAME_HEADERS)
        label = name if name else addr

        print("  Row %d: %s" % (row_num, label[:60]))

        att_status, att_fiber, att_speed, svc_type = check_att(addr, zipc, delay)
        ptype = pitch_type(att_status)

        if att_status == "FIBER":
            icon = "✅ FIBER"
            fiber_ct += 1
        elif att_status == "COPPER":
            icon = "🔶 UPGRADE"
            copper_ct += 1
        elif att_status == "NONE":
            icon = "📡 AIR"
            air_ct += 1
        else:
            icon = "⚠ %s" % att_status
            error_ct += 1

        checked += 1

        print("       → %s | %s" % (icon, ptype))

        now_str = datetime.now().strftime("%m/%d/%Y %I:%M %p")

        # Individual cell updates so it does not matter where the result columns are.
        updates.extend([
            {
                "range": "%s%d" % (col_letter(att_col), row_num),
                "values": [[att_status]],
            },
            {
                "range": "%s%d" % (col_letter(pitch_col), row_num),
                "values": [[ptype]],
            },
            {
                "range": "%s%d" % (col_letter(speed_col), row_num),
                "values": [[att_speed]],
            },
            {
                "range": "%s%d" % (col_letter(fiber_col), row_num),
                "values": [[att_fiber]],
            },
            {
                "range": "%s%d" % (col_letter(service_col), row_num),
                "values": [[svc_type]],
            },
            {
                "range": "%s%d" % (col_letter(checked_col), row_num),
                "values": [[now_str]],
            },
        ])

        if checked % SAVE_BATCH_SIZE == 0:
            safe_batch_update(ws, updates)
            updates = []
            print("       Saved batch to Google Sheets ✓")

    if updates:
        safe_batch_update(ws, updates)
        print("       Saved final batch to Google Sheets ✓")

    print("\n  Commercial tab complete: %s" % ws.title)
    print("  Checked: %d | Skipped already checked: %d" % (checked, skipped))
    print("  Fiber: %d | Copper: %d | Air: %d | Errors: %d" % (
        fiber_ct,
        copper_ct,
        air_ct,
        error_ct,
    ))

    return {
        "checked": checked,
        "fiber": fiber_ct,
        "copper": copper_ct,
        "air": air_ct,
        "errors": error_ct,
    }


def main():
    parser = argparse.ArgumentParser(description="VALIDATOR MAN v1.3 COMMERCIAL SAME-TAB")

    parser.add_argument(
        "--tab",
        type=str,
        default=None,
        help='Only check one tab by exact name. Example: --tab "Commercial"'
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=BASE_DELAY,
        help="Seconds between AT&T checks"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Recheck rows even if ATT Status already exists"
    )

    args = parser.parse_args()

    print("\n" + "█" * 60)
    print("  VALIDATOR MAN v1.3")
    print("  Commercial same-tab Google Sheets writer")
    print("  No new tab. No 10M cell overflow.")
    print("█" * 60 + "\n")

    ss = connect_sheets()

    tabs = get_tabs_to_process(ss, tab_filter=args.tab)

    totals = {
        "checked": 0,
        "fiber": 0,
        "copper": 0,
        "air": 0,
        "errors": 0,
    }

    for ws in tabs:
        result = process_tab(ws, delay=args.delay, force=args.force)

        for k in totals:
            totals[k] += result.get(k, 0)

    print("\n" + "█" * 60)
    print("  VALIDATOR MAN FINISHED")
    print("█" * 60)
    print("  Total checked      : %d" % totals["checked"])
    print("  ✅ ATT FIBER       : %d" % totals["fiber"])
    print("  🔶 ATT UPGRADE     : %d" % totals["copper"])
    print("  📡 ATT INTERNET AIR: %d" % totals["air"])
    print("  ⚠ Errors          : %d" % totals["errors"])
    print("█" * 60)

    if totals["checked"] == 0:
        print("\nNothing checked.")
        print("Try:")
        print('python validatorman.py --tab "Commercial" --force')


if __name__ == "__main__":
    main()