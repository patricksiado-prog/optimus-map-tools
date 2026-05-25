#!/usr/bin/env python3
"""
THE MAP MAN v10.24.0 API Resolver
"""
import os, re, json, time, math, argparse
import requests

VERSION = "10.24.0-api-resolver"
API_KEY = "AIzaSyA9PJQJmf1LGFN3lATv8-se3tsIy6kCG9g"
SHEET_ID = "1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA"
SRC_TAB = "Hunter Commercial"
OUT_TAB = "Fiber Commercial Leads"

CITIES = {
    "1": ("Biloxi", "Biloxi"),
    "2": ("D'Iberville", "D'Iberville"),
    "3": ("Gulfport", "Gulfport"),
    "4": ("Ocean Springs", "Ocean Springs"),
    "5": ("Long Beach", "Long Beach"),
}

RADII = [30, 60, 100]
MAX_TENANT_M = 60

COMMERCIAL = {
    "store","restaurant","food","cafe","bakery","bar","meal_takeaway",
    "meal_delivery","supermarket","grocery_or_supermarket","convenience_store",
    "liquor_store","clothing_store","electronics_store","furniture_store",
    "hardware_store","home_goods_store","jewelry_store","shoe_store",
    "book_store","pet_store","bicycle_store","car_dealer","car_repair",
    "car_wash","gas_station","doctor","dentist","pharmacy","physiotherapist",
    "veterinary_care","gym","spa","beauty_salon","hair_care","lodging",
    "finance","insurance_agency","lawyer","real_estate_agency","travel_agency",
    "accounting","bank","plumber","electrician","roofing_contractor",
    "general_contractor","painter","locksmith","moving_company","storage",
    "laundry","night_club",
}
NON_TENANT = {
    "premise","street_address","subpremise","route","locality","political",
    "postal_code","geocode","park","parking","transit_station","train_station",
    "subway_station","bus_station","light_rail_station","taxi_stand","airport",
    "cemetery","church","mosque","synagogue","hindu_temple","place_of_worship",
    "city_hall","courthouse","embassy","local_government_office","police",
    "fire_station","post_office","school","university","library","campground",
    "rv_park","natural_feature",
}

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CRED_PATHS = [
    "google_creds.json",
    "/storage/emulated/0/Download/google_creds.json",
    "/storage/emulated/0/Documents/google_creds.json",
    os.path.expanduser("~/google_creds.json"),
]

def _creds():
    from google.oauth2.service_account import Credentials
    env = os.environ.get("GOOGLE_CREDS_JSON")
    if env:
        return Credentials.from_service_account_info(json.loads(env), scopes=SCOPES)
    for p in CRED_PATHS:
        if os.path.exists(p):
            return Credentials.from_service_account_file(p, scopes=SCOPES)
    raise RuntimeError("google_creds.json not found")

def _sheet():
    import gspread
    return gspread.authorize(_creds()).open_by_key(SHEET_ID)

def _dist_m(lat1, lng1, lat2, lng2):
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def geocode(addr):
    r = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json",
                     params={"query": addr, "key": API_KEY}, timeout=20).json()
    res = r.get("results") or []
    if not res:
        return None
    loc = res[0].get("geometry", {}).get("location", {})
    if "lat" in loc and "lng" in loc:
        return loc["lat"], loc["lng"]
    return None

def nearby(lat, lng, radius):
    r = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json",
                     params={"location": f"{lat},{lng}", "radius": radius, "key": API_KEY}, timeout=20).json()
    return r.get("results") or []

def details(pid):
    p = {"place_id": pid, "key": API_KEY,
         "fields": "name,formatted_phone_number,business_status,types,rating,formatted_address,website"}
    r = requests.get("https://maps.googleapis.com/maps/api/place/details/json", params=p, timeout=20).json()
    return r.get("result", {})

def is_commercial(types):
    if any(t in NON_TENANT for t in types):
        return False
    return any(t in COMMERCIAL for t in types)

def has_phone(ph):
    return bool(ph) and len(re.sub(r"\D", "", ph)) >= 7

def _lead(d, dist, source, fiber_addr, zip_code):
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
        scored.sort(key=lambda x: x[0])
        for dist, c in scored:
            d = details(c["place_id"])
            time.sleep(0.1)
            if d.get("business_status", "OPERATIONAL") == "OPERATIONAL" and has_phone(d.get("formatted_phone_number")):
                return _lead(d, dist, "Tenant resolver", addr, "")
    return None

def _open_out(sh):
    try:
        return sh.worksheet(OUT_TAB)
    except Exception:
        ws = sh.add_worksheet(OUT_TAB, 4000, 12)
        ws.append_row(["Business","Phone","Type","Rating","FiberAddress",
                       "MatchedAddress","Zip","DistM","Status","Website","Source","AddedAt"])
        return ws

def _row(lead, now):
    return [lead["biz"], lead["phone"], lead["type"], lead["rating"],
            lead["fiber_addr"], lead["matched"], lead["zip"], lead["dist_m"],
            lead["status"], lead["website"], lead["source"], now]

def enrich_city(city_name, fallback=False):
    sh = _sheet()
    ws = _open_out(sh)
    existing = ws.get_all_values()[1:]
    seen = set(r[1] for r in existing if len(r) > 1 and r[1])
    now = time.strftime("%Y-%m-%d %H:%M")

    rows = sh.worksheet(SRC_TAB).get_all_values()
    added = 0
    batch = []

    for r in rows[1:]:
        if len(r) < 5 or not r[0].strip():
            continue
        full = f"{r[0].strip()}, {r[2].strip()}, {r[3].strip()} {r[4].strip()}"
        if city_name and city_name.lower() not in full.lower():
            continue

        lead = tenant_at(full)
        if lead and lead["phone"] not in seen:
            seen.add(lead["phone"])
            lead["zip"] = lead["zip"] or r[4].strip()
            batch.append(_row(lead, now))
            if len(batch) >= 20:
                ws.append_rows(batch)
                added += len(batch)
                batch = []
                print(f"  +{added} leads")
        time.sleep(0.1)

    if batch:
        ws.append_rows(batch)
        added += len(batch)
    
    print(f"\n✅ DONE. {added} callable tenants -> {OUT_TAB}")
    return added

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--addr", default=None)
    parser.add_argument("--city", default=None)
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    if args.addr:
        lead = tenant_at(args.addr)
        print(lead)
    elif args.all:
        for _, (name, _) in CITIES.items():
            print(f"\n--- {name} ---")
            enrich_city(name)
    elif args.city:
        enrich_city(args.city)
    else:
        print("Pick: --all, --city NAME, or --addr ADDRESS")
