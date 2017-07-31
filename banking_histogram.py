import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from pdb import set_trace as st
import banking

bb = banking.bank()

def banking_chart(date_type, data_type_str, time_scale_str, bias=0):
  bank_data = [j for (i,j) in date_type]
  if bias == 1: # positive or negative valuation
    chart_bias = max(bank_data) + 100
  else:
    chart_bias = min(bank_data) - 100

  weeks = len(date_type)
  verts = [(-i, j) for (i, j) in zip(range(len(bank_data)), bank_data)]

  line_tos = [Path.LINETO for i in range(weeks - 1)]
  codes = [Path.MOVETO] + line_tos

  path = Path(verts, codes)

  fig = plt.figure()
  ax = fig.add_subplot(111)
  patch = patches.PathPatch(path, facecolor='none', lw=3)
  ax.add_patch(patch)
  ax.set_xlim(-weeks, 0)
  ax.set_ylim(0, chart_bias)

  plt.xlabel(time_scale_str)
  plt.ylabel(data_type_str)

# banking_chart(bb.daily_spent, 'Spent', 'Days', 0)
banking_chart(bb.weekly_spent, 'Spent', 'Weeks', 0)
banking_chart(bb.weekly_balance, 'Balance', 'Days', 1)
plt.show()