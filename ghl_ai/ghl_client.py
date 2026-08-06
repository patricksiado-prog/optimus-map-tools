#!/usr/bin/env python3
"""
ghl_client.py -- thin GoHighLevel REST helper (LeadConnector API v2).

Reaches the parts of GHL the official MCP does NOT expose: custom fields,
contact search, bulk tagging, opportunities, add-to-workflow, SMS send.

Auth: a full-scope Private Integration Token in env var GHL_TOKEN, plus
GHL_LOCATION_ID. NOTE: this must run where outbound to
services.leadconnectorhq.com is allowed (your machine / Render / Cloud Run) --
the Claude container is network-blocked from GHL ("Host not in allowlist").

Quick use:
  export GHL_TOKEN=pit-...   GHL_LOCATION_ID=TXw28sw0Z2rI6tcCDhJY
  python ghl_client.py whoami
  python ghl_client.py customfields
  python ghl_client.py search --query "fiber" --limit 5
  python ghl_client.py tag --contact <id> --tags att-fiber-drip,hot
  python ghl_client.py send --contact <id> --message "Hi from AT&T Fiber"
  python ghl_client.py add-to-workflow --contact <id> --workflow <workflowId>
"""
import os
import sys
import json
import argparse
import requests

BASE = "https://services.leadconnectorhq.com"
VER_DEFAULT = "2021-07-28"     # most endpoints
VER_CONV = "2021-04-15"        # conversations/messages

TOKEN = os.environ.get("GHL_TOKEN", "")
LOCATION = os.environ.get("GHL_LOCATION_ID", "")


def _headers(version=VER_DEFAULT):
    return {
        "Authorization": "Bearer " + TOKEN,
        "Version": version,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _req(method, path, version=VER_DEFAULT, **kw):
    if not TOKEN:
        sys.exit("GHL_TOKEN not set")
    r = requests.request(method, BASE + path, headers=_headers(version), timeout=30, **kw)
    if r.status_code >= 400:
        raise RuntimeError("%s %s -> %s %s" % (method, path, r.status_code, r.text[:400]))
    return r.json() if r.text else {}


# ---- reads -----------------------------------------------------------------
def whoami():
    """Confirms the token + location work."""
    return _req("GET", "/locations/" + LOCATION)


def custom_fields():
    return _req("GET", "/locations/" + LOCATION + "/customFields")


def search(query="", limit=20):
    body = {"locationId": LOCATION, "page": 1, "pageLimit": limit}
    if query:
        body["query"] = query
    return _req("POST", "/contacts/search", json=body)


def get_contact(cid):
    return _req("GET", "/contacts/" + cid)


# ---- writes ----------------------------------------------------------------
def upsert(contact):
    contact = dict(contact)
    contact.setdefault("locationId", LOCATION)
    return _req("POST", "/contacts/upsert", json=contact)


def add_tags(cid, tags):
    return _req("POST", "/contacts/" + cid + "/tags", json={"tags": tags})


def set_custom_field(cid, field_id, value):
    body = {"customFields": [{"id": field_id, "value": value}]}
    return _req("PUT", "/contacts/" + cid, json=body)


def send_sms(cid, message, msg_type="SMS"):
    body = {"type": msg_type, "contactId": cid, "message": message}
    return _req("POST", "/conversations/messages", version=VER_CONV, json=body)


def add_to_workflow(cid, workflow_id):
    return _req("POST", "/contacts/" + cid + "/workflow/" + workflow_id, json={})


# ---- cli -------------------------------------------------------------------
def main():
    p = argparse.ArgumentParser(description="GHL REST helper")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("whoami")
    sub.add_parser("customfields")

    s = sub.add_parser("search"); s.add_argument("--query", default=""); s.add_argument("--limit", type=int, default=20)
    g = sub.add_parser("get"); g.add_argument("--contact", required=True)
    t = sub.add_parser("tag"); t.add_argument("--contact", required=True); t.add_argument("--tags", required=True)
    m = sub.add_parser("send"); m.add_argument("--contact", required=True); m.add_argument("--message", required=True)
    w = sub.add_parser("add-to-workflow"); w.add_argument("--contact", required=True); w.add_argument("--workflow", required=True)

    a = p.parse_args()
    if a.cmd == "whoami":
        out = whoami()
    elif a.cmd == "customfields":
        out = custom_fields()
    elif a.cmd == "search":
        out = search(a.query, a.limit)
    elif a.cmd == "get":
        out = get_contact(a.contact)
    elif a.cmd == "tag":
        out = add_tags(a.contact, [x.strip() for x in a.tags.split(",") if x.strip()])
    elif a.cmd == "send":
        out = send_sms(a.contact, a.message)
    elif a.cmd == "add-to-workflow":
        out = add_to_workflow(a.contact, a.workflow)
    print(json.dumps(out, indent=2)[:4000])


if __name__ == "__main__":
    main()
