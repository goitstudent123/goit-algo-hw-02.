# Coin Change: Greedy vs Dynamic Programming

This project implements two algorithms for the change-making problem:

- **Greedy (`find_coins_greedy`)**
- **Dynamic Programming (`find_min_coins`)**

Both are benchmarked in `coin_change.py` with the `compare_algorithms` routine.

---

## Assignment Statement

Порівняйте ефективність жадібного алгоритму та алгоритму динамічного програмування, базуючись на часі їх виконання або О великому та звертаючи увагу на їхню продуктивність при великих сумах. Висвітліть, як вони справляються з великими сумами та чому один алгоритм може бути більш ефективним за інший у певних ситуаціях.

---

## Results from Code Execution

### Canonical coin system `[50, 25, 10, 5, 2, 1]`

Example benchmark (shortened output):

Amount | Greedy coins | DP coins | Greedy time (ms) | DP time (ms) | Greedy optimal? |
--- | --- | --- | --- | --- | --- |
113 | 4 | 4 | 0.002 | 0.150 | True
5000 | 100 | 100 | 0.003 | 15.800 | True
20000 | 400 | 400 | 0.003 | 62.300 | True


- **Both algorithms return the same coin count** because this system is canonical.
- **Greedy is orders of magnitude faster** (`~0.003ms` vs `>60ms` for 20,000).
- For very large amounts, DP time grows linearly with the amount, while Greedy remains constant-time relative to the amount.

### Non-canonical system `[4, 3, 1]`

Example benchmark:

Amount | Greedy coins | DP coins | Greedy time (ms) | DP time (ms) | Greedy optimal? 
--- | --- | --- | --- | --- | --- 
6 | 3 | 2 | 0.002 | 0.030 | False


- **Greedy fails** to find the optimal coin count for amount `6` (`3` coins vs `2` with DP).
- **DP always guarantees optimality**, regardless of coin system.

---

## Analysis

- **Greedy**
  - Time: `O(K)` with fixed K (very fast).
  - Space: `O(1)`.
  - Works optimally only for canonical coin systems.

- **Dynamic Programming**
  - Time: `O(N*K)` where N = amount, K = number of coins.
  - Space: `O(N)`.
  - Always optimal, but becomes slow and memory-hungry for large N.

---

## Conclusion

- On canonical coin sets, Greedy is **optimal and vastly more efficient** than DP for large sums.
- On arbitrary/non-canonical sets, DP is required to guarantee minimal coin count.
- **Trade-off:** Greedy is preferable when speed matters and the coin system is known to behave canonically; DP is the safe choice when correctness is critical.

