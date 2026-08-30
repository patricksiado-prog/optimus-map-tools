#!/usr/bin/env bash
# Counts Patrick's messages and demands a brain write every 5th one.
#
# WHY THIS IS A HOOK AND NOT A RULE IN CLAUDE.md: Patrick asked on 2026-08-30
# for the brain to be written "every 5th request from me". A rule in a file is
# something Claude has to remember to obey, and the whole reason he asked is
# that remembering is exactly what keeps failing. A hook counts, so nothing has
# to be remembered. Same reasoning as the SessionStart hook beside it.
#
# Never blocks and never fails the turn: it prints to stdout, which the harness
# feeds into context, and exits 0 no matter what.
set -uo pipefail

DIR="${CLAUDE_PROJECT_DIR:-.}/.claude/hooks"
COUNT_FILE="$DIR/.prompt-count"
EVERY=5

N=0
[ -f "$COUNT_FILE" ] && N=$(cat "$COUNT_FILE" 2>/dev/null | tr -dc '0-9')
[ -z "$N" ] && N=0
N=$((N + 1))
echo "$N" > "$COUNT_FILE" 2>/dev/null || true

SINCE=$((N % EVERY))
if [ "$SINCE" -ne 0 ]; then
  DUE=$((EVERY - SINCE))
  echo "[brain] message $N — brain write due in $DUE."
  exit 0
fi

BRAIN="${CLAUDE_PROJECT_DIR:-.}/CLAUDE.md"
STAMP=$(grep -m1 '^# CURRENT STATE' "$BRAIN" 2>/dev/null | sed 's/.*updated //')
UNPUSHED=$(cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null \
  && git log --oneline @{u}..HEAD 2>/dev/null | wc -l | tr -d ' ')
[ -z "$UNPUSHED" ] && UNPUSHED=0

cat <<BANNER

==============================================================
 BRAIN WRITE IS DUE — message $N (every $EVERY, Patrick's standing
 instruction, 2026-08-30). Do this in THIS turn, not later.
==============================================================
 CURRENT STATE block last updated: ${STAMP:-UNKNOWN}
 Unpushed commits on this branch: $UNPUSHED

 Before you answer, write down anything from the last $EVERY
 messages that a future session would otherwise lose:
   - decisions he made, and anything he killed ("no", "don't")
   - numbers you MEASURED this turn, with how and when
   - what is now broken, fixed, or newly blocked on him
   - corrections to something the brain currently claims

 Then update the CURRENT STATE block if any line in it changed,
 commit, and PUSH. A finding that lives only in this chat dies
 with this session — that is the whole point of the counter.

 Nothing new to record? Say so in one line and move on. Do not
 invent an entry to satisfy the counter.
==============================================================

BANNER
exit 0
