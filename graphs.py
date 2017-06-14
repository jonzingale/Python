from listables import reduce
from operator import add, mul, mod, pow

import pdb

# recursive HH
def havelhakimi(xs):
  if len(xs) == 1:
    return (0 == xs[0])
  else:
    (head, tail) = xs[0], xs[1:]
    mlist = list(map(lambda x: x-1, tail[:head]))
    tlist = mlist + tail[head:]
    return havelhakimi(qsort(tlist))

def qsort(xs):
  if (len(xs) < 1): return []
  else:
    return qsort(less(xs[0], xs[1:])) + xs[:1] + qsort(more_eq(xs[0], xs[1:]))

def less(x, xs):
  return list(filter(lambda t: t < x, xs))

def more_eq(x, xs):
  return list(filter(lambda t: t >= x, xs))

print(havelhakimi([2,3,4,3,2]))

