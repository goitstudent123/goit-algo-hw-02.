# Task 3: Benchmark merge sort, insertion sort, and Python's built-in Timsort (sorted).

import random
import timeit

# ----------------- Algorithms -----------------

def merge_sort(arr):
    """Classic recursive merge sort that returns a new sorted list."""
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    i = j = 0
    out = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    if i < len(left):
        out.extend(left[i:])
    if j < len(right):
        out.extend(right[j:])
    return out

def insertion_sort(arr):
    """In-place insertion sort; returns the same list for convenience."""
    a = arr[:]  # Work on a copy to be fair
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j+1] = a[j]
            j -= 1
        a[j+1] = key
    return a

# ----------------- Data generators -----------------

def gen_random(n, seed=123):
    random.seed(seed)
    return [random.randint(0, 10**6) for _ in range(n)]

def gen_nearly_sorted(n, seed=123, swaps= int(0.01 * 10_000)):  # small number of swaps
    random.seed(seed)
    a = list(range(n))
    # Apply limited random swaps
    for _ in range(max(1, n//100)):
        i = random.randrange(n)
        j = random.randrange(n)
        a[i], a[j] = a[j], a[i]
    return a

def gen_reverse(n):
    return list(range(n, 0, -1))

def gen_dups(n, seed=123):
    random.seed(seed)
    return [random.randint(0, 100) for _ in range(n)]  # many duplicates

# ----------------- Benchmark harness -----------------

def bench_once(label, func, data):
    """Measure a single timing for func(data) using timeit.Timer."""
    timer = timeit.Timer(lambda: func(data))
    # Small number of repeats to keep runtime reasonable
    tries, reps = 3, 1
    best = min(timer.repeat(repeat=tries, number=reps))
    return best

def run_suite():
    sizes = [1000, 5000, 10000, 20000]
    datasets = [
        ("random", gen_random),
        ("nearly_sorted", gen_nearly_sorted),
        ("reverse", gen_reverse),
        ("duplicates", gen_dups),
    ]

    algos = [
        ("merge_sort", merge_sort),
        ("insertion_sort", insertion_sort),
        ("timsort_sorted", sorted),
    ]

    print("# Benchmark results (seconds):\n")
    print(f"{'dataset':<16}{'n':>8}{'algorithm':>20}{'time':>12}")
    print("-" * 56)

    for name, gen in datasets:
        for n in sizes:
            data = gen(n)
            for algo_name, algo in algos:
                # Limit insertion sort on large n to avoid very long runtimes
                if algo_name == "insertion_sort" and n > 10000:
                    continue
                t = bench_once(name, algo, data)
                print(f"{name:<16}{n:>8}{algo_name:>20}{t:>12.6f}")

    print("\nNotes:") 
    print("- Insertion sort: very slow on large arrays, but fine on tiny or nearly-sorted ones.")
    print("- Merge sort: consistently fast, works the same on all types of input, and is stable.")
    print("- Timsort (Python’s sorted): combines merge sort and insertion sort, detects ordered runs, very fast on nearly-sorted data, stable, C-optimized, and the fastest in practice.")

if __name__ == "__main__":
    run_suite()
