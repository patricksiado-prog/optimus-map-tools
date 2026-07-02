# Optimus Session Log

## 2026-07-02 — Claude
**SESSION GOAL:** Fix themapman.py "keeps stopping" — make it self-healing so phone network blips, Sheets quota, and API errors never kill a run.

- themapman.py v11.2.5 → **v11.3.0** (patched, not rewritten — same tabs, columns, flow):
  - All Google API calls (geocode/nearby/details) now retry with exponential backoff instead of failing the row on one dropped connection.
  - Transient failures are queued and retried in later passes, NOT written to the sheet — fixes the poisoning bug where a network blip wrote rows as GEOCODE_FAILED/NO_TENANT_FOUND and the resume logic then skipped those leads forever.
  - Sheets connection self-heals: startup connect retries forever with backoff; mid-run write failures reconnect + re-auth. 429/quota errors now wait 65s (write quota resets per minute — the old 3 quick retries could never survive it).
  - OVER_QUERY_LIMIT / REQUEST_DENIED from Places API pause + retry instead of plowing through marking everything NO_TENANT_FOUND.
  - A row that keeps failing while OTHERS succeed gets recorded as ERROR after 5 tries (a global outage never burns strikes — the loop just waits for the network to come back).
- Pydroid tip recorded in the script header: if the run vanishes with no error, it's Android killing Pydroid — enable "Keep screen on" + set Pydroid battery to Unrestricted.
- Note: old rows already stamped GEOCODE_FAILED by v11.2.5 during blips stay skipped; delete those rows from "Fiber Commercial Leads" to have v11.3.0 retry them.

## 2026-05-23 22:03 CT — Claude
**SESSION GOAL:** Fix GitHub-write via Make so it reliably creates AND updates files, document it in the BRAIN, and start timestamp + session-goal stamping.

- Fixed Make scenario 5084486 (GitHub write): SHA read is now non-fatal (handleErrors), and the PUT includes `sha` only when the file already exists — so it creates new files and updates existing ones.
- This file being created here is the proof the create-path works.
- Capability map: GitHub write = Make scenario **5084486**. BRAIN append = Make scenario **5073448**. Both run via update-trigger → activate → run → deactivate.
