# Parse new bank csvs and merge with historical csv.
from pdb import set_trace as st
from os.path import expanduser
import datetime as dt
import pandas as pd
import re
import os

# TODO:
# 1. Add categories column.

HOME = expanduser("~/Desktop/banking/GCU")
HISTORICAL_CSV = '%s/historical.csv' % HOME
NEW_CSV_PATH = '%s/gcu_histories/' % HOME

DATE_FIELDS = ['Effective Date', 'Posted']
HEADER = ["Account Number","Type","Posted","Effective Date","Transfer ID",
  "Description","Memo","Amount","Ending Balance"]

CSV_REGEX = '(\d+)-\d+'

def most_recent_csv():
  most_recent_date = last_date
  most_recent = None

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

def merge_new_into_old():
  csv = pd.read_csv(NEW_CSV_PATH + newest_csv, parse_dates=DATE_FIELDS)
  rows = []
  for row in csv.iterrows():
    if row[1][3] > last_date: rows.append(row[1])

  new_csv = pd.DataFrame(rows, columns=HEADER)
  new_historical = pd.concat([historical, new_csv], ignore_index=True)

  # save the merged files.
  new_historical.to_csv(HISTORICAL_CSV, index=False)

# Main
historical = pd.read_csv(HISTORICAL_CSV, parse_dates=DATE_FIELDS)
last_date = pd.to_datetime(historical['Effective Date'].array[-1])
newest_csv = most_recent_csv()

if newest_csv: merge_new_into_old()
