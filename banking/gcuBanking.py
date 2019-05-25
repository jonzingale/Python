from pdb import set_trace as st
from pprint import pprint as pp
from os.path import expanduser
from itertools import groupby
import datetime as dt
import csv
import re

HOME = expanduser("~")

# FILENAME = '%s/Desktop/banking/GCU/savings_Jan19_May19.csv' % HOME
FILENAME = '%s/Desktop/banking/GCU/checking_Jan19_May19.csv' % HOME

HEADERS = ['Account Number', 'Type', 'Posted', 'Effective Date',
           'Transfer ID', 'Description', 'Memo', 'Amount', 'Ending Balance']

class bank:
  def __init__(self):
    self.rows = self.get_data()

    self.daily_spent = self.end_of_day_debit()
    self.daily_credit = self.end_of_day_credit()
    self.weekly_debit = self.end_of_week_debit()

    self.daily_balance = self.end_of_day_balance()
    self.weekly_balance = self.end_of_week_balance()

  def parseCurrency(self, string):
    currency = float(re.sub('\$?','', string).replace(',',''))
    return(currency)

  def get_data(self, rows=[], data={}):
    with open(FILENAME) as csvfile:
      banking = csv.reader(csvfile, delimiter=',')
      next(banking, None)

      for row in banking:
        date = row[3] # effective date 0
        data[date] = {'debit': 0, 'credit': 0, 'balance': 0}
        rows.append(row)

      for row in rows:
        debit = self.parseCurrency(row[7])
        balance = self.parseCurrency(row[8])

        if (debit < 0): # remove credits
          data[row[3]]['debit'] += debit

        if (debit > 0): # remove credits
          data[row[3]]['credit'] += debit

        data[row[3]]['balance'] = balance
    return(data)

  def end_of_day_debit(self):
    spents = [ -v['debit'] for v in self.rows.values()]
    return(spents)

  def end_of_day_credit(self):
    spents = [ v['credit'] for v in self.rows.values()]
    return(spents)

  def end_of_day_balance(self):
    balances = [ v['balance'] for v in self.rows.values()]
    return(balances)

  def end_of_week_debit(self):
    return(self.daily_spent[0::7])

  def end_of_week_balance(self):
    return(self.daily_balance[0::7])

bb = bank()
pp(bb.end_of_week_debit())
# st()