from pdb import set_trace as st
from os.path import expanduser
import datetime as dt
import csv
import re

home = expanduser("~")

FILENAME = '%s/Desktop/banking/one_year.csv' % home
LOCATION_REGEX = 'Check Card: |SQ \*|  (\d{2}\/?)+Card \d+ #\d+|Card \d+ #\d+'

class bank:
  def __init__(self):
    self.rows = self.get_data()
    self.weekly_spent = self.spent_per_week()
    self.daily_spent = self.spent_per_day()
    self.weekly_balance = self.balance_per_week()
    self.daily_balance = self.balance_per_day()

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

  def rows_for_dates(self, start_date, end_date):
    delta = start_date - end_date
    date_list = []
    for i in range(delta.days):
      date_list.append(start_date - dt.timedelta(days=i))
    return(date_list)

  def spent_between_dates(self, start_date, end_date):
    dates = self.rows_for_dates(start_date, end_date)
    total = 0

    for row in self.rows:
      if row[0] in dates and row[2] < 0 and not self.likely_rent(row):
        total += row[2]
    return(round(total,2))

  # average balance between days.
  def balance_between_dates(self, start_date, end_date):
    dates = self.rows_for_dates(start_date, end_date)
    total, row_count = 0, 0

    for row in self.rows:
      if row[0] in dates:
        row_count += 1
        total += row[3]
    return(round(total/row_count, 2))

  def likely_rent(self, row):
    if re.search('Guadalupe CU|CU ANYTIME|Century Bank', row[1]): return(True) 

  def balance_per_day(self):
    daily_balance = []
    for row in self.rows:
      daily_balance.append((row[0], row[3]))
    return(daily_balance)

  def balance_per_week(self):
    inc_date = self.rows[0][0]
    furthest_date = self.rows[-1][0]

    weekly_balance = []
    while (inc_date - furthest_date).days > 7:
      end_date = inc_date - dt.timedelta(days=7)
      balance = self.balance_between_dates(inc_date, end_date)
      weekly_balance.append((inc_date, balance))
      inc_date = end_date
    return(weekly_balance)

  def spent_per_day(self):
    daily_spent = []
    for row in self.rows:
      if row[2] < 0 and not self.likely_rent(row):
        daily_spent.append((row[0], row[2]))
    return(daily_spent)

  def spent_per_week(self):
    inc_date = self.rows[0][0]
    furthest_date = self.rows[-1][0]

    weekly_spent = []
    while (inc_date - furthest_date).days > 7:
      end_date = inc_date - dt.timedelta(days=7)
      spent = self.spent_between_dates(inc_date, end_date)
      weekly_spent.append((inc_date, spent))
      inc_date = end_date
    return(weekly_spent)

  def pp_weekly_spent(self):
    for pair in self.spent:
      print("Week of %s: %s" % (inc_date, spent))

  def pp_rows(self):
    for row in bb.rows: print(row)

# bb = bank()
# bb.pp_rows()
# st()
