# Herein live Numerical Recipes
from listables import reduce
from operator import add
from pdb import set_trace
from random import *

def div(n, d, i=0):
  while n >= d:
    n -= d
    i += 1
  return i

def mod(n, d):
  return n - div(n, d) * d

def gcd(a, b):
  if b == 0: return a
  else: return gcd(b, a % b)

def triangle_num(n):
  return reduce(add, range(n), 0)

def triangle_num2(n):
  return reduce(lambda a, b: a + b, range(n), 0)

def qsort(xs):
  if (len(xs) < 1): return []
  else:
    return qsort(less(xs[0], xs[1:])) + xs[:1] + qsort(more_eq(xs[0], xs[1:]))

def less(x, xs):
  return list(filter(lambda t: t < x, xs))

def more_eq(x, xs):
  return list(filter(lambda t: t >= x, xs))

ary = list(map(lambda x: 10-x, range(10)))
lamb = (lambda x: x+1)(2)

ls = [triangle_num(5),triangle_num2(3),qsort(ary),div(10,2),mod(10,3)]
for i in ls: print(i)

# PYTHAGOREAN TRIPLES
def rand_triple():
  ss = randint(1, 10**3)
  rr = randint(1, ss)
  if ss + rr % 2 == 0: ss += 1  
  a = ss**2 - rr**2 
  b = 2*rr*ss
  c = rr**2 + ss**2
  return([a,b,c])

def test_triple(ary):
  a, b, c = ary
  print(a**2 + b**2 == c**2)

test_triple(rand_triple())











