"""
mirror_to_drive.py
==================
Drop-in helper. Mirrors files to Drive folder Claude can read.

Usage in any push script:
    import mirror_to_drive
    mirror_to_drive.upload("BRAIN.md", content_string)
"""
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload

FOLDER_NAME = "Optimus-Claude-Context"
CREDS_CANDIDATES = [
    "/storage/emulated/0/Download/google_creds.json",
    "/storage/emulated/0/google_creds.json",
    "./google_creds.json",
]
SCOPES = ["https://www.googleapis.com/auth/drive"]

_drive = None
_folder_id = None

def _init():
    global _drive, _folder_id
    if _drive is not None:
        return
    p = next((c for c in CREDS_CANDIDATES if os.path.exists(c)), None)
    if not p:
        raise FileNotFoundError("google_creds.json not found")
    creds = Credentials.from_service_account_file(p, scopes=SCOPES)
    _drive = build("drive", "v3", credentials=creds)
    q = (f"name='{FOLDER_NAME}' and "
         f"mimeType='application/vnd.google-apps.folder' and trashed=false")
    res = _drive.files().list(q=q, fields="files(id)").execute()
    folders = res.get("files", [])
    if not folders:
        raise RuntimeError(f"Folder {FOLDER_NAME!r} not found. Run setup first.")
    _folder_id = folders[0]["id"]

def upload(filename, content):
    """Create or update file in the Claude-Context folder."""
    _init()
    if isinstance(content, str):
        content = content.encode("utf-8")
    media = MediaInMemoryUpload(content, mimetype="text/markdown")
    q = f"name='{filename}' and '{_folder_id}' in parents and trashed=false"
    found = _drive.files().list(q=q, fields="files(id)").execute().get("files", [])
    if found:
        _drive.files().update(fileId=found[0]["id"], media_body=media).execute()
        print(f"  [drive] updated {filename}")
    else:
        meta = {"name": filename, "parents": [_folder_id]}
        _drive.files().create(body=meta, media_body=media).execute()
        print(f"  [drive] created {filename}")
