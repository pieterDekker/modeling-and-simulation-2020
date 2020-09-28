from potentials import get_acceleration
from math import sqrt
from numpy import subtract, dot

def step_leapfrog(x,v,a,m,ngal,np,dt):
  i = 0
  for i in range(np):
    v[i] = v[i] + (0.5 * dt * a[i])
    x[i] = x[i] + (dt * v[i])
    a[i] = [0,0,0]
    for j in range(ngal):
      if i is not j:
        dx = subtract(x[i],x[j])
        r2 = dot(dx, dx)
        r = sqrt(r2)
        a[i] = a[i] - m[j] * dx / (r**3)
    v[i] = v[i] + (0.5 * dt * a[i])
  return x, v, a
