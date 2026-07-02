#!/usr/bin/env python3
"""
THE MAP MAN v11.3.0 - Run on Pydroid (cell phone)

v11.3.0 - SELF-HEALING (fixes "keeps stopping"):
  - Never dies on a network blip: all Google API calls retry with backoff
  - Sheets connection auto-reconnects (startup AND mid-run, incl. 429 quota)
  - Transient failures are NOT written to the sheet anymore, so those
    addresses get retried instead of being poisoned as failed forever
  - OVER_QUERY_LIMIT / REQUEST_DENIED pause + retry instead of marking
    every row NO_TENANT_FOUND
  - Rows that keep failing while others succeed get written as ERROR
    after 5 tries so one cursed address can't loop forever

IF THE PHONE ITSELF KILLS THE RUN (script gone, no error printed):
  - Pydroid menu -> Settings -> enable "Keep screen on"
  - Android Settings -> Apps -> Pydroid 3 -> Battery -> Unrestricted
    (battery optimization is what murders long runs overnight)
  - Keep the phone plugged in
"""
import subprocess, sys, os, re, json, math, time
from datetime import datetime, timezone

VERSION = "11.3.0"

print("Checking packages...")
for pkg in ["gspread", "google-auth", "requests"]:
    try:
        __import__(pkg.replace("-", "_"))
        print("  %s OK" % pkg)
    except:
        print("  Installing %s..." % pkg)
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

import gspread
from google.oauth2.service_account import Credentials
import requests

API_KEY  = "AIzaSyA9PJQJmf1LGFN3lATv8-se3tsIy6kCG9g"
SHEET_ID = "1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA"
IN_TAB   = "Hunter Green Commercial"
OUT_TAB  = "Fiber Commercial Leads"
SCOPES   = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
RADII    = [30, 60, 100, 200, 500]
MAX_M    = 150
EARTH_M  = 6371000

TRANSIENT = "TRANSIENT"          # sentinel: network/API trouble, retry later, never write
MAX_ROW_FAILS = 5                # give up on one address after this many failed passes

creds_file = None
for p in ["google_creds.json", "/storage/emulated/0/Download/google_creds.json", "/storage/emulated/0/google_creds.json"]:
    if os.path.exists(p):
        creds_file = p
        break
if not creds_file:
    print("ERROR: google_creds.json not found. Put it in /Download or same folder.")
    sys.exit(1)

def haversine(lat1, lng1, lat2, lng2):
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return EARTH_M * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def api_get(url, params, tries=4):
    """GET with retry/backoff. Returns parsed JSON dict, or None if the
    network/API stayed down through all tries (caller treats as TRANSIENT)."""
    delay = 2
    for attempt in range(tries):
        try:
            r = requests.get(url, params=params, timeout=60)
            data = r.json()
            status = data.get("status")
            if status in ("OVER_QUERY_LIMIT", "UNKNOWN_ERROR"):
                print("  API says %s - waiting %ds..." % (status, delay))
            elif status == "REQUEST_DENIED":
                print("  API REQUEST_DENIED (key/billing?): %s - waiting %ds..." % (
                    data.get("error_message", ""), delay))
            else:
                return data
        except Exception as e:
            print("  Network error (try %d/%d): %s" % (attempt + 1, tries, e))
        time.sleep(delay)
        delay = min(delay * 2, 60)
    return None

def geocode(address):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    data = api_get(url, {"query": address, "key": API_KEY})
    if data is None:
        return TRANSIENT
    if data.get("status") == "OK" and data.get("results"):
        loc = data["results"][0]["geometry"]["location"]
        return {"lat": loc["lat"], "lng": loc["lng"]}
    if data.get("status") == "ZERO_RESULTS":
        return None
    return None

def nearby(lat, lng, radius):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    data = api_get(url, {"location": "%s,%s" % (lat, lng), "radius": radius, "key": API_KEY})
    if data is None:
        return TRANSIENT
    if data.get("status") == "OK":
        return [{
            "place_id": p.get("place_id"),
            "name": p.get("name"),
            "types": p.get("types", []),
            "status": p.get("business_status", "UNKNOWN"),
            "lat": p["geometry"]["location"]["lat"],
            "lng": p["geometry"]["location"]["lng"],
        } for p in data.get("results", [])]
    return []

def place_details(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    data = api_get(url, {
        "place_id": place_id,
        "fields": "name,formatted_phone_number,formatted_address,website,types,business_status",
        "key": API_KEY,
    })
    if data is None:
        return TRANSIENT
    if data.get("status") == "OK":
        rr = data.get("result", {})
        return {
            "name": rr.get("name"),
            "phone": rr.get("formatted_phone_number"),
            "address": rr.get("formatted_address"),
            "website": rr.get("website"),
            "types": rr.get("types", []),
        }
    return None

BLOCKED_NAMES = {
    "walmart", "target", "costco", "sam's club", "kroger", "heb", "aldi",
    "dollar general", "family dollar", "dollar tree", "big lots",
    "mcdonald's", "burger king", "wendy's", "jack in the box", "taco bell",
    "kfc", "popeyes", "chick-fil-a", "sonic", "arbys", "dairy queen",
    "subway", "jimmy john's", "jersey mike's", "firehouse subs",
    "starbucks", "dunkin", "dunkin donuts",
    "usps", "post office", "dmv", "irs", "courthouse", "city hall",
    "police", "fire station", "library", "school", "elementary", "middle school",
    "high school", "university", "college", "hospital", "clinic", "medical center",
    "bank of america", "chase", "wells fargo", "citibank", "pnc", "regions",
    "shell", "exxon", "chevron", "bp", "mobil", "valero", "circle k",
    "7-eleven", "speedway", "quiktrip", "racetrac",
    "home depot", "lowe's", "menards", "ace hardware",
    "best buy", "circuit city",
    "autozone", "o'reilly", "advance auto parts", "napa",
    "cvs", "walgreens", "rite aid", "duane reade",
    "t-mobile", "verizon", "at&t", "sprint", "cricket",
    "ihop", "denny's", "cracker barrel", "applebee's", "chili's",
    "tgi fridays", "red lobster", "olive garden", "longhorn",
    "buffalo wild wings", "hooters", "outback",
    "marriott", "hilton", "hampton", "holiday inn", "best western",
    "la quinta", "motel 6", "super 8", "comfort inn", "quality inn",
    "fedex", "ups", "usps", "amazon", "whole foods", "trader joe's",
}

def is_blocked(name):
    if not name:
        return False
    n = name.lower()
    for blocked in BLOCKED_NAMES:
        if blocked in n:
            return True
    return False

COMM_TYPES = {
    "store","restaurant","food","cafe","health","doctor","dentist",
    "pharmacy","gym","spa","beauty_salon","hair_care","lodging",
    "finance","insurance_agency","lawyer","real_estate_agency",
    "travel_agency","accounting","bank","car_repair","car_dealer",
    "gas_station","shopping_mall","clothing_store","electronics_store",
    "furniture_store","hardware_store","home_goods_store",
    "jewelry_store","shoe_store","supermarket","grocery_or_supermarket",
    "convenience_store","liquor_store","bakery","meal_delivery",
    "meal_takeaway","night_club","bar","bowling_alley","casino",
    "movie_theater","amusement_park","aquarium","art_gallery","museum",
    "zoo","book_store","veterinary_care","physiotherapist",
    "plumber","electrician","roofing_contractor","general_contractor",
    "painter","locksmith","moving_company","storage","laundry",
    "car_wash","funeral_home","office","establishment",
    "point_of_interest","local_government_office","post_office",
    "library","fire_station","police","hospital","courthouse",
    "city_hall","parking",
}

def is_commercial(types):
    return any(t in COMM_TYPES for t in types)

def has_phone(phone):
    return phone and len(re.sub(r"\D", "", phone)) >= 7

def blank_result(address):
    return {
        "input": address, "source": None, "radius": None,
        "distance_m": None, "place_id": None, "status": None,
        "name": None, "phone": None, "address": None,
        "website": None, "types": None,
        "fiber_lat": None, "fiber_lng": None, "error": None
    }

def resolve(address, fiber_lat=None, fiber_lng=None, want_state=None):
    result = blank_result(address)
    def _ff(x):
        try:
            return float(str(x).strip())
        except Exception:
            return None
    _flat, _flng = _ff(fiber_lat), _ff(fiber_lng)
    geo = {"lat": _flat, "lng": _flng} if (_flat is not None and _flng is not None) else geocode(address)
    if geo == TRANSIENT:
        result["status"] = TRANSIENT
        return result
    if not geo:
        result["status"] = "GEOCODE_FAILED"
        result["error"] = "Could not geocode"
        return result
    result["fiber_lat"] = geo["lat"]
    result["fiber_lng"] = geo["lng"]
    for radius in RADII:
        cands = nearby(geo["lat"], geo["lng"], radius)
        if cands == TRANSIENT:
            result["status"] = TRANSIENT
            return result
        filtered = [c for c in cands
                    if c.get("status") == "OPERATIONAL"
                    and c.get("place_id")
                    and is_commercial(c.get("types", []))
                    and not is_blocked(c.get("name", ""))]
        if not filtered:
            continue
        for c in filtered:
            c["distance_m"] = haversine(geo["lat"], geo["lng"], c["lat"], c["lng"])
        filtered.sort(key=lambda x: x["distance_m"])
        best = filtered[0]
        if best["distance_m"] > MAX_M:
            continue
        det = place_details(best["place_id"])
        if det == TRANSIENT:
            result["status"] = TRANSIENT
            return result
        if not det or not has_phone(det.get("phone")):
            continue
        if is_blocked(det.get("name", "")):
            continue
        result.update({
            "source": "Tenant resolver",
            "radius": radius,
            "distance_m": round(best["distance_m"], 1),
            "place_id": best["place_id"],
            "status": "RESOLVED",
            "name": det["name"],
            "phone": det["phone"],
            "address": det["address"],
            "website": det["website"],
            "types": ", ".join(det.get("types", []))
        })
        return result
    result["status"] = "NO_TENANT_FOUND"
    result["error"] = "No valid tenant with phone"
    return result

# ── SHEETS CONNECTION (self-healing) ─────────────────────────────────
client = None
out_ws = None

def connect():
    """(Re)connect to Sheets. Retries forever with backoff - never crashes."""
    global client, out_ws
    delay = 5
    while True:
        try:
            client = gspread.authorize(Credentials.from_service_account_file(creds_file, scopes=SCOPES))
            try:
                out_ws = client.open_by_key(SHEET_ID).worksheet(OUT_TAB)
            except gspread.WorksheetNotFound:
                out_ws = client.open_by_key(SHEET_ID).add_worksheet(title=OUT_TAB, rows="1000", cols="20")
            init_out(out_ws)
            return
        except Exception as e:
            print("  Sheets connect failed: %s" % e)
            print("  Retrying in %ds..." % delay)
            time.sleep(delay)
            delay = min(delay * 2, 300)

def sheets_read(fn, desc):
    """Run a Sheets read, reconnect + retry forever on failure."""
    while True:
        try:
            return fn()
        except Exception as e:
            print("  %s failed: %s" % (desc, e))
            print("  Reconnecting, retrying in 15s...")
            time.sleep(15)
            connect()

def read_input(sheet_id, tab):
    ws = client.open_by_key(sheet_id).worksheet(tab)
    records = ws.get_all_records()
    out = []
    for row in records:
        addr = (row.get("Address") or row.get("address") or
                row.get("Street Address") or row.get("Full Address") or
                row.get("Location"))
        if addr and str(addr).strip():
            out.append({"address": str(addr).strip(), "lat": row.get("Lat") or row.get("lat"), "lng": row.get("Lng") or row.get("lng"), "state": (row.get("State") or row.get("state") or "")})
    return out

def get_already_done(sheet_id, tab):
    try:
        ws = client.open_by_key(sheet_id).worksheet(tab)
        rows = ws.get_all_values()
        if len(rows) <= 1:
            return set()
        return set(row[0].strip() for row in rows[1:] if row and row[0].strip())
    except gspread.WorksheetNotFound:
        return set()

def init_out(ws):
    headers = [
        "Input Address", "Source", "Resolver Radius", "Resolver Distance Meters",
        "Place ID", "Resolver Status", "Tenant Name", "Tenant Phone",
        "Tenant Address", "Tenant Website", "Tenant Types",
        "Fiber Lat", "Fiber Lng", "Processed At", "Error"
    ]
    if not ws.get_all_values():
        ws.append_row(headers)
    return headers

def write_result(result, max_retries=5):
    row = [
        result.get("input", ""), result.get("source", ""),
        result.get("radius", ""), result.get("distance_m", ""),
        result.get("place_id", ""), result.get("status", ""),
        result.get("name", ""), result.get("phone", ""),
        result.get("address", ""), result.get("website", ""),
        result.get("types", ""), result.get("fiber_lat", ""),
        result.get("fiber_lng", ""),
        datetime.now(timezone.utc).isoformat(),
        result.get("error", "")
    ]
    delay = 2
    for attempt in range(max_retries):
        try:
            out_ws.append_row(row)
            return True
        except Exception as e:
            msg = str(e)
            print("  Write error (attempt %d/%d): %s" % (attempt + 1, max_retries, e))
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg or "Quota" in msg or "quota" in msg:
                wait = 65  # write quota resets per minute - short retries never survive it
            else:
                wait = delay
                delay = min(delay * 2, 60)
            print("  Waiting %ds..." % wait)
            time.sleep(wait)
            if attempt >= 1:
                connect()  # token/socket may be dead - rebuild connection
    print("  FAILED to write after %d attempts" % max_retries)
    return False

print("\n" + "="*55)
print("  THE MAP MAN v%s - API Resolver (pulls phones)" % VERSION)
print("  Running on Pydroid - cell phone")
print("="*55)
print("Connecting to Google Sheets...")
connect()

print("Checking for already-processed addresses...")
already_done = sheets_read(lambda: get_already_done(SHEET_ID, OUT_TAB), "Read output tab")
print("Found %d already processed. Will skip them." % len(already_done))

addresses = sheets_read(lambda: read_input(SHEET_ID, IN_TAB), "Read input tab")
print("Loaded %d total addresses from '%s'" % (len(addresses), IN_TAB))

to_process = [a for a in addresses if a["address"] not in already_done]
print("New addresses to process: %d" % len(to_process))

if not to_process:
    print("Nothing new to process. All done!")
    sys.exit(0)

# ── MAIN LOOP: passes over pending rows until everything is done ─────
# Transient (network/API) failures are queued and retried next pass
# instead of being written to the sheet as failed. Program only exits
# when every address is genuinely done.
pending = to_process
fail_counts = {}
pass_delay = 60
pass_num = 0
total = len(to_process)
done_count = 0

while pending:
    pass_num += 1
    if pass_num > 1:
        print("\n--- Retry pass %d: %d address(es) left ---" % (pass_num, len(pending)))
    retry_later = []
    successes = 0
    for i, item in enumerate(pending, 1):
        addr = item["address"]
        print("\n[%d/%d] %s" % (done_count + 1, total, addr))
        try:
            result = resolve(addr, item.get("lat"), item.get("lng"), item.get("state"))
        except Exception as e:
            print("  Unexpected error: %s" % e)
            result = blank_result(addr)
            result["status"] = TRANSIENT
        if result["status"] == TRANSIENT:
            print("  -> network/API trouble, will retry this one later")
            retry_later.append(item)
            continue
        success = write_result(result)
        if success:
            done_count += 1
            successes += 1
            print("  -> %s | Name: %s | Phone: %s | Distance: %sm" % (
                result["status"], result.get("name") or "N/A",
                result.get("phone") or "N/A",
                result.get("distance_m") or "N/A"
            ))
        else:
            print("  -> WRITE FAILED, will retry this one later")
            retry_later.append(item)
        time.sleep(0.2)

    # Only count a strike against a row when OTHER rows succeeded this
    # pass (network was fine, that row is cursed). A global outage never
    # burns strikes - the loop just waits for the network to come back.
    if retry_later and successes:
        still = []
        for item in retry_later:
            a = item["address"]
            fail_counts[a] = fail_counts.get(a, 0) + 1
            if fail_counts[a] >= MAX_ROW_FAILS:
                r = blank_result(a)
                r["status"] = "ERROR"
                r["error"] = "Gave up after %d failed attempts" % fail_counts[a]
                write_result(r)
                done_count += 1
                print("  Gave up on %s after %d tries (recorded as ERROR)" % (a, fail_counts[a]))
            else:
                still.append(item)
        retry_later = still

    if retry_later:
        if successes:
            pass_delay = 60
        else:
            pass_delay = min(pass_delay * 2, 600)
        print("\n%d address(es) hit trouble. Waiting %ds, then retrying..." % (len(retry_later), pass_delay))
        time.sleep(pass_delay)
        connect()  # refresh connection before the retry pass
    pending = retry_later

print("\nDone! Results in '%s' tab." % OUT_TAB)
