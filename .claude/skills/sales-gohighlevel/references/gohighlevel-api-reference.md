<!-- Source: https://marketplace.gohighlevel.com/docs/ , https://github.com/GoHighLevel/highlevel-api-docs , https://marketplace.gohighlevel.com/docs/webhook/WebhookIntegrationGuide/ , https://marketplace.gohighlevel.com/docs/Authorization/DeveloperGlossary — fetched 2026-06. Some concrete endpoint paths corroborated by third-party integration guides (ecosire.com, ghllogic.com); marked where so. -->

# GoHighLevel (HighLevel) API v2 Reference

## Overview

- **Base URL:** `https://services.leadconnectorhq.com`
- **API version:** v2 (v1 / `rest.gohighlevel.com` is legacy — build on v2)
- **Auth:** OAuth 2.0 (Marketplace apps) **or** Private Integration Tokens (internal tools)
- **Official docs:** https://marketplace.gohighlevel.com/docs/ · public docs repo: https://github.com/GoHighLevel/highlevel-api-docs
- **Dev community:** https://developers.gohighlevel.com/join-dev-community

## Required headers

| Header | Value |
|---|---|
| `Authorization` | `Bearer <access_token or Private Integration Token>` |
| `Version` | `2021-07-28` (**required** on v2 calls; other dated versions exist — pin one) |
| `Content-Type` | `application/json` |

## Authentication

### Private Integration Tokens (PIT)
Generated directly in **Agency** or **Sub-account → Settings → Private Integrations**, with granular scopes (e.g. `contacts.readonly`, `contacts.write`, `opportunities.write`, `conversations/message.write`). Best for internal/single-org tools — no OAuth install flow. Send as `Authorization: Bearer <PIT>`.

### OAuth 2.0 (Marketplace apps)
For public / multi-account apps distributed via the HighLevel Marketplace.
- **Authorize:** `https://marketplace.gohighlevel.com/oauth/chooselocation?response_type=code&redirect_uri=YOUR_CALLBACK&client_id=YOUR_CLIENT_ID&scope=...`
- **Token:** `POST https://services.leadconnectorhq.com/oauth/token`
  - body: `client_id`, `client_secret`, `grant_type=authorization_code`, `code=AUTH_CODE`, `redirect_uri`
  - refresh: `grant_type=refresh_token` + `refresh_token`
- Tokens are issued per **location** (sub-account) or per **company** (agency) depending on the chosen scope/flow.

## Scoping: locationId

Most resources are scoped to a **sub-account** via `locationId` (query param or body field). A token scoped to one sub-account cannot read another. Agency-level operations (creating sub-accounts, snapshots) use agency-scoped tokens.

## Rate limits

- **Burst:** **100 requests / 10 seconds** (per resource, per location/marketplace-app). <!-- corroborated by ecosire.com & ghllogic.com -->
- **Daily:** a per-app/day cap also applies (commonly cited ~200,000/day — verify against current docs).
- On `429`, back off exponentially with jitter and retry.

## Pagination

Responses include a `meta` object (`total`, `currentPage`, `nextPage`) and/or cursor-based `startAfterId` (+ `startAfter` timestamp) for list endpoints. Follow `nextPage`/`startAfterId` until exhausted. <!-- shape per ecosire.com; confirm per-endpoint in official docs -->

## Core endpoints (v2)

> Paths corroborated by third-party guides; confirm exact request/response schemas in the official docs before building.

| Resource | Method | Path |
|---|---|---|
| Create/update contact | POST | `/contacts/` |
| Get contact | GET | `/contacts/{contactId}` |
| Search contacts | GET | `/contacts/search?locationId=...&email=...` |
| Add tags to contact | POST | `/contacts/{contactId}/tags` |
| Create opportunity | POST | `/opportunities/` |
| Update opportunity | PUT | `/opportunities/{id}` |
| Search opportunities | GET | `/opportunities/search?location_id=...` |
| Send message (SMS/email) | POST | `/conversations/messages` |
| Calendars / availability / book | GET/POST | `/calendars/...` (fetch slots, create appointment) |
| Payments / invoices / orders | (various) | `/payments/...`, `/invoices/...` |

### Example: create a contact
```bash
curl -X POST "https://services.leadconnectorhq.com/contacts/" \
  -H "Authorization: Bearer $GHL_TOKEN" \
  -H "Version: 2021-07-28" \
  -H "Content-Type: application/json" \
  -d '{
        "locationId": "YOUR_LOCATION_ID",
        "firstName": "Jane",
        "lastName": "Smith",
        "email": "jane@example.com",
        "phone": "+14155551234",
        "source": "shopify-integration",
        "tags": ["new-customer", "shopify"],
        "customFields": [{ "id": "CUSTOM_FIELD_ID", "field_value": "1" }]
      }'
```

## Webhooks

Outbound webhooks POST JSON to your configured URL when platform events occur (contact created/updated/deleted, tag changes, opportunity lifecycle, tasks, appointments, invoices, products, associations, location/user events — 50+ types).

### Payload envelope
```json
{
  "type": "ContactCreate",
  "timestamp": "2026-06-19T12:00:00.000Z",
  "webhookId": "a1b2c3d4-...",
  "data": { "id": "...", "locationId": "...", "...": "event-specific" }
}
```

### Signature verification
Two headers may be present:

- **`X-GHL-Signature` — Ed25519 (current standard).** Verify the signature over the raw request body using the published public key:
  ```
  MCowBQYDK2VwAyEAi2HR1srL4o18O8BRa7gVJY7G7bupbN3H9AwJrHCDiOg=
  ```
  (SubjectPublicKeyInfo DER, base64-encoded — re-confirm the current key in the webhook docs.)
- **`X-WH-Signature` — RSA-SHA256 (legacy).** **Deprecated 2026-07-01** — migrate to Ed25519 before then.

### Retries & delivery
Failed deliveries (non-`2xx`) retry with **exponential backoff up to 12 times**, with random jitter to avoid retry storms. Delivery is therefore **at-least-once** — make handlers idempotent on `webhookId` and respond `2xx` quickly. Already-exhausted deliveries can be replayed manually from the **Webhook Logs Dashboard**.

## SDKs & tools

- Official docs repo (request/response examples, error codes, models): `github.com/GoHighLevel/highlevel-api-docs`
- Community SDKs exist for Node/Python; many builders call the REST API directly or via Zapier/Make/n8n.

## Gaps (verify against official docs before relying)

- Exact request/response **schemas and field-level detail** per endpoint (use the docs repo `models/`).
- The precise **daily** rate-limit number and any per-endpoint limits.
- Full **scope list** for PIT/OAuth.
- Per-endpoint **pagination** specifics (cursor vs page) — varies by resource.
- Whether the published **Ed25519 public key** has rotated since 2026-06.
