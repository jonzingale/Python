from pdb import set_trace as st
import datetime as dt
import csv
import re

FILENAME = './../../banking/one_year.csv'
LOCATION_REGEX = 'Check Card: |SQ \*|  (\d{2}\/?)+Card \d+ #\d+|Card \d+ #\d+'

class bank:
  def __init__(self):
    self.get_data()
    self.spent_per_week()
    self.spent_per_day()

  def string_to_date(self, date_str):
    month, day, year = map(lambda x: int(x), date_str.split('/'))
    return(dt.date(year, month, day))

  def get_data(self):
    self.rows = []
    with open(FILENAME) as csvfile:
      banking = csv.reader(csvfile, delimiter=',')
      for row in banking:
        date = self.string_to_date(row[0])
        location = re.sub(LOCATION_REGEX,'',row[1])
        debit = float(re.sub('\$','',row[2]))    
        balance = float(re.sub('\$','',row[3])) 

        clean_row = [date, location, debit, balance]
        self.rows.append(clean_row)

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
    return([row, round(total,2)])

  def likely_rent(self, row):
    if re.search('Guadalupe CU|CU ANYTIME|Century Bank', row[1]): return(True) 

  def spent_per_day(self):
    self.daily_spent = []
    for row in self.rows:
      if row[2] < 0 and not self.likely_rent(row):
        self.daily_spent.append((row[0], row[2]))

  def spent_per_week(self):
    inc_date = self.rows[0][0]
    furthest_date = self.rows[-1][0]

    self.weekly_spent = []
    while (inc_date - furthest_date).days > 7:
      end_date = inc_date - dt.timedelta(days=7)
      row, spent = self.spent_between_dates(inc_date, end_date)
      self.weekly_spent.append((inc_date, spent))
      inc_date = end_date

  def pp_weekly_spent(self):
    for pair in self.spent:
      print("Week of %s: %s" % (inc_date, spent))

  def pp_rows(self):
    for row in bb.rows: print(row)

# bb = bank()
# bb.pp_rows()
# st()
