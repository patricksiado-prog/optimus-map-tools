#!/usr/bin/env python3
"""
cleaner.py - Trims bloated tabs in ATT FIBER LEADS sheet so the 10M cell
ceiling stops blocking fiber_hunter / mapman / validate when they try to
add new tabs.

Run from any folder that contains google_creds.json:
    python cleaner.py
"""
import os
import sys
import gspread
from google.oauth2.service_account import Credentials

SHEET_ID = "12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag"

TRIM_PLAN = {
    "HOT ZONES":         500,
    "Gold Clusters":     200,
    "GOLD ALERTS":       500,
    "Green Residential": 8500,
}

CRED_PATHS = [
    os.path.expanduser("~/optimus/google_creds.json"),
    "google_creds.json",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "google_creds.json"),
    "/storage/emulated/0/Download/google_creds.json",
    "/storage/emulated/0/Pydroid3/google_creds.json",
]

creds_file = next((p for p in CRED_PATHS if os.path.exists(p)), None)
if not creds_file:
    print("ERROR: google_creds.json not found in any of:")
    for p in CRED_PATHS:
        print(f"  {p}")
    sys.exit(1)

print(f"Using creds: {creds_file}")

creds = Credentials.from_service_account_file(
    creds_file,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(creds)
sh = gc.open_by_key(SHEET_ID)

print(f"Opened: {sh.title}\n")

print("Current tab sizes:")
total_cells_before = 0
for ws in sh.worksheets():
    cells = ws.row_count * ws.col_count
    total_cells_before += cells
    flag = " <-- BLOATED" if cells > 500_000 else ""
    print(f"  {ws.title:40s}  {ws.row_count:>7} rows x {ws.col_count:>4} cols = {cells:>10,} cells{flag}")
print(f"  TOTAL: {total_cells_before:,} cells\n")

freed_total = 0
for tab_name, target_rows in TRIM_PLAN.items():
    try:
        ws = sh.worksheet(tab_name)
    except gspread.exceptions.WorksheetNotFound:
        print(f"MISS  {tab_name}: tab not found")
        continue

    cur_rows = ws.row_count
    cur_cols = ws.col_count
    if cur_rows <= target_rows:
        print(f"SKIP  {tab_name}: already {cur_rows} rows")
        continue

    freed = (cur_rows - target_rows) * cur_cols
    print(f"TRIM  {tab_name}: {cur_rows} -> {target_rows}  (frees {freed:,} cells)")
    try:
        ws.resize(rows=target_rows, cols=cur_cols)
        freed_total += freed
        print(f"      done")
    except Exception as e:
        print(f"      FAIL: {str(e)[:100]}")

print(f"\nTotal cells freed: {freed_total:,}")
print(f"Sheet cell budget after trim: ~{total_cells_before - freed_total:,} of 10,000,000")
print("\nNow re-run fiber_hunter - it should be able to add its tab.")
