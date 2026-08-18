# BRANCH MAP — where the real work actually lives

Last updated: 2026-08-18

## Why this file exists

`main` is stale. Eight `claude/*` branches carry ~14,000 lines of working code
that has **never been merged**. Every new chat starts from `main`, does not see
that work, and rebuilds it. This is the "forgetting trap" in WORKING_PATTERNS.md
showing up as branch sprawl instead of file churn.

Read this before building anything. The thing you are about to write probably
already exists on one of these branches.

## The branches, most valuable first

| Branch | Lines vs main | What it has | Verdict |
|---|---|---|---|
| `chat-repetitive-questions-9ex5h7` | +10,438 | `optimus/precise_fiber_hunter.py` (4,215 ln), `optimus_api_capture.py`, `optimus_dot_detect.py`, `maps_scraper.py`, standalone scraper, install .bats, 2 test files | **Richest branch. Merge candidate #1.** |
| `claude-md-docs-m4TxE` | +2,289 | `ghl_ai/` AI sales robot (FastAPI + GHL client + Docker + render.yaml), La Porte drip campaign runbooks, SMS campaign docs, `precise_hunter_desktop.py`, `optimus_install_pc.py` | Only branch with the GHL AI robot. Merge candidate #2. |
| `precise-hunter-read-brain-g3ywob` | +644 | `hunter_fixes.py` (safe flush, drift-proof dedup, junk-address filter, building roll-up), `backend_classifier.py`, 2 test files | Bug fixes for known failures. Low risk. |
| `att-fiber-leads-dedupe-lqr67f` | +671 | `dialer_exclusions.json` (489 ln master exclusion list), BRAIN audit notes, canonical lead-counting method | Data + rules, not code. Safe to merge. |
| `fiber-scout-brain-read-ki0fl5` | +482 | `backend_classifier.py`, `scout_dot_score.py` | Superseded by the two branches above. |
| `program-stopping-issue-2dqxko` | +226/-75 | `themapman.py` v11.3.0 — self-healing, never stops on network/API/quota errors | Straight upgrade to a file on main. |
| `ghl-autodialer-research-7f6bzn` | +79/-22 | `fiber_hunter.py` fresh-fiber detection fix + `--scout` mode, BRAIN sheet-ID and Location-ID corrections | Small, already-correct fixes. |
| `lead-gen-software-research-brho9a` | this branch | API key removal, BRAIN corrections, this file | — |

## The single most important idea buried in here

`optimus_api_capture.py` and `backend_classifier.py` both do the same thing:
**stop counting pixels, read the map's own backend JSON.**

The AT&T dealer map answers every "Search this area" with JSON containing, per
lead, the exact `address`, `latitude`, `longitude`, `subscriber_ban`, and
`curr_ntwrk_bld_type_cd` — up to ~3,000 leads per response.

That removes, in one move, every failure mode WORKING_PATTERNS.md documents:
no color-threshold calibration, no HiDPI click drift, no neighbour-popup
mis-reads, no Nominatim 1-req/sec reverse-geocoding bottleneck, no OCR stage.

Colour legend maps to fields directly:
- `subscriber_ban` empty → non-customer → **GREEN, the prize**
- `subscriber_ban` present → existing customer → GREY or GOLD
- `curr_ntwrk_bld_type_cd == "unavailable"` → not lit → skip

### The one open question blocking it
`FIBER_BUILD_CODES` and `COPPER_BUILD_CODES` in `backend_classifier.py` are
still empty sets. Until they are filled, existing customers classify as
`CUSTOMER` instead of splitting into GREY (already sold, skip) vs
GOLD (copper customer, forced FCC upgrade — a real target).

**To fill them:** run `inspect()` over a green-heavy area (the Arbor/Blodgett
Third Ward view is named in the source), read the cross-tab it prints, drop the
codes in. That is a one-session job and it unlocks the gold-dot segment.

## Rule going forward

One branch at a time, merged to `main` before the next chat starts. A chat that
ends with work only on a `claude/*` branch has not shipped — it has hidden.
