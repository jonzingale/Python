# from listables import reduce
# from operator import add, mul, mod, pow

from pdb import set_trace as st


# TODO:
# import Springrank functionality.
# write CSV importer for springRank.
#   - csv to springRank functionality.
# import scipy or numpy stats functionality.
#   - Matrix: spectra, eigenvalues, etc ..
#   - Stats: ChiSqr . . 

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

class Blinky(): # THIS IS HERE FOR REFERENCE.
  def __init__(self, seed=None, rule=90):
    if seed is None: self.seed_state()
    else: self.state = seed
    self.rule = self.to_binary(rule)

  def seed_state(self):
    self.state = []
    for i in range(150): # set number of columns.
      self.state.append(randint(0,1))


# set_trace()
# import timeit
# print(timeit.timeit("havelhakimi([2,3,4,3,2])",
#                     setup="from __main__ import havelhakimi",
#                     number=10**5))