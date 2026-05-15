import csv, requests, time, os

VERSION = "1.4"
API_KEY = "AIzaSyA9PJQJmf1LGFN3lATv8-se3tsIy6kCG9g"
INPUT  = "enrich_queue.csv"
OUTPUT = "enrich_queue_filled.csv"
BATCH_ORDER = ["HOUSTON_DT", "AUSTIN", "LOUISIANA", "EDMOND"]

COMMERCIAL_TYPES = {
    "restaurant","cafe","store","shopping_mall","supermarket","gas_station",
    "car_repair","car_dealer","hospital","doctor","dentist","pharmacy",
    "bank","atm","hotel","gym","spa","beauty_salon","hair_care",
    "clothing_store","electronics_store","furniture_store","hardware_store",
    "jewelry_store","shoe_store","book_store","department_store","florist",
    "pet_store","real_estate_agency","insurance_agency","lawyer","accountant",
    "travel_agency","electrician","plumber","roofing_contractor",
    "general_contractor","moving_company","locksmith","painter",
    "car_wash","car_rental","movie_theater","casino","bowling_alley",
    "amusement_park","art_gallery","museum","night_club","bar",
    "liquor_store","bakery","school","university","library","fire_station",
    "police","post_office","courthouse","church","mosque","synagogue",
    "cemetery","funeral_home","laundry","storage","veterinary_care"
}

def find_place(addr, city, state):
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {"input": f"{addr}, {city}, {state}", "inputtype": "textquery",
              "fields": "place_id,name,types,business_status", "key": API_KEY}
    try:
        r = requests.get(url, params=params, timeout=10).json()
        if r.get("status") != "OK":
            print(f"  >>> {r.get('status')} {r.get('error_message','')}")
            return None
        return r["candidates"][0] if r.get("candidates") else None
    except Exception as e:
        print(f"  ERR: {e}")
        return None

def get_details(pid):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {"place_id": pid, "fields": "formatted_phone_number,business_status", "key": API_KEY}
    try:
        r = requests.get(url, params=params, timeout=10).json()
        return r.get("result", {}) if r.get("status") == "OK" else {}
    except Exception:
        return {}

def main():
    print(f"\nMAPMAN ENRICHMENT v{VERSION}\n")
    if not os.path.exists(INPUT):
        print(f"ERROR: {INPUT} not found in {os.getcwd()}")
        print("Put enrich_queue.csv in this folder, then run again.")
        input("Press Enter to close...")
        return

    with open(INPUT, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        print("Empty input")
        input("Press Enter to close...")
        return

    extra_cols = ["verified_biz", "verified_types", "verified_phone", "verdict"]
    fieldnames = list(rows[0].keys())
    for c in extra_cols:
        if c not in fieldnames:
            fieldnames.append(c)

    def keyof(r):
        return f"{r.get('address','') or r.get('Address','')}|{r.get('city','') or r.get('City','')}|{r.get('state','') or r.get('State','')}"

    done = set()
    if os.path.exists(OUTPUT):
        try:
            with open(OUTPUT, newline="", encoding="utf-8-sig") as fh:
                for r in csv.DictReader(fh):
                    if r.get("verdict"):
                        done.add(keyof(r))
            print(f"RESUME: skipping {len(done)} done rows")
        except Exception as e:
            print(f"  resume err: {e}")

    if "batch" in rows[0]:
        rows.sort(key=lambda r: BATCH_ORDER.index(r.get("batch","")) if r.get("batch","") in BATCH_ORDER else 99)

    remaining = [r for r in rows if keyof(r) not in done]
    print(f"Total: {len(rows)} | Done: {len(done)} | Remaining: {len(remaining)}\n")

    if not remaining:
        input("Nothing remaining. Press Enter to close...")
        return

    mode = "a" if done else "w"
    with open(OUTPUT, mode, newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if not done:
            w.writeheader()

        for i, row in enumerate(remaining, 1):
            for c in extra_cols:
                row.setdefault(c, "")

            addr  = (row.get("address") or row.get("Address") or "").strip()
            city  = (row.get("city") or row.get("City") or "").strip()
            state = (row.get("state") or row.get("State") or "").strip()

            if not addr:
                row["verdict"] = "SKIP_NO_ADDRESS"
                w.writerow(row); f.flush()
                print(f"[{i}/{len(remaining)}] (no address) -> SKIP")
                continue

            result = find_place(addr, city, state)
            if not result:
                row["verdict"] = "NOT_FOUND"
            else:
                types = result.get("types", [])
                row["verified_biz"] = result.get("name", "")
                row["verified_types"] = "|".join(types[:5])
                if any(t in COMMERCIAL_TYPES for t in types):
                    d = get_details(result["place_id"])
                    status = d.get("business_status", "OPERATIONAL")
                    if status != "OPERATIONAL":
                        row["verdict"] = f"CLOSED ({status})"
                    else:
                        row["verified_phone"] = d.get("formatted_phone_number", "")
                        row["verdict"] = "COMMERCIAL_VERIFIED" if row["verified_phone"] else "COMMERCIAL_NO_PHONE"
                else:
                    row["verdict"] = "RESIDENTIAL_OR_OTHER"

            w.writerow(row); f.flush()
            print(f"[{i}/{len(remaining)}] {row.get('batch',''):10} {addr[:30]:30} -> {row['verdict']:22} {row.get('verified_biz','')[:25]}")
            time.sleep(0.05)

    print(f"\nDONE. See {OUTPUT}")
    input("Press Enter to close...")

if __name__ == "__main__":
    main()
