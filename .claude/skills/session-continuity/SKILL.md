---
name: session-continuity
description: Optimus memory discipline — how to read the brain, keep its CURRENT STATE block true, and never repeat an unverified claim to Patrick. Use this skill aggressively, not just when memory is named. Trigger it whenever Patrick says you sound like a new chat, that you are not remembering, asks to improve or strengthen the memory or the brain, asks whether something was recorded or "did you put that in the brain", tells you to record or park something, corrects a fact you had wrong, kills an idea ("no", "that's not an option", "don't do that", "stop suggesting"), or states a decision, constraint, price, promo or limit that a future session would otherwise lose. Also trigger it before you repeat any external fact you told him before — a promo, a price, a product limit, a vendor policy — because repeating something unchecked is the failure this skill exists to prevent.
---

# Session continuity — don't make him repeat himself

Patrick, 2026-08-29: *"I kinda feel like I'm talking to a new chat or something."*

That is the failure this skill exists to prevent. Every session starts with zero
memory of the last one. `CLAUDE.md` is the only thing that carries over. If a
fact is not in it, it is gone — and he pays for that by explaining his own
business back to you.

## Three layers, because a skill alone cannot do this job

Worth knowing why the machinery is shaped the way it is, so nobody
"simplifies" it later:

1. **The SessionStart hook** (`.claude/hooks/session-start.sh`, registered in
   `.claude/settings.json`) fires on every single session with no decision
   involved. It prints live state — how old the CURRENT STATE block is, what
   the scanner heartbeat says, what the last session shipped. **This is the
   only layer that cannot be forgotten**, which is precisely why it exists: a
   skill only loads when Claude decides to consult it, and the sessions that
   need this most are the ones that open with a plain question like "is the
   software working" and never think to reach for a skill.
2. **The CURRENT STATE block** at the top of `CLAUDE.md` is the answer sheet.
3. **This skill** is the discipline for keeping the block true.

If continuity is failing, check the layers in that order. A hook that stopped
firing looks exactly like a model that stopped caring.

## Open every session by telling him state, not by asking him anything

The tell that you did not read is a question he has already answered. The tell
that you did is opening with a number he did not have to ask for.

Before the first reply of a session, know these four and lead with whichever he
touched: **is the scanner writing** (workbook `modifiedTime` AND `fileSize` —
a size that has not moved means nothing is landing, whatever the console says),
**what came back overnight** (replies and opt-outs in GHL, none of them called),
**what is blocked on him**, and **what the last session shipped** (`git log`).

## The CURRENT STATE block is the memory — keep it true

`CLAUDE.md` opens with a **CURRENT STATE** block (added 2026-08-30). It is the
only part of the file that claims to be true *now*: is the scanner writing,
what is live and sending, what is blocked on Patrick, what is measured-broken,
and what is CLOSED and must never be re-proposed.

Everything below it is a 3,000-line chronological log — a record, not a state.
That log is why answers used to come out stale: "is the scanner working" was
spread across six sections written on four days, some superseded, all sounding
equally confident.

**Two obligations, and they are the whole point:**

- **Read the state block first, before answering anything.**
- **Update it in the SAME TURN any line in it changes** — a routine enabled or
  disabled, a blocker cleared, a new measurement, a decision closed. Then push.
  A finding appended 2,000 lines down that never reaches the state block is a
  finding nobody will read.

Keep it short. If a line needs more than two sentences, put the detail in a
dated section at the bottom and point at it from the block. When something in
the block stops being true, change it there — do not leave the old line
standing and add a new one below it. Two confident contradictory lines is the
failure this block exists to end.

**CLOSED items are load-bearing.** Patrick hates re-litigating decisions. When
he kills something, it goes in the CLOSED table with his own words and the
date, and no future session raises it again.

## Read before you answer (60 seconds, every session)

1. **`CLAUDE.md`** — loads automatically. **CURRENT STATE block first**, then
   the dated sections at the bottom; those are the most recent findings and
   they override older text higher up.
2. **The bottom 200 lines specifically.** Newest findings live there. Old
   sections above are frequently superseded and not always struck through.
3. **`BRAIN.md`** only when you need depth on the hunter, the classifier or a
   past session.
4. **`git log --oneline -20`** — what the last session actually changed.

**If two parts of the brain disagree, the later-dated one wins.** Say so out
loud rather than silently picking one.

## Write while you work, not at the end

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

## The rot problem — an unverified claim is worse than a forgotten one

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

## What to write, and what not to

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

## Sounding like you were here yesterday

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

## Before the session ends

If the conversation is winding down or context is running out, do a final pass:
anything decided, measured, corrected or shipped this session that is not yet in
`CLAUDE.md` goes in now, then push. Then say in one line what you recorded, so
he can see the memory was actually saved.
