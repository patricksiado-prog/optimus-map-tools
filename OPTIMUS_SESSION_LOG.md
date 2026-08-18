# Optimus Session Log

## 2026-05-23 22:03 CT — Claude
**SESSION GOAL:** Fix GitHub-write via Make so it reliably creates AND updates files, document it in the BRAIN, and start timestamp + session-goal stamping.

- Fixed Make scenario 5084486 (GitHub write): SHA read is now non-fatal (handleErrors), and the PUT includes `sha` only when the file already exists — so it creates new files and updates existing ones.
- This file being created here is the proof the create-path works.
- Capability map: GitHub write = Make scenario **5084486**. BRAIN append = Make scenario **5073448**. Both run via update-trigger → activate → run → deactivate.

## 2026-08-18 — Claude (lead-gen-software-research)
**SESSION GOAL:** Full sweep — brain, other chats, repo, Railway, Gmail, Drive, the live sheet — then fix what the sweep exposed.

Findings:
- **Leaked key.** Google Maps/Places key `AIzaSy...kCG9g` was hardcoded in
  themapman.py, mapman_api.py, mapman_api_batch.py, mapman_pydroid_runner.py and
  is in git history. Removed from the working tree; all four now call
  `optimus_secrets.get_maps_api_key()`. **The key itself still has to be rotated
  in Google Cloud — deleting the line does not un-leak it.**
- **Wrong sheet in BRAIN.** BRAIN.md said active sheet was `12PII...`; the code
  actually opens `1FhO...` ("ATT FIBER LEADS", 5.5 MB, last written 2026-08-18).
  Four different sheet IDs are referenced across the .py files. Corrected.
- **Branch sprawl.** 8 unmerged `claude/*` branches, ~14,000 lines, none on main.
  Documented in BRANCH_MAP.md. Richest: `chat-repetitive-questions-9ex5h7` (+10,438).
- **The unlock.** `optimus_api_capture.py` / `backend_classifier.py` read the AT&T
  dealer-map backend JSON (address + lat/lng + subscriber_ban + build-type code)
  instead of counting pixels. Blocked only on filling FIBER_BUILD_CODES /
  COPPER_BUILD_CODES via one `inspect()` run over a green-heavy area.
- **Railway.** Two projects (fulfilling-growth, loving-heart) each run one
  Go-High-Level-MCP-2026-Complete service. Both SUCCESS, both last deployed
  2026-06-30. Duplicate — consolidate to one.

Changed: optimus_secrets.py (new), BRANCH_MAP.md (new), BRAIN.md, .gitignore,
themapman.py, mapman_api.py, mapman_api_batch.py, mapman_pydroid_runner.py
