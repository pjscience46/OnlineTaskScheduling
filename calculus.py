from math import log, sqrt
import matplotlib.pyplot as plt
import numpy as np


def f(p):
    return (2 * log(p)) / (1 + log(p * log(p)))


MAX_RATIO = 10.0


# for p in range(1, 200):
#     print(f"f({2**p}) = {f(2**p)}")

def mu(alpha: float, beta: float) -> float:
    nom = alpha + beta + 1 - sqrt(pow(alpha + beta + 1, 2) - 4 * beta)
    return nom / (2 * beta)


print(1.0/mu(1.5, 1.42))


def ratio(x: float) -> float:
    alpha = x
    beta = (1+x)/(2 * sqrt(x))
    if alpha < 1 or beta < 1:
        return MAX_RATIO
    return min(MAX_RATIO, 1.0 / mu(alpha, beta))


x = np.linspace(1, 5, 100000)
y = np.vectorize(ratio)(x)

m = 1 << 30
x_min = -1
for el in x:
    if ratio(el) < m:
        m = ratio(el)
        x_min = el
print(f"mu min: {m}, reached for x = {x_min}")

plt.plot(x, y)
plt.show()