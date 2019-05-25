import matplotlib.pyplot as plt
from pdb import set_trace as st
import gcuBanking

bb = gcuBanking.bank()
fig = plt.figure(figsize=(17, 8))

def banking_chart(data):
  plt.plot(range(len(data)), data)#, 'ro')
  plt.show()

# banking_chart(bb.daily_debit)
# banking_chart(bb.daily_balance)
# banking_chart(bb.daily_credit)

banking_chart(bb.weekly_debit)
# banking_chart(bb.weekly_balance)

plt.show()

