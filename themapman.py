# =============================================================
# HUNTER ENRICH ADDON v1  —  paste at TOP of themapman.py (line 1)
# Run with:    python themapman.py --enrich --visible --limit 10
# Full pass:   python themapman.py --enrich
# Flags: --enrich  --visible  --all  --limit N  --tab "Name"
# Adds Phone + Business Name to Hunter Green Commercial + Hunter
# Commercial in place. Self-contained. Does not touch existing
# themapman code paths. Exits before themapman main() runs.
# =============================================================
if any(_a in ("--enrich", "--hunter-enrich") for _a in __import__("sys").argv):
    import argparse, os, re, sys, time
    import gspread
    from google.oauth2.service_account import Credentials
    from playwright.sync_api import sync_playwright

    _SHEET_ID = "12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag"
    _TABS     = ["Hunter Green Commercial", "Hunter Commercial"]
    _CREDS    = "google_creds.json"
    _SCOPES   = ["https://www.googleapis.com/auth/spreadsheets"]
    _ELIG     = ("fiber", "upgrade", "eligible", "gold", "green")

    _p = argparse.ArgumentParser(add_help=False)
    _p.add_argument("--enrich", action="store_true")
    _p.add_argument("--hunter-enrich", action="store_true")
    _p.add_argument("--visible", action="store_true")
    _p.add_argument("--all", action="store_true")
    _p.add_argument("--limit", type=int, default=0)
    _p.add_argument("--tab")
    _args, _ = _p.parse_known_args()

    def _blank(v): return v is None or str(v).strip() == ""
    def _is_elig(s): return any(k in (s or "").lower() for k in _ELIG)

    def _fmt_phone(s):
        d = re.sub(r"\D", "", str(s or ""))
        if len(d) == 11 and d.startswith("1"): d = d[1:]
        return f"({d[:3]}) {d[3:6]}-{d[6:]}" if len(d) == 10 else ""

    def _find_col(headers, *cands):
        for c in cands:
            for i, h in enumerate(headers):
                if h.strip().lower() == c.lower(): return i + 1
        return None

    def _maps_lookup(page, addr):
        try:
            q = re.sub(r"\s+", "+", addr.strip())
            page.goto(f"https://www.google.com/maps/search/{q}", timeout=30000)
            page.wait_for_timeout(2500)
            n, ph = None, None
            try:
                t = page.locator("h1").first.inner_text(timeout=2000).strip()
                if t and t.lower() != "results": n = t
            except Exception: pass
            try:
                lbl = page.locator('button[aria-label^="Phone:"]').first.get_attribute(
                    "aria-label", timeout=2000) or ""
                m = re.search(r"Phone:\s*([\d\s\-\(\)+]+)", lbl)
                if m: ph = _fmt_phone(m.group(1))
            except Exception: pass
            return n, ph
        except Exception as e:
            print(f"    lookup err: {e}")
            return None, None

    print("=== HUNTER ENRICH ADDON v1 ===")
    if not os.path.exists(_CREDS):
        sys.exit(f"missing {_CREDS}")
    _gc = gspread.authorize(Credentials.from_service_account_file(_CREDS, scopes=_SCOPES))
    _ss = _gc.open_by_key(_SHEET_ID)
    _tabs_to_run = [_args.tab] if _args.tab else _TABS
    _total = 0

    with sync_playwright() as _pw:
        _br = _pw.chromium.launch(headless=not _args.visible)
        _pg = _br.new_context().new_page()
        for _tn in _tabs_to_run:
            print(f"\n--- {_tn} ---")
            try:
                _ws = _ss.worksheet(_tn)
            except gspread.WorksheetNotFound:
                print("  NOT FOUND"); continue
            _data = _ws.get_all_values()
            if len(_data) < 2:
                print("  empty"); continue
            _hd = _data[0]
            print(f"  headers: {_hd}")
            _ca = _find_col(_hd, "Address", "Address 1", "Street")
            _cp = _find_col(_hd, "Phone", "Phone Number")
            _cb = _find_col(_hd, "Business Name", "Name", "Business")
            _cs = _find_col(_hd, "Fiber Status", "Status")
            if not _ca:
                print("  NO ADDRESS COL"); continue
            print(f"  cols: addr={_ca} phone={_cp} biz={_cb} stat={_cs}")
            _cands = []
            for _ri, _row in enumerate(_data[1:], start=2):
                def _g(c): return _row[c-1] if c and c-1 < len(_row) else ""
                _ad = _g(_ca).strip()
                if not _ad: continue
                if (not _args.all) and _cs and not _is_elig(_g(_cs)): continue
                _np = bool(_cp) and _blank(_g(_cp))
                _nb = bool(_cb) and _blank(_g(_cb))
                if not (_np or _nb): continue
                _cands.append((_ri, _ad, _np, _nb))
            print(f"  candidates: {len(_cands)}")
            if _args.limit: _cands = _cands[:_args.limit]
            for _i, (_ri, _ad, _np, _nb) in enumerate(_cands, 1):
                print(f"  [{_i}/{len(_cands)}] r{_ri}: {_ad[:70]}")
                _bz, _ph = _maps_lookup(_pg, _ad)
                if _np and _ph:
                    _ws.update_cell(_ri, _cp, _ph); print(f"    + phone {_ph}"); _total += 1
                if _nb and _bz:
                    _ws.update_cell(_ri, _cb, _bz); print(f"    + biz   {_bz}"); _total += 1
                time.sleep(1.0)
        _br.close()
    print(f"\nTOTAL CELLS WRITTEN: {_total}")
    sys.exit(0)
# =============================================================
# END HUNTER ENRICH ADDON
# =============================================================
