# Optimus Portal v1

Mobile-Chrome-first group chat portal. Reads + writes the team Drive doc.

## Local run (Pydroid or PC)

1. Make sure `google_creds.json` is at `/storage/emulated/0/Download/google_creds.json` on phone, or set `GOOGLE_CREDS_JSON` env var on PC.
2. `pip install -r requirements.txt`
3. `python app.py`
4. Open http://127.0.0.1:5000 (it redirects to /optimus-houston-2026/chat)

## Deploy to Render

1. Sign in at https://render.com (use GitHub login).
2. Dashboard -> New -> Blueprint.
3. Pick the repo `patricksiado-prog/optimus-map-tools`.
4. Render reads `portal/render.yaml` automatically.
5. When prompted, set the env var `GOOGLE_CREDS_JSON` to the full contents of your `google_creds.json` file (paste the whole JSON in).
6. Click Apply. Build takes ~2-3 min.
7. Render gives you a URL. Chat lives at `<url>/optimus-houston-2026/chat`.

Free tier sleeps after 15 min idle (~30s cold start on first hit).
