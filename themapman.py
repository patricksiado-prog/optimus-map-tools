#!/usr/bin/env python3
"""
THE MAP MAN v11.1.0 - API Resolver
Reads Hunter Green Commercial, adds phones, skips done, blocks chains.
"""
import subprocess, sys, os, re, json, math, time
from datetime import datetime, timezone

VERSION = "11.1.0"

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

import pathlib
creds_file = None
for p in ["google_creds.json", "./google_creds.json", "/storage/emulated/0/Download/google_creds.json", "/storage/emulated/0/google_creds.json", "C:/Users/patri/Desktop/google_creds.json"]:
    if pathlib.Path(p).exists():
        creds_file = str(pathlib.Path(p).resolve())
        break
if not creds_file:
    print("ERROR: google_creds.json not found.")
    sys.exit(1)

def haversine(lat1, lng1, lat2, lng2):
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return EARTH_M * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def geocode(address):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": address, "key": API_KEY}
    try:
        r = requests.get(url, params=params, timeout=60)
        data = r.json()
        if data.get("status") == "OK" and data.get("results"):
            loc = data["results"][0]["geometry"]["location"]
            return {"lat": loc["lat"], "lng": loc["lng"]}
    except Exception as e:
        print("  Geocode error: %s" % e)
    return None

def nearby(lat, lng, radius):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {"location": "%s,%s" % (lat, lng), "radius": radius, "key": API_KEY}
    try:
        r = requests.get(url, params=params, timeout=60)
        data = r.json()
        if data.get("status") == "OK":
            return [{
                "place_id": p.get("place_id"),
                "name": p.get("name"),
                "types": p.get("types", []),
                "status": p.get("business_status", "UNKNOWN"),
                "lat": p["geometry"]["location"]["lat"],
                "lng": p["geometry"]["location"]["lng"],
            } for p in data.get("results", [])]
    except Exception as e:
        print("  Nearby error: %s" % e)
    return []

def place_details(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_phone_number,formatted_address,website,types,business_status",
        "key": API_KEY,
    }
    try:
        r = requests.get(url, params=params, timeout=60)
        data = r.json()
        if data.get("status") == "OK":
            rr = data.get("result", {})
            return {
                "name": rr.get("name"),
                "phone": rr.get("formatted_phone_number"),
                "address": rr.get("formatted_address"),
                "website": rr.get("website"),
                "types": rr.get("types", []),
            }
    except Exception as e:
        print("  Details error: %s" % e)
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

def resolve(address):
    result = {
        "input": address, "source": None, "radius": None,
        "distance_m": None, "place_id": None, "status": None,
        "name": None, "phone": None, "address": None,
        "website": None, "types": None,
        "fiber_lat": None, "fiber_lng": None, "error": None
    }
    geo = geocode(address)
    if not geo:
        result["status"] = "GEOCODE_FAILED"
        result["error"] = "Could not geocode"
        return result
    result["fiber_lat"] = geo["lat"]
    result["fiber_lng"] = geo["lng"]
    for radius in RADII:
        cands = nearby(geo["lat"], geo["lng"], radius)
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

def read_input(client, sheet_id, tab):
    ws = client.open_by_key(sheet_id).worksheet(tab)
    records = ws.get_all_records()
    out = []
    for row in records:
        addr = (row.get("Address") or row.get("address") or
                row.get("Street Address") or row.get("Full Address") or
                row.get("Location"))
        if addr and str(addr).strip():
            out.append({"address": str(addr).strip()})
    return out

def get_already_done(client, sheet_id, tab):
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

def write_result(ws, result):
    ws.append_row([
        result.get("input", ""), result.get("source", ""),
        result.get("radius", ""), result.get("distance_m", ""),
        result.get("place_id", ""), result.get("status", ""),
        result.get("name", ""), result.get("phone", ""),
        result.get("address", ""), result.get("website", ""),
        result.get("types", ""), result.get("fiber_lat", ""),
        result.get("fiber_lng", ""),
        datetime.now(timezone.utc).isoformat(),
        result.get("error", "")
    ])

print("\n" + "="*55)
print("  THE MAP MAN v%s - API Resolver (pulls phones)" % VERSION)
print("="*55)
print("Connecting to Google Sheets...")
client = gspread.authorize(Credentials.from_service_account_file(creds_file, scopes=SCOPES))

print("Checking for already-processed addresses...")
already_done = get_already_done(client, SHEET_ID, OUT_TAB)
print("Found %d already processed. Will skip them." % len(already_done))

addresses = read_input(client, SHEET_ID, IN_TAB)
print("Loaded %d total addresses from '%s'" % (len(addresses), IN_TAB))

to_process = [a for a in addresses if a["address"] not in already_done]
print("New addresses to process: %d" % len(to_process))

if not to_process:
    print("Nothing new to process. All done!")
    sys.exit(0)

try:
    out_ws = client.open_by_key(SHEET_ID).worksheet(OUT_TAB)
except gspread.WorksheetNotFound:
    out_ws = client.open_by_key(SHEET_ID).add_worksheet(title=OUT_TAB, rows="1000", cols="20")
init_out(out_ws)

for i, item in enumerate(to_process, 1):
    addr = item["address"]
    print("\n[%d/%d] %s" % (i, len(to_process), addr))
    result = resolve(addr)
    write_result(out_ws, result)
    print("  -> %s | Phone: %s | Distance: %sm" % (
        result["status"], result.get("phone") or "N/A",
        result.get("distance_m") or "N/A"
    ))
    time.sleep(0.2)

print("\nDone! Results in '%s' tab." % OUT_TAB)
