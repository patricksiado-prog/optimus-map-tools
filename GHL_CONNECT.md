# Connect Claude to GoHighLevel (GHL)

Copy this to a teammate so their Claude can **control GHL** — read/write contacts,
send texts, tag leads, manage conversations and opportunities.

## What you need
1. **Claude Code** installed (`npm install -g @anthropic-ai/claude-code`), or the
   Claude desktop/web app that supports custom connectors.
2. A **GHL Private Integration Token** (a `pit-...` string). Either ask Patrick for
   the shared one, or make your own:
   GHL → Settings → **Private Integrations** → New → tick **all scopes** → Copy.

Pick the sub-account you're connecting:
- **Frontline Direct** → locationId `TXw28sw0Z2rI6tcCDhJY`
- **Connect & Comm**  → locationId `xZj500PjsflIQg2j9f9D`

---

## Option A — Claude Code (one command)

Paste in a terminal, replacing `PASTE_TOKEN_HERE` and the locationId:

```
claude mcp add --transport http ghl https://services.leadconnectorhq.com/mcp/ \
  --header "Authorization: Bearer PASTE_TOKEN_HERE" \
  --header "locationId: TXw28sw0Z2rI6tcCDhJY"
```

Restart Claude Code. Done.

## Option B — Claude desktop / web (custom connector)

Settings → Connectors → Add custom connector:
- **URL:** `https://services.leadconnectorhq.com/mcp/`
- **Header:** `Authorization: Bearer PASTE_TOKEN_HERE`
- **Header:** `locationId: TXw28sw0Z2rI6tcCDhJY`

Save, then start a new chat.

---

## What you can do once connected
Just ask Claude in plain English, e.g.:
- "Look up the contact for 832-555-1234."
- "Text contact X: 'Hi, AT&T fiber is available at your address...'"
- "Tag these contacts `att-fiber-drip`."
- "Show recent conversations / opportunities."

## What it can't do (GHL UI only)
Smart-list creation, the number-intelligence trigger, and the workflow builder are
not in GHL's API — those still have to be done in the GHL website.

> Keep your token private — it grants full read/write to that sub-account. Rotate it
> in Settings → Private Integrations if it ever leaks.
