#!/usr/bin/env python3
"""
mapman_api_batch.py - Optimus MapMan (area-search edition, v2.0)
Finds CALLABLE COMMERCIAL businesses inside fiber-eligible ZIPs and writes
their phones to the sheet. Does NOT enrich bare addresses - that returns the
empty lot (proven: address lookups give premise/street_address, no phone).

METHOD (proven live): Places Text Search by business type within each fiber
ZIP -> Place Details for the phone -> keep OPERATIONAL + has phone + commercial
type -> write to 'Fiber Commercial Leads'. Dedupe by phone (place_id kept too),
paginate with next_page_token, loop business types per ZIP.

RUN MODES:
  CLI / Pydroid / HP : python mapman_api_batch.py
  Cloud Run endpoint : gunicorn mapman_api_batch:app   (POST /run, GET /healthz)
"""
import os, time, json
import requests

VERSION = "2.0-area"
API_KEY = os.environ.get("PLACES_API_KEY", "AIzaSyA9PJQJmf1LGFN3lATv8-se3tsIy6kCG9g")
SHEET_ID = "1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA"
SRC_TAB = "Hunter Commercial"
OUT_TAB = "Fiber Commercial Leads"

TYPES = ["restaurant", "store", "car_repair", "contractor", "medical", "dentist",
         "lawyer", "real_estate_agency", "gym", "bank", "hotel", "pharmacy",
         "beauty_salon", "veterinary_care", "electrician", "plumber", "insurance_agency"]
COMMERCIAL = {"establishment", "store", "restaurant", "food", "health", "finance",
              "car_repair", "lawyer", "doctor", "dentist", "gym", "lodging",
              "point_of_interest", "general_contractor", "electrician", "plumber"}

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


def textsearch(q, token=None):
    p = {"pagetoken": token, "key": API_KEY} if token else {"query": q, "key": API_KEY}
    return requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json",
                        params=p, timeout=20).json()


def details(pid):
    p = {"place_id": pid, "key": API_KEY,
         "fields": "name,formatted_phone_number,business_status,types,rating,formatted_address"}
    return requests.get("https://maps.googleapis.com/maps/api/place/details/json",
                        params=p, timeout=20).json().get("result", {})


def worth_calling(d):
    if d.get("business_status") != "OPERATIONAL":
        return False
    if not d.get("formatted_phone_number"):
        return False
    return any(t in COMMERCIAL for t in d.get("types", []))


def fiber_zips(sh):
    """Distinct (zip, 'City ST') pulled from the Hunter Commercial tab."""
    vals = sh.worksheet(SRC_TAB).get_all_values()
    out, seen = [], set()
    for r in vals[1:]:
        if len(r) < 5:
            continue
        city, state, zc = r[2].strip(), r[3].strip(), r[4].strip()
        if zc and zc not in seen:
            seen.add(zc)
            out.append((zc, ("%s %s" % (city, state)).strip()))
    return out


def enrich(zips=None, limit_types=None):
    sh = _sheet()
    try:
        ws = sh.worksheet(OUT_TAB)
    except Exception:
        ws = sh.add_worksheet(OUT_TAB, 2000, 9)
        ws.append_row(["Business", "Phone", "Type", "Rating", "Address",
                       "Zip", "PlaceId", "Status", "Source"])
    existing = ws.get_all_values()[1:]
    seen_phone = set(r[1] for r in existing if len(r) > 1 and r[1])
    seen_pid = set(r[6] for r in existing if len(r) > 6 and r[6])
    zips = zips or fiber_zips(sh)
    types = limit_types or TYPES
    added = 0
    for zc, zq in zips:
        rows = []
        for t in types:
            token = None
            for _ in range(3):
                r = textsearch("%s in %s %s" % (t, zq, zc), token)
                for c in r.get("results", []):
                    pid = c.get("place_id", "")
                    if not pid or pid in seen_pid:
                        continue
                    d = details(pid)
                    time.sleep(0.1)
                    ph = d.get("formatted_phone_number", "")
                    if worth_calling(d) and ph not in seen_phone:
                        seen_phone.add(ph)
                        seen_pid.add(pid)
                        rows.append([d.get("name", ""), ph, t, d.get("rating", ""),
                                     d.get("formatted_address", ""), zc, pid,
                                     d.get("business_status", ""), "Places area"])
                token = r.get("next_page_token")
                if not token:
                    break
                time.sleep(2)
        if rows:
            ws.append_rows(rows)
            added += len(rows)
            print("ZIP %s: +%d leads" % (zc, len(rows)))
    print("DONE. %d new callable leads -> %s" % (added, OUT_TAB))
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
        zips = None
        if body.get("zip"):
            zips = [(str(body["zip"]), body.get("area", ""))]
        try:
            n = enrich(zips=zips)
            return jsonify({"ok": True, "added": n})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 200
except Exception:
    app = None


if __name__ == "__main__":
    enrich()
