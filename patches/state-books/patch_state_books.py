# -*- coding: utf-8 -*-
import re, sys
P = "optimus/standalone/maps_scraper_standalone.py"
s = open(P, encoding="utf-8").read()
orig = s

# ---------- 1. constants next to PF_SPLIT_SHEET_ID ----------
anchor = 'PF_SPLIT_SHEET_ID = "1DXu-nuQvVKrqQVk8LDNwLztG31ddi6sAyo8vXDFKcmQ"\n'
assert s.count(anchor) == 1
s = s.replace(anchor, anchor + '''
# THE TWO STATE WORKBOOKS (Patrick, 2026-09-05: "2 sheets TX non Texas / tabs Green
# Gold Grey Biz Fiber Biz / address name cell / color coded / ghl + dealmachine
# enrichment / both programs in sync / someone can read the sheet with no AI /
# we don't tweak shit after this"). The five GHL tabs + a LEGEND are rebuilt into
# BOTH of these at every launch, each row routed by its State (ZIP when State is
# blank). Baked in so NO PC needs a file. Both are shared with the fiberscanner
# service account as writer (done 2026-09-05). Empty string = that book is off.
TX_SHEET_ID = "1XkiFxn5E6AugHl7EAn02ivGwix0Mus1XiY1mM-g0_ls"        # OPTIMUS LEADS - TEXAS
NONTX_SHEET_ID = "1rVvg5NaF1exOvnP9F4PPmD8_AEgsDo9DLxRdA3dDb48"     # OPTIMUS LEADS - NON-TEXAS
TX_ZIP_PREFIXES = ("75", "76", "77", "78", "79", "733")
''')

# ---------- 2. helpers before sync_ghl_status ----------
anchor2 = "def sync_ghl_status(sh):\n"
assert s.count(anchor2) == 1
helpers = r'''LEGEND_TAB = "LEGEND"


def _route_state(row):
    """'TX' or 'NON-TX' for one GHL_HEADER row. State first; ZIP when State is
    blank (Texas ZIPs are 75xxx-79xxx plus 733xx). Pure -- tested without Google."""
    st = _s(row[_G["State"]]).upper()
    if st in ("TX", "TEXAS"):
        return "TX"
    if st:
        return "NON-TX"
    return "TX" if _s(row[_G["ZIP"]]).startswith(TX_ZIP_PREFIXES) else "NON-TX"


def _state_books(sh):
    """{'TX': Spreadsheet|None, 'NON-TX': Spreadsheet|None}. A book that will
    not open is announced LOUDLY -- a quiet fallback is how gold vanished for
    weeks -- and nothing is written into production instead."""
    out = {}
    try:
        gc = _gc(sh)
    except Exception as e:
        print("  GHL STATUS: no Google client (%s) -- state workbooks not opened." % str(e)[:50])
        return {"TX": None, "NON-TX": None}
    for state, sid in (("TX", TX_SHEET_ID), ("NON-TX", NONTX_SHEET_ID)):
        if not sid:
            out[state] = None
            continue
        try:
            _sheet_throttle()
            b = gc.open_by_key(sid)
            print("  GHL STATUS: %s -> '%s' (%s)" % (state, b.title, sid))
            out[state] = b
        except Exception as e:
            print("")
            print("  " + "!" * 66)
            print("  CANNOT OPEN THE %s WORKBOOK  id: %s" % (state, sid))
            print("  error: %s" % str(e)[:90])
            print("  Almost always: it is not shared with the service account. Open")
            print("  google_creds.json, copy \"client_email\", share the sheet with that")
            print("  address as Editor, relaunch. Nothing is written anywhere else.")
            print("  " + "!" * 66)
            print("")
            out[state] = None
    return out


def _legend_rows(state, stamp):
    """The LEGEND tab. Written so a rep with no AI and no brain file can read
    the workbook cold. Plain words, no jargon, no commission figures."""
    return [
        ["THIS WORKBOOK", "OPTIMUS LEADS - %s. Rebuilt by the Maps Scraper at every launch from the"
                          " hunter tabs + GoHighLevel. Last rebuild: %s" % (state, stamp)],
        ["", ""],
        ["ROW COLOUR = SALE STATE (from GoHighLevel)", ""],
        ["BLUE", "SOLD / PAID / INSTALLED - a closed sale. Do not pitch again."],
        ["GREEN", "CB / CALL BACK / MAYBE - they asked to be called back. Call them."],
        ["RED", "NI / NOT INTERESTED / DEAD / DNC - finished. Do not call, do not text."],
        ["GREY", "NO FIBER - service not available at that address. Not a lead."],
        ["No colour", "Never dispositioned. Nobody has spoken to them yet."],
        ["", ""],
        ["TABS", ""],
        ["Green", "Not an AT&T customer, fiber is available. The real prospect. An availability"
                  " notice, not a switch pitch."],
        ["Gold", "Already an AT&T customer, still on copper, fiber available. An UPGRADE - no"
                 " competitor to beat. Easiest sale. EVERY gold dot on the map is here, enriched or not."],
        ["Grey", "Already on AT&T fiber. NOT A LEAD. Never call, never text. Here only so nobody"
                 " wastes a dial on them."],
        ["Biz", "A scraped business at a fiber address."],
        ["Fiber Biz", "A business on a confirmed-green street - the new-fiber detector. ALL of them"
                      " are here, enriched or not."],
        ["", ""],
        ["COLUMNS", ""],
        ["Enriched", "YES = a cell number is on the GoHighLevel contact. NO = nobody has pulled a"
                     " number yet - this is the DealMachine backlog. NEVER re-enrich a YES."],
        ["Name / Cell / Email", "From GoHighLevel. Blank = not enriched."],
        ["Dot Color", "GREEN / GOLD / GREY = the hunter saw that dot on the AT&T map on the date in"
                      " Captured At. UNVERIFIED = somebody typed a tag; a claim, not a dot. Open"
                      " with: who do you have for internet today?"],
        ["Disposition", "SOLD, CB, NI, DNC, NO FIBER - from the tags on the GoHighLevel contact."
                        " This is what colours the row."],
        ["DND", "YES = they replied STOP. Never text them. Calling is still allowed unless"
                " Disposition says NI or DNC."],
        ["Synced At", "When this row was last rebuilt from GoHighLevel."],
        ["", ""],
        ["RULES", ""],
        ["Grey never ships", "No grey row goes in a call list, a text list or a dialer."],
        ["Address first", "Say the street address out loud before you pitch. These leads ARE the"
                          " address."],
        ["No flat price", "\"In the $20s to $30s for the first year, I'll confirm your exact price"
                          " before anything is ordered.\" Business is priced by speed tier."],
        ["One state per book", "TX rows live in the TEXAS workbook, everything else in NON-TEXAS,"
                               " routed by State (ZIP when State is blank)."],
    ]


def _write_legend(book, state, stamp):
    """REPLACE the LEGEND tab. Never raises."""
    try:
        try:
            ws = book.worksheet(LEGEND_TAB)
        except Exception:
            _sheet_throttle()
            ws = book.add_worksheet(title=LEGEND_TAB, rows="60", cols="2")
        rows = _legend_rows(state, stamp)
        _sheet_throttle()
        ws.clear()
        if ws.row_count < len(rows):
            _sheet_throttle()
            ws.resize(rows=len(rows) + 5, cols=2)
        _sheet_throttle()
        ws.update("A1:B%d" % len(rows), rows, value_input_option="RAW")
        print("  GHL STATUS: '%s' written in the %s workbook." % (LEGEND_TAB, state))
    except Exception as e:
        print("  (GHL STATUS: '%s' not written in %s: %s)" % (LEGEND_TAB, state, str(e)[:50]))


'''
s = s.replace(anchor2, helpers + anchor2)

# ---------- 3. the body of sync_ghl_status: from the def to 'def publish_tab_counts' ----------
start = s.index("def sync_ghl_status(sh):\n")
end = s.index("def publish_tab_counts(sh):")
new_body = r'''def sync_ghl_status(sh):
    """The five GHL tabs + LEGEND, rebuilt into BOTH state workbooks. Runs after
    sync_sheet_log(), so init_match()'s green set is loaded.

    Every gold dot and every Fiber Biz row is SEEDED first, unenriched, so the
    whole gold list is visible whether or not anyone has pulled a number
    (Enriched = NO is the DealMachine backlog, on the sheet, for a human).
    GoHighLevel contacts then OVERLAY: a contact at a seeded address replaces
    the seed with the enriched row; everyone else lands as before. Green, Grey
    and Biz carry only GHL-touched rows -- the raw pools are 687k / 57k / 39k
    rows and live in the hunter tabs. Each row is routed to TX or NON-TX by
    its State (ZIP when blank). Production is never written."""
    if sh is None:
        return
    try:
        token = _ghl_token()
        if not token:
            print("  GHL STATUS: no ghl_token.txt next to the scraper -- the GHL columns stay"
                  " as they are. (GHL -> Settings -> Private Integrations, scope"
                  " contacts.readonly; paste the token into ghl_token.txt)")
            return
        books = _state_books(sh)
        if not any(books.values()):
            print("  GHL STATUS: neither state workbook opened -- nothing written.")
            return
        stamp = time.strftime("%Y-%m-%d %H:%M:%S")
        t0 = time.time()
        contacts, complete = _ghl_contacts(token)
        print("  GHL STATUS: %d contact(s) read from GoHighLevel in %ds%s."
              % (len(contacts), int(time.time() - t0), "" if complete else " (PARTIAL)"))
        known = _hunter_lookup(sh)
        per = {t: {} for t in GHL_TABS}                 # tab -> {key: row}
        seeded = 0
        blank_ghl = ["NO", "", "", "", "", "", "", "", stamp]      # Enriched..Synced At
        for k, (tab, hrow) in known.items():
            if tab not in (GOLD_TAB, ORANGE_BIZ_TAB, GREEN_BIZ_TAB):
                continue
            row = list(hrow) + [tab] + list(blank_ghl)
            for t in _GHL_ROUTE.get(tab, ()):
                per[t]["A:" + k] = row
                seeded += 1
        seen, skipped, unverified = set(), 0, 0
        for c in contacts:
            gid = _s(c.get("id"))
            if not gid or gid in seen:
                continue
            seen.add(gid)
            tabs, row = _ghl_row(c, known, stamp)
            if not tabs:
                skipped += 1
                continue
            if row[1] == "UNVERIFIED":
                unverified += 1
            k = _norm_addr(_s(c.get("address1")))
            for t in tabs:
                d = per[t]
                if k and ("A:" + k) in d:
                    d["A:" + k] = row                    # enriched row replaces the seed
                else:
                    d["G:" + gid] = row
        print("  GHL STATUS: %d map row(s) seeded (every gold dot + every Fiber Biz), %d people"
              " overlaid, %d on no hunter tab and carrying no colour tag -- not placed."
              % (seeded, len(seen), skipped))
        report = {"generated_at": stamp, "source": "maps_scraper startup",
                  "contacts_read": len(contacts), "pull_complete": complete,
                  "people": len(seen), "seeded": seeded, "unverified": unverified,
                  "not_placed": skipped, "books": {}}
        for state, book in books.items():
            if book is None:
                report["books"][state] = {"opened": False}
                continue
            full, bstate = False, {"opened": True, "tabs": {}}
            for t in GHL_TABS:
                rows = [r for r in per[t].values() if _route_state(r) == state]
                n = {"rows": len(rows),
                     "enriched": sum(1 for r in rows if r[_G["Enriched"]] == "YES"),
                     "not_enriched": sum(1 for r in rows if r[_G["Enriched"]] != "YES"),
                     "sold": sum(1 for r in rows if r[_G["Disposition"]] == "SOLD"),
                     "cb": sum(1 for r in rows if r[_G["Disposition"]] == "CB"),
                     "ni": sum(1 for r in rows if r[_G["Disposition"]] == "NI"),
                     "dnc": sum(1 for r in rows if r[_G["Disposition"]] == "DNC"),
                     "no_fiber": sum(1 for r in rows if r[_G["Disposition"]] == "NO FIBER"),
                     "sms_stop": sum(1 for r in rows if r[_G["DND"]]),
                     "unverified": sum(1 for r in rows if r[1] == "UNVERIFIED")}
                if full:
                    n["written"] = False
                else:
                    ok, full = _ghl_write_tab(book, t, rows, "%s workbook" % state)
                    n["written"] = ok
                    if full:
                        print("  *** GHL STATUS: the %s workbook is at the 10,000,000-cell"
                              " ceiling -- the remaining tabs are skipped this launch." % state)
                bstate["tabs"][t] = n
                print("  GHL STATUS %s '%s': %d rows (%d enriched, %d not yet, %d sold, %d CB,"
                      " %d NI, %d no fiber)%s"
                      % (state, t, n["rows"], n["enriched"], n["not_enriched"], n["sold"],
                         n["cb"], n["ni"], n["no_fiber"], "" if n["written"] else " -- NOT WRITTEN"))
            if not full:
                _write_legend(book, state, stamp)
            report["books"][state] = bstate
        # Which gold dots on the map have NO GHL contact at that address yet:
        # the enrichment backlog, published as addresses of map dots only --
        # never a name, phone or email. Capped so the file stays readable.
        try:
            in_ghl = set(k for k in (_norm_addr(_s(c.get("address1"))) for c in contacts) if k)
            gold = [(k, row) for k, (tab, row) in known.items() if tab == GOLD_TAB]
            missing = [(k, row) for k, row in gold if k not in in_ghl]
            addrs = [{"address": row[0] or k.replace("|", " "), "city": row[_G["City"]],
                      "state": row[_G["State"]], "zip": row[_G["ZIP"]], "lat": row[_G["Lat"]],
                      "lng": row[_G["Lng"]], "captured_at": row[_G["Captured At"]]}
                     for k, row in missing[:GHL_GOLD_LIST_CAP]]
            gold_counts = {"gold_dots_total": len(gold), "in_ghl": len(gold) - len(missing),
                           "not_in_ghl": len(missing)}
            out = dict({"generated_at": stamp}, **gold_counts)
            if len(missing) > GHL_GOLD_LIST_CAP:
                out["capped"] = True
            out["addresses"] = addrs
            gh_put(FEED_ROOT + "/gold_unenriched.json", json.dumps(out, separators=(",", ":")))
            report["gold"] = gold_counts
            print("  GHL STATUS: gold dots on the map: %d unique, %d in GHL (enriched), %d not yet"
                  " enriched -> _feed/gold_unenriched.json"
                  % (len(gold), len(gold) - len(missing), len(missing)))
        except Exception as e:
            print("  (GHL STATUS: gold backlog not published: %s)" % str(e)[:60])
        gh_put(FEED_ROOT + "/_ghl_status.json", json.dumps(report, separators=(",", ":")))
    except Exception as e:
        print("  (GHL STATUS skipped: %s)" % str(e)[:60])


'''
s = s[:start] + new_body + s[end:]

# ---------- 4. the header comment that says 'split workbook' ----------
s = s.replace("# person whose tags changed moves, and nothing is ever duplicated. Production\n"
              "# is at the 10,000,000-cell ceiling, so these tabs are never written there:\n"
              "# if the split workbook does not open, one line says so and nothing happens.",
              "# person whose tags changed moves, and nothing is ever duplicated. Production\n"
              "# is at the 10,000,000-cell ceiling, so these tabs are never written there:\n"
              "# they go into the TWO STATE WORKBOOKS (TX_SHEET_ID / NONTX_SHEET_ID); a book\n"
              "# that does not open is announced loudly and nothing happens.")
assert s != orig
open(P, "w", encoding="utf-8").write(s)
print("patched:", len(orig.splitlines()), "->", len(s.splitlines()), "lines")
