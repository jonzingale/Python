from pdb import set_trace as st
from itertools import *
import datetime as dt
import csv
import re

import banking
import os

# the idea here is to structure incoming csvs
# to match the format of the master csv.

# Is there a good way to merge the two csvs
# without converting to an array first?
# bash would likely be straightforward.

HISTORICAL_CSV = './../../../banking/one_year.csv'
NEW_CSV_PATH = './../../../banking/'
CSV_REGEX = 'History-(\d+)-\d+'

# TODO: save updated csv to new file.

class bank_csv:
  def __init__(self):
    self.rows = self.get_data()
    self.last_date = self.string_to_date(self.rows[0][0])
    self.newest_csv = self.most_recent_csv()
    self.merge_new_into_old()

  def string_to_date(self, date_str):
    month, day, year = map(lambda x: int(x), date_str.split('/'))
    return(dt.date(year, month, day))

  def most_recent_csv(self):
    most_recent_date, most_recent = self.last_date, None

    for root, dir, files in os.walk(NEW_CSV_PATH):
      for file in files:
        date_match = re.match(CSV_REGEX,file)
        if date_match:
          month, day, yr = re.findall('\d{2}', date_match[1])
          date = dt.date(2000 + int(yr), int(month), int(day))
          if not most_recent or (date - most_recent_date).days > 0:
            most_recent_date = date
            most_recent = file
    return(most_recent)

  def merge_new_into_old(self):
    with open(NEW_CSV_PATH + self.newest_csv) as csvfile:
      banking = csv.reader(csvfile, delimiter=',')
      rows = [row for row in banking]
      recents = takewhile(lambda x: self.string_to_date(x[0]) > self.last_date, rows)
      self.rows = list(recents) + self.rows

  def get_data(self):
    with open(HISTORICAL_CSV) as csvfile:
      banking = csv.reader(csvfile, delimiter=',')
      rows = [row for row in banking]
    return(rows)

it = bank_csv()
merged = it.rows
st()