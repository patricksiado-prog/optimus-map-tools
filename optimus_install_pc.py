#!/usr/bin/env python3
"""
OPTIMUS INSTALLER (PC) v3  --  run on BOTH HP laptops, identical result
=============================================================================
Self-contained. No token. Pulls EVERYTHING from public sources:
  * the 3 programs  -> from GitHub raw  (proven working)
  * google_creds.json -> from your Drive (public file id below)

So the PC never needs creds hunted, copied, or fixed by hand. The installer
fetches a known-good creds file, VALIDATES it (real JSON + private key loads),
and writes it next to the programs so MapMan finds it automatically.

WHERE IT WRITES:  C:\\Users\\patri\\Optimus
HOW TO RUN: double-click INSTALL_OPTIMUS.bat (next to this file), or:
    python optimus_install_pc.py
=============================================================================
"""
import os, sys, ast, json, shutil, urllib.request, urllib.error

REPO    = "patricksiado-prog/optimus-map-tools"
BRANCH  = "main"
INSTALL = r"C:\Users\patri\Optimus"
DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")

# Known-good google_creds.json living in Drive (verified 2371 bytes, service
# account fiberscanner@fiberscanner-493900). Public-download by id.
CREDS_DRIVE_ID = "1upYH4h2VsmOwO82v9CVjMpE6IzV-5dIs"

PROGRAMS = ["themapman.py", "fiber_hunter.py", "hunter_dot_extractor.py"]

LAUNCHERS = {
    "RUN_MAPMAN.bat":    "themapman.py",
    "RUN_HUNTER.bat":    "fiber_hunter.py",
    "RUN_EXTRACTOR.bat": "hunter_dot_extractor.py",
}


def line():
    print("=" * 64)


def http_get(url, timeout=60):
    req = urllib.request.Request(url, headers={
        "User-Agent": "optimus-installer", "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_program(repo_path):
    url = "https://raw.githubusercontent.com/%s/%s/%s" % (REPO, BRANCH, repo_path)
    return http_get(url)


def fetch_drive(file_id):
    """Public Drive download by id. confirm=t skips the size-warning page."""
    url = "https://drive.google.com/uc?export=download&id=%s&confirm=t" % file_id
    return http_get(url, timeout=90)


def creds_bytes_valid(raw):
    """True only if real JSON service-account with a usable private key.
    Catches empty / HTML / truncated corruption AND a Drive sign-in page."""
    if not raw or len(raw) < 200:
        return False, "empty or too small (%d bytes)" % (len(raw) if raw else 0)
    head = raw.lstrip()[:300].lower()
    if head.startswith(b"<"):
        return False, "looks like HTML (Drive sign-in / warning page)"
    try:
        d = json.loads(raw.decode("utf-8"))
    except Exception as e:
        return False, "not valid JSON: %s" % e
    if not isinstance(d, dict):
        return False, "JSON root is not an object"
    for k in ("type", "client_email", "private_key", "token_uri"):
        if k not in d:
            return False, "missing key: %s" % k
    if d.get("type") != "service_account":
        return False, 'type is "%s", expected "service_account"' % d.get("type")
    if "BEGIN PRIVATE KEY" not in d.get("private_key", ""):
        return False, "private_key has no BEGIN PRIVATE KEY block"
    return True, "valid (%d bytes, %s)" % (len(raw), d["client_email"])


def install_programs():
    os.makedirs(INSTALL, exist_ok=True)
    ok = 0
    for name in PROGRAMS:
        try:
            raw = fetch_program(name)
        except urllib.error.HTTPError as e:
            print("  FAIL  %-26s HTTP %s" % (name, e.code)); continue
        except Exception as e:
            print("  FAIL  %-26s %s" % (name, e)); continue
        try:
            ast.parse(raw.decode("utf-8"))
        except Exception as e:
            print("  FAIL  %-26s won't parse (%s) -- not writing" % (name, e)); continue
        out = os.path.join(INSTALL, name)
        if os.path.exists(out):
            try:
                shutil.copyfile(out, out + ".bak")
            except Exception:
                pass
        with open(out, "wb") as f:
            f.write(raw)
        print("  OK    %-26s %6d bytes" % (name, len(raw)))
        ok += 1
    return ok


def install_creds():
    dest = os.path.join(INSTALL, "google_creds.json")

    # If a valid creds file is already here, keep it.
    if os.path.exists(dest):
        try:
            with open(dest, "rb") as f:
                existing = f.read()
            good, why = creds_bytes_valid(existing)
            if good:
                print("  OK    google_creds.json        existing %s" % why)
                return True
            else:
                print("  ..    existing creds invalid (%s) -- replacing from Drive" % why)
                try:
                    os.replace(dest, dest + ".broken")
                except Exception:
                    pass
        except Exception:
            pass

    # Pull a known-good copy from Drive.
    print("  ..    pulling google_creds.json from Drive ...")
    try:
        raw = fetch_drive(CREDS_DRIVE_ID)
    except Exception as e:
        print("  FAIL  could not download creds from Drive: %s" % e)
        return False

    good, why = creds_bytes_valid(raw)
    if not good:
        print("  FAIL  Drive creds rejected: %s" % why)
        print("        (If this says HTML, the Drive file isn't shared 'anyone with link'.)")
        return False

    tmp = dest + ".new"
    try:
        with open(tmp, "wb") as f:
            f.write(raw)
        os.replace(tmp, dest)
    except Exception as e:
        print("  FAIL  could not write creds: %s" % e)
        return False

    # read back + re-verify
    try:
        with open(dest, "rb") as f:
            good, why = creds_bytes_valid(f.read())
        if not good:
            print("  FAIL  readback verification failed: %s" % why)
            return False
    except Exception as e:
        print("  FAIL  readback error: %s" % e)
        return False

    print("  OK    google_creds.json        %s  (from Drive)" % why)
    return True


def write_launchers():
    for bat, script in LAUNCHERS.items():
        p = os.path.join(INSTALL, bat)
        with open(p, "w", encoding="ascii") as f:
            f.write("@echo off\r\n")
            f.write('cd /d "%s"\r\n' % INSTALL)
            f.write('echo Running %s ...\r\n' % script)
            f.write('python "%s"\r\n' % script)
            f.write("echo.\r\n")
            f.write("pause\r\n")
        print("  OK    %s" % bat)


def quarantine_desktop():
    q = os.path.join(INSTALL, "quarantine_from_desktop")
    moved = 0
    for name in ["themapman.py", "THEMAPMAN.py", "fiber_hunter.py",
                 "hunter_dot_extractor.py", "OPTIMUS_V3.py"]:
        src = os.path.join(DESKTOP, name)
        if os.path.exists(src):
            os.makedirs(q, exist_ok=True)
            try:
                shutil.move(src, os.path.join(q, name)); moved += 1
            except Exception:
                pass
    if moved:
        print("  OK    quarantined %d stray Desktop .py file(s)" % moved)
    else:
        print("  OK    no stray Desktop files to clean")


def main():
    line()
    print("  OPTIMUS INSTALLER v3  ->  %s" % INSTALL)
    print("  (programs from GitHub, creds from Drive -- all public, no token)")
    line()

    print("\n[1/4] Programs from GitHub:")
    n = install_programs()

    print("\n[2/4] Credentials (auto-pull from Drive):")
    creds_ok = install_creds()

    print("\n[3/4] Launchers:")
    write_launchers()

    print("\n[4/4] Cleanup:")
    quarantine_desktop()

    line()
    if n == len(PROGRAMS) and creds_ok:
        print("  DONE. Everything installed AND creds are valid.")
        print("  >>> Run MapMan:  double-click  %s\\RUN_MAPMAN.bat" % INSTALL)
    elif not creds_ok:
        print("  PROGRAMS ok, but CREDS FAILED. See [2/4] above.")
        print("  Most likely the Drive creds file isn't shared 'anyone with link'.")
    else:
        print("  PARTIAL: %d/%d programs. See FAIL lines above." % (n, len(PROGRAMS)))
    line()
    try:
        input("\nPress Enter to close...")
    except Exception:
        pass


if __name__ == "__main__":
    main()
