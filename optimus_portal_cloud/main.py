#!/usr/bin/env python3
from flask import Flask, render_template_string, request, jsonify
from google.cloud import firestore
from datetime import datetime
from threading import Thread
import subprocess
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

PROJECT_ID = os.getenv('GCP_PROJECT', 'optimus-portal-10186d3825862')
db = firestore.Client(project=PROJECT_ID)

DASHBOARD_HTML = '''<!DOCTYPE html><html><head><meta charset="utf-8"><title>Optimus Fiber Scanner</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;padding:20px}.container{max-width:1200px;margin:0 auto}header{background:white;padding:30px;border-radius:8px;margin-bottom:30px;box-shadow:0 4px 6px rgba(0,0,0,.1)}h1{font-size:2.5em;color:#333;margin-bottom:5px}.subtitle{color:#666;font-size:1.1em}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px;margin-bottom:30px}.card{background:white;padding:20px;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,.1)}.card h3{color:#333;margin-bottom:10px;font-size:.9em;text-transform:uppercase}.card-value{font-size:2.5em;font-weight:bold;color:#667eea}.form-section{background:white;padding:30px;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,.1);margin-bottom:30px}.form-group{margin-bottom:20px}label{display:block;margin-bottom:8px;color:#333;font-weight:500}input,select,textarea{width:100%;padding:12px;border:1px solid #ddd;border-radius:4px;font-family:monospace;font-size:1em}input:focus,select:focus,textarea:focus{outline:0;border-color:#667eea;box-shadow:0 0 0 3px rgba(102,126,234,.1)}button{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:12px 30px;border:0;border-radius:4px;cursor:pointer;font-size:1em;font-weight:600;transition:transform .2s}button:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(102,126,234,.4)}button:active{transform:translateY(0)}.job-list{background:white;padding:30px;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,.1)}.job-item{padding:15px;border-bottom:1px solid #eee;display:flex;justify-content:space-between;align-items:center}.job-item:last-child{border-bottom:0}.job-details{flex:1}.job-type{font-weight:600;color:#333}.job-params{color:#666;font-size:.9em;margin:5px 0}.job-time{color:#999;font-size:.85em}.badge{padding:5px 12px;border-radius:20px;font-size:.85em;font-weight:600}.badge-pending{background:#ffc107;color:#333}.badge-running{background:#17a2b8;color:white}.badge-completed{background:#28a745;color:white}.badge-error{background:#dc3545;color:white}.alert{padding:15px;border-radius:4px;margin-bottom:20px}.alert-success{background:#d4edda;color:#155724;border:1px solid #c3e6cb}.alert-error{background:#f8d7da;color:#721c24;border:1px solid #f5c6cb}</style></head><body><div class="container"><header><h1>Optimus Fiber Scanner</h1><p class="subtitle">Cloud-Native Portal</p></header><div class="grid"><div class="card"><h3>Pending</h3><div class="card-value" id="pending-count">-</div></div><div class="card"><h3>Running</h3><div class="card-value" id="running-count">-</div></div><div class="card"><h3>Completed</h3><div class="card-value" id="completed-count">-</div></div><div class="card"><h3>Total</h3><div class="card-value" id="total-count">-</div></div></div><div class="form-section"><h2>Submit Job</h2><div id="alert-container"></div><form id="submit-form"><div class="form-group"><label>Job Type *</label><select name="job_type" required><option value="">-- Select --</option><option value="fiber_hunter">Fiber Hunter</option><option value="mapman">Map Enrichment</option><option value="dot_extractor">Dot Extractor</option></select></div><div class="form-group"><label>Parameters *</label><textarea name="params" required rows="3"></textarea></div><button type="submit">Submit</button></form></div><div class="job-list"><h2>Jobs</h2><div id="job-list">Loading...</div></div></div><script>const API="/api";async function load(){try{const r=await fetch(API+"/stats");const d=await r.json();document.getElementById("pending-count").textContent=d.pending||0;document.getElementById("running-count").textContent=d.running||0;document.getElementById("completed-count").textContent=d.completed||0;document.getElementById("total-count").textContent=(d.pending||0)+(d.running||0)+(d.completed||0);const j=await fetch(API+"/jobs");const jobs=await j.json();document.getElementById("job-list").innerHTML=jobs.map(x=>`<div class="job-item"><div class="job-details"><div class="job-type">${x.job_type}</div><div class="job-params">${x.params}</div><div class="job-time">${new Date(x.created_at).toLocaleString()}</div></div><span class="badge badge-${x.status}">${x.status}</span></div>`).join("")}catch(e){console.error(e)}}document.getElementById("submit-form").addEventListener("submit",async e=>{e.preventDefault();const f=new FormData(e.target);try{const r=await fetch(API+"/submit",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({job_type:f.get("job_type"),params:f.get("params")})});if(r.ok){document.getElementById("alert-container").innerHTML='<div class="alert alert-success">Job submitted!</div>';e.target.reset();setTimeout(()=>load(),500)}else{const err=await r.json();document.getElementById("alert-container").innerHTML=`<div class="alert alert-error">Error: ${err.error}</div>`}}catch(e){document.getElementById("alert-container").innerHTML=`<div class="alert alert-error">Error: ${e.message}</div>`}});load();setInterval(load,3000)</script></body></html>'''

@app.route('/')
def index():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/stats')
def stats():
    try:
        jobs = db.collection('jobs').stream()
        p = r = c = 0
        for job in jobs:
            s = job.to_dict().get('status', '')
            if s == 'pending': p += 1
            elif s == 'running': r += 1
            elif s == 'completed': c += 1
        return jsonify({'pending': p, 'running': r, 'completed': c})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/jobs')
def jobs_list():
    try:
        jobs = []
        for doc in db.collection('jobs').order_by('created_at', direction=firestore.Query.DESCENDING).limit(20).stream():
            job = doc.to_dict()
            job['id'] = doc.id
            jobs.append(job)
        return jsonify(jobs)
    except:
        return jsonify([])

@app.route('/api/submit', methods=['POST'])
def submit_job():
    try:
        data = request.json
        job_type = data.get('job_type')
        params = data.get('params', '')
        if not job_type or job_type not in ['fiber_hunter', 'mapman', 'dot_extractor']:
            return jsonify({'error': 'Invalid'}), 400
        doc = db.collection('jobs').document()
        doc.set({'job_type': job_type, 'params': params, 'status': 'pending', 'created_at': datetime.now().isoformat(), 'output': '', 'error': ''})
        Thread(target=execute_job, args=(doc.id, job_type, params)).start()
        return jsonify({'id': doc.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

def execute_job(job_id, job_type, params):
    try:
        db.collection('jobs').document(job_id).update({'status': 'running'})
        output = ''
        if job_type == 'fiber_hunter':
            result = subprocess.run(['python', '-m', 'fiber_hunter', '--city', params], capture_output=True, text=True, timeout=1800)
            output = result.stdout[:5000]
        elif job_type == 'mapman':
            result = subprocess.run(['python', '-m', 'themapman', '--city', params], capture_output=True, text=True, timeout=1800)
            output = result.stdout[:5000]
        elif job_type == 'dot_extractor':
            result = subprocess.run(['python', '-m', 'hunter_dot_extractor', '--drive-folder', params], capture_output=True, text=True, timeout=3600)
            output = result.stdout[:5000]
        db.collection('jobs').document(job_id).update({'status': 'completed', 'output': output, 'completed_at': datetime.now().isoformat()})
    except subprocess.TimeoutExpired:
        db.collection('jobs').document(job_id).update({'status': 'error', 'error': 'timeout'})
    except Exception as e:
        db.collection('jobs').document(job_id).update({'status': 'error', 'error': str(e)})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
