#!/usr/bin/env python3
"""
OPTIMUS PORTAL v2.0 - Claude-only chat. Pure ASCII (no emoji/smart chars) to
avoid the UTF-8 mojibake that broke v1.2. Runs on Cloud Run.
"""
import os
import logging
from flask import Flask, request, jsonify, Response
import requests

VERSION = "2.0"
SHEET_ID = "1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA"
PORT = int(os.environ.get("PORT", 8080))
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

CLAUDE_SYSTEM = (
    "You are Claude in Patrick's Optimus Portal, for his AT&T fiber sales pipeline. "
    "Master sheet 1FhO. Pipeline: fiber_hunter screenshots the AT&T map -> "
    "hunter_dot_extractor reads dots -> mapman API enriches addresses to phones via "
    "Google Places. Green dots = fiber eligible, not yet AT&T customers. "
    "Patrick is a rep, not a developer. Be direct, practical, mobile-friendly."
)

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


@app.route("/status")
def status():
    return jsonify({
        "version": VERSION,
        "sheet_url": "https://docs.google.com/spreadsheets/d/" + SHEET_ID + "/edit",
        "chat_enabled": bool(ANTHROPIC_KEY),
    })


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
        return jsonify({"error": d.get("error", {}).get("message", "no content")}), 200
    except Exception as e:
        logging.exception("chat error")
        return jsonify({"error": str(e)}), 200


PORTAL_HTML = """<!doctype html>
<html><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Optimus Portal</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{font:15px -apple-system,Segoe UI,sans-serif;background:#0a0e1a;color:#e4e7ec;min-height:100vh;display:flex;flex-direction:column}
  header{background:#111827;padding:14px 16px;border-bottom:1px solid #1f2937;display:flex;justify-content:space-between;align-items:center}
  h1{font-size:17px;font-weight:700;color:#60a5fa;letter-spacing:.5px}
  .ver{font-size:11px;color:#6b7280}
  main{flex:1;display:flex;flex-direction:column;padding:12px;gap:10px;overflow:hidden}
  #log{flex:1;background:#111827;border:1px solid #1f2937;border-radius:8px;padding:12px;overflow-y:auto;font-size:14px;line-height:1.5}
  .msg{margin-bottom:12px;padding:9px 12px;border-radius:8px}
  .u{background:#1e3a8a;margin-left:32px}
  .a{background:#1f2937;margin-right:32px}
  .a strong{color:#60a5fa}
  form{display:flex;gap:8px}
  #q{flex:1;padding:12px;background:#111827;border:1px solid #1f2937;border-radius:8px;color:#e4e7ec;font-size:15px}
  #q:focus{outline:none;border-color:#3b82f6}
  .send{padding:12px 18px;background:#3b82f6;border:0;border-radius:8px;color:#fff;font-weight:600;cursor:pointer;font:inherit}
  .send:disabled{opacity:.5}
</style>
</head><body>
<header><h1>Optimus Portal</h1><span class="ver">v2.0 - Claude</span></header>
<main>
  <div id="log"></div>
  <form id="f">
    <input id="q" placeholder="Ask Claude about your pipeline..." autocomplete="off">
    <button class="send" id="b" type="submit">Send</button>
  </form>
</main>
<script>
const log=document.getElementById('log'),q=document.getElementById('q'),b=document.getElementById('b'),history=[];
function add(role,text){const d=document.createElement('div');d.className='msg '+(role==='user'?'u':'a');d.innerHTML=(role==='user'?'':'<strong>Claude:</strong> ')+text.replace(/\\n/g,'<br>');log.appendChild(d);log.scrollTop=log.scrollHeight;}
document.getElementById('f').onsubmit=async(e)=>{
  e.preventDefault();const text=q.value.trim();if(!text)return;
  add('user',text);history.push({role:'user',content:text});
  q.value='';b.disabled=true;b.textContent='...';
  try{
    const r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({messages:history})});
    const d=await r.json();const reply=d.text||('Error: '+(d.error||'unknown'));
    add('claude',reply);history.push({role:'assistant',content:reply});
  }catch(e){add('claude','Network error: '+e.message);}
  finally{b.disabled=false;b.textContent='Send';q.focus();}
};
q.focus();add('claude','Portal v2.0 live. Ask me anything about the pipeline.');
</script>
</body></html>"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
