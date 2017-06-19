# from operator import add, mul, mod, pow
from operator import *
import pdb

def pry(): pdb.set_trace()

def reduce(opr, ls, base):
  for i in ls: base = opr(base, i)
  return base

# Shuffling #
def key_shuffle(deck):
  size = len(deck)
  zipped = list(zip(rands(size), deck))
  zipped.sort()
  return list(zip(*zipped))[1]

def rands(n):
  ary = []
  logn = math.log(n**3,2)
  for i in range(n):
    ary.append(getrandbits(math.floor(logn)))
  return ary
