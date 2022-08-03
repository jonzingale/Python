import pandas as pd
from pdb import set_trace as st
import re

# This file parses csvs, via pandas, into dataframes.
# data cleaning, exceptions and memo substitutions.

def getCategories(filename):
  df = pd.read_csv(filename)
  # df = df.sort_values('Memo')

  memos = {}
  for memo in df['Memo']:
    if pd.isnull(memo): break

    if re.match('WORLD SCIENTIFIC PUB HTTPSWWW.WORL', memo):
      memo = 'WORLD SCIENTIFIC'

    if re.match('AMAZON.COM SEATTLE WA AMAZON.COM\*\w+', memo):
      memo = 'AMAZON'

    memos[memo] = None

def pandaData(filename):
  df = pd.read_csv(filename)

  memos = {}
  for memo in df['Memo']:
    if pd.isnull(memo): break

    # How do I replace values in pandas?
    if re.match('Prime Video.+', memo):
      df['Memo'][memo] = 'Prime Video'

    if re.match('WORLD SCIENTIFIC PUB HTTPSWWW.WORL', memo):
      memo = 'WORLD SCIENTIFIC'

    if re.match('AMAZON.COM SEATTLE WA.+', memo):
      memo = 'AMAZON'

    memos[memo] = None

  # debug cleaned df @ checking
  # if re.match('.+checking', filename): st()

  # get unique categories
  print(df['Memo'].unique())
  st()
