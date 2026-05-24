#!/usr/bin/env python3
"""
mapman_api_batch.py - Optimus MapMan (v3.1, tenant-resolver, nearest-match)

PRIMARY (precision) workflow - this is the product:
  fiber-serviceable address  ->  geocode to coordinates  ->  nearby search at
  a SMALL radius  ->  NEAREST operating commercial tenant to the point  ->
  Place Details  ->  phone  ->  write lead. If no commercial tenant is
  operating at/near the point, the address is residential/vacant -> SKIP.

  Why nearest: a small-radius search still returns businesses across the
  street. We sort candidates by distance from the fiber coordinate and take
  the closest OPERATIONAL commercial one - that is the actual tenant.

  Why coordinates: Google resolves a bare address string to the PARCEL, not
  the tenant. Resolve by COORDINATE + tight radius instead. (Patrick+ChatGPT.)

FALLBACK (area lead-gen, NOT the product): businesses by type in a fiber ZIP.
  Clearly labeled Source='Area fallback' so hit rates can be compared.

RUN MODES:
  CLI / Pydroid / HP : python mapman_api_batch.py
  Cloud Run endpoint : gunicorn mapman_api_batch:app
      POST /run                 -> precision over all Hunter Commercial rows
      POST /run {"addr":"..."}  -> precision for ONE address (returns the lead)
      POST /run_area {"zip":"39564","area":"Ocean Springs MS"} -> fallback
      GET  /healthz
"""
import os, time, json, math
import requests

VERSION = "3.1-tenant-resolver-nearest"
API_KEY = os.environ.get("PLACES_API_KEY", "AIzaSyA9PJQJmf1LGFN3lATv8-se3tsIy6kCG9g")
SHEET_ID = "1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA"
SRC_TAB = "Hunter Commercial"
OUT_TAB = "Fiber Commercial Leads"
RADIUS_M = 55          # tight radius: tenant AT the point, not the neighborhood
MAX_TENANT_M = 35      # accept tenant only if within this distance of the coordinate

COMMERCIAL = {"establishment", "store", "restaurant", "food", "health", "finance",
              "car_repair", "lawyer", "doctor", "dentist", "gym", "lodging",
              "point_of_interest", "general_contractor", "electrician", "plumber",
              "real_estate_agency", "insurance_agency", "beauty_salon", "bank",
              "pharmacy", "veterinary_care", "bakery", "bar", "school"}
NON_TENANT = {"premise", "street_address", "subpremise", "route", "locality",
              "political", "postal_code", "geocode"}

AREA_TYPES = ["restaurant", "store", "car_repair", "contractor", "medical",
              "dentist", "lawyer", "real_estate_agency", "gym", "bank", "hotel",
              "pharmacy", "beauty_salon", "veterinary_care", "electrician", "plumber"]

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
    """Approximate meters between two lat/lng points (haversine)."""
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


def nearby(lat, lng):
    """establishments operating at this coordinate (tight radius)."""
    r = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json",
                     params={"location": "%s,%s" % (lat, lng), "radius": RADIUS_M,
                             "key": API_KEY}, timeout=20).json()
    return r.get("results") or []


def details(pid):
    p = {"place_id": pid, "key": API_KEY,
         "fields": "name,formatted_phone_number,business_status,types,rating,formatted_address"}
    return requests.get("https://maps.googleapis.com/maps/api/place/details/json",
                        params=p, timeout=20).json().get("result", {})


def is_commercial(types):
    return any(t in COMMERCIAL for t in types)


def tenant_at(addr):
    """PRECISION resolver: the NEAREST operating commercial tenant to a fiber
    address, with phone. Returns a lead dict, or None if residential/vacant."""
    geo = geocode(addr)
    if not geo:
        return None
    lat, lng = geo

    # keep only commercial candidates, tag each with distance from the point
    scored = []
    for c in nearby(lat, lng):
        types = c.get("types", [])
        if not is_commercial(types):
            continue
        if any(t in NON_TENANT for t in types) and not is_commercial(types):
            continue
        if c.get("business_status") and c.get("business_status") != "OPERATIONAL":
            continue
        cl = c.get("geometry", {}).get("location", {})
        if "lat" not in cl or "lng" not in cl:
            continue
        dist = _dist_m(lat, lng, cl["lat"], cl["lng"])
        scored.append((dist, c))

    # NEAREST first - that is the tenant at this address, not across the street
    scored.sort(key=lambda x: x[0])

    for dist, c in scored:
        if dist > MAX_TENANT_M:
            break  # nearest commercial is too far -> no tenant at this address
        d = details(c["place_id"])
        time.sleep(0.1)
        ph = d.get("formatted_phone_number", "")
        if d.get("business_status", "OPERATIONAL") == "OPERATIONAL" and ph:
            return {"biz": d.get("name", ""), "phone": ph,
                    "type": (d.get("types", [""])[0] if d.get("types") else ""),
                    "rating": d.get("rating", ""), "matched": d.get("formatted_address", ""),
                    "status": d.get("business_status", ""), "dist_m": round(dist)}
    return None


def _open_out(sh):
    try:
        return sh.worksheet(OUT_TAB)
    except Exception:
        ws = sh.add_worksheet(OUT_TAB, 4000, 11)
        ws.append_row(["Business", "Phone", "Type", "Rating", "FiberAddress",
                       "MatchedAddress", "Zip", "DistM", "Status", "Source", "AddedAt"])
        return ws


def enrich(addr=None):
    """Precision run. addr=one address -> returns that lead. else all Hunter
    Commercial rows -> writes leads to the sheet."""
    sh = _sheet()
    ws = _open_out(sh)
    existing = ws.get_all_values()[1:]
    seen = set(r[1] for r in existing if len(r) > 1 and r[1])
    now = time.strftime("%Y-%m-%d %H:%M")

    if addr:
        lead = tenant_at(addr)
        if lead and lead["phone"] not in seen:
            ws.append_row([lead["biz"], lead["phone"], lead["type"], lead["rating"],
                           addr, lead["matched"], "", lead["dist_m"], lead["status"],
                           "Tenant resolver", now])
        return lead

    rows = sh.worksheet(SRC_TAB).get_all_values()
    added = 0
    batch = []
    for r in rows[1:]:
        if len(r) < 5 or not r[0].strip():
            continue
        full = "%s, %s, %s %s" % (r[0].strip(), r[2].strip(), r[3].strip(), r[4].strip())
        lead = tenant_at(full)
        if lead and lead["phone"] not in seen:
            seen.add(lead["phone"])
            batch.append([lead["biz"], lead["phone"], lead["type"], lead["rating"],
                          full, lead["matched"], r[4].strip(), lead["dist_m"],
                          lead["status"], "Tenant resolver", now])
            if len(batch) >= 20:
                ws.append_rows(batch); added += len(batch); batch = []
                print("  +%d leads (running)" % added)
        time.sleep(0.1)
    if batch:
        ws.append_rows(batch); added += len(batch)
    print("DONE. %d callable tenants at fiber addresses -> %s" % (added, OUT_TAB))
    return added


def enrich_area(zip_code, area):
    """FALLBACK only: businesses by type in a fiber ZIP. Source='Area fallback'."""
    sh = _sheet()
    ws = _open_out(sh)
    existing = ws.get_all_values()[1:]
    seen = set(r[1] for r in existing if len(r) > 1 and r[1])
    now = time.strftime("%Y-%m-%d %H:%M")
    added = 0
    for t in AREA_TYPES:
        token = None
        for _ in range(3):
            p = {"pagetoken": token, "key": API_KEY} if token else {
                "query": "%s in %s %s" % (t, area, zip_code), "key": API_KEY}
            r = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json",
                             params=p, timeout=20).json()
            for c in r.get("results", []):
                d = details(c.get("place_id", "")); time.sleep(0.1)
                ph = d.get("formatted_phone_number", "")
                if d.get("business_status") == "OPERATIONAL" and ph and ph not in seen and is_commercial(d.get("types", [])):
                    seen.add(ph)
                    ws.append_row([d.get("name", ""), ph, t, d.get("rating", ""), "",
                                   d.get("formatted_address", ""), zip_code, "",
                                   d.get("business_status", ""), "Area fallback", now])
                    added += 1
            token = r.get("next_page_token")
            if not token:
                break
            time.sleep(2)
    print("DONE (fallback). %d area leads -> %s" % (added, OUT_TAB))
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
            res = enrich(addr=body.get("addr"))
            return jsonify({"ok": True, "result": res})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 200

    @app.route("/run_area", methods=["POST"])
    def _run_area():
        body = request.get_json(silent=True) or {}
        try:
            n = enrich_area(str(body.get("zip", "")), body.get("area", ""))
            return jsonify({"ok": True, "added": n})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 200
except Exception:
    app = None


if __name__ == "__main__":
    enrich()
