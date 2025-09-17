# coin_change.py
from collections import defaultdict
from time import perf_counter
from typing import Dict, List, Tuple


DEFAULT_COINS = [50, 25, 10, 5, 2, 1]


def validate_amount(amount: int):
    if not isinstance(amount, int):
        raise TypeError("amount must be an integer")
    if amount < 0:
        raise ValueError("amount cannot be negative")


def find_coins_greedy(amount: int, coins: List[int] = DEFAULT_COINS) -> Dict[int, int]:
    """
    Greedy algorithm: always take the largest coin not exceeding the remainder.
    Returns a dict {denomination: count}.
    Time: O(K) given a fixed coin set, where K is the number of denominations.
    """
    validate_amount(amount)
    result: Dict[int, int] = {}
    remaining = amount
    for coin in sorted(coins, reverse=True):
        if remaining == 0:
            break
        cnt, remaining = divmod(remaining, coin)
        if cnt:
            result[coin] = cnt
    return result


def find_min_coins(amount: int, coins: List[int] = DEFAULT_COINS) -> Dict[int, int]:
    """
    Dynamic Programming (bottom-up) that guarantees the minimum number of coins.
    Returns a dict {denomination: count}.
    Time: O(N*K), Memory: O(N) where N=amount and K=len(coins).
    """
    validate_amount(amount)
    if amount == 0:
        return {}

    coins = sorted(coins)
    INF = amount + 1

    # dp[x] = minimal coin count for sum x
    dp = [0] + [INF] * amount
    # prev_coin[x] = last coin used in an optimal solution for x
    prev_coin = [-1] * (amount + 1)

    for x in range(1, amount + 1):
        best = INF
        best_coin = -1
        for c in coins:
            if c > x:
                break
            if dp[x - c] + 1 < best:
                best = dp[x - c] + 1
                best_coin = c
        dp[x] = best
        prev_coin[x] = best_coin

    if dp[amount] == INF:
        raise ValueError("Cannot form the amount with the given coins")

    # Reconstruct solution
    counts = defaultdict(int)
    cur = amount
    while cur > 0:
        c = prev_coin[cur]
        counts[c] += 1
        cur -= c
    # Sorted by denomination ascending for determinism
    return dict(sorted(counts.items()))


def count_coins(sol: Dict[int, int]) -> int:
    """Total number of coins used in a solution dict."""
    return sum(sol.values())


def solution_value(sol: Dict[int, int]) -> int:
    """Total monetary value of a solution dict."""
    return sum(k * v for k, v in sol.items())


def time_call(fn, *args, repeat: int = 3, **kwargs) -> Tuple[float, object]:
    """
    Time a callable over `repeat` runs; return (best_time_seconds, last_result).
    We take the best time to reduce noise from the interpreter/OS scheduling.
    """
    best = float("inf")
    last_result = None
    for _ in range(repeat):
        t0 = perf_counter()
        last_result = fn(*args, **kwargs)
        dt = perf_counter() - t0
        if dt < best:
            best = dt
    return best, last_result


def compare_algorithms(
    amounts: List[int],
    coins: List[int] = DEFAULT_COINS,
    repeat: int = 5,
    show_solutions: bool = False,
):
    """
    Compare Greedy vs DP across a list of amounts:
    - Verifies both produce the same total value.
    - Reports coin counts and timing (best-of-N runs).
    - Optionally prints the actual solutions.
    """
    print(f"Denominations: {coins}")
    header = (
        f"{'Amount':>8} | {'Greedy coins':>12} | {'DP coins':>8} | "
        f"{'Greedy time (ms)':>16} | {'DP time (ms)':>12} | {'Greedy optimal?':>14}"
    )
    print(header)
    print("-" * len(header))

    for amt in amounts:
        tg, sol_g = time_call(find_coins_greedy, amt, coins, repeat=repeat)
        td, sol_d = time_call(find_min_coins, amt, coins, repeat=repeat)

        # Basic checks
        vg = solution_value(sol_g)
        vd = solution_value(sol_d)
        if vg != amt or vd != amt:
            raise AssertionError("One of the algorithms returned a wrong amount")

        cg = count_coins(sol_g)
        cd = count_coins(sol_d)

        # Greedy is optimal if it uses the same number of coins as DP
        greedy_optimal = (cg == cd)

        print(
            f"{amt:>8} | {cg:>12} | {cd:>8} | "
            f"{tg * 1000:>16.3f} | {td * 1000:>12.3f} | {str(greedy_optimal):>14}"
        )

        if show_solutions:
            print(f"  Greedy: {dict(sorted(sol_g.items()))}")
            print(f"  DP    : {dict(sorted(sol_d.items()))}")

    print("\nNote: times are best-of-{repeat} runs per amount.".format(repeat=repeat))


if __name__ == "__main__":
    # Demo set: small, medium, and large amounts.
    demo_amounts = [0, 1, 6, 13, 113, 999, 5000, 20000]

    # 1) Canonical coin system: greedy should be optimal and much faster.
    print("=== Canonical system [50, 25, 10, 5, 2, 1] ===")
    compare_algorithms(demo_amounts, coins=DEFAULT_COINS, repeat=5, show_solutions=False)

    # 2) Non-canonical example where greedy can fail:
    print("\n=== Non-canonical system [4, 3, 1] (greedy can be suboptimal) ===")
    compare_algorithms([6, 7, 8, 25], coins=[4, 3, 1], repeat=5, show_solutions=True)
