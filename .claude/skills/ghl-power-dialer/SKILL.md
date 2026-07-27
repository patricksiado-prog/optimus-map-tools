---
name: ghl-power-dialer
description: >-
  Build, load, and troubleshoot a GoHighLevel (GHL/LeadConnector) Manual-Call
  Power Dialer queue via the command_connector MCP. Use whenever the task
  involves the GHL dialer, manual-call workflows, recycling/redialing a lead
  list, "Manual Actions" showing empty, enrolling contacts into a call queue,
  or dispositions. Encodes verified API quirks so the 3-day setup mistakes are
  never repeated.
---

# GHL Power Dialer — Working Playbook

Location ID for this account: `xZj500PjsflIQg2j9f9D`
Reps (userId → name): `qOa2OVzPabolfU9xjVXM` = **Zack Woodring** (zack@fiberforcesales.com).

## The one mental model that matters

GHL's "Power Dialer" **is** the **Conversations → Manual Actions** screen. Leads
appear there only when a contact is **enrolled in a workflow whose first action
is a `manual-call` step** AND that step has a **valid assignee**. Three separate
things must all be true, or the screen shows *"Good Work! You have no pending
tasks"*:

1. Contact is **tagged/exists** and **assigned to a rep** (`assignedTo`).
2. Contact is **enrolled** in the dialer workflow (`add_contact_to_workflow`).
3. The workflow's `manual-call` action has a non-empty **`assignTo`** in its
   `attributes`.

**Tagging ≠ enrolling.** A contact can be tagged and assigned and still never
appear in the queue until it is enrolled. This was the root of the multi-day
"dialer is empty" problem.

## THE bug that ate 3 days: empty `assignTo`

`manual-call` actions built through `ghl_update_workflow_actions` come out with
`"attributes": {}`. An empty assignee makes GHL create the call task
**Unassigned**, so it is invisible when the Manual Actions screen is filtered to
a specific rep. **Fix: always set `assignTo` to the rep's userId.**

Working action array for a recycling dialer (call → wait 2 days → loop back):

```json
[
  {
    "type": "manual-call",
    "name": "Fiber Call",
    "id": "480aee65-f027-44ac-a667-c982b450c6e8",
    "order": 0,
    "attributes": { "assignTo": "qOa2OVzPabolfU9xjVXM" },
    "next": ["c1d2e3f4-0002-4002-8002-000000000002"]
  },
  {
    "type": "wait",
    "name": "Wait 2 days before re-dial",
    "id": "c1d2e3f4-0002-4002-8002-000000000002",
    "order": 1,
    "parentKey": "480aee65-f027-44ac-a667-c982b450c6e8",
    "attributes": { "value": 2, "unit": "days" },
    "next": ["480aee65-f027-44ac-a667-c982b450c6e8"]
  }
]
```

After editing an action, contacts already enrolled ran through the OLD step —
**remove and re-add them** (`remove_contact_from_workflow` then
`add_contact_to_workflow`) so they hit the corrected action.

Always **re-GET** the workflow (`ghl_get_workflow_full`) after an update to
confirm `attributes` and `next`/`parentKey` (the loop) survived.

## The recycle loop (how it redials)

A `manual-call` step only advances **when the rep deletes/completes the task**
in Manual Actions after calling. Then: `Wait 2 days → back to Manual Call → the
same lead reappears`. That loop-back `next` pointer IS the recycle. No native
disposition branching exists inside `manual-call` (still an open GHL feature
request), so dispositions are handled by the rep:

- **No / not interested** → mark contact **DND** and `remove_contact_from_workflow`.
- **Yes / sold** → move to pipeline (opportunity) and remove from workflow.
- **No answer / busy** → just complete the task; it auto-recycles in 2 days.

## Loading the full list (enrollment at scale)

- The workflow to enroll into for Zack: **"Optimus Dialer 2 — Zack Call Queue"**
  = `9d3c7d0c-8f6f-44a9-93f9-d55d78e3b4a8`.
- Tag for the fiber-biz lead set: **`optimus-fiber-biz`** (~2,525 unique
  callable contacts, all assigned to Zack).
- Get contact IDs with **`official_contacts_get_contacts`** — it filters by
  `query=optimus-fiber-biz` AND paginates via `startAfter` + `startAfterId`
  (100/page; read `data.meta.startAfter/startAfterId/nextPage`). Large responses
  are auto-saved to a file — use `jq -r '.data.contacts[].id'` to extract IDs.
- Enroll with **`add_contact_to_workflow`** (single contact only; no bulk API).
  Returns `{"succeeded": true}`. There is no bulk "add to workflow" endpoint.
- **Fastest path if a human is available:** desktop app.gohighlevel.com →
  Contacts → filter Tag = `optimus-fiber-biz` → Select All → Bulk Actions → Add
  To Workflow → the dialer workflow. Three clicks enrolls all of them; the UI
  runs the workflow properly.

## Verified API limits (do not fight these)

- **Manual Actions are invisible to the API.** `get_contact_tasks` /
  `search_location_tasks` return `[]` for enrolled contacts — Manual Actions are
  NOT Tasks. You **cannot self-verify** the queue populated; a human must look at
  Conversations → Manual Actions. Prefer the **desktop** web app for checking;
  the mobile app's Manual Action screen is unreliable.
- **Workflow triggers are UI-only.** `ghl_update_workflow_actions` accepts a
  `triggers` array but silently drops it (re-GET shows `triggers: []`). Cannot
  auto-enroll by tag-added trigger via API — enroll explicitly instead.
- `ghl_get_workflow_executions` → 404 (endpoint absent). No execution-log read.
- `search_contacts` → `limit` max **500**, and no pagination cursor. Use
  `official_contacts_get_contacts` when you need to walk >500 or the whole set.
- `create_smart_list` → 404 (smart lists are UI-only).
- `get_users` → 422 ("companyId must be a string"). Use `get_user` by userId, or
  `official_users_get_user_by_location` (can time out; retry).
- The underlying Railway MCP host is **blocked by egress policy** — you cannot
  curl the GHL API directly; everything must go through the command_connector
  MCP tools, one call at a time.

## Fast triage when "the dialer is empty"

1. `ghl_get_workflow_full` on the dialer workflow → confirm the `manual-call`
   action has `attributes.assignTo` set to the rep. If `{}` → that's the bug; fix
   it (see above), then remove+re-add enrolled contacts.
2. Confirm target contacts are `assignedTo` that same rep (`get_contact`).
3. Confirm they are actually enrolled (you enrolled them this session, or bulk
   UI add). Tagging alone is not enrollment.
4. Have a human check **desktop** Conversations → Manual Actions, staff = rep.
5. If still empty on desktop with assignTo set and contacts enrolled → it is a
   genuine platform limit on API-created call steps; rebuild the `manual-call`
   action in the desktop workflow UI, or dial from a Contacts smart list.
