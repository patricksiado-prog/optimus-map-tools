#!/usr/bin/env python3
"""
PRECISE FIBER HUNTER v0.2  (COMMERCIAL green-dot exact-address grabber)
=============================================================================
Drives the AT&T fiber map in a real Chromium window (Playwright), clicks each
GREEN dot, reads the EXACT address from the popup, records it, then pans to the
next viewport. Snake pattern across a cols x rows grid.

CONFIG CENTRALIZATION (v0.2 + config patch):
  SHEET_ID and SCOPES are imported from optimus_config.py when present, with a
  hardcoded fallback so the script still runs standalone. OUT_TAB stays LOCAL
  on purpose -- this tool writes ONLY to 'Precise Fiber', never to
  'Hunter Green Commercial' or 'Fiber Commercial Leads'.

CHANGES v0.1 -> v0.2 (per field feedback):
  1. ZOOM: --zoom-in N and --zoom-out N (button -> keyboard -> wheel fallback).
  2. CLICK ALL DOTS THEN PAN: viewport fully drained before any pan.
  3. PAN bulletproofing: map focused before every pan; snake direction reverses.
  4. RESUME: already_seen() reads 'Precise Fiber' and skips captured addresses.
  5. POPUP CLOSE FALLBACK: x button -> empty-map click -> Escape.
  6. HSV / area thresholds desktop-tuned (1366x768); tune after first --dry.

URL: https://youachieve.att.com/yourefer/fiber

DEPLOY (HP desktop only):
  pip install playwright opencv-python numpy gspread google-auth
  python -m playwright install chromium

RUN:
  Log in once:   python precise_fiber_hunter.py --login
  Dry test:      python precise_fiber_hunter.py --zip 77447 --dry
  Real scan:     python precise_fiber_hunter.py --zip 77447 --cols 4 --rows 3 --zoom-in 3
  Broader sweep: python precise_fiber_hunter.py --zip 77447 --zoom-out 2 --cols 5 --rows 5
=============================================================================
"""

import os, sys, time, argparse, re

# ----------------------------------------------------------------------------
# CONFIG  (edit these first if detection is off)
# ----------------------------------------------------------------------------
MAP_URL     = "https://youachieve.att.com/yourefer/fiber"
PROFILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "att_profile")

# --- centralized config with standalone fallback ---
try:
    from optimus_config import SHEET_ID, SCOPES
except ImportError:
    SHEET_ID = "1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA"
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

# OUT_TAB stays LOCAL on purpose. Do NOT write to Hunter Green Commercial or
# Fiber Commercial Leads from this tool.
OUT_TAB = "Precise Fiber"

# --- GREEN dot color window (tune here). AT&T green dot is a vivid green. ---
GREEN_HUE_LO  = 70
GREEN_HUE_HI  = 95
GREEN_SAT_MIN = 120
GREEN_VAL_MIN = 90
MIN_DOT_AREA  = 60
MAX_DOT_AREA  = 4000

# --- map viewport region of the screen (fractions of the window) ---
MAP_TOP_FRAC    = 0.18
MAP_BOTTOM_FRAC = 0.96
MAP_LEFT_FRAC   = 0.02
MAP_RIGHT_FRAC  = 0.98

# --- pacing (seconds) ---
WAIT_AFTER_PAN   = 1.5
WAIT_AFTER_CLICK = 1.1
WAIT_AFTER_ZOOM  = 1.5
PAN_PRESSES      = 6

# --- popup parsing ---
POPUP_KEYS = {
    "eligible": re.compile(r"FIBER\s+ELIGIBLE", re.I),
    "address":  re.compile(r"Address:\s*(.+?)(?:\s*Status:|\s*Subscriber|\s*CREATE|$)", re.I | re.S),
    "status":   re.compile(r"Status:\s*(.+?)(?:\s*Subscriber|\s*CREATE|$)", re.I | re.S),
    "ban":      re.compile(r"Subscriber\s+BAN:\s*([*\d]+)", re.I),
}

# popup container selectors (scoped read; falls back to body if none match)
POPUP_SELECTORS = [".gm-style-iw", "[role='dialog']", ".popup", ".info-window", ".mapboxgl-popup-content"]


# ----------------------------------------------------------------------------
# deps
# ----------------------------------------------------------------------------
def _need(mod, pip_name=None):
    try:
        return __import__(mod)
    except Exception:
        print("MISSING: %s  ->  pip install %s" % (mod, pip_name or mod))
        sys.exit(1)

cv2 = _need("cv2", "opencv-python")
np  = _need("numpy", "numpy")
_need("playwright", "playwright")
from playwright.sync_api import sync_playwright


# ----------------------------------------------------------------------------
# sheet
# ----------------------------------------------------------------------------
def open_sheet():
    import gspread
    from google.oauth2.service_account import Credentials
    creds_file = None
    for p in ["google_creds.json",
              r"C:\Users\patri\Optimus\google_creds.json",
              r"C:\Users\patri\optimus\google_creds.json",
              os.path.join(os.path.expanduser("~"), "Desktop", "google_creds.json")]:
        if os.path.exists(p):
            creds_file = p; break
    if not creds_file:
        print("google_creds.json not found; will run as dry (no writes).")
        return None
    client = gspread.authorize(Credentials.from_service_account_file(creds_file, scopes=SCOPES))
    sh = client.open_by_key(SHEET_ID)
    try:
        ws = sh.worksheet(OUT_TAB)
    except Exception:
        ws = sh.add_worksheet(title=OUT_TAB, rows="5000", cols="8")
    if not ws.get_all_values():
        ws.append_row(["Address", "Status", "Subscriber BAN", "Eligible", "Captured At", "ZIP/Area"])
    return ws


def already_seen(ws):
    """Resume: read existing addresses so a re-run skips them (survives crashes)."""
    if not ws:
        return set()
    try:
        rows = ws.get_all_values()
    except Exception:
        return set()
    return set(r[0].strip().upper() for r in rows[1:] if r and r[0].strip())


# ----------------------------------------------------------------------------
# screenshot + green dot detection
# ----------------------------------------------------------------------------
def grab(page):
    raw = page.screenshot(type="png")
    arr = np.frombuffer(raw, dtype=np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)   # BGR


def map_region(img):
    h, w = img.shape[:2]
    return (int(h * MAP_TOP_FRAC), int(h * MAP_BOTTOM_FRAC),
            int(w * MAP_LEFT_FRAC), int(w * MAP_RIGHT_FRAC))


def find_green_dots(img):
    top, bottom, left, right = map_region(img)
    roi = img[top:bottom, left:right]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lower = np.array([GREEN_HUE_LO, GREEN_SAT_MIN, GREEN_VAL_MIN])
    upper = np.array([GREEN_HUE_HI, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    dots = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area < MIN_DOT_AREA or area > MAX_DOT_AREA:
            continue
        M = cv2.moments(c)
        if M["m00"] == 0:
            continue
        cx = int(M["m10"] / M["m00"]) + left
        cy = int(M["m01"] / M["m00"]) + top
        dots.append((cx, cy))
    dots.sort(key=lambda p: (p[1] // 40, p[0]))   # reading order
    return dots


# ----------------------------------------------------------------------------
# popup reading (scoped; falls back to body)
# ----------------------------------------------------------------------------
def _popup_text(page):
    for sel in POPUP_SELECTORS:
        try:
            el = page.query_selector(sel)
            if el:
                t = el.inner_text()
                if t and POPUP_KEYS["eligible"].search(t):
                    return t
        except Exception:
            continue
    try:
        return page.inner_text("body")
    except Exception:
        return ""


def read_popup(page):
    txt = _popup_text(page)
    if not txt or not POPUP_KEYS["eligible"].search(txt):
        return None
    out = {"eligible": True, "address": None, "status": None, "ban": None}
    m = POPUP_KEYS["address"].search(txt)
    if m:
        out["address"] = " ".join(m.group(1).split())[:160]
    m = POPUP_KEYS["status"].search(txt)
    if m:
        out["status"] = " ".join(m.group(1).split())[:80]
    m = POPUP_KEYS["ban"].search(txt)
    if m:
        out["ban"] = m.group(1).strip()
    return out if out["address"] else None


def empty_map_point(page):
    """A spot in the map region with no dot -- top-left corner of the map area."""
    vp = page.viewport_size or {"width": 1366, "height": 768}
    x = int(vp["width"] * (MAP_LEFT_FRAC + 0.01))
    y = int(vp["height"] * (MAP_TOP_FRAC + 0.02))
    return x, y


def close_popup(page):
    # 1) try an explicit close control
    for sel in ["[aria-label='Close']", "button:has-text('\u00d7')", "text=\u00d7", ".gm-ui-hover-effect"]:
        try:
            el = page.query_selector(sel)
            if el:
                el.click(timeout=800)
                time.sleep(0.2)
                return
        except Exception:
            pass
    # 2) fallback: click an EMPTY map spot (never a dot) to dismiss
    try:
        x, y = empty_map_point(page)
        page.mouse.click(x, y)
        time.sleep(0.2)
    except Exception:
        pass
    # 3) last resort
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


# ----------------------------------------------------------------------------
# map controls
# ----------------------------------------------------------------------------
def focus_map(page):
    """Focus the map WITHOUT hitting a dot: click an empty corner of the map."""
    x, y = empty_map_point(page)
    page.mouse.click(x, y)
    time.sleep(0.3)


def _zoom_once(page, direction):
    """Try on-screen button, then keyboard, then wheel. direction = 'in'|'out'."""
    btn_selectors = (["[aria-label='Zoom in']", "button[title='Zoom in']", "text=+"]
                     if direction == "in"
                     else ["[aria-label='Zoom out']", "button[title='Zoom out']", "text=-"])
    for sel in btn_selectors:
        try:
            el = page.query_selector(sel)
            if el:
                el.click(timeout=800)
                return
        except Exception:
            pass
    # keyboard
    try:
        page.keyboard.press("Equal" if direction == "in" else "Minus")
        return
    except Exception:
        pass
    # mouse wheel over map center
    vp = page.viewport_size or {"width": 1366, "height": 768}
    page.mouse.move(vp["width"] // 2, int(vp["height"] * 0.55))
    page.mouse.wheel(0, -300 if direction == "in" else 300)


def zoom(page, presses, direction):
    for _ in range(max(0, presses)):
        _zoom_once(page, direction)
        time.sleep(0.3)
    if presses > 0:
        time.sleep(WAIT_AFTER_ZOOM)


def pan(page, direction):
    focus_map(page)   # make sure arrow keys land on the map
    key = {"left": "ArrowLeft", "right": "ArrowRight",
           "up": "ArrowUp", "down": "ArrowDown"}[direction]
    for _ in range(PAN_PRESSES):
        page.keyboard.press(key)
        time.sleep(0.12)
    time.sleep(WAIT_AFTER_PAN)


def search_zip(page, zip_code):
    for sel in ["input[type='search']", "input[placeholder*='ddress']",
                "input[placeholder*='earch']", "input"]:
        try:
            box = page.query_selector(sel)
            if box:
                box.click()
                box.fill(str(zip_code))
                time.sleep(0.4)
                page.keyboard.press("Enter")
                time.sleep(3.0)
                return True
        except Exception:
            continue
    return False


# ----------------------------------------------------------------------------
# scan: drain each viewport fully, THEN pan; snake across grid
# ----------------------------------------------------------------------------
def drain_viewport(page, ws, seen, area_label, dry):
    """Click EVERY green dot in the current viewport, capture, return count."""
    captured = 0
    clicked_pixels = set()
    dots = find_green_dots(grab(page))
    print("  viewport: %d green dots" % len(dots))
    for (x, y) in dots:
        keyxy = (x // 12, y // 12)          # coarse de-dupe within this viewport
        if keyxy in clicked_pixels:
            continue
        clicked_pixels.add(keyxy)
        try:
            page.mouse.click(x, y)
        except Exception:
            continue
        time.sleep(WAIT_AFTER_CLICK)
        info = read_popup(page)
        if info and info.get("address"):
            addr_key = info["address"].strip().upper()
            if addr_key not in seen:
                seen.add(addr_key)
                row = [info["address"], info.get("status") or "",
                       info.get("ban") or "", "FIBER ELIGIBLE",
                       time.strftime("%Y-%m-%d %H:%M:%S"), area_label]
                if dry or not ws:
                    print("    + %s | %s | BAN %s" %
                          (info["address"], info.get("status") or "-", info.get("ban") or "-"))
                else:
                    try:
                        ws.append_row(row)
                    except Exception as e:
                        print("    write error: %s" % e)
                captured += 1
        close_popup(page)
        time.sleep(0.3)
    return captured


def scan(page, ws, area_label, cols, rows, dry):
    seen = already_seen(ws)
    print("Resume: %d addresses already captured -> will skip them." % len(seen))
    total = 0
    for r in range(rows):
        for c in range(cols):
            print("[cell r%d c%d]" % (r, c))
            total += drain_viewport(page, ws, seen, area_label, dry)   # ALL dots first
            if c < cols - 1:
                pan(page, "right" if r % 2 == 0 else "left")           # THEN pan
        if r < rows - 1:
            pan(page, "down")                                          # next row, reverse dir
    return total


# ----------------------------------------------------------------------------
# entry
# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--login", action="store_true", help="open browser to log in once, then quit")
    ap.add_argument("--zip", default=None, help="ZIP/area to search before scanning")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--rows", type=int, default=3)
    ap.add_argument("--zoom-in", type=int, default=0, help="press zoom-IN this many times after load")
    ap.add_argument("--zoom-out", type=int, default=0, help="press zoom-OUT this many times after load")
    ap.add_argument("--dry", action="store_true", help="don't write to the sheet, just print")
    args = ap.parse_args()

    os.makedirs(PROFILE_DIR, exist_ok=True)

    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(
            PROFILE_DIR, headless=False,
            viewport={"width": 1366, "height": 768},
            args=["--start-maximized"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(MAP_URL, wait_until="domcontentloaded", timeout=60000)

        if args.login:
            print("\nLOG IN in the browser, open the Fiber Map, then come back here.")
            input("Press Enter when you're logged in and the map is showing... ")
            print("Session saved to %s. You can now run without --login." % PROFILE_DIR)
            ctx.close()
            return

        ws = None if args.dry else open_sheet()
        focus_map(page)

        if args.zip:
            print("Searching area: %s" % args.zip)
            if not search_zip(page, args.zip):
                print("Couldn't find the search box -- pan/zoom to your area by hand.")
                input("Press Enter when the map shows your area... ")
            focus_map(page)

        if args.zoom_in:
            print("Zooming IN x%d" % args.zoom_in)
            zoom(page, args.zoom_in, "in")
        if args.zoom_out:
            print("Zooming OUT x%d" % args.zoom_out)
            zoom(page, args.zoom_out, "out")

        print("Scanning %d x %d viewports...\n" % (args.cols, args.rows))
        n = scan(page, ws, args.zip or "manual", args.cols, args.rows, args.dry)
        print("\nDONE. Captured %d new fiber-eligible addresses." % n)
        print(("They're in the '%s' tab." % OUT_TAB) if ws else "(dry run, nothing written)")
        input("Press Enter to close the browser... ")
        ctx.close()


if __name__ == "__main__":
    main()
