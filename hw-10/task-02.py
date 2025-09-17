#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi
from dataclasses import dataclass
from typing import Callable
from math import isfinite

# Define non-standard function: f(x) = e^{-x} * sin^2(6x) + x^{0.3}
def f(x: np.ndarray) -> np.ndarray:
    return np.exp(-x) * np.sin(6*x)**2 + np.power(x, 0.3)

a, b = 0.0, 3.0

@dataclass
class MCResult:
    N: int
    estimate: float
    stderr: float
    seed: int

def mc_integral(func: Callable[[np.ndarray], np.ndarray], a: float, b: float, N: int, seed: int = 12345) -> MCResult:
    rng = np.random.default_rng(seed)
    xs = rng.uniform(a, b, size=N)
    vals = func(xs)
    width = b - a
    est = width * float(np.mean(vals))
    stderr = width * float(np.std(vals, ddof=1) / np.sqrt(N))
    return MCResult(N=N, estimate=est, stderr=stderr, seed=seed)

def main():
    # 1) Plot the function and shade the integration interval
    x = np.linspace(-0.2, 3.2, 1000)
    y = f(x)
    fig, ax = plt.subplots()
    ax.plot(x, y, linewidth=2, label="f(x) = e^{-x}·sin^2(6x) + x^{0.3}")
    ix = np.linspace(a, b, 600)
    iy = f(ix)
    ax.fill_between(ix, iy, alpha=0.25, label="Area under curve on [0, 3]")
    ax.axvline(a, linestyle="--")
    ax.axvline(b, linestyle="--")
    ax.set_xlim(x.min(), x.max())
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title("Function and integration interval")
    ax.grid(True, linewidth=0.5, alpha=0.5)
    ax.legend()
    plt.show()

    # 2) Monte Carlo runs
    Ns = [1_000, 10_000, 100_000]
    results = [mc_integral(f, a, b, N=n, seed=12345) for n in Ns]

    # 3) Reference via scipy.quad
    quad_val, quad_err = spi.quad(lambda t: float(np.exp(-t) * np.sin(6*t)**2 + np.power(t, 0.3)), a, b)
    print(f"Reference integral via scipy.quad on [0, 3]: {quad_val} (reported quad abs error ≈ {quad_err:.3e})")

    # 4) Print a table
    print("\nN (samples) | MC estimate   | MC std. error | abs. error   | rel. error   | |error|/stderr")
    print("-"*86)
    for r in results:
        abs_err = abs(r.estimate - quad_val)
        rel_err = abs_err / quad_val if quad_val != 0 else float("nan")
        z = abs_err / r.stderr if r.stderr > 0 and isfinite(r.stderr) else float("nan")
        print(f"{r.N:10,d} | {r.estimate:12.8f} | {r.stderr:13.8f} | {abs_err:12.8f} | {rel_err:12.3e} | {z:12.2f}")

if __name__ == "__main__":
    main()
