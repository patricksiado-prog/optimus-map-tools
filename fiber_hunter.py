"""
push_fiber_hunter_v58_PATCH.py
==============================
PYDROID-RUN, ONE-SHOT.

Fetches current fiber_hunter.py from GitHub main, applies two targeted
fixes (Amazon/commercial-keyword GREY -> also write to Hunter Commercial,
and "(no #)" address rejection from Hunter Commercial), bumps VERSION
to 5.8, pushes back to main.

Token at /storage/emulated/0/Download/github_token.txt
Repo:   patricksiado-prog/optimus-map-tools
Branch: main
File:   fiber_hunter.py
"""

import os, sys, base64, json, urllib.request, urllib.error

REPO   = "patricksiado-prog/optimus-map-tools"
BRANCH = "main"
PATH   = "fiber_hunter.py"
TOKEN_FILE = "/storage/emulated/0/Download/github_token.txt"

NEW_VERSION = "5.8"

def http(method, url, token, body=None):
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", "token " + token)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "fiber-hunter-patch")
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, data=data, timeout=30) as r:
            return r.status, json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))

def main():
    if not os.path.exists(TOKEN_FILE):
        print("ERR: token file missing at " + TOKEN_FILE)
        sys.exit(1)
    token = open(TOKEN_FILE).read().strip()
    if not token:
        print("ERR: token file empty")
        sys.exit(1)

    print("[1/6] Fetching current %s from %s@%s..." % (PATH, REPO, BRANCH))
    url = "https://api.github.com/repos/%s/contents/%s?ref=%s" % (REPO, PATH, BRANCH)
    status, data = http("GET", url, token)
    if status != 200:
        print("ERR fetch: %d %s" % (status, data))
        sys.exit(1)
    sha = data["sha"]
    src = base64.b64decode(data["content"]).decode("utf-8")
    print("    got %d bytes, sha %s" % (len(src), sha[:8]))

    cur_version = None
    for line in src.splitlines():
        if line.startswith("VERSION ="):
            cur_version = line.split("=",1)[1].strip().strip('"').strip("'")
            break
    print("    current VERSION = %s" % cur_version)

    if cur_version == NEW_VERSION:
        print("ERR: repo already at v%s, abort" % NEW_VERSION)
        sys.exit(1)

    print("[2/6] Applying patches...")

    # ----- PATCH A: bump VERSION -----
    old_v = 'VERSION = "%s"' % cur_version
    new_v = 'VERSION = "%s"' % NEW_VERSION
    if old_v not in src:
        print("ERR: VERSION line not found"); sys.exit(1)
    src = src.replace(old_v, new_v, 1)
    print("    A. VERSION %s -> %s" % (cur_version, NEW_VERSION))

    # ----- PATCH B: GREY commercial promotion -----
    # Find the GREY skip in _process and insert commercial promotion before continue.
    grey_anchor = (
        '            if is_grey:\n'
        '                self.counters["grey"] += 1\n'
        '                continue\n'
    )
    grey_replacement = (
        '            if is_grey:\n'
        '                self.counters["grey"] += 1\n'
        '                # v5.8: GREY commercial buildings still get written to Hunter Commercial\n'
        '                # as social-proof / upsell targets (e.g. Amazon Fulfillment Centers).\n'
        '                if ptype == "COMMERCIAL" and biz:\n'
        '                    sheet_write(self.tabs, "Hunter Commercial", [\n'
        '                        full, biz, dot_type, gcity, state, zipc,\n'
        '                        zone_name, inst, str(self.scan_num), "Existing Fiber",\n'
        '                        REP_NAME, now, phone,\n'
        '                        "GREY - existing fiber customer (social proof / upsell)",\n'
        '                        verified_color,\n'
        '                    ], full)\n'
        '                continue\n'
    )
    if grey_anchor not in src:
        print("ERR: GREY anchor not found - source may have changed"); sys.exit(1)
    src = src.replace(grey_anchor, grey_replacement, 1)
    print("    B. GREY commercial promotion inserted")

    # ----- PATCH C: reject "(no #)" rows from Hunter Commercial -----
    # Find the COMMERCIAL write block in _process and gate it on house number presence.
    comm_anchor = (
        '            if ptype == "COMMERCIAL":\n'
        '                if is_green: self.counters["g_comm"] += 1\n'
        '                else:        self.counters["o_comm"] += 1\n'
        '                sheet_write(self.tabs, "Hunter Commercial", [\n'
    )
    comm_replacement = (
        '            if ptype == "COMMERCIAL":\n'
        '                if is_green: self.counters["g_comm"] += 1\n'
        '                else:        self.counters["o_comm"] += 1\n'
        '                # v5.8: skip "(no #)" rows from Hunter Commercial - they are\n'
        '                # street-only echoes, not real businesses. Still in Hunter Leads.\n'
        '                if full.endswith("(no #)"):\n'
        '                    pass\n'
        '                else:\n'
        '                    sheet_write(self.tabs, "Hunter Commercial", [\n'
    )
    if comm_anchor not in src:
        print("ERR: COMM anchor not found - source may have changed"); sys.exit(1)
    src = src.replace(comm_anchor, comm_replacement, 1)
    # The original sheet_write block ends with "], full)" - we need to close the else.
    # Find the very next "], full)\n                if is_green:" after our replacement
    # and add proper indentation.
    needle = (
        '                    sheet_write(self.tabs, "Hunter Commercial", [\n'
        '                    full, biz, dot_type, gcity, state, zipc,\n'
        '                    zone_name, inst, str(self.scan_num), "New", REP_NAME, now,\n'
        '                    phone, "", verified_color,\n'
        '                ], full)\n'
        '                if is_green:'
    )
    fixed = (
        '                    sheet_write(self.tabs, "Hunter Commercial", [\n'
        '                        full, biz, dot_type, gcity, state, zipc,\n'
        '                        zone_name, inst, str(self.scan_num), "New", REP_NAME, now,\n'
        '                        phone, "", verified_color,\n'
        '                    ], full)\n'
        '                if is_green:'
    )
    if needle not in src:
        print("ERR: indent-fix needle not found after PATCH C")
        print("     Source layout has changed - bailing without push")
        sys.exit(1)
    src = src.replace(needle, fixed, 1)
    print("    C. Hunter Commercial '(no #)' rejection + indent fix")

    print("[3/6] Validating syntax...")
    try:
        compile(src, "fiber_hunter.py", "exec")
        print("    syntax OK")
    except SyntaxError as e:
        print("ERR: patched source has syntax error - aborting push")
        print("     %s at line %d" % (e.msg, e.lineno))
        # Dump the suspicious region for inspection
        lines = src.split("\n")
        lo = max(0, (e.lineno or 1) - 5)
        hi = min(len(lines), (e.lineno or 1) + 5)
        for i in range(lo, hi):
            print("    %4d: %s" % (i+1, lines[i]))
        sys.exit(1)

    print("[4/6] Patch summary:")
    print("    new size: %d bytes" % len(src))
    print("    grey commercial promo present: %s" %
          ('GREY - existing fiber customer' in src))
    print("    no# guard present: %s" % ('endswith("(no #)")' in src))

    print("[5/6] Encoding and pushing...")
    new_b64 = base64.b64encode(src.encode("utf-8")).decode("ascii")

    put_url = "https://api.github.com/repos/%s/contents/%s" % (REPO, PATH)
    body = {
        "message": "fiber_hunter v5.8: GREY commercial promotion + '(no #)' guard",
        "content": new_b64,
        "branch":  BRANCH,
        "sha":     sha,
    }
    status, resp = http("PUT", put_url, token, body)
    if status not in (200, 201):
        print("ERR push: %d %s" % (status, resp))
        sys.exit(1)
    new_sha = resp.get("content", {}).get("sha", "?")
    print("    pushed. new sha %s" % new_sha[:8])

    print("[6/6] Done. Repo HEAD now v%s." % NEW_VERSION)
    print("      Patrick: stop fiber_hunter when ready, restart, auto-update kicks in.")

if __name__ == "__main__":
    main()