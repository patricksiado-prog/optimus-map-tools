#!/usr/bin/env python3
"""
mapman_api_batch.py - Optimus MapMan (v3.2, tenant-resolver)

PRIMARY (precision) workflow - this is the product:
  fiber-serviceable address -> geocode to coordinates -> nearby search at a
  SMALL radius -> NEAREST operating commercial tenant to the point -> Place
  Details -> phone -> write lead. If no commercial tenant with a phone is
  operating near the point, the address is residential/vacant -> SKIP.

  Radius cascade 30 -> 60 -> 100m: take the nearest qualifying tenant at the
  tightest radius that produces one. Tighter = more confident it is THE tenant.

  Why coordinates: Google resolves a bare address string to the PARCEL, not the
  tenant. Resolve by COORDINATE + tight radius instead. (Proven live.)

FALLBACK (area lead-gen, NOT the product): nearest commercial business to a ZIP
  center. DEFAULT OFF. Rows are clearly labeled Source='Area fallback' so they
  are never confused with address-precise leads. Turn on only deliberately.

RUN MODES:
  CLI / Pydroid / HP : python mapman_api_batch.py            (fallback OFF)
                       python mapman_api_batch.py --fallback (fallback ON)
  Cloud Run endpoint : gunicorn mapman_api_batch:app
      POST /run                          -> precision, all Hunter Commercial rows
      POST /run {"addr":"..."}           -> precision for ONE address
      POST /run {"fallback":true}        -> precision + area fallback on misses
      GET  /healthz
"""
import os, re, json, time, math
import requests

VERSION = "3.2-tenant-resolver"

# ---- production defaults (override via env) ----
API_KEY = os.environ.get("PLACES_API_KEY", "AIzaSyA9PJQJmf1LGFN3lATv8-se3tsIy6kCG9g")
SHEET_ID = os.environ.get("MAP_SHEET_ID", "1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA")
SRC_TAB = os.environ.get("MAP_INPUT_TAB", "Hunter Commercial")
OUT_TAB = os.environ.get("MAP_OUTPUT_TAB", "Fiber Commercial Leads")

RADII = [30, 60, 100]      # tight-first cascade; nearest qualifying tenant wins
MAX_TENANT_M = 60          # never accept a match farther than this from the point
FALLBACK_RADIUS_M = 4000   # area fallback search radius around ZIP center

# Tightened to REAL callable businesses. No parks, transit, cemeteries,
# airports, parking, places of worship, government, etc.
COMMERCIAL = {
    "store", "restaurant", "food", "cafe", "bakery", "bar", "meal_takeaway",
    "meal_delivery", "supermarket", "grocery_or_supermarket", "convenience_store",
    "liquor_store", "clothing_store", "electronics_store", "furniture_store",
    "hardware_store", "home_goods_store", "jewelry_store", "shoe_store",
    "book_store", "pet_store", "bicycle_store", "car_dealer", "car_repair",
    "car_wash", "gas_station", "doctor", "dentist", "pharmacy", "physiotherapist",
    "veterinary_care", "gym", "spa", "beauty_salon", "hair_care", "lodging",
    "finance", "insurance_agency", "lawyer", "real_estate_agency", "travel_agency",
    "accounting", "bank", "plumber", "electrician", "roofing_contractor",
    "general_contractor", "painter", "locksmith", "moving_company", "storage",
    "laundry", "night_club",
}
# generic types that are not, by themselves, a callable commercial tenant
GENERIC = {"point_of_interest", "establishment"}
# hard reject - never a sales lead even if tagged establishment/POI
NON_TENANT = {
    "premise", "street_address", "subpremise", "route", "locality", "political",
    "postal_code", "geocode", "park", "parking", "transit_station", "train_station",
    "subway_station", "bus_station", "light_rail_station", "taxi_stand", "airport",
    "cemetery", "church", "mosque", "synagogue", "hindu_temple", "place_of_worship",
    "city_hall", "courthouse", "embassy", "local_government_office", "police",
    "fire_station", "post_office", "school", "university", "library", "campground",
    "rv_park", "natural_feature",
}

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CRED_PATHS = ["google_creds.json",
              "/storage/emulated/0/Download/google_creds.json",
              os.path.expanduser("~/google_creds.json"),
              "C:/Users/patri/Desktop/google_creds.json"]


def _creds():
    from google.oauth2.service_account import Credentials
    env = os.environ.get("GOOGLE_CREDS_JSON")
    if env:
        return Credentials.from_service_account_info(json.loads(env), scopes=SCOPES)
    for p in CRED_PATHS:
        if os.path.exists(p):
            return Credentials.from_service_account_file(p, scopes=SCOPES)
    raise RuntimeError("google_creds.json not found in any known path")


def _sheet():
    import gspread
    return gspread.authorize(_creds()).open_by_key(SHEET_ID)


def _dist_m(lat1, lng1, lat2, lng2):
    """Meters between two lat/lng points (haversine)."""
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def geocode(addr):
    """address -> (lat, lng) or None."""
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json",
                     params={"address": addr, "key": API_KEY}, timeout=20).json()
    res = r.get("results") or []
    if not res:
        return None
    loc = res[0].get("geometry", {}).get("location", {})
    if "lat" in loc and "lng" in loc:
        return loc["lat"], loc["lng"]
    return None


def nearby(lat, lng, radius):
    r = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json",
                     params={"location": "%s,%s" % (lat, lng), "radius": radius,
                             "key": API_KEY}, timeout=20).json()
    return r.get("results") or []


def details(pid):
    p = {"place_id": pid, "key": API_KEY,
         "fields": "name,formatted_phone_number,business_status,types,rating,formatted_address,website"}
    return requests.get("https://maps.googleapis.com/maps/api/place/details/json",
                        params=p, timeout=20).json().get("result", {})


def is_commercial(types):
    """Real callable business: a concrete commercial type, and not a hard-reject."""
    if any(t in NON_TENANT for t in types):
        return False
    return any(t in COMMERCIAL for t in types)


def has_phone(ph):
    return bool(ph) and len(re.sub(r"\D", "", ph)) >= 7


def _lead_from_details(d, dist, source, fiber_addr, zip_code):
    return {
        "biz": d.get("name", ""),
        "phone": d.get("formatted_phone_number", ""),
        "type": (d.get("types", [""])[0] if d.get("types") else ""),
        "rating": d.get("rating", ""),
        "matched": d.get("formatted_address", ""),
        "website": d.get("website", ""),
        "status": d.get("business_status", ""),
        "dist_m": (round(dist) if dist is not None else ""),
        "source": source,
        "fiber_addr": fiber_addr,
        "zip": zip_code,
    }


def tenant_at(addr):
    """PRECISION: nearest operating commercial tenant (with phone) to a fiber
    address. Cascades 30->60->100m, tightest first. None if residential/vacant."""
    geo = geocode(addr)
    if not geo:
        return None
    lat, lng = geo

    for radius in RADII:
        scored = []
        for c in nearby(lat, lng, radius):
            types = c.get("types", [])
            if not is_commercial(types):
                continue
            if c.get("business_status") and c.get("business_status") != "OPERATIONAL":
                continue
            cl = c.get("geometry", {}).get("location", {})
            if "lat" not in cl or "lng" not in cl:
                continue
            dist = _dist_m(lat, lng, cl["lat"], cl["lng"])
            if dist > MAX_TENANT_M:
                continue
            scored.append((dist, c))
        scored.sort(key=lambda x: x[0])     # NEAREST first = the tenant
        for dist, c in scored:
            d = details(c["place_id"])
            time.sleep(0.1)
            if d.get("business_status", "OPERATIONAL") == "OPERATIONAL" and has_phone(d.get("formatted_phone_number")):
                return _lead_from_details(d, dist, "Tenant resolver", addr, "")
    return None


def area_fallback(addr, zip_code=""):
    """FALLBACK only (off by default): nearest operating commercial business to
    the ZIP center. Source='Area fallback'. NOT address-precise."""
    if not zip_code:
        m = re.search(r"\b\d{5}(?:-\d{4})?\b", addr)
        zip_code = m.group(0) if m else ""
    if not zip_code:
        return None
    geo = geocode(zip_code)
    if not geo:
        return None
    lat, lng = geo
    scored = []
    for c in nearby(lat, lng, FALLBACK_RADIUS_M):
        types = c.get("types", [])
        if not is_commercial(types):
            continue
        if c.get("business_status") and c.get("business_status") != "OPERATIONAL":
            continue
        cl = c.get("geometry", {}).get("location", {})
        if "lat" not in cl or "lng" not in cl:
            continue
        scored.append((_dist_m(lat, lng, cl["lat"], cl["lng"]), c))
    scored.sort(key=lambda x: x[0])
    for dist, c in scored:
        d = details(c["place_id"])
        time.sleep(0.1)
        if d.get("business_status", "OPERATIONAL") == "OPERATIONAL" and has_phone(d.get("formatted_phone_number")):
            return _lead_from_details(d, dist, "Area fallback", addr, zip_code)
    return None


def _open_out(sh):
    try:
        return sh.worksheet(OUT_TAB)
    except Exception:
        ws = sh.add_worksheet(OUT_TAB, 4000, 12)
        ws.append_row(["Business", "Phone", "Type", "Rating", "FiberAddress",
                       "MatchedAddress", "Zip", "DistM", "Status", "Website",
                       "Source", "AddedAt"])
        return ws


def _row(lead, now):
    return [lead["biz"], lead["phone"], lead["type"], lead["rating"],
            lead["fiber_addr"], lead["matched"], lead["zip"], lead["dist_m"],
            lead["status"], lead["website"], lead["source"], now]


def enrich(addr=None, fallback=False):
    """Precision run. addr=one address -> returns that lead. else all Hunter
    Commercial rows -> writes leads to the sheet. fallback=True only adds an
    'Area fallback' row when the precise resolver misses."""
    sh = _sheet()
    ws = _open_out(sh)
    existing = ws.get_all_values()[1:]
    seen = set(r[1] for r in existing if len(r) > 1 and r[1])
    now = time.strftime("%Y-%m-%d %H:%M")

    if addr:
        lead = tenant_at(addr) or (area_fallback(addr) if fallback else None)
        if lead and lead["phone"] not in seen:
            ws.append_row(_row(lead, now))
        return lead

    rows = sh.worksheet(SRC_TAB).get_all_values()
    added = 0
    batch = []
    for r in rows[1:]:
        if len(r) < 5 or not r[0].strip():
            continue
        full = "%s, %s, %s %s" % (r[0].strip(), r[2].strip(), r[3].strip(), r[4].strip())
        lead = tenant_at(full)
        if not lead and fallback:
            lead = area_fallback(full, r[4].strip())
        if lead and lead["phone"] not in seen:
            seen.add(lead["phone"])
            lead["zip"] = lead["zip"] or r[4].strip()
            batch.append(_row(lead, now))
            if len(batch) >= 20:
                ws.append_rows(batch); added += len(batch); batch = []
                print("  +%d leads (running)" % added)
        time.sleep(0.1)
    if batch:
        ws.append_rows(batch); added += len(batch)
    print("DONE. %d callable tenants -> %s" % (added, OUT_TAB))
    return added


try:
    from flask import Flask, request, jsonify
    app = Flask(__name__)

    @app.route("/healthz")
    def _h():
        return jsonify({"ok": True, "version": VERSION})

    @app.route("/run", methods=["POST", "GET"])
    def _run():
        body = request.get_json(silent=True) or {}
        try:
            res = enrich(addr=body.get("addr"), fallback=bool(body.get("fallback", False)))
            return jsonify({"ok": True, "result": res})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 200
except Exception:
    app = None


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="MapMan v3.2 tenant resolver")
    ap.add_argument("--addr", default=None, help="resolve a single address")
    ap.add_argument("--fallback", action="store_true", help="enable area fallback on misses (default OFF)")
    a = ap.parse_args()
    print(enrich(addr=a.addr, fallback=a.fallback))
