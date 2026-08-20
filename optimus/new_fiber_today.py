"""
new_fiber_today.py -- the addresses that lit up since we last looked.

THE MISSION (BRAIN sections 98-103)
    The AT&T dealer map only plots addresses where fiber is ALREADY available.
    So an address that appears in a sweep today and was ABSENT from an earlier
    sweep of the same ground lit up in between. Those people are not prospects
    being pitched -- many have been waiting for it -- and they close easily.

THE PROBLEM THIS SOLVES WITHOUT A ZONE REGISTRY
    A first sweep of new ground makes every address look "new" when it is only
    new to US. Telling those apart normally needs a registry of which ground was
    swept when.

    This uses a proxy that works with the data we already have: STREET-LEVEL
    PRIOR COVERAGE. If we have seen other addresses on the same street on an
    EARLIER date, then that street was already swept -- so an address on it
    appearing for the first time today is genuinely newly lit, not newly noticed.

    Streets with no earlier sighting are reported separately as NEW GROUND, not
    mixed into the newly-lit list. Never inflate the headline number with them.

RUN
    python new_fiber_today.py                 # since yesterday
    python new_fiber_today.py --days 7        # the last week
    python new_fiber_today.py --write         # also write a 'New Fiber Today' tab

Reads the same google_creds.json the hunter uses, from the same folder.
"""
import argparse
import os
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
SHEET_ID = "1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA"
SRC_TAB = "Precise Fiber"
OUT_TAB = "New Fiber Today"
OUT_HEADER = ["First Seen", "Address", "Dot Color", "Street",
              "Street First Swept", "Days Street Known", "Confidence"]


def street_of(addr):
    """'6355 IVANHOE LN APT 2' -> 'IVANHOE LN'. Drops house number and unit."""
    a = re.sub(r"\s+", " ", (addr or "").strip().upper())
    a = re.sub(r"\b(APT|UNIT|STE|SUITE|#)\s*\S+$", "", a).strip()
    a = re.sub(r"^\d+[A-Z]?\s+", "", a)          # leading house number
    return a or "?"


def open_sheet():
    import gspread
    from google.oauth2.service_account import Credentials
    for name in ("google_creds.json", "creds.json", "service_account.json"):
        p = os.path.join(HERE, name)
        if os.path.exists(p):
            c = Credentials.from_service_account_file(
                p, scopes=["https://www.googleapis.com/auth/spreadsheets"])
            return gspread.authorize(c).open_by_key(SHEET_ID)
    raise SystemExit("No google_creds.json next to this script.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=1,
                    help="how far back counts as 'new' (default 1 = today)")
    ap.add_argument("--write", action="store_true", help="write the output tab")
    a = ap.parse_args()

    sh = open_sheet()
    ws = sh.worksheet(SRC_TAB)
    print("reading %s ..." % SRC_TAB)
    rows = ws.get("A2:C")                      # address, colour, captured-at
    print("  %d rows" % len(rows))

    # earliest sighting per address, and per street
    first_addr, first_street, colour = {}, {}, {}
    for r in rows:
        if not r or not r[0]:
            continue
        addr = r[0].strip()
        d = (r[2][:10] if len(r) > 2 and r[2] else "")
        if not d:
            continue
        if addr not in first_addr or d < first_addr[addr]:
            first_addr[addr] = d
            colour[addr] = (r[1] if len(r) > 1 else "") or ""
        s = street_of(addr)
        if s not in first_street or d < first_street[s]:
            first_street[s] = d

    cutoff = (date.today() - timedelta(days=a.days - 1)).isoformat()
    newly_lit, new_ground = [], defaultdict(int)
    for addr, d in first_addr.items():
        if d < cutoff:
            continue
        s = street_of(addr)
        sd = first_street.get(s, d)
        if sd < d:
            known = (datetime.fromisoformat(d) - datetime.fromisoformat(sd)).days
            conf = "HIGH" if known >= 3 else "MEDIUM"
            newly_lit.append([d, addr, colour.get(addr, ""), s, sd, known, conf])
        else:
            new_ground[s] += 1

    newly_lit.sort(key=lambda x: (x[0], x[3], x[1]))
    print("\n" + "=" * 68)
    print("NEWLY LIT since %s  (street was already swept -> genuinely new)" % cutoff)
    print("=" * 68)
    print("  addresses : %d" % len(newly_lit))
    if newly_lit:
        by_c = defaultdict(int)
        for r in newly_lit:
            by_c[r[2] or "?"] += 1
        print("  by colour : %s" % dict(by_c))
        by_s = defaultdict(int)
        for r in newly_lit:
            by_s[r[3]] += 1
        print("  top streets:")
        for s, n in sorted(by_s.items(), key=lambda kv: -kv[1])[:10]:
            print("     %-34s %d" % (s[:34], n))
        print("\n  first 15:")
        for r in newly_lit[:15]:
            print("     %s  %-42s %-7s (street known %sd)" % (r[0], r[1][:42], r[2], r[5]))
    else:
        print("  none. Either nothing lit up, or -- far more likely -- no ground")
        print("  was RE-SWEPT in this window. The signal only exists on a second")
        print("  pass over the same streets. Re-sweep a covered area and re-run.")

    print("\n  NEW GROUND (first ever sighting of the street -- NOT newly lit):")
    print("     %d streets, %d addresses" % (len(new_ground), sum(new_ground.values())))
    print("     These are new to us, not new to the world. Reported separately")
    print("     on purpose -- folding them in would inflate the headline.")

    if a.write and newly_lit:
        try:
            try:
                out = sh.worksheet(OUT_TAB)
                out.clear()
            except Exception:
                out = sh.add_worksheet(title=OUT_TAB, rows="5000",
                                       cols=str(len(OUT_HEADER)))
            out.append_row(OUT_HEADER, value_input_option="RAW")
            for i in range(0, len(newly_lit), 500):
                out.append_rows(newly_lit[i:i + 500], value_input_option="RAW")
            print("\n  wrote %d rows -> '%s'" % (len(newly_lit), OUT_TAB))
        except Exception as e:
            print("\n  tab write failed: %s" % str(e)[:80])
    return 0


if __name__ == "__main__":
    sys.exit(main())
