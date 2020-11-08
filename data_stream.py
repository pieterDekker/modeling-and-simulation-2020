from numpy import array

from bounding_cube import BoundingCube
from step import step_leapfrog, step_leapfrog_barnes_hut
from output import unpickle_state


def unpickle_stream(dir, nsteps):
    for i in range(nsteps):
        yield unpickle_state(i, dir)


def massless_stream(x, v, a, m, ngal, np, dt, nsteps):
    for i in range(nsteps):
        x, v, a = step_leapfrog(x, v, a, m, ngal, np, dt)
        yield x


def barnes_pos_stream(x, v, a, m, np, dt, nsteps, theta, max_dist):
    for i in range(nsteps):
        bounding_cube = BoundingCube(array([0, 0, 0]), 5 * max_dist)
        x, v, a, max_dist = step_leapfrog_barnes_hut(x, v, a, m, np, dt, theta, bounding_cube)
        yield x
