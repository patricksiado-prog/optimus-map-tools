"""
FIBER HUNTER v3.0 — SPIRAL SCANNER
====================================
Pure scanning tool. No news, no internet research, no noise.
Type a ZIP, spiral outward forever, alert on every hot spot.
Stop with Ctrl+C anytime.

INDEPENDENT OF FIBER_SCAN — own state files, own sheet tabs.

USAGE:
  python fiber_hunter.py --calibrate         # one-time setup (2 points)
  python fiber_hunter.py --test              # type ZIPs one by one
  python fiber_hunter.py --spiral 77070      # spiral from ZIP, forever
  python fiber_hunter.py --spiral 77070 --step 250    # smaller spiral steps

WHAT IT DOES (--spiral mode):
  1. Types ZIP into YouAchieve search bar → presses Enter
  2. Waits 4 sec for map to travel
  3. Clicks safe spot on map → presses + 3 times to zoom in
  4. Screenshots map → counts gold/green/gray dots
  5. If hot → 🔥 ALERT + write to "🔥 Hunter Alerts" sheet tab
  6. If dead → silent skip
  7. Drags map outward in spiral pattern
  8. Repeat 4-7 forever until Ctrl+C

WHAT'S A "HOT SPOT":
  🔥🔥🔥 VIRGIN BUILD  = 3+ gold + ≤2 gray (brand new, no sales activity)
  🔥🔥 HOT             = 3+ gold dots
  🔥 FRESH GREEN ZONE  = 20+ green + <30% gray
  💀 SATURATED         = >70% gray (skip silently)
  💤 EMPTY             = <5 dots total (skip silently)
"""

import os, sys, time, json, argparse, re
from datetime import datetime
from collections import Counter

try:
    import pyautogui
    import numpy as np
    from PIL import Image, ImageGrab
    from scipy import ndimage
    SCAN_AVAILABLE = True
except ImportError:
    SCAN_AVAILABLE = False

try:
    import requests
except ImportError:
    requests = None

try:
    import gspread
    from google.oauth2.service_account import Credentials
    SHEETS_AVAILABLE = True
except ImportError:
    SHEETS_AVAILABLE = False

VERSION = "3.0"

# ── AUTO-UPDATER ──────────────────────────────────────────────────
AUTO_UPDATE = True
GITHUB_REPO = "patricksiado-prog/optimus-map-tools"
GITHUB_FILE = "fiber_hunter.py"
GITHUB_BRANCH = "main"

def check_update():
    if not AUTO_UPDATE or not requests:
        return
    try:
        url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{GITHUB_FILE}"
        print("Checking for updates...")
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            print(f"  Update check failed (HTTP {r.status_code})")
            return
        remote = r.text
        m = re.search(r'VERSION\s*=\s*["\']([\d.]+)["\']', remote)
        if not m: return
        rv = m.group(1)
        if rv == VERSION:
            print(f"  Up to date (v{VERSION})")
            return
        def vt(v): return tuple(int(x) for x in v.split("."))
        if vt(rv) <= vt(VERSION):
            print(f"  Local v{VERSION} newer than remote v{rv}")
            return
        print(f"  Updating to v{rv}...")
        with open(__file__, "w", encoding="utf-8") as f:
            f.write(remote)
        print("  Restarting...")
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print(f"  Update err: {str(e)[:100]}")


# ── CONFIG ────────────────────────────────────────────────────────
CREDS_FILE = "google_creds.json"
SHEET_ID   = "15ymTkIGPWs6quB035l414ns5hkG9cQ5xr_W4ukd0OAA"

# Hunter-only sheet tabs (separate from fiber_scan)
HUNTER_ALERTS_TAB = "Hunter Alerts"
HUNTER_LEADS_TAB  = "Hunter Leads"

CALIB_FILE = "hunter_calib.json"

# ── ZOOM / TIMING ─────────────────────────────────────────────────
AUTO_ZOOM_CLICKS   = 3
WAIT_AFTER_TYPING  = 1.0
WAIT_AFTER_ENTER   = 4.0
WAIT_BETWEEN_ZOOMS = 0.5
WAIT_AFTER_ZOOM    = 1.5
SCREENSHOT_DELAY   = 0.5
START_DELAY        = 8

# ── SPIRAL ────────────────────────────────────────────────────────
SPIRAL_STEP_PIXELS = 350    # how far to drag per step (~0.5 mi at zoom 3)

# ── ALERT THRESHOLDS ──────────────────────────────────────────────
ALERT_MIN_GOLD     = 3
ALERT_VIRGIN_GOLD  = 3
ALERT_VIRGIN_GRAY  = 2
SKIP_IF_TOTAL_LT   = 5
SKIP_IF_GRAY_PCT   = 0.70

# ── COLOR DETECTION ───────────────────────────────────────────────
GOLD_DOT_MIN = (220, 160, 0)
GOLD_DOT_MAX = (255, 200, 60)
GREEN_DOT_MIN = (30, 130, 30)
GREEN_DOT_MAX = (100, 210, 80)
GRAY_DOT_MIN = (140, 140, 140)
GRAY_DOT_MAX = (200, 200, 200)
MIN_DOT_PIXELS = 8
MAX_DOT_PIXELS = 250
MAX_ASPECT_RATIO = 2.5
MIN_FILL_RATIO = 0.45

# ── MAP COORDS (from CALIB_FILE) ──────────────────────────────────
SEARCH_X, SEARCH_Y = 200, 250
MAP_SAFE_X, MAP_SAFE_Y = 700, 600
MAP_LEFT, MAP_TOP = 0, 200
MAP_RIGHT, MAP_BOTTOM = 1366, 720


def now_str():
    return datetime.now().strftime("%m/%d/%Y %I:%M %p")


# ── CALIBRATION ───────────────────────────────────────────────────
def calibrate():
    print("\n" + "=" * 60)
    print("CALIBRATION — 2 points only")
    print("=" * 60)
    print("\n1. Open youachieve.att.com in your browser")
    print("2. Make sure the fiber map is fully visible\n")

    cfg = {}
    print("a) Hover mouse over the SEARCH BAR (where ZIP gets typed)")
    input("   Press Enter when ready: ")
    x, y = pyautogui.position()
    cfg["search_x"] = x
    cfg["search_y"] = y
    print(f"   Saved: ({x}, {y})\n")

    print("b) Hover over a SAFE empty spot on the map")
    print("   (not search bar, not buttons, just plain map area)")
    input("   Press Enter when ready: ")
    x, y = pyautogui.position()
    cfg["map_safe_x"] = x
    cfg["map_safe_y"] = y
    print(f"   Saved: ({x}, {y})\n")

    sw, sh = pyautogui.size()
    cfg["map_left"]   = 0
    cfg["map_top"]    = 200
    cfg["map_right"]  = sw
    cfg["map_bottom"] = sh - 50

    with open(CALIB_FILE, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"Saved to {CALIB_FILE}")
    print(f"  Search bar:    ({cfg['search_x']}, {cfg['search_y']})")
    print(f"  Safe map spot: ({cfg['map_safe_x']}, {cfg['map_safe_y']})")
    print(f"  Map bounds:    ({cfg['map_left']},{cfg['map_top']}) "
          f"to ({cfg['map_right']},{cfg['map_bottom']})")

def load_calibration():
    global SEARCH_X, SEARCH_Y, MAP_SAFE_X, MAP_SAFE_Y
    global MAP_LEFT, MAP_TOP, MAP_RIGHT, MAP_BOTTOM
    if not os.path.exists(CALIB_FILE):
        return None
    with open(CALIB_FILE) as f:
        cfg = json.load(f)
    SEARCH_X = cfg["search_x"]
    SEARCH_Y = cfg["search_y"]
    MAP_SAFE_X = cfg["map_safe_x"]
    MAP_SAFE_Y = cfg["map_safe_y"]
    MAP_LEFT   = cfg.get("map_left", 0)
    MAP_TOP    = cfg.get("map_top", 200)
    MAP_RIGHT  = cfg.get("map_right", 1366)
    MAP_BOTTOM = cfg.get("map_bottom", 720)
    return cfg


# ── MAP DRIVING ───────────────────────────────────────────────────
def search_and_zoom(zipcode):
    """Type ZIP, press Enter, click safe map spot, zoom 3x."""
    pyautogui.click(SEARCH_X, SEARCH_Y)
    time.sleep(0.5)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(0.3)
    pyautogui.typewrite(zipcode, interval=0.05)
    time.sleep(WAIT_AFTER_TYPING)
    pyautogui.press("enter")
    time.sleep(WAIT_AFTER_ENTER)
    pyautogui.click(MAP_SAFE_X, MAP_SAFE_Y)
    time.sleep(0.4)
    for _ in range(AUTO_ZOOM_CLICKS):
        pyautogui.press("+")
        time.sleep(WAIT_BETWEEN_ZOOMS)
    time.sleep(WAIT_AFTER_ZOOM)

def drag_map(dx, dy):
    """Click+hold safe spot, drag dx/dy pixels to pan map."""
    pyautogui.moveTo(MAP_SAFE_X, MAP_SAFE_Y)
    time.sleep(0.2)
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.moveTo(MAP_SAFE_X + dx, MAP_SAFE_Y + dy, duration=0.6)
    time.sleep(0.2)
    pyautogui.mouseUp()
    time.sleep(1.5)

def grab_map():
    return ImageGrab.grab(bbox=(MAP_LEFT, MAP_TOP, MAP_RIGHT, MAP_BOTTOM))


# ── DOT DETECTION ─────────────────────────────────────────────────
def find_dots(img, cmin, cmax):
    arr = np.array(img)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    mask = ((r >= cmin[0]) & (r <= cmax[0]) &
            (g >= cmin[1]) & (g <= cmax[1]) &
            (b >= cmin[2]) & (b <= cmax[2]))
    labeled, num = ndimage.label(mask)
    dots = []
    for i in range(1, num + 1):
        ys, xs = np.where(labeled == i)
        n = len(ys)
        if n < MIN_DOT_PIXELS or n > MAX_DOT_PIXELS: continue
        h = ys.max() - ys.min() + 1
        w = xs.max() - xs.min() + 1
        if h == 0 or w == 0: continue
        if max(h,w)/max(min(h,w),1) > MAX_ASPECT_RATIO: continue
        if n / float(h*w) < MIN_FILL_RATIO: continue
        dots.append((int(xs.mean()), int(ys.mean())))
    return dots

def scan_view(seed_zip, step_n):
    """Screenshot current map, count dots, decide if hot."""
    img = grab_map()
    gold  = find_dots(img, GOLD_DOT_MIN,  GOLD_DOT_MAX)
    green = find_dots(img, GREEN_DOT_MIN, GREEN_DOT_MAX)
    gray  = find_dots(img, GRAY_DOT_MIN,  GRAY_DOT_MAX)
    total = len(gold) + len(green) + len(gray)

    print(f"  [{step_n}] Gold:{len(gold):3d} Green:{len(green):3d} Gray:{len(gray):3d}",
          end="")

    if total < SKIP_IF_TOTAL_LT:
        print("  → empty 💤")
        return None, []

    gray_pct = len(gray) / total if total else 0
    if gray_pct > SKIP_IF_GRAY_PCT:
        print(f"  → {int(gray_pct*100)}% gray, saturated 💀")
        return None, []

    is_virgin = (len(gold) >= ALERT_VIRGIN_GOLD and len(gray) <= ALERT_VIRGIN_GRAY)
    is_hot = (len(gold) >= ALERT_MIN_GOLD)
    is_fresh_green = (len(green) >= 20 and gray_pct < 0.30)

    if is_virgin:
        priority = "🔥🔥🔥 VIRGIN BUILD"
    elif is_hot:
        priority = "🔥🔥 HOT"
    elif is_fresh_green:
        priority = "🔥 FRESH GREEN"
    else:
        print("  → has dots, not hot")
        return None, []

    print(f"  → {priority}")
    print("\n" + "🔥" * 30)
    print(f"  HOT SPOT — step {step_n} from seed {seed_zip}")
    print(f"  {priority}")
    print(f"  Gold:{len(gold)}  Green:{len(green)}  Gray:{len(gray)}")
    print("🔥" * 30 + "\n")

    alert = {
        "seed_zip": seed_zip,
        "step": step_n,
        "priority": priority,
        "gold": len(gold),
        "green": len(green),
        "gray": len(gray),
        "scanned_at": now_str(),
    }
    leads = []
    for color, dots in [("GOLD", gold[:30]), ("GREEN", green[:30])]:
        for px, py in dots:
            leads.append({
                "seed_zip": seed_zip,
                "step": step_n,
                "dot_color": color,
                "px": px, "py": py,
                "priority": priority,
                "scanned_at": now_str(),
            })
    return alert, leads


# ── SPIRAL GENERATOR ──────────────────────────────────────────────
def spiral_dirs(step):
    """Yields (dx, dy) for an infinite square spiral."""
    dirs = [(1,0), (0,-1), (-1,0), (0,1)]   # right, up, left, down
    leg = 1
    di = 0
    while True:
        for _ in range(2):
            dx, dy = dirs[di % 4]
            for _ in range(leg):
                yield (dx * step, dy * step)
            di += 1
        leg += 1


# ── SHEETS ────────────────────────────────────────────────────────
def connect_sheet():
    if not SHEETS_AVAILABLE or not os.path.exists(CREDS_FILE):
        return None
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets",
                  "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(CREDS_FILE, scopes=scopes)
        return gspread.authorize(creds).open_by_key(SHEET_ID)
    except Exception as e:
        print(f"  Sheets err: {e}")
        return None

ALERT_HDR = ["Seed ZIP","Step","Priority","Gold","Green","Gray","Scanned At"]
LEAD_HDR  = ["Seed ZIP","Step","Dot Color","Px","Py","Priority","Scanned At"]

def write_alerts(ss, alerts):
    if not ss or not alerts: return
    try:
        try: ws = ss.worksheet(HUNTER_ALERTS_TAB)
        except: ws = ss.add_worksheet(HUNTER_ALERTS_TAB, rows=2000, cols=10)
        if not ws.get_all_values():
            ws.update(range_name="A1", values=[ALERT_HDR])
        rows = [[a["seed_zip"], a["step"], a["priority"],
                 a["gold"], a["green"], a["gray"], a["scanned_at"]]
                for a in alerts]
        ws.append_rows(rows, value_input_option="USER_ENTERED")
        print(f"  ✓ {len(rows)} alerts → '{HUNTER_ALERTS_TAB}'")
    except Exception as e:
        print(f"  Alerts err: {e}")

def write_leads(ss, leads):
    if not ss or not leads: return
    try:
        try: ws = ss.worksheet(HUNTER_LEADS_TAB)
        except: ws = ss.add_worksheet(HUNTER_LEADS_TAB, rows=10000, cols=10)
        if not ws.get_all_values():
            ws.update(range_name="A1", values=[LEAD_HDR])
        rows = [[L["seed_zip"], L["step"], L["dot_color"],
                 L["px"], L["py"], L["priority"], L["scanned_at"]]
                for L in leads]
        ws.append_rows(rows, value_input_option="USER_ENTERED")
        print(f"  ✓ {len(rows)} leads → '{HUNTER_LEADS_TAB}'")
    except Exception as e:
        print(f"  Leads err: {e}")


# ── SPIRAL HUNT ───────────────────────────────────────────────────
def run_spiral(seed_zip, step_pixels):
    cfg = load_calibration()
    if not cfg:
        print("\n❌ No calibration. Run --calibrate first.")
        return

    print("\n" + "=" * 60)
    print(f"  🌀 SPIRAL HUNT — seed ZIP {seed_zip}")
    print(f"  Step size: {step_pixels}px (~{step_pixels/700:.1f} mi)")
    print(f"  Press Ctrl+C to stop anytime")
    print("=" * 60)
    print("\n⚠ Make sure youachieve.att.com is OPEN and VISIBLE")
    print("⚠ DO NOT touch the mouse during scanning")
    print(f"\nStarting in {START_DELAY}s — switch to your browser NOW")
    for s in range(START_DELAY, 0, -1):
        print(f"  {s}...", end=" ", flush=True)
        time.sleep(1)
    print()

    print(f"\n🚀 Jumping to seed ZIP {seed_zip}...")
    try:
        search_and_zoom(seed_zip)
    except Exception as e:
        print(f"  Failed to jump: {e}")
        return

    all_alerts = []
    all_leads = []
    step_n = 0
    hot_count = 0
    dead_count = 0

    # Scan starting position
    print("\n📡 Scanning seed position...")
    try:
        time.sleep(SCREENSHOT_DELAY)
        alert, leads = scan_view(seed_zip, step_n)
        if alert:
            all_alerts.append(alert)
            all_leads.extend(leads)
            hot_count += 1
        else:
            dead_count += 1
    except Exception as e:
        print(f"  Scan err: {e}")

    # Spiral until Ctrl+C
    print("\n🌀 Beginning spiral. Ctrl+C to stop.\n")
    try:
        for dx, dy in spiral_dirs(step_pixels):
            step_n += 1
            print(f"➡  Step {step_n}: drag ({dx:+d},{dy:+d})...")
            try:
                drag_map(dx, dy)
                time.sleep(SCREENSHOT_DELAY)
                alert, leads = scan_view(seed_zip, step_n)
                if alert:
                    all_alerts.append(alert)
                    all_leads.extend(leads)
                    hot_count += 1
                    # Periodic save in case of crash
                    if hot_count % 5 == 0:
                        _save_progress(seed_zip, all_alerts, all_leads)
                else:
                    dead_count += 1
            except pyautogui.FailSafeException:
                print("\n⚠ FailSafe (mouse hit corner). Stopping.")
                break
            except Exception as e:
                print(f"  Step err: {e}")
                continue
    except KeyboardInterrupt:
        print("\n\n⛔ Ctrl+C received — stopping cleanly.")

    # Summary
    print("\n" + "=" * 60)
    print(f"  SPIRAL DONE")
    print("=" * 60)
    print(f"  Seed ZIP:     {seed_zip}")
    print(f"  Total steps:  {step_n + 1}")
    print(f"  🔥 Hot:       {hot_count}")
    print(f"  💀 Dead:      {dead_count}")
    print(f"  Leads:        {len(all_leads)}")

    if all_alerts or all_leads:
        ss = connect_sheet()
        if ss:
            print("\n  Writing to Google Sheet...")
            write_alerts(ss, all_alerts)
            write_leads(ss, all_leads)


def _save_progress(seed_zip, alerts, leads):
    try:
        with open(f"spiral_{seed_zip}_progress.json", "w") as f:
            json.dump({"seed": seed_zip, "alerts": alerts, "leads": leads,
                       "saved_at": now_str()}, f, indent=2, default=str)
    except: pass


# ── TEST MODE ─────────────────────────────────────────────────────
def test_mode():
    cfg = load_calibration()
    if not cfg:
        print("❌ No calibration. Run --calibrate first.")
        return
    print("\n🧪 TEST MODE — type ZIPs one by one, scan each (no spiral)")
    print(f"⚠ Make sure youachieve.att.com is OPEN and VISIBLE")
    input("\nPress Enter when ready... ")
    print(f"\nStarting in {START_DELAY}s — switch to browser NOW")
    time.sleep(START_DELAY)

    while True:
        z = input("\n📍 ZIP (or 'q'): ").strip().lower()
        if z in ("q","quit","exit",""):
            break
        if not (z.isdigit() and len(z) == 5):
            print("  Enter a 5-digit ZIP")
            continue
        try:
            search_and_zoom(z)
            time.sleep(SCREENSHOT_DELAY)
            alert, leads = scan_view(z, 0)
            if alert:
                print(f"  ✅ {alert['priority']}")
            else:
                print("  💤 nothing hot")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"  err: {e}")


# ── MAIN ──────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--calibrate", action="store_true",
                        help="2-point calibration setup")
    parser.add_argument("--test", action="store_true",
                        help="Type ZIPs manually, scan each (no spiral)")
    parser.add_argument("--spiral", type=str, default=None,
                        help="Spiral from this ZIP forever, Ctrl+C to stop")
    parser.add_argument("--step", type=int, default=SPIRAL_STEP_PIXELS,
                        help=f"Spiral step in pixels (default {SPIRAL_STEP_PIXELS})")
    parser.add_argument("--no-update", action="store_true")
    args = parser.parse_args()

    if not args.no_update:
        check_update()

    print("\n" + "#" * 60)
    print(f"  FIBER HUNTER v{VERSION} — SPIRAL SCANNER")
    print("#" * 60)

    if not SCAN_AVAILABLE:
        print("\nERROR: pyautogui/numpy/PIL/scipy needed.")
        print("Install: pip install pyautogui numpy pillow scipy")
        sys.exit(1)

    if args.calibrate:
        calibrate()
        return

    if args.test:
        test_mode()
        return

    if args.spiral:
        if not (args.spiral.isdigit() and len(args.spiral) == 5):
            print("ERROR: --spiral needs a 5-digit ZIP. Example: --spiral 77070")
            sys.exit(1)
        run_spiral(args.spiral, args.step)
        return

    print("\nPick a mode:")
    print("  python fiber_hunter.py --calibrate")
    print("  python fiber_hunter.py --test")
    print("  python fiber_hunter.py --spiral 77070")
    print("\nRun with --help for more options.")


if __name__ == "__main__":
    main()
