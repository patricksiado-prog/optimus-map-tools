# The launcher has refused every hunter update since 2026-08-25 — found 2026-09-04 off Patrick's console

**NOT PUSHED. RULE 0.** The hunter half is a deploy to every PC and needs Patrick's go.

## What the console showed

    Checking for the latest version...
    *** Update looked stale/partial (GitHub cache) -- keeping the copy you have. ***
    CODE UPDATED 2026-08-18 -- GOLD CAPTURE ON: copper customers write as ORANGE ...
    GOLD DOTS TAB ON: every gold (upgrade) dot address -> 'Gold Dots' tab

The PC was running the **August 18** build: pre green-only Precise Fiber, pre `Gold Confirmed`,
pre Build Code / Status, pre split workbook, pre login-chooser wait. It would have written gold
to `Gold Dots`, a tab the clean deleted.

## Mechanism, proven

`optimus/install/RUN_HUNTER.bat` (the Desktop launcher; **launchers do not self-update**) downloads
the hunter to a `.new` file and only replaces the real one if:

    findstr /C:"GOLD CAPTURE ON" precise_fiber_hunter.py.new   || goto :dlbad

`INSTALL_OPTIMUS.bat` line 56 has the same check. That text lived in the launch banner.
Commit `67bf57b` (2026-08-25, "Cut the launch banner to one block") removed the banner.
`git grep` proves it: parent of 67bf57b has the string once, 67bf57b and today's head have it 0 times.

**Every hunter push since then — 25 of them — has been rejected as "stale/partial" by every PC
that updates through its launcher.** The 09-03 BUILD_DATE lesson fixed the hunter's INTERNAL
updater; nobody knew the launcher had a second, independent gate. The raw CDN is serving the
right file (BUILD_DATE 2026-09-03, 399,476 bytes); the launcher throws it away.

PCs with git installed self-heal through `self_update()`'s `git reset --hard` path, which runs
AFTER the launcher gave up — that is how some runs today carried 09-03 code while this PC did not.

## The fix — two halves

**1. Hunter (`hunter-sentinel.diff`, the half that matters tonight):** put the literal text back
as a constant next to BUILD_DATE, with a comment saying never remove it, and bump BUILD_DATE to
2026-09-04. **Every launcher and installer already on every PC accepts the very next download
with no launcher change.** This is the whole un-pin.

**2. Launchers (`RUN_HUNTER.bat.diff`, `INSTALL_OPTIMUS.bat.diff`):** check for `BUILD_DATE = `
instead, which every build carries, so a future banner edit cannot re-pin the fleet. Reaches a PC
only when the installer is re-run; harmless to ship now.

## Test — `python3 test_launcher_sentinel.py`

    reproduced: deployed RUN_HUNTER.bat / INSTALL_OPTIMUS.bat REJECT the current hunter (no 'GOLD CAPTURE ON')
    fixed: every deployed launcher ACCEPTS the patched hunter without any launcher change
    BUILD_DATE bumped 2026-09-03 -> 2026-09-04
    new launcher/installer check (BUILD_DATE) accepts both today's and the patched hunter
    py_compile clean
    
    ALL TESTS PASS

## Tonight's workaround on the stale PC, no push needed

`INSTALL_OPTIMUS.bat` curls the hunter STRAIGHT to its final path and only WARNS when the
sentinel check fails — it does not revert the file. So re-running the installer puts the 09-03
hunter on disk. It will print `WARNING: still got OLD hunter code` — that message is this same
bug and is wrong; the proof is the next launch printing `BUILD_DATE : 2026-09-03`.

## Deploy (on Patrick's go)

Apply all three diffs on a fresh fetch of `claude/optimus-map-tools-setup-6dcl6o`. The hunter
diff bumps BUILD_DATE, so the hunter's own updater accepts it too. Add the brain-verify claim
`^LAUNCHER_SENTINEL = "GOLD CAPTURE ON"` present in the hunter (already added; reads DRIFT
until this lands, correctly).
