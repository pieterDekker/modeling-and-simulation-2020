from math import sqrt
from numpy import subtract, dot

def get_acceleration(x, a, m,ngal,np):
  for i in range(np):
    a[i] = [0,0,0]
    for j in range(ngal):
      if i is not j:
        dx = subtract(x[i], x[j])
        r2 = dot(dx, dx)
        r = sqrt(r2)
        a[i] = a[i] -m[j] * dx / (r ** 3) # (4.2) on page 37 of Celestial Mechanics
  return a

def get_potential(x,m,ngal,np):
  potential = 0
  for i in range(ngal):
    phi = 0
    for j in range(i + 1, ngal):
      dx = [pos_i - pos_j for (pos_i, pos_j) in zip(x[i], x[j])]
      r2 = [pdx * pdx for pdx in dx]
      r = sqrt(r2)
      phi = phi - m[j] / r
    potential = potential + m[i] * phi
