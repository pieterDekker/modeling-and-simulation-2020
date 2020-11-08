from math import inf, sqrt
from numpy import subtract, dot, array, zeros
from octree import Octree
from bounding_cube import BoundingCube


def step_leapfrog(x, v, a, m, ngal, np, dt):
    for i in range(np):
        v[i] = v[i] + (0.5 * dt * a[i])
        x[i] = x[i] + (dt * v[i])
        a[i] = [0, 0, 0]
        for j in range(ngal):
            if i is not j:
                dx = subtract(x[i], x[j])
                r2 = dot(dx, dx)
                r = sqrt(r2)
                a[i] = a[i] - m[j] * dx / (r ** 3)
        v[i] = v[i] + (0.5 * dt * a[i])
    return x, v, a


def step_leapfrog_barnes_hut(x, v, a, m, np, dt, theta, bounding_cube: BoundingCube):
    ot = Octree(bounding_cube)
    max_dim = -inf
    for i in range(np):
        ot.add_object(x[i], m[i])
    for i in range(np):
        v[i] = v[i] + (0.5 * dt * a[i])
        x[i] = x[i] + (dt * v[i])
        a[i] = [0, 0, 0]
        max_dim = max(max_dim, max(abs(x[i])))
        points_masses = zip(*ot.get_points_masses(x[i], theta))
        for point, mass in points_masses:
            dx = subtract(x[i], point)
            r2 = dot(dx, dx)
            r = sqrt(r2)
            if r == 0.0:
                continue
            a[i] = a[i] - mass * dx / (r ** 3)
        v[i] = v[i] + (0.5 * dt * a[i])
    return x, v, a, max_dim
