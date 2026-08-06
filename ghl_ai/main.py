#!/usr/bin/env python3
"""
GHL <-> CLAUDE AUTO-REPLY BRIDGE  v1.0
======================================================================
Connects GoHighLevel (Optimus Houston / "Frontline Direct") to Claude.

WHAT IT DOES
  - GHL fires a webhook on an inbound lead message (SMS / chat).
  - This service pulls recent conversation history from GHL for context,
    asks Claude to draft an AT&T-fiber sales reply, and posts it back to
    the lead through the GHL conversations API.
  - The SAME endpoint works as a "Custom Webhook" action inside a GHL
    workflow, so Claude can also be one step in an automation.

SAFETY (read this)
  - DRY_RUN defaults to TRUE. In dry-run the bridge drafts the reply and
    returns/logs it but DOES NOT send anything to the lead. Flip
    DRY_RUN=false only when you have tested on a real thread and want it
    live. This protects the 44k-contact list from an accidental blast.
  - Opt-out words (STOP, UNSUBSCRIBE, ...) are never replied to.
  - The model is told not to invent install dates, prices, or promises,
    and to hand scheduling/payment to a human.

CONFIG (environment variables; never hardcode secrets)
  ANTHROPIC_API_KEY  - required. Claude API key.
  GHL_TOKEN          - required to SEND. GHL Private Integration Token
                       (or API key) scoped to the location, with
                       conversations read+write.
  GHL_LOCATION_ID    - defaults to the Frontline Direct location.
  CLAUDE_MODEL       - default claude-opus-4-8. Set claude-sonnet-4-6 for
                       cheaper/faster high-volume SMS if you prefer.
  CLAUDE_EFFORT      - low | medium | high (default medium).
  GHL_MESSAGE_TYPE   - default SMS.
  BRIDGE_SECRET      - if set, inbound requests must send a matching
                       X-Bridge-Secret header (simple shared-secret auth).
  DRY_RUN            - default true. Set "false" to actually send.
  MAX_REPLY_TOKENS   - default 400 (SMS-length replies).

RUN
  pip install -r requirements.txt
  python main.py                      # local, http://127.0.0.1:8080
  # or in production: gunicorn main:app
"""

import os
import logging

from flask import Flask, request, jsonify
import requests

VERSION = "1.0"

# --- Config -----------------------------------------------------------------
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
GHL_TOKEN = os.environ.get("GHL_TOKEN", "")
GHL_LOCATION_ID = os.environ.get("GHL_LOCATION_ID", "TXw28sw0Z2rI6tcCDhJY")
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-4-8")
CLAUDE_EFFORT = os.environ.get("CLAUDE_EFFORT", "medium")
GHL_MESSAGE_TYPE = os.environ.get("GHL_MESSAGE_TYPE", "SMS")
BRIDGE_SECRET = os.environ.get("BRIDGE_SECRET", "")
DRY_RUN = os.environ.get("DRY_RUN", "true").strip().lower() not in ("0", "false", "no", "off")
MAX_REPLY_TOKENS = int(os.environ.get("MAX_REPLY_TOKENS", "400"))
PORT = int(os.environ.get("PORT", "8080"))

GHL_API = "https://services.leadconnectorhq.com"
GHL_VERSION = "2021-04-15"
HISTORY_LIMIT = 12

OPT_OUT = {"stop", "stopall", "unsubscribe", "cancel", "end", "quit", "optout", "opt-out", "remove"}

# System prompt is stable + reused on every request, so it is a good cache
# prefix. (Caching only kicks in above the model minimum; harmless otherwise.)
SYSTEM_PROMPT = (
    "You are the SMS assistant for Optimus Houston / Frontline Direct, an AT&T "
    "fiber door-to-door sales operation in Texas. You reply to inbound texts "
    "from leads on behalf of the rep (Patrick's team).\n\n"
    "GOAL: book interested leads for an AT&T fiber install or a quick call. Be "
    "warm, direct, and human. This is a text conversation, not an email.\n\n"
    "DOMAIN:\n"
    "- AT&T fiber is the product. Main competitor in Texas is Spectrum (cable, "
    "outage-prone); also Xfinity. AT&T fiber and Verizon Fios do not overlap.\n"
    "- Angles that work: Spectrum outage history vs AT&T uptime; a neighbor "
    "already has AT&T fiber (social proof); copper/DSL being retired; price "
    "stability and no data cap.\n\n"
    "HARD RULES:\n"
    "- Keep replies under ~320 characters (about two SMS segments). One idea "
    "per text. No emoji walls, no markdown, plain text only.\n"
    "- NEVER invent specifics you were not given: do not state a guaranteed "
    "install date, an exact price, a speed, or a promo unless it appears in the "
    "conversation. If asked, say you will confirm and offer a call.\n"
    "- Do not schedule installs or take payment yourself. For scheduling, "
    "pricing confirmation, or payment, offer to connect them with the rep.\n"
    "- If the lead is not interested or asks to stop, acknowledge politely and "
    "do not push.\n"
    "- Sound like a real local person, not a bot. Do not say you are an AI.\n"
    "- Output ONLY the message text to send. No preamble, no quotes, no labels."
)


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("ghl_claude_bridge")

# Lazy Claude client so the app still boots (health checks) without a key.
_client = None


def claude():
    global _client
    if _client is None:
        import anthropic
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def ghl_headers():
    return {
        "Authorization": "Bearer " + GHL_TOKEN,
        "Version": GHL_VERSION,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def first(payload, *keys):
    """Return the first non-empty value among the given keys (top level)."""
    for k in keys:
        v = payload.get(k)
        if v not in (None, ""):
            return v
    return None


def extract_inbound(payload):
    """Pull the fields we need from a GHL webhook payload defensively.

    GHL inbound-message and custom webhooks vary in shape, so check several
    common key spellings and one nested 'message' object.
    """
    nested = payload.get("message") if isinstance(payload.get("message"), dict) else {}

    def grab(*keys):
        return first(payload, *keys) or first(nested, *keys)

    body = grab("body", "message", "messageBody", "text", "snippet")
    if isinstance(body, dict):  # 'message' was an object, not a string
        body = first(body, "body", "text") or ""
    return {
        "contact_id": grab("contactId", "contact_id", "contactID"),
        "conversation_id": grab("conversationId", "conversation_id"),
        "body": (body or "").strip(),
        "direction": (grab("direction") or "inbound"),
    }


def fetch_history(conversation_id):
    """Best-effort: return chronological [(role, text)] for the thread."""
    if not (conversation_id and GHL_TOKEN):
        return []
    try:
        r = requests.get(
            GHL_API + "/conversations/" + conversation_id + "/messages",
            headers=ghl_headers(),
            params={"limit": HISTORY_LIMIT},
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()
        msgs = data.get("messages")
        if isinstance(msgs, dict):
            msgs = msgs.get("messages", [])
        msgs = msgs or []
        out = []
        for m in reversed(msgs):  # API returns newest-first
            text = (m.get("body") or "").strip()
            if not text:
                continue
            direction = (m.get("direction") or "").lower()
            role = "assistant" if direction == "outbound" else "user"
            out.append((role, text))
        return out
    except Exception as e:
        log.warning("history fetch failed: %s", e)
        return []


def build_messages(history, body):
    """Claude messages: must start with a user turn and end on the lead."""
    msgs = [{"role": r, "content": t} for r, t in history]
    while msgs and msgs[0]["role"] != "user":
        msgs.pop(0)
    if not msgs or msgs[-1]["role"] != "user":
        if body:
            msgs.append({"role": "user", "content": body})
    if not msgs:
        msgs = [{"role": "user", "content": body or "(no message)"}]
    return msgs


def draft_reply(history, body):
    resp = claude().messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_REPLY_TOKENS,
        system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
        thinking={"type": "adaptive"},
        output_config={"effort": CLAUDE_EFFORT},
        messages=build_messages(history, body),
    )
    text = next((b.text for b in resp.content if b.type == "text"), "")
    return text.strip()


def send_sms(contact_id, message):
    payload = {
        "type": GHL_MESSAGE_TYPE,
        "contactId": contact_id,
        "message": message,
    }
    r = requests.post(
        GHL_API + "/conversations/messages",
        headers=ghl_headers(),
        json=payload,
        timeout=20,
    )
    r.raise_for_status()
    return r.json()


@app.after_request
def add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type,X-Bridge-Secret"
    return resp


@app.route("/healthz")
def healthz():
    return jsonify({"ok": True, "version": VERSION})


@app.route("/status")
def status():
    return jsonify({
        "version": VERSION,
        "model": CLAUDE_MODEL,
        "effort": CLAUDE_EFFORT,
        "location_id": GHL_LOCATION_ID,
        "dry_run": DRY_RUN,
        "claude_ready": bool(ANTHROPIC_API_KEY),
        "ghl_send_ready": bool(GHL_TOKEN),
        "auth_required": bool(BRIDGE_SECRET),
    })


@app.route("/ghl/inbound", methods=["POST", "OPTIONS"])
def inbound():
    if request.method == "OPTIONS":
        return ("", 204)

    if BRIDGE_SECRET and request.headers.get("X-Bridge-Secret", "") != BRIDGE_SECRET:
        return jsonify({"error": "unauthorized"}), 401

    payload = request.get_json(silent=True) or {}
    info = extract_inbound(payload)
    body = info["body"]
    contact_id = info["contact_id"]

    # Cheap skips first (no model call, no key needed).
    if not body:
        return jsonify({"skipped": "no message body in payload"}), 200
    if info["direction"].lower() == "outbound":
        return jsonify({"skipped": "outbound message"}), 200
    if body.strip().lower() in OPT_OUT:
        return jsonify({"skipped": "opt-out keyword"}), 200

    if not ANTHROPIC_API_KEY:
        return jsonify({"error": "ANTHROPIC_API_KEY not set"}), 500

    history = fetch_history(info["conversation_id"])
    try:
        reply = draft_reply(history, body)
    except Exception as e:
        log.exception("claude draft failed")
        return jsonify({"error": "draft failed", "detail": str(e)}), 502

    if not reply:
        return jsonify({"skipped": "empty draft"}), 200

    if DRY_RUN:
        log.info("[DRY_RUN] contact=%s reply=%r", contact_id, reply)
        return jsonify({"dry_run": True, "contact_id": contact_id, "reply": reply}), 200

    if not (GHL_TOKEN and contact_id):
        return jsonify({"error": "missing GHL_TOKEN or contactId; cannot send",
                        "reply": reply}), 200

    try:
        result = send_sms(contact_id, reply)
    except Exception as e:
        log.exception("ghl send failed")
        return jsonify({"error": "send failed", "detail": str(e), "reply": reply}), 502

    log.info("sent contact=%s reply=%r", contact_id, reply)
    return jsonify({"sent": True, "contact_id": contact_id, "reply": reply, "ghl": result}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
