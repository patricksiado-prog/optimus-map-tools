#!/usr/bin/env python3
"""
OPTIMUS_CLOUD v1.0 - Cloud Run portal for Optimus fiber pipeline.

Endpoints:
  GET  /              -> mobile portal HTML
  GET  /healthz       -> liveness check
  GET  /status        -> read pipeline state from master sheet
  POST /chat          -> proxy to Anthropic API (Claude)
  POST /command       -> forward script-run command to Make webhook (HP polls)

Secrets via env vars (set in Cloud Run UI or Secret Manager):
  ANTHROPIC_API_KEY        - for /chat
  MAKE_COMMAND_WEBHOOK     - Make webhook URL HP polls (optional)
  GOOGLE_CREDS_JSON        - service account JSON as a string (for sheet reads)

Deploy:
  cd cloud/
  gcloud run deploy optimus-portal --source . --region us-central1 \\
    --allow-unauthenticated --set-env-vars=ANTHROPIC_API_KEY=sk-ant-...
"""

import os
import json
import logging
from flask import Flask, request, jsonify, Response
import requests

VERSION = "1.0"
SHEET_ID = "1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA"
PORT = int(os.environ.get("PORT", 8080))

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MAKE_WEBHOOK = os.environ.get("MAKE_COMMAND_WEBHOOK", "")
GOOGLE_CREDS = os.environ.get("GOOGLE_CREDS_JSON", "")

CLAUDE_SYSTEM = """You are Claude embedded in the Optimus Portal for Patrick's AT&T fiber sales pipeline.

CONTEXT YOU SHOULD KNOW:
- Master sheet: 1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA
- Pipeline: fiber_hunter screenshots AT&T map -> hunter_dot_extractor reads dots -> mapman_api enriches via Google Places API -> phones land in Hunter Commercial / Hunter Green Commercial / Ready To Call / $ LEADS tabs
- Patrick is a rep, not a developer. Be direct and practical.
- Don't lecture about sleep, breaks, hydration, or wellbeing.
- Keep responses tight. Mobile screen.
"""

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.after_request
def add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


@app.route("/healthz")
def healthz():
    return jsonify({"ok": True, "version": VERSION})


@app.route("/")
def portal():
    return Response(PORTAL_HTML, mimetype="text/html")


@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return ("", 204)
    if not ANTHROPIC_KEY:
        return jsonify({"text": "Set ANTHROPIC_API_KEY in Cloud Run env to enable chat."})
    body = request.get_json(silent=True) or {}
    msgs = body.get("messages", [])
    if not msgs:
        return jsonify({"error": "no messages"}), 400
    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": ANTHROPIC_KEY,
                "anthropic-version": "2023-06-01",
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 1500,
                "system": CLAUDE_SYSTEM,
                "messages": msgs,
            },
            timeout=45,
        )
        d = r.json()
        if "content" in d and d["content"]:
            text = "".join(b.get("text", "") for b in d["content"] if b.get("type") == "text")
            return jsonify({"text": text})
        return jsonify({"error": d.get("error", {}).get("message", "no content"), "raw": d}), 200
    except Exception as e:
        logging.exception("chat error")
        return jsonify({"error": str(e)}), 200


@app.route("/command", methods=["POST"])
def command():
    """Forward command to Make webhook. HP polls Make for pending commands."""
    if not MAKE_WEBHOOK:
        return jsonify({"error": "MAKE_COMMAND_WEBHOOK not configured"}), 200
    body = request.get_json(silent=True) or {}
    cmd = body.get("cmd", "")
    if not cmd:
        return jsonify({"error": "no cmd"}), 400
    try:
        r = requests.post(MAKE_WEBHOOK, json={"cmd": cmd}, timeout=15)
        return jsonify({"ok": True, "make_status": r.status_code, "cmd": cmd})
    except Exception as e:
        return jsonify({"error": str(e)}), 200


@app.route("/status")
def status():
    """Return basic pipeline status. Sheet read requires google-auth + gspread."""
    return jsonify({
        "version": VERSION,
        "sheet_id": SHEET_ID,
        "sheet_url": f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit",
        "chat_enabled": bool(ANTHROPIC_KEY),
        "command_bridge": bool(MAKE_WEBHOOK),
        "scripts": {
            "fiber_hunter": "runs on HP (GUI required)",
            "hunter_dot_extractor": "runs on HP",
            "mapman_api": "could run on Cloud Run as a job",
        },
    })


PORTAL_HTML = """<!doctype html>
<html><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Optimus Portal</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{font:14px -apple-system,Segoe UI,sans-serif;background:#0a0e1a;color:#e4e7ec;min-height:100vh;display:flex;flex-direction:column}
  header{background:#111827;padding:12px 16px;border-bottom:1px solid #1f2937;display:flex;justify-content:space-between;align-items:center}
  h1{font-size:16px;font-weight:600;color:#60a5fa}
  .ver{font-size:11px;color:#6b7280}
  main{flex:1;display:flex;flex-direction:column;padding:12px;gap:8px;overflow:hidden}
  #log{flex:1;background:#111827;border:1px solid #1f2937;border-radius:8px;padding:10px;overflow-y:auto;font-size:13px;line-height:1.5}
  .msg{margin-bottom:10px;padding:8px 10px;border-radius:6px}
  .u{background:#1e3a8a;margin-left:32px}
  .a{background:#1f2937;margin-right:32px}
  .a strong{color:#60a5fa}
  form{display:flex;gap:6px}
  input{flex:1;padding:10px 12px;background:#111827;border:1px solid #1f2937;border-radius:8px;color:#e4e7ec;font-size:14px}
  input:focus{outline:none;border-color:#3b82f6}
  button{padding:10px 16px;background:#3b82f6;border:0;border-radius:8px;color:#fff;font-weight:600;cursor:pointer}
  button:disabled{opacity:0.5}
  .links{display:flex;gap:8px;flex-wrap:wrap;font-size:12px}
  .links a{color:#60a5fa;text-decoration:none;padding:6px 10px;background:#111827;border:1px solid #1f2937;border-radius:6px}
</style>
</head><body>
<header>
  <h1>Optimus Portal</h1>
  <span class="ver" id="ver">v1.0</span>
</header>
<main>
  <div class="links">
    <a href="https://docs.google.com/spreadsheets/d/1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA/edit" target="_blank">Master Sheet</a>
    <a href="/status" target="_blank">Status</a>
    <a href="/healthz" target="_blank">Health</a>
  </div>
  <div id="log"></div>
  <form id="f">
    <input id="q" placeholder="Ask Claude about your pipeline..." autocomplete="off">
    <button id="b" type="submit">Send</button>
  </form>
</main>
<script>
const log = document.getElementById('log');
const q = document.getElementById('q');
const b = document.getElementById('b');
const f = document.getElementById('f');
const history = [];

function add(role, text) {
  const d = document.createElement('div');
  d.className = 'msg ' + (role === 'user' ? 'u' : 'a');
  d.innerHTML = (role === 'user' ? '' : '<strong>Claude:</strong> ') + text.replace(/\\n/g, '<br>');
  log.appendChild(d);
  log.scrollTop = log.scrollHeight;
}

f.onsubmit = async (e) => {
  e.preventDefault();
  const text = q.value.trim();
  if (!text) return;
  add('user', text);
  history.push({role: 'user', content: text});
  q.value = '';
  b.disabled = true;
  b.textContent = '...';
  try {
    const r = await fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({messages: history})
    });
    const d = await r.json();
    const reply = d.text || ('Error: ' + (d.error || 'unknown'));
    add('claude', reply);
    history.push({role: 'assistant', content: reply});
  } catch (e) {
    add('claude', 'Network error: ' + e.message);
  } finally {
    b.disabled = false;
    b.textContent = 'Send';
    q.focus();
  }
};

q.focus();
add('claude', 'Portal live. Ask about your pipeline, leads, or scripts.');
</script>
</body></html>"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
