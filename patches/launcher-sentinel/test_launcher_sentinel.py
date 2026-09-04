"""Proves the launcher pin and the fix, with no Windows needed.
findstr /C:"X" file  ==  the literal substring test below."""
import io, subprocess, sys
live   = io.open('hunter_live.py', encoding='utf-8').read()          # branch head today
fixed  = io.open('precise_fiber_hunter.py', encoding='utf-8').read() # patched
def launcher_accepts(text, sentinel): return sentinel in text
# 1. reproduce: the deployed launchers reject TODAY'S hunter
assert not launcher_accepts(live, "GOLD CAPTURE ON"), "live hunter unexpectedly carries the sentinel"
print("reproduced: deployed RUN_HUNTER.bat / INSTALL_OPTIMUS.bat REJECT the current hunter (no 'GOLD CAPTURE ON')")
# 2. fix: the same deployed launchers accept the patched hunter
assert launcher_accepts(fixed, "GOLD CAPTURE ON")
print("fixed: every deployed launcher ACCEPTS the patched hunter without any launcher change")
# 3. BUILD_DATE bumped, so the hunter's own updater also treats it as new
assert 'BUILD_DATE = "2026-09-04"' in fixed and 'BUILD_DATE = "2026-09-03"' not in fixed
print("BUILD_DATE bumped 2026-09-03 -> 2026-09-04")
# 4. the new launcher check is satisfied by BOTH old and new hunters (no re-pin possible)
for f in ('RUN_HUNTER.bat','INSTALL_OPTIMUS.bat'):
    b=io.open(f,encoding='utf-8',errors='replace').read()
    assert 'findstr /C:"BUILD_DATE = "' in b and 'findstr /C:"GOLD CAPTURE ON"' not in b, f
    assert launcher_accepts(live, "BUILD_DATE = ") and launcher_accepts(fixed, "BUILD_DATE = ")
print("new launcher/installer check (BUILD_DATE) accepts both today's and the patched hunter")
# 5. still valid python
subprocess.check_call([sys.executable, "-m", "py_compile", "precise_fiber_hunter.py"])
print("py_compile clean")
print("\nALL TESTS PASS")
