---
name: session-continuity
description: Keep continuity with Patrick across sessions so he never has to re-explain his business. Load at the START of every Optimus session, before answering anything — it says what to read, in what order, and how often to write findings back. Also use whenever he says you sound like a new chat, asks whether something was recorded, says "put that in the brain", corrects a fact you had wrong, or gives a decision that a future session would otherwise lose.
---

# Session continuity — don't make him repeat himself

Patrick, 2026-08-29: *"I kinda feel like I'm talking to a new chat or something."*

That is the failure this skill exists to prevent. Every session starts with zero
memory of the last one. `CLAUDE.md` is the only thing that carries over. If a
fact is not in it, it is gone — and he pays for that by explaining his own
business back to you.

## Read before you answer (60 seconds, every session)

1. **`CLAUDE.md`** — loads automatically. Actually read it, especially the
   dated sections at the bottom; those are the most recent decisions and they
   override older text higher up.
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
