# Giving Claude Access to Private Repo Files

## The problem
optimus-map-tools is a private GitHub repo. Claude cannot fetch files from it
directly — even with a raw URL, GitHub blocks unauthenticated requests to
private repos and Claude has no auth token on its side.

## Two ways to give Claude access during a chat

### Option A — paste the raw URL (only if you make the repo public)
If repo is public:
  https://raw.githubusercontent.com/patricksiado-prog/optimus-map-tools/main/BRAIN.md
  https://raw.githubusercontent.com/patricksiado-prog/optimus-map-tools/main/themapman.py
Claude fetches it via web_fetch and reads it inline.

Public repo tradeoff: GitHub token, Sheet ID, Location ID, service account
email — none of these should sit in a public repo. Token especially. If going
public, audit all files first and move secrets to .env or a private gist.

### Option B — paste the content directly into chat (works while private)
- Copy/paste the file contents into the chat message
- For BRAIN.md: open it in any text editor on phone, select all, paste
- For code files: same thing
- Claude reads from chat directly, no auth needed

Option B is the right default. Repo stays private, Claude still gets context
on whatever specific file matters for that conversation.

## What this means going forward
When asking Claude "check brain" or "look at the X file":
- Don't expect Claude to fetch from the private repo
- Either paste the relevant section into chat
- Or summarize the current state in your message ("Map Man is at v9.5,
  card-only mode, no addresses yet")
- Claude can then reason from what's actually in front of it

## Pasted-URL trap
If Claude says "paste the raw URL" and the repo is private, the fetch will
fail silently or return a 404-like error. Don't burn time on that loop —
go straight to pasting content.
