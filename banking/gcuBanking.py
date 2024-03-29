from pdb import set_trace as st
from pprint import pprint as pp
from os.path import expanduser
import pandas as pd
import csv
import re

REL_PATH = expanduser("~/Desktop/banking/GCU")
CHECKING = '%s/historical.csv' % REL_PATH

class account:
  def __init__(self, filename):
    self.data = {}
    self.parseDATA(filename)

  def parseCurrency(self, string):
    currency = float(re.sub('\$?','', string).replace(',',''))
    return(currency)

  def parseDate(self, date_str):
    pddt = pd.to_datetime(date_str)
    return(pddt)

  def parseDATA(self, filename, data={}, rows=[]):
    with open(filename) as csvfile:
      banking = csv.reader(csvfile, delimiter=',')
      next(banking, None) # remove header

      for row in banking:
        dateKey = self.parseDate(row[3])
        data[dateKey] = {'debit': 0, 'credit': 0, 'balance': 0}
        rows.append(row)

      for row in rows:
        dateKey = self.parseDate(row[3])
        debit = self.parseCurrency(row[7])
        balance = self.parseCurrency(row[8])

        if (debit < 0): # remove credits
          data[dateKey]['debit'] += debit

        if (debit > 0): # remove credits
          data[dateKey]['credit'] += debit

        data[dateKey]['balance'] = balance
        self.data.update(data)

class bank:
  def __init__(self):
    self.total_data = {}
    self.checking = account(CHECKING)
    self.get_total_data()

  def get_total_data(self, data={}, rows=[]):
    checking = self.checking.data

    # until transfers are worked out credit
    # and debit are the same
    for key in checking.keys():
      data[key] = {'debit': 0, 'balance': 0}

    self.total_data.update(data)

  def daily_debit(self):
    spents = [ -v['debit'] for v in self.checking.data.values()]
    return(spents)

  def daily_credit(self):
    spents = [ v['credit'] for v in self.checking.data.values()]
    return(spents)

  def daily_balance(self):
    balances = [ v['balance'] for v in self.checking.data.values()]
    return(balances)

  def weekly_debit(self, tots=[]):
    dd = self.daily_debit()
    for i in range(len(dd)//7):
      val = sum(dd[i*7:(i+1)*7])
      tots.append(val)
    return(tots)

  def weekly_credit(self, tots=[]):
    dc = self.daily_credit()
    for i in range(len(dc)//7):
      val = sum(dc[i*7:(i+1)*7])
      tots.append(val)
    return(tots)

  def weekly_balance(self):
    dailybal = self.daily_balance()
    return(dailybal[0::7])

  def total_debit(self):
    debits = [ -v['debit'] for v in self.total_data.values()]
    return(debits)

  def total_balance(self):
    balances = [ -v['balance'] for v in self.total_data.values()]
    return(balances)

bb = bank()
