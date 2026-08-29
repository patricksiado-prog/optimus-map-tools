#!/usr/bin/env python3
"""
optimus_secrets.py - one place to resolve API keys, so no key is ever
hardcoded in a tool file again.

Resolution order for the Google Places/Maps key:
  1. env var GOOGLE_MAPS_API_KEY  (or legacy PLACES_API_KEY)
  2. maps_api_key.txt next to the script
  3. maps_api_key.txt in the phone Download folders - same paths the tools
     already search for google_creds.json

Setup is one file, once per device:
  echo YOUR_NEW_KEY > maps_api_key.txt      (laptop, next to the .py)
  /storage/emulated/0/Download/maps_api_key.txt   (Pydroid / phone)

maps_api_key.txt is gitignored. Never paste a key into a .py file.
"""

import os

_KEY_FILE = "maps_api_key.txt"

# same search path the tools already use for google_creds.json
_SEARCH_PATHS = [
    _KEY_FILE,
    os.path.join(os.path.dirname(os.path.abspath(__file__)), _KEY_FILE),
    "/storage/emulated/0/Download/" + _KEY_FILE,
    "/storage/emulated/0/" + _KEY_FILE,
    os.path.expanduser("~/" + _KEY_FILE),
]

_SETUP_HELP = """
No Google Maps API key found.

Fix it once, then every Optimus tool picks it up:

  Laptop:  put the key in a file named maps_api_key.txt next to the script
  Phone:   put it at /storage/emulated/0/Download/maps_api_key.txt
  Or:      set the env var GOOGLE_MAPS_API_KEY

The file holds the key and nothing else. It is gitignored on purpose -
a key committed to the repo has to be treated as burned and rotated.
"""


def get_maps_api_key(required=True):
    """Return the Google Places/Maps key, or None when required=False."""
    for var in ("GOOGLE_MAPS_API_KEY", "PLACES_API_KEY"):
        val = os.environ.get(var, "").strip()
        if val:
            return val

    for path in _SEARCH_PATHS:
        try:
            if os.path.exists(path):
                with open(path) as fh:
                    val = fh.read().strip()
                if val:
                    return val
        except OSError:
            continue

    if required:
        raise SystemExit(_SETUP_HELP)
    return None
