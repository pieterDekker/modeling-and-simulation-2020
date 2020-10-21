from math import floor, log

from numpy import zeros
from step import step_leapfrog
from init import initialize
from potentials import get_acceleration
from mpl_toolkits.mplot3d import Axes3D
import cProfile
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from output import write_params, write_state

def main():
  # TODO: obtain through input
  dt = 0.05 # default = 0.01
  dtout = 10 # default = 10
  tmax = 50 # default = 5000

  nsteps = floor(tmax / dt)
  nout = round(dtout / dt)

  ring_spacing = [] # ring spacing
  e = [] # eccentricities
  m = [] # masses
  ninner = [] # number of particles on innermost rings
  nrings = [] # number of rins
  thetadeg = [] # inclination angles in degrees
  a = [] # accellerations
  v = [] # velocities
  x = [] # positions
  maxp = 10000 # maximum number of particles
  ngal = 0 # number of galaxies
  np = 0 # number of particles
  outdir = './output'
  rmin = 0

  #######
  # DEFAULTS
  print('using defaults')
  ngal = 2
  m = [10,10]
  e = [0,0]
  rmin = 40
  thetadeg = [0, 0]
  nrings = [5, 5]
  ninner = [100, 100]
  ring_spacing = [10, 10]
  #######

  while not 1 <= ngal <= 4:
    ngal = int(input('Enter the number of galaxies: ').strip())

  while len(m) != ngal:
    m = list(map(lambda x: int(x), input('please enter {} masses, separated by spaces: '.format(ngal)).strip().split(' ')))

  while len(e) != ngal:
    e = list(map(lambda x: float(x), input('please enter {} eccentricities, separated by spaces: '.format(ngal)).strip().split(' ')))

  while rmin <= 0:
    rmin = int(input('Enter the minimum separation: ').strip())

  while len(thetadeg) != ngal:
    thetadeg = list(map(lambda x: float(x), input('please enter {} inclination angels in degrees, separated by spaces: '.format(ngal)).strip().split(' ')))

  while len(nrings) != ngal:
    nrings = list(map(lambda x: float(x), input('please enter {} numbers of rings, separated by spaces: '.format(ngal)).strip().split(' ')))

  while len(ninner) != ngal:
    ninner = list(map(lambda x: float(x), input('please enter {} numbers of particles on the inner rings, separated by spaces: '.format(ngal)).strip().split(' ')))

  while len(ring_spacing) != ngal:
    ring_spacing = list(map(lambda x: float(x), input('please enter {} ring spacings, separated by spaces (kpc): '.format(ngal)).strip().split(' ')))  

  print('initializing...')
  x, v, maxes = initialize(m, e, rmin, thetadeg, nrings, ninner, ring_spacing, ngal, maxp)
  print(a[:5])
  print('setting initial accellerations...')
  a = zeros(shape=(maxp,3))
  a = get_acceleration(x, a, m, ngal, maxp)
  print(a[:5])

  print('performing {} steps'.format(nsteps))
  for i in range(nsteps):
    x, v, a = step_leapfrog(x,v,a,m, ngal, np, dt)
    

if __name__ == '__main__':
  main()