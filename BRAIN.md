# Optimus BRAIN

_Last updated: 2026-06-02 (GHL contact count refreshed from live API)_

## Active systems
- GitHub repo: patricksiado-prog/optimus-map-tools
- Active sheet: 12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag
- GHL Houston Location: TXw28sw0Z2rl6tcCDhJY — "Frontline Direct" (44,523 contacts as of 2026-06-02, up from ~41,325 on 2026-05-02)
- Service account: fiberscanner@fiberscanner-493900.iam.gserviceaccount.com
- Map Man v10
- Drive mirror: 1u38EOzaGO7Sd5Y8ERqQoXeYZW5Pws8Z_

## Phase targets
- Phase 1: 500 sales/week
- Phase 2: 1000/week
- Phase 3: 2000/week

## Run log
(append new entries below this line)

- 2026-06-02 — GHL contacts at 44,523 (live API, location Frontline Direct TXw28sw0Z2rl6tcCDhJY). Up +3,198 since 2026-05-02 baseline of ~41,325. Newest 100 all added 2026-06-01 via CSV import through the GHL CRM UI; allowDuplicateContact=false so the gain is net-new (deduped on email+phone).
- 2026-06-02 — Added `ghl_ai/` GHL<->Claude auto-reply bridge (Flask, deployable on Render/Cloud Run like the other portals). GHL workflow webhook -> /ghl/inbound -> Claude drafts an AT&T fiber SMS reply -> sent back via GHL conversations API. Model claude-opus-4-8 (CLAUDE_MODEL overridable). DRY_RUN defaults TRUE (drafts only, no send) to protect the 44k list; opt-out words never answered. Secrets via env vars (ANTHROPIC_API_KEY, GHL_TOKEN, BRIDGE_SECRET). Setup steps in ghl_ai/README.md.
- 2026-06-02 — Created GHL Private Integration "claude11" for the Connect & Comm sub-account (location xZj500PjsflIQg2j9f9D). Frontline Direct (TXw28sw0Z2rl6tcCDhJY) stays on the session connector.

## GHL Private Integration Tokens
(Saved here at Patrick's explicit request. NOTE: this file is pushed to GitHub and mirrored to Drive, so these tokens are exposed in those places + in git history. Rotate in GHL -> Settings -> Private Integrations if that becomes a problem.)
(Tokens can't be verified from the Claude container — outbound to GHL is blocked. Clean transcriptions from Patrick's doc, for the deployed bridge / MCP setup.)
- Frontline Direct (TXw28sw0Z2rl6tcCDhJY) — "claude" (read-only): pit-88412578-4972-47af-a6bc-8fc71824693e
- Frontline Direct (TXw28sw0Z2rl6tcCDhJY) — "claude-writes" (ALL scopes incl WRITE, 2026-06-06): pit-9b15a452-5250-4c33-bacc-0bd749046f1d  <-- put this in Railway GHL_API_KEY for ghl-full write
- Connect & Comm (xZj500PjsflIQg2j9f9D) — "claude11": pit-ca275b6d-4ec1-4e44-bcc5-29be36035950
- Account UNCONFIRMED (likely Connect & Comm): pit-d04904c8-9e39-4023-88df-e60fa0cff61e
- GHL MCP endpoint: https://services.leadconnectorhq.com/mcp/
- Self-hosted "fuller" GHL MCP (Go-High-Level-MCP-2026-Complete, deployed on Railway, 2026-06-04): https://go-high-level-mcp-2026-complete-production-46d1.up.railway.app  (env vars set: GHL_API_KEY=Frontline pit, GHL_LOCATION_ID=TXw28sw0Z2rl6tcCDhJY, public domain mapped to port 8080). Connect path is /mcp. CONNECTED to Claude as custom connector "ghl-full" 2026-06-04 (654 tools, status Needs-approval). Add via Claude app Settings -> Connectors -> Add custom connector -> URL .../mcp (no token in the connector; server holds it).

<!-- REPO_LOG_BRAIN_THINK_ACT_RECORD_START -->
## OPERATING RULE - REPO LOG BRAIN THINK ACT RECORD

Date added: 2026-05-02

Rule:
Before answering or doing anything new on Optimus / AT&T / fiber / GHL / Sheets / GitHub / app-builder work:

REPO -> LOG -> BRAIN -> THINK -> ACT -> RECORD

Meaning:
1. Read repo/context first when available.
2. Check logs/history before changing code.
3. Read BRAIN before acting.
4. Think through the task before speaking or editing.
5. Act only after understanding the current source/context.
6. Record important changes, rules, scripts, repo updates, file links, and fixes back into BRAIN.

Source of truth:
- Repo: patricksiado-prog/optimus-map-tools
- Short brain: BRAIN.md
- Full context: BRAIN_FULL_CONTEXT.md
- Drive brain: Optimus Scripts Notes 2026-05-02
- Drive mirror file: BRAIN.md

Important:
- Do not guess from memory if repo/BRAIN/context is available.
- Do not create workaround files when the correct move is to fix the real repo/BAT/program.
- If GitHub connector is unavailable, use Drive BRAIN, Drive mirror files, and uploaded repo bundle until live GitHub access is fixed.
<!-- REPO_LOG_BRAIN_THINK_ACT_RECORD_END -->
