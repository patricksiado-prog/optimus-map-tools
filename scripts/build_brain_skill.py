#!/usr/bin/env python3
"""Generate the `optimus-brain` skill from CLAUDE.md.

WHY THIS EXISTS
    CLAUDE.md only loads in Claude Code, and only inside this repo. Cowork and
    claude.ai assemble the account's SKILLS instead, so the same facts have to
    exist as a skill to reach those surfaces.

    Two hand-maintained copies of the same brain would drift, and a brain that
    disagrees with itself is worse than one place that is occasionally stale --
    you stop being able to tell which is true. So the skill is GENERATED from
    CLAUDE.md and never edited directly. Edit CLAUDE.md, re-run this, commit.

USAGE
    python3 scripts/build_brain_skill.py
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "CLAUDE.md")
OUT_DIR = os.path.join(ROOT, ".claude", "skills", "optimus-brain")
OUT = os.path.join(OUT_DIR, "SKILL.md")

DESCRIPTION = (
    "The Optimus operating brain — who Patrick Siado's AT&T fiber dealership is, "
    "the green/gold/grey dot legend and what each is worth, the master sheet and "
    "GoHighLevel IDs, which sheet tabs the hunter owns, and the texting, "
    "DealMachine and data-integrity facts that were learned the expensive way. "
    "Load this whenever the work touches Optimus, AT&T fiber leads, the fiber "
    "map, gold or green dots, the ATT FIBER LEADS sheet, GoHighLevel outreach, "
    "DealMachine skip tracing, or the hunter — and load it before texting, "
    "quoting a price, or spending DealMachine credits, because those are where "
    "the costly mistakes live."
)

HEADER = """---
name: optimus-brain
description: {desc}
---

<!-- GENERATED FILE — do not edit.
     Source: CLAUDE.md in patricksiado-prog/optimus-map-tools
     Rebuild: python3 scripts/build_brain_skill.py
     Editing this file directly gets overwritten and lets the brain drift. -->

# Optimus operating brain

This is the same brain Claude Code loads automatically from `CLAUDE.md` in the
`optimus-map-tools` repo. It exists as a skill so Cowork and claude.ai get the
same facts, since those surfaces load account skills rather than repo files.

For the full lead loop — cluster, enrich, text, book, follow up — use the
`gold-cluster-sweep` skill. This file is the context that loop runs on.

"""


def main():
    if not os.path.exists(SRC):
        sys.exit("CLAUDE.md not found at %s" % SRC)
    body = open(SRC, encoding="utf-8").read()

    # Drop CLAUDE.md's own first heading and its "Claude Code loads this file"
    # preamble; the skill states its own provenance above and repeating it reads
    # as a contradiction on a surface where it is NOT auto-loaded.
    lines = body.split("\n")
    start = 0
    for i, line in enumerate(lines):
        if line.startswith("## "):
            start = i
            break
    body = "\n".join(lines[start:]).strip() + "\n"

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(HEADER.format(desc=DESCRIPTION) + body)

    n = sum(1 for _ in open(OUT, encoding="utf-8"))
    print("wrote %s (%d lines) from CLAUDE.md" % (os.path.relpath(OUT, ROOT), n))


if __name__ == "__main__":
    main()
