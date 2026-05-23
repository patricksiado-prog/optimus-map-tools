#!/usr/bin/env python3
"""Optimus Portal - Cloud Run Flask app with lazy Firestore init"""

from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import logging
import os

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
            log.info("Firestore connected")
        except Exception as e:
            log.warning(f"Firestore offline: {e}")
            _db = False
    return _db if _db is not False else None

HTML = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Optimus Portal</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto; background: linear-gradient(135deg, #667eea, #764ba2); min-height: 100vh; padding: 20px; }
    .container { max-width: 1200px; margin: 0 auto; }
    header { background: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; }
    h1 { font-size: 2em; color: #333; }
    p { color: #666; margin-top: 5px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
    .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,.1); }
    .card h3 { color: #666; font-size: .9em; margin-bottom: 10px; text-transform: uppercase; }
    .value { font-size: 2.5em; font-weight: bold; color: #667eea; }
    .form { background: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; }
    .form-group { margin-bottom: 20px; }
    label { display: block; margin-bottom: 5px; color: #333; font-weight: 500; }
    input, select, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-family: monospace; }
    button { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 10px 20px; border: 0; border-radius: 4px; cursor: pointer; font-weight: 600; }
    button:hover { opacity: .9; }
    .jobs { background: white; padding: 30px; border-radius: 8px; }
    .job { padding: 15px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
    .job-type { font-weight: 600; color: #333; }
    .badge { padding: 5px 12px; border-radius: 20px; font-size: .85em; font-weight: 600; }
    .badge-pending { background: #ffc107; color: #333; }
    .badge-running { background: #17a2b8; color: white; }
    .badge-completed { background: #28a745; color: white; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>Optimus Portal</h1>
      <p>Fiber Scanner Dashboard</p>
    </header>
    
    <div class="grid">
      <div class="card">
        <h3>Pending</h3>
        <div class="value" id="pending">-</div>
      </div>
      <div class="card">
        <h3>Running</h3>
        <div class="value" id="running">-</div>
      </div>
      <div class="card">
        <h3>Completed</h3>
        <div class="value" id="completed">-</div>
      </div>
    </div>
    
    <div class="form">
      <h2>Submit Job</h2>
      <form id="jobForm">
        <div class="form-group">
          <label>Job Type</label>
          <select name="type" required>
            <option value="">-- Select --</option>
            <option value="fiber_hunter">Fiber Hunter</option>
            <option value="mapman">Map Enrichment</option>
            <option value="dot_extractor">Dot Extractor</option>
          </select>
        </div>
        <div class="form-group">
          <label>Parameters</label>
          <textarea name="params" placeholder="e.g., Houston, TX" required rows="3"></textarea>
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
    
    <div class="jobs">
      <h2>Jobs</h2>
      <div id="jobList">Loading...</div>
    </div>
  </div>
  
  <script>
    async function load() {
      try {
        const stats = await fetch('/api/stats').then(r => r.json());
        document.getElementById('pending').textContent = stats.pending || 0;
        document.getElementById('running').textContent = stats.running || 0;
        document.getElementById('completed').textContent = stats.completed || 0;
        
        const jobs = await fetch('/api/jobs').then(r => r.json());
        document.getElementById('jobList').innerHTML = jobs.map(j => 
          `<div class="job">
            <div><strong>${j.job_type}</strong><br><span style="color: #666; font-size: .9em;">${j.params}</span></div>
            <span class="badge badge-${j.status}">${j.status}</span>
          </div>`
        ).join('');
      } catch (e) {
        console.error(e);
      }
    }
    
    document.getElementById('jobForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const form = new FormData(e.target);
      await fetch('/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ job_type: form.get('type'), params: form.get('params') })
      });
      e.target.reset();
      load();
    });
    
    load();
    setInterval(load, 3000);
  </script>
</body>
</html>"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/stats')
def stats():
    try:
        db = get_db()
        if not db:
            return jsonify({'pending': 0, 'running': 0, 'completed': 0})
        
        jobs = list(db.collection('jobs').stream())
        pending = sum(1 for j in jobs if j.to_dict().get('status') == 'pending')
        running = sum(1 for j in jobs if j.to_dict().get('status') == 'running')
        completed = sum(1 for j in jobs if j.to_dict().get('status') == 'completed')
        
        return jsonify({'pending': pending, 'running': running, 'completed': completed})
    except Exception as e:
        log.error(f"Stats error: {e}")
        return jsonify({'pending': 0, 'running': 0, 'completed': 0})

@app.route('/api/jobs')
def jobs_list():
    try:
        db = get_db()
        if not db:
            return jsonify([])
        
        jobs = []
        for doc in db.collection('jobs').order_by('created_at', direction='descending').limit(20).stream():
            job = doc.to_dict()
            job['id'] = doc.id
            jobs.append(job)
        return jsonify(jobs)
    except Exception as e:
        log.error(f"Jobs error: {e}")
        return jsonify([])

@app.route('/api/submit', methods=['POST'])
def submit_job():
    try:
        data = request.json
        job_type = data.get('job_type')
        params = data.get('params', '')
        
        if not job_type or job_type not in ['fiber_hunter', 'mapman', 'dot_extractor']:
            return jsonify({'error': 'Invalid job type'}), 400
        
        db = get_db()
        if not db:
            return jsonify({'error': 'Database offline'}), 503
        
        doc = db.collection('jobs').document()
        doc.set({
            'job_type': job_type,
            'params': params,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'output': '',
            'error': ''
        })
        
        return jsonify({'id': doc.id}), 201
    except Exception as e:
        log.error(f"Submit error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'optimus-portal'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    log.info(f"Starting Portal on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
