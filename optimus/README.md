# optimus/ — Fiber Hunter / Scraper / Scout programs

Production source for the three Optimus desktop programs, copied here so they
live alongside the rest of the tooling and are backed up in one place.

## Source
Copied verbatim from the repo the desktop installer pulls from:
`patricksiado-prog/Go-High-Level-MCP-2026-Complete`,
branch `claude/optimus-map-tools-setup-6dcl6o`, folder `optimus/`.

## Programs
| File | What it is |
|------|-----------|
| `precise_fiber_hunter.py` | v0.4 — Playwright "click every dot" exact-address grabber (drives the AT&T fiber map, reads popups, writes the Precise Fiber tab). |
| `fiber_scout.py` | Surveys an area for NEW fiber (lots of green + gold, little/no grey). |
| `maps_scraper.py` | v1.0 self-contained Google Maps business scraper (names + phones by ZIP). |
| `standalone/maps_scraper_standalone.py` | Standalone build the scraper installer downloads and runs. |

## Shared modules
| File | What it is |
|------|-----------|
| `optimus_dot_detect.py` | Screenshot dot-detection helpers. |
| `optimus_api_capture.py` | Network/API lead capture. |
| `hunter_fixes.py` | SafePending (write-before-delete), canonical-address deduper, junk blocker, apartment roll-up, phone normalizer. |
| `backend_classifier.py` | Classifies dealer-map JSON leads (GREEN/GOLD/GREY/CUSTOMER/SKIP). |
| `build_codes.json` | Fiber/copper build-code config. |

## Tests
`test_hunter_fixes.py`, `test_backend_classifier.py` — run with `python3 test_hunter_fixes.py`.

## Launchers (`install/`)
Windows `.bat` launchers that auto-update from GitHub and run each program.
Note: these currently point at the `Go-High-Level-MCP-2026-Complete` raw URLs
(the original install source); left as-is for reference.
