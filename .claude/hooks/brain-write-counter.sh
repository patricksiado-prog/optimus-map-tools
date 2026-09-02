#!/usr/bin/env bash
# Two jobs, both on Patrick's instruction:
#
#   1. READ GUARD — prints on EVERY message. Added 2026-09-02 after ~4,800
#      DealMachine credits were spent enriching leads in the wrong market.
#      The brain ALREADY held the answer: line "Grab from GHL before spending
#      anything", and a measured list of the real gold streets (STACEWOOD,
#      NORWOOD, SHAKESPEARE, GALWAY, MONTERREY / LANGHAM, POTTER). Nobody
#      grepped for either. Patrick: "u wasted credits on shit that doesn't need
#      to be enriched that is already recorded in the brain."
#
#   2. WRITE COUNTER — every 3rd message (was 5; he asked to increase the
#      frequency the same day).
#
# WHY A HOOK AND NOT A RULE IN CLAUDE.md: a rule is something Claude has to
# remember to obey, and forgetting is the exact failure being fixed. A hook
# counts and prints whether anyone remembers or not.
#
# Never blocks and never fails the turn: prints to stdout, exits 0 regardless.
set -uo pipefail

DIR="${CLAUDE_PROJECT_DIR:-.}/.claude/hooks"
COUNT_FILE="$DIR/.prompt-count"
BRAIN="${CLAUDE_PROJECT_DIR:-.}/CLAUDE.md"
EVERY=3

# ---------- 1. READ GUARD — every single message ----------
cat <<'GUARD'
[brain] SEARCH BEFORE YOU ACT — there is a tool, it takes seconds:
    B=.claude/skills/session-continuity/scripts/brain
    $B find <topic>   $B money   $B closed   $B state   $B corrections
  REQUIRED before: spending credits · sending texts · building a lead list ·
  quoting any count · saying something is broken. History now lives in BRAIN.md (not auto-loaded);
  the tool searches it — it usually already has the answer — on 2026-09-02 not looking cost ~4,783 credits.
  Results are NEWEST FIRST; a later section overrides an earlier one.
  Counting? Grep the marker that NAMES the thing (VERIFIED_GOLD, a Status
  string, a tag) and count UNIQUE ADDRESSES, never rows. Never infer from a ZIP,
  a city name, a tab position or a row shape.

[sheet] ANY question about the ATT FIBER LEADS sheet -> LOAD THE `optimus-sheet`
  SKILL FIRST. It has the tab map, the 5 read paths in order, and the 4 tools
  that already exist on Patrick's PC. THE CLEAN RUNS ITSELF AT MAPS SCRAPER LAUNCH
  (since 2026-09-03). CLEAN_SHEET.bat is UNSAFE -- its whitelist deletes rep tabs.
  The unique gold count is `py gold_audit.py`. A whole tab is
  `py sheet_feed.py --tab "<name>"`. NEVER say the sheet cannot be read, counted
  or cleaned — say WHICH of the five paths you tried.
GUARD

N=0
[ -f "$COUNT_FILE" ] && N=$(cat "$COUNT_FILE" 2>/dev/null | tr -dc '0-9')
[ -z "$N" ] && N=0
N=$((N + 1))
echo "$N" > "$COUNT_FILE" 2>/dev/null || true

# ---------- 2. WRITE COUNTER ----------
SINCE=$((N % EVERY))
if [ "$SINCE" -ne 0 ]; then
  DUE=$((EVERY - SINCE))
  echo "[brain] message $N — brain write due in $DUE."
  exit 0
fi

STAMP=$(grep -m1 '^# CURRENT STATE' "$BRAIN" 2>/dev/null | sed 's/.*updated //')
UNPUSHED=$(cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null \
  && git log --oneline @{u}..HEAD 2>/dev/null | wc -l | tr -d ' ')
[ -z "$UNPUSHED" ] && UNPUSHED=0

cat <<BANNER

==============================================================
 BRAIN WRITE IS DUE — message $N (every $EVERY, Patrick's standing
 instruction; raised from 5 to $EVERY on 2026-09-02). Do it in
 THIS turn, not later.
==============================================================
 CURRENT STATE block last updated: ${STAMP:-UNKNOWN}
 Unpushed commits on this branch: $UNPUSHED

 Write down anything from the last $EVERY messages a future
 session would otherwise lose:
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
