# DEPLOY 2026-09-04 — four files, tested, ready to push to the hunter repo

Target: `patricksiado-prog/Go-High-Level-MCP-2026-Complete`, branch
`claude/optimus-map-tools-setup-6dcl6o`. Tested against upstream `0259d39`.

| File | What changes |
|---|---|
| `optimus/precise_fiber_hunter.py` | `LAUNCHER_SENTINEL = "GOLD CAPTURE ON"` back next to `BUILD_DATE`, bumped to 2026-09-04. **Every launcher on every PC accepts the next download — no reinstall.** |
| `optimus/install/RUN_HUNTER.bat` | accept-gate on `BUILD_DATE = ` instead of the banner text |
| `optimus/install/INSTALL_OPTIMUS.bat` | v2: BUILD_DATE gate, repairs the launcher on the PC, `pip install "gspread<6"` |
| `optimus/standalone/maps_scraper_standalone.py` | dedupe `Gold Confirmed` + `Grey Fiber Customers`; `_gc(sh)` gspread-6 client; `sync_ghl_status` = five tabs Green/Gold/Grey/Biz/Fiber Biz in the split workbook (needs `ghl_token.txt` on the PC) |

Tests, all green on these exact files: `patches/launcher-sentinel/test_launcher_sentinel.py`,
`patches/dedupe-gold-grey/test_dedupe_goldgrey.py`, `patches/gspread6-client/test_gspread6_client.py`,
`patches/ghl-status/test_ghl_sync.py`.

## To push (any machine allowed to push to the hunter repo — the desktop Claude Code)

    git clone --branch claude/optimus-map-tools-setup-6dcl6o https://github.com/patricksiado-prog/Go-High-Level-MCP-2026-Complete hunter
    cp -r patches/DEPLOY-2026-09-04/optimus/* hunter/optimus/
    cd hunter && git add -A optimus && git commit -m "Un-pin every PC (LAUNCHER_SENTINEL, BUILD_DATE 2026-09-04); launcher/installer gate on BUILD_DATE; scraper dedupe gold+grey, gspread-6 client, five GHL colour tabs" && git push origin claude/optimus-map-tools-setup-6dcl6o

Then, so the EMAILED release link serves the fixed installer (same URL):

    gh release upload installer patches/DEPLOY-2026-09-04/optimus/install/INSTALL_OPTIMUS.bat --clobber

Wait ~3 minutes for the raw CDN, then relaunch a hunter: the console must print
`BUILD_DATE : 2026-09-04`.
