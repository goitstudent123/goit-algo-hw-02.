import os
import sys
import shutil
import argparse
import tempfile
from pathlib import Path

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def safe_copy(src, dst_dir):
    ensure_dir(dst_dir)
    basename = os.path.basename(src)
    name, ext = os.path.splitext(basename)
    candidate = os.path.join(dst_dir, basename)
    counter = 1
    while os.path.exists(candidate):
        candidate = os.path.join(dst_dir, f"{name}__{counter}{ext}")
        counter += 1
    try:
        shutil.copy2(src, candidate)
        return candidate
    except PermissionError as e:
        print(f"[WARN] Permission denied: {src} -> {candidate}: {e}")
    except FileNotFoundError as e:
        print(f"[WARN] File not found: {src}: {e}")
    except OSError as e:
        print(f"[WARN] OS error while copying {src}: {e}")
    return None

def walk_and_copy(src_root, dst_root):
    src_root = os.path.abspath(src_root)
    dst_root = os.path.abspath(dst_root)

    for root, dirs, files in os.walk(src_root):
        for name in files:
            src_path = os.path.join(root, name)
            _, ext = os.path.splitext(name)
            ext_folder = (ext[1:].lower() if ext else "no_ext") or "no_ext"
            dst_dir = os.path.join(dst_root, ext_folder)
            copied = safe_copy(src_path, dst_dir)
            if copied:
                print(f"Copied: {src_path} -> {copied}")

def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Recursively copy files from SOURCE to DEST, sorting by extension."
    )
    parser.add_argument("source", nargs="?", help="Path to source directory to scan recursively.")
    parser.add_argument("dest", nargs="?", default="dist",
                        help="Destination directory (default: dist).")
    return parser.parse_args(argv)

# ---- Self-test harness (runs only when no CLI args are given) ----

def make_sample_tree(base):
    """
    Create:
      test_src/
        a.txt, b.md, e
        sub1/c.py
        sub2/d.txt
    Returns (src_dir_path, dest_dir_path_expected)
    """
    src = Path(base) / "test_src"
    dist = Path(base) / "test_dist"
    (src / "sub1").mkdir(parents=True, exist_ok=True)
    (src / "sub2").mkdir(parents=True, exist_ok=True)

    (src / "a.txt").write_text("hello\n", encoding="utf-8")
    (src / "b.md").write_text("world\n", encoding="utf-8")
    (src / "e").write_text("noext\n", encoding="utf-8")
    (src / "sub1" / "c.py").write_text("print('py')\n", encoding="utf-8")
    (src / "sub2" / "d.txt").write_text("notes\n", encoding="utf-8")
    return str(src), str(dist)

def validate_structure(dist):
    """
    Validate the expected layout:
      dist/
        md/b.md
        no_ext/e
        py/c.py
        txt/a.txt
        txt/d.txt
    """
    dist = Path(dist)
    expected = [
        dist / "md" / "b.md",
        dist / "no_ext" / "e",
        dist / "py" / "c.py",
        dist / "txt" / "a.txt",
        dist / "txt" / "d.txt",
    ]
    missing = [str(p) for p in expected if not p.exists()]
    extra = []
    # Collect extras by walking
    present = set(str(p) for p in expected)
    for root, _, files in os.walk(dist):
        for f in files:
            path = str(Path(root) / f)
            if path not in present:
                extra.append(path)
    ok = (len(missing) == 0)
    return ok, missing, extra

def run_selftest():
    """
    Create sample tree, run copy, validate results, and always cleanup.
    """
    tempdir = tempfile.mkdtemp(prefix="task01_selftest_")
    print(f"[SELFTEST] Working in: {tempdir}")
    src = dest = None
    try:
        src, dest = make_sample_tree(tempdir)
        print(f"[SELFTEST] Source: {src}")
        print(f"[SELFTEST] Dest:   {dest}")

        ensure_dir(dest)
        walk_and_copy(src, dest)

        ok, missing, extra = validate_structure(dest)
        if ok:
            print("[SELFTEST] PASS: expected files are present.")
        else:
            print("[SELFTEST] FAIL: missing expected files:")
            for m in missing:
                print(f"  - {m}")

        if extra:
            print("[SELFTEST] NOTE: unexpected extra files found:")
            for e in extra:
                print(f"  - {e}")

        return 0 if ok else 1
    except Exception as e:
        print(f"[SELFTEST] ERROR: {e}")
        return 1
    finally:
        try:
            shutil.rmtree(tempdir, ignore_errors=False)
            print(f"[SELFTEST] Cleaned: {tempdir}")
        except Exception as ce:
            print(f"[SELFTEST] Cleanup error: {ce}")

# ---- Entry point ----

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    # If no args: run the self-test harness
    if len(argv) == 0:
        return run_selftest()

    args = parse_args(argv)

    if not os.path.isdir(args.source):
        print(f"[ERROR] Source is not a directory: {args.source}")
        return 1

    try:
        ensure_dir(args.dest)
    except PermissionError as e:
        print(f"[ERROR] Permission denied creating destination: {args.dest}: {e}")
        return 1
    except OSError as e:
        print(f"[ERROR] OS error creating destination: {args.dest}: {e}")
        return 1

    try:
        walk_and_copy(args.source, args.dest)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
