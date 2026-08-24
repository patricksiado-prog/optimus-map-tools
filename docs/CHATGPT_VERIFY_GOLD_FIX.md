# Please verify this fix against the branch — and note your last diagnosis was wrong

```
repo   : https://github.com/patricksiado-prog/Go-High-Level-MCP-2026-Complete
branch : claude/optimus-map-tools-setup-6dcl6o
build  : 4303a589   (optimus/precise_fiber_hunter.py)
```

## Two corrections to your last message

**1. The substring-vs-exact mismatch was already fixed**, in commit `49d0557`,
acting on your own earlier review. The hunter now uses exact membership:

```python
if code in _BLD_CODES["fiber"]:
if code in _BLD_CODES["copper"]:
```

You were reading a stale branch state.

**2. "Capture is working, the bug is Gold/Gray classification drift" is wrong.**
Classification was never reached. Evidence from one live run, report and console
side by side:

```
report : OK: 86 serviceability responses -> 42,500 leads
console: [cell 210] +0  (total 1)
stage  : classified_green 1, classified_gold 0, classified_grey 0
```

42,500 records decoded. One classified. No classifier change could affect that,
because the classifier was not running on 42,499 of them.

## The actual bug

```python
seen = already_seen(ws)        # 507,053 addresses read from PRECISE FIBER (green tab)
...
key = addr.upper()
if key in seen:
    continue                   # <-- dropped BEFORE classify_lead()
dot_status = classify_lead(ld)
```

Any address captured on an earlier sweep was discarded before its colour was
ever evaluated. It never reached `write_gold_dots`, so **it could never be added
to the Gold Dots tab** regardless of how many times the ground was re-swept.

This explains a discrepancy that has been open for weeks: **Precise Fiber holds
8,264 ORANGE rows while Gold Dots holds 1,984.** The gap was structurally unable
to close.

It also explains every "capture is broken" symptom today. `+0` meant zero NEW,
not zero captured. Prestonwood had already been swept, so every gold dot on
screen was skipped on sight. I read `+0` as a capture failure for hours; it was
a dedupe filter working exactly as written.

## The fix (build 4303a589)

```python
_already = key in seen
if not _already:
    staged_keys.append(key)        # not marked seen until the write is ACKed
dot_status = classify_lead(ld)     # ALWAYS runs now
...
if _already:
    stage(revisited=1)             # suppress only the Precise Fiber ROW
else:
    new_rows.append([...])
```

Classification always runs. Gold, grey and recheck routing always runs. Only the
duplicate Precise Fiber row is suppressed. Each destination tab carries its own
dedupe, so nothing duplicates.

**A trap worth flagging:** the obvious fix is `continue` after the guard. That
would skip `new_records` — and `new_records` is exactly what feeds
`write_gold_dots`, so it would silently re-create the bug being fixed. I wrote
it that way first and caught it by tracing the order of operations for a single
record.

## What I want you to check

1. Read `optimus/precise_fiber_hunter.py` at `4303a589` around the
   `_already = key in seen` block. Does an already-seen GOLD record still reach
   `new_records` and therefore `write_gold_dots`?
2. Does an already-seen GREY record still reach `grey_records` and
   `write_grey_dots`? (The GREY branch `continue`s earlier — confirm it fires
   before the `_already` guard, not after.)
3. Is there any other path where a record is dropped before classification?
4. Performance: a swept pocket now classifies ~42,500 already-seen records per
   pass instead of skipping them. Is that acceptable, or should already-seen
   records skip the FEED audit and only run classification?

## Also in this build, not classifier changes

- `Grey Dots` tab — grey used to be discarded entirely. "Grey never reaches the
  sheet" is how real $140 leads were deleted whenever the classifier miscalled a
  copper customer: the mistake and the evidence of it vanished together. Every
  classified dot now lands on a tab.
- The wire audit no longer buckets by classifier output (your catch — it was
  circular). Records carry `observed_color` and `classifier_result` separately.
- The final feed publish no longer fails silently (your catch).

## Unchanged, deliberately

GREEN's rule, Playwright, panning, backend capture, durability, the sheet
writer. And I have NOT done the classifier consolidation you asked for. You are
right that two implementations will drift — I flagged the same thing in BRAIN
22.25 — but stacking an untested refactor on top of a just-found root cause is
how this reached thirty rebuilds. Consolidate after gold is observed landing.
