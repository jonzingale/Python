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
# HISTORICAL_CSV = '%s/historical_2020.csv' % HOME
HISTORICAL_CSV = '%s/last_pay_period.csv' % HOME

DATE_FIELDS = ['Effective Date', 'Posted']
CATEGORIES = ["Paycheck","Beer","Grocery","Book","Coffee","Bill","Video",
	"Restaurant","Child Care","Art","CVS","Music","IFAM","Gas","Reimbursement",
	"Zoo","Parking","Bodywork","Other"]

data = pd.read_csv(HISTORICAL_CSV, parse_dates=DATE_FIELDS)

# get unique categories
def categories():
	for b in data['Category'].unique():
		print(b)

payroll = []
for row in data.iterrows():
	if row[1]['Memo'] == 'OPENEYE SCIENTIF/DIRECT DEP':
		payroll.append(row)

totals = {}
for cat in CATEGORIES:
	totals[cat] = 0
	for row in data.iterrows():
		if row[1]['Category'] == cat:
			amount = row[1]["Amount"]
			if isinstance(amount, str):
				amount = amount.replace(',','')
			totals[cat] += float(amount)

monthly_diff = data['Amount'].sum()

def main():
	pp(totals)
	pp(monthly_diff)

main()
# st()