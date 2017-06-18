# from operator import add, mul, mod, pow
from operator import *
import pdb

def pry(): pdb.set_trace()

def reduce(opr, ls, base):
  for i in ls: base = opr(base, i)
  return base
