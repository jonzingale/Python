import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from pdb import set_trace as st
import numpy as np
# import banking
import gcuBanking

# bb = banking.bank()
bb = gcuBanking.bank()
fig = plt.figure(figsize=(17, 8))

def banking_chart(date_type, data_type_str, time_scale_str,
                  bias=0, subplot=111):

  bank_data = [j for (i,j) in date_type]

  # positive or negative valuation
  chart_bias = [min(bank_data) - 100, max(bank_data) + 100][bias]

  weeks = len(date_type)
  verts = [(-i, j) for (i, j) in zip(range(len(bank_data)), bank_data)]

  line_tos = [Path.LINETO for i in range(weeks - 1)]
  codes = [Path.MOVETO] + line_tos

  # path = Path(verts[0::1], codes[0::1]) # bi-monthly [0::2]
  path = Path(verts[0::1], codes[0::1])
  ax = fig.add_subplot(subplot)

  patch = patches.PathPatch(path, facecolor='none', lw=3)
  ax.add_patch(patch)

  # spending goal line technology:
  weekly_budget = 500
  if data_type_str == 'Spent':
    x = np.linspace(1-weeks, 0, num=2)
    y = [-weekly_budget, -weekly_budget]
    plt.plot(x, y)

  ax.set_xlim(-weeks, 0)
  ax.set_ylim(0, chart_bias)

  plt.xlabel(time_scale_str)
  plt.ylabel(data_type_str)

banking_chart(bb.daily_spent, 'Spent', 'Days', 0, 121)
banking_chart(bb.daily_balance, 'Balance', 'Days', 1, 122)

# banking_chart(bb.weekly_spent, 'Spent', 'Weeks', 0, 121)
# banking_chart(bb.weekly_balance, 'Balance', 'Weeks', 1, 122)

plt.show()

