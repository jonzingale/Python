# Herein live Numerical Recipes
import operator
import pdb

def pry(): pdb.set_trace()

def triangle_num(xs):
  ary = range(1, xs + 1)
  return reduce(operator.add, ary, 0)

def triangle_num2(xs):
  ary = range(1, xs + 1)
  return reduce(lambda a, b: a+b, ary, 0)

# pry()
print triangle_num(5)
print triangle_num2(3)
