# Optimus Dialer 2 — why the call queue was dead

Workflow `9d3c7d0c-8f6f-44a9-93f9-d55d78e3b4a8` ("Optimus Dialer 2 — Zack Call
Queue"), published, version 21, 8 actions. Read live 2026-08-22.

## The bug

The first node a contact hits, at order 0, is an **Add Tag** action that applies
the tag `not interested`:

```
c2ac183a  Add Tag  ->  tags: ["not interested"]
   |
   v
65f5a6ff  if_else "yes"  ->  does the contact have the tag "not interested"?
   |                                    |
  yes                                  no (else)
   |                                    |
721a3060  Remove from Workflow    06ecb548  manual-call "Fiber Call" -> Zack
                                          |
                                  c7efa7f2  Wait 0.5 minutes
                                          |
                                  f3445773  Go to -> back to 65f5a6ff
```

Every contact is tagged `not interested` on entry, then immediately fails the
very condition meant to catch reps marking a rejection, and is removed from the
workflow. **The `manual-call` branch is unreachable.** Nobody was ever queued,
and everyone who entered came out wearing a rejection tag they never earned.

The condition itself is right — the rep tags `not interested` during the call
and the loop ejects them. The Add Tag node at the top is the mistake.

## Second problem, only visible once the first is fixed

The loop waits **0.5 minutes** before the `goto` sends the contact back to the
condition. Fix the entry bug alone and every untagged contact re-queues a call
task roughly every 30 seconds — about 2,880 tasks per contact per day straight
into Zack's queue. `dialer2_corrected_actions.json` sets that wait to **1 day** (Patrick's call, 2026-08-22).

## Scope note

`triggers` is `[]` — nothing enters this workflow on its own. Entry is manual
only (someone adding contacts, or `add_contact_to_workflow`). So this bug
explains an unknown share of the 331 contacts tagged `not interested`, not
necessarily all of them. Sizing that needs a tag-filtered contact query, which
the connector does not currently expose.

## Files

- `../backups/dialer2_9d3c7d0c_v21_BEFORE.json` — exact live state. Pass its
  `actions` array back through `ghl_update_workflow_actions` to restore v21.
- `dialer2_corrected_actions.json` — the 7-action replacement.

`ghl_update_workflow_actions` replaces the whole actions array and does save
reliably. (`triggers` on that same endpoint returns success and writes nothing —
triggers still have to be set in the UI.)

## Status

**Not applied.** Patrick's call 2026-08-22: leave Dialer 2 alone for now, keep the
corrected array staged. Loop cadence set to 1 day per his answer. Applying it is
one `ghl_update_workflow_actions` call with `dialer2_corrected_actions.json`.
