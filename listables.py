from operator import add, mul, mod, pow
import pdb

def pry(): pdb.set_trace()

def reduce(opr, ls, base):
  for i in ls: base = opr(base, i)
  return base
