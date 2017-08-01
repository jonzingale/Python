import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from pdb import set_trace as st
import numpy as np
import banking

bb = banking.bank()
fig = plt.figure(figsize=(17, 8))

def banking_chart(date_type, data_type_str, time_scale_str, bias=0, subplot=111):
  bank_data = [j for (i,j) in date_type]
  if bias == 1: # positive or negative valuation
    chart_bias = max(bank_data) + 100
  else:
    chart_bias = min(bank_data) - 100

  weeks = len(date_type)
  verts = [(-i, j) for (i, j) in zip(range(len(bank_data)), bank_data)]

  line_tos = [Path.LINETO for i in range(weeks - 1)]
  codes = [Path.MOVETO] + line_tos

  path = Path(verts[0::1], codes[0::1]) # bi-weekly [0::2]
  ax = fig.add_subplot(subplot)

  patch = patches.PathPatch(path, facecolor='none', lw=3)
  ax.add_patch(patch)

  # spending goal line technology:
  if data_type_str == 'Spent':
    x = np.linspace(1-weeks, 0, num=2)
    y = [-219.5, -219.5]
    plt.plot(x, y)

  ax.set_xlim(-weeks, 0)
  ax.set_ylim(0, chart_bias)

  plt.xlabel(time_scale_str)
  plt.ylabel(data_type_str)

# Todo: make all daily, and use slice [::] to scale.
# banking_chart(bb.daily_spent, 'Spent', 'Days', 0)
banking_chart(bb.weekly_spent, 'Spent', 'Weeks', 0, 121)
banking_chart(bb.weekly_balance, 'Balance', 'Weeks', 1, 122)

plt.show()

