import pdb

def pry(): pdb.set_trace()

class Pizza(object):
  def __init__(self, size):
      self.size = size
  def get_size(self):
      return self.size

it = Pizza(45)
Pizza.get_size(it)

# Some lambdas
one = filter(lambda s: s == Pizza.get_size(it), range(100))
two = lambda pair: pair[0] + pair[1]
thr = lambda s, t: s + t

pry()