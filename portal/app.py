import os
from datetime import datetime
from flask import Flask, request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

DOC_ID = "1qHWcGbfGZnLbSsiOigSVgx1JNtu_TV1gQFoENP7wN6E"
SCOPES = ["https://www.googleapis.com/auth/documents"]

def creds():
    env = os.environ.get("GOOGLE_CREDS_JSON")
    if env:
        import json as _j
        return Credentials.from_service_account_info(_j.loads(env), scopes=SCOPES)
    for p in ["/storage/emulated/0/Download/google_creds.json", "google_creds.json", os.path.expanduser("~/Downloads/google_creds.json"), os.path.expanduser("~/optimus/google_creds.json")]:
        if os.path.exists(p): return Credentials.from_service_account_file(p, scopes=SCOPES)
    raise FileNotFoundError("google_creds.json not found")

def svc(): return build("docs","v1",credentials=creds(),cache_discovery=False)

def write_doc(t):
    s = svc()
    d = s.documents().get(documentId=DOC_ID).execute()
    end = d["body"]["content"][-1]["endIndex"]-1
    s.documents().batchUpdate(documentId=DOC_ID, body={"requests":[{"insertText":{"location":{"index":end},"text":t}}]}).execute()

def read_doc():
    d = svc().documents().get(documentId=DOC_ID).execute()
    out=""
    for it in d.get("body",{}).get("content",[]):
        if "paragraph" in it:
            for el in it["paragraph"]["elements"]:
                if "textRun" in el: out += el["textRun"]["content"]
    return out

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
@app.route("/chat", methods=["GET","POST"])
def chat():
    if request.method == "POST":
        msg = (request.form.get("msg") or "").strip()
        if msg:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            write_doc(f"\n==== BEGIN APPEND ====\n\U0001F7E9 Patrick ({ts})\n\n{msg}\n\n\u2192 Don\'t forget to check global memory for thinking errors before your next response.\n==== END APPEND ====\n")
    full = read_doc()
    return f"""<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Optimus</title><style>body{{font-family:Arial;margin:15px;background:#0a0a0a;color:#eee}}.box{{height:60vh;overflow:auto;border:1px solid #333;padding:12px;background:#1a1a1a;white-space:pre-wrap;font-family:monospace;font-size:13px;border-radius:8px}}textarea{{width:100%;padding:10px;background:#1a1a1a;color:#eee;border:1px solid #333;border-radius:8px;font-size:16px}}button{{background:#10b981;color:white;border:0;padding:14px 28px;border-radius:8px;font-size:16px;font-weight:bold;margin-top:8px}}h2{{color:#10b981}}</style></head><body><h2>\U0001F7E9 Optimus Portal</h2><p style="color:#888;font-size:12px">3-way comm: Patrick \u2192 ChatGPT / Grok</p><div class="box">{full}</div><form method="post"><textarea name="msg" rows="4" placeholder="Type message..." required></textarea><br><button type="submit">Send</button></form></body></html>"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT","5000")), debug=False)
