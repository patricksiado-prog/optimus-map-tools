---
name: sales-gohighlevel
description: "GoHighLevel (HighLevel) platform help — all-in-one agency/SMB business OS: CRM + sales pipelines, funnels/websites, email/SMS/WhatsApp, workflows, calendars, reputation, payments, memberships, conversation AI, and white-label SaaS resale (gohighlevel.com). Covers the v2 REST API (base services.leadconnectorhq.com, OAuth 2.0 or Private Integration Tokens, required dated API-Version header), 50+ outbound webhooks (Ed25519 X-GHL-Signature), and sub-accounts/snapshots. Use when building a v2 API or webhook integration, a Private Integration Token's scopes are too narrow, hitting the 100-requests/10-second rate limit, syncing contacts/opportunities/conversations into or out of GHL, verifying webhook signatures, setting up sub-accounts or snapshots for clients, configuring SaaS-mode rebilling, or choosing between the Starter, Unlimited, and SaaS Pro plans. Do NOT use for choosing a CRM across vendors (use /sales-crm-selection) or funnel strategy across tools (use /sales-funnel)."
argument-hint: "[describe what you need help with in GoHighLevel]"
license: MIT
version: 1.0.3
tags: [sales, crm, all-in-one, agency, platform]
github: "https://github.com/GoHighLevel"
---

# GoHighLevel (HighLevel) Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Build a v2 API integration — contacts, opportunities, conversations, calendars, payments
   - B) Set up webhooks — 50+ events, signature verification, retries
   - C) Pick the auth model — Private Integration Token (internal) vs Marketplace OAuth app (public/multi-account)
   - D) Agency setup — sub-accounts (locations), snapshots, white-label, SaaS-mode rebilling
   - E) Automate inside GHL — workflows, pipelines, smart lists, conversation/voice AI
   - F) Wire GHL to other tools — Zapier/Make, native integrations, custom middleware
   - G) Pick a plan — Starter $97 vs Unlimited $297 vs SaaS Pro $497
   - H) Something else — describe it

2. **Agency or single business?** Reselling to clients (sub-accounts, white-label, SaaS mode) vs running your own one business — drives plan + architecture.

3. **Where does data need to flow?** Stay in GHL / sync to a CRM or warehouse / drive an external app — drives API vs webhook vs Zapier.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Choosing a CRM across vendors (GHL vs HubSpot vs Attio…) | `/sales-crm-selection {question}` |
| Multi-step funnel strategy across tools | `/sales-funnel {question}` |
| Email marketing strategy (deliverability, sequences) | `/sales-email-marketing {question}` |
| SMS marketing strategy / compliance | `/sales-sms-marketing {question}` |
| Appointment-scheduling strategy across tools | `/sales-meeting-scheduler {question}` |
| Reviews / reputation strategy | `/sales-customer-reviews {question}` |
| Chatbot / conversational marketing strategy | `/sales-chatbot {question}` |
| Connecting GHL to other tools (architecture) | `/sales-integration {question}` |

When routing, give the exact command.

## Step 3 — GoHighLevel platform reference

**Read `references/platform-guide.md`** for the full reference — the Capture/Nurture/Close/Evangelize/Reactivate module map, sub-account/location/snapshot model, pricing and plan gates, integrations, and quick-start recipes (sync contacts via the v2 API + Private Integration Token; verify an Ed25519 webhook; agency sub-account + snapshot rollout).

**Read `references/gohighlevel-api-reference.md`** for the v2 API — base `https://services.leadconnectorhq.com`, OAuth 2.0 vs Private Integration Tokens, the required `Version: 2021-07-28` header, the 100-request/10-second rate limit, `meta`/`startAfterId` pagination, core endpoints (contacts, opportunities, conversations/messages, calendars, payments), and the webhook signature scheme (Ed25519 `X-GHL-Signature` + public key; legacy RSA `X-WH-Signature` deprecating 2026-07-01).

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Use API v2** (`services.leadconnectorhq.com`) and **always send the `Version: 2021-07-28` header** — v1 keys/endpoints are legacy.
- **Pick the auth model deliberately:** a **Private Integration Token** (generated in Agency or Sub-account settings, scoped) is simplest for your own internal tools; a **Marketplace OAuth app** is for public/multi-account distribution. Most resources are scoped to a **`locationId`** (sub-account) — agency-level calls differ.
- **Throttle to the 100-requests/10-second burst limit** (per resource/location) — batch, cache `describe`-style lookups, and use exponential backoff on `429`.
- **Verify webhooks with Ed25519** (`X-GHL-Signature` + the published public key). The legacy RSA `X-WH-Signature` is **deprecated 2026-07-01** — migrate before then. Make handlers idempotent (retries fire up to 12× with backoff).
- **Usage is billed on top of the plan** — email/SMS/phone run through LeadConnector; SaaS-mode rebilling (SaaS Pro) marks up client usage. White-label needs Unlimited+; reselling as your own SaaS needs SaaS Pro.
- **Snapshots** are the agency superpower — build a sub-account template once, deploy to every client.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing which change frequently.*

1. **Most v2 endpoints require a `locationId`** (sub-account scope). Agency-level vs location-level tokens and calls are different — a token scoped to one sub-account can't read another.
2. **The `Version: 2021-07-28` header is mandatory** on v2 calls — omitting it returns errors. (Other dated versions exist; pin one.)
3. **Rate limit is 100 requests / 10 seconds (burst, per resource/location)**, plus a daily cap. Bulk jobs need throttling + backoff; spread work across locations where possible.
4. **Webhook signatures are migrating.** Current = Ed25519 `X-GHL-Signature`; legacy = RSA-SHA256 `X-WH-Signature`, **deprecated 2026-07-01**. Verify with the published Ed25519 public key, not the old RSA one.
5. **Private Integration Token scopes are granular and easy to under-scope** — a "Contacts read-only" token will 403 on writes. Re-issue with the scopes you actually need.
6. **API v1 is legacy.** Old `rest.gohighlevel.com`/v1 API keys still float around in tutorials; build on v2 (`services.leadconnectorhq.com`).
7. **Usage costs are separate and add up** — SMS/email/phone/AI are metered through LeadConnector on top of the $97/$297/$497 plan price. SaaS-mode rebilling is how agencies profit on that usage.
8. **Plan gates:** white-label branding needs **Unlimited ($297)**; reselling GHL as your own SaaS (SaaS configurator + Stripe rebilling) needs **SaaS Pro ($497)**. Starter ($97) caps you at 3 sub-accounts and no white-label.

## Related skills

- `/sales-crm-selection` — CRM comparison and selection (GoHighLevel vs HubSpot, Attio, Salesforce, and others)
- `/sales-funnel` — Funnel strategy across tools (GoHighLevel is one of the funnel builders covered)
- `/sales-email-marketing` — Email marketing strategy (sequences, deliverability)
- `/sales-sms-marketing` — SMS marketing strategy and compliance
- `/sales-meeting-scheduler` — Appointment scheduling strategy across tools
- `/sales-customer-reviews` — Reputation and review-generation strategy
- `/sales-integration` — Connecting GoHighLevel to other tools (webhooks, Zapier, Make, middleware)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Sync new app signups into a GHL sub-account (developer/automation)
**User says**: "When someone signs up in my app, I want to create or update their contact in my GoHighLevel sub-account and tag them. What's the cleanest API setup?"
**Skill does**: Recommends a **Private Integration Token** (Sub-account settings → scoped to Contacts write) over a full OAuth app for an internal tool. Shows the v2 call: `POST https://services.leadconnectorhq.com/contacts/` with `Authorization: Bearer <PIT>`, `Version: 2021-07-28`, `Content-Type: application/json`, and a body including `locationId`, `email`, `tags`, and `customFields` (Recipe 1 in `references/platform-guide.md`). Notes the 100-req/10s limit and to upsert by email to avoid duplicates.
**Result**: User has a scoped token and a working create/update-contact integration.

### Example 2: Verify a GHL webhook and react to opportunity changes (developer)
**User says**: "I'm receiving GoHighLevel webhooks but I'm not sure how to verify they're authentic, and some seem to arrive twice."
**Skill does**: Explains the payload shape (`type`, `timestamp`, `webhookId`, `data`) and verification: compute/verify the **Ed25519 `X-GHL-Signature`** against the published public key (legacy RSA `X-WH-Signature` is deprecated 2026-07-01). For duplicates, notes retries fire up to 12× with exponential backoff + jitter, so dedupe on `webhookId` and respond `2xx` quickly (Recipe 2). Points to the Webhook Logs Dashboard for manual replay.
**Result**: User verifies signatures correctly and handles at-least-once delivery idempotently.

### Example 3: Agency rollout — sub-accounts, snapshots, and SaaS-mode rebilling
**User says**: "I run an agency with 20 clients. How should I set up GoHighLevel so each client has their own setup, and can I resell it under my brand?"
**Skill does**: Maps it to **Unlimited ($297)** for unlimited sub-accounts + white-label, or **SaaS Pro ($497)** to resell GHL as your own SaaS with the SaaS configurator + Stripe rebilling. Recommends building one **snapshot** (pipelines, workflows, calendars, funnels) and deploying it to each client sub-account. Flags that SMS/email/phone usage is metered and SaaS-mode rebilling lets you mark it up.
**Result**: User has a plan choice and a snapshot-driven multi-client architecture.

## Troubleshooting

### API calls return 401/403 or "insufficient scope"
**Symptom**: Requests fail with unauthorized/forbidden errors or scope messages, even with a valid-looking token.
**Cause**: Token type/scope mismatch — a Private Integration Token under-scoped (e.g., read-only on a write call), a token scoped to a different sub-account/`locationId`, an expired OAuth access token, or a missing `Version` header.
**Solution**: Re-issue the Private Integration Token with the exact scopes needed and confirm it's the right sub-account; for OAuth, refresh the access token and confirm the granted scopes. Always send `Version: 2021-07-28` and the correct `locationId`. Build on v2 (`services.leadconnectorhq.com`), not legacy v1.

### Hitting rate limits (429 Too Many Requests)
**Symptom**: Bulk syncs or busy integrations start returning 429s.
**Cause**: The burst limit is 100 requests / 10 seconds per resource/location (plus a daily cap). Tight loops and unbatched syncs blow through it.
**Solution**: Add client-side throttling to stay under 100/10s, use exponential backoff with jitter on 429, cache rarely-changing lookups, and spread work across locations/time. For large migrations, queue and pace the writes rather than firing them all at once.

### Webhooks aren't verifying or seem to arrive twice
**Symptom**: Signature checks fail, or your system processes the same event multiple times.
**Cause**: Verifying against the wrong scheme/key (the RSA `X-WH-Signature` is deprecated 2026-07-01) or not handling retries — failed deliveries retry up to 12× with backoff.
**Solution**: Verify the **Ed25519 `X-GHL-Signature`** with the published public key. Respond `2xx` fast (do slow work async) so GHL doesn't retry, and dedupe on `webhookId` to make processing idempotent. Use the Webhook Logs Dashboard to inspect/replay deliveries.
