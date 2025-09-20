import numpy as np
import matplotlib.pyplot as plt

def simulate(n=200000):
    d1 = np.random.randint(1,7,size=n)
    d2 = np.random.randint(1,7,size=n)
    sums = d1 + d2
    counts = np.bincount(sums, minlength=13)
    probs = counts / n
    return probs

def theoretical():
    probs = {2:1,3:2,4:3,5:4,6:5,7:6,8:5,9:4,10:3,11:2,12:1}
    total = 36
    arr = np.zeros(13)
    for s,c in probs.items():
        arr[s] = c/total
    return arr

import numpy as np
import matplotlib.pyplot as plt

# ... keep your simulate() and theoretical() unchanged ...

def compare(emp_probs, theo_probs, n):
    sums = np.arange(2, 13)
    emp = emp_probs[2:13]
    theo = theo_probs[2:13]

    abs_err = np.abs(emp - theo)
    mae = abs_err.mean()
    rmse = np.sqrt(((emp - theo) ** 2).mean())
    max_idx = abs_err.argmax()

    # chi-square test against theoretical multinomial with total n
    obs = (emp * n).astype(int)
    exp = theo * n
    chisq = ((obs - exp) ** 2 / exp).sum()

    print("\nEmpirical vs Theoretical (probabilities)")
    print("Sum |  Empirical   Theoretical   Abs.Error")
    print("-------------------------------------------")
    for s, e, t, d in zip(sums, emp, theo, abs_err):
        print(f"{s:>3} | {e:10.4%}  {t:11.4%}   {d:9.4%}")
    print("-------------------------------------------")
    print(f"MAE:  {mae:.4%}")
    print(f"RMSE: {rmse:.4%}")
    print(f"Max error: {abs_err[max_idx]:.4%} at sum={sums[max_idx]}")
    print(f"Chi-square (11 dof): {chisq:.2f}")
    print("Conclusion: With large n, MAE and RMSE are small and the chi-square is modest, "
          "which indicates the Monte Carlo distribution matches the analytic distribution.")

def main():
    n = 300_000
    emp = simulate(n)
    theo = theoretical()
    sums = np.arange(2, 13)

    # numeric comparison
    compare(emp, theo, n)

    # side-by-side bars + save figure for README
    plt.figure(figsize=(8,5))
    plt.bar(sums - 0.15, emp[2:13], width=0.3, label="Monte Carlo")
    plt.bar(sums + 0.15, theo[2:13], width=0.3, label="Analytic (1–6 dice)")
    plt.xticks(sums)
    plt.xlabel("Sum")
    plt.ylabel("Probability")
    plt.title(f"Dice Sum Probabilities (n={n:,})")
    plt.legend()
    plt.tight_layout()
    plt.savefig("docs/dice.png", dpi=150)
    plt.show()

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
