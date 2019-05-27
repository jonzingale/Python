from pdb import set_trace as st
from pprint import pprint as pp
from os.path import expanduser
import datetime as dt
import pandas as pd
from personal import *
import csv
import re

REL_PATH = expanduser("~/Desktop/banking/GCU")

SAVINGS = '%s/savings_Jan19_May19.csv' % REL_PATH
CHECKING = '%s/checking_Jan19_May19.csv' % REL_PATH

HEADERS = ['Account Number', 'Type', 'Posted', 'Effective Date',
           'Transfer ID', 'Description', 'Memo', 'Amount', 'Ending Balance']

class account:
  def __init__(self, filename):
    self.data = {}
    self.parseDATA(filename)
    pandaData(filename)

  def parseCurrency(self, string):
    currency = float(re.sub('\$?','', string).replace(',',''))
    return(currency)

  def parseDate(self, date_str):
    month, day, year = map(lambda x: int(x), date_str.split('/'))
    return(dt.date(year, month, day))

  def parseDATA(self, filename, data={}, rows=[]):
    with open(filename) as csvfile:
      banking = csv.reader(csvfile, delimiter=',')
      next(banking, None)

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
        # update instead of equals, otherwise shares
        # data between savings and checking objects :(
        self.data.update(data)

class bank:
  def __init__(self):
    self.total_data = {}
    self.checking = account(CHECKING)
    self.savings = account(SAVINGS)
    self.get_total_data()

  def get_total_data(self, data={}, rows=[]):
    checking = self.checking.data
    savings = self.savings.data

    # till transfers are worked out credit
    # and debit are the same
    for key in checking.keys():
      data[key] = {'debit': 0, 'balance': 0}

    for key in savings.keys():
      data[key]['debit'] += savings[key]['debit']
      data[key]['debit'] += savings[key]['credit']
      data[key]['balance'] += savings[key]['balance']
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
    for i in range(len(self.daily_debit)//7):
      val = sum(self.daily_debit[i*7:(i+1)*7])
      tots.append(val)
    return(tots)

  def weekly_credit(self, tots=[]):
    for i in range(len(self.daily_credit)//7):
      val = sum(self.daily_credit[i*7:(i+1)*7])
      tots.append(val)
    return(tots)

  def weekly_balance(self):
    return(self.daily_balance[0::7])

  def total_debit(self):
    debits = [ -v['debit'] for v in self.total_data.values()]
    return(debits)

  def total_balance(self):
    balances = [ -v['balance'] for v in self.total_data.values()]
    return(balances)

  def average_weekly_debit(self):
    num = sum(self.weekly_debit())
    div = len(self.weekly_debit())
    return(num/div)

  def average_total_daily_debit(self):
    num = sum(self.total_debit())
    div = len(self.total_debit())
    return(num/div)

  def average_daily_debit(self):
    num = sum(self.daily_debit())
    div = len(self.daily_debit())
    return(num/div)

  def average_weekly_credit(self):
    num = sum(self.weekly_credit())
    div = len(self.weekly_credit())
    return(num/div)

bb = bank()
