from listables import reduce
from operator import add, mul, mod, pow

from pdb import set_trace

# recursive HH
def havelhakimi(xs):
  if len(xs) == 1:
    return (0 == xs[0])
  else:
    (head, tail) = xs[0], xs[1:]
    mlist = list(map(lambda x: x-1, tail[:head]))
    mlist += tail[head:]
    return havelhakimi(sorted(mlist))

print(havelhakimi([2,3,4,3,2])) # no Erdos graphs
print(havelhakimi([2,1,1])) # yes Erdos graphs


# set_trace()
# import timeit
# print(timeit.timeit("havelhakimi([2,3,4,3,2])",
#                     setup="from __main__ import havelhakimi",
#                     number=10**5))