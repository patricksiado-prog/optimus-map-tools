#!/usr/bin/env python3
"""
find_clusters.py — locate dense gold-dot clusters from Gold Dots lat/lng.

WHY THIS EXISTS
    "Find the gold cluster" is the one step nobody can do by eye at scale. The
    map shows dots; the sheet has 3,000+ gold rows with coordinates. Ranking
    gold by raw street count sorts you into residential subdivisions (Wenda 92,
    Oak Lawn 91, Mallow 62 — zero businesses between them). Clustering on
    COORDINATES finds a worked-able geographic pocket instead of a long street.

    Gold = an AT&T customer still on copper. A pocket thick with gold means
    nobody has converted that area yet, so nobody has worked it. That is the
    only freshness signal that survives (capture date just records when we
    looked, and grey is never written to the sheet at all).

INPUT
    CSV/TSV on stdin or a file path. The Gold Dots tab has NO header row:
        A=Address  B=Captured At  C=Lat  D=Lng
    Pass --has-header if your export added one. Rows with unparseable or
    zero coordinates are skipped and counted in `skipped`, never silently
    dropped — a cluster you cannot trust is worse than no cluster.

OUTPUT
    JSON to stdout: ranked clusters with count, centroid, bounding box, span,
    and the street breakdown. Feed the centroid + streets into the enrichment
    step.

USAGE
    python3 find_clusters.py gold_dots.csv --top 10
    python3 find_clusters.py gold_dots.csv --cell-meters 400 --min-count 8
"""
import argparse
import csv
import json
import math
import re
import sys
from collections import Counter, defaultdict

EARTH_M_PER_DEG_LAT = 111_320.0


def parse_rows(handle, has_header, delim):
    """Yield (address, lat, lng). Tolerates junk: the sheet is hand-touched."""
    reader = csv.reader(handle, delimiter=delim)
    if has_header:
        next(reader, None)
    good, skipped = [], 0
    for row in reader:
        if len(row) < 4:
            skipped += 1
            continue
        addr = (row[0] or "").strip()
        try:
            lat = float(str(row[2]).strip())
            lng = float(str(row[3]).strip())
        except (ValueError, TypeError):
            skipped += 1
            continue
        # 0,0 is the Atlantic. It means "no coordinate", not a location.
        if not addr or lat == 0 or lng == 0:
            skipped += 1
            continue
        if not (-90 <= lat <= 90 and -180 <= lng <= 180):
            skipped += 1
            continue
        good.append((addr, lat, lng))
    return good, skipped


STREET_RE = re.compile(
    r"\b(\d+)?\s*(.+?)\s+"
    r"(ST|STREET|RD|ROAD|DR|DRIVE|LN|LANE|BLVD|BOULEVARD|AVE|AVENUE|CT|COURT|"
    r"CIR|CIRCLE|WAY|PKWY|PARKWAY|TRL|TRAIL|HWY|HIGHWAY|PL|PLACE|TER|TERRACE)\b",
    re.I)

# Businesses sit on through-roads, not cul-de-sacs. A cluster whose streets are
# all LN/CT/CIR is a subdivision: fine for $500 green residential, wrong if you
# came looking for business gold.
COMMERCIAL_SUFFIXES = {"BLVD", "BOULEVARD", "RD", "ROAD", "HWY", "HIGHWAY",
                       "DR", "DRIVE", "PKWY", "PARKWAY", "AVE", "AVENUE"}


def street_of(address):
    """'10519 GRANT RD' -> ('GRANT RD', 'RD'). Returns (None, None) if unclear."""
    m = STREET_RE.search(address.upper())
    if not m:
        return None, None
    name = " ".join(m.group(2).split())
    suffix = m.group(3).upper()
    return "%s %s" % (name, suffix), suffix


def cluster(points, cell_meters):
    """Grid the points, then connect touching cells into one cluster.

    A grid plus 8-neighbour merge beats a fixed radius here: gold pockets are
    shaped like the streets they sit on, not like circles, so a merged grid
    follows a corridor while a radius would cut it into pieces.
    """
    if not points:
        return []
    mean_lat = sum(p[1] for p in points) / len(points)
    deg_lat = cell_meters / EARTH_M_PER_DEG_LAT
    # Longitude degrees shrink as you leave the equator; without the cos()
    # correction cells are far too wide in Texas and clusters over-merge.
    deg_lng = cell_meters / (EARTH_M_PER_DEG_LAT * max(0.01, math.cos(math.radians(mean_lat))))

    cells = defaultdict(list)
    for addr, lat, lng in points:
        cells[(int(math.floor(lat / deg_lat)), int(math.floor(lng / deg_lng)))].append((addr, lat, lng))

    seen, clusters = set(), []
    for key in cells:
        if key in seen:
            continue
        stack, members = [key], []
        seen.add(key)
        while stack:
            cy, cx = stack.pop()
            members.extend(cells[(cy, cx)])
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nk = (cy + dy, cx + dx)
                    if nk in cells and nk not in seen:
                        seen.add(nk)
                        stack.append(nk)
        clusters.append(members)
    return clusters


def describe(members):
    lats = [m[1] for m in members]
    lngs = [m[2] for m in members]
    streets, suffixes = Counter(), Counter()
    for addr, _, _ in members:
        name, suffix = street_of(addr)
        if name:
            streets[name] += 1
            suffixes[suffix] += 1
    commercial = sum(n for s, n in suffixes.items() if s in COMMERCIAL_SUFFIXES)
    total_named = sum(suffixes.values()) or 1
    mean_lat = sum(lats) / len(lats)
    span_ns = (max(lats) - min(lats)) * EARTH_M_PER_DEG_LAT
    span_ew = ((max(lngs) - min(lngs)) * EARTH_M_PER_DEG_LAT
               * math.cos(math.radians(mean_lat)))
    return {
        "gold_count": len(members),
        "centroid": {"lat": round(mean_lat, 6),
                     "lng": round(sum(lngs) / len(lngs), 6)},
        "bbox": {"min_lat": round(min(lats), 6), "max_lat": round(max(lats), 6),
                 "min_lng": round(min(lngs), 6), "max_lng": round(max(lngs), 6)},
        "span_meters": {"ns": round(span_ns), "ew": round(span_ew)},
        "streets": [{"street": s, "gold": n} for s, n in streets.most_common(12)],
        "commercial_suffix_pct": round(100.0 * commercial / total_named, 1),
        "profile": ("commercial-leaning" if commercial / total_named >= 0.5
                    else "residential-leaning"),
        "sample_addresses": [m[0] for m in members[:5]],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", help="CSV/TSV file; omit to read stdin")
    ap.add_argument("--has-header", action="store_true",
                    help="skip row 1 (the live Gold Dots tab has NO header)")
    ap.add_argument("--delim", default=",", help="field delimiter (default ,)")
    ap.add_argument("--cell-meters", type=float, default=400.0,
                    help="grid cell size; bigger merges more (default 400)")
    ap.add_argument("--min-count", type=int, default=5,
                    help="ignore clusters smaller than this (default 5)")
    ap.add_argument("--top", type=int, default=10, help="clusters to report")
    args = ap.parse_args()

    handle = open(args.path, newline="", encoding="utf-8-sig") if args.path else sys.stdin
    try:
        points, skipped = parse_rows(handle, args.has_header, args.delim)
    finally:
        if args.path:
            handle.close()

    groups = [g for g in cluster(points, args.cell_meters) if len(g) >= args.min_count]
    groups.sort(key=len, reverse=True)
    out = [dict(rank=i + 1, **describe(g)) for i, g in enumerate(groups[:args.top])]

    json.dump({
        "gold_rows_read": len(points),
        "rows_skipped_bad_coords": skipped,
        "clusters_found": len(groups),
        "cell_meters": args.cell_meters,
        "clusters": out,
    }, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
