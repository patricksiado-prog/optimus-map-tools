# GHL <-> Claude Auto-Reply Bridge

Connects GoHighLevel (Optimus Houston / "Frontline Direct") to Claude so inbound
lead texts get an AT&T-fiber sales reply drafted by Claude and sent back through
GHL. The same endpoint can also be used as a Custom Webhook step inside a GHL
workflow.

## How it works

```
Lead texts in
   -> GHL workflow trigger "Customer Replied"
      -> Webhook action POST  ->  /ghl/inbound  (this service)
            1. pulls recent conversation history from GHL (context)
            2. Claude drafts a reply
            3. service posts the reply back via GHL conversations API
```

## Safety: DRY_RUN is ON by default

With `DRY_RUN=true` (the default) the bridge **drafts and returns the reply but
does not send it**. Watch the logs / responses, confirm the replies read well on
a real thread, then set `DRY_RUN=false` to go live. This keeps the 44k-contact
list safe from an accidental blast. Opt-out words (STOP, UNSUBSCRIBE, ...) are
never answered.

## Environment variables

| Var | Required | Default | Notes |
|-----|----------|---------|-------|
| `ANTHROPIC_API_KEY` | yes | - | Claude API key |
| `GHL_TOKEN` | to send | - | GHL Private Integration Token / API key, location-scoped, conversations read+write |
| `GHL_LOCATION_ID` | no | Frontline Direct | location id |
| `CLAUDE_MODEL` | no | `claude-opus-4-8` | set `claude-sonnet-4-6` for cheaper/faster high-volume SMS |
| `CLAUDE_EFFORT` | no | `medium` | `low` \| `medium` \| `high` |
| `GHL_MESSAGE_TYPE` | no | `SMS` | |
| `BRIDGE_SECRET` | no | - | if set, inbound requests must send header `X-Bridge-Secret: <value>` |
| `DRY_RUN` | no | `true` | set `false` to actually send |
| `MAX_REPLY_TOKENS` | no | `400` | SMS-length replies |

## Run locally

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python main.py            # http://127.0.0.1:8080

# smoke test (stays in dry-run, no GHL token needed):
curl -X POST http://127.0.0.1:8080/ghl/inbound \
  -H 'Content-Type: application/json' \
  -d '{"contactId":"test123","body":"is fiber actually available at my house?"}'
```

You get back the drafted reply as JSON. Check `/status` for current config.

## Deploy

### Render (matches the other portals in this repo)

1. Render dashboard -> New -> Blueprint -> pick `patricksiado-prog/optimus-map-tools`.
2. Render reads `ghl_ai/render.yaml`.
3. Set `ANTHROPIC_API_KEY`, `GHL_TOKEN`, and a `BRIDGE_SECRET` when prompted.
4. Apply. You get a URL; the webhook lives at `<url>/ghl/inbound`.

### Docker / Cloud Run

```bash
docker build -t ghl-claude-bridge ghl_ai/
# deploy the image; set the env vars above
```

## Wire it into GHL

1. **Get a token.** GHL -> Settings -> Private Integrations (or API key) for the
   Frontline Direct location, with **conversations** read + write scope. Put it
   in `GHL_TOKEN`.
2. **Build a workflow.** Automation -> Workflows -> new workflow.
   - Trigger: **Customer Replied** (or **Inbound Message**).
   - Action: **Webhook** -> `POST` to `https://<your-url>/ghl/inbound`.
   - Add a custom header `X-Bridge-Secret` matching `BRIDGE_SECRET`.
   - Map the body to include at least `contactId`, `conversationId`, and the
     message `body` (the payload keys are read defensively).
3. **Test in dry-run**, then set `DRY_RUN=false` and re-test on your own number.

## Using Claude inside a workflow step (instead of auto-send)

Keep `DRY_RUN=true`: the endpoint returns `{"reply": "..."}` without sending.
Capture that in the workflow and route it wherever you want (manual approval,
a different channel, etc.).
