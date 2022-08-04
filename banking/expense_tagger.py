# This is an interactive module for tagging expenses.
import pandas as pd
from memos_and_categories import kv_categories
from os.path import expanduser
from pdb import set_trace as st
from pprint import pprint as pp
import shutil
import re

HOME = expanduser("~/Desktop/banking/GCU")
HISTORICAL_CSV = '%s/historical_2020.csv' % HOME
# TAGGED_CSV = '%s/last_pay_period.csv' % HOME
CSV_TMP = '%s/historical_2020_tmp.csv' % HOME

UNIDENTIFIED = 'Not Labeled'
DATE_FIELDS = ['Effective Date', 'Posted']
CATEGORIES = ["Paycheck","Beer","Grocery","Book","Coffee","Bill","Video",
	"Restaurant","Child Care","Art","CVS","Music","Gas","Reimbursement",
	"Entertainment","Parking","Bodywork","Other","Clothing","Taxes"]

HEADER = ["Account Number","Type","Posted","Effective Date","Transfer ID",
	"Description","Memo","Amount","Ending Balance","Category"]

def get_nones(df):
	nones = [r for r in df.iterrows() if r[1]['Category'] == UNIDENTIFIED]
	nones_df = pd.DataFrame([x for i,x in nones], columns=HEADER)
	# pp [r[1]['Memo'] for r in nones_df]
	pp(nones_df['Memo'].unique())

def to_currency(maybeStr):
	if isinstance(maybeStr, str):
		maybeStr = maybeStr.replace(',','')
	return(float(maybeStr))

# TODO:
# Make module a function of dataset rather than hard-coded CSV
# convert currencies early

# 0. initialize data, make backup
shutil.copyfile(HISTORICAL_CSV, CSV_TMP)
untagged_data = pd.read_csv(HISTORICAL_CSV, parse_dates=DATE_FIELDS)

# 1. make category column with None values
if 'Category' not in untagged_data.columns:
	untagged_data['Category'] = [UNIDENTIFIED for i in untagged_data.iterrows()]
data = untagged_data

# 2. compare untagged csv to dictionary or known values
categories = []
for row in untagged_data.iterrows():
	if row[1]['Category'] == UNIDENTIFIED:
		row_memo = row[1]['Memo']
		cond1 = row_memo in kv_categories.keys() and kv_categories[row_memo]
		cond2 = re.match('CHECK NO. d*', row[1]['Description'], re.IGNORECASE)
		cond3 = row[1]['Amount'] == "-1,300.00"
		cond4 = abs(to_currency(row[1]['Amount'])) < 1000
		if cond1: # known dictionary
			categories.append(cond2)
		elif cond2 and cond3: # rent
			categories.append('Bill')
		elif cond2 and cond4: # likely child care
			categories.append('Child Care')
		else: # mark as unidentified
			categories.append(UNIDENTIFIED)
	else: # pass through category
		categories.append(row[1]['Category'])

data['Category'] = categories

# convert Amount to float
# df_new['Amount'].transform(lambda x: float(x))

# save with new data
data.to_csv(HISTORICAL_CSV, index=False)

# 3. hand tag with client
