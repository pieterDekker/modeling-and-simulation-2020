from functools import reduce
from math import cos, pi, pow, radians, sin, sqrt
from random import random
import numpy
from numpy.core.fromnumeric import shape

def jitt():
  return ((random() -0.5) * 2) / 1000

def initialize(masses, eccentricities, rmin, thetadeg, nrings, ninner, ring_spacing, ngal, np, maxp, outdir):
  """
  Initializes the simulation

  Parameters
  ----------
  masses : list
    The masses of each galaxy
  eccentricities : list
    the eccentricites of the orbits of each galaxy
  rmin : int
    The minimum separation in kiloparsecs  (> 30 recommended) ?? what is this in physics ??
  thetadeg : list
    The inclination angles of each galaxy in degrees
  nrings : list
    The number of rings of each galaxy
  ninner : list
    The number of particles on the inner ring of each galaxy
  ring_spacing : list
    The distance in kiloparsecs between each ring of each galaxy
  ngal : int
    The number of galaxies
  maxp : int
    The maximum number of particles
  """
  # Initialize positions to zeros
  positions = numpy.zeros(shape=(maxp,3))
  # Initialize velocities to zeros
  velocities = numpy.zeros(shape=(maxp,3))
  # TODO: initialize masses
  # TODO: add G

  # convert inclination angles to degrees
  inclination_angles = [radians(theta_degree) for theta_degree in thetadeg] # incliniation = theta in f90

  # compute semi-major axis ?? see https://en.wikipedia.org/wiki/Apsis
  semi_major_axes = [rmin / (1 - eccentricity) for eccentricity in eccentricities] # semi_major_axes = a in f90

  # compute apastron distances
  apastron_distances = [semi_major_axis * (1 + eccentricity) for (semi_major_axis, eccentricity) in zip(semi_major_axes, eccentricities)] # apostron distances = r in f90

  # galaxy at positions[0] is the center, so we don't update its position.
  # galaxy at velocities[0] is motionless, so we don't update its velocity.
  for i in range(1, ngal):
    total_mass = masses[0] + masses[i]
    positions[i][i-1] = apastron_distances[i-1]
    v0 = sqrt(semi_major_axes[i-1] * (1-pow(eccentricities[i-1], 2)) * total_mass) / apastron_distances[i-1]
    velocities[i][i % 3] = v0
  
  
  np = ngal
  # create galaxies
  for i in range(ngal):
    positions, velocities, np = create_galaxy(positions, velocities, np, maxp, positions[i], velocities[i], masses[i], inclination_angles[i], nrings[i], ninner[i], ring_spacing[i])
  print('set up {} particles'.format(np))
  return positions, velocities, np

def create_galaxy(positions, velocities, np, maxp, x0, v0, m0, theta, nrings, ninner, ring_spacing):
  """Creata a galaxy and at its data to the appropriate vectors

  Args:
      positions (list):  a nx3 list of positions
      velocities (list): an nx3 list of velocities
      np (int): the total number of particles
      maxp (int): the maximum number of particles
      x0 (list): a 1x3 list of the initial position
      v0 (list): a 1x3 list of the initial velocity
      m0 (int): the mass
      theta (float): the inclincation angle in radians
      nrings (int): the amount of rings
      ninner (int): the amount of particles on the inner ring
      ring_spacing (int): the space between rings in kpc
  """
  for j in range(nrings):
    ring_radius = (j + 1) * ring_spacing
    nphi = ninner + (ninner / 2) * j # number of particles per ring
    vphi = sqrt(m0/ring_radius)
    dphi = 2 * pi / nphi
    for i in range(int(nphi)):
      phi = i * dphi
      if (np > maxp):
        print("np > maxp: need bigger maxp")
      dx = [
        ring_radius * cos(phi) * cos(theta),
        ring_radius * sin(phi),
        -1 * ring_radius * cos(phi) * sin(theta)
      ]
      position = [px0 + pdx + jitt() for (px0, pdx) in zip(x0, dx)]
      positions[np] = position
      dv = [
        -1 * vphi * sin(phi) * cos(theta),
        vphi * cos(phi), 
        vphi * sin(phi)*sin(theta)
      ]
      velocity = [pv0 + pdv for (pv0, pdv) in zip(v0, dv)]
      velocities[np][:] = velocity
      np += 1 # count the total number of particles
  return positions, velocities, np