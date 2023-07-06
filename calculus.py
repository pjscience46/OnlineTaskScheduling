from math import log, sqrt
import matplotlib.pyplot as plt
import numpy as np


def f(p):
    return (2 * log(p)) / (1 + log(p * log(p)))


MAX_RATIO = 10.0


# for p in range(1, 200):
#     print(f"f({2**p}) = {f(2**p)}")


def dis_point(alpha, gamma, p):
    return ((p+1)**(gamma+1) - alpha)/(alpha - 1)


print(f"Point : {dis_point(1.54, 0.01, 1)}")


def f_dis(alpha, gamma, p):
    w = dis_point(alpha, gamma, p)
    top = w/p + p**gamma
    if gamma == 0:
        bot = 1
    else:
        bot = (gamma+1)*(w/gamma)**(gamma/(gamma+1))
    return top/bot


print(f"Dis value: {f_dis(1.54, 0.01, 1)}")
print(f"Dis value: {f_dis(1.54, 0.01, 2)}")

def beta(x):
    return (x + (x - 1) ** 2) / (2 * sqrt(x) * (x - 1))


def mu(alpha: float, beta: float) -> float:
    nom = alpha + beta + 1 - sqrt(pow(alpha + beta + 1, 2) - 4 * beta)
    return nom / (2 * beta)


print(1.0/mu(1.5, 1.34))


def ratio(alpha: float) -> float:
    if alpha < 1 or beta(alpha) < 1:
        return MAX_RATIO
    return min(MAX_RATIO, 1.0 / mu(alpha, beta(alpha)))


x = np.linspace(0, 1, 1000)
ratios = []
alphas = []
betas = []

for g in x:
    best_ratio = 100
    best_p = None
    best_alpha = None
    best_beta = None
    for alpha in np.linspace(1.01, 2, 1000):
        p = 1
        while f_dis(alpha, g, p) < f_dis(alpha, g, p+1) and p < 1000:
            p += 1
        if 1.0/mu(alpha, f_dis(alpha, g, p)) < best_ratio:
            best_ratio = 1.0/mu(alpha, f_dis(alpha, g, p))
            best_p = p
            best_alpha = alpha
            best_beta = f_dis(alpha, g, p)
    ratios.append(best_ratio)
    alphas.append(best_alpha)
    betas.append(best_beta)
    # print(f"gamma: {g:.2f}, ratio : {best_ratio:.3f}, p : {best_p:<5d}, alpha: {best_alpha:.3f}, beta : {best_beta:.3f}")


plt.plot(x, ratios)
plt.plot(x, alphas)
plt.plot(x, betas)

plt.legend(["ratio", "beta", "alpha"])
plt.xlabel("gamma")
"""
x = np.linspace(1.1, 5, 100000)
y = np.vectorize(ratio)(x)

m = 1 << 30
a_min = -1
for a in x:
    if ratio(a) < m:
        m = ratio(a)
        a_min = a
print(f"mu min: {m:.4f}, reached for alpha = {a_min:.4f}, beta = {beta(a_min):.4f}")

plt.plot(x, y)"""
plt.show()