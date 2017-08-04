# Parse new bank csvs and merge with historical.
from pdb import set_trace as st
from os.path import expanduser
from itertools import *
import datetime as dt
import csv
import re
import os

HOME = expanduser("~")
HISTORICAL_CSV = '%s/Desktop/banking/one_year.csv' % HOME
NEW_CSV_PATH = './../../../banking/'
CSV_REGEX = 'History-(\d+)-\d+'

class bank_csv:
  def __init__(self):
    self.rows = self.get_data()
    self.last_date = self.string_to_date(self.rows[0][0])
    self.newest_csv = self.most_recent_csv()
    if self.newest_csv: self.merge_new_into_old()

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

      # save the merged files.
      with open(HISTORICAL_CSV, 'w') as csvfile:
          writer = csv.writer(csvfile)
          writer.writerows(self.rows)

  def get_data(self):
    with open(HISTORICAL_CSV) as csvfile:
      banking = csv.reader(csvfile, delimiter=',')
      rows = [row for row in banking]
    return(rows)

bank_csv()
