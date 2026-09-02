# Make ONE double-click delete the extra tabs AND the junk gold rows — safely

MEASURED + written 2026-09-03. **NOT pushed — RULE 0.**

Patrick: *"get rid of it extra tabs and the junk data please"*, and before that
*"do it don't make me work u do it."* So this has to be one action, and it has
to be safe enough to run without reading a dry run line by line.

Today it is neither. It is two actions in two different programs, and the first
one deletes leads.

## Problem 1 — CLEAN_SHEET.bat as it stands deletes Patrick's working tabs

`clean_sheet.py` is a **whitelist**: anything not on `KEEP` / `KEEP_SUBSTR` is
deleted (CSV-backed-up first). Run against the 29 live tabs it removes 14 tabs /
22,457 rows, and **7 of them are hand-built working lists, not junk**:

| Tab | Rows | Verdict |
|---|---|---|
| `Warm Backlog — Replied YES` | 40 | **KEEP — people who already said YES.** The single highest-value tab in the book |
| `Angleton Call List — Aug 2026` | 20 | **KEEP** — rep call list |
| `WORK LIST — Beaumont + Angleton` | 29 | **KEEP** — rep work list |
| `Beaumont Gold — Aug 2026` | 238 | **KEEP** — market slice |
| `GOLD — CLEAN` | 3,328 | **KEEP** — the cleaned copy of the retired tab |
| `HOUSTON UNVERIFIED — Aug 19` | 1,339 | **KEEP** — unverified, not junk |
| `Operator Scorecard` | 12 | **KEEP** — who scanned what |
| `Gold Dots` | 3,328 | delete — RETIRED, contaminated, `GOLD — CLEAN` supersedes it |
| `TEST-Green-2026-08-24` | 13,027 | delete — frozen snapshot |
| `TEST-Gold-2026-08-24` | 5 | delete AFTER migrating into `Gold Confirmed` |
| `TMP Sweep Census` | 92 | delete — temp |
| `ZZ_TMP_GRID` | 999 | delete — temp |
| ` _temp_ash_lookup` | 0 | delete — temp |
| `_optimus_probe` | 0 | delete — write probe |

A whitelist is the wrong shape for this workbook. Reps and one-off scripts
create tabs constantly, and a whitelist deletes everything nobody thought to
list — which is exactly backwards. **Every new tab should survive by default;
only named junk should go.**

### Fix 1 — invert it to an explicit junk list

Replace `_keep()` with `_is_junk()`. Nothing is deleted unless it matches:

```python
# Junk, by name. A tab NOT on this list is KEPT -- reps and one-off scripts
# make tabs all the time, and a whitelist deletes the ones nobody thought to
# add. Wrong way round on a sheet people work in. Named junk only.
JUNK = {
    "gold dots",              # RETIRED, gold-by-default contamination
                              # ('GOLD - CLEAN' is the cleaned copy -- keep that)
    "tmp sweep census",
    "zz_tmp_grid",
    "_temp_ash_lookup",
    "_optimus_probe",         # write-access probe, transient by design
    "at&t test",
}
JUNK_PREFIX = ("test-", "debug", "_tmp", "tmp_", "zz_", "copy of ")

def _is_junk(title):
    low = title.strip().lower()
    return low in JUNK or low.startswith(JUNK_PREFIX)
```

Everything else stays. `TEST-Gold-*` still migrates into `Gold Confirmed` before
its tab is dropped, exactly as today.

## Problem 2 — the row purge is in a different program, and it is gated shut

The 9,052 pre-2026-08-24 gold-by-default rows are 79% of `Gold Confirmed`. The
only code that removes them is `purge_prefix_gold()` in
`maps_scraper_standalone.py`, which never runs — see
`patches/gold-purge-never-runs.md`. `clean_sheet.py` dedupes by address and has
no date cut at all, so the junk rows are unique addresses and survive it
untouched.

### Fix 2 — put the date purge inside clean_sheet.py

`clean_sheet.py` opens tabs by name and never calls `add_worksheet`, so it does
NOT hit the full-workbook gate that stops the scraper's copy. Same logic, same
backups, new home — and then ONE double-click does the whole job.

```python
GOLD_CUTOFF = "2026-08-24"   # gold-by-default died 2026-08-23 (BRAIN 22.17);
                             # confirmed-copper capture verified 2026-08-24

def purge_prefix_gold(sh, dry, bdir, log=print):
    """Remove rows from 'Gold Confirmed' captured before GOLD_CUTOFF -- the era
    when an undecodable build code was labelled GOLD by default. Backs the whole
    tab up first, then writes the survivors and trims. Aborts touching nothing
    if the 'Captured At' header is missing."""
    try:
        ws = sh.worksheet(GOLD_TAB)
        rows = ws.get_all_values()
    except Exception as e:
        log("  gold purge SKIPPED -- cannot read '%s': %s" % (GOLD_TAB, str(e)[:60]))
        return 0
    if len(rows) < 2:
        log("  gold purge SKIPPED -- '%s' read as %d rows. NOT marking done; "
            "an empty read is a failed read, not a clean tab." % (GOLD_TAB, len(rows)))
        return 0
    hdr = [h.strip().lower() for h in rows[0]]
    if "captured at" not in hdr:
        log("  gold purge ABORTED -- no 'Captured At' column. Nothing touched.")
        return 0
    ci = hdr.index("captured at")
    # A date guard, not a plain string compare: "not a date" sorts above
    # "2026-08-24" as a string and would survive the cut.
    import re
    datelike = re.compile(r"^\d{4}-\d{2}-\d{2}")
    keep, remove = [rows[0]], []
    for r in rows[1:]:
        v = (r[ci] if ci < len(r) else "").strip()
        m = datelike.match(v)
        (remove if (m and v[:10] < GOLD_CUTOFF) else keep).append(r)
    if not remove:
        log("  gold purge: nothing to remove -- all %d rows are post-%s."
            % (len(rows) - 1, GOLD_CUTOFF))
        return 0
    log("  GOLD PURGE: '%s' has %d rows; %d captured before %s (gold-by-default "
        "era) -> removing. %d confirmed gold kept."
        % (GOLD_TAB, len(rows) - 1, len(remove), GOLD_CUTOFF, len(keep) - 1))
    if dry:
        log("  (dry run -- nothing written)")
        return len(remove)
    _backup(ws, bdir)                       # whole tab to CSV before touching it
    import io, json, os, time
    with io.open(os.path.join(bdir, "gold_purged_%s.json" % time.strftime("%Y%m%d-%H%M%S")),
                 "w", encoding="utf-8") as f:
        f.write(json.dumps(remove, ensure_ascii=False))
    ws.update("A1", keep, value_input_option="RAW")
    if len(rows) > len(keep):
        ws.delete_rows(len(keep) + 1, len(rows))
    log("  GOLD PURGE DONE: kept %d, removed %d." % (len(keep) - 1, len(remove)))
    return len(remove)
```

Call it in `main()` right after the `TEST-Gold-*` migration and before the tab
deletions, so migrated rows are date-checked too. It respects `--yes` /dry-run
like every other step.

## What one double-click then does

`CLEAN_SHEET.bat` -> dry run -> type YES:

1. migrate `TEST-Gold-2026-08-24` (5 rows) into `Gold Confirmed`
2. **purge 9,052 pre-08-24 rows from `Gold Confirmed`** (backup + JSON first)
3. dedupe `Gold Confirmed` and `Precise Fiber` by address
4. delete **7 junk tabs / 17,451 rows**, each CSV-backed-up:
   `Gold Dots`, `TEST-Green-2026-08-24`, `TEST-Gold-2026-08-24`,
   `TMP Sweep Census`, `ZZ_TMP_GRID`, ` _temp_ash_lookup`, `_optimus_probe`
5. **keeps** every rep tab, every campaign, and `Warm Backlog — Replied YES`

Frees roughly 300,000+ cells against the 10M ceiling (tabs bill for their whole
grid, not their rows), which is also what unsticks the workbook's refused writes.

## Not pushed

`clean_sheet.py` is in `_CORE_FILES`. A push is a deploy to every PC. Needs
Patrick's go.
