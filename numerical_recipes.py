# Herein live Numerical Recipes
import operator
import pdb

def pry(): pdb.set_trace()

def div(n, d, i=0):
  while n >= d:
    n -= d
    i += 1
  return i

def mod(n, d):
  return n - div(n, d) * d

def gcd(a, b):
  if b == 0: return a
  else: return gcd(b, a % b)

def triangle_num(xs):
  return reduce(operator.add, range(xs), 0)

def triangle_num2(xs):
  return reduce(lambda a, b: a + b, range(xs), 0)

def qsort(xs):
  if (len(xs) < 1): return []
  else:
    return qsort(less(xs[0], xs[1:])) + xs[:1] + qsort(more_eq(xs[0], xs[1:]))

def less(x, xs):
  return list(filter(lambda t: t < x, xs))

def more_eq(x, xs):
  return list(filter(lambda t: t >= x, xs))

ary = map(lambda x: 10-x, range(10))
lamb = (lambda x: x+1)(2)

# print triangle_num(5)
# print triangle_num2(3)
# print qsort(ary)
# print div(10,2)
# print mod(10,3)
print gcd(36, 9)
# pry()