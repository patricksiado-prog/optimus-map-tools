"""
Optimus Portal v1 - mobile-Chrome-first group chat portal.

Reads + writes the shared group chat Google Doc via the fiberscanner
service account. No login (per Patrick's call). Auto-refreshes.
Color-coded speaker lanes for the four participants.

Local run:
    python app.py
    open http://127.0.0.1:5000

Render deploys this automatically via render.yaml.
"""

import os
import re
import html
from datetime import datetime
from flask import Flask, request, redirect, url_for

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# ---------- CONFIG ----------

DOC_ID = "1qHWcGbfGZnLbSsiOigSVgx1JNtu_TV1gQFoENP7wN6E"

CREDS_FILE_PATH = "/storage/emulated/0/Download/google_creds.json"
CREDS_JSON_ENV = "GOOGLE_CREDS_JSON"

SCOPES = ["https://www.googleapis.com/auth/documents"]

TAIL_MESSAGES = 50

SPEAKER_STYLE = {
    "Patrick":  {"bar": "bg-emerald-500", "name": "text-emerald-400", "emoji": "\U0001F7E9"},
    "Claude":   {"bar": "bg-yellow-500",  "name": "text-yellow-300",  "emoji": "\U0001F7E8"},
    "ChatGPT":  {"bar": "bg-blue-500",    "name": "text-blue-300",    "emoji": "\U0001F7E6"},
    "Grok":     {"bar": "bg-red-500",     "name": "text-red-300",     "emoji": "\U0001F7E5"},
}
DEFAULT_STYLE = {"bar": "bg-zinc-500", "name": "text-zinc-300", "emoji": "\u26AA"}


def get_credentials():
    env_json = os.environ.get(CREDS_JSON_ENV)
    if env_json:
        import json as _json
        info = _json.loads(env_json)
        return Credentials.from_service_account_info(info, scopes=SCOPES)
    return Credentials.from_service_account_file(CREDS_FILE_PATH, scopes=SCOPES)


def get_service():
    return build("docs", "v1", credentials=get_credentials(), cache_discovery=False)


def read_doc_text():
    service = get_service()
    doc = service.documents().get(documentId=DOC_ID).execute()
    out = []
    for item in doc.get("body", {}).get("content", []):
        if "paragraph" in item:
            for elem in item["paragraph"]["elements"]:
                tr = elem.get("textRun")
                if tr and "content" in tr:
                    out.append(tr["content"])
    return "".join(out)


def append_to_doc(text):
    service = get_service()
    doc = service.documents().get(documentId=DOC_ID).execute()
    end_index = doc["body"]["content"][-1]["endIndex"] - 1

    full_text = read_doc_text()
    needs_leading_nl = bool(full_text) and not full_text.endswith("\n")
    payload = ("\n" if needs_leading_nl else "") + text
    if not payload.endswith("\n"):
        payload += "\n"

    service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": [
            {"insertText": {"location": {"index": end_index}, "text": payload}}
        ]},
    ).execute()


APPEND_BLOCK = re.compile(
    r"==== BEGIN APPEND ====\s*\n(.*?)\n==== END APPEND ====",
    re.DOTALL,
)

SPEAKER_LINE = re.compile(
    r"^[\U0001F7E5\U0001F7E6\U0001F7E8\U0001F7E9\u26AA]?\s*"
    r"(Patrick|Claude|ChatGPT|Grok)\b\s*"
    r"(?:\(([^)]*)\))?",
)


def parse_messages(doc_text):
    msgs = []
    for m in APPEND_BLOCK.finditer(doc_text):
        body = m.group(1).strip()
        lines = body.split("\n")
        speaker = "Unknown"
        ts = ""
        body_lines = lines

        if lines:
            sm = SPEAKER_LINE.match(lines[0].strip())
            if sm:
                speaker = sm.group(1)
                ts = sm.group(2) or ""
                body_lines = lines[1:]

        body_text = "\n".join(body_lines).strip()

        body_text = re.sub(
            r"\n?\u2192 Don't forget to check global memory.*?next response\.\s*$",
            "",
            body_text,
            flags=re.IGNORECASE,
        ).strip()

        if body_text:
            msgs.append({"speaker": speaker, "ts": ts, "body": body_text})
    return msgs


app = Flask(__name__)


@app.route("/", methods=["GET"])
def root():
    return redirect(url_for("chat"))


@app.route("/optimus-houston-2026/chat", methods=["GET", "POST"])
def chat():
    error = None
    if request.method == "POST":
        msg = (request.form.get("msg") or "").strip()
        if msg:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            block = (
                "==== BEGIN APPEND ====\n"
                "\U0001F7E9 Patrick (" + ts + ")\n\n"
                + msg + "\n\n"
                "\u2192 Don't forget to check global memory for thinking errors before your next response.\n"
                "==== END APPEND ===="
            )
            try:
                append_to_doc(block)
            except Exception as e:
                error = "Send failed: " + str(e)
        return redirect(url_for("chat"))

    try:
        doc_text = read_doc_text()
        messages = parse_messages(doc_text)
    except Exception as e:
        doc_text = ""
        messages = []
        error = "Read failed: " + str(e)

    tail = messages[-TAIL_MESSAGES:] if messages else []
    return render(tail, error)


PAGE_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<meta http-equiv="refresh" content="10">
<title>Optimus</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
  html, body { height: 100%; }
  body { background: #09090b; }
  textarea, input { font-size: 16px !important; }
  .scroll-anchor { scroll-margin-bottom: 200px; }
</style>
</head>
"""


def render(messages, error):
    bubbles_html = []
    for m in messages:
        style = SPEAKER_STYLE.get(m["speaker"], DEFAULT_STYLE)
        safe_body = html.escape(m["body"]).replace("\n", "<br>")
        ts = html.escape(m["ts"])
        speaker = html.escape(m["speaker"])
        bubble = (
            '<div class="mb-4">'
            '  <div class="flex items-baseline gap-2 mb-1">'
            '    <span class="font-semibold ' + style["name"] + '">'
            + style["emoji"] + ' ' + speaker + '</span>'
            '    <span class="text-xs text-zinc-500">' + ts + '</span>'
            '  </div>'
            '  <div class="border-l-4 ' + style["bar"] + ' bg-zinc-900 rounded-r-xl px-4 py-3 text-zinc-100 text-base leading-relaxed">'
            + safe_body +
            '  </div>'
            '</div>'
        )
        bubbles_html.append(bubble)

    if not bubbles_html:
        bubbles_html.append(
            '<div class="text-zinc-500 text-center py-8">'
            'No messages yet. Send the first one below.'
            '</div>'
        )

    err_html = ""
    if error:
        err_html = (
            '<div class="bg-red-900 text-red-100 px-4 py-2 rounded-lg mb-3">'
            + html.escape(error) + '</div>'
        )

    body = (
        PAGE_HEAD +
        '<body class="text-zinc-100">'
        '<div class="max-w-2xl mx-auto flex flex-col" style="min-height: 100vh;">'
        '  <header class="sticky top-0 bg-zinc-950 border-b border-zinc-800 px-4 py-3 flex items-center gap-2 z-10">'
        '    <div class="text-2xl">\U0001F7E9</div>'
        '    <div>'
        '      <div class="font-bold text-lg">Optimus</div>'
        '      <div class="text-xs text-zinc-500">Group chat \u2022 auto-refresh 10s</div>'
        '    </div>'
        '  </header>'
        '  <main class="flex-1 px-4 py-4 overflow-y-auto">'
        + err_html
        + "".join(bubbles_html)
        + '    <div id="bottom" class="scroll-anchor"></div>'
        '  </main>'
        '  <form method="POST" class="sticky bottom-0 bg-zinc-950 border-t border-zinc-800 px-3 py-3 flex gap-2">'
        '    <textarea name="msg" rows="2" placeholder="Type as Patrick..." '
        '              class="flex-1 bg-zinc-900 border border-zinc-800 rounded-xl px-4 py-3 text-zinc-100 placeholder-zinc-500 resize-none" '
        '              required></textarea>'
        '    <button type="submit" '
        '            class="bg-emerald-600 hover:bg-emerald-500 active:bg-emerald-700 text-white font-semibold rounded-xl px-5">'
        '      Send'
        '    </button>'
        '  </form>'
        '</div>'
        '<script>'
        'window.addEventListener("load", function(){'
        '  var el = document.getElementById("bottom");'
        '  if (el) el.scrollIntoView();'
        '});'
        '</script>'
        '</body></html>'
    )
    return body


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
