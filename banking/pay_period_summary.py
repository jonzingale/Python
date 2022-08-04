# This module exists to partition banking data into
# sections based on pay period.

import pandas as pd
from os.path import expanduser
from pdb import set_trace as st
from pprint import pprint as pp

# TODO:
# 1. method given month/year returns summary object
# 2. summary object methods, visualizer

HOME = expanduser("~/Desktop/banking/GCU")
HISTORICAL_CSV = '%s/historical_2020.csv' % HOME
# HISTORICAL_CSV = '%s/last_pay_period.csv' % HOME

DATE_FIELDS = ['Effective Date', 'Posted']
CATEGORIES = ["Paycheck","Beer","Grocery","Book","Coffee","Bill","Video",
	"Restaurant","Child Care","Art","CVS","Music","Gas","Reimbursement",
	"Entertainment","Parking","Bodywork","Other","Not Labeled","Taxes"]

HEADER = ["Account Number","Type","Posted","Effective Date","Transfer ID",
  "Description","Memo","Amount","Ending Balance","Category"]

data = pd.read_csv(HISTORICAL_CSV, parse_dates=DATE_FIELDS)

# get unique categories
def categories():
	for b in data['Category'].unique():
		print(b)

# get paycheck periods
def periods():
	# group by Paycheck
	grouped = data.groupby(data['Category'])
	# get indices of Paychecks
	paycheck_idxs = grouped.get_group('Paycheck').index

	# cleverly zip and slice
	ps = []
	(head,*tail) = paycheck_idxs
	zipped = zip(paycheck_idxs, tail)
	for (x,y) in zipped:
		ps.append(data.iloc[x:y])

	return(ps)

def totals(df):
	totals = {}
	for cat in CATEGORIES:
		totals[cat] = 0
		for row in df.iterrows():
			if row[1]['Category'] == cat:
				amount = row[1]["Amount"]
				totals[cat] += float(amount)
	totals['_Delta'] = sum(df['Amount'])
	return(totals)

def main():
	ps = periods()
	for period in periods():
		p = pd.DataFrame(period, columns=HEADER)
		pp(totals(p))

	pp([totals(p)["_Delta"] for p in periods()])

main()