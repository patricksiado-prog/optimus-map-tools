"""
ZIP JUMP TEST v1.0
==================
Standalone test for the YouAchieve map navigation flow.
NO scanning, NO dot detection, NO sheets — just verify the
type → travel → click → zoom sequence lands at the right spot.

WHAT IT DOES:
  1. Loads existing fiber_hunter calibration (search bar + safe map spot)
  2. Asks you for a ZIP
  3. Performs the full sequence:
       - Click search bar
       - Type ZIP
       - Press Enter
       - Wait 4 sec for map to travel
       - Click safe spot on map
       - Press + three times
       - Wait for redraw
  4. Pauses so you can VISUALLY check:
       - Did it land at the right ZIP?
       - Is the zoom at neighborhood level?
       - Are dots clearly visible?
  5. Press Enter for next ZIP, or 'q' to quit

USAGE:
  python test_zip_jump.py

REQUIRES:
  hunter_calib.json (from running fiber_hunter.py --calibrate)
  pyautogui

NO Google Sheets, no internet, no permissions, no risk.
Pure visual verification.
"""

import os, sys, time, json

try:
    import pyautogui
except ImportError:
    print("ERROR: pyautogui not installed.")
    print("Run: pip install pyautogui")
    sys.exit(1)

VERSION = "1.0"
CALIB_FILE = "hunter_calib.json"

# ── ZOOM TIMING ───────────────────────────────────────────────────
ZOOM_CLICKS       = 3      # press + this many times after each ZIP
WAIT_AFTER_TYPING = 1.0    # let autocomplete dropdown appear
WAIT_AFTER_ENTER  = 4.0    # let map travel
WAIT_BETWEEN_ZOOMS = 0.5
WAIT_AFTER_ZOOM   = 1.5    # let dots redraw
START_DELAY       = 5      # seconds before first action


def load_calibration():
    if not os.path.exists(CALIB_FILE):
        print(f"\n❌ No calibration file ({CALIB_FILE}) found.")
        print("   Run: python fiber_hunter.py --calibrate")
        return None
    with open(CALIB_FILE) as f:
        cfg = json.load(f)
    required = ["search_x", "search_y", "map_safe_x", "map_safe_y"]
    for k in required:
        if k not in cfg:
            print(f"\n❌ Calibration is missing '{k}'.")
            print("   Re-run: python fiber_hunter.py --calibrate")
            return None
    return cfg


def jump_to_zip(zipcode, cfg):
    """Type ZIP, press Enter, wait, click safe spot, zoom 3x.
    No scanning. Pure navigation."""
    print(f"\n  🚀 Jumping to {zipcode}...")

    # 1. Click search bar
    print(f"     1) Click search bar at ({cfg['search_x']}, {cfg['search_y']})")
    pyautogui.click(cfg["search_x"], cfg["search_y"])
    time.sleep(0.5)

    # 2. Clear any existing text
    print(f"     2) Clearing search bar...")
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(0.3)

    # 3. Type ZIP
    print(f"     3) Typing '{zipcode}'...")
    pyautogui.typewrite(zipcode, interval=0.05)
    time.sleep(WAIT_AFTER_TYPING)

    # 4. Press Enter
    print(f"     4) Pressing Enter...")
    pyautogui.press("enter")

    # 5. Wait for map to travel
    print(f"     5) Waiting {WAIT_AFTER_ENTER}s for map to travel...")
    time.sleep(WAIT_AFTER_ENTER)

    # 6. Click safe spot on map
    print(f"     6) Click safe map spot at ({cfg['map_safe_x']}, {cfg['map_safe_y']})")
    pyautogui.click(cfg["map_safe_x"], cfg["map_safe_y"])
    time.sleep(0.4)

    # 7. Zoom in N times
    print(f"     7) Pressing + {ZOOM_CLICKS} times...")
    for i in range(ZOOM_CLICKS):
        pyautogui.press("+")
        print(f"        zoom {i+1}/{ZOOM_CLICKS}")
        time.sleep(WAIT_BETWEEN_ZOOMS)

    # 8. Wait for redraw
    print(f"     8) Waiting {WAIT_AFTER_ZOOM}s for dots to redraw...")
    time.sleep(WAIT_AFTER_ZOOM)

    print(f"     ✓ Done. Look at the map now.")


def main():
    print("\n" + "=" * 60)
    print(f"  ZIP JUMP TEST v{VERSION}")
    print("  Pure navigation test — no scanning, no sheets")
    print("=" * 60)

    cfg = load_calibration()
    if not cfg:
        sys.exit(1)

    print(f"\n  Loaded calibration:")
    print(f"    Search bar:    ({cfg['search_x']}, {cfg['search_y']})")
    print(f"    Safe map spot: ({cfg['map_safe_x']}, {cfg['map_safe_y']})")

    print(f"\n⚠ Make sure youachieve.att.com is OPEN and VISIBLE.")
    print(f"⚠ DO NOT touch the mouse during a jump.")
    print(f"  (PyAutoGUI failsafe: slam mouse to top-left to abort)")
    print("\nQuick test ZIPs:")
    print("  77088 (Houston, TX — Acres Homes)")
    print("  77070 (Houston, TX — Champions)")
    print("  36602 (Mobile, AL — downtown)")
    print("  35211 (Birmingham, AL)")
    input("\n  Press Enter when YouAchieve is ready... ")

    print(f"\n  Starting in {START_DELAY}s — switch to your browser NOW")
    for s in range(START_DELAY, 0, -1):
        print(f"    {s}...", end=" ", flush=True)
        time.sleep(1)
    print()

    jump_count = 0
    while True:
        z = input("\n📍 ZIP to jump to (or 'q' to quit): ").strip().lower()
        if z in ("q", "quit", "exit", ""):
            break
        if not (z.isdigit() and len(z) == 5):
            print("  ⚠ Enter a 5-digit ZIP")
            continue

        try:
            jump_to_zip(z, cfg)
            jump_count += 1
        except KeyboardInterrupt:
            print("\n  Stopped.")
            break
        except pyautogui.FailSafeException:
            print("\n  ⚠ FailSafe triggered (mouse hit corner). Aborting.")
            break
        except Exception as e:
            print(f"  ❌ err: {e}")

        print("\n  Look at the map. Did it land right? Is the zoom good?")
        ans = input("  Press Enter for next ZIP, or 'q' to quit: ").strip().lower()
        if ans in ("q", "quit", "exit"):
            break

    print(f"\n\n  Test session done. {jump_count} ZIPs tested.")
    print("  If jumps landed correctly, fiber_hunter scanning will work.\n")


if __name__ == "__main__":
    main()
