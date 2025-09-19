from typing import Dict, Tuple, List

items = {
  "pizza": {"cost": 50, "calories": 300},
  "hamburger": {"cost": 40, "calories": 250},
  "hot-dog": {"cost": 30, "calories": 200},
  "pepsi": {"cost": 10, "calories": 100},
  "cola": {"cost": 15, "calories": 220},
  "potato": {"cost": 25, "calories": 350}
}

def greedy_algorithm(budget: int) -> Tuple[List[str], int, int]:
    sorted_items = sorted(items.items(), key=lambda kv: kv[1]["calories"]/kv[1]["cost"], reverse=True)
    chosen = []
    total_cost = 0
    total_cal = 0
    for name, info in sorted_items:
        if total_cost + info["cost"] <= budget:
            chosen.append(name)
            total_cost += info["cost"]
            total_cal += info["calories"]
    return chosen, total_cost, total_cal

def dynamic_programming(budget: int) -> Tuple[List[str], int, int]:
    names = list(items.keys())
    costs = [items[n]["cost"] for n in names]
    cals = [items[n]["calories"] for n in names]
    dp = [[0]*(budget+1) for _ in range(len(names)+1)]
    keep = [[False]*(budget+1) for _ in range(len(names)+1)]
    for i in range(1, len(names)+1):
        for b in range(budget+1):
            dp[i][b] = dp[i-1][b]
            if costs[i-1] <= b:
                val = dp[i-1][b - costs[i-1]] + cals[i-1]
                if val > dp[i][b]:
                    dp[i][b] = val
                    keep[i][b] = True
    b = budget
    chosen = []
    for i in range(len(names), 0, -1):
        if keep[i][b]:
            chosen.append(names[i-1])
            b -= costs[i-1]
    chosen.reverse()
    total_cost = sum(items[n]["cost"] for n in chosen)
    total_cal = sum(items[n]["calories"] for n in chosen)
    return chosen, total_cost, total_cal

def main():
    budget = 100
    g_items, g_cost, g_cal = greedy_algorithm(budget)
    d_items, d_cost, d_cal = dynamic_programming(budget)

    print(f"Budget: {budget}")
    print("Greedy:", g_items, "cost=", g_cost, "calories=", g_cal)
    print("Dynamic:", d_items, "cost=", d_cost, "calories=", d_cal)

    better = "dynamic programming" if d_cal >= g_cal else "greedy"
    print(f"Conclusion: {better} achieves equal or higher calories for this budget; greedy is faster but may miss optimal combinations.")

if __name__ == "__main__":
    main()
