import matplotlib.pyplot as plt
from pdb import set_trace as st
import gcuBanking

bb = gcuBanking.bank()
fig = plt.figure(figsize=(17, 8))

def banking_chart(data1=[], data2=[]):
  plt.plot(range(len(data1)), data1, 'b')
  plt.plot(range(len(data2)), data2, 'g')
  plt.show()

# banking_chart(bb.daily_balance(), bb.daily_debit())
banking_chart(bb.weekly_balance(), bb.weekly_debit())

plt.show()

# methods:
# daily_debit
# daily_credit
# daily_balance

# weekly_debit
# weekly_credit
# weekly_balance

# total_debit
# total_balance
