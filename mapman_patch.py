"""
mapman_patch.py
Global retry + timeout patch for themapman.py.

USAGE:
    Save next to themapman.py on Desktop, then run MapMan with:
        python -c "import mapman_patch; exec(open('themapman.py').read())"

    OR add ONE line at the top of themapman.py (after imports):
        import mapman_patch

What it does:
- Forces 30-second timeout on every HTTP request (gspread, requests, urllib3, etc)
- Retries up to 3 times on ReadTimeout or ConnectionError with exponential backoff
- Prints retry attempts so you see what's happening

Fixes the "ReadTimeout: HTTPSConnectionPool sheets.googleapis.com Read timed out"
crash that happens when the leads sheet gets large and reads hang.
"""

import requests
import time

_orig_send = requests.adapters.HTTPAdapter.send

def _patched_send(self, request, **kwargs):
    if not kwargs.get("timeout"):
        kwargs["timeout"] = 30
    last_err = None
    for attempt in range(3):
        try:
            return _orig_send(self, request, **kwargs)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            last_err = e
            if attempt == 2:
                break
            wait = 2 ** attempt
            print(f"  [mapman_patch] RETRY {attempt+1}/3 in {wait}s: {type(e).__name__}")
            time.sleep(wait)
    raise last_err

requests.adapters.HTTPAdapter.send = _patched_send

print("[mapman_patch] active: 30s timeout, 3 retries with backoff")
