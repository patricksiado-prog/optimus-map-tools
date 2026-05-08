#!/usr/bin/env python3
"""
build_dedup_tab.py
==================
Pulls commercial leads from Hunter Commercial + Hunter Green Commercial
for a chosen metro, deduplicates by normalized address, and writes them
to a new tab named "Hunter <METRO> Dedup". Mapman picks up the tab
automatically (Hunter prefix) — run mapman against it with:

    python themapman.py --tab "Hunter OKC Dedup" --no-pick

USAGE:
  python build_dedup_tab.py okc       # creates Hunter OKC Dedup
  python build_dedup_tab.py houston   # creates Hunter Houston Dedup
  python build_dedup_tab.py austin    # creates Hunter Austin Dedup
  python build_dedup_tab.py ms        # creates Hunter MS Gulf Dedup
  python build_dedup_tab.py           # interactive picker

PREREQS:
  - google_creds.json in same folder (service account JSON)
  - gspread + google-auth installed (already from mapman install)

REQUIRES:
  - Hunter Commercial + Hunter Green Commercial source tabs.
  - These must have at minimum: Address, City columns.
"""

import sys, re, time
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

# ─── CONFIG ──────────────────────────────────────────────────────────
SHEET_ID = "12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag"
CREDS    = "google_creds.json"

SOURCE_TABS = ["Hunter Commercial", "Hunter Green Commercial"]

METROS = {
    "okc": {
        "label":  "OKC metro",
        "cities": ["oklahoma city", "edmond", "midwest city", "choctaw"],
        "tab":    "Hunter OKC Dedup",
    },
    "houston": {
        "label":  "Houston metro",
        "cities": ["houston", "bellaire"],
        "tab":    "Hunter Houston Dedup",
    },
    "austin": {
        "label":  "Austin metro",
        "cities": ["austin", "hornsby bend"],
        "tab":    "Hunter Austin Dedup",
    },
    "ms": {
        "label":  "MS Gulf Coast",
        "cities": ["biloxi", "ocean springs", "gulfport"],
        "tab":    "Hunter MS Gulf Dedup",
    },
}

ABBREV = {"street":"st","road":"rd","avenue":"ave","drive":"dr",
          "lane":"ln","boulevard":"blvd","circle":"cir","court":"ct"}

OUTPUT_HEADERS = [
    "Address", "City", "State", "ZIP",
    "Phone", "Business Name", "Business Address",
    "Dot Type",
    "Phone Source", "Checked At",
    "Source Tab",
]


def norm_addr(a):
    if not a: return ""
    s = str(a).lower().strip()
    s = re.sub(r"[,\.]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return " ".join(ABBREV.get(t, t) for t in s.split()).strip()


def find_col(headers, *names):
    """Return 1-indexed column for first matching header, else None."""
    low = [str(h).strip().lower() if h else "" for h in headers]
    for name in names:
        n = name.lower()
        if n in low:
            return low.index(n) + 1
    return None


def cell(row, c):
    return str(row[c-1]).strip() if c and c-1 < len(row) and row[c-1] else ""


def pick_metro_interactive():
    print("\n" + "=" * 60)
    print("  build_dedup_tab.py  -  pick metro")
    print("=" * 60)
    keys = list(METROS.keys())
    for i, k in enumerate(keys, 1):
        m = METROS[k]
        print(f"    {i}. {m['label']:<22} -> {m['tab']}")
    print()
    while True:
        try:
            choice = input(f"  Pick (1-{len(keys)}): ").strip()
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)
        if choice.isdigit() and 1 <= int(choice) <= len(keys):
            return keys[int(choice) - 1]
        print("  Invalid. Try again.")


def main():
    # Pick metro from CLI or interactive
    metro_key = None
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower().strip()
        if arg in METROS:
            metro_key = arg
        else:
            print(f"Unknown metro '{arg}'. Valid: {', '.join(METROS.keys())}")
            sys.exit(1)
    else:
        metro_key = pick_metro_interactive()

    metro = METROS[metro_key]
    target_cities = set(c.lower() for c in metro["cities"])
    target_tab = metro["tab"]

    print(f"\n  Metro:        {metro['label']}")
    print(f"  Cities:       {', '.join(metro['cities'])}")
    print(f"  Target tab:   {target_tab}")
    print(f"  Source tabs:  {', '.join(SOURCE_TABS)}")
    print()

    # Connect
    if not Path(CREDS).exists():
        sys.exit(f"ERROR: {CREDS} not in current folder. cd to the folder "
                 f"containing google_creds.json then re-run.")
    creds = Credentials.from_service_account_file(CREDS, scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"])
    gc = gspread.authorize(creds)
    ss = gc.open_by_key(SHEET_ID)

    # Pull rows from source tabs
    seen = {}    # norm_addr -> row dict (keep first occurrence)
    stats = {"scanned": 0, "matched_city": 0, "already_checked": 0,
             "duplicates": 0, "kept": 0}

    for tab_name in SOURCE_TABS:
        try:
            ws = ss.worksheet(tab_name)
        except gspread.exceptions.WorksheetNotFound:
            print(f"  WARN: source tab '{tab_name}' not found, skipping.")
            continue
        print(f"  Reading '{tab_name}' ...", end=" ", flush=True)
        data = ws.get_all_values()
        if len(data) < 2:
            print("(empty)")
            continue
        headers = data[0]
        c_addr  = find_col(headers, "Address", "Address 1", "Street")
        c_city  = find_col(headers, "City")
        c_state = find_col(headers, "State")
        c_zip   = find_col(headers, "ZIP", "Zip", "Zip Code", "Postal Code")
        c_phone = find_col(headers, "Phone", "Phone Number")
        c_biz   = find_col(headers, "Business Name", "Name", "Business")
        c_baddr = find_col(headers, "Business Address", "Verified Address")
        c_psrc  = find_col(headers, "Phone Source")
        c_chk   = find_col(headers, "Checked At", "Phone Checked At")
        c_dot   = find_col(headers, "Dot Type", "Type", "Fiber Status")

        if not c_addr or not c_city:
            print(f"(SKIP — missing Address or City column)")
            continue

        kept_this_tab = 0
        merged_this_tab = 0
        for row in data[1:]:
            stats["scanned"] += 1
            addr = cell(row, c_addr)
            if not addr:
                continue
            city = cell(row, c_city).lower()
            if city not in target_cities:
                continue
            stats["matched_city"] += 1

            n = norm_addr(addr)
            if not n:
                continue

            # Determine Fiber Green status:
            # - Hunter Green Commercial → always "Yes"
            # - Hunter Commercial with Dot Type containing "FIBER ELIGIBLE"
            #   or "Green" → "Yes"
            # - Hunter Commercial with "UPGRADE ELIGIBLE" / "Gold" / "Orange"
            #   → "No" (upgrade-eligible but not fiber yet)
            # - Otherwise blank (unknown)
            dot_value = cell(row, c_dot) if c_dot else ""
            dot_lower = dot_value.lower()
            if tab_name in GREEN_SOURCE_TABS:
                fiber_green = "Yes"
            elif "fiber eligible" in dot_lower or "(green)" in dot_lower:
                fiber_green = "Yes"
            elif ("upgrade eligible" in dot_lower or "gold" in dot_lower
                  or "orange" in dot_lower):
                fiber_green = "No"
            else:
                fiber_green = ""

            # Build the candidate row
            candidate = {
                "Address":          addr,
                "City":             cell(row, c_city) if c_city else "",
                "State":            cell(row, c_state) if c_state else "",
                "ZIP":              cell(row, c_zip)   if c_zip   else "",
                "Phone":            cell(row, c_phone) if c_phone else "",
                "Business Name":    cell(row, c_biz)   if c_biz   else "",
                "Business Address": cell(row, c_baddr) if c_baddr else "",
                "Fiber Green":      fiber_green,
                "Phone Source":     cell(row, c_psrc) if c_psrc else "",
                "Checked At":       cell(row, c_chk)  if c_chk  else "",
                "Source Tab":       tab_name,
            }

            if n in seen:
                # Merge: keep richer (non-empty) value for every field.
                # If the existing row already has data for a field,
                # the candidate cannot overwrite it with blank.
                # If the existing row is blank for a field and the
                # candidate has data, take it.
                existing = seen[n]
                changed = False
                for k, v in candidate.items():
                    if v and not existing.get(k):
                        existing[k] = v
                        changed = True
                # Special case: Fiber Green = "Yes" always wins over "No".
                # If we previously marked an address No (saw it as upgrade-
                # eligible only) and a Green Commercial pass shows it's
                # actually fiber-eligible, upgrade to Yes.
                if (candidate.get("Fiber Green") == "Yes"
                        and existing.get("Fiber Green") != "Yes"):
                    existing["Fiber Green"] = "Yes"
                    changed = True
                # Track source provenance: append tab name if new
                if tab_name not in existing["Source Tab"].split(", "):
                    existing["Source Tab"] = (existing["Source Tab"]
                                              + ", " + tab_name).strip(", ")
                    changed = True
                if changed:
                    merged_this_tab += 1
                stats["duplicates"] += 1
                continue

            # First time seeing this address
            seen[n] = candidate
            kept_this_tab += 1
            stats["kept"] += 1
        print(f"matched {kept_this_tab} new uniques, "
              f"merged {merged_this_tab} duplicates")

    rows = list(seen.values())
    print(f"\n  Stats:")
    print(f"    Total rows scanned:         {stats['scanned']}")
    print(f"    Matched city filter:        {stats['matched_city']}")
    print(f"    Already had phone (kept):   "
          f"{sum(1 for r in rows if r['Phone'])}")
    print(f"    Cross-tab duplicates:       {stats['duplicates']}")
    print(f"    Unique addresses to write:  {len(rows)}")

    if not rows:
        print("\n  Nothing to write. Exiting.")
        return

    # Create or clear target tab
    try:
        target_ws = ss.worksheet(target_tab)
        print(f"\n  Tab '{target_tab}' exists. Clearing and rewriting.")
        target_ws.clear()
    except gspread.exceptions.WorksheetNotFound:
        print(f"\n  Creating new tab '{target_tab}' ...")
        target_ws = ss.add_worksheet(
            title=target_tab,
            rows=str(len(rows) + 100),
            cols=str(len(OUTPUT_HEADERS) + 2))

    # Write headers + rows
    payload = [OUTPUT_HEADERS]
    for r in rows:
        payload.append([r.get(h, "") for h in OUTPUT_HEADERS])
    target_ws.update(values=payload, range_name="A1",
                     value_input_option="RAW")

    print(f"  ✓ Wrote {len(rows)} rows to '{target_tab}'.")
    print()
    print(f"  NEXT STEP — run mapman against this tab:")
    print(f"    python themapman.py --tab \"{target_tab}\" --no-pick")
    print()
    print(f"  Or with 2 instances parallel:")
    print(f"    PC A: python themapman.py --tab \"{target_tab}\" --instance 1of2 --no-pick")
    print(f"    PC B: python themapman.py --tab \"{target_tab}\" --instance 2of2 --no-pick")


if __name__ == "__main__":
    main()
