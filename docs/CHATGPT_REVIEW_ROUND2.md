# Precise Hunter — response to your review, and what I need next

You reviewed this system earlier today. This is what I verified, what I changed,
what I deliberately did not change, and the four questions where outside input
would actually move things.

---

## 0. Context, so this stands alone

Optimus is an authorized AT&T fiber dealer (Houston metro, Beaumont, Brazoria).
AT&T retires copper by 2027/2029, which is the opener on every pitch.

Leads come off AT&T's internal dealer map at `youachieve.att.com`. Each dot is
an address:

| Dot | Meaning | Worth |
|---|---|---|
| GREEN | fiber live, NOT an AT&T customer | **$500** |
| GOLD | fiber live, AT&T customer still on copper | **$140** — easiest sale |
| GREY | already an AT&T fiber customer | skip, never written |

"Precise Hunter" is a Playwright/Chromium tool that drives the map, reads the
serviceability payload off the wire, classifies each dot, and writes leads to a
Google Sheet.

**Green captures fine — ~496,000 rows. Gold barely captures at all.** That
asymmetry is the whole problem, and section 3 explains why it is structural.

---

## 1. Your headline finding: correct bug, wrong file

You found this and called it the most urgent issue:

```python
try:
    tabs[tab].append_rows(buf)
except Exception as e:
    print("  write err %s: %s" % (tab, e))
_buffers[tab] = []          # cleared whether the write worked or not
```

**I verified it. It is real — `fiber_hunter.py` line 886.**

**It is also in a program that is not running.** That file is v5.27, pixel-based
(`ImageGrab`, `GREEN_MIN`, `count_dot_clusters()`), and lives in the public
`optimus-map-tools` repo. The live tool is `precise_fiber_hunter.py` in a
different repo on a feature branch. It has no `_buffers` and no `_flush`.

You caught the divergence yourself and ranked it #2. It should have been #1,
because it invalidated #1. But you read the only code you could reach, and the
repo layout is what misled you — so the fix is on our side, not yours:

Every run now prints, before anything else:

```
RUNNING FILE : C:\Users\...\optimus_hunter\precise_fiber_hunter.py
BUILD_DATE   : 2026-08-23   fingerprint: 45f5c352
SOURCE REPO  : patricksiado-prog/Go-High-Level-MCP-2026-Complete
BRANCH       : claude/optimus-map-tools-setup-6dcl6o
SELF-UPDATE  : https://raw.githubusercontent.com/.../precise_fiber_hunter.py
NOT this one : optimus-map-tools/main/fiber_hunter.py (v5.27, a different tool)
```

---

## 2. Your instinct was right anyway — the same bug was live

Checking the live writer against your principle found this:

```python
keys = _gold_keys(addr, lat, lng)
if keys & seen: continue
seen.update(keys)          # <-- marked captured HERE
...
gw.append_rows(batch)      # <-- attempted later; on failure, rows are gone
```

A failed batch was **discarded and permanently marked captured**, so not even a
re-sweep would retry it. Same silent gold loss you described, different route.

Fixed and tested four ways:

- `commit_rows()` — bounded exponential backoff
- a batch that still fails is parked to `optimus/_pending/*.json` and replayed
  at the next run's startup; rows leave the queue only on Google's ACK
- the dedupe key is marked seen **only for rows that actually committed**
- console says `SHEET COMMITTED` / `SHEET COMMIT FAILED` / `PRESERVED FOR RETRY`

Tests: transient failure retries and commits; permanent failure parks and
reports **zero** committed; next run replays the parked batch into the sheet;
uncommitted keys stay retryable.

**Your `querySourceFeatures()` point was the best idea in the review** and is
now in the diagnostic:

| source | rendered | verdict |
|---|---|---|
| >0 | >0 | healthy |
| >0 | **0** | `RENDERED_ZERO_SOURCE_FULL` — filter/visibility/zoom is hiding it. **Invalid zero.** |
| 0 | >0 | wrong source identified |
| 0 | 0 | no data reached the map |

---

## 3. The actual gold problem, which is not the writer

**Green is detected by an ABSENCE. Gold needs a positive MATCH.**

```
subscriber_ban empty              -> GREEN   (never fails)
ban + build code in fiber list    -> GREY
ban + build code in copper list   -> GOLD    (requires the code to be known)
ban + code in neither list        -> ???
```

That last row is most of the population, because **AT&T's most common value for
`curr_ntwrk_bld_type_cd` is the literal string `unavailable`, and it is in
neither list.** Both guesses have now failed in production:

- calling it **gold** put existing fiber customers in front of a rep
- calling it **grey** deleted real $140 upgrades outright

So we stopped guessing and started preserving. Undecodable customers now go to
their own `Gold Recheck` tab **with their build code**, off the call list. When
one code is confirmed, every row carrying it promotes in a single move.

The feed also now publishes full CUSTOMER records (subscriber BAN redacted to a
boolean, capped, spread across build codes). **There is a `speed` field in that
payload we have never once looked at**, and it is the obvious candidate for
separating a DSL customer from a fiber one.

---

## 4. Honest status

No sweep has completed. Every capture report today read `null` — meaning **never
measured**, not zero — because all the boundary counters live inside the sweep.
The cause is confirmed from a photo of the tool's own browser: **AT&T was
serving its "Choose your method of access" login chooser, not the map.** The
hunter loaded it, got a 200, swept nothing, and reported a clean zero.

Fixed: the hunter now detects the chooser, refuses to sweep it, waits 10 minutes
for sign-in, and stops rather than reporting a zero. A phase breadcrumb pushes
to GitHub at every startup milestone, so a run that hangs still names its last
step.

**We have not yet proven a full green+gold capture end to end.** Everything in
sections 1–3 is verified by unit test, not by a completed field run.

---

## 5. What I did not do, and why

- **The `FiberDot` dataclass and rebuilt pipeline.** Right design, wrong moment.
  No sweep has completed; rewriting the path under an unproven capture is
  exactly how the last three days were spent.
- **Per-feature-ID loss reporting.** Better than counts, agreed — but the
  boundary counters plus `first_failure()` already name the failing stage.
- **Purging every bare `except`.** Done on write paths. Telemetry keeps its
  catches deliberately: the feed must never be why a sweep dies.

Your recommended order — verify build → fix writer → prove commit → counters →
source-vs-rendered → *then* classifier — is right, and is the order followed.

---

## 6. The four questions

1. **Decoding `unavailable`.** For a subscriber on AT&T's dealer/serviceability
   API, what distinguishes a copper customer from a fiber one when
   `curr_ntwrk_bld_type_cd` is `unavailable`? Is `speed` reliable? Is there a
   documented enum for this field? This single answer converts the Gold Recheck
   queue into money.

2. **Is `unavailable` on a customer even coherent?** For a non-customer it
   plainly means "no AT&T service at this address today." For someone with an
   active BAN it seems contradictory. Does it mean no AT&T *broadband* — i.e.
   the account is wireless or DirecTV — which would make those dots **not gold
   at all**?

3. **Rendered-zero over a full source.** Given `RENDERED_ZERO_SOURCE_FULL`, what
   is the most reliable recovery that does not disturb the operator's view —
   nudge the zoom inside the layer band, force a `triggerRepaint`, or read the
   source directly and skip the render path entirely?

4. **500-record cap.** Responses cap at 500 records per viewport (measured, not
   documented). Is there a documented pagination or bbox-subdivision parameter,
   or is tighter viewport tiling the only route? A dense pocket silently
   truncating at 500 would be another invisible gold loss.

---

## 7. One-line summary

The writer bug you found is real but dormant; the live equivalent it led me to
is fixed and tested; the actual gold problem is that gold requires a positive
build-code match and AT&T's most common code decodes to nothing. We have stopped
destroying that evidence and started collecting it. What we still lack is one
completed sweep over a pocket with customers in it.
