"""Reproduces Patrick's console error on gspread 6, then proves _gc() fixes it.
No network: builds the same objects the scraper holds after open_sheet()."""
import io, re, sys, types
import gspread
from gspread.http_client import HTTPClient
from gspread.spreadsheet import Spreadsheet
from google.auth.credentials import AnonymousCredentials

print("gspread", gspread.__version__)
creds = AnonymousCredentials()
http = HTTPClient(creds)                                   # what gspread 6 hands a Spreadsheet
# gspread 6 fetches metadata in __init__; stub it so this never touches Google
Spreadsheet.fetch_sheet_metadata = lambda self, params=None: {"properties": {"title": "fake"}, "sheets": []}
sh = Spreadsheet(http, {"id": "1DXu-fake", "properties": {"title": "fake"}})
assert type(sh.client).__name__ == "HTTPClient", type(sh.client)   # the gspread-6 shape, proven

# 1. REPRODUCE the exact console failure with the OLD code path
try:
    sh.client.open_by_key("1DXu-fake")
    print("*** did NOT reproduce -- old path worked?!"); sys.exit(1)
except AttributeError as e:
    assert "'HTTPClient' object has no attribute 'open_by_key'" in str(e), str(e)
    print("reproduced (old path):", e)
try:
    sh.client.list_spreadsheet_files(folder_id="x")
    print("*** did NOT reproduce list_spreadsheet_files"); sys.exit(1)
except AttributeError as e:
    assert "list_spreadsheet_files" in str(e), str(e)
    print("reproduced (old path):", e)

# 2. Load ONLY the helper from the patched scraper (no selenium etc.)
src = io.open("maps_scraper_standalone.py", encoding="utf-8").read()
m = re.search(r"\ndef _gc\(sh\):.*?\n(?=\ndef |\n[A-Za-z_]+ = )", src, re.S)
assert m, "helper not found in patched file"
ns = {}; exec(m.group(0), ns); _gc = ns["_gc"]

# 3. FIX: _gc(sh) returns a real Client on gspread 6
gc = _gc(sh)
assert isinstance(gc, gspread.Client), type(gc)
assert callable(getattr(gc, "open_by_key", None)), "no open_by_key on fixed client"
assert callable(getattr(gc, "list_spreadsheet_files", None)), "no list_spreadsheet_files"
assert gc.http_client.session.credentials is creds, "fixed client lost the service-account credentials"
assert gc.http_client.session is sh.client.session, "fixed client should reuse the existing authorized session (no re-auth)"
print("fixed (gspread 6): _gc(sh) ->", type(gc).__name__, "with open_by_key + list_spreadsheet_files, same creds")

# 4. gspread 5 shape: sh.client is ALREADY a Client -> returned unchanged
class OldClient:                      # what gspread 5.x put on Spreadsheet.client
    def open_by_key(self, k): return "ok"
old = types.SimpleNamespace(client=OldClient())
assert _gc(old) is old.client
print("gspread 5 shape: returned the existing Client unchanged")

# 5. The two call sites in the patched file no longer touch sh.client
assert "sh.client.open_by_key" not in src, "old redirect call still present"
assert "client = sh.client\n" not in src, "old sheet-log call still present"
assert src.count("_gc(sh).open_by_key(") == 1 and src.count("client = _gc(sh)\n") == 1, "call sites"
print("both call sites now go through _gc(sh); no sh.client.open_by_key left")
print("\nALL TESTS PASS")
