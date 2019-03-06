# Parsing Sarahs Chemistry Data.
from pdb import set_trace as st
import matplotlib.pyplot as plt

from matplotlib.path import Path
import matplotlib.patches as patches

import numpy as np

# Parse Excel as CSV
import xlrd
import csv

def csv_from_excel():
    wb = xlrd.open_workbook('chem_data.xlsx')
    sh = wb.sheet_by_name('Sheet1')
    chemCsv = open('chem_data.csv', 'w')
    wr = csv.writer(chemCsv, quoting=csv.QUOTE_ALL)
    ary = []
    for rownum in range(sh.nrows):
      [x, y, *cs] = sh.row_values(rownum)
      ary.append([x,y])
      wr.writerow([x,y])

    chemCsv.close()
    return(ary[3:])

def parse_excel():
    wb = xlrd.open_workbook('chem_data.xlsx')
    sh = wb.sheet_by_name('Sheet1')
    ary, bry = [], []

    for rownum in range(sh.nrows):
      [x, y, *cs] = sh.row_values(rownum)
      ary.append([x,y])

    for [x,y] in ary[3:]:
      if (x==''): break
      bry.append([float(x),float(y)])

    return(bry)

# Begin Data Display
fig = plt.figure(figsize=(9, 9))
epsilon = 0.0000000001

def dxdt(data):
  ary = []
  for ([x1,y1],[x2,y2]) in zip(data, data[1:]):
    if (x1 == x2): dx = epsilon
    else: dx = x1 - x2
    ary.append([x1, (y1-y2)/dx])
  return(ary)

def displayData(data, grid):
  for cs in data:
    ax = fig.add_subplot(grid)
    plt.plot(*cs, 'bo', markersize=1.5)

def displayData2(data, grid, yliml=0, ylimh=13):
  line_tos = [Path.LINETO for i in range(len(data)-1)]
  codes = [Path.MOVETO] + line_tos
  path = Path(data)
  ax = fig.add_subplot(grid)
  patch = patches.PathPatch(path, facecolor='none', lw=1)
  ax.add_patch(patch)
  ax.set_xlim(0, 20)
  ax.set_ylim(yliml, ylimh)

data = parse_excel()
displayData2(data, 221)
displayData2(dxdt(data), 222)
displayData(dxdt(dxdt(data)), 224)
displayData2(dxdt(dxdt(data)), 223, -300, 300)
plt.show()


