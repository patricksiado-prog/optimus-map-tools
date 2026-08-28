# SCRAPER FIX — the business-to-dot cross-match has never written a row

**File:** `optimus/standalone/maps_scraper_standalone.py`
**Repo:** `patricksiado-prog/Go-High-Level-MCP-2026-Complete`, branch `claude/optimus-map-tools-setup-6dcl6o`
**Function:** `_match_new`, line 625
**Status:** written, compiled, reproduced and verified locally 2026-08-28. NOT DEPLOYED — `git push` and `add_repo` to the hunter repo are both classifier-blocked in this sandbox.

## The bug

`_safe_append` builds each row **7 wide**:

```python
new.append([r.get("name") or "", _a, _p,
            r.get("website") or "", r.get("category") or "",
            resi_hint(_a), cell_hint(_p)])
```

`_match_new` unpacks a fixed **5**:

```python
for name, addr, phone, web, cat in new:
```

That raises `ValueError: too many values to unpack (expected 5, got 7)` on the
**first row of every batch**, so the entire cross-match aborts every time. The
caller swallows it:

```python
try:
    _match_new(new)
except Exception as e:
    print("  (cross-match skipped: %s)" % str(e)[:50])
```

which is the `cross-match skipped: too many values to unpack (expected 5, got 7)`
line repeating down Ara's console on 2026-08-28.

**Effect:** the business-to-dot match — the join Patrick called *"most importan
thing"* — has produced **nothing** since the two hint columns were added.
`Upgrade Orange Biz` is stuck at 62 rows and `Fiber Green Biz` has not grown
from matching. It was never "not built". It was built and silently dying.

## The fix

Replace line 625:

```python
    for name, addr, phone, web, cat in new:
```

with:

```python
    for _row in new:
        # _safe_append builds 7-wide rows (…, resi_hint, cell_hint). Unpacking a
        # fixed 5 raised ValueError on the FIRST row, so every cross-match batch
        # aborted and the business-to-dot match never wrote anything. Slice, so
        # adding a column can never silently kill the match again.
        name, addr, phone, web, cat = _row[:5]
```

Slicing rather than unpacking means a future column addition can never kill the
match again — which is exactly how this happened.

## Verified

- Reproduced the exact `ValueError` against the real 7-wide row shape.
- Applied fix, `py_compile` clean.
- `diff` is one line replaced by six (five of them comment).
- Base file md5 `b9bf80084595a192e5e8f83b02b24f44` — matches the deployed HEAD,
  so the patch applies cleanly to what is live.

## Deploying it

`git push` to the hunter repo is blocked here, and the file is 78,946 bytes —
too large to retype through `create_or_update_file` without risking corruption
on a file that auto-deploys to every PC. So either:

1. Unblock the push permission for this session, or
2. Apply the six lines above by hand — it is one `for` statement.

Do not attempt to reproduce the whole file by hand. That is the mistake this
note exists to prevent.
