
import subprocess,sys,os,json,threading
from http.server import HTTPServer,BaseHTTPRequestHandler
from pathlib import Path
PORT=5050
DESK=Path(os.path.expanduser("~"))/"Desktop"
SCRIPTS={"extractor":str(DESK/"hunter_dot_extractor.py"),"mapman":str(DESK/"THEMAPMAN.py"),"hunter":str(DESK/"fiber_hunter.py")}
MAPMAN_ARGS=["--no-update","--commercial-only"]
_procs={};_logs={k:[]for k in SCRIPTS}
def _stream(n,p):
    for l in iter(p.stdout.readline,b""):
        _logs[n].append(l.decode(errors="replace").rstrip())
        if len(_logs[n])>500:_logs[n]=_logs[n][-500:]
    p.wait()
def start_script(n):
    if n not in SCRIPTS:return{"ok":False,"error":"unknown"}
    if n in _procs and _procs[n].poll() is None:return{"ok":False,"error":"already running"}
    if not os.path.exists(SCRIPTS[n]):return{"ok":False,"error":f"not found: {SCRIPTS[n]}"}
    args=[sys.executable,SCRIPTS[n]]+(MAPMAN_ARGS if n=="mapman" else [])
    _logs[n]=[]
    p=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,cwd=str(DESK))
    _procs[n]=p;threading.Thread(target=_stream,args=(n,p),daemon=True).start()
    return{"ok":True,"msg":f"{n} started"}
def stop_script(n):
    p=_procs.get(n)
    if not p or p.poll() is not None:return{"ok":False,"error":"not running"}
    p.terminate();return{"ok":True,"msg":f"{n} stopped"}
def status():
    out={k:("running"if k in _procs and _procs[k].poll() is None else"stopped")for k in SCRIPTS}
    return out
class H(BaseHTTPRequestHandler):
    def log_message(self,*a):pass
    def _s(self,c,o):
        b=json.dumps(o).encode()
        self.send_response(c);self.send_header("Content-Type","application/json");self.send_header("Access-Control-Allow-Origin","*");self.send_header("Content-Length",len(b));self.end_headers();self.wfile.write(b)
    def do_OPTIONS(self):
        self.send_response(200);self.send_header("Access-Control-Allow-Origin","*");self.send_header("Access-Control-Allow-Methods","GET,POST,OPTIONS");self.send_header("Access-Control-Allow-Headers","Content-Type");self.end_headers()
    def do_GET(self):
        if self.path=="/status":self._s(200,status())
        elif self.path.startswith("/logs/"):self._s(200,{"lines":_logs.get(self.path.split("/")[-1],[])[-100:]})
        else:self._s(404,{"error":"not found"})
    def do_POST(self):
        b=json.loads(self.rfile.read(int(self.headers.get("Content-Length",0)))or b"{}")
        if self.path=="/start":self._s(200,start_script(b.get("script","")))
        elif self.path=="/stop":self._s(200,stop_script(b.get("script","")))
        else:self._s(404,{"error":"not found"})
if __name__=="__main__":
    print(f"Optimus Server at http://localhost:{PORT}");HTTPServer(("localhost",PORT),H).serve_forever()
