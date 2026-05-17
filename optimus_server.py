"""
optimus_server.py v2 - Local control server for Optimus Portal
Run on HP: python optimus_server.py
Portal connects to http://localhost:5050

v2 changes:
- MapMan starts with mapman_patch wrapper (30s timeout + 3 retries on requests)
- /start endpoint accepts optional 'city' arg for MapMan
- Logs include the actual command run (debugging visibility)
"""
import subprocess, sys, os, json, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

PORT = 5050
DESKTOP = Path(r"C:\Users\patri\Desktop")

SCRIPTS = {
    "extractor": str(DESKTOP / "hunter_dot_extractor.py"),
    "mapman":    str(DESKTOP / "THEMAPMAN.py"),
    "hunter":    str(DESKTOP / "fiber_hunter.py"),
}
MAPMAN_PATCH = str(DESKTOP / "mapman_patch.py")
MAPMAN_DEFAULT_ARGS = ["--no-update", "--commercial-only", "--tab", "Hunter Commercial", "--instance", "1of2", "--no-pick", "--no-spawn"]

_procs = {}
_logs = {k: [] for k in SCRIPTS}

def _stream(name, proc):
    for line in iter(proc.stdout.readline, b""):
        text = line.decode("utf-8", errors="replace").rstrip()
        _logs[name].append(text)
        if len(_logs[name]) > 500:
            _logs[name] = _logs[name][-500:]
    proc.wait()
    _logs[name].append(f"[exit code {proc.returncode}]")

def _build_mapman_cmd(city=None, instance=None, tab=None):
    """Build MapMan command via the patch wrapper for ReadTimeout retries."""
    target = SCRIPTS["mapman"]
    if os.path.exists(MAPMAN_PATCH):
        inner = f"import mapman_patch; exec(open(r'{target}').read())"
        cmd = [sys.executable, "-c", inner] + MAPMAN_DEFAULT_ARGS
    else:
        cmd = [sys.executable, target] + MAPMAN_DEFAULT_ARGS
    if city:
        cmd += ["--city", city]
    if instance:
        if "--instance" in cmd:
            idx = cmd.index("--instance")
            cmd[idx+1] = instance
        else:
            cmd += ["--instance", instance]
    if tab:
        if "--tab" in cmd:
            idx = cmd.index("--tab")
            cmd[idx+1] = tab
        else:
            cmd += ["--tab", tab]
    return cmd

def start_script(name, opts=None):
    opts = opts or {}
    if name not in SCRIPTS:
        return {"ok": False, "error": f"Unknown script: {name}"}
    if name in _procs and _procs[name].poll() is None:
        return {"ok": False, "error": f"{name} already running"}
    path = SCRIPTS[name]
    if not os.path.exists(path):
        return {"ok": False, "error": f"File not found: {path}"}

    if name == "mapman":
        args = _build_mapman_cmd(
            city=opts.get("city") or None,
            instance=opts.get("instance") or None,
            tab=opts.get("tab") or None,
        )
        if not os.path.exists(MAPMAN_PATCH):
            _logs[name] = [f"[WARN] {MAPMAN_PATCH} missing - ReadTimeout protection disabled"]
        else:
            _logs[name] = [f"[OK] mapman_patch wrapper active"]
    else:
        args = [sys.executable, path]
        _logs[name] = []

    _logs[name].append("CMD: " + " ".join(args))

    try:
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=str(DESKTOP))
    except Exception as e:
        return {"ok": False, "error": f"spawn failed: {e}"}
    _procs[name] = proc
    threading.Thread(target=_stream, args=(name, proc), daemon=True).start()
    return {"ok": True, "msg": f"{name} started"}

def stop_script(name):
    proc = _procs.get(name)
    if not proc or proc.poll() is not None:
        return {"ok": False, "error": f"{name} not running"}
    proc.terminate()
    return {"ok": True, "msg": f"{name} stopped"}

def status():
    out = {}
    for k, p in _procs.items():
        out[k] = "running" if p.poll() is None else "stopped"
    for k in SCRIPTS:
        if k not in out:
            out[k] = "stopped"
    return out

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/status":
            self._send(200, status())
        elif self.path.startswith("/logs/"):
            name = self.path.split("/")[-1]
            self._send(200, {"lines": _logs.get(name, [])[-100:]})
        elif self.path == "/health":
            self._send(200, {"ok": True, "scripts": list(SCRIPTS.keys()), "patch_present": os.path.exists(MAPMAN_PATCH)})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) or b"{}")
        if self.path == "/start":
            opts = {k: body.get(k) for k in ("city", "instance", "tab")}
            self._send(200, start_script(body.get("script", ""), opts))
        elif self.path == "/stop":
            self._send(200, stop_script(body.get("script", "")))
        elif self.path == "/chat":
            API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
            if not API_KEY:
                self._send(200, {"text": "Add ANTHROPIC_API_KEY to environment to enable chat."})
                return
            import urllib.request
            msgs = body.get("messages", [])
            payload = json.dumps({
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1000,
                "system": "You are Claude embedded in the Optimus Portal. You have full context of the AT&T fiber lead pipeline. Be concise.",
                "messages": msgs
            }).encode()
            req = urllib.request.Request(
                "https://api.anthropic.com/v1/messages",
                data=payload,
                headers={"Content-Type":"application/json","x-api-key":API_KEY,"anthropic-version":"2023-06-01"},
                method="POST"
            )
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    d = json.loads(r.read())
                self._send(200, {"text": d["content"][0]["text"]})
            except Exception as e:
                self._send(200, {"error": str(e)})
        else:
            self._send(404, {"error": "not found"})

if __name__ == "__main__":
    print(f"Optimus Server v2 running at http://localhost:{PORT}")
    print(f"  mapman_patch present: {os.path.exists(MAPMAN_PATCH)}")
    print(f"  patch path: {MAPMAN_PATCH}")
    print("Open optimus_portal.html in Chrome")
    print("To enable Claude chat: set ANTHROPIC_API_KEY environment variable")
    HTTPServer(("localhost", PORT), Handler).serve_forever()
