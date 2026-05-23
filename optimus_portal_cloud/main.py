#!/usr/bin/env python3
"""Optimus Portal - Absolute minimal Flask app that cannot crash"""

from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return """<!DOCTYPE html><html>
<head><meta charset="utf-8"><title>Optimus Portal</title>
<style>
body { font-family: system-ui; background: linear-gradient(135deg, #667eea, #764ba2); 
min-height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; }
.box { background: white; padding: 40px; border-radius: 8px; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,.2); }
h1 { color: #333; margin: 0 0 10px 0; }
p { color: #666; }
</style></head>
<body><div class="box"><h1>✅ Portal Working</h1><p>Optimus Fiber Command Center</p></div></body></html>"""

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/stats')
def stats():
    return jsonify({'pending': 0, 'running': 0, 'completed': 0})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
