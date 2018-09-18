import matplotlib.pyplot as plt
import numpy as np
from pdb import set_trace as st

# fig = plt.figure()  # an empty figure with no axes
# fig.suptitle('No axes on this figure')  # Add a title so we know which it is

# fig, ax_lst = plt.subplots(2, 2)  # a figure with a 2x2 grid of Axes


x = np.linspace(0, 2, 100)

plt.plot(x, x, label='linear')
plt.plot(x, x**2, label='quadratic')
plt.plot(x, x**3, label='cubic')

plt.xlabel('x label')
plt.ylabel('y label')

plt.title("Simple Plot")

plt.legend()

plt.show()