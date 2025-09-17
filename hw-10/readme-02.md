# Monte Carlo Integration

This project estimates the area under a function curve using the Monte Carlo method and compares it with a high-accuracy numerical integration (`scipy.quad`).

---

## Assignment Statement

Обчисліть значення інтеграла функції за допомогою методу Монте-Карло. Перевірте правильність результату шляхом порівняння з аналітичним або чисельним методом. Зробіть висновки.

---

## Function

We integrate on the interval `[0, 3]` the function:

```
f(x) = exp(-x) * sin^2(6x) + x^0.3
```

This function is non-standard:
- it has oscillations (from `sin^2(6x)`)
- it decays with `exp(-x)`
- it has a cusp near 0 from `x^0.3`.

---

## Results from Code Execution

Reference value from `scipy.quad`: **3.682269831963**

Monte Carlo estimates:

Samples (N) | MC estimate | MC std. error | Abs. error | Rel. error
----------- | ----------- | ------------- | ----------- | ----------
1,000       | 3.684776    | 0.018951      | 0.002506    | 0.00068
10,000      | 3.681703    | 0.006153      | 0.000567    | 0.00015
100,000     | 3.685228    | 0.001941      | 0.002958    | 0.00080

---

## Analysis

- **Monte Carlo**
  - Very easy to implement.
  - Accuracy improves as sample size increases.
  - Error decreases ~ as `1/sqrt(N)`.
  - Works well for complex or high-dimensional integrals.

- **scipy.quad**
  - Deterministic and highly accurate for 1D integrals.
  - Much faster and more precise for this case.
  - Not practical in higher dimensions.

---

## Conclusion

- Monte Carlo integration gives results close to the reference, with accuracy improving as the number of samples grows.
- For simple one-dimensional integrals, classical numerical methods (`quad`) are far more efficient.
- Monte Carlo is most useful when dealing with **complex functions** or **multi-dimensional integrals** where standard methods are not feasible.
