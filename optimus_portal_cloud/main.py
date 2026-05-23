#!/usr/bin/env python3
from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import logging, os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

_db = None
def get_db():
    global _db
    if _db is None:
        try:
            from google.cloud import firestore
            _db = firestore.Client()
        except Exception as e:
            log.warning(f"Firestore offline: {e}")
            _db = False
    return _db if _db is not False else None

HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>Optimus</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:system-ui;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;padding:20px}.container{max-width:1200px;margin:0 auto}header{background:white;padding:30px;border-radius:8px;margin-bottom:30px}h1{font-size:2em;color:#333}p{color:#666}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;margin-bottom:30px}.card{background:white;padding:20px;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,.1)}.card h3{color:#666;font-size:.9em;margin-bottom:10px;text-transform:uppercase}.value{font-size:2.5em;font-weight:bold;color:#667eea}.form{background:white;padding:30px;border-radius:8px;margin-bottom:30px}.form-group{margin-bottom:20px}label{display:block;margin-bottom:5px;color:#333;font-weight:500}input,select,textarea{width:100%;padding:10px;border:1px solid #ddd;border-radius:4px}button{background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:10px 20px;border:0;border-radius:4px;cursor:pointer;font-weight:600}button:hover{opacity:.9}.jobs{background:white;padding:30px;border-radius:8px}.job{padding:15px;border-bottom:1px solid #eee;display:flex;justify-content:space-between}.badge{padding:5px 10px;font-size:.85em;width:auto}.badge-pending{background:#ffc107;color:#333}.badge-running{background:#17a2b8;color:white}.badge-completed{background:#28a745;color:white}</style></head><body><div class="container"><header><h1>Optimus Portal</h1><p>Fiber Scanner</p></header><div class="grid"><div class="card"><h3>Pending</h3><div class="value" id="p">0</div></div><div class="card"><h3>Running</h3><div class="value" id="r">0</div></div><div class="card"><h3>Done</h3><div class="value" id="d">0</div></div></div><div class="form"><h2>Submit Job</h2><form id="f"><select name="t" required><option>-- Select Job --</option><option value="fiber_hunter">Fiber Hunter</option><option value="mapman">Map Enrichment</option></select><textarea name="p" placeholder="Parameters" required></textarea><button type="submit">Submit</button></form></div><div class="jobs"><h2>Jobs</h2><div id="j">Loading...</div></div></div><script>async function load(){const s=await fetch("/api/stats").then(r=>r.json());document.getElementById("p").textContent=s.p||0;document.getElementById("r").textContent=s.r||0;document.getElementById("d").textContent=s.d||0;const jobs=await fetch("/api/jobs").then(r=>r.json());document.getElementById("j").innerHTML=jobs.map(x=>`<div class="job"><div><strong>${x.job_type}</strong></div><button class="badge badge-${x.status}">${x.status}</button></div>`).join("")}document.getElementById("f").addEventListener("submit",async e=>{e.preventDefault();const f=new FormData(e.target);await fetch("/api/submit",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({job_type:f.get("t"),params:f.get("p")})});e.target.reset();load()});load();setInterval(load,3000)</script></body></html>"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/stats")
def stats():
    try:
        db = get_db()
        if not db:
            return jsonify({"p": 0, "r": 0, "d": 0})
        jobs = list(db.collection("jobs").stream())
        return jsonify({
            "p": sum(1 for j in jobs if j.to_dict().get("status") == "pending"),
            "r": sum(1 for j in jobs if j.to_dict().get("status") == "running"),
            "d": sum(1 for j in jobs if j.to_dict().get("status") == "completed"),
        })
    except:
        return jsonify({"p": 0, "r": 0, "d": 0})

@app.route("/api/jobs")
def jobs_list():
    try:
        db = get_db()
        if not db:
            return jsonify([])
        return jsonify([{**j.to_dict(), "id": j.id} for j in db.collection("jobs").order_by("created_at", direction="descending").limit(10).stream()])
    except:
        return jsonify([])

@app.route("/api/submit", methods=["POST"])
def submit():
    try:
        data = request.json
        db = get_db()
        if not db:
            return jsonify({"error": "offline"}), 503
        db.collection("jobs").document().set({
            "job_type": data["job_type"],
            "params": data["params"],
            "status": "pending",
            "created_at": datetime.now().isoformat()
        })
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)), debug=False)
