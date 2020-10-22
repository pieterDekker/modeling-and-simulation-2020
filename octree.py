import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt
from bounding_cube import BoundingCube

class Octree():
  def __init__(self, bcube) -> None:
    self._bcube = bcube
    self._children = []
    self._com = 0
    self._mass = 0
  
  def add_object(self, position, mass):
    if self._mass == 0:
      self._com = position
      self._mass = mass

if __name__ == "__main__":
  def plot_bc(bc, ax, c, alph = 1):
    for s, e in combinations(bc.get_corners(), 2):
      if np.abs(np.sum(np.abs(s-e)) - bc.width) < 0.005:
        ax.plot3D(*zip(s, e), color=c, alpha=alph)
  
  fig = plt.figure()
  ax = fig.gca(projection='3d')

  bc = BoundingCube(np.array([0,0,0]), 2)
  plot_bc(bc, ax, 'b')
  for subbc in bc.get_subcubes():
    plot_bc(subbc, ax, 'r', 0.5)

  plt.show()