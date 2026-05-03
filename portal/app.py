"""Optimus Portal v1 - mobile-Chrome-first group chat portal."""
import os, re, html
from datetime import datetime
from flask import Flask, request, redirect, url_for
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

DOC_ID = "1qHWcGbfGZnLbSsiOigSVgx1JNtu_TV1gQFoENP7wN6E"
CREDS_FILE_PATH = "/storage/emulated/0/Download/google_creds.json"
CREDS_JSON_ENV = "GOOGLE_CREDS_JSON"
SCOPES = ["https://www.googleapis.com/auth/documents"]
TAIL = 50

STYLE = {
    "Patrick": {"bar":"bg-emerald-500","name":"text-emerald-400","emoji":"\U0001F7E9"},
    "Claude":  {"bar":"bg-yellow-500","name":"text-yellow-300","emoji":"\U0001F7E8"},
    "ChatGPT": {"bar":"bg-blue-500","name":"text-blue-300","emoji":"\U0001F7E6"},
    "Grok":    {"bar":"bg-red-500","name":"text-red-300","emoji":"\U0001F7E5"},
}
DEFAULT = {"bar":"bg-zinc-500","name":"text-zinc-300","emoji":"\u26AA"}

def creds():
    env = os.environ.get(CREDS_JSON_ENV)
    if env:
        import json as _j
        return Credentials.from_service_account_info(_j.loads(env), scopes=SCOPES)
    return Credentials.from_service_account_file(CREDS_FILE_PATH, scopes=SCOPES)

def svc():
    return build("docs","v1",credentials=creds(),cache_discovery=False)

def read_doc():
    d = svc().documents().get(documentId=DOC_ID).execute()
    out=[]
    for it in d.get("body",{}).get("content",[]):
        if "paragraph" in it:
            for el in it["paragraph"]["elements"]:
                tr = el.get("textRun")
                if tr and "content" in tr: out.append(tr["content"])
    return "".join(out)

def append(text):
    s = svc()
    d = s.documents().get(documentId=DOC_ID).execute()
    end = d["body"]["content"][-1]["endIndex"]-1
    full = read_doc()
    pre = "\n" if full and not full.endswith("\n") else ""
    payload = pre + text + ("" if text.endswith("\n") else "\n")
    s.documents().batchUpdate(documentId=DOC_ID,body={"requests":[
        {"insertText":{"location":{"index":end},"text":payload}}]}).execute()

BLOCK = re.compile(r"==== BEGIN APPEND ====\s*\n(.*?)\n==== END APPEND ====", re.DOTALL)
SPK = re.compile(r"^[\U0001F7E5\U0001F7E6\U0001F7E8\U0001F7E9\u26AA]?\s*(Patrick|Claude|ChatGPT|Grok)\b\s*(?:\(([^)]*)\))?")

def parse(t):
    msgs=[]
    for m in BLOCK.finditer(t):
        body = m.group(1).strip()
        lines = body.split("\n")
        spk,ts,bl = "Unknown","",lines
        if lines:
            sm = SPK.match(lines[0].strip())
            if sm:
                spk = sm.group(1); ts = sm.group(2) or ""; bl = lines[1:]
        bt = "\n".join(bl).strip()
        bt = re.sub(r"\n?\u2192 Don't forget to check global memory.*?next response\.\s*$","",bt,flags=re.I).strip()
        if bt: msgs.append({"speaker":spk,"ts":ts,"body":bt})
    return msgs

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root(): return redirect(url_for("chat"))

@app.route("/optimus-houston-2026/chat", methods=["GET","POST"])
def chat():
    err = None
    if request.method == "POST":
        msg = (request.form.get("msg") or "").strip()
        if msg:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            block = ("==== BEGIN APPEND ====\n"
                "\U0001F7E9 Patrick (" + ts + ")\n\n" + msg + "\n\n"
                "\u2192 Don't forget to check global memory for thinking errors before your next response.\n"
                "==== END APPEND ====")
            try: append(block)
            except Exception as e: err = "Send failed: " + str(e)
        return redirect(url_for("chat"))
    try:
        msgs = parse(read_doc())
    except Exception as e:
        msgs = []; err = "Read failed: " + str(e)
    return render(msgs[-TAIL:] if msgs else [], err)

HEAD = """<!DOCTYPE html><html><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="10"><title>Optimus</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>body{background:#09090b}textarea,input{font-size:16px!important}</style>
</head>"""

def render(msgs, err):
    bs=[]
    for m in msgs:
        s = STYLE.get(m["speaker"], DEFAULT)
        body = html.escape(m["body"]).replace("\n","<br>")
        bs.append('<div class="mb-4"><div class="flex gap-2 mb-1">'
            '<span class="font-semibold ' + s["name"] + '">' + s["emoji"] + ' ' + html.escape(m["speaker"]) + '</span>'
            '<span class="text-xs text-zinc-500">' + html.escape(m["ts"]) + '</span></div>'
            '<div class="border-l-4 ' + s["bar"] + ' bg-zinc-900 rounded-r-xl px-4 py-3 text-zinc-100">' + body + '</div></div>')
    if not bs: bs.append('<div class="text-zinc-500 text-center py-8">No messages yet.</div>')
    eh = ('<div class="bg-red-900 text-red-100 px-4 py-2 rounded mb-3">' + html.escape(err) + '</div>') if err else ""
    return (HEAD + '<body class="text-zinc-100"><div class="max-w-2xl mx-auto flex flex-col" style="min-height:100vh">'
        '<header class="sticky top-0 bg-zinc-950 border-b border-zinc-800 px-4 py-3"><div class="font-bold text-lg">\U0001F7E9 Optimus</div><div class="text-xs text-zinc-500">auto-refresh 10s</div></header>'
        '<main class="flex-1 px-4 py-4">' + eh + "".join(bs) + '</main>'
        '<form method="POST" class="sticky bottom-0 bg-zinc-950 border-t border-zinc-800 px-3 py-3 flex gap-2">'
        '<textarea name="msg" rows="2" placeholder="Type as Patrick..." required class="flex-1 bg-zinc-900 border border-zinc-800 rounded-xl px-4 py-3 text-zinc-100"></textarea>'
        '<button class="bg-emerald-600 text-white font-semibold rounded-xl px-5">Send</button>'
        '</form></div></body></html>')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT","5000")), debug=False)
