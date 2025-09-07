#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Compare substring search algorithms (Boyer–Moore, KMP, Rabin–Karp)
on one or more local text files. Measures performance for:
 - a pattern that exists in the text, and
 - a pattern that does not exist,
using timeit and prints a summary table.

Examples:
  python task-01.py --files data/article1.txt data/article2.txt
  python task-01.py --files data/article1.txt --pat-exist "алгоритм" --pat-absent "qwertyQWERTY"
  python task-01.py --files data/article1.txt data/article2.txt --repeat 7 --number 5 --csv results.csv
"""

import argparse
import statistics as stats
import sys
import timeit
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

# ------------------------------
# Loading utilities (LOCAL FILES ONLY)
# ------------------------------

def load_text(path: str, encoding: str = "utf-8") -> str:
    """
    Load text from a local file path only.
    """
    try:
        with open(path, "r", encoding=encoding, errors="replace") as f:
            return f.read()
    except Exception as e:
        print(f"[error] Failed to read file {path}: {e}", file=sys.stderr)
        sys.exit(1)

# ------------------------------
# Algorithms
# ------------------------------

def bm_search(text: str, pattern: str) -> int:
    """
    Boyer–Moore (bad character rule only, simple variant). Returns index or -1.
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return 0

    # Build last-occurrence table for characters
    last = {ch: -1 for ch in set(text)}
    for i, ch in enumerate(pattern):
        last[ch] = i

    i = m - 1  # index in text
    k = m - 1  # index in pattern
    while i < n:
        if text[i] == pattern[k]:
            if k == 0:
                return i
            i -= 1
            k -= 1
        else:
            li = last.get(text[i], -1)
            i += m - min(k, 1 + li)
            k = m - 1
    return -1

def kmp_search(text: str, pattern: str) -> int:
    """
    Knuth–Morris–Pratt. Returns index or -1.
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return 0

    # Longest Prefix Suffix (LPS) table
    lps = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j

    i = 0
    j = 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                return i - m
        else:
            if j > 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

def rabin_karp_search(text: str, pattern: str) -> int:
    """
    Rabin–Karp with rolling hash. Returns index or -1.
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1

    base = 256
    mod = 1_000_000_007  # large prime
    high_base = pow(base, m - 1, mod)

    def rhash(s: str) -> int:
        h = 0
        for ch in s:
            h = (h * base + ord(ch)) % mod
        return h

    pat_h = rhash(pattern)
    win_h = rhash(text[:m])

    for i in range(n - m + 1):
        if pat_h == win_h:
            # Verify to avoid false positives due to collisions
            if text[i : i + m] == pattern:
                return i
        if i < n - m:
            win_h = ((win_h - ord(text[i]) * high_base) * base + ord(text[i + m])) % mod
            if win_h < 0:
                win_h += mod
    return -1

ALGORITHMS: Dict[str, Callable[[str, str], int]] = {
    "Boyer-Moore": bm_search,
    "KMP": kmp_search,
    "Rabin-Karp": rabin_karp_search,
}

# ------------------------------
# Test pattern selection & validation
# ------------------------------

def make_default_patterns(text: str, prefer_len: int = 48) -> Tuple[str, str]:
    """
    Choose an 'existing' substring from the middle of the text and synthesize a guaranteed 'absent' one.
    """
    n = len(text)
    if n == 0:
        return "", "___ABSENT___"

    start = max(0, n // 2 - prefer_len // 2)
    exist = text[start : start + prefer_len]

    # If too short or whitespace-y, take from the start
    if len(exist) < 4:
        exist = text[: min(prefer_len, n)]
    exist = exist.strip()
    if not exist:
        exist = " "

    # Create an absent variant by mutating a single character
    def mutate(s: str) -> str:
        if not s:
            return "__ABSENT__"
        pos = len(s) // 2
        ch = s[pos]
        repl = chr((ord(ch) + 137) % 0x10FFFF)
        return s[:pos] + repl + s[pos + 1 :]

    absent = mutate(exist)

    # Ensure absence (retry if needed)
    tries = 0
    while text.find(absent) != -1 and tries < 10:
        absent = mutate(absent)
        tries += 1
    if text.find(absent) != -1:
        absent = absent + "\u0000"  # guaranteed to be absent in normal text

    return exist, absent

def sanity_check(text: str, pattern: str, algo: Callable[[str, str], int]) -> None:
    """
    Ensures the algorithm agrees with Python's built-in text.find.
    """
    expected = text.find(pattern)
    got = algo(text, pattern)
    if (expected == -1 and got != -1) or (expected != -1 and got != expected):
        raise AssertionError(
            f"Inconsistent with str.find: expected {expected}, got {got} ({algo.__name__})"
        )

# ------------------------------
# Benchmarking
# ------------------------------

@dataclass
class BenchResult:
    algo: str
    file: str
    case: str    # "exists" | "absent"
    n_runs: int
    n_inner: int
    mean: float
    stdev: float
    best: float

def time_algo(func: Callable[[], None], repeat: int, number: int) -> Tuple[float, float, float]:
    times = timeit.repeat(func, repeat=repeat, number=number)
    return (stats.mean(times), stats.pstdev(times), min(times))

def fmt_sec(s: float) -> str:
    if s < 1e-6:
        return f"{s*1e9:.1f} ns"
    if s < 1e-3:
        return f"{s*1e6:.1f} µs"
    if s < 1:
        return f"{s*1e3:.1f} ms"
    return f"{s:.3f} s"

def benchmark_on_text(
    text: str, file_label: str, pat_exist: str, pat_absent: str, repeat: int, number: int
) -> List[BenchResult]:
    results: List[BenchResult] = []
    for name, algo in ALGORITHMS.items():
        # One-time sanity-check per case
        sanity_check(text, pat_exist, algo)
        sanity_check(text, pat_absent, algo)

        # Existing pattern
        def run_exist():
            algo(text, pat_exist)
        mean, stdev, best = time_algo(run_exist, repeat, number)
        results.append(BenchResult(name, file_label, "exists", repeat, number, mean, stdev, best))

        # Absent pattern
        def run_absent():
            algo(text, pat_absent)
        mean, stdev, best = time_algo(run_absent, repeat, number)
        results.append(BenchResult(name, file_label, "absent", repeat, number, mean, stdev, best))
    return results

def choose_winner(results: List[BenchResult]) -> Tuple[str, BenchResult]:
    """
    Returns (criterion_description, winner) by the smallest mean time.
    """
    winner = min(results, key=lambda r: r.mean)
    return ("minimum mean time", winner)

def print_table(results: List[BenchResult]) -> None:
    headers = ["File", "Case", "Algorithm", "mean", "stdev", "best", "repeat×number"]
    rows = []
    for r in results:
        rows.append([
            r.file,
            r.case,
            r.algo,
            fmt_sec(r.mean),
            fmt_sec(r.stdev),
            fmt_sec(r.best),
            f"{r.n_runs}×{r.n_inner}",
        ])

    colw = [max(len(h), *(len(str(row[i])) for row in rows)) for i, h in enumerate(headers)]

    def header_line(sep_left="| ", sep_mid=" | ", sep_right=" |"):
        return sep_left + sep_mid.join(headers[i].ljust(colw[i]) for i in range(len(headers))) + sep_right

    def row_line(row):
        return "| " + " | ".join(str(row[i]).ljust(colw[i]) for i in range(len(headers))) + " |"

    print("\n" + header_line())
    print("|-" + "-|-".join("-" * w for w in colw) + "-|")
    for row in rows:
        print(row_line(row))
    print()

def save_csv(results: List[BenchResult], path: str) -> None:
    import csv
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["file", "case", "algorithm", "repeat", "number", "mean_sec", "stdev_sec", "best_sec"])
        for r in results:
            w.writerow([r.file, r.case, r.algo, r.n_runs, r.n_inner, r.mean, r.stdev, r.best])
    print(f"[ok] CSV saved to: {path}")

# ------------------------------
# CLI
# ------------------------------

def main():
    ap = argparse.ArgumentParser(description="Compare substring search algorithms on local text files")
    ap.add_argument("--files", nargs="+", required=True,
                    help="Paths to local text files")
    ap.add_argument("--pat-exist", dest="pat_exist", default=None,
                    help="A pattern guaranteed to exist in each text (auto-selected if omitted)")
    ap.add_argument("--pat-absent", dest="pat_absent", default=None,
                    help="A pattern guaranteed NOT to exist in each text (auto-synthesized if omitted)")
    ap.add_argument("--repeat", type=int, default=7, help="Number of timeit.repeat measurements (rows)")
    ap.add_argument("--number", type=int, default=5, help="Number of calls inside one measurement")
    ap.add_argument("--csv", type=str, default=None, help="Optional path to save CSV with results")
    args = ap.parse_args()

    all_results: List[BenchResult] = []

    for src in args.files:
        text = load_text(src)

        # Patterns for this text
        if args.pat_exist is None or args.pat_absent is None:
            auto_exist, auto_absent = make_default_patterns(text)
            pat_exist = args.pat_exist if args.pat_exist is not None else auto_exist
            pat_absent = args.pat_absent if args.pat_absent is not None else auto_absent
        else:
            pat_exist, pat_absent = args.pat_exist, args.pat_absent

        # If user-specified existing pattern is actually missing — warn and fall back to auto
        if text.find(pat_exist) == -1:
            print(f"[warn] In file '{src}' the provided --pat-exist was not found. Falling back to auto-selected.", file=sys.stderr)
            pat_exist, _ = make_default_patterns(text)

        # If user-specified absent pattern actually appears — warn and synthesize a new absent one
        if text.find(pat_absent) != -1:
            print(f"[warn] In file '{src}' the provided --pat-absent occurs in text. Generating a guaranteed-absent variant.", file=sys.stderr)
            _, pat_absent = make_default_patterns(text)

        file_label = src.split("/")[-1] or src
        results = benchmark_on_text(text, file_label, pat_exist, pat_absent, args.repeat, args.number)
        all_results.extend(results)

        # Per-file summary
        print(f"\n=== Results for: {file_label} ===")
        print(f"Existing pattern : {repr(pat_exist[:60])}{'…' if len(pat_exist) > 60 else ''}")
        print(f"Absent pattern   : {repr(pat_absent[:60])}{'…' if len(pat_absent) > 60 else ''}")
        print_table(results)
        crit, win = choose_winner(results)
        print(f"Fastest for '{file_label}' ({crit}): {win.algo} — {fmt_sec(win.mean)}\n")

    # Global winner across all files/cases
    if all_results:
        crit, win = choose_winner(all_results)
        print(f"=== Overall fastest algorithm ({crit} across all files/cases) ===")
        print(f"{win.algo} — {fmt_sec(win.mean)} (file: {win.file}, case: {win.case})")

    if args.csv:
        save_csv(all_results, args.csv)

if __name__ == "__main__":
    main()
