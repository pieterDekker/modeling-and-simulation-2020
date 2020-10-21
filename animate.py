from math import floor
import os
from numpy import zeros

from step import step_leapfrog
from init import initialize, initialize_masses
from potentials import get_acceleration
from animated_scatter import AnimatedScatter

import argparse
import json

def data_stream(x, v, a, m, ngal, np, dt, nsteps):
  for i in range(nsteps):
    x,v,a = step_leapfrog(x, v, a, m, ngal, np, dt)
    yield x

def expectedParticles(ngal, ninner, nrings):
  ep = 0
  for i in range(ngal):
    p = ninner[i]
    n = nrings[i]
    ep += p * (n + (n * (n - 1) / 4))
  ep += ngal
  return int(ep)

def main():
  # TODO: obtain through input
  dt = 0.05 # default = 0.01
  dtout = 10 # default = 10
  tmax = 1000 # default = 5000

  nsteps = floor(tmax / dt)
  nout = round(dtout / dt)
  write_output = False
  outdir = ''

  ap = argparse.ArgumentParser(description='Simulate N bodies')
  ap.add_argument('file')
  ap.add_argument('-o', '--output-dir')
  args = ap.parse_args()
  with open(args.file, 'r') as f:
    params = json.load(f)
    ngal = params['ngal']
    m = params['m']
    e = params['e']
    rmin = params['rmin']
    ring_spacing = params['ring_spacing']
    thetadeg = params['thetadeg']
    nrings = params['nrings']
    ninner = params['ninner']
    if 'output_dir' in params:
      outdir = params['output_dir']
      write_output = True

  n_particles = expectedParticles(ngal, ninner, nrings)

  m = initialize_masses(m, n_particles)

  x, v, maxes = initialize(m, e, rmin, thetadeg, nrings, ninner, ring_spacing, ngal, n_particles)
  a = zeros(shape=(n_particles,3))
  a = get_acceleration(x, a, m, ngal, n_particles)

  anim = AnimatedScatter(data_stream(x, v, a, m, ngal, n_particles, dt, nsteps), 1.01 * max(maxes), ngal, 500, os.path.join(os.getcwd(), 'test_output'))

if __name__ == '__main__':
  main()