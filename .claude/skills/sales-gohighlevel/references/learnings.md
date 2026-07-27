# GoHighLevel (HighLevel) Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-19**: Research baseline — modules, sub-account/snapshot model, pricing tiers, v2 API surface, and webhook security captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-06-19**: API v2 essentials — base `https://services.leadconnectorhq.com`, mandatory `Version: 2021-07-28` header, auth via OAuth 2.0 (Marketplace apps; authorize at marketplace.gohighlevel.com/oauth/chooselocation, token at /oauth/token) OR Private Integration Tokens (scoped, generated in Agency/Sub-account settings). Most resources scoped to `locationId`. Rate limit 100 req/10s burst per resource/location (+ a daily cap, ~200K commonly cited — unverified). Pagination via `meta`/`startAfterId`. v1 (`rest.gohighlevel.com`) is legacy.

**2026-06-19**: Webhooks — outbound POST with envelope `{type, timestamp, webhookId, data}`, 50+ event types. Verify the **Ed25519 `X-GHL-Signature`** with published public key `MCowBQYDK2VwAyEAi2HR1srL4o18O8BRa7gVJY7G7bupbN3H9AwJrHCDiOg=`. Legacy RSA-SHA256 `X-WH-Signature` is **deprecated 2026-07-01**. Retries up to 12× exponential backoff + jitter → at-least-once; dedupe on `webhookId`, respond 2xx fast. Manual replay via Webhook Logs Dashboard.

**2026-06-19**: Pricing best-effort — Starter $97 (3 sub-accounts, no white-label), Unlimited $297 (unlimited sub-accounts + white-label), SaaS Pro $497 (SaaS resale + Stripe rebilling). Usage (SMS/email/phone/AI via LeadConnector) billed separately on top. Agency model = sub-accounts (locations) + snapshots (templates) + SaaS mode. Verify live; third-party pricing pages vary.

**2026-06-19**: Note — official marketing pages (gohighlevel.com/*, /alternatives) are JS-rendered / often 404 to WebFetch; the API docs repo (github.com/GoHighLevel/highlevel-api-docs) and marketplace.gohighlevel.com/docs are the better sources. Exact endpoint request/response schemas live in the repo's `models/` and `docs/`.
