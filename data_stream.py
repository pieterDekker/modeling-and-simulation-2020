from numpy.core._multiarray_umath import array

from bounding_cube import BoundingCube
from step import step_leapfrog, step_leapfrog_barnes_hut
from output import unpickle_state

def unpickle_stream(dir, nsteps):
    for i in range(nsteps):
        yield unpickle_state(i, dir)


def massless_pos_stream(x, v, a, m, ngal, np, dt, nsteps):
    # print(f'streaming for {nsteps} steps')
    for i in range(nsteps):
        # print(f'step {i}')
        x, v, a = step_leapfrog(x, v, a, m, ngal, np, dt)
        yield x


def massless_pos_vel_stream(x, v, a, m, ngal, np, dt, nsteps):
    # print(f'streaming for {nsteps} steps')
    for i in range(nsteps):
        # print(f'step {i}')
        x, v, a = step_leapfrog(x, v, a, m, ngal, np, dt)
        yield x, v

def barnes_hut_pos_stream(x, v, a, m, np, dt, nsteps, theta, max_dist):
    # print(f'streaming for {nsteps} steps')
    for i in range(nsteps):
        # print(f'step {i}')
        bounding_cube = BoundingCube(array([0, 0, 0]), 5 * max_dist)
        x, v, a, max_dist = step_leapfrog_barnes_hut(x, v, a, m, np, dt, theta, bounding_cube)
        yield x

def barnes_hut_pos_vel_stream(x, v, a, m, np, dt, nsteps, theta, max_dist):
    # print(f'streaming for {nsteps} steps')
    for i in range(nsteps):
        # print(f'step {i}')
        bounding_cube = BoundingCube(array([0, 0, 0]), 5 * max_dist)
        x, v, a, max_dist = step_leapfrog_barnes_hut(x, v, a, m, np, dt, theta, bounding_cube)
        yield x, v