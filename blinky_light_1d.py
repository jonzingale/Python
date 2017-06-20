from random import *
from pdb import set_trace
from time import sleep

# perhaps use bitstrings.
class Blinky():
  def __init__(self):
    self.seed_state()

  def seed_state(self):
    self.state = []
    for i in range(60):
      self.state.append(randint(0,1))

  def apply_rule(self, ury):
    # [000, 001, 010, 011, 100, 101, 110, 111]
    if [0,0,0] == ury: return(0)
    elif [0,0,1] == ury: return(1)
    elif [0,1,0] == ury: return(0)
    elif [0,1,1] == ury: return(1)
    elif [1,0,0] == ury: return(1)
    elif [1,0,1] == ury: return(1)
    elif [1,1,0] == ury: return(1)
    elif [1,1,1] == ury: return(0)
    else : None

  def get_neighbors(self):
    state_len = len(self.state) - 1  
    ns = []
    for i in range(1, state_len): ns.append(self.state[i-1:i+2])
    self.neighborhoods = ns

  def blink(self):
    new_state = self.state[:1]
    self.get_neighbors()

    for ury in self.neighborhoods:
      cell = self.apply_rule(ury)
      new_state.append(cell)
    self.state = new_state + self.state[-1:]

  def ppblink(self):
    str = ''
    for i in self.state:
      if i == 0: str += ' '
      else: str += '*'
    print(str)

it = Blinky()

for i in range(10**2):
  it.blink()
  it.ppblink()
  sleep(0.1)