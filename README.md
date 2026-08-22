# optimus-map-tools

Optimus is an authorized AT&T dealer selling fiber across Houston metro,
Beaumont and Brazoria County. This repo holds the brain, the skills and the map
tooling. If you are Claude, `CLAUDE.md` is already loaded — start there.

## Two repos, and they do different jobs

| Repo | What it holds | Careful |
|---|---|---|
| **optimus-map-tools** (this one) | The brain, the skills, map tools | Safe to push. Nothing here auto-deploys. |
| **Go-High-Level-MCP-2026-Complete** | The hunter that scans the dealer map, and the GHL MCP server | **The hunter self-updates from it.** Any file listed in `_CORE_FILES` in `precise_fiber_hunter.py` reaches every hunter PC on next launch. A push there is a deploy. |

Hunter code pushed to *this* repo reaches nobody. That mistake has been made
before, which is why it is the first thing on this page.

## Where things live

| File | What it is | When to read it |
|---|---|---|
| **`CLAUDE.md`** | The operating brain. Loads automatically at the start of every Claude Code session in this repo. | Always — it arrives on its own. |
| **`BRAIN.md`** | Long-form memory. Depth behind CLAUDE.md, organised in numbered Parts. | On demand, when you need detail. |
| **`OPTIMUS_SESSION_LOG.md`** | Dated record of what happened in each session. | When you want history rather than facts. |
| **`.claude/skills/`** | Packaged workflows Claude runs. `gold-cluster-sweep` is the full lead loop. | Claude picks these up by itself. |
| **`docs/`** | Reference material. | As needed. |
| **`docs/archive/`** | Superseded material kept for history. | Rarely. Do not act on it. |

## Why CLAUDE.md exists

Claude Code reads `CLAUDE.md` from the repo root at the start of every session,
automatically. Before it existed, every session began by pasting a long handoff
prompt, and anything learned in a chat died with that chat.

It is deliberately short. A very large file loaded on every session burns
context and gets skimmed rather than read, so `CLAUDE.md` carries the operating
facts and points at `BRAIN.md` for depth.

## Keeping every surface on the same brain

Claude Code reads `CLAUDE.md` automatically, but only inside this repo. Cowork and
claude.ai load your **account's plugins** instead. So the brain ships as a plugin, and
this repo is its marketplace.

**One-time setup, per person:**

```
/plugin marketplace add patricksiado-prog/optimus-map-tools
/plugin install optimus
```

That installs two skills — `optimus-brain` (the context) and `gold-cluster-sweep` (the
lead loop) — and they then load in Cowork, claude.ai and Claude Code alike.

**Updating, from then on:**

1. Edit `CLAUDE.md` (short facts) or `BRAIN.md` (depth)
2. `python3 scripts/build_brain_skill.py` — regenerates the `optimus-brain` skill
3. Commit and push

Everyone picks the change up on their next plugin refresh. Nobody re-installs anything,
and nobody hand-copies a `.skill` file.

`optimus-brain/SKILL.md` is **generated** from `CLAUDE.md` and carries a do-not-edit
header. Editing it directly gets overwritten on the next build and lets the plugin drift
from the repo — which is the whole failure this setup exists to prevent.

## Keeping the brain alive

When something is learned that would change what a future session does:

- short fact → add it to `CLAUDE.md`
- detail, or a full session's findings → add a Part to `BRAIN.md`
- then **commit and push**

Anything not committed does not survive. A finding that lives only in a chat is
gone when that chat closes — that is exactly how one full write-up of the hunter
capture path was lost.

## Filenames

Keep names distinct without relying on capitalisation. The hunter PCs run
Windows, where `BRAIN.md` and `brain.md` are the same file — this repo used to
contain both plus a `BRAIN/` directory, which breaks a Windows checkout. That
has been cleaned up; don't reintroduce it.
