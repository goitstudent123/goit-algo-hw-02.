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

def main():
    n = 300000
    emp = simulate(n)
    theo = theoretical()
    sums = np.arange(2,13)
    print("Empirical probabilities:")
    for s in sums:
        print(f"{s}: {emp[s]*100:.2f}%")
    print("Conclusion: empirical probabilities approach theoretical values as n grows; 7 is the most likely sum (~16.67%).")

    plt.figure(figsize=(8,5))
    plt.bar(sums-0.15, emp[2:13], width=0.3, label="Empirical")
    plt.bar(sums+0.15, theo[2:13], width=0.3, label="Theoretical")
    plt.xticks(sums)
    plt.xlabel("Sum")
    plt.ylabel("Probability")
    plt.title(f"Dice sum probabilities (n={n})")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
