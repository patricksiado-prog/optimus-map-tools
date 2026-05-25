#!/usr/bin/env python3
"""
optimus_config.py - Shared config for all Optimus tools
Unified tab structure and helper functions
"""

VERSION = "2025.05.25"

# UNIFIED TAB STRUCTURE - all 3 programs use these
TABS = {
    "Hunter Leads": [
        "Address", "Business Name", "Dot Type", "Property Type",
        "City", "State", "Zip", "Zone", "Instance", "Scan #",
        "Status", "Rep", "Date", "Phone", "Lat", "Lng",
        "Verified Color", "Dot Confidence", "Source Screenshot", "Scan Status",
    ],
    "Hunter Green Commercial": [
        "Address", "Business Name", "City", "State", "Zip",
        "Zone", "Instance", "Scan #", "Date", "Phone", "Lat", "Lng",
        "Verified Color",
    ],
    "Hunter Green Residential": [
        "Address", "City", "State", "Zip",
        "Zone", "Instance", "Scan #", "Date", "Lat", "Lng",
        "Verified Color",
    ],
    "Hunter Commercial": [
        "Address", "Business Name", "Dot Type", "City", "State", "Zip",
        "Zone", "Instance", "Scan #", "Status", "Rep", "Date", "Phone", "Notes",
        "Verified Color",
    ],
    "Hunter Residential": [
        "Address", "Dot Type", "City", "State", "Zip",
        "Zone", "Instance", "Scan #", "Status", "Rep", "Date",
        "Verified Color",
    ],
    "Hunter Hot Zones": [
        "Date", "Zone", "City", "Instance", "Change", "Details",
        "Scan #", "Action",
    ],
    "Hunter Changes": [
        "Date", "Address", "Change", "Details", "Zone", "City",
        "Instance", "Scan #",
    ],
    "Fiber Commercial Leads": [
        "Input Address", "Source", "Resolver Radius", "Resolver Distance Meters",
        "Place ID", "Resolver Status", "Tenant Name", "Tenant Phone",
        "Tenant Address", "Tenant Website", "Tenant Types",
        "Fiber Lat", "Fiber Lng", "Processed At", "Error",
    ],
}

# Unified write function - all programs use this
def init_tabs(client, sheet_name_or_id):
    """Initialize all tabs with correct headers"""
    try:
        ss = client.open_by_key(sheet_name_or_id)
    except:
        ss = client.open(sheet_name_or_id)
    
    existing = [ws.title for ws in ss.worksheets()]
    tabs = {}
    
    for tname, headers in TABS.items():
        if tname not in existing:
            ws = ss.add_worksheet(title=tname, rows=1000, cols=max(20, len(headers)))
            ws.append_row(headers)
        else:
            ws = ss.worksheet(tname)
            # Check/update headers
            try:
                current = ws.row_values(1)
                if len(current) < len(headers):
                    new_cols = headers[len(current):]
                    full_row = list(current) + new_cols
                    ws.update(values=[full_row], range_name="A1")
            except:
                pass
        tabs[tname] = ws
    
    return tabs

# Unified dedup - all programs use this
def get_existing(tabs):
    """Get all existing addresses from Hunter Leads"""
    existing = {}
    if not tabs or "Hunter Leads" not in tabs:
        return existing
    try:
        vals = tabs["Hunter Leads"].get_all_values()
        if not vals:
            return existing
        header = vals[0]
        try:
            vc_idx = header.index("Verified Color")
        except ValueError:
            vc_idx = -1
        for row in vals[1:]:
            if not row or not row[0]:
                continue
            addr = row[0].strip()
            if vc_idx >= 0 and vc_idx < len(row) and row[vc_idx].strip():
                vc = row[vc_idx].strip().lower()
                if vc == "green":
                    dot = "FIBER ELIGIBLE (Green)"
                elif vc == "gold":
                    dot = "UPGRADE ELIGIBLE (Gold/Orange)"
                elif vc in ("grey", "gray"):
                    dot = "EXISTING FIBER (Grey)"
                else:
                    dot = row[2].strip() if len(row) > 2 else ""
            else:
                dot = row[2].strip() if len(row) > 2 else ""
            existing.setdefault(addr, set()).add(dot)
    except Exception as e:
        print(f"  get_existing warn: {e}")
    print(f"Loaded {len(existing)} existing hunter addresses")
    return existing

# Unified classification helpers
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
    "city_hall","parking","car_wash","dentist","doctor",
    "pharmacy","health","physiotherapist","veterinary_care",
    "car_repair","car_dealer","gas_station","clothing_store",
    "electronics_store","furniture_store","hardware_store",
    "jewelry_store","shoe_store","bakery","meal_delivery",
    "meal_takeaway","night_club","bar","bowling_alley",
    "book_store","plumber","electrician","roofing_contractor",
    "general_contractor","painter","locksmith","moving_company",
    "storage","laundry","car_wash","funeral_home",
    "real_estate_agency","travel_agency","accounting","insurance_agency",
    "lawyer","finance","bank","gym","spa","beauty_salon",
    "hair_care","lodging","store","restaurant","food","cafe",
}

def is_commercial(types):
    return any(t in COMM_TYPES for t in types)

# Version comparison (all programs use this)
def vtuple(v):
    nums = __import__('re').findall(r'(\d+)', v)
    return tuple(int(x) for x in nums[:3]) if nums else (0, 0, 0)
