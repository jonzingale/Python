# Herein live Numerical Recipes
import operator
import pdb

def pry(): pdb.set_trace()

def triangle_num(xs):
  ary = range(1, xs + 1)
  return reduce(operator.add, ary, 0)

def triangle_num2(xs):
  ary = range(1, xs + 1)
  return reduce(lambda a, b: a + b, ary, 0)


def qsort(xs):
  if (len(xs) < 1):
    return []
  else:
    return qsort(less(xs[0], xs[1:])) + xs[:1] + qsort(more_eq(xs[0], xs[1:]))


def less(x, xs):
  return list(filter(lambda t: t < x, xs))

def more_eq(x, xs):
  return list(filter(lambda t: t >= x, xs))


ary=map(lambda x: 10-x, range(1,11))

print triangle_num(5)
print triangle_num2(3)
print qsort(ary)
