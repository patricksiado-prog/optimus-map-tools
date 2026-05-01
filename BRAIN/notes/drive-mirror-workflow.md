# Claude Context via Drive Mirror

## Why this exists
GitHub repo is private — Claude can't fetch from it. So BRAIN files and any
source Claude needs to debug are mirrored to a Drive folder Claude reads via
the Google Drive connector. No public repo, no token exposure, no copy-paste.

## The folder
`Optimus-Claude-Context` — appears in "Shared with me" in Drive.
Owned by service account fiberscanner@fiberscanner-493900.iam.gserviceaccount.com,
shared with Patrick as Editor.

## How push scripts mirror to it
```python
import mirror_to_drive
mirror_to_drive.upload("BRAIN.md", content_string)
mirror_to_drive.upload("themapman.py", source_code_string)
```
Two lines after the GitHub push. Same content lands in both places.

## Saying "check brain" in chat
Claude pulls latest from the Drive folder. Claude knows the folder name from
its memory, no need to repeat it.

## What to mirror
- BRAIN.md (always)
- Any tool source you want Claude debugging this week (themapman.py,
  validation_man.py, addressman.py, etc.)
- Session summaries

## Setup (already done, here for reference)
Ran setup_drive_mirror.py once. It:
1. Created the Drive folder
2. Shared it with Patrick's Gmail
3. Pushed mirror_to_drive.py helper to repo
4. Pushed this note
