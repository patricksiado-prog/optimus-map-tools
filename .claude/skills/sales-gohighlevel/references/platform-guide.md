<!-- Source: https://www.gohighlevel.com/ , https://www.gohighlevel.com/pricing , https://marketplace.gohighlevel.com/docs/ , https://github.com/GoHighLevel/highlevel-api-docs , https://marketplace.gohighlevel.com/docs/webhook/WebhookIntegrationGuide/ — fetched 2026-06 -->

# GoHighLevel (HighLevel) Platform Reference

## Overview

GoHighLevel (now branded **HighLevel**) is an all-in-one "AI-powered business operating system" for agencies, freelancers, and SMBs: CRM + sales pipelines, funnels/websites, multi-channel messaging (email, SMS, WhatsApp, social DMs), workflows/automations, calendars, reputation management, payments, memberships/courses, conversation/voice AI, and — its signature differentiator — **white-label SaaS resale** so agencies can sell the whole platform under their own brand. Sold not by edition features but by **sub-account count + resale rights**. Competes with HubSpot, Keap, Kartra, Systeme.io, Ontraport, and (for agencies) Vendasta.

## Module map (Capture → Nurture → Close → Evangelize → Reactivate)

| Stage | Modules |
|---|---|
| **Capture** | CRM, Forms/Surveys/Quizzes, Websites/Funnels/Landing pages, Webinar funnels, Chat widget, Voice AI, Call tracking, Inbound SMS & social DMs, Social planner, Missed-call text-back, Ad manager |
| **Nurture** | Conversation AI, unified inbox (SMS/Messenger/IG DM/WhatsApp/LiveChat), Sales pipelines, Workflows & automations, Calendars, Appointment reminders, Ringless voicemail, Mobile app |
| **Close** | Lead scoring, Estimates & proposals, Invoicing, Payments, Paid calendars, Order forms, Upsells/downsells, Memberships/courses, Text-2-Pay, Gift cards, Loyalty |
| **Evangelize** | Reputation management, Automated review requests, AI review reply, Affiliate manager, Review widgets, Communities |
| **Reactivate** | Broadcast campaigns (email/SMS/WhatsApp/Messenger), Smart lists/segmentation, Birthday/seasonal campaigns, Newsletter automation, Content AI |

## Key terminology

- **Agency** (top level) → **Sub-Accounts** (a.k.a. **Locations**, one per client/business). Most API calls are scoped to a `locationId`.
- **Snapshot** — a reusable template of a sub-account's setup (pipelines, workflows, funnels, calendars). Build once, deploy to every client.
- **SaaS mode** — resell GHL under your brand with the SaaS configurator + Stripe rebilling (SaaS Pro plan).
- **LeadConnector (LC)** — the underlying phone/email infrastructure; usage (SMS/email/phone/AI) is metered here on top of the plan.

## Capabilities & automation surface

| Capability | Automation surface |
|---|---|
| Contacts, Opportunities, Conversations, Calendars, Payments | **API v2 + webhooks** |
| Workflows / automations (internal) | UI builder (can call webhooks / custom code steps) |
| Funnels, websites, forms | UI; submissions trigger workflows + webhooks |
| Reputation / reviews | UI + API + webhooks (review events) |
| Sub-account / snapshot management | API (agency-scoped) + UI |
| SaaS-mode rebilling | UI (SaaS Pro) |
| Voice/Conversation AI | UI config; events surface via webhooks |
| MCP server | None official found |

## Pricing, limits & plan gates

> Best-effort (2026-06) — verify on the live pricing page. Usage (SMS/email/phone/AI via LeadConnector) is billed **separately** on top of every plan.

| Plan | Price | Sub-accounts | Notable gates |
|---|---|---|---|
| **Starter** | $97/mo | 3 | Full CRM + funnels + email/SMS + calendars + reputation; **no white-label, no SaaS resale** |
| **Unlimited** | $297/mo | Unlimited | **White-label** the platform, advanced reporting, custom menu links, rebill usage |
| **SaaS Pro** | $497/mo | Unlimited | Everything in Unlimited **+ SaaS configurator + automated Stripe billing + usage-based rebilling** (resell as your own SaaS) |

All plans: unlimited contacts + users, 14-day trial. **API rate limit: 100 requests / 10 seconds (burst, per resource/location)** plus a daily cap — see api-reference.

## Integrations

- **API v2** (`services.leadconnectorhq.com`) — contacts, opportunities, conversations, calendars, payments, etc. OAuth 2.0 (Marketplace apps) or Private Integration Tokens (internal).
- **Outbound webhooks** — 50+ events; Ed25519-signed (`X-GHL-Signature`).
- **Marketplace apps** — public apps distributed via the HighLevel Marketplace.
- **iPaaS** — Zapier, Make, Pabbly, n8n (community); plus native integrations (payments via Stripe/PayPal/Square/Authorize.net/NMI, Google/Outlook calendar, QuickBooks, Shopify, social platforms).
- **Inbound webhooks / custom code** — workflow steps can POST to external systems and run custom code.

## Data model (representative)

> Shapes assembled from documented fields/endpoints — verify against the live v2 docs.

**Contact** (POST `/contacts/`):
```json
{
  "firstName": "Jane",
  "lastName": "Smith",
  "email": "jane@example.com",
  "phone": "+14155551234",
  "locationId": "YOUR_LOCATION_ID",
  "source": "shopify-integration",
  "tags": ["new-customer", "shopify"],
  "customFields": [{ "id": "CUSTOM_FIELD_ID", "field_value": "1" }]
}
```

**Webhook envelope** (outbound POST to your endpoint):
```json
{
  "type": "ContactCreate",
  "timestamp": "2026-06-19T12:00:00.000Z",
  "webhookId": "a1b2c3d4-...",
  "data": { "id": "contactId", "locationId": "...", "email": "jane@example.com" }
}
```

## Quick-start recipes

### Recipe 1 — Upsert a contact into a sub-account (v2 API + Private Integration Token)
```bash
# Private Integration Token from Sub-account Settings → Private Integrations (scope: contacts.write)
curl -X POST "https://services.leadconnectorhq.com/contacts/" \
  -H "Authorization: Bearer $GHL_PIT" \
  -H "Version: 2021-07-28" \
  -H "Content-Type: application/json" \
  -d '{
        "locationId": "'$GHL_LOCATION_ID'",
        "email": "jane@example.com",
        "firstName": "Jane",
        "tags": ["app-signup"],
        "source": "my-app"
      }'
```
```python
import os, requests
H = {"Authorization": f"Bearer {os.environ['GHL_PIT']}",
     "Version": "2021-07-28", "Content-Type": "application/json"}
body = {"locationId": os.environ["GHL_LOCATION_ID"], "email": "jane@example.com",
        "firstName": "Jane", "tags": ["app-signup"], "source": "my-app"}
r = requests.post("https://services.leadconnectorhq.com/contacts/", headers=H, json=body)
# Upsert-by-email avoids dupes; on 429 back off and retry (limit: 100 req / 10s)
print(r.status_code, r.json())
```
**Gotchas:** the `Version` header is mandatory; `locationId` scopes the write; throttle to 100/10s.

### Recipe 2 — Verify an inbound webhook (Ed25519) and dedupe
```python
from flask import Flask, request, abort
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
import base64, json

app = Flask(__name__)
# Published HighLevel Ed25519 public key (verify current value in the webhook docs)
PUB_B64 = "MCowBQYDK2VwAyEAi2HR1srL4o18O8BRa7gVJY7G7bupbN3H9AwJrHCDiOg="
SEEN = set()

@app.post("/hooks/ghl")
def ghl():
    sig = request.headers.get("X-GHL-Signature")     # Ed25519 (current); X-WH-Signature RSA is deprecated 2026-07-01
    raw = request.get_data()
    try:
        # public key is SubjectPublicKeyInfo DER, base64-encoded
        from cryptography.hazmat.primitives.serialization import load_der_public_key
        load_der_public_key(base64.b64decode(PUB_B64)).verify(base64.b64decode(sig), raw)
    except Exception:
        abort(401)
    evt = json.loads(raw)
    if evt["webhookId"] in SEEN:           # retries fire up to 12x with backoff → dedupe
        return ("dup", 200)
    SEEN.add(evt["webhookId"])
    # handle evt["type"] / evt["data"] ...
    return ("ok", 200)                      # respond 2xx fast so GHL doesn't retry
```
**Gotchas:** verify against the **Ed25519** key (not the legacy RSA one); respond 2xx quickly; dedupe on `webhookId`.

### Recipe 3 — Agency rollout: snapshot → many sub-accounts
1. Build one sub-account fully (pipelines, workflows, calendars, funnels, review requests).
2. Save it as a **Snapshot** (Agency view → Account Snapshots).
3. Create each client sub-account from the snapshot (UI or agency-scoped API) so every client starts identical.
4. On **Unlimited** white-label the UI; on **SaaS Pro** turn on SaaS mode + Stripe rebilling to resell and mark up usage.

## Integration patterns

- **Auth choice:** Private Integration Token for your own internal/sub-account tools (fast, scoped); Marketplace OAuth app for public multi-account distribution (token refresh, install flow).
- **Scope discipline:** issue PITs with exactly the scopes you need; expect 403s if under-scoped or pointed at the wrong `locationId`.
- **Throughput:** queue + pace writes under 100/10s; backoff on 429; spread bulk work across locations.
- **Eventing:** prefer webhooks (Ed25519-verified, idempotent on `webhookId`) over polling; reconcile periodically via the API since delivery is at-least-once.

## Fit vs. alternatives

| Need | Better fit |
|---|---|
| All-in-one CRM + funnels + messaging + **white-label SaaS resale** for an agency | **GoHighLevel** |
| Inbound marketing + mature CRM, less agency/resale focus | `/sales-crm-selection` → HubSpot |
| Just multi-step funnels/checkout (no agency layer) | `/sales-funnel` (ClickFunnels, Kartra, Systeme.io) |
| Lightweight, API-first CRM for a small team | `/sales-crm-selection` → Attio / Pipedrive |
