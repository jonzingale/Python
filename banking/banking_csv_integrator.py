# Parse new bank csvs and merge with historical.
from pdb import set_trace as st
from os.path import expanduser
from itertools import *
import datetime as dt
import pandas as pd
import csv
import re
import os

# TODO:
# 1. Add categories column.

HOME = expanduser("~")
HISTORICAL_CSV = '%s/Desktop/banking/GCU/historical_2020.csv' % HOME
NEW_CSV_PATH = './../../../banking/GCU/gcu_histories/'
HEADER = ["Account Number","Type","Posted","Effective Date","Transfer ID",
  "Description","Memo","Amount","Ending Balance"]
HEADER2 = ["Index"].append(HEADER)
CSV_REGEX = '(\d+)-\d+'

class bank_csv:
  def __init__(self):
    self.historical = self.get_historical_data()
    self.last_date = pd.to_datetime(self.historical['Effective Date'].array[-1])
    self.newest_csv = self.most_recent_csv()
    if self.newest_csv: self.merge_new_into_old()

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
    csv = pd.read_csv(NEW_CSV_PATH + self.newest_csv, header='infer',
      parse_dates=['Effective Date', 'Posted'])

    rows = []
    for row in csv.iterrows():
      if row[1][3] > self.last_date:
        rows.append(row[1])

    new_csv = pd.DataFrame(rows, columns=HEADER)
    new_historical = pd.concat([self.historical, new_csv], ignore_index=True)
    # print(new_historical['Effective Date'])

    # save the merged files.
    new_historical.to_csv(HISTORICAL_CSV, index=False)

  def get_historical_data(self):
    csv = pd.read_csv(HISTORICAL_CSV, header='infer',
      parse_dates=['Effective Date', 'Posted'])
    return(csv)

bank_csv()
