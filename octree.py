from typing import List
import numpy as np
from bounding_cube import BoundingCube
import graphviz
import uuid
from itertools import starmap
from table import Table
from math import sqrt

MAX_OBJECTS = 2

class Octree():
  def __init__(self, bcube) -> None:
    self._bcube = bcube
    self._children = []
    self._objects =[]
    self._com = 0
    self._mass = 0
  
  def get_appropriate_child_idx(self, point):
    return sum(np.array([4,2,1])[(point - self.get_bcube().get_center()) < 0])

  def get_com(self):
    return self._com

  def get_mass(self):
    return self._mass

  def get_bcube(self) -> BoundingCube:
    return self._bcube

  def get_children(self):
    return self._children
  
  def get_objects(self):
    return self._objects

  def subdivide(self):
    # Create sub octrees
    for subbcube in self.get_bcube().get_subcubes():
      self.get_children().append(Octree(subbcube))
    # Add objects to appropriate sub octrees
    for (position, mass) in self._objects:
      idx = self.get_appropriate_child_idx(position)
      self.get_children()[idx].add_object(position, mass)
    # Remove objects, update com
    self._objects = []
    self._com = self.calculate_com()
  
  def count_objects(self, position, mass):
    count = 0
    for o in self._objects:
      if np.all(o[0] == position) and o[1] == mass:
        count += 1
    return count

  def get_points_masses(self, point, theta):
    d = sqrt(sum((self.get_com() - point) ** 2))
    print(f'the ratio at {self.get_com()} s/d={self.get_bcube().get_width()/d}')
    if len(self.get_children()) == 0:
      print('have no children, directly returning objects')
      points, masses = zip(*self.get_objects())
      return list(points), list(masses)
    if self.get_bcube().get_width() / d < theta:
      print('cube is sufficiently far away, returning com')
      return [self.get_com()], [self.get_mass()]
    else:
      print('cube is close enough, get objects from children')
      points = []
      masses = []
      for child in self.get_children():
        child_points, child_masses = child.get_points_masses(point, theta)
        points += child_points
        masses += child_masses
      return points, masses

  def add_object(self, position, mass):
    if not self.get_bcube().contains(position):
      raise Exception(f'Error, point {list(position)} falls outside bounding cube at {list(self.get_bcube().get_center())} with width {self.get_bcube().get_width()}')
    
    if len(self._objects) == MAX_OBJECTS:
      if self.count_objects(position, mass) >= MAX_OBJECTS - 1:
        raise Exception(f'Too many duplicates of {(position, mass)}')
      self.subdivide()
    
    self._mass += mass
    if len(self.get_children()) > 0:
      idx = self.get_appropriate_child_idx(position)
      self.get_children()[idx].add_object(position, mass)
    else:
      self._objects.append((position, mass))
    self._com = self.calculate_com()
  
  def calculate_com(self):
    if len(self.get_children()) > 0:
      com = sum(list(map(lambda x: x.get_com() * x.get_mass(), self.get_children()))) / self._mass
    else:
      com = sum(list(starmap(lambda pos, m: pos * m, self._objects))) / self._mass
    return com

  def render_graph(self):
    dot = graphviz.Digraph(comment='The Octree')
    dot = self.render_graph_rec(dot)
    dot.render('test-output/round-table.gv', view=True)
  
  def render_graph_rec(self, dot):
    dot.node(str(self.get_bcube().get_center()), self.get_node_table().get_gv_html())
    if len(self.get_children()) > 0:
      for c in self.get_children():
        dot.edge(str(self.get_bcube().get_center()), str(c.get_bcube().get_center()))
        dot = c.render_graph_rec(dot)
    else:
      id = str(uuid.uuid1())
      if len(self._objects) > 0:
        label = self.get_object_table().get_gv_html()
      else:
        label = '\<empty\>'
      dot.node(id, label=label, _attributes={'shape': 'box'})
      dot.edge(str(self.get_bcube().get_center()), id)
    return dot

  def get_object_table(self):
    t = Table()
    t.set_header('Pos.', 'Mass')
    for o in self._objects:
      t.add_row(list(o[0]), o[1])
    return t

  def get_node_table(self):
    t = Table()
    t.set_header('COM', 'Mass')
    t.add_row(self.get_com(), self.get_mass())
    return t

if __name__ == "__main__":
  ot = Octree(BoundingCube(np.array([0,0,0]), 4))
  points = [np.array([x,y,z]) for x in [1,-1] for y in [1,-1] for z in [1,-1]]
  for p, idx in zip(points, range(1,len(points) + 1)):
    ot.add_object(p, idx)
  for p, idx in zip(points, range(1,len(points) + 1)):
    ot.add_object(p, idx)
  ot.add_object(np.array([1,2,1]), 20)
  ot.render_graph()
  print(ot.get_points_masses(np.array([0,0,0]), 1))
