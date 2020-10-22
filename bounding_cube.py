import numpy as np

class BoundingCube():
  def __init__(self, center, width) -> None:
    self.center = center
    self.width = width
  
  def get_center(self):
    return self.center
  
  def get_width(self):
    return self.width
  
  def get_subcubes(self) -> list:
    return [
      BoundingCube(self.center + np.array([x,y,z]), self.width / 2) 
      for x in [self.width/4, -self.width/4] 
      for y in [self.width/4, -self.width/4] 
      for z in [self.width/4, -self.width/4]
      ]

  def get_corners(self) -> list:
    return [
      self.center + np.array([x,y,z]) 
      for x in [self.width/2, -self.width/2] 
      for y in [self.width/2, -self.width/2] 
      for z in [self.width/2, -self.width/2]
      ]

  def __str__(self) -> str:
    return f'width: {self.width}\tcenter: {str(self.center)}'