# APPLY: insert everything between the two markers below verbatim into
# optimus/standalone/maps_scraper_standalone.py immediately BEFORE the line
#     def publish_tab_counts(sh):
# Then insert the CALL SITE (at the bottom of this file) into main() right after
# the replay_parked try/except. Do NOT add it to _run_startup_clean -- it must
# run after open_sheet()/init_match().
# ==== BLOCK START ===========================================================
# ---------------------------------------------------------------------------
# THE SHEET AS THE FOLLOW-UP BOARD -- enrichment, GHL status and sales, landed
# at every launch.
#
# Patrick, 2026-09-03: "when we enrich leads add that to the sheet" -> "so u
# don't enrich 2x, dnd, u can check if we called and if dead" -> "use the sheet
# to log sales etc" -> "color for sales status red no / green cb maybe / blue
# paid" -> "I want ghl data and whether or not we already enriched something to
# be obvious ... and if it's sold or needs to be called back cuz we're doing an
# atrocious job of following up" -> "the same columns grey green gold biz fiber
# green biz, and if it's enriched it has name cell number, color coded for
# sales cb or ni".
#
# So 'Enriched Leads' is ONE ROW PER PERSON, laid out like the hunter's own
# tabs: the 13 hunter columns first (Address .. Status, copied from whichever
# tab the address sits on: Gold Confirmed, Grey Fiber Customers, Precise Fiber,
# or a business tab), then WHICH TAB it came from, then Name and Cell, then the
# enrichment record, then the GHL follow-up block. The whole row is coloured by
# Disposition: green = call back, red = no / not interested / dead, blue = paid.
# A white row is a person nobody has touched -- the follow-up being lost.
#
# HOW IT GETS HERE. Claude cannot write the workbook (its Drive connector is
# file-level only), and names and cell numbers cannot go through GitHub (both
# repos are PUBLIC). So Claude drops a small Google Sheet titled
# "OPTIMUS FEED <kind>" into the Drive folder FEED_FOLDER_ID, which is shared
# with the service account this program already runs as. At launch this step
# lists that folder, lands every file it has not seen, and renames the file
# "LANDED ..." so it is never read twice. Then it stamps a receipt on GitHub
# (optimus/_feed/_landed.json, no PII) so Claude can confirm delivery without
# Google auth: CHECK THE DESTINATION, not the return value.
#
# "So that doesn't cause a prob": every row carries a key (GHL contact id,
# else ADDRESS|ENRICHED AT; a sale keys on the opportunity id), so a launch
# repeats safely; the tabs live in the SPLIT workbook because production is at
# the 10,000,000-cell ceiling; a FULL workbook is said out loud and never
# retried; rows a person typed by hand on 'Sales Log' are never touched; and
# no dollar figure is ever written -- the sheet is shared with the team.
# ---------------------------------------------------------------------------
FEED_FOLDER_ID = "1XOqADybKvneC5gwsxjpsGkVC6RLQ-1an"      # 'OPTIMUS FEED (Claude -> sheet)'
FEED_TITLE = "OPTIMUS FEED"                               # + " enriched" | " status" | " sales"
FEED_ROOT = "optimus/_feed"                               # the receipt lives here on GitHub
ENRICHED_TAB = "Enriched Leads"
HUNTER_COLS = ["Address", "Dot Color", "Captured At", "Business", "Phone",
               "Run ID", "Operator", "Lat", "Lng", "City", "State", "ZIP", "Status"]
ENRICHED_HEADER = HUNTER_COLS + [
    "Tab",                                                 # which hunter tab the dot is on
    "Name", "Cell", "Phone Type",                          # the person (DealMachine / GHL)
    "Enriched At", "Source", "Pool", "GHL Contact ID", "Likely Gold", "DNC",
    "Dialed", "Last Call", "Disposition", "DND", "Dead", "Status At"]   # GHL follow-up
STATUS_COLS = ("dialed", "last_call", "disposition", "dnd", "dead", "status_at")
STATUS_FIRST_COL = ENRICHED_HEADER.index("Dialed") + 1          # 1-based
_E = {name: i for i, name in enumerate(ENRICHED_HEADER)}        # column index by name
SALES_TAB = "Sales Log"
SALES_HEADER = ["Sold At", "Address", "City", "State", "ZIP", "Name", "Cell", "Product",
                "Rep #", "Pool", "Source", "GHL Contact ID", "Opportunity ID", "Stage",
                "Status", "Logged At"]
# The whole row takes the colour of its Disposition / Status cell. Free text:
# CB, CALL BACK, MAYBE -> green; NO, NI, NOT INTERESTED, DEAD -> red; PAID,
# SOLD, INSTALLED -> blue.
STATUS_COLOURS = (
    ("PAID|SOLD|INSTALLED",              {"red": 0.74, "green": 0.84, "blue": 0.98}),  # blue
    ("^NO$|^NI$|NOT INTERESTED|DEAD|DNC", {"red": 0.96, "green": 0.72, "blue": 0.72}),  # red
    ("^CB|CALL ?BACK|MAYBE",             {"red": 0.72, "green": 0.90, "blue": 0.72}),  # green
)
GREY_TAB = "Grey Fiber Customers"
MAPS_BIZ_TAB = "Maps Businesses"
_STATUS_WORDS = {"GREEN": "Non-AT&T Customer - Can Get Fiber",
                 "ORANGE": "Upgrade Customer - On Copper, Fiber Available",
                 "GOLD": "Upgrade Customer - On Copper, Fiber Available",
                 "GREY": "Existing AT&T Customer"}


def _feed_sheets(client, kind):
    """[(spreadsheet id, title)] of unlanded feed files for one kind, oldest
    first. A landed file is renamed 'LANDED ...' and no longer matches."""
    want = ("%s %s" % (FEED_TITLE, kind)).lower()
    out = []
    for f in client.list_spreadsheet_files(folder_id=FEED_FOLDER_ID):
        name = (f.get("name") or "").strip()
        if name.lower().startswith(want):
            out.append((f.get("id"), name))
    return sorted(out, key=lambda x: x[1])


def _feed_rows(client, sid):
    """First tab of a feed sheet -> list of dicts keyed by its header row."""
    vals = client.open_by_key(sid).sheet1.get_all_values()
    if not vals:
        return []
    head = [h.strip().lower().replace(" ", "_") for h in vals[0]]
    rows = []
    for r in vals[1:]:
        if not any(c.strip() for c in r):
            continue
        rows.append({h: r[i].strip() for i, h in enumerate(head) if h and i < len(r)})
    return rows


def _mark_landed(client, sid, name):
    try:
        client.open_by_key(sid).update_title("LANDED " + name)
    except Exception as e:
        print("  (SHEET LOG: could not rename feed '%s' -- it is re-read next launch,"
              " harmlessly: %s)" % (name, str(e)[:40]))


def _hunter_lookup(book_main):
    """Normalised address -> (tab, the 13 hunter columns). Gold and grey from
    their own tabs (small); the three business tabs give Business + Phone;
    green from the biz-match set, which init_match() already loaded from the
    ~700k-row Precise Fiber tab. Read ONLY when there is something to land."""
    known = {}

    def take(tab, header, rows):
        idx = {h: i for i, h in enumerate(header)}
        for r in rows:
            k = _norm_addr(r[0] if r else "")
            if not k or k in known:
                continue
            row = [""] * len(HUNTER_COLS)
            for j, col in enumerate(HUNTER_COLS):
                i = idx.get(col)
                if i is not None and i < len(r):
                    row[j] = r[i]
            if not row[1]:
                row[1] = "ORANGE" if tab == GOLD_TAB else "GREY"
            if not row[12]:
                row[12] = _STATUS_WORDS.get(row[1].upper(), "")
            known[k] = (tab, row)

    for tab in (GOLD_TAB, GREY_TAB):
        try:
            _sheet_throttle()
            vals = book_main.worksheet(tab).get_all_values()
            if vals:
                take(tab, vals[0], vals[1:])
        except Exception as e:
            print("  (SHEET LOG: '%s' not read for the lookup: %s)" % (tab, str(e)[:40]))
    for tab in (GREEN_BIZ_TAB, ORANGE_BIZ_TAB, MAPS_BIZ_TAB):
        try:
            _sheet_throttle()
            vals = book_main.worksheet(tab).get_all_values()
        except Exception:
            continue
        for r in vals[1:]:                       # BIZ_HEADER: Business Name, Phone, Address, ...
            k = _norm_addr(r[2] if len(r) > 2 else "")
            if not k:
                continue
            if k in known:
                row = known[k][1]
                if not row[3]:
                    row[3], row[4] = r[0], (r[1] if len(r) > 1 else "")
                continue
            row = [""] * len(HUNTER_COLS)
            row[0], row[3], row[4] = r[2], r[0], (r[1] if len(r) > 1 else "")
            row[1] = "GREEN" if tab == GREEN_BIZ_TAB else "ORANGE" if tab == ORANGE_BIZ_TAB else ""
            row[12] = _STATUS_WORDS.get(row[1], "")
            known[k] = (tab, row)
    for k, colour in (_MATCH.get("leads") or {}).items():
        if k not in known:
            row = [""] * len(HUNTER_COLS)
            row[1], row[12] = colour, _STATUS_WORDS.get(colour, "")
            known[k] = ("Precise Fiber" if colour == "GREEN" else GOLD_TAB, row)
    return known


def _s(v):
    if v is True:
        return "YES"
    if v is False or v is None:
        return ""
    return str(v).strip()


def _yes(v):
    return "YES" if _s(v).upper() in ("YES", "TRUE", "1", "Y") else ""


def _enriched_row(r, known, stamp):
    """One 'enriched' feed row -> (key, sheet row). Pure -- tested without
    Google. Hunter columns come from the lookup when the address is on the
    map; the feed's own city/state/zip/lat/lng fill any blank. Key = GHL id,
    else ADDRESS|ENRICHED AT."""
    addr = _s(r.get("address"))
    if not addr:
        return None
    when = _s(r.get("enriched_at"))
    gid = _s(r.get("ghl_contact_id"))
    key = gid or ("%s|%s" % (addr.upper(), when))
    tab, hrow = known.get(_norm_addr(addr), ("", [""] * len(HUNTER_COLS)))
    row = list(hrow)
    row[0] = row[0] or addr
    for col, fld in (("City", "city"), ("State", "state"), ("ZIP", "zip"),
                     ("Lat", "lat"), ("Lng", "lng"), ("Business", "business")):
        if not row[_E[col]]:
            row[_E[col]] = _s(r.get(fld))
    if not row[1]:
        row[1] = (_s(r.get("colour")) or "UNVERIFIED").upper()
    if not row[12]:
        row[12] = _STATUS_WORDS.get(row[1], "Not on the hunter map yet - colour unverified")
    row += [tab, _s(r.get("name")), _s(r.get("cell")), _s(r.get("phone_type")), when,
            _s(r.get("source")), _s(r.get("pool")), gid,
            _yes(r.get("likely_gold")), _yes(r.get("dnc"))]
    row += [_s(r.get(c)) for c in STATUS_COLS]
    if not row[-1] and any(row[-6:-1]):
        row[-1] = stamp
    return key, row


def _sales_row(r, stamp):
    """One 'sales' feed row -> (key, sheet row). Key = opportunity id, else
    GHL id|sold at. No dollar figures: the sheet is shared with the team."""
    sold = _s(r.get("sold_at"))
    gid, oid, addr = _s(r.get("ghl_contact_id")), _s(r.get("opportunity_id")), _s(r.get("address"))
    if not (gid or oid or addr):
        return None
    key = oid or ("%s|%s" % (gid or addr.upper(), sold))
    return key, [sold, addr, _s(r.get("city")), _s(r.get("state")), _s(r.get("zip")),
                 _s(r.get("name")), _s(r.get("cell")), _s(r.get("product")), _s(r.get("rep")),
                 _s(r.get("pool")), _s(r.get("source")), gid, oid, _s(r.get("stage")),
                 _s(r.get("status")) or "PAID", stamp]


def _colour_status_rows(book, ws, header, col_name):
    """Conditional formatting: colour the whole row by the text in `col_name`.
    Added once, when the tab is created. Formatting can never stop rows from
    landing -- any failure is one printed line."""
    try:
        c = header.index(col_name)
        col = _col_letter(c + 1)
        reqs = []
        for i, (pattern, rgb) in enumerate(STATUS_COLOURS):
            reqs.append({"addConditionalFormatRule": {"index": i, "rule": {
                "ranges": [{"sheetId": ws.id, "startRowIndex": 1,
                            "startColumnIndex": 0, "endColumnIndex": len(header)}],
                "booleanRule": {
                    "condition": {"type": "CUSTOM_FORMULA", "values": [
                        {"userEnteredValue": '=REGEXMATCH(UPPER($%s2),"%s")' % (col, pattern)}]},
                    "format": {"backgroundColor": rgb}}}}})
        _sheet_throttle()
        book.batch_update({"requests": reqs})
        print("  SHEET LOG: '%s' rows colour by %s (green CB / red NI / blue PAID)."
              % (ws.title, col_name))
    except Exception as e:
        print("  (SHEET LOG: colour rules not added on '%s': %s)" % (ws.title, str(e)[:50]))


def _status_row(r, stamp):
    """One 'status' feed row -> (ghl id, [Dialed, Last Call, Disposition, DND, Dead, Status At])."""
    gid = _s(r.get("ghl_contact_id"))
    if not gid:
        return None
    vals = [_s(r.get(c)) for c in STATUS_COLS]
    if not vals[-1]:
        vals[-1] = stamp
    return gid, vals


def _tab_keys(values, id_col, key_cols):
    """Keys already on a tab: the id column when filled, else key_cols joined."""
    have = set()
    for row in values[1:]:
        if not row:
            continue
        gid = row[id_col].strip() if len(row) > id_col else ""
        if gid:
            have.add(gid)
            continue
        parts = [(row[c].strip().upper() if c == key_cols[0] else row[c].strip())
                 if len(row) > c else "" for c in key_cols]
        if parts[0]:
            have.add("|".join(parts))
    return have


def _col_letter(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _open_log_tab(book, title, header, where):
    """The tab, created with its header if missing, header widened if an
    older build made it narrower. None (already explained) on failure."""
    try:
        ws = book.worksheet(title)
    except Exception:
        try:
            _sheet_throttle()
            ws = book.add_worksheet(title=title, rows="1000", cols=str(len(header)))
            _sheet_throttle()
            ws.append_row(header, value_input_option="RAW")
            print("  SHEET LOG: created tab '%s' in the %s." % (title, where))
            _colour_status_rows(book, ws, header,
                                "Status" if title == SALES_TAB else "Disposition")
            return ws
        except Exception as e:
            if _err_kind(e) == "FULL":
                print("  *** SHEET LOG NOT LANDED: the %s is at the 10,000,000-cell"
                      " ceiling, so '%s' cannot be created there. Share the split"
                      " workbook with the service account and relaunch." % (where, title))
            else:
                print("  *** SHEET LOG NOT LANDED: could not make '%s': %s"
                      % (title, str(e)[:60]))
            return None
    try:
        _sheet_throttle()
        head = ws.row_values(1)
        if head and head != header[:len(head)]:
            print("  *** SHEET LOG: '%s' has a different header than this build expects"
                  " -- leaving it alone. Rename that tab to keep it, then relaunch." % title)
            return None
        if len(head) < len(header):
            if ws.col_count < len(header):
                _sheet_throttle()
                ws.resize(cols=len(header))
            _sheet_throttle()
            ws.update("A1:%s1" % _col_letter(len(header)), [header],
                      value_input_option="RAW")
            print("  SHEET LOG: '%s' header widened to %d columns." % (title, len(header)))
    except Exception as e:
        print("  (SHEET LOG: could not check the '%s' header: %s)" % (title, str(e)[:50]))
    return ws


def _append_rows(ws, rows, kind):
    """Append in 500-row batches under the write throttle. (landed, all ok)."""
    landed = 0
    for i in range(0, len(rows), 500):
        chunk = rows[i:i + 500]
        try:
            _sheet_throttle()
            ws.append_rows(chunk, value_input_option="RAW")
            landed += len(chunk)
        except Exception as e:
            print("  *** SHEET LOG: %d of %d '%s' row(s) NOT landed -- %s%s"
                  % (len(rows) - landed, len(rows), kind,
                     "workbook FULL (cell ceiling), " if _err_kind(e) == "FULL" else "",
                     str(e)[:50]))
            print("  *** The feed file stays unlanded and is retried next launch.")
            return landed, False
    return landed, True


def _read_feed_files(client, files, to_row, stamp, have=None, collect=None):
    """Every row of every feed file -> to_row(); rows whose key is already on
    the tab are skipped. Returns the files that were fully read."""
    ok = []
    for sid, name in files:
        try:
            rows = _feed_rows(client, sid)
        except Exception as e:
            print("  (SHEET LOG: feed '%s' unreadable: %s)" % (name, str(e)[:40]))
            continue
        for r in rows:
            kr = to_row(r, stamp)
            if kr and (have is None or kr[0] not in have):
                if have is not None:
                    have.add(kr[0])
                collect(kr)
        ok.append((sid, name))
    return ok


def sync_sheet_log(sh):
    """Runs after open_sheet()/init_match(), so the green set is loaded."""
    if sh is None:
        return
    client = sh.client
    book = _pf_spreadsheet(sh)
    where = "split workbook" if book is not sh else "MAIN workbook (split did not open)"
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    report = {"generated_at": stamp, "source": "maps_scraper startup", "workbook": where}
    try:
        feeds = {k: _feed_sheets(client, k) for k in ("enriched", "status", "sales")}
    except Exception as e:
        print("  SHEET LOG: feed folder not readable (%s) -- share Drive folder %s with"
              " the service account. Retries next launch." % (str(e)[:40], FEED_FOLDER_ID))
        return
    if not any(feeds.values()):
        print("  SHEET LOG: nothing new in the feed folder.")
        gh_put(FEED_ROOT + "/_landed.json",
               json.dumps(dict(report, nothing_new=True), separators=(",", ":")))
        return
    values = None
    ws = _open_log_tab(book, ENRICHED_TAB, ENRICHED_HEADER, where) \
        if (feeds["enriched"] or feeds["status"]) else None
    if ws is not None:
        try:
            _sheet_throttle()
            values = ws.get_all_values()
        except Exception as e:
            print("  *** SHEET LOG: cannot read '%s': %s" % (ENRICHED_TAB, str(e)[:60]))
    if ws is not None and values is not None:
        # 1. enriched: new people, laid out like the hunter's tabs
        if feeds["enriched"]:
            known = _hunter_lookup(sh)
            have = _tab_keys(values, _E["GHL Contact ID"], (0, _E["Enriched At"]))
            new = []
            files = _read_feed_files(client, feeds["enriched"],
                                     lambda r, st: _enriched_row(r, known, st),
                                     stamp, have, lambda kr: new.append(kr[1]))
            landed, ok = _append_rows(ws, new, "enriched")
            done = new[:landed]
            on_map = sum(1 for r in done if r[_E["Tab"]])
            print("  SHEET LOG: enriched -> '%s': %d file(s), %d new row(s), %d on the hunter"
                  " map (%d gold/orange, %d grey, %d green)"
                  % (ENRICHED_TAB, len(files), landed, on_map,
                     sum(1 for r in done if r[1] in ("ORANGE", "GOLD")),
                     sum(1 for r in done if r[1] == "GREY"),
                     sum(1 for r in done if r[1] == "GREEN")))
            if ok:
                for sid, name in files:
                    _mark_landed(client, sid, name)
            report["enriched"] = {"files": len(files), "landed": landed, "on_map": on_map}
            if landed:
                try:
                    _sheet_throttle()
                    values = ws.get_all_values()
                except Exception:
                    values = None
        # 2. status: the GHL follow-up columns on those rows, newest file wins
        if feeds["status"] and values is not None:
            latest = {}
            files = _read_feed_files(client, feeds["status"], _status_row, stamp,
                                     None, lambda kv: latest.__setitem__(kv[0], kv[1]))
            idx = {}
            gcol = _E["GHL Contact ID"]
            for n, row in enumerate(values[1:], start=2):
                g = row[gcol].strip() if len(row) > gcol else ""
                if g:
                    idx.setdefault(g, n)
            c0 = _col_letter(STATUS_FIRST_COL)
            c1 = _col_letter(STATUS_FIRST_COL + len(STATUS_COLS) - 1)
            updates, missing = [], 0
            for gid, vals in latest.items():
                n = idx.get(gid)
                if n is None:
                    missing += 1
                    continue
                cur = values[n - 1][STATUS_FIRST_COL - 1:STATUS_FIRST_COL - 1 + len(STATUS_COLS)]
                if len(cur) == len(vals) and [c.strip() for c in cur] == vals:
                    continue
                updates.append({"range": "%s%d:%s%d" % (c0, n, c1, n), "values": [vals]})
            done, ok = 0, True
            for i in range(0, len(updates), 500):
                try:
                    _sheet_throttle()
                    ws.batch_update(updates[i:i + 500], value_input_option="RAW")
                    done += len(updates[i:i + 500])
                except Exception as e:
                    print("  *** SHEET LOG: %d status row(s) NOT updated -- %s"
                          % (len(updates) - done, str(e)[:60]))
                    ok = False
                    break
            print("  SHEET LOG: status -> '%s': %d file(s), %d row(s) updated, %d unchanged%s"
                  % (ENRICHED_TAB, len(files), done, len(latest) - len(updates) - missing,
                     ", %d id(s) not on the tab (enrich them first)" % missing if missing else ""))
            if ok:
                for sid, name in files:
                    _mark_landed(client, sid, name)
            report["status"] = {"files": len(files), "updated": done, "not_on_tab": missing}
        try:
            report["enriched_rows_on_tab"] = max(len(ws.col_values(1)) - 1, 0)
        except Exception:
            pass
    # 3. sales on 'Sales Log' -- hand-typed rows have no id and are left alone
    if feeds["sales"]:
        ws2 = _open_log_tab(book, SALES_TAB, SALES_HEADER, where)
        if ws2 is not None:
            try:
                _sheet_throttle()
                vals = ws2.get_all_values()
                oi, gi = SALES_HEADER.index("Opportunity ID"), SALES_HEADER.index("GHL Contact ID")
                have = _tab_keys(vals, oi, (1, 0))
                for row in vals[1:]:
                    if len(row) > gi and row[gi].strip():
                        have.add("%s|%s" % (row[gi].strip(), row[0].strip()))
                new = []
                files = _read_feed_files(client, feeds["sales"], _sales_row, stamp,
                                         have, lambda kr: new.append(kr[1]))
                landed, ok = _append_rows(ws2, new, "sales")
                print("  SHEET LOG: sales -> '%s': %d file(s), %d new row(s)"
                      % (SALES_TAB, len(files), landed))
                if ok:
                    for sid, name in files:
                        _mark_landed(client, sid, name)
                report["sales"] = {"files": len(files), "landed": landed,
                                   "rows_on_tab": len(vals) - 1 + landed}
            except Exception as e:
                print("  *** SHEET LOG: cannot read '%s': %s" % (SALES_TAB, str(e)[:60]))
    # Tell Claude what landed WITHOUT Google auth: CHECK THE DESTINATION, not
    # the return value. A launch that lands nothing still stamps this, so a
    # stale stamp means "no scraper launch since", not "nothing to land".
    gh_put(FEED_ROOT + "/_landed.json", json.dumps(report, separators=(",", ":")))


# ==== BLOCK END =============================================================
#
# ==== CALL SITE: insert into main() right after this existing code:
#     try:
#         replay_parked(sheet_ws, sheet_seen)
#     except Exception as e:
#         print("  (replay skipped: %s)" % str(e)[:60])
# ---- add:
#     # THE FOLLOW-UP BOARD (Patrick 2026-09-03): land what Claude enriched, the
#     # GHL status and sales on the split workbook. After open_sheet() on purpose:
#     # init_match() has read Precise Fiber by now, so green dots resolve free.
#     if _want_clean and sheet_ws is not None:
#         try:
#             sync_sheet_log(sheet_ws.spreadsheet)
#         except Exception as e:
#             print("  *** SHEET LOG DID NOT RUN: %s" % str(e)[:70])
