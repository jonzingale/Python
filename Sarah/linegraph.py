import matplotlib.pyplot as plt
from pdb import set_trace as st
import numpy as np

def graphLines():
  x = np.linspace(0, 2, 100)
  plt.plot(x, x, label='linear')
  plt.plot(x, x**2, label='quadratic')
  plt.plot(x, x**3, label='cubic')
  plt.xlabel('x label')
  plt.ylabel('y label')
  plt.title("Simple Plot")
  plt.legend()
  plt.show()

def barGraph():
  x = np.linspace(0, 15, 10)
  plt.bar(x, x**2, label='quadratic')
  plt.xlabel('x label')
  plt.ylabel('y label')
  plt.title("Simple Bar")
  plt.legend()
  plt.show()

# How would I make this better?
def table():
  plt.table(cellText="this dude")
  plt.title("An Excel Table?")
  plt.show()

# Can I use eval or something like
# it to typeset the latex?

# st()
