# This is an interactive module for tagging expenses.
import pandas as pd
from memos_and_categories import kv_categories
from numpy import isin
from os.path import expanduser
from pdb import set_trace as st
from pprint import pprint as pp
import re

HOME = expanduser("~/Desktop/banking/GCU")
UNTAGGED_CSV = '%s/historical_2020.csv' % HOME
TAGGED_CSV = '%s/last_pay_period.csv' % HOME
CSV_TMP = '%s/historical_2020.csv' % HOME

UNIDENTIFIED = 'Not Labeled'
DATE_FIELDS = ['Effective Date', 'Posted']
CATEGORIES = ["Paycheck","Beer","Grocery","Book","Coffee","Bill","Video",
	"Restaurant","Child Care","Art","CVS","Music","IFAM","Gas","Reimbursement",
	"Zoo","Parking","Bodywork","Other","Clothing","Taxes"]

HEADER = ["Account Number","Type","Posted","Effective Date","Transfer ID",
	"Description","Memo","Amount","Ending Balance","Category"]

def get_nones(df):
	nones = [r for r in df.iterrows() if r[1]['Category'] == UNIDENTIFIED]
	nones_df = pd.DataFrame([x for i,x in nones], columns=HEADER)
	# pp [r[1]['Memo'] for r in nones_df]
	pp(nones_df['Memo'].unique())

# TODO: Don't overwrite data

# 0. make category column with None values
untagged_data = pd.read_csv(UNTAGGED_CSV, parse_dates=DATE_FIELDS)
untagged_data['Category'] = [UNIDENTIFIED for i in untagged_data.iterrows()]
data = untagged_data

# 1. compare untagged csv to a tagged csv, None for unknowns
tagged_data = pd.read_csv(TAGGED_CSV, parse_dates=DATE_FIELDS)
tagged_memos = tagged_data['Memo'].unique()

categories = []
for row in untagged_data.iterrows():
	row_memo = row[1]['Memo']
	cond = row_memo in tagged_memos
	cond2 = row_memo in kv_categories.keys() and kv_categories[row_memo]
	cond3 = re.match('CHECK NO. d*', row[1]['Description'], re.IGNORECASE)
	cond4 = row[1]['Amount'] == "-1,300.00"
	if cond:
		label = row_memo
		vals = tagged_data.query('Memo == @label')
		cat = vals.head(1)['Category'].values[0]
		categories.append(cat)
	elif cond2:
		categories.append(cond2)
	elif cond3 and cond4:
		categories.append('Bill')
	else:
		categories.append(UNIDENTIFIED)

data['Category'] = categories

# convert Amount to float
# df_new['Amount'].transform(lambda x: float(x))

# save with new data
data.to_csv(CSV_TMP, index=False)

# 2. hand tag with client
