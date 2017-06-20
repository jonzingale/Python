from random import *
from pdb import set_trace
from time import sleep

SEEDS = [[0] * 30 + [1,1] + [0] * 30, None]

class Blinky():
  def __init__(self, seed=None, rule=90):
    if seed is None: self.seed_state()
    else: self.state = seed
    self.rule = self.to_binary(rule)

  def seed_state(self):
    self.state = []
    for i in range(150): # set number of columns.
      self.state.append(randint(0,1))

  def to_binary(self, num, ary=[]):
    num = num % 256 # ensure rule range.
    while num > 0:
      ary.insert(0, num % 2)
      num //= 2
    while len(ary) < 8: ary.insert(0,0)
    return ary

  def to_decimal(self, bry, num=0):
    for i in range(0,len(bry)):
      num += (2**i * bry.pop())
    return num

  def apply_rule(self, ury):
    rule_hash = {}
    val = self.to_decimal(ury)
    for i in range(0,8):
      rule_hash.update({i: self.rule[i]})

    return(rule_hash[val])

  def get_neighbors(self):
    state_len, ns = len(self.state) - 1, []
    for i in range(1, state_len): ns.append(self.state[i-1:i+2])
    self.neighborhoods = ns

  def blink(self):
    new_state = self.state[:1]
    self.get_neighbors()

    for ury in self.neighborhoods:
      cell = self.apply_rule(ury)
      new_state.append(cell)
    self.state = new_state + self.state[-1:]

  def ppblink(self, str=''):
    for i in self.state:
      if i == 0: str += ' '
      else: str += '*'
    print(str)

# Execute example automata:
rand_rule = SEEDS[randint(0,1)]
it = Blinky(rand_rule, 90)

for i in range(10**2):
  it.blink()
  it.ppblink()
  sleep(0.1)
