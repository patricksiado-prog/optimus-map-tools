#!/usr/bin/env python3
"""
PRECISE HUNTER (DESKTOP / pyautogui + OCR)  v1.0
=============================================================================
Why this exists: youachieve.att.com is a hardened AT&T portal with MFA + bot
detection. It BLOCKS automated browsers (Playwright/Selenium/--remote-debugging).
So this tool does NOT control a browser at all. It drives the REAL mouse on the
screen (pyautogui) over YOUR normal, already-logged-in Chrome -- AT&T can't tell
it from a human. It clicks each GREEN dot, screenshots the popup, and reads the
EXACT address with on-screen OCR (Tesseract). Same idea as fiber_hunter's proven
pyautogui motion, plus per-dot click + OCR for exact addresses.

SETUP (HP desktop only):
  pip install pyautogui opencv-python numpy pytesseract pillow gspread google-auth
  Install Tesseract OCR (Windows):  https://github.com/UB-Mannheim/tesseract/wiki
    (default path C:\\Program Files\\Tesseract-OCR\\tesseract.exe is auto-detected)

HOW TO RUN:
  1. Open your NORMAL Chrome, log into the AT&T fiber map (do your MFA), maximize it,
     zoom to a cluster of green dots. Shrink the cmd window to a corner (don't cover map).
  2. First time only -- calibrate:
        python precise_hunter_desktop.py --calibrate
     (hover the map center, Enter; hover the "Search this area" button, Enter)
  3. Test (clicks dots, OCRs, prints, writes nothing, saves debug crops):
        python precise_hunter_desktop.py --dry
  4. Real run (writes to the "Precise Fiber" tab), snake a grid or go forever:
        python precise_hunter_desktop.py --cols 4 --rows 3
        python precise_hunter_desktop.py --forever
=============================================================================
"""
import os, sys, time, json, argparse, re

# ---------------------------------------------------------------------------
# CONFIG  (tune after the first --dry run)
# ---------------------------------------------------------------------------
CALIB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "precise_desktop_calib.json")
DEBUG_DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "precise_debug")

# GREEN dot color window (HSV). AT&T green dot is a vivid green.
GREEN_HUE_LO, GREEN_HUE_HI = 70, 95
GREEN_SAT_MIN, GREEN_VAL_MIN = 120, 90
MIN_DOT_AREA, MAX_DOT_AREA = 60, 4000

# Map region of the SCREEN (fractions of full screen) -- where dots live.
MAP_TOP_FRAC, MAP_BOTTOM_FRAC = 0.14, 0.97
MAP_LEFT_FRAC, MAP_RIGHT_FRAC = 0.02, 0.98

# Popup capture box relative to the clicked dot (pixels). The info popup opens
# near the dot; this box is OCR'd. Widen/move it if OCR misses the address.
POPUP_DX, POPUP_DY = -260, -210      # top-left of crop relative to click point
POPUP_W,  POPUP_H  = 520, 230

# Pan (pyautogui drag) -- fiber_hunter's proven values.
PAN_PIXELS = 300
WAIT_AFTER_PAN   = 1.6
WAIT_AFTER_CLICK = 1.0
WAIT_AFTER_SEARCH = 1.6

OUT_TAB  = "Precise Fiber"   # LOCAL on purpose; never the Hunter/Commercial tabs
try:
    from optimus_config import SHEET_ID, SCOPES
except ImportError:
    SHEET_ID = "1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA"
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"]

POPUP_KEYS = {
    "eligible": re.compile(r"FIBER\s+ELIGIBLE", re.I),
    "address":  re.compile(r"Address:\s*(.+?)(?:\s*Status:|\s*Subscriber|\s*CREATE|$)", re.I | re.S),
    "status":   re.compile(r"Status:\s*(.+?)(?:\s*Subscriber|\s*CREATE|$)", re.I | re.S),
    "ban":      re.compile(r"Subscriber\s+BAN:\s*([*\d]+)", re.I),
}


# ---------------------------------------------------------------------------
# deps
# ---------------------------------------------------------------------------
def _need(mod, pip_name=None):
    try:
        return __import__(mod)
    except Exception:
        print("MISSING: %s  ->  pip install %s" % (mod, pip_name or mod))
        sys.exit(1)

pyautogui = _need("pyautogui")
cv2 = _need("cv2", "opencv-python")
np  = _need("numpy")
pytesseract = _need("pytesseract")
from PIL import Image  # noqa

pyautogui.FAILSAFE = True   # slam mouse to a corner to abort

# auto-find tesseract on Windows
for _t in [r"C:\Program Files\Tesseract-OCR\tesseract.exe",
           r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"]:
    if os.path.exists(_t):
        pytesseract.pytesseract.tesseract_cmd = _t
        break


# ---------------------------------------------------------------------------
# calibration
# ---------------------------------------------------------------------------
def calibrate():
    print("\nCALIBRATION -- have the AT&T map open + maximized.")
    input("1) Hover the mouse over the CENTER of the map, then press Enter... ")
    cx, cy = pyautogui.position()
    input("2) Hover the mouse over the 'Search this area' button, then press Enter... ")
    bx, by = pyautogui.position()
    data = {"map_cx": cx, "map_cy": cy, "search_x": bx, "search_y": by}
    with open(CALIB_FILE, "w") as f:
        json.dump(data, f)
    print("Saved calibration: %s" % data)
    return data


def load_calib():
    if os.path.exists(CALIB_FILE):
        with open(CALIB_FILE) as f:
            return json.load(f)
    print("No calibration found -- run:  python precise_hunter_desktop.py --calibrate")
    sys.exit(1)


# ---------------------------------------------------------------------------
# screenshot + green dot detection
# ---------------------------------------------------------------------------
def grab():
    img = pyautogui.screenshot()
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


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
    dots.sort(key=lambda p: (p[1] // 40, p[0]))
    return dots


# ---------------------------------------------------------------------------
# popup OCR
# ---------------------------------------------------------------------------
def ocr_popup(click_x, click_y, dry, idx):
    screen = pyautogui.screenshot()
    W, H = screen.size
    x0 = max(0, click_x + POPUP_DX); y0 = max(0, click_y + POPUP_DY)
    x1 = min(W, x0 + POPUP_W);       y1 = min(H, y0 + POPUP_H)
    crop = screen.crop((x0, y0, x1, y1))
    if dry:
        try:
            os.makedirs(DEBUG_DIR, exist_ok=True)
            crop.save(os.path.join(DEBUG_DIR, "popup_%03d.png" % idx))
        except Exception:
            pass
    try:
        return pytesseract.image_to_string(crop)
    except Exception as e:
        print("    OCR error: %s" % e)
        return ""


def parse_popup(txt):
    if not txt or not POPUP_KEYS["eligible"].search(txt):
        return None
    out = {"address": None, "status": None, "ban": None}
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


# ---------------------------------------------------------------------------
# sheet
# ---------------------------------------------------------------------------
def open_sheet():
    import gspread
    from google.oauth2.service_account import Credentials
    for p in ["google_creds.json", r"C:\Users\patri\Optimus\google_creds.json",
              os.path.join(os.path.expanduser("~"), "Desktop", "google_creds.json")]:
        if os.path.exists(p):
            client = gspread.authorize(Credentials.from_service_account_file(p, scopes=SCOPES))
            sh = client.open_by_key(SHEET_ID)
            try:
                ws = sh.worksheet(OUT_TAB)
            except Exception:
                ws = sh.add_worksheet(title=OUT_TAB, rows="5000", cols="8")
            if not ws.get_all_values():
                ws.append_row(["Address", "Status", "Subscriber BAN", "Eligible", "Captured At", "Area"])
            return ws
    print("google_creds.json not found -- running dry (no writes).")
    return None


def already_seen(ws):
    if not ws:
        return set()
    try:
        rows = ws.get_all_values()
    except Exception:
        return set()
    return set(r[0].strip().upper() for r in rows[1:] if r and r[0].strip())


# ---------------------------------------------------------------------------
# mouse actions
# ---------------------------------------------------------------------------
def park_mouse():
    w, h = pyautogui.size()
    pyautogui.moveTo(w - 3, h - 3)


def close_popup(cal):
    # click an empty map spot (top-left of map), then Escape
    try:
        pyautogui.click(cal["map_cx"] - 350, cal["map_cy"] - 250)
    except Exception:
        pass
    time.sleep(0.2)
    pyautogui.press("esc")
    time.sleep(0.2)


def click_search(cal):
    pyautogui.click(cal["search_x"], cal["search_y"])
    time.sleep(WAIT_AFTER_SEARCH)
    park_mouse()


def pan(cal, direction):
    pyautogui.moveTo(cal["map_cx"], cal["map_cy"])
    if direction == "right":
        pyautogui.dragRel(-PAN_PIXELS, 0, duration=0.25, button="left")
    elif direction == "left":
        pyautogui.dragRel(PAN_PIXELS, 0, duration=0.25, button="left")
    elif direction == "down":
        pyautogui.dragRel(0, -PAN_PIXELS, duration=0.25, button="left")
    time.sleep(WAIT_AFTER_PAN)
    park_mouse()


# ---------------------------------------------------------------------------
# scan one viewport
# ---------------------------------------------------------------------------
def drain_viewport(cal, ws, seen, area_label, dry, counter):
    click_search(cal)                # load this area's dots (fiber_hunter pattern)
    dots = find_green_dots(grab())
    print("  viewport: %d green dots" % len(dots))
    captured = 0
    clicked = set()
    for (x, y) in dots:
        k = (x // 14, y // 14)
        if k in clicked:
            continue
        clicked.add(k)
        pyautogui.click(x, y)
        time.sleep(WAIT_AFTER_CLICK)
        counter[0] += 1
        info = parse_popup(ocr_popup(x, y, dry, counter[0]))
        if info and info["address"]:
            key = info["address"].strip().upper()
            if key not in seen:
                seen.add(key)
                row = [info["address"], info.get("status") or "", info.get("ban") or "",
                       "FIBER ELIGIBLE", time.strftime("%Y-%m-%d %H:%M:%S"), area_label]
                if dry or not ws:
                    print("    + %s | %s | BAN %s" %
                          (info["address"], info.get("status") or "-", info.get("ban") or "-"))
                else:
                    try:
                        ws.append_row(row)
                    except Exception as e:
                        print("    write error: %s" % e)
                captured += 1
        close_popup(cal)
    return captured


# ---------------------------------------------------------------------------
# entry
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrate", action="store_true", help="set map center + search button, then quit")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--rows", type=int, default=3)
    ap.add_argument("--forever", action="store_true", help="snake the grid until you press Ctrl+C")
    ap.add_argument("--dry", action="store_true", help="OCR + print, write nothing, save debug crops")
    ap.add_argument("--area", default="manual", help="label written in the Area column")
    args = ap.parse_args()

    if args.calibrate:
        calibrate()
        return

    cal = load_calib()
    ws = None if args.dry else open_sheet()
    seen = already_seen(ws)
    print("Resume: %d addresses already captured -> will skip them." % len(seen))
    print("Starting in 4 seconds -- click your Chrome map window NOW so it's on top.")
    time.sleep(4)

    counter = [0]
    total = 0
    try:
        if args.forever:
            print("FOREVER mode: snaking until Ctrl+C.\n")
            width = max(2, args.cols)
            going_right = True
            while True:
                for c in range(width):
                    total += drain_viewport(cal, ws, seen, args.area, args.dry, counter)
                    if c < width - 1:
                        pan(cal, "right" if going_right else "left")
                pan(cal, "down")
                going_right = not going_right
                print("  ... %d captured so far (Ctrl+C to stop)" % total)
        else:
            for r in range(args.rows):
                for c in range(args.cols):
                    print("[cell r%d c%d]" % (r, c))
                    total += drain_viewport(cal, ws, seen, args.area, args.dry, counter)
                    if c < args.cols - 1:
                        pan(cal, "right" if r % 2 == 0 else "left")
                if r < args.rows - 1:
                    pan(cal, "down")
    except KeyboardInterrupt:
        print("\nStopped.")
    print("\nDONE. Captured %d new fiber-eligible addresses." % total)
    print(("They're in the '%s' tab." % OUT_TAB) if ws else "(dry run, nothing written; debug crops in %s)" % DEBUG_DIR)


if __name__ == "__main__":
    main()
