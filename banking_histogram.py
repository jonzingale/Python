import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from pdb import set_trace as st
import banking

bb = banking.bank()

def gen_spent_chart(spent_type, spent_type_str):
  spents = [j for (i,j) in spent_type]
  max_spent = min(spents) - 20
  weeks = len(spent_type)

  verts = [(-i, j) for (i, j) in zip(range(len(spents)), spents)]

  line_tos = [Path.LINETO for i in range(weeks - 1)]
  codes = [Path.MOVETO] + line_tos

  path = Path(verts, codes)

  fig = plt.figure()
  ax = fig.add_subplot(111)
  patch = patches.PathPatch(path, facecolor='none', lw=3)
  ax.add_patch(patch)
  ax.set_xlim(-weeks, 0)
  ax.set_ylim(0, max_spent)

  plt.xlabel(spent_type_str)
  plt.ylabel('Spent')

  plt.show()

# gen_spent_chart(bb.daily_spent, 'Days')
gen_spent_chart(bb.weekly_spent, 'Weeks')