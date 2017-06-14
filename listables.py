import operator
import pdb

def pry(): pdb.set_trace()

def to_a(rs):
  accum = []
  for i in rs: accum.append(i)
  return accum

def reduce(opr, ls, base):
  for i in ls: base = opr(base, i)
  return base

trinum = reduce(operator.add, to_a(range(4)), 0)
