#!/usr/bin/env python3
"""
OPTIMUS_CLOUD v1.2 - Cloud Run portal for Optimus fiber pipeline.
"""

import os
import logging
from flask import Flask, request, jsonify, Response
import requests

VERSION = "1.2"
SHEET_ID = "1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA"
PORT = int(os.environ.get("PORT", 8080))
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MAKE_WEBHOOK = os.environ.get("MAKE_COMMAND_WEBHOOK", "")

COMMAND_WEBHOOKS = {
    "RUN_HUNTER":    "https://hook.us2.make.com/exjyi3f9wu58upnayjuh5oustilolila",
    "RUN_EXTRACTOR": "https://hook.us2.make.com/pqyqwzz60g7386n3mn34ai1xkveecg6w",
    "RUN_MAPMAN":    "https://hook.us2.make.com/x7g1fxqo2bath8eyrtl7jj2at09htckh",
    "RUN_HUNTER_ZIP":"https://hook.us2.make.com/exjyi3f9wu58upnayjuh5oustilolila",
}

CLAUDE_SYSTEM = """You are Claude embedded in the Optimus Portal for Patrick's AT&T fiber sales pipeline.

CONTEXT:
- Master sheet: 1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA
- Pipeline: fiber_hunter screenshots AT&T map -> hunter_dot_extractor reads dots -> mapman_api enriches via Google Places -> phones land in Hunter Commercial / Hunter Green Commercial tabs
- Green dots = FIBER ELIGIBLE, NOT AT&T customer (new acquisition)
- Gold/Orange dots = UPGRADE ELIGIBLE (current AT&T copper customers)
- Hunter Commercial = 202 unique phones | Hunter Green Commercial = 121 unique phones
- Portal buttons trigger scripts on the HP via Make webhooks
- "Leads by ZIP" sends a ZIP code to fiber_hunter so it scans that specific area
- Patrick is a rep, not a developer. Be direct and practical. Mobile screen."""

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
    body = request.get_json(silent=True) or {}
    cmd = body.get("cmd", "").upper()
    params = body.get("params", "")
    if not cmd:
        return jsonify({"error": "no cmd"}), 400
    webhook_url = COMMAND_WEBHOOKS.get(cmd, MAKE_WEBHOOK)
    if not webhook_url:
        return jsonify({"error": f"no webhook for {cmd}"}), 200
    try:
        r = requests.post(webhook_url, json={"cmd": cmd, "params": params}, timeout=15)
        return jsonify({"ok": True, "make_status": r.status_code, "cmd": cmd, "params": params})
    except Exception as e:
        return jsonify({"error": str(e)}), 200


@app.route("/status")
def status():
    return jsonify({
        "version": VERSION,
        "sheet_id": SHEET_ID,
        "sheet_url": f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit",
        "chat_enabled": bool(ANTHROPIC_KEY),
        "command_webhooks": {k: "configured" for k in COMMAND_WEBHOOKS},
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
  h1{font-size:16px;font-weight:700;color:#60a5fa;letter-spacing:.5px}
  .ver{font-size:11px;color:#6b7280}
  main{flex:1;display:flex;flex-direction:column;padding:12px;gap:10px;overflow:hidden}
  .sect-label{font-size:10px;font-weight:700;color:#6b7280;letter-spacing:1px;text-transform:uppercase;padding-bottom:4px}
  .programs{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px}
  .prog-btn{background:#111827;border:1px solid #1f2937;border-radius:10px;padding:12px 6px;text-align:center;cursor:pointer;transition:border-color .15s,background .15s;color:#e4e7ec;font:inherit;width:100%}
  .prog-btn:active{transform:scale(.96)}
  .prog-btn.running{border-color:#f59e0b;background:#1a1200;animation:pulse 1s infinite}
  .prog-btn.done{border-color:#10b981;background:#021c0e}
  .prog-btn.err{border-color:#ef4444;background:#1a0000}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.6}}
  .prog-icon{font-size:20px;margin-bottom:4px}
  .prog-name{font-size:10px;font-weight:700;color:#93c5fd;letter-spacing:.5px}
  .prog-status{font-size:10px;color:#6b7280;margin-top:3px;min-height:14px}
  .zip-card{background:#111827;border:1px solid #1f2937;border-radius:10px;padding:12px}
  .zip-row{display:flex;gap:6px;margin-top:8px}
  .zip-input{flex:1;padding:9px 12px;background:#0a0e1a;border:1px solid #1f2937;border-radius:8px;color:#e4e7ec;font-size:14px;letter-spacing:1px}
  .zip-input:focus{outline:none;border-color:#3b82f6}
  .zip-btn{padding:9px 14px;background:#7c3aed;border:0;border-radius:8px;color:#fff;font-weight:600;cursor:pointer;font:inherit;white-space:nowrap}
  .zip-btn:disabled{opacity:.5}
  .zip-status{font-size:11px;color:#6b7280;margin-top:6px;min-height:14px}
  .links{display:flex;gap:6px;flex-wrap:wrap}
  .links a{color:#60a5fa;text-decoration:none;padding:5px 10px;background:#111827;border:1px solid #1f2937;border-radius:6px;font-size:11px}
  #log{flex:1;background:#111827;border:1px solid #1f2937;border-radius:8px;padding:10px;overflow-y:auto;font-size:13px;line-height:1.5;min-height:80px}
  .msg{margin-bottom:10px;padding:8px 10px;border-radius:6px}
  .u{background:#1e3a8a;margin-left:20px}
  .a{background:#1f2937;margin-right:20px}
  .a strong{color:#60a5fa}
  form#f{display:flex;gap:6px}
  input#q{flex:1;padding:10px 12px;background:#111827;border:1px solid #1f2937;border-radius:8px;color:#e4e7ec;font-size:14px}
  input#q:focus{outline:none;border-color:#3b82f6}
  .send{padding:10px 16px;background:#3b82f6;border:0;border-radius:8px;color:#fff;font-weight:600;cursor:pointer;font:inherit}
  .send:disabled{opacity:.5}
</style>
</head><body>
<header>
  <h1>⚡ Optimus Portal</h1>
  <span class="ver">v1.2</span>
</header>
<main>
  <div class="sect-label">Run Scripts</div>
  <div class="programs">
    <button class="prog-btn" id="btn-hunter" onclick="runCmd('hunter')">
      <div class="prog-icon">📸</div>
      <div class="prog-name">FIBER HUNTER</div>
      <div class="prog-status" id="st-hunter">tap to run</div>
    </button>
    <button class="prog-btn" id="btn-extractor" onclick="runCmd('extractor')">
      <div class="prog-icon">🔍</div>
      <div class="prog-name">EXTRACTOR</div>
      <div class="prog-status" id="st-extractor">tap to run</div>
    </button>
    <button class="prog-btn" id="btn-mapman" onclick="runCmd('mapman')">
      <div class="prog-icon">📞</div>
      <div class="prog-name">MAPMAN API2</div>
      <div class="prog-status" id="st-mapman">tap to run</div>
    </button>
  </div>
  <div class="sect-label">Request Leads by ZIP</div>
  <div class="zip-card">
    <div style="font-size:12px;color:#9ca3af">Enter a ZIP code to scan that area for fiber-eligible leads</div>
    <div class="zip-row">
      <input class="zip-input" id="zip" type="text" maxlength="5" placeholder="e.g. 73007" inputmode="numeric">
      <button class="zip-btn" id="zip-btn" onclick="requestZip()">🗺 Get Leads</button>
    </div>
    <div class="zip-status" id="zip-status"></div>
  </div>
  <div class="links">
    <a href="https://docs.google.com/spreadsheets/d/1FhO2BTMXGefm1tLwKbbMPXvzT1160882Auauzep7ooA/edit" target="_blank">📊 Master Sheet</a>
    <a href="/status" target="_blank">⚙�️ Status</a>
    <a href="/healthz" target="_blank">💚 Health</a>
  </div>
  <div id="log"></div>
  <form id="f">
    <input id="q" placeholder="Ask Claude about your pipeline..." autocomplete="off">
    <button class="send" id="b" type="submit">Send</button>
  </form>
</main>
<script>
const log = document.getElementById('log');
const q = document.getElementById('q');
const b = document.getElementById('b');
const history = [];
function add(role, text) {
  const d = document.createElement('div');
  d.className = 'msg ' + (role === 'user' ? 'u' : 'a');
  d.innerHTML = (role === 'user' ? '' : '<strong>Claude:</strong> ') + text.replace(/\n/g, '<br>');
  log.appendChild(d);
  log.scrollTop = log.scrollHeight;
}
async function runCmd(prog) {
  const cmds = {hunter:'RUN_HUNTER', extractor:'RUN_EXTRACTOR', mapman:'RUN_MAPMAN'};
  const labels = {hunter:'Fiber Hunter', extractor:'Extractor', mapman:'MapMan'};
  const btn = document.getElementById('btn-' + prog);
  const st = document.getElementById('st-' + prog);
  btn.className = 'prog-btn running';
  st.textContent = 'sending...';
  try {
    const r = await fetch('/command', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({cmd: cmds[prog]})
    });
    const d = await r.json();
    if (d.ok) {
      btn.className = 'prog-btn done'; st.textContent = 'queued ✓';
      add('claude', labels[prog] + ' command sent to HP. Check back in a few minutes.');
    } else { btn.className = 'prog-btn err'; st.textContent = d.error || 'error'; }
  } catch(e) { btn.className = 'prog-btn err'; st.textContent = 'network error'; }
  setTimeout(() => { btn.className = 'prog-btn'; st.textContent = 'tap to run'; }, 5000);
}
async function requestZip() {
  const zip = document.getElementById('zip').value.trim();
  const zipBtn = document.getElementById('zip-btn');
  const zipSt = document.getElementById('zip-status');
  if (!/^[0-9]{5}$/.test(zip)) { zipSt.textContent = '❠ Enter a valid 5-digit ZIP'; zipSt.style.color='#f59e0b'; return; }
  zipBtn.disabled = true; zipSt.style.color='#6b7280'; zipSt.textContent = 'Sending...';
  try {
    const r = await fetch('/command', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({cmd:'RUN_HUNTER_ZIP', params: zip})
    });
    const d = await r.json();
    if (d.ok) {
      zipSt.style.color='#10b981'; zipSt.textContent = '✓ ZIP '+zip+' queued';
      add('claude', 'Lead request for ZIP '+zip+' sent to HP.');
    } else { zipSt.style.color='#ef4444'; zipSt.textContent = 'Error: '+(d.error||'unknown'); }
  } catch(e) { zipSt.style.color='#ef4444'; zipSt.textContent='Network error'; }
  setTimeout(()=>{zipBtn.disabled=false;},3000);
}
document.getElementById('f').onsubmit = async (e) => {
  e.preventDefault();
  const text = q.value.trim();
  if (!text) return;
  add('user', text);
  history.push({role:'user',content:text});
  q.value=''; b.disabled=true; b.textContent='...';
  try {
    const r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({messages:history})});
    const d=await r.json();
    const reply=d.text||('Error: '+(d.error||'unknown'));
    add('claude',reply); history.push({role:'assistant',content:reply});
  } catch(e){add('claude','Network error: '+e.message);}
  finally{b.disabled=false;b.textContent='Send';q.focus();}
};
q.focus();
add('claude','Portal v1.2 live. Tap a script button or enter a ZIP for leads.');
</script>
</body></html>"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
