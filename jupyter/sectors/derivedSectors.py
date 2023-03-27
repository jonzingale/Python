from pdb import set_trace as st
from sklearn.cluster import KMeans
from numpy.linalg import svd
import yfinance as yf
import numpy as np

# This module calculates kmodes from a correlation matrix
# construed as a distance matrix.

SYMS = ['AAPL','ADI','AMAT','AMZN','ASML','BRK-B','CDNS','GOOGL',
  'INTC','IQV','JNJ','LMT','MKL','NOC','NVDA','REPX','TSM','WSC']

SYMS = ['NVDA','CDNS','AAPL','ASML','NOC','AMZN','MKL','LMT','TSM','WSC','IQV',
  'GOOGL','ADI','BRK-B','JNJ','INTC','DD','ITA','UBS','SIEGY','AMAT','REPX',
  'VDE','EGLE','IX','VFC','VDC','PARA','IBM','SPG','PHG','CVX','SWN','EQT',
  'SE','LRCX','BIDU']

def dist_to_coords(vs):
  G = vs.T.dot(vs)
  U,S,_ = svd(G)
  X = U * np.sqrt(S)
  return X

# histories are alphabetized
def get_portfolio(syms, years=7):
  symStr = ' '.join(syms) # download takes a string argument
  histories = yf.download(symStr, period='%dy' % years)
  prices = histories['Adj Close'].values
  priceMatrix = np.array(prices).T
  return priceMatrix

def cluster_coordinates(syms, graph, k):
  kmeans = KMeans(k).fit(graph)
  lbls = kmeans.labels_

  clusters = {}
  for (sym, idx) in zip(syms , lbls):
    if idx in clusters.keys():
      clusters[idx].append(sym)
    else:
      clusters.update({idx: [sym]})

  return clusters

def main(syms, k=3, yrs=7):
  syms.sort()
  prices = get_portfolio(syms, yrs)

  # calculate correlations
  correlations = np.corrcoef(prices)

  # svd correlations to get coordinates
  graph = dist_to_coords(correlations)

  # cluster coordinates from graph
  clusters = cluster_coordinates(syms, graph, k)

  return clusters

# ret = main(SYMS, 15, 5)
# print(ret)
