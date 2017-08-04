from pdb import set_trace as st
from pprint import pprint as pp
from os.path import expanduser
from itertools import groupby
import datetime as dt
import csv
import re

HOME = expanduser("~")
FILENAME = '%s/Desktop/banking/one_year.csv' % HOME
LOCATION_REGEX = 'Check Card: |SQ \*|  (\d{2}\/?)+Card \d+ #\d+|Card \d+ #\d+'
LIKELY_RENT_REGEX = 'Guadalupe CU|CU ANYTIME|Century Bank'

class bank:
  def __init__(self):
    self.rows = self.get_data()

    self.daily_spent = self.end_of_day_spent()
    self.weekly_spent = self.end_of_week_spent()

    self.daily_balance = self.end_of_day_balance()
    self.weekly_balance = self.end_of_week_balance()

  def string_to_date(self, date_str):
    month, day, year = map(lambda x: int(x), date_str.split('/'))
    return(dt.date(year, month, day))

  def get_data(self):
    rows = []
    with open(FILENAME) as csvfile:
      banking = csv.reader(csvfile, delimiter=',')
      for row in banking:
        date = self.string_to_date(row[0])
        location = re.sub(LOCATION_REGEX,'',row[1])
        debit = float(re.sub('\$','',row[2]))    
        balance = float(re.sub('\$','',row[3])) 

        clean_row = [date, location, debit, balance]
        rows.append(clean_row)
    return(rows)

  def likely_rent(self, row):
    if re.search(LIKELY_RENT_REGEX, row[1]): return(True) 

  def end_of_day_spent(self):
    spents = []
    for key, group in groupby(self.rows, lambda x: x[0]):
      spent = 0
      for row in group:
        if not self.likely_rent(row) and row[2] < 0:
          spent += row[2]
      spents.append((key, spent))
    return(spents)

  def end_of_week_spent(self):
    spents = self.daily_spent
    spent_by_week = []
    while spents:
      week_spent = spents[0:7]
      week_total = 0
      date = week_spent[0][0]
      for date, spent in week_spent:
        week_total += spent
      clean_total = round(week_total,2)
      spent_by_week.append((date, clean_total))
      spents = spents[7:]
    return(spent_by_week)

  def end_of_day_balance(self):
    balances = []
    for key, group in groupby(self.rows, lambda x: x[0]):
      balances.append((key, list(group)[0][-1]))
    return(balances)

  def end_of_week_balance(self):
    return(self.daily_balance[0::7])

# bb = bank()
# st()
