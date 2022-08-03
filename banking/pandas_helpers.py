import pandas as pd
from os.path import expanduser
from pdb import set_trace as st
from pprint import pprint as pp

HOME = expanduser("~/Desktop/banking/GCU")
HISTORICAL_CSV = '%s/historical_2020.csv' % HOME
DATE_FIELDS = ['Effective Date', 'Posted']

df = pd.read_csv(HISTORICAL_CSV, parse_dates=DATE_FIELDS)

grouped = df.groupby(df['Category'])
df_new = grouped.get_group('Paycheck')

# df_new['Amount'].transform(lambda x: float(x)) # :: Series

df_new['Amount'].index
df.iloc[501:738] # between paychecks
