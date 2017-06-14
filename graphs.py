from listables import reduce
from operator import add, mul, mod, pow

import pdb
# Haskell:
# havelhakimi :: [Int] -> Bool
# havelhakimi (a:[]) = a == 0
# havelhakimi (a:as) = havelhakimi.qsort $ 
#   map (+ (-1)) (take a as) ++ drop a as


# recursive HH
def havelhakimi(xs):
  if len(xs) == 1:
    return (0 == xs[0]) # print works why not return?
  else:
    (head, tail) = xs[0], xs[1:]
    mlist = list(map(lambda x: x-1, tail[:head]))
    tlist = mlist + tail[head:]
    havelhakimi(qsort(tlist))


def qsort(xs):
  if (len(xs) < 1): return []
  else:
    return qsort(less(xs[0], xs[1:])) + xs[:1] + qsort(more_eq(xs[0], xs[1:]))

def less(x, xs):
  return list(filter(lambda t: t < x, xs))

def more_eq(x, xs):
  return list(filter(lambda t: t >= x, xs))

it = havelhakimi([2,3,4,3,2])
print(it)

