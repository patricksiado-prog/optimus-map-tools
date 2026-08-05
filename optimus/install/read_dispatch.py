# Reads the next scrape target from the sheet's _dispatch tab (A1=ZIP seed, A2=depth).
# Claude writes those cells; this PC obeys them. Falls back to 77008 / Deep.
import gspread
SHEET = "1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA"
try:
    ws = gspread.service_account(filename="google_creds.json").open_by_key(SHEET).worksheet("_dispatch")
    z = (ws.acell("A1").value or "77008").strip() or "77008"
    d = (ws.acell("A2").value or "3").strip() or "3"
    print(z + "|" + d)
except Exception:
    print("77008|3")
