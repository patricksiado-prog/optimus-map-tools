---
name: session-continuity
description: Optimus memory — how to SEARCH the brain before you act, keep its CURRENT STATE block true, and never repeat an unverified claim to Patrick. The brain is 5,000+ lines and the failure is no longer forgetting, it is not looking. Trigger this skill BEFORE spending DealMachine credits, sending texts, building a lead list, quoting any count, or saying something is broken — and whenever Patrick says you sound like a new chat, asks to make the memory stronger, asks whether something was recorded, tells you to record or park something, corrects a fact you had wrong, kills an idea ("no", "don't do that", "stop suggesting"), or states a decision, constraint, price, promo or limit a future session would lose. Also trigger it before repeating any external fact you have told him before.
---

# Optimus memory

Two different failures, and the second one is the expensive one.

**Forgetting.** Patrick, 2026-08-29: *"I kinda feel like I'm talking to a new
chat or something."* Every session starts blank. `CLAUDE.md` is the only thing
that carries over.

**Not looking.** Patrick, 2026-09-02: *"u wasted credits on shit that doesn't
need to be enriched that is already recorded in the brain."* He was right. The
brain already said **"Grab from GHL before spending anything"** and already
listed the measured gold streets. Neither was found, because nobody knew the
word to grep for. ~4,783 DealMachine credits went to the wrong market.

**A 5,000-line file you read once at session start and never re-open is not
memory. It is an archive.** This skill exists to make it behave like memory.

## The shape, as of 2026-09-02 — know this before you go looking

`CLAUDE.md` used to be 5,250 lines / ~69,400 tokens, loaded IN FULL every
session. **Anthropic's guidance is under 200 lines**, because a long file costs
tokens on every turn and measurably reduces adherence to its own instructions.

| File | What is in it | Auto-loaded? |
|---|---|---|
| `CLAUDE.md` | CURRENT STATE, standing rules, dot legend, system IDs, CLOSED decisions | **yes, every session** (~11,700 tokens) |
| `BRAIN.md` | all dated session history — 4,445 lines moved there verbatim | **no** |
| `OPTIMUS_SESSION_LOG.md` | older session records | no |

**The `brain` tool searches all three.** That is what made the split safe:
retrieval is decoupled from auto-loading, so history costs nothing until it is
needed. **Never `@import` BRAIN.md into CLAUDE.md** — imported files load at
launch too, which would restore the entire cost.

**Routine maintenance, not a decision:** when `CLAUDE.md` drifts back over ~800
lines, move the oldest dated sections to the bottom of `BRAIN.md`. Verify by line
count that nothing was dropped, and never edit a section while moving it.

---

# 1. THE PROTOCOL — search before you act

There is a tool. Use it. It is at
`.claude/skills/session-continuity/scripts/brain` and it takes seconds.

```bash
B=.claude/skills/session-continuity/scripts/brain
$B find <topic...>    # search CLAUDE.md + BRAIN.md + the log, NEWEST FIRST
$B state              # the CURRENT STATE block — the only part claiming "now"
$B rules              # standing rules, each bought with a real mistake
$B closed             # decisions Patrick killed. Never re-propose these
$B corrections        # where the brain corrects itself. The correction wins
$B money              # read this before spending a single credit
$B stale [days]       # MEASURED claims going out of date — re-verify first
$B index              # every section with its date, newest first
```

**These four actions REQUIRE a search first. No exceptions.**

| Before you… | Run | Because |
|---|---|---|
| **spend credits / enrich / export** | `$B money` and `$B find <market>` | 4,783 credits went on ground the brain had already mapped |
| **send texts / build a send list** | `$B find texting` and `$B find <pocket>` | copy rules, quiet hours, the live number list, who already opted out |
| **quote a count or a colour** | `$B find <the thing>` | four separate counts have been wrong by inference |
| **say something is broken/fixed** | `$B find <component>` | the answer is usually already measured, with a date |

**And when the search comes back empty, that is a real answer.** It means the
thing is genuinely new — so measure it, and then write it down.

## Reading what comes back

**Results are newest-first and stamped with the date of their section. A later
section overrides an earlier one.** The brain is append-only and chronological,
so position is truth. If two entries disagree, the one nearer the top of the
output is current — say so out loud rather than silently picking one.

`$B corrections` exists because the file corrects itself often. A corrected
claim still sits in the file above its correction; quoting it is the single
easiest way to tell Patrick something he has already told you is wrong.

## Counting anything

The bug that keeps recurring is **assigning a value by the shape of the data
instead of measuring it**: gold-by-default (8/23), colour-by-default (8/29),
agent-by-first-match (9/01), city-name-as-colour (9/02). Nothing ever errors —
the count just comes back looking fine.

- **Grep the marker that NAMES the thing** — `VERIFIED_GOLD`, a Status string,
  a tag. Never a ZIP, a city name, a tab position or a row shape.
- **Count UNIQUE ADDRESSES, never rows.** The sheet holds one row per sighting;
  170 gold rows turned out to be 4 dots.
- **Say which it is.** "170 rows / 4 unique addresses" is an answer. "170 gold"
  is a guess wearing a number.

---

# 2. The layers, and why there are four

Worth knowing so nobody "simplifies" it later:

1. **The SessionStart hook** (`.claude/hooks/session-start.sh`) fires every
   session with no decision involved and prints live state. **The only layer
   that cannot be forgotten** — a skill only loads when Claude reaches for it,
   and the sessions that need it most open with a plain question and never do.
2. **The read guard** (`.claude/hooks/brain-write-counter.sh`) prints on EVERY
   message: grep the brain before spending, sending or asserting. Added
   2026-09-02, for the reason above.
3. **The write counter**, same hook, **every 3rd message** (raised from 5 by
   Patrick on 2026-09-02).
4. **This skill and the `brain` tool** — the discipline and the machinery.

If continuity is failing, check them in that order. A hook that stopped firing
looks exactly like a model that stopped caring.

---

# 3. The CURRENT STATE block is the memory — keep it true

`CLAUDE.md` opens with a **CURRENT STATE** block. It is the only part of the
file that claims to be true *now*. Everything below is a 5,000-line
chronological record.

- **Read it first, before answering anything** (`$B state`).
- **Update it in the SAME TURN any line in it changes** — a routine enabled, a
  blocker cleared, a new measurement, a decision closed. Then push.

Keep it short; if a line needs more than two sentences, put the detail in a
dated section and point at it. When something stops being true, **change it
there** — do not leave the old line standing with a new one below it. Two
confident contradictory lines is the failure this block exists to end.

**CLOSED items are load-bearing.** When he kills something it goes in the CLOSED
table with his own words and the date, and no future session raises it again.

---

# 4. Open with state, not questions

The tell that you did not read is a question he has already answered. The tell
that you did is opening with a number he did not have to ask for.

Know these four before the first reply and lead with whichever he touched:
**is the scanner writing** (workbook `modifiedTime` AND `fileSize` — a flat size
means nothing is landing, whatever the console says), **what came back
overnight**, **what is blocked on him**, **what the last session shipped**.

---

# 5. Write while you work, not at the end

The old habit was one big brain-dump at the end of a session. Sessions get cut
off, and everything unwritten dies with them. Write in small pieces as you go.

**Append to `CLAUDE.md` and push the moment any of these happen:**

- He makes a **decision** ("6 attempts", "don't break that template", "start
  texting tomorrow") — record it with the date and his own words.
- He **corrects you.** Record the correction AND what you had wrong, so the next
  session doesn't repeat the mistake. His corrections are the highest-value
  content in the file.
- You **measure something** — a count, a rate, a live read. Record the number,
  the date, and how you got it so it can be re-measured.
- You **discover a limit** — a tool that 404s, a blocked domain, a permission
  denied. That saves the next session a wasted turn.
- Something **ships** — a routine created or changed, a deploy, an email sent to
  the team, a file handed over.
- A **person, number, ID or account detail** turns up.

Commit message says what changed. Push every time — an unpushed commit is not
memory, it is a local file in a container that gets reclaimed.

# 6. The rot problem — an unverified claim is worse than a forgotten one

Patrick, 2026-08-30: *"u keep saying 20 million cell google thing but why isn't
that an option?"* He was right. A recommendation went into the brain once on
2026-08-26, was never checked, and got read back out as fact in four separate
sessions — each repetition making it sound better established. When it was
finally verified it turned out to be **allowlisted per domain by a Workspace
admin**, and the sheet is on a personal Gmail account, so it was never
available at all.

**That is what "you don't feel like you're remembering" actually means.** Not
gaps — confidently repeating something nobody ever checked. A forgotten fact
gets looked up again. A confidently wrong one never does.

Three rules, and they are the point of this skill as much as the write cadence:

**1. Mark every claim MEASURED or ASSUMED, and date it.**
A measured claim carries the number, the date, and how it was measured, so the
next session can re-measure it. An assumed one says so out loud. Right now the
brain writes both in the same confident voice, which is exactly why an
unchecked recommendation reads like a verified count.

**2. Re-verify before repeating.**
Any external fact — a price, a promo, a product limit, a vendor policy, an API
capability — gets re-checked before it goes to Patrick a *second* time. Promos
move monthly. Betas close. Limits change. If it cannot be checked this turn,
say "unverified" in the same sentence rather than restating it clean.

**3. Every recommendation names WHO can do it.**
"Fill out the form" survived four sessions because nobody asked who was
eligible to fill it out. A recommendation without an actor is a wish, and a
parked item with no owner is where wishes go to look like plans. Name the
person: Patrick, Churchie, Christian, a Workspace admin, or us.

**When Patrick pushes back on something you have said before, treat that as a
signal the claim was never verified** — check it before defending it. He is
usually pushing because it has not moved, and things that do not move are
usually things nobody could actually do.

## 6b. THE FIX FOR CODE-CLAIM ROT: `brain-verify` (added 2026-09-03)

Numbers in the brain rot slowly, because a number carries a date and a method
and gets re-measured. **Claims about CODE rot silently**, because nobody greps
them again. On 2026-09-03 four of them were found wrong at once -- "the purge
runs at hunter launch", "the cross-match fix is NOT deployed", "git push to the
hunter is blocked", "the match reads orange from Precise Fiber" -- and each had
sent Patrick after the wrong fix.

**The common tactic: test the documentation like code.**

```
.claude/skills/session-continuity/scripts/brain-verify
```

runs at EVERY session start (wired into `session-start.sh`). It fetches the live
hunter, scraper and clean_sheet files plus `tabs.json` from GitHub and checks
every claim in its manifest: `pass` / `*** DRIFT` / `UNVERIFIED`. It also says
whether the sheet clean has run (junk tabs still present or not) and whether any
protected tab has vanished. ~1.5 seconds.

**The three rules that make it work forever:**

1. **A code claim that is not in the manifest is ASSUMED**, no matter how
   confidently CLAUDE.md states it. If you are about to tell Patrick where some
   code lives or what it does, and there is no line for it, add one first.
2. **When you deploy a change, add its claim in the SAME commit.** That is how
   the manifest stays the truth instead of another stale document.
3. **A DRIFT line is fixed in the first turn of the session**, in CLAUDE.md and
   in the manifest. Never delete a line to silence it.

`UNVERIFIED` means the file could not be fetched. It is "I could not look", not
"it is fine". Say so if the answer depends on it.

# 7. What to write, and what not to

**Write facts, findings, decisions and numbers.**

**Do not invent rules.** Patrick, 2026-08-29: *"nothing that going to create
extra dumb rules for me but info."* And from the older brain: *"Don't add hard
rules to the brain that he then has to deprogram."* A rule he did not ask for
becomes something he has to argue with later. If he said it, record it as his
decision with his wording. If you merely think it is a good idea, it is a
recommendation in chat, not a line in the brain.

**Never put customer PII in the repo** — names, phone numbers, account numbers.
It is pushed to GitHub. Record the source ID and the method instead so the work
can be reproduced.

**Keep it tight.** A section someone has to skim past forever is a cost. Date
every section. When something is superseded, say so in the old section rather
than leaving two contradictory versions.

# 8. Sounding like you were here yesterday

- **Never re-ask what the brain already answers.** Who Dave is, what a gold dot
  is worth, which sheet is the master, what the dot legend means. Asking those
  is the tell that you did not read.
- **Reference the history when it is relevant** — "this is the same failure as
  the `free_space.py` MIN_COLS one" lands very differently from asking him to
  re-explain.
- **Open with state, not questions.** If he asks whether something went out,
  check it and tell him the number. Do not ask him what he means.
- **Carry his day forward.** He logs food, training, meetings and wins in chat,
  not in a sheet. Anything he mentions is that day's log — put it in the brain
  the same turn so the next brief has it.
- **When you do not know, say so and go look**, rather than asking him to fill
  the gap.

# 9. Before the session ends

If the conversation is winding down or context is running out, do a final pass:
anything decided, measured, corrected or shipped this session that is not yet in
`CLAUDE.md` goes in now, then push. Then say in one line what you recorded, so
he can see the memory was actually saved.
