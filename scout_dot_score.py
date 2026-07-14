"""
scout_dot_score.py  --  give the Fiber Scout the HUNTER's proven dot detection.

WHY
---
The Scout's own green window (optimus_dot_detect.py) reads GREEN 0 even on views
full of green dots. The HUNTER's color detection works (it pulled thousands of
green leads from the 77027 corridor). This module ports the hunter's EXACT color
windows + shape-filtered cluster counter, and adds a FRESH scorer tuned for what
a new-fiber area looks like: lots of GREEN + GOLD, very little GREY.

Colors, thresholds, and the cluster/shape/blank logic below are copied verbatim
from fiber_hunter.py so the Scout counts dots the same way the hunter does.

USE (in fiber_scout.py, per scanned view)
-----------------------------------------
    import scout_dot_score as sds
    r = sds.score_view(screenshot)          # PIL image, path, or np array
    # write to the "Fiber Scout" tab:
    #   r["green"], r["gold"], r["grey"], r["grey_pct"], r["verdict"]
    if r["verdict"] == "FRESH":
        ...  # send hunter + scraper here
"""

import numpy as np
from scipy import ndimage


# ── HUNTER color windows (verbatim from fiber_hunter.py) ────────────────────
GOLD_MIN  = (220, 160, 0)      # ORANGE_MIN — fiber eligible / copper customer
GOLD_MAX  = (255, 200, 60)     # ORANGE_MAX
GREEN_MIN = (30, 130, 30)      # fiber eligible / non-customer  (THE PRIZE)
GREEN_MAX = (100, 210, 80)
GREY_MIN  = (140, 140, 160)    # existing fiber customer  (sold, skip)
GREY_MAX  = (190, 190, 210)

# ── HUNTER dot-shape gate (verbatim) ────────────────────────────────────────
MIN_DOT_PIXELS      = 3
MAX_DOT_PIXELS      = 800
MAX_DOT_BBOX_AREA   = 1500
MIN_DOT_COMPACTNESS = 0.45
MAX_DOT_ASPECT      = 2.5
MIN_DOT_CLUSTERS    = 1

# ── HUNTER blank-map gate (verbatim) ────────────────────────────────────────
BLANK_STD_THRESHOLD        = 12.0
BLANK_CENTER_STD_THRESHOLD = 9.0
BLANK_BRIGHT_MEAN          = 240
BLANK_DARK_MEAN            = 30

# ── FRESH rule: new fiber = green+gold high, grey very low ──────────────────
FRESH_MIN_GREENGOLD = 6     # need at least this many green+gold dots in view
FRESH_MAX_GREY_PCT  = 20.0  # ...and grey must be under this % of all dots


def _as_rgb_array(img):
    """Accept a PIL Image, a file path, or an np array; return an HxWx3 array."""
    if isinstance(img, str):
        from PIL import Image
        img = Image.open(img)
    if hasattr(img, "convert"):
        return np.array(img.convert("RGB"))
    return np.array(img)


def _is_dot_shape(size, ys, xs):
    """Real fiber dots are roughly circular. Reject park slivers, skinny
    road markers, and oversized blobs. (verbatim from hunter)"""
    if size < MIN_DOT_PIXELS or size > MAX_DOT_PIXELS:
        return False
    h = int(ys.max()) - int(ys.min()) + 1
    w = int(xs.max()) - int(xs.min()) + 1
    bbox_area = h * w
    if bbox_area > MAX_DOT_BBOX_AREA:
        return False
    if float(size) / float(bbox_area) < MIN_DOT_COMPACTNESS:
        return False
    short = max(min(h, w), 1)
    if float(max(h, w)) / float(short) > MAX_DOT_ASPECT:
        return False
    return True


def count_dot_clusters(arr, cmin, cmax):
    """Connected-component count in a color window, each passing the dot-shape
    check. (verbatim logic from hunter)"""
    try:
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        mask = ((r >= cmin[0]) & (r <= cmax[0]) &
                (g >= cmin[1]) & (g <= cmax[1]) &
                (b >= cmin[2]) & (b <= cmax[2]))
        labeled, num = ndimage.label(mask)
        count = 0
        for i in range(1, num + 1):
            ys, xs = np.where(labeled == i)
            if _is_dot_shape(len(ys), ys, xs):
                count += 1
        return count
    except Exception:
        return 0


def is_blank_map(arr):
    """True if the view is blank / loading / timeout (don't score it). (verbatim)"""
    try:
        if float(arr.std()) < BLANK_STD_THRESHOLD:
            return True
        m = float(arr.mean())
        if m >= BLANK_BRIGHT_MEAN or m <= BLANK_DARK_MEAN:
            return True
        h, w = arr.shape[:2]
        center = arr[h // 4:3 * h // 4, w // 4:3 * w // 4]
        if float(center.std()) < BLANK_CENTER_STD_THRESHOLD:
            return True
        return False
    except Exception:
        return True


def score_view(img):
    """Score one map view the way the hunter sees dots.

    Returns dict: green, gold, grey (cluster counts), plotted, grey_pct,
    blank (bool), verdict (FRESH / MATURE / BLANK).
    FRESH = green+gold >= FRESH_MIN_GREENGOLD and grey% < FRESH_MAX_GREY_PCT.
    """
    arr = _as_rgb_array(img)

    if is_blank_map(arr):
        return {"green": 0, "gold": 0, "grey": 0, "plotted": 0,
                "grey_pct": 0.0, "blank": True, "verdict": "BLANK"}

    green = count_dot_clusters(arr, GREEN_MIN, GREEN_MAX)
    gold  = count_dot_clusters(arr, GOLD_MIN,  GOLD_MAX)
    grey  = count_dot_clusters(arr, GREY_MIN,  GREY_MAX)

    plotted = green + gold + grey
    grey_pct = (100.0 * grey / plotted) if plotted else 0.0
    fresh = (green + gold) >= FRESH_MIN_GREENGOLD and grey_pct < FRESH_MAX_GREY_PCT

    return {"green": green, "gold": gold, "grey": grey, "plotted": plotted,
            "grey_pct": round(grey_pct, 1), "blank": False,
            "verdict": "FRESH" if fresh else "MATURE"}


def summary_row(img):
    """Convenience: the Fiber Scout tab's columns in order.
    -> (Green, Gold, Grey, "Grey%", Verdict)"""
    r = score_view(img)
    return (r["green"], r["gold"], r["grey"], "%d%%" % round(r["grey_pct"]),
            r["verdict"])


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("usage: python scout_dot_score.py <map_screenshot.png> [...]")
        raise SystemExit(1)
    for p in sys.argv[1:]:
        r = score_view(p)
        print("%-40s green=%-3d gold=%-3d grey=%-3d grey%%=%-5s -> %s"
              % (p, r["green"], r["gold"], r["grey"],
                 "%d%%" % round(r["grey_pct"]), r["verdict"]))
