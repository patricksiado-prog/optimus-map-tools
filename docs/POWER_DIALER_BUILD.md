# POWER DIALER BUILD — T-OPTIMUS

Build these six workflows by hand. Do NOT use the GHL AI builder for this — it
keeps producing "Add Note" steps because GHL has no "record disposition" action
and no "loop" action for it to reach for. Every action listed below is a real one
you pick from GHL's action list.

---

## THE IDEA IN ONE LINE

**Tags are the disposition, and tags are the loop.**

GHL's own Power Dialer disposition only saves when the rep clicks "Next call".
Stop mid-list, close the tab, take a break — it is gone. So we do not use it.
The rep's Claude writes a TAG instead. Tags save instantly, fire workflows, and
both Claude and I can read and write them.

## HOW THE REPEAT WORKS

There is no "loop" step in GHL. The cycle is made of tags:

    contact gets tag  queue-dial
            |
            v
    DIAL QUEUE workflow  ->  removes queue-dial, holds them for the dialer
            |
            v
    rep calls.  Rep says the outcome out loud.
    Rep's Claude writes  disp-no-answer
            |
            v
    DISP - No Answer  ->  wait 4h  ->  remove disp-no-answer  ->  ADD queue-dial
            |
            +-----------------> back to the top. That is the repeat.

Nobody re-enrolls anyone by hand. The tag does it.

**This only works if "Allow re-entry" is ON in every workflow.** With it off, the
second lap is silently skipped and you will think the whole thing is broken.

---

## STEP 1 — create the tags

Settings -> Tags -> add these eight:

    queue-dial
    disp-no-answer
    disp-voicemail
    disp-callback
    disp-interested
    disp-not-interested
    disp-dnc
    disp-sold

---

## STEP 2 — build DIAL QUEUE

New Workflow -> Start from Scratch -> **make sure the object is Contact**, not
Company. Name it `DIAL QUEUE`.

| Step | Action to pick | Setting |
|---|---|---|
| Trigger | Contact Tag | tag = `queue-dial` |
| 1 | Remove Contact Tag | `queue-dial` |
| 2 | Wait | 30 seconds |

Settings tab: **Allow re-entry ON**, **Stop on response ON**. Then **Publish**.

Removing the tag immediately is deliberate. It is what lets the same contact come
back round later instead of being blocked as "still enrolled".

---

## STEP 3 — build DISP - No Answer  (BUILD THIS ONE FIRST AND TEST IT)

This is the smallest thing that proves the repeat works.

| Step | Action to pick | Setting |
|---|---|---|
| Trigger | Contact Tag | tag = `disp-no-answer` |
| 1 | Wait | 4 hours |
| 2 | Remove Contact Tag | `disp-no-answer` |
| 3 | Add Contact Tag | `queue-dial` |

Settings: **Allow re-entry ON**. **Publish**.

### TEST IT NOW — 60 seconds

1. Pick any contact. Add the tag `disp-no-answer` by hand.
2. Open the workflow -> **Enrollment history** tab.
3. That contact should appear within a few seconds.

**If Enrollment history is empty, STOP.** The trigger did not take, and building
the other four will just multiply the problem. Common causes: workflow still in
Draft, wrong object type (Company instead of Contact), tag name typed
differently.

---

## STEP 4 — the remaining four

Same shape, different actions.

### DISP - Callback
| Step | Action | Setting |
|---|---|---|
| Trigger | Contact Tag | `disp-callback` |
| 1 | Create Task | "Scheduled callback", due in 1 day |
| 2 | Wait | 1 day |
| 3 | Remove Contact Tag | `disp-callback` |
| 4 | Add Contact Tag | `queue-dial` |

### DISP - Voicemail
| Step | Action | Setting |
|---|---|---|
| Trigger | Contact Tag | `disp-voicemail` |
| 1 | Wait | 1 day |
| 2 | Remove Contact Tag | `disp-voicemail` |
| 3 | Add Contact Tag | `queue-dial` |

### DISP - Interested   <- the one that makes money
| Step | Action | Setting |
|---|---|---|
| Trigger | Contact Tag | `disp-interested` |
| 1 | Assign to User | the closer |
| 2 | Create Task | "CALL BACK WITHIN 1 HOUR", due in 1 hour |
| 3 | Send Internal Notification | to your phone |
| 4 | Remove from all other workflows | — |

No wait step. No re-queue. Contact rates fall about 80% after five minutes and
the first person to call back wins roughly half the deals. We have had 22 people
say YES and close zero because nobody got back to them, and seven of those
blocked us while they waited. This workflow exists to stop that happening again.

### DISP - Not Interested  /  DISP - DNC
| Step | Action | Setting |
|---|---|---|
| Trigger | Contact Tag | `disp-not-interested` (and a second one for `disp-dnc`) |
| 1 | Add Contact Tag | `dnd` (DNC workflow only) |
| 2 | Remove from all workflows | — |
| 3 | End | — |

No re-queue. These never get dialled again.

---

## STEP 5 — turn the settings on for EVERY workflow

For all six: Settings tab -> **Allow re-entry ON** -> **Stop on response ON** ->
Save -> **Publish** (not Draft).

A workflow left in Draft enrols nobody and says nothing about it.

---

## STEP 6 — the one thing you need from me

The connector's GHL token does not include T-OPTIMUS. Every call returns:

    403 - The token does not have access to this location

To fix: **Settings -> Private Integrations** (or Integrations) -> open the token
the connector uses -> **edit the location list -> tick T-OPTIMUS Houston** ->
save. If it is agency-level you may need to reissue it with both sub-accounts
ticked.

Once that is done I can build and verify all six myself, create the tags, load
the 61 Beaumont contacts, and read dispositions back to tell you who replied and
was never called.

---

## HOW THE REP USES IT

They never touch a disposition dropdown. They finish the call and say the outcome
out loud. Their Claude writes the tag and the note:

> "not interested, moving in November"

-> `add_contact_tags: disp-not-interested`
-> `create_contact_note: "Moving Nov, revisit Q1"`

The tag fires the workflow. The workflow either re-queues them or stops them.
Nothing depends on the rep remembering to click anything.
