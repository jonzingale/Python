# Herein live methods for Summing.
from listables import reduce
from operator import add, mul, mod, pow
import pdb

def dot_prod(xs, ys):
  return sum(map(mul, xs, ys))

def trinum(n):
  return reduce(add, range(n+1), 0)

def tetranum(n):
  return sum(map(lambda x: reduce(add, range(x+1), 0), range(n+1)))

print(dot_prod([1,2,3],[3,4,5]))
print(tetranum(5))
print(trinum(5))
