from math import sqrt
from numpy import subtract, dot


def get_acceleration(x, a, m, ngal, np):
    for i in range(np):
        a[i] = [0, 0, 0]
        for j in range(ngal):
            if i is not j:
                dx = subtract(x[i], x[j])
                r2 = dot(dx, dx)
                r = sqrt(r2)
                a[i] = a[i] - m[j] * dx / (r ** 3)
    return a
